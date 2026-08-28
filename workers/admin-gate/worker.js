/**
 * CB Grup Barna · Porta d'accés d'/admin/ amb límit d'intents
 *
 * scripts/admin-gate.js hi envia el SHA-256 de la contrasenya que algú ha
 * escrit a /admin/ (mai la contrasenya en clar). Aquest Worker el compara
 * amb el secret PASS_HASH i, si falla massa cops seguits des de la mateixa
 * IP, bloqueja nous intents durant una estona — exactament el que un hash
 * públic guardat al repositori (com hi havia abans) no pot fer per si sol:
 * un atacant amb el fitxer pot provar milions de contrasenyes per segon amb
 * una GPU, offline; contra aquest Worker, com a molt en pot provar 8 cada
 * 15 minuts.
 *
 * Mentre no el despleguis i no omplis GATE_ENDPOINT a
 * scripts/admin-gate.js, la porta segueix funcionant exactament com fins
 * ara (comparació local contra PASS_HASH, sense límit d'intents). Res es
 * trenca per tenir aquest codi al repositori sense usar-lo.
 *
 * Bindings i variables que ha de tenir aquest Worker:
 *   INTENTS    KV namespace binding, per comptar intents fallits per IP
 *   PASS_HASH  secret — el mateix SHA-256 que hi havia (o hi ha) a
 *              scripts/admin-gate.js, però a partir d'ara NOMÉS aquí, mai
 *              més enganxat en clar a cap fitxer públic del repositori
 *
 * Desplegament: vegeu README.md d'aquesta carpeta.
 */

const ALLOWED_ORIGINS = new Set([
  'https://cbgrupbarna.info',
  'https://www.cbgrupbarna.info',
]);

const MAX_INTENTS = 8;            // intents fallits permesos...
const FINESTRA_SEGONS = 15 * 60;  // ...dins d'aquesta finestra de temps

function corsHeaders(origin) {
  const allow = ALLOWED_ORIGINS.has(origin) ? origin : 'https://cbgrupbarna.info';
  return {
    'Access-Control-Allow-Origin': allow,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
}

function json(body, status, cors) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, 'Content-Type': 'application/json' },
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '';
    const cors = corsHeaders(origin);

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors });
    }
    if (url.pathname === '/health') {
      return json({
        ok: true,
        worker: 'admin-gate',
        passConfigured: !!env.PASS_HASH,
        kvBound: !!env.INTENTS,
      }, 200, cors);
    }
    if (request.method !== 'POST') {
      return json({ ok: false, error: 'method not allowed' }, 405, cors);
    }
    if (!env.PASS_HASH || !env.INTENTS) {
      return json({ ok: false, error: 'worker not configured' }, 500, cors);
    }

    const ip = request.headers.get('CF-Connecting-IP') || 'desconegut';
    const clau = `intents:${ip}`;
    const ara = Math.floor(Date.now() / 1000);

    const actual = await env.INTENTS.get(clau, { type: 'json' });
    if (actual && ara < actual.finsA && actual.count >= MAX_INTENTS) {
      return json({ ok: false, blocked: true, retryAfter: actual.finsA - ara }, 429, cors);
    }

    let hash;
    try {
      const cos = await request.json();
      hash = String(cos.hash || '').toLowerCase();
    } catch (e) {
      return json({ ok: false, error: 'bad request' }, 400, cors);
    }
    if (!/^[0-9a-f]{64}$/.test(hash)) {
      return json({ ok: false, error: 'bad hash' }, 400, cors);
    }

    if (hash === env.PASS_HASH.toLowerCase()) {
      await env.INTENTS.delete(clau);
      return json({ ok: true }, 200, cors);
    }

    const comptaDesDe = actual && ara < actual.finsA ? actual.count : 0;
    await env.INTENTS.put(clau, JSON.stringify({ count: comptaDesDe + 1, finsA: ara + FINESTRA_SEGONS }), {
      expirationTtl: FINESTRA_SEGONS,
    });
    return json({ ok: false }, 200, cors);
  },
};
