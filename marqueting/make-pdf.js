/**
 * Genera el PDF del dashboard de màrqueting a partir de index.html.
 *
 *   node make-pdf.js [sortida.pdf]
 *
 * Chromium (no LibreOffice, que en aquest entorn no converteix res).
 */
const path = require('path');
const { chromium } = require('playwright');

const OUT = process.argv[2] || path.join(__dirname, 'dashboard-marqueting-cbgb.pdf');
const SRC = 'file://' + path.join(__dirname, 'index.html');

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage();
  await page.emulateMedia({ media: 'print', colorScheme: 'light' });
  await page.goto(SRC, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);

  // print-only tweaks: unstick the topbar, drop hover chrome noise
  await page.addStyleTag({ content: `
    .topbar{position:static !important;}
    a.card:hover, .chip:hover{transform:none !important;}
    .card, .sw, .vscol{break-inside:avoid;}
    table{break-inside:auto;}
    tr{break-inside:avoid;}
  `});

  await page.pdf({
    path: OUT,
    format: 'A4',
    printBackground: true,
    margin: { top: '12mm', bottom: '12mm', left: '10mm', right: '10mm' },
  });

  await browser.close();
  console.log('PDF escrit a', OUT);
})();
