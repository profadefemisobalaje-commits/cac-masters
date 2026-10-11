#!/usr/bin/env python3
"""Serve the lecture media over HTTP with a browser video gallery.

    python3 tools/serve_media.py [--port 8080]

Why a custom handler rather than `python -m http.server`:

* **Range requests.** Browsers require HTTP 206 partial-content responses to
  play and seek within video. SimpleHTTPRequestHandler ignores the Range
  header, so players either refuse to start or cannot scrub. This implements
  Range properly, which is the difference between a working preview and a
  broken one.
* **Embedding.** It sends no X-Frame-Options and no restrictive CSP, so the
  page renders inside the platform's preview iframe.
* **Bind address.** Binds 0.0.0.0 so the port is reachable through the preview
  proxy rather than only from inside the sandbox.
"""
from __future__ import annotations
import argparse
import html
import mimetypes
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.course import ROOT, MEDIA, branding

BRAND = branding()
RANGE_RE = re.compile(r"bytes=(\d*)-(\d*)")

MIME = {
    ".mp4": "video/mp4", ".webm": "video/webm", ".m4v": "video/mp4",
    ".mp3": "audio/mpeg", ".m4a": "audio/mp4", ".wav": "audio/wav",
    ".vtt": "text/vtt", ".txt": "text/plain; charset=utf-8",
    ".png": "image/png", ".jpg": "image/jpeg", ".pptx":
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".json": "application/json",
}


def human(n: int) -> str:
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {u}" if u != "B" else f"{n} {u}"
        n /= 1024
    return f"{n:.1f} TB"


def probe_duration(path: str) -> str:
    """Read the duration line ffmpeg prints when opening the file."""
    from lib.video import FFMPEG
    import subprocess
    try:
        r = subprocess.run([FFMPEG, "-hide_banner", "-i", path],
                           capture_output=True, text=True)
        m = re.search(r"Duration: (\d+):(\d\d):(\d\d)", r.stderr)
        if m:
            return f"{m.group(1)}:{m.group(2)}:{m.group(3)}"
    except Exception:
        pass
    return ""


def resolution(path: str) -> str:
    from lib.video import FFMPEG
    import subprocess
    try:
        r = subprocess.run([FFMPEG, "-hide_banner", "-i", path],
                           capture_output=True, text=True)
        m = re.search(r"Video:.*?(\d{3,4})x(\d{3,4})", r.stderr)
        if m:
            return f"{m.group(1)}×{m.group(2)}"
    except Exception:
        pass
    return ""


def collect_videos() -> list[dict]:
    """Every .mp4 under media/, newest lecture first, with metadata."""
    out = []
    if not os.path.isdir(MEDIA):
        return out
    for r, dirs, files in os.walk(MEDIA):
        dirs[:] = [d for d in dirs if not d.startswith("work")]
        for f in sorted(files):
            if not f.lower().endswith((".mp4", ".webm")):
                continue
            p = os.path.join(r, f)
            rel = os.path.relpath(p, MEDIA)
            out.append({
                "path": p, "rel": rel.replace(os.sep, "/"),
                "name": f, "size": os.path.getsize(p),
                "slug": os.path.basename(os.path.dirname(p)),
                "duration": probe_duration(p),
                "resolution": resolution(p),
                "kind": ("preview" if "PREVIEW" in f
                         else "compact" if "COMPACT" in f else "master"),
            })
    order = {"master": 0, "compact": 1, "preview": 2}
    out.sort(key=lambda v: (v["slug"], order.get(v["kind"], 9)))
    return out


def gallery_html() -> str:
    videos = collect_videos()
    rows = []
    for v in videos:
        q = html.escape
        badge = {"master": "Master · 1080p", "compact": "Compact · 540p",
                 "preview": "Short preview"}[v["kind"]]
        rows.append(f"""
    <section class="card">
      <header>
        <h2>{q(v['slug'])} <span class="badge {v['kind']}">{q(badge)}</span></h2>
        <p class="meta">{q(v['name'])} &middot; {human(v['size'])}
           {('&middot; ' + q(v['duration'])) if v['duration'] else ''}
           {('&middot; ' + q(v['resolution'])) if v['resolution'] else ''}</p>
      </header>
      <video controls preload="metadata" playsinline
             src="{q(v['rel'])}"></video>
      <p class="actions">
        <a class="btn" href="{q(v['rel'])}" download>Download</a>
        <a class="btn ghost" href="{q(v['rel'])}" target="_blank">Open full screen</a>
      </p>
    </section>""")

    if not videos:
        rows.append("<p class='empty'>No rendered video in media/ right now. "
                    "Build one with tools/build_lecture.py assemble.</p>")

    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lecture Videos — {html.escape(BRAND.get('programme',''))}</title>
