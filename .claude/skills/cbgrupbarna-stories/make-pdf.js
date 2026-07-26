/**
 * Genera el PDF de la guia editorial a partir de reference.html.
 *
 *   node make-pdf.js [sortida.pdf]
 *
 * Per què Chromium i no LibreOffice: en aquest entorn `soffice` no converteix
 * res (falla amb "source file could not be loaded" fins i tot amb un .txt),
 * així que la ruta bona és imprimir l'HTML amb Chromium headless. El CSS
 * d'impressió de reference.html ja fa que cada grup de fitxes comenci a
 * pàgina nova (`.sheetgroup { break-before: page }`).
 *
 * Cal playwright disponible; si no és al projecte:
 *   NODE_PATH=$(npm root -g) node make-pdf.js
 */
const path = require('path');
const { chromium } = require('playwright');

const OUT = process.argv[2] || path.join(__dirname, 'guia-editorial-cbgb.pdf');
const SRC = 'file://' + path.join(__dirname, 'reference.html');

(async () => {
  const browser = await chromium.launch({
    // Chromium preinstal·lat de l'entorn; treure'l si el sistema ja en té un.
    executablePath: '/opt/pw-browsers/chromium',
  });
  const page = await browser.newPage();

  // colorScheme light: la guia és theme-aware i en dark el PDF sortiria fosc.
  await page.emulateMedia({ media: 'print', colorScheme: 'light' });
  await page.goto(SRC, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1200); // deixa assentar fonts i imatges base64

  await page.pdf({
    path: OUT,
    format: 'A4',
    printBackground: true,
    margin: { top: '14mm', bottom: '14mm', left: '12mm', right: '12mm' },
  });

  await browser.close();
  console.log('PDF escrit a', OUT);
})();
