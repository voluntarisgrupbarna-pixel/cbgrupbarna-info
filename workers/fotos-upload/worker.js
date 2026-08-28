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
 * Bindings i variables que ha de tenir aquest Worker (Settings del Worker
 * al dashboard de Cloudflare):
 *   FOTOS        R2 bucket binding, apuntant al bucket cbgb-fotos
 *   PUBLIC_BASE  variable normal, la URL pública del bucket (p.ex.
 *                https://pub-xxxx.r2.dev) — només s'usa a /health, per
 *                comprovar que coincideix amb el que hi ha a fotos/config.js
 *   UPLOAD_TOKEN secret, la contrasenya que ha de portar cada pujada
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
    'Access-Control-Allow-Methods': 'PUT, GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-Upload-Secret',
    'Access-Control-Max-Age': '86400',
  };
}

function timingSafeEqual(a, b) {
  // === surt tan bon punt troba la primera lletra diferent: qui pugui
  // mesurar la resposta amb prou precisió podria endevinar el secret
  // lletra a lletra. Aquí sempre es recorren totes dues cadenes senceres.
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

function checkAuth(request, url, env) {
  if (!env.UPLOAD_TOKEN) return false;
  const given = request.headers.get('X-Upload-Secret') || url.searchParams.get('secret') || '';
  return timingSafeEqual(given, env.UPLOAD_TOKEN);
}

async function handleHealth(env, cors) {
  return new Response(JSON.stringify({
    ok: true,
    worker: 'fotos-upload',
    bucketBound: !!env.FOTOS,
    tokenConfigured: !!env.UPLOAD_TOKEN,
    publicBase: env.PUBLIC_BASE || null,
  }), { status: 200, headers: { ...cors, 'Content-Type': 'application/json' } });
}

async function handleList(request, url, env, cors) {
  if (!checkAuth(request, url, env)) {
    return new Response('Unauthorized', { status: 401, headers: cors });
  }
  const prefix = url.searchParams.get('prefix') || 'uploads/';
  const listed = await env.FOTOS.list({ prefix, limit: 50 });
  const objects = listed.objects.map(o => ({ key: o.key, size: o.size, uploaded: o.uploaded }));
  return new Response(JSON.stringify({ ok: true, prefix, truncated: listed.truncated, objects }), {
    status: 200,
    headers: { ...cors, 'Content-Type': 'application/json' },
  });
}

async function handleUpload(request, url, env, cors) {
  if (!env.UPLOAD_TOKEN) {
    return new Response('Worker sense configurar: falta el secret UPLOAD_TOKEN', { status: 500, headers: cors });
  }
  if (!checkAuth(request, url, env)) {
    return new Response('Unauthorized', { status: 401, headers: cors });
  }

  const key = decodeURIComponent(url.pathname.replace(/^\/+/, ''));

  // Nomes fotos i videos coneguts, nomes dins de uploads/<event>/<fitxer>.
  // Mateixes extensions que IMATGES/VIDEOS a scripts/build-gallery-images.py
  // i isVideoRef() a fotos/index.html — si s'hi afegeix un format nou, cal
  // afegir-lo als tres llocs (i a CONTENT_TYPES, aqui sota). Sense aquest
  // filtre, qui tingui el secret (o el trobi filtrat) podria escriure
  // qualsevol fitxer al bucket, que es públic.
  const CONTENT_TYPES = {
    jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', webp: 'image/webp',
    heic: 'image/heic', heif: 'image/heif',
    mp4: 'video/mp4', mov: 'video/quicktime', webm: 'video/webm',
    m4v: 'video/x-m4v', avi: 'video/x-msvideo',
  };
  const m = /^uploads\/[^/]+\/[^/]+\.([A-Za-z0-9]+)$/.exec(key);
  const ext = m ? m[1].toLowerCase() : '';
  if (!m || key.includes('..') || !CONTENT_TYPES[ext]) {
    return new Response('Clau no vàlida: nomes fotos i videos', { status: 400, headers: cors });
  }

  const MAX_BYTES = 200 * 1024 * 1024; // 200 MB: marge ampli per a vídeos de mòbil
  const len = Number(request.headers.get('Content-Length') || '0');
  if (len && len > MAX_BYTES) {
    return new Response('Fitxer massa gran', { status: 413, headers: cors });
  }

  try {
    // El content-type el decidim per l'extensio, no pel que digui el
    // navegador: alguns (HEIC des de mobil, sobretot) no l'envien be, i no
    // volem que un client pugui declarar el que vulgui.
    await env.FOTOS.put(key, request.body, {
      httpMetadata: { contentType: CONTENT_TYPES[ext] },
    });
  } catch (err) {
    return new Response(`Error escrivint a R2: ${err.message}`, { status: 502, headers: cors });
  }

  return new Response(JSON.stringify({ ok: true, key }), {
    status: 200,
    headers: { ...cors, 'Content-Type': 'application/json' },
  });
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const cors = corsHeaders(origin);
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors });
    }
    if (request.method === 'GET' && url.pathname === '/health') {
      return handleHealth(env, cors);
    }
    if (request.method === 'GET' && url.pathname === '/list') {
      return handleList(request, url, env, cors);
    }
    if (request.method === 'PUT') {
      return handleUpload(request, url, env, cors);
    }
    return new Response('Method not allowed', { status: 405, headers: cors });
  },
};
