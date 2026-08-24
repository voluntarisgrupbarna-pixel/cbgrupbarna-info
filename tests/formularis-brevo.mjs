// Comprova que TOTS els formularis del web arriben a Brevo amb les dades que
// toquen, i que la campanya d'entrada els segueix encara que s'enviïn des
// d'una altra pàgina.
//
//   node tests/formularis-brevo.mjs
//
// No surt res de la màquina: tot el que no sigui el servidor local es talla,
// i l'`action` de Brevo és falsa. El que es mira és què s'hi hauria enviat.
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import { startServer } from './lib/server.mjs';

const require = createRequire(import.meta.url);
const { chromium } = (() => {
  try { return require('playwright'); }
  catch { return require('/opt/node22/lib/node_modules/playwright'); }
})();

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
// S'hi arriba per un anunci del campus i s'envia el formulari des d'una altra
// pàgina: la campanya ha d'arribar igualment a Brevo.
const ENTRADA = '/campus/?utm_source=instagram&utm_medium=reel&utm_campaign=campus-nadal-2026';

const CASOS = [
  ['/', 'portada', ['NOM', 'TELEFON', 'EMAIL'], async p => {
    await p.fill('#f-nom', 'Ana Prova'); await p.fill('#f-mobil', '600111222');
    await p.fill('#f-mail', 'ana@example.com'); await p.check('#f-ok');
    await p.click('#infoForm button[type=submit]');
  }],
  ['/es/', 'portada', ['NOM', 'TELEFON', 'EMAIL'], async p => {
    await p.fill('#f-nom', 'Ana Prova'); await p.fill('#f-mobil', '600111222');
    await p.fill('#f-mail', 'ana@example.com'); await p.check('#f-ok');
    await p.click('#infoForm button[type=submit]');
  }],
  ['/en/', 'portada', ['NOM', 'TELEFON', 'EMAIL'], async p => {
    await p.fill('#f-nom', 'Ana Prova'); await p.fill('#f-mobil', '600111222');
    await p.fill('#f-mail', 'ana@example.com'); await p.check('#f-ok');
    await p.click('#infoForm button[type=submit]');
  }],
  ['/escriu-nos/', 'informacio', ['NOM', 'TELEFON', 'EMAIL'], async p => {
    await p.fill('#in-nom', 'Ana'); await p.fill('#in-tel', '600111222');
    await p.fill('#in-mail', 'ana@example.com'); await p.fill('#in-msg', 'Hola');
    await p.click('#in-form button[type=submit]');
  }],
  ['/portes-obertes/', 'portesObertes', ['NOM', 'TELEFON', 'EMAIL', 'ANY_NAIX'], async p => {
    await p.fill('#po-nom', 'Nen Prova'); await p.fill('#po-any', '2014');
    await p.fill('#po-contacte', 'Ana'); await p.fill('#po-tel', '600111222');
    await p.fill('#po-mail', 'ana@example.com');
    await p.click('#po-form button[type=submit]');
  }],
  ['/newsletter/', 'newsletter', ['EMAIL', 'CONSENT'], async p => {
    await p.fill('#nl-email', 'ana@example.com'); await p.fill('#nl-nom', 'Ana');
    await p.check('#nl-ok'); await p.click('#nl-form button[type=submit]');
  }],
  ['/bustia/', 'bustia', ['EMAIL'], async p => {
    await p.selectOption('#bu-tema', 'Escoleta'); await p.fill('#bu-msg', 'Una idea');
    await p.fill('#bu-mail', 'ana@example.com'); await p.click('#bu-form button[type=submit]');
  }],
  ['/opina/', 'ressenya', ['EMAIL', 'ESTRELLES'], async p => {
    await p.fill('#rs-nom', 'Ana'); await p.fill('#rs-mail', 'ana@example.com');
    await p.fill('#rs-msg', 'Molt bé'); await p.click('#rs-form button[type=submit]');
  }],
  ['/documents/', 'descarrega', ['NOM', 'TELEFON', 'EMAIL'], async p => {
    await p.click('a[data-descarrega]');
    await p.fill('input[name=nom]', 'Ana Prova'); await p.fill('input[name=email]', 'ana@example.com');
    await p.fill('input[name=mobil]', '600111222'); await p.check('input[name=rgpd]');
    await p.click('form button[type=submit]');
  }],
  ['/galeria-3x3-glories/', 'galeria', ['NOM', 'TELEFON', 'EMAIL'], async p => {
    await p.fill('#nom', 'Ana'); await p.fill('#cognoms', 'Prova');
    await p.fill('#email', 'ana@example.com'); await p.fill('#mobil', '600111222');
    await p.fill('#club', 'CB Grup Barna'); await p.check('#gate-consent');
    await p.click('#gate-btn'); await p.waitForTimeout(300);
    await p.check('#follow-check'); await p.click('#follow-btn, button[onclick*=handleFollow]');
  }],
];

const { origin, close } = await startServer(ROOT);
const nav = await chromium.launch();
let mal = 0;

for (const [ruta, canal, obligatoris, omple] of CASOS) {
  const ctx = await nav.newContext();
  const pag = await ctx.newPage();
  const errors = [];
  pag.on('pageerror', e => errors.push(String(e)));
  // Res no surt de la màquina. Els <script> de fora es responen amb un fitxer
  // buit i no amb JSON: si no, el navegador es queixa d'un error de sintaxi
  // que no és del web.
  await pag.route('**', r => {
    if (r.request().url().startsWith(origin)) return r.continue();
    return r.request().resourceType() === 'script'
      ? r.fulfill({ status: 200, body: '', contentType: 'text/javascript' })
      : r.fulfill({ status: 200, body: '{"success":"true"}', contentType: 'application/json' });
  });

  await pag.goto(origin + ENTRADA, { waitUntil: 'domcontentloaded' });
  await pag.goto(origin + ruta, { waitUntil: 'domcontentloaded' });
  await pag.evaluate(c => {
    window.CANALS.brevo.formularis[c] = 'https://sibforms.com/serve/PROVA';
    window.__brevo = [];
    const orig = window.fetch;
    window.fetch = function (url, opt) {
      if (String(url).includes('sibforms.com')) {
        const camps = {};
        if (opt && opt.body && opt.body.forEach) opt.body.forEach((v, k) => { camps[k] = v; });
        window.__brevo.push(camps);
      }
      return orig.apply(this, arguments);
    };
  }, canal);

  let falla = [];
  try { await omple(pag); } catch (e) { falla.push('no s\'ha pogut omplir: ' + e.message.split('\n')[0]); }
  await pag.waitForTimeout(500);
  const enviat = (await pag.evaluate(() => window.__brevo))[0];

  if (!enviat) falla.push('no ha arribat res a Brevo');
  else {
    for (const camp of ['EMAIL', 'ORIGEN', 'IDIOMA', ...obligatoris]) {
      if (!enviat[camp]) falla.push('falta ' + camp);
    }
    if (enviat.CAMPANYA !== 'campus-nadal-2026') falla.push('s\'ha perdut la campanya');
    if (enviat.FONT !== 'instagram') falla.push('s\'ha perdut la font');
  }
  if (errors.length) falla.push('errors de JS: ' + errors.join(' | '));

  if (falla.length) mal++;
  console.log((falla.length ? '✗ ' : '✔ ') + ruta.padEnd(24) + canal.padEnd(15) +
              (falla.length ? falla.join('; ') : 'correcte'));
  await ctx.close();
}

await nav.close();
await close();
console.log(mal ? '\n' + mal + ' formularis fallen' : '\nTots els formularis arriben a Brevo');
process.exit(mal ? 1 : 0);
