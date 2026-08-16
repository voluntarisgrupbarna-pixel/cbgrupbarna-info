/* Genera el PDF de /presentacio/ en diapositives 16:9 apaisades.
 *
 * El PDF surt de la MATEIXA pagina, amb el full @media print que hi ha a
 * presentacio/index.html: si es canvia el contingut de la pagina, s'ha de
 * tornar a executar aixo o el PDF que es descarrega quedara desfasat.
 *
 *   python3 -m http.server 8899          (des de l'arrel del repositori)
 *   node scripts/generate-presentacio-pdf.mjs
 *
 * Comprova que no hi hagi cap pagina en blanc: apareixen quan un bloc de
 * diapositiva arriba just a l'alcada de la pagina.
 */
import { chromium } from 'playwright';

const URL = process.env.URL || 'http://localhost:8899/presentacio/';
const OUT = 'presentacio/cb-grup-barna-presentacio.pdf';

const browser = await chromium.launch({
  executablePath: process.env.CHROMIUM || undefined,
});
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 });

// Les fotos van amb carrega mandrosa i l'entrada de les peces amb scroll:
// sense aixo, al PDF hi sortirien forats blancs i blocs invisibles.
await page.evaluate(async () => {
  document.querySelectorAll('img[loading="lazy"]').forEach((i) => (i.loading = 'eager'));
  document.querySelectorAll('.rv').forEach((e) => e.classList.add('in'));
  for (let y = 0; y < document.body.scrollHeight; y += 600) {
    window.scrollTo(0, y);
    await new Promise((r) => setTimeout(r, 120));
  }
  window.scrollTo(0, 0);
});
await page.waitForLoadState('networkidle');
await page.waitForTimeout(1500);

await page.emulateMedia({ media: 'print' });
await page.pdf({
  path: OUT,
  width: '1280px',
  height: '720px',
  printBackground: true,
  preferCSSPageSize: true,
  margin: { top: 0, right: 0, bottom: 0, left: 0 },
});
await browser.close();
console.log('PDF generat a', OUT);
