// Servidor estàtic mínim per servir el lloc tal com el publica GitHub Pages:
// una carpeta amb index.html es resol com la carpeta, i els 404 són 404 de debò.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.avif': 'image/avif',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.pdf': 'application/pdf',
  '.ics': 'text/calendar; charset=utf-8',
  '.vcf': 'text/vcard; charset=utf-8',
  '.mp4': 'video/mp4',
};

export function startServer(root, port = 0) {
  const server = http.createServer((req, res) => {
    let pathname;
    try {
      pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    } catch {
      res.writeHead(400).end('bad url');
      return;
    }

    // Cap sortida de l'arrel del lloc.
    const target = path.join(root, path.normalize(pathname));
    if (!target.startsWith(root)) {
      res.writeHead(403).end('forbidden');
      return;
    }

    let file = target;
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) {
      file = path.join(file, 'index.html');
    }
    if (!fs.existsSync(file) || !fs.statSync(file).isFile()) {
      res.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' }).end('404');
      return;
    }

    const type = TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream';
    const body = fs.readFileSync(file);

    // Sense suport de rangs, un <video> avorta la petició i semblaria que el
    // fitxer no existeix. GitHub Pages sí que els serveix.
    const range = req.headers.range;
    const m = range && range.match(/bytes=(\d*)-(\d*)/);
    if (m) {
      const start = m[1] ? +m[1] : 0;
      const end = m[2] ? +m[2] : body.length - 1;
      if (start >= body.length) {
        res.writeHead(416, { 'content-range': `bytes */${body.length}` }).end();
        return;
      }
      const slice = body.subarray(start, end + 1);
      res.writeHead(206, {
        'content-type': type,
        'content-length': slice.length,
        'content-range': `bytes ${start}-${end}/${body.length}`,
        'accept-ranges': 'bytes',
      });
      res.end(slice);
      return;
    }

    res.writeHead(200, { 'content-type': type, 'content-length': body.length, 'accept-ranges': 'bytes' });
    res.end(body);
  });

  return new Promise((resolve) => {
    server.listen(port, '127.0.0.1', () => {
      const { port: actual } = server.address();
      resolve({ server, origin: `http://127.0.0.1:${actual}`, close: () => new Promise((r) => server.close(r)) });
    });
  });
}
