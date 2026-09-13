/**
 * CB Grup Barna · Comptador de la campanya de setembre
 * ──────────────────────────────────────────────────────────────────────────
 * Aquest fitxer NO s'executa al web: és el codi que ha de viure a Google
 * Apps Script, al mateix document on cauen els formularis. El web només el
 * llegeix (js/comptador.js) per pintar les xifres de la portada:
 *
 *     · places lliures del grup de noies del 2018
 *     · nens i nenes apuntats a les portes obertes del setembre
 *
 * Els dies que falten NO surten d'aquí: els compta el navegador des de la
 * data escrita a la portada, que no depèn de ningú.
 *
 * ─── PER QUÈ HI HA UNA PESTANYA «Comptador» ───────────────────────────────
 * No tothom reserva pel web: hi ha famílies que ho fan pel WhatsApp del club
 * o parlant amb en Julio a la pista. Si el comptador només comptés files del
 * formulari, diria que queden places que en realitat ja no hi són — i un
 * comptador que enganya val menys que no tenir-ne cap.
 *
 * Per això el número final és:
 *
 *     reserves del web  +  les que s'apunten a mà a la pestanya «Comptador»
 *
 * ─── COM ES POSA EN MARXA (10 minuts, una sola vegada) ────────────────────
 *  1. Obre el full de càlcul on cauen els formularis del web.
 *  2. Crea una pestanya nova i posa-li de nom exactament «Comptador».
 *  3. Escriu-hi això, a les columnes A i B:
 *
 *        A1: clau            B1: valor
 *        A2: grup2018        B2: 5      ← places del grup de noies del 2018
 *        A3: fora2018        B3: 0      ← reserves del 2018 fetes fora del web
 *        A4: placesSetembre  B4: 50     ← places de portes obertes del setembre
 *        A5: foraSetembre    B5: 0      ← apuntats del setembre fora del web
 *
 *  4. Extensions → Apps Script, enganxa TOT aquest fitxer i desa.
 *  5. Desplega → Nou desplegament → tipus «Aplicació web»:
 *        Executa com a:    jo (el compte del club)
 *        Qui hi té accés:  Qualsevol
 *  6. Copia l'URL que acaba en /exec i enganxa'l a js/canals.js, al camp
 *     `comptadorEndpoint`. Res més.
 *
 * Mentre aquell camp estigui buit, la portada segueix funcionant amb els
 * números escrits a mà al bloc del comptador: no es trenca res.
 *
 * Per provar-ho: obre l'URL /exec al navegador. Ha de sortir una línia de
 * JSON amb lliures, grup, apuntats i places.
 * ─────────────────────────────────────────────────────────────────────────
 */

/** Pestanya on cauen les files dels formularis del web. */
var FULLA_FORMULARIS = 'Respostes';

/** Pestanya dels números que es porten a mà. */
var FULLA_COMPTADOR = 'Comptador';

/** Marca amb què el web envia les reserves de la prova (js/reserva-prova.js). */
var SOURCE_PROVA = 'prova-escoleta';

/** Marques que compten com a apuntats de portes obertes del setembre. */
var SOURCES_SETEMBRE = ['prova-escoleta', 'portes-obertes'];

/** L'any de naixement del grup que estem omplint. */
var ANY_GRUP = '2018';

/** El mes que es compta, en format any-mes. */
var MES = '2026-09';


function doGet(e) {
  var dades;
  try {
    dades = compta();
  } catch (err) {
    dades = { ok: false, error: String(err) };
  }
  var cb = e && e.parameter ? e.parameter.callback : '';
  return resposta(dades, cb);
}


/** Llegeix les dues pestanyes i retorna les xifres ja fetes. */
function compta() {
  var doc = SpreadsheetApp.getActiveSpreadsheet();
  var manual = llegeixComptador(doc);

  var web2018 = 0, webSetembre = 0;
  var fulla = doc.getSheetByName(FULLA_FORMULARIS);
  if (fulla) {
    var files = fulla.getDataRange().getValues();
    var cap = files.length ? files[0].map(normalitza) : [];
    var iData = indexDe(cap, ['data']);
    var iAny = indexDe(cap, ['any', 'any de naixement']);
    var iFont = indexDe(cap, ['origen', 'source', 'font']);

    for (var i = 1; i < files.length; i++) {
      var f = files[i];
      var font = iFont >= 0 ? String(f[iFont]).trim() : '';
      if (!esDelMes(iData >= 0 ? f[iData] : null)) continue;
      if (SOURCES_SETEMBRE.indexOf(font) >= 0) webSetembre++;
      if (font === SOURCE_PROVA && iAny >= 0 && String(f[iAny]).trim() === ANY_GRUP) web2018++;
    }
  }

  var grup = manual.grup2018;
  var ocupades = web2018 + manual.fora2018;
  var lliures = Math.max(0, grup - ocupades);
  var apuntats = Math.min(manual.placesSetembre, webSetembre + manual.foraSetembre);

  return {
    ok: true,
    lliures: lliures,
    grup: grup,
    apuntats: apuntats,
    places: manual.placesSetembre,
    actualitzat: new Date().toISOString()
  };
}


/** Els números que el club porta a mà, amb valors per defecte si no hi són. */
function llegeixComptador(doc) {
  var valors = { grup2018: 5, fora2018: 0, placesSetembre: 50, foraSetembre: 0 };
  var fulla = doc.getSheetByName(FULLA_COMPTADOR);
  if (!fulla) return valors;
  var files = fulla.getDataRange().getValues();
  for (var i = 0; i < files.length; i++) {
    var clau = normalitza(files[i][0]);
    var valor = parseInt(files[i][1], 10);
    if (isNaN(valor)) continue;
    if (clau === 'grup2018') valors.grup2018 = valor;
    if (clau === 'fora2018') valors.fora2018 = valor;
    if (clau === 'placessetembre') valors.placesSetembre = valor;
    if (clau === 'forasetembre') valors.foraSetembre = valor;
  }
  return valors;
}


/** Només compten les files del mes de la campanya. */
function esDelMes(valor) {
  if (!valor) return true;                 // sense data, no es descarta ningú
  var d = valor instanceof Date ? valor : new Date(valor);
  if (isNaN(d.getTime())) return true;
  var mes = d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2);
  return mes === MES;
}


function indexDe(capcaleres, noms) {
  for (var i = 0; i < capcaleres.length; i++) {
    if (noms.indexOf(capcaleres[i]) >= 0) return i;
  }
  return -1;
}


function normalitza(v) {
  return String(v == null ? '' : v)
    .toLowerCase()
    .normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]/g, '');
}


/** JSON per a qui el vulgui llegir, o JSONP si el web ho demana. */
function resposta(obj, callback) {
  var text = JSON.stringify(obj);
  if (callback && /^[A-Za-z_$][A-Za-z0-9_$]*$/.test(callback)) {
    return ContentService
      .createTextOutput(callback + '(' + text + ');')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService
    .createTextOutput(text)
    .setMimeType(ContentService.MimeType.JSON);
}
