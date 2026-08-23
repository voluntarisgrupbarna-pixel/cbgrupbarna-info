/**
 * Cens de zones tocables: totes, no una mostra.
 *
 * PER QUÈ EXISTEIX. tests/ux-deep.mjs ja comprova les zones tocables, però al
 * seu informe només hi desa sis exemples per recorregut. Amb centenars
 * d'avisos, això vol dir que un objectiu massa petit es pot quedar sense
 * sortir mai a la llista, i llavors sembla arreglat quan no ho és: així
 * s'havien passat per alt els botons de la barra de galetes (42 px, a dos de
 * la pauta) i els enllaços del peu de /escoleta/ (16 px).
 *
 * Aquest fitxer passa el MATEIX mesurament —el llegeix de ux-deep.mjs, no en
 * fa una còpia que es pugui desincronitzar— però els compta tots i separa el
 * que és curt d'ALÇADA del que només ho és d'AMPLE. La distinció importa: el
 * que decideix si es pot prémer una cosa amb el dit és l'alçada, i hi ha
 * controls del lloc (els tres botons de dues lletres del canvi d'idioma) que
 * es queden curts d'ample a propòsit i amb la raó escrita al CSS.
 *
 * Les galetes es responen abans de mesurar: si no, la barra de consentiment
 * tapa mitja pàgina i els seus dos botons surten a totes les mesures.
 *
 *     node tests/zones-tocables.mjs
 *     node tests/zones-tocables.mjs --tot     # llista tots els casos
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { startServer } from './lib/server.mjs';

const require = createRequire(import.meta.url);
const { chromium } = (() => {
  try { return require('playwright'); }
  catch { return require('/opt/node22/lib/node_modules/playwright'); }
})();

const ARREL = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const TOT = process.argv.includes('--tot');

// El mesurament surt de la bateria gran: una sola definició, cap còpia.
const font = fs.readFileSync(path.join(ARREL, 'tests/ux-deep.mjs'), 'utf8');
const inici = font.indexOf('const TOCS = `');
const TOCS = font.slice(inici + 'const TOCS = `'.length, font.indexOf('})()`;', inici) + 4);

const PAGINES = ['/', '/escoleta/', '/partits/', '/partits/calendaris/', '/campus/',
  '/femeni/', '/patrocinadors/', '/blog/', '/club/', '/faq/', '/opina/', '/3x3/',
  '/organigrama/', '/instal-lacions/', '/premsa/', '/newsletter/', '/es/', '/en/'];

// Només pantalles que es toquen amb el dit: amb ratolí, la pauta no s'aplica.
const DISPOSITIUS = [
  ['mobil-320', 320, 568], ['mobil-360', 360, 740], ['mobil-390', 390, 844],
  ['mobil-430', 430, 932], ['mobil-ajagut', 844, 390], ['tauleta-768', 768, 1024],
  ['tauleta-820', 820, 1180], ['tauleta-ajaguda', 1180, 820], ['tauleta-1024', 1024, 1366],
];

const servidor = await startServer(ARREL);
const navegador = await chromium.launch();
const curts = [];
let nomesAmple = 0;

for (const [nom, width, height] of DISPOSITIUS) {
  const ctx = await navegador.newContext({
    viewport: { width, height }, hasTouch: true, isMobile: true, locale: 'ca-ES',
  });
  for (const url of PAGINES) {
    const pag = await ctx.newPage();
    try {
      await pag.goto(servidor.origin + url, { waitUntil: 'networkidle', timeout: 20000 });
      // Respondre les galetes: si no, la barra tapa la pàgina i els seus dos
      // botons surten a cadascuna de les 162 mesures.
      await pag.evaluate(() => {
        try {
          localStorage.setItem('cbgb_galetes', 'accepta');
          localStorage.setItem('cbgb_galetes_v', '1');
        } catch (e) { /* mode privat: la barra hi serà i sortirà a la llista */ }
      });
      await pag.reload({ waitUntil: 'networkidle', timeout: 20000 });
      await pag.waitForTimeout(250);
      for (const t of await pag.evaluate(TOCS)) {
        if (t.h < 44) curts.push({ nom, url, ...t });
        else nomesAmple++;
      }
    } catch (e) {
      console.log(`  no s'ha pogut mesurar ${url} @ ${nom}: ${e.message.slice(0, 70)}`);
    }
    await pag.close();
  }
  await ctx.close();
}

console.log(`\n${DISPOSITIUS.length} dispositius tàctils × ${PAGINES.length} pàgines`);
console.log(`curts d'ALÇADA: ${curts.length}`);
console.log(`només curts d'AMPLE: ${nomesAmple}`);
if (curts.length) {
  console.log('');
  const mostra = TOT ? curts : curts.slice(0, 40);
  for (const c of mostra) {
    console.log(`  ${c.nom.padEnd(16)} ${c.url.padEnd(22)} ${c.tag} «${c.text}» ${c.w}×${c.h}`);
  }
  if (!TOT && curts.length > mostra.length) {
    console.log(`  …i ${curts.length - mostra.length} més (amb --tot surten tots)`);
  }
}

await navegador.close();
servidor.close();
process.exit(curts.length ? 1 : 0);
