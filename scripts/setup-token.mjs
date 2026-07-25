#!/usr/bin/env node
/**
 * setup-token.mjs — Ajudant per obtenir els 2 secrets del panell d'Instagram.
 *
 * El pas humà (iniciar sessió a Meta i generar un token) NO es pot automatitzar:
 * és una autorització personal dins de la web de Meta. Aquest script fa TOTA
 * la resta a partir d'un token curt:
 *   1) converteix el token curt en un de LLARGA DURADA (~60 dies)
 *   2) troba la pàgina de Facebook i el compte de Instagram vinculat (IG_USER_ID)
 *   3) t'imprimeix els 2 valors per enganxar a GitHub → Settings → Secrets
 *
 * ⚠️  NO enganxis mai el token ni l'APP_SECRET al xat ni al repositori.
 *     Executa'l al teu ordinador i copia el resultat directament a GitHub Secrets.
 *
 * Ús:
 *   APP_ID=xxx APP_SECRET=yyy SHORT_TOKEN=zzz node scripts/setup-token.mjs
 *
 * On aconseguir cada cosa (una sola vegada):
 *   APP_ID / APP_SECRET → developers.facebook.com → la teva app → Configuració → Bàsica
 *   SHORT_TOKEN         → developers.facebook.com/tools/explorer
 *                         (tria la teva app, afegeix els permisos, "Generate Access Token")
 *     Permisos: instagram_basic, instagram_manage_insights, instagram_manage_comments,
 *               pages_read_engagement, pages_show_list, business_management
 */

const API = process.env.IG_API_VERSION || 'v21.0';
const BASE = `https://graph.facebook.com/${API}`;
const { APP_ID, APP_SECRET, SHORT_TOKEN } = process.env;

function die(msg) { console.error('❌ ' + msg); process.exit(1); }
if (!APP_ID || !APP_SECRET || !SHORT_TOKEN) {
  die('Falten variables. Ús:\n   APP_ID=... APP_SECRET=... SHORT_TOKEN=... node scripts/setup-token.mjs');
}

async function get(path, params) {
  const url = new URL(`${BASE}/${path}`);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  const res = await fetch(url);
  const json = await res.json();
  if (json.error) die(`${path}: ${json.error.message} (code ${json.error.code})`);
  return json;
}

const mask = (t) => t.slice(0, 8) + '…' + t.slice(-6);

(async () => {
  // 1) Token de llarga durada
  console.log('→ Convertint a token de llarga durada…');
  const long = await get('oauth/access_token', {
    grant_type: 'fb_exchange_token', client_id: APP_ID, client_secret: APP_SECRET, fb_exchange_token: SHORT_TOKEN,
  });
  const LONG_TOKEN = long.access_token;
  const days = long.expires_in ? Math.round(long.expires_in / 86400) : '≈60';
  console.log(`  ✔ token llarg obtingut (${mask(LONG_TOKEN)}) · caduca en ${days} dies`);

  // 2) Pàgines de Facebook de l'usuari
  console.log('→ Buscant pàgines de Facebook…');
  const pages = await get('me/accounts', { access_token: LONG_TOKEN, fields: 'id,name,instagram_business_account{id,username}' });
  if (!pages.data?.length) die('Aquest usuari no gestiona cap pàgina de Facebook. Vincula @cbgrupbarna a una pàgina.');

  // 3) Compte d'Instagram vinculat
  let ig = null, pageName = '';
  for (const p of pages.data) {
    if (p.instagram_business_account) { ig = p.instagram_business_account; pageName = p.name; break; }
  }
  if (!ig) die('Cap pàgina té un compte de Instagram Business vinculat. Revisa Instagram → Configuració → Comptes vinculats.');
  console.log(`  ✔ pàgina "${pageName}" → Instagram @${ig.username || '?'} (id ${ig.id})`);

  // Resultat
  console.log('\n════════════════════════════════════════════════════════════');
  console.log(' Enganxa aquests 2 valors a GitHub → Settings →');
  console.log(' Secrets and variables → Actions → New repository secret');
  console.log('════════════════════════════════════════════════════════════');
  console.log(`  IG_ACCESS_TOKEN = ${LONG_TOKEN}`);
  console.log(`  IG_USER_ID      = ${ig.id}`);
  console.log('════════════════════════════════════════════════════════════');
  console.log('Després: Actions → "Panell Instagram (fetch dades)" → Run workflow.\n');
})();
