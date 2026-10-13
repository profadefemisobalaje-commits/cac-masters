"""
serve.py — Static server for the lecture library, with HTTP Range support.

    python tools/serve.py [--port 8000] [--host 0.0.0.0]

Routes
    /                 -> site/
    /video/<file>     -> videos/<file>        (MP4s, range-enabled, attachment on ?dl=1)
    /script/<file>    -> lectures/<file>    (markdown scripts)

Files this size need Range requests: without them a browser cannot seek
inside a 53 MB lecture or resume an interrupted download.

Courtesy: Triune Biblical University Global Extension, USA.
"""

from __future__ import annotations

import argparse
import html
import io
import json
import os
import re
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SITE = os.path.join(ROOT, "site")
DIST = os.path.join(ROOT, "videos")
LECTURES = os.path.join(ROOT, "lectures")

MIME = {
    ".mp4": "video/mp4",
    ".md": "text/markdown; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".srt": "application/x-subrip; charset=utf-8",
    ".vtt": "text/vtt; charset=utf-8",
}


def _nice_names() -> dict:
    """lecture-01.mp4 -> 'Lecture 01 - Title.mp4' for the download filename."""
    out = {}
    cdir = os.path.join(ROOT, "content")
    if not os.path.isdir(cdir):
        return out
    for fn in sorted(os.listdir(cdir)):
        m = re.match(r"lecture-(\d+)\.json$", fn)
        if not m:
            continue
        try:
            d = json.load(open(os.path.join(cdir, fn), encoding="utf-8"))
        except Exception:
            continue
        no = int(m.group(1))
        title = re.sub(r"[^\w\- ]+", "", d.get("title", "")).strip()
        title = re.sub(r"\s+", " ", title)
        out[f"lecture-{no:02d}.mp4"] = f"Lecture {no:02d} - {title}.mp4"
    return out


class Handler(SimpleHTTPRequestHandler):
    server_version = "LectureLibrary/1.0"
    # HTTP/1.1 rather than the library default of 1.0: preview proxies and
    # sandbox ingress layers routinely refuse or mis-frame 1.0 responses.
    protocol_version = "HTTP/1.1"
    nice: dict = {}

    # ---------------------------------------------------------------- paths
    def translate_path(self, path: str) -> str:
        p = path.split("?", 1)[0].split("#", 1)[0]
        if p == "/health":
            return os.path.join(SITE, "index.html")
        if p.startswith("/video/"):
            return os.path.join(DIST, os.path.basename(p[len("/video/"):]))
        if p.startswith("/script/"):
            return os.path.join(LECTURES, os.path.basename(p[len("/script/"):]))
        if p == "/" or p == "":
            p = "/index.html"
        if p.startswith("/"):
            p = p[1:]
        return os.path.join(SITE, p)

    def guess_type(self, path: str) -> str:
        ext = os.path.splitext(path)[1].lower()
        return MIME.get(ext, super().guess_type(path))

    # ------------------------------------------------------------- headers
    def _attachment_name(self) -> str | None:
        base = os.path.basename(self.path.split("?", 1)[0])
        return self.nice.get(base)

    def send_head(self):
        # Cheap liveness probe: proxy health checks must never pull 34 KB of
        # HTML or touch a 90 MB video.
        if self.path.split("?", 1)[0] == "/health":
            body = b"ok\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return None if self.command == "HEAD" else io.BytesIO(body)

        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        if not os.path.isfile(path):
            self.send_error(404, "File not found")
            return None

        query = self.path.split("?", 1)[1] if "?" in self.path else ""
        want_dl = "dl=1" in query or "download=1" in query

        size = os.path.getsize(path)
        rng = self.headers.get("Range")
        start, end = 0, size - 1
        status = 200

        if rng and rng.startswith("bytes="):
            spec = rng[6:].split(",")[0].strip()
            if "-" in spec:
                a, _, b = spec.partition("-")
                if a:
                    start = int(a)
                    end = int(b) if b else size - 1
                elif b:
                    start = max(0, size - int(b))
            if start >= size or start > end:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
            end = min(end, size - 1)
            status = 206

        length = end - start + 1
        self.send_response(status)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Length", str(length))
        self.send_header("Accept-Ranges", "bytes")
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        if want_dl:
            name = self._attachment_name() or os.path.basename(path)
            self.send_header("Content-Disposition",
                             f'attachment; filename="{name}"')
        self.send_header("Cache-Control", "public, max-age=3600")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        if self.command == "HEAD":
            return None
        f = open(path, "rb")
        f.seek(start)
        return _Limited(f, length)

    def end_headers(self):
        # Never advertise keep-alive on a 206 we stream by hand.
        self.send_header("Connection", "close")
        super().end_headers()

    # ------------------------------------------------------------- output
    def copyfile(self, source, outputfile):
        """Stream only `length` bytes, in chunks (53 MB files)."""
        try:
            remaining = getattr(source, "remaining", None)
            if remaining is None:
                return super().copyfile(source, outputfile)
            chunk = 1 << 18
            while remaining > 0:
                buf = source.read(min(chunk, remaining))
                if not buf:
                    break
                outputfile.write(buf)
                remaining -= len(buf)
        finally:
            try:
                source.close()
            except Exception:
                pass

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


class _Limited:
    """File wrapper that stops after `length` bytes."""

    def __init__(self, f, length):
        self.f = f
        self.remaining = length

    def read(self, n=-1):
        if self.remaining <= 0:
            return b""
        if n is None or n < 0:
            n = self.remaining
        data = self.f.read(min(n, self.remaining))
        self.remaining -= len(data)
        return data

    def close(self):
        try:
            self.f.close()
        except Exception:
            pass


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--dir", default=None, help="unused; routes are fixed")
    a = ap.parse_args()

    Handler.nice = _nice_names()
    h = partial(Handler, directory=SITE)
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    srv.daemon_threads = True
    print(f"Lecture library on http://{a.host}:{a.port}/", flush=True)
    print(f"  site    {SITE}", flush=True)
    print(f"  videos  {DIST}  ({Handler.nice and len(Handler.nice)} named)", flush=True)
    print(f"  scripts {LECTURES}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()