<style>
  :root {{
    --ink:#0f2a44; --ink2:#0a1d2f; --accent:#0d9494; --gold:#d69e36;
    --paper:#f6f9fb; --rule:#dbe4eb; --text:#1c2733; --muted:#6a7a8a;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--paper); color:var(--text);
    font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  .top {{ background:linear-gradient(135deg,var(--ink),var(--ink2));
    color:#e8f0f7; padding:34px 28px 30px; border-bottom:4px solid var(--accent); }}
  .top .inst {{ font-size:13px; letter-spacing:.09em; text-transform:uppercase;
    color:var(--accent); font-weight:600; }}
  .top h1 {{ margin:8px 0 6px; font-size:27px; font-weight:700; letter-spacing:-.01em; }}
  .top p {{ margin:0; color:#9db6cc; font-size:14px; }}
  main {{ max-width:1000px; margin:0 auto; padding:26px 20px 70px; }}
  .card {{ background:#fff; border:1px solid var(--rule); border-radius:14px;
    padding:18px 18px 14px; margin:0 0 26px; box-shadow:0 1px 2px rgba(15,42,68,.05); }}
  .card h2 {{ margin:0 0 4px; font-size:18px; color:var(--ink); font-weight:700; }}
  .badge {{ font-size:11px; font-weight:700; letter-spacing:.05em; text-transform:uppercase;
    padding:3px 9px; border-radius:20px; vertical-align:middle; margin-left:8px; }}
  .badge.master {{ background:#e6f4f4; color:#0b6f6f; }}
  .badge.compact {{ background:#fdf3e0; color:#8a6413; }}
  .badge.preview {{ background:#eef1f5; color:#5a6b7c; }}
  .meta {{ margin:0 0 12px; color:var(--muted); font-size:13px; }}
  video {{ width:100%; aspect-ratio:16/9; background:#0a1d2f; border-radius:10px;
    display:block; }}
  .actions {{ margin:12px 0 2px; display:flex; gap:10px; flex-wrap:wrap; }}
  .btn {{ text-decoration:none; font-size:14px; font-weight:600; padding:9px 16px;
    border-radius:8px; background:var(--accent); color:#fff; }}
  .btn.ghost {{ background:#fff; color:var(--ink); border:1px solid var(--rule); }}
  .btn:hover {{ filter:brightness(1.06); }}
  .empty {{ padding:40px; text-align:center; color:var(--muted); }}
  footer {{ color:var(--muted); font-size:13px; text-align:center; padding:10px 20px 40px; }}
</style></head>
<body>
  <div class="top">
    <div class="inst">{html.escape(BRAND.get('institution',''))}</div>
    <h1>{html.escape(BRAND.get('programme',''))}</h1>
    <p>{html.escape(BRAND.get('lecturer',''))} &middot;
       {len(videos)} rendered video{'s' if len(videos) != 1 else ''} available</p>
  </div>
  <main>{''.join(rows)}</main>
  <footer>Served locally from the lecture build. Range requests supported, so
    seeking works in the player.</footer>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "LectureMedia/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    # ---------------------------------------------------------------- helpers
    def _send(self, code, ctype, body=None, length=None, extra=None, head=False):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-store")
        # deliberately no X-Frame-Options / restrictive CSP so the preview
        # iframe can embed this page
        if length is not None:
            self.send_header("Content-Length", str(length))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if body is not None and not head:
            self.wfile.write(body)

    def _resolve(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            return "__gallery__"
        rel = os.path.normpath(path.lstrip("/"))
        if rel.startswith("..") or os.path.isabs(rel):
            return None
        full = os.path.join(MEDIA, rel)
        return full if os.path.exists(full) else None

    # ---------------------------------------------------------------- verbs
    def do_HEAD(self):
        self._serve(head=True)

    def do_GET(self):
        self._serve(head=False)

    def _serve(self, head: bool):
        target = self._resolve()
        if target is None:
            self._send(404, "text/plain; charset=utf-8", b"Not found", 9, head=head)
            return
        if target == "__gallery__":
            body = gallery_html().encode("utf-8")
            self._send(200, "text/html; charset=utf-8", body, len(body), head=head)
            return

        size = os.path.getsize(target)
        ctype = MIME.get(os.path.splitext(target)[1].lower()) \
            or mimetypes.guess_type(target)[0] or "application/octet-stream"
        rng = self.headers.get("Range")

        if not rng:
            # a browser probing with HEAD should see the full length and
            # accept-ranges, which is what makes it offer a scrubber
            with open(target, "rb") as f:
                body = None if head else f.read()
            self._send(200, ctype, body, size, head=head)
            return

        m = RANGE_RE.match(rng.strip())
        if not m:
            self._send(416, "text/plain", b"Bad range", 9,
                       {"Content-Range": f"bytes */{size}"}, head=head)
            return
        start_s, end_s = m.groups()
        if start_s == "":                        # suffix range: last N bytes
            n = int(end_s or 0)
            start = max(0, size - n)
            end = size - 1
        else:
            start = int(start_s)
            end = int(end_s) if end_s else size - 1
        end = min(end, size - 1)
        if start > end or start >= size:
            self._send(416, "text/plain", b"Bad range", 9,
                       {"Content-Range": f"bytes */{size}"}, head=head)
            return
        length = end - start + 1
        with open(target, "rb") as f:
            f.seek(start)
            chunk = None if head else f.read(length)
        self._send(206, ctype, chunk, length,
                   {"Content-Range": f"bytes {start}-{end}/{size}"}, head=head)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--host", default="0.0.0.0")
    a = ap.parse_args()
    videos = collect_videos()
    print(f"serving {len(videos)} video(s) from {MEDIA}")
    for v in videos:
        print(f"  {human(v['size']):>9}  {v['rel']}")
    httpd = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"\nlistening on http://{a.host}:{a.port}/  (range requests enabled)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
