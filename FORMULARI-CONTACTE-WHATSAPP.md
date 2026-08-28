# Formulari de contacte del xat de WhatsApp

El botó flotant de WhatsApp (`js/xat-whatsapp.js`) ara demana nom, telèfon,
tema i missatge abans d'obrir WhatsApp. Amb això:

1. Les dades es desen en un **Google Sheet** i arriba un **correu** amb el
   contingut, gràcies a un petit script d'Apps Script (codi més avall).
2. **Sempre**, tingui èxit el pas 1 o no, s'obre WhatsApp en una pestanya
   nova amb el mateix missatge ja escrit, perquè la persona el pugui enviar
   i el contacte arribi també per allà.

El pas 1 és opcional i additiu: si no es desplega res, el xat funciona
exactament com abans (només WhatsApp). Per activar-lo:

## Desplegar l'Apps Script (una sola vegada)

1. Ves a **sheets.google.com** → Full de càlcul en blanc. Anomena'l, per
   exemple, «Contactes web CBGB».
2. **Extensions → Apps Script.** Esborra el contingut per defecte
   (`function myFunction() {...}`) i enganxa tot el codi de la secció
   següent.
3. A dalt de tot del codi, revisa `DESTI_EMAIL` — per defecte hi va
   `marqueting@cbgrupbarna.info`; canvia-ho si vols que arribi a una altra
   bústia (per exemple, la teva personal).
4. **Desa** (icona de disquet o `Ctrl/Cmd+S`).
5. **Desplegar → Nova implementació**:
   - Tipus: **Aplicació web**
   - Executar com: **Jo** (el teu compte de Google)
   - Qui hi té accés: **Qualsevol**
6. Google et demanarà autoritzar permisos la primera vegada (és el teu
   propi full de càlcul i el teu propi correu, per això cal donar-hi permís
   explícit). Accepta-ho.
7. Copia la **URL de l'aplicació web** que et dona (acaba en `/exec`).
8. Obre `js/xat-whatsapp.js`, busca la línia `var SHEETS_ENDPOINT = '';` a
   dalt de tot i enganxa-hi la URL entre les cometes. Puja el canvi.

**Si mai cal canviar el codi:** torna a Apps Script, edita, desa, i a
**Desplegar → Gestiona els desplegaments** fes servir el llapis per crear
una **nova versió** del mateix desplegament — la URL no canvia, no cal
tornar a enganxar-la a `xat-whatsapp.js`.

## El codi (Apps Script)

```javascript
/**
 * CB Grup Barna · rep els contactes del xat de WhatsApp del web
 * i els desa a aquest Google Sheet + envia un correu d'avís.
 */
var DESTI_EMAIL = 'marqueting@cbgrupbarna.info';
var NOM_FULL = 'Contactes';

function doPost(e) {
  var dades = JSON.parse(e.postData.contents);
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var full = ss.getSheetByName(NOM_FULL);
  if (!full) {
    full = ss.insertSheet(NOM_FULL);
    full.appendRow(['Data', 'Nom', 'Telèfon', 'Tema', 'Missatge', 'Pàgina', 'Idioma']);
  }
  full.appendRow([
    new Date(), dades.nom || '', dades.telefon || '', dades.tema || '',
    dades.missatge || '', dades.pagina || '', dades.idioma || ''
  ]);

  MailApp.sendEmail({
    to: DESTI_EMAIL,
    subject: 'Nou contacte web: ' + (dades.nom || 'sense nom'),
    body: 'Nou contacte des del xat de WhatsApp de cbgrupbarna.info\n\n' +
      'Nom: ' + (dades.nom || '-') + '\n' +
      'Telèfon: ' + (dades.telefon || '-') + '\n' +
      'Tema: ' + (dades.tema || '-') + '\n' +
      'Missatge: ' + (dades.missatge || '-') + '\n' +
      'Pàgina: ' + (dades.pagina || '-') + '\n\n' +
      'Aquesta persona ja té obert WhatsApp per escriure\'t; també li ha ' +
      'arribat el mateix missatge amb aquestes dades.'
  });

  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

## Per què està fet així (i les seves trampes)

- **`fetch(..., {mode:'no-cors'})` des del navegador.** Un `doPost` d'Apps
  Script no respon amb les capçaleres CORS que un navegador exigeix per
  llegir la resposta des d'un altre origen. La solució estàndard és
  enviar-hi la petició en mode `no-cors`: arriba i s'executa igual, però el
  navegador no deixa llegir la resposta — per això `enviaDades()` a
  `xat-whatsapp.js` no comprova si ha anat bé, només dispara la petició i
  continua. No calen capçaleres `Content-Type` personalitzades (evitaria el
  mode `no-cors` i faria una petició *preflight* que Apps Script no gestiona
  bé); el cos es passa tal qual com a text, i `doPost` el interpreta amb
  `JSON.parse(e.postData.contents)`.
- **Mai bloqueja WhatsApp.** Si `SHEETS_ENDPOINT` és buit, si no hi ha
  connexió, o si l'script no s'ha desplegat encara, `enviaDades()` falla en
  silenci (try/catch) i el codi continua igualment cap a `window.open` amb
  l'enllaç de WhatsApp. El full de càlcul és un extra, mai un requisit pel
  contacte real.
- **Per què un correu i no només el full.** Un full de càlcul no avisa de
  res per si sol; qui no l'obre cada dia no es n'assabenta. El correu és el
  que fa que arribi de veritat sense haver-hi de pensar.
- **La casella de consentiment és pròpia del formulari, no del banner de
  galetes.** Aquí la persona sempre decideix activament escriure les seves
  dades i prémer «Enviar» — no és una cookie de seguiment que calgui
  acceptar abans de res, és una acció voluntària amb el seu propi text
  legal, igual que la resta de formularis del web (`fotos/`, `fotos-3x3/`,
  etc.).
