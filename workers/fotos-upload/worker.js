/**
 * CB Grup Barna · Galeria · pujador directe a R2
 *
 * L'admin panel (/fotos/admin.html) fa un PUT aquí amb la foto/vídeo en
 * brut i una clau compartida. Aquest Worker la comprova i escriu directament
 * al bucket R2 amb el seu binding natiu — la clau d'R2 no surt mai del
 * Worker, i el navegador no en sap res.
 *
 * Objectiu: que pujar 200 fotos torni a ser 200 escriptures a R2, no 200
 * commits al repositori (vegeu fotos/admin.html i el comentari de dalt de
 * .github/workflows/sync-r2.yml).
 *
 * Desplegament: vegeu README.md d'aquesta carpeta.
 */

const ALLOWED_ORIGINS = new Set([
  'https://cbgrupbarna.info',
  'https://www.cbgrupbarna.info',
]);

function corsHeaders(origin) {
  const allow = ALLOWED_ORIGINS.has(origin) ? origin : 'https://cbgrupbarna.info';
  return {
    'Access-Control-Allow-Origin': allow,
    'Access-Control-Allow-Methods': 'PUT, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-Upload-Secret',
    'Access-Control-Max-Age': '86400',
  };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const cors = corsHeaders(origin);

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors });
    }

    if (request.method !== 'PUT') {
      return new Response('Method not allowed', { status: 405, headers: cors });
    }

    if (!env.UPLOAD_SECRET) {
      return new Response('Worker sense configurar: falta el secret UPLOAD_SECRET', { status: 500, headers: cors });
    }
    const given = request.headers.get('X-Upload-Secret') || '';
    if (given !== env.UPLOAD_SECRET) {
      return new Response('Unauthorized', { status: 401, headers: cors });
    }

    const url = new URL(request.url);
    const key = decodeURIComponent(url.pathname.replace(/^\/+/, ''));

    // Nomes fotos i videos, nomes dins de uploads/<event>/<fitxer>. Sense
    // aixo qualsevol que tingui el secret podria escriure a qualsevol clau.
    if (!/^uploads\/[^/]+\/[^/]+\.[A-Za-z0-9]+$/.test(key)) {
      return new Response('Clau no vàlida', { status: 400, headers: cors });
    }
    if (key.includes('..')) {
      return new Response('Clau no vàlida', { status: 400, headers: cors });
    }

    const MAX_BYTES = 200 * 1024 * 1024; // 200 MB: marge ampli per a vídeos de mòbil
    const len = Number(request.headers.get('Content-Length') || '0');
    if (len && len > MAX_BYTES) {
      return new Response('Fitxer massa gran', { status: 413, headers: cors });
    }

    try {
      await env.BUCKET.put(key, request.body, {
        httpMetadata: {
          contentType: request.headers.get('Content-Type') || 'application/octet-stream',
        },
      });
    } catch (err) {
      return new Response(`Error escrivint a R2: ${err.message}`, { status: 502, headers: cors });
    }

    return new Response(JSON.stringify({ ok: true, key }), {
      status: 200,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  },
};
