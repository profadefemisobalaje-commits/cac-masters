#!/usr/bin/env python3
"""Range-capable static server for the CPY 701 lecture preview.

Serves the course folder (preview site at /preview/, media at /dist/) and
honours HTTP Range requests so the narrated MP4s seek properly in browsers.

    python3 preview/server.py [port]
"""
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
RANGE = re.compile(r'bytes=(\d*)-(\d*)')


class Handler(SimpleHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def translate_path(self, path):
        return super().translate_path(path)

    def send_head(self):
        rng = self.headers.get('Range')
        if not rng:
            return super().send_head()
        path = self.translate_path(self.path)
        if not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        m = RANGE.match(rng)
        if not m:
            return super().send_head()
        start, end = m.group(1), m.group(2)
        start = int(start) if start else 0
        end = int(end) if end else size - 1
        end = min(end, size - 1)
        if start > end or start >= size:
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{size}')
            self.end_headers()
            return None
        f = open(path, 'rb')
        f.seek(start)
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.end_headers()
        self._limit = end - start + 1
        return f

    def copyfile(self, source, outputfile):
        limit = getattr(self, '_limit', None)
        self._limit = None
        if limit is None:
            return super().copyfile(source, outputfile)
        remaining = limit
        while remaining > 0:
            chunk = source.read(min(64 * 1024, remaining))
            if not chunk:
                break
            remaining -= len(chunk)
            outputfile.write(chunk)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    os.chdir(ROOT)
    srv = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    print(f'CPY 701 preview serving {ROOT} on port {port} (player at /preview/)')
    srv.serve_forever()
