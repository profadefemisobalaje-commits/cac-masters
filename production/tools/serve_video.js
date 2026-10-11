// Tiny static file server with HTTP Range support (required for video
// seeking in browsers). Serves production/out/video on 0.0.0.0:8000.
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..', 'out', 'video');
const MIME = { '.mp4': 'video/mp4', '.html': 'text/html; charset=utf-8',
               '.jpg': 'image/jpeg', '.srt': 'text/plain; charset=utf-8',
               '.vtt': 'text/vtt; charset=utf-8' };
http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p === '/' || p === '') p = '/index.html';
  const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  fs.stat(f, (e, st) => {
    if (e || !st.isFile()) { res.writeHead(404); return res.end('not found'); }
    const mime = MIME[path.extname(f)] || 'application/octet-stream';
    const range = req.headers.range;
    if (range) {
      const m = /bytes=(\d*)-(\d*)/.exec(range);
      const s = m && m[1] ? parseInt(m[1], 10) : 0;
      const e = m && m[2] ? Math.min(parseInt(m[2], 10), st.size - 1) : st.size - 1;
      res.writeHead(206, {
        'Content-Range': `bytes ${s}-${e}/${st.size}`,
        'Accept-Ranges': 'bytes', 'Content-Length': e - s + 1,
        'Content-Type': mime, 'Access-Control-Allow-Origin': '*',
      });
      fs.createReadStream(f, { start: s, end: e }).pipe(res);
    } else {
      res.writeHead(200, { 'Content-Length': st.size, 'Content-Type': mime,
                           'Accept-Ranges': 'bytes',
                           'Access-Control-Allow-Origin': '*' });
      fs.createReadStream(f).pipe(res);
    }
  });
}).listen(8000, '0.0.0.0', () => console.log('video server listening on 0.0.0.0:8000'));
