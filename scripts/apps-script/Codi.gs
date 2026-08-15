/**
 * CB GRUP BARNA · BÚSTIA ÚNICA DE FORMULARIS
 * ---------------------------------------------------------------------------
 * Rep tots els formularis de cbgrupbarna.info, escriu una fila a la pestanya
 * que toca del full de càlcul i avisa per correu al moment.
 *
 * Les instruccions per posar-ho en marxa són a README.md, en aquesta mateixa
 * carpeta. Aquí només cal tocar el bloc CONFIGURACIÓ.
 * ---------------------------------------------------------------------------
 */

// ═══════════════════════════════════════════════════════════════════════════
//  CONFIGURACIÓ · això és l'únic que s'ha de tocar
// ═══════════════════════════════════════════════════════════════════════════

/** ID del full de càlcul. És el tros llarg de la URL, entre /d/ i /edit. */
var FULL_ID = '';

/** A qui arriba l'avís de cada formulari nou. */
var AVIS_A = 'voluntarisgrupbarna@gmail.com';

/** Còpia opcional. Deixa-ho buit si no en vols. */
var AVIS_CC = '';

/** Posa-ho a false per deixar d'enviar correus sense tocar res més. */
var ENVIA_CORREU = true;

// ═══════════════════════════════════════════════════════════════════════════
//  Una pestanya per tipus de formulari. La clau és el que envia la web.
//  Si arriba un tipus que no és en aquesta llista, va a «Altres».
// ═══════════════════════════════════════════════════════════════════════════

var PESTANYES = {
  'informacio':  'Informació',
  'galeria-3x3': 'Galeria 3x3',
  'fotos-3x3':   'Fotos 3x3',
  'campus':      'Campus',
  'patrocini':   'Patrocini',
  'entrenador':  'Entrenadors'
};
var PESTANYA_PER_DEFECTE = 'Altres';

/** L'ordre de les columnes. Afegir-ne al final no trenca res del que ja hi ha. */
var COLUMNES = [
  'Data', 'Hora', 'Tipus', 'Nom', 'Cognoms', 'Mòbil', 'Correu',
  'Club', 'Interès', 'Missatge', 'Consentiment', 'Pàgina', 'Font'
];

// ═══════════════════════════════════════════════════════════════════════════
//  ENTRADA
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Comprovació ràpida des del navegador: obrir la URL /exec ha de mostrar
 * {"ok":true,...}. Si això no surt, el desplegament no està bé i no cal
 * seguir provant res més.
 */
function doGet() {
  var estat = { ok: true, servei: 'Bústia de formularis · CB Grup Barna' };
  try {
    var full = SpreadsheetApp.openById(FULL_ID);
    estat.full = full.getName();
    estat.pestanyes = full.getSheets().map(function (f) { return f.getName(); });
  } catch (err) {
    estat.ok = false;
    estat.error = 'No puc obrir el full: ' + err;
  }
  return json(estat);
}

function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return json({ ok: false, error: 'Sense dades' });
    }
    var d = JSON.parse(e.postData.contents);

    // Trampa per a robots: el camp «web» és invisible per a les persones.
    // Si ve omplert, ho donem per bo perquè el bot no ho torni a provar,
    // però no ho desem enlloc.
    if (d.web) return json({ ok: true, ignorat: 'bot' });

    // Un formulari omplert en menys de dos segons no l'ha omplert ningú.
    if (typeof d.ms === 'number' && d.ms >= 0 && d.ms < 2000) {
      return json({ ok: true, ignorat: 'massa-rapid' });
    }

    var fila = desa(d);
    if (ENVIA_CORREU) avisa(d);
    return json({ ok: true, fila: fila });

  } catch (err) {
    // L'error es guarda perquè no es perdi encara que el correu falli.
    try { registraError(err, e); } catch (_) {}
    return json({ ok: false, error: String(err) });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
//  DESAR
// ═══════════════════════════════════════════════════════════════════════════

function desa(d) {
  // El pany evita que dos enviaments alhora escriguin a la mateixa fila.
  var pany = LockService.getScriptLock();
  pany.waitLock(20000);
  try {
    var pestanya = pestanyaPer(d.tipus);
    var ara = new Date();
    var tz = Session.getScriptTimeZone() || 'Europe/Madrid';

    pestanya.appendRow([
      Utilities.formatDate(ara, tz, 'dd/MM/yyyy'),
      Utilities.formatDate(ara, tz, 'HH:mm'),
      text(d.tipus),
      text(d.nom),
      text(d.cognoms),
      "'" + text(d.mobil),          // apòstrof al davant: els mòbils no són números
      text(d.correu),
      text(d.club),
      text(d.interes),
      text(d.missatge),
      d.consentiment ? 'Sí' : 'No',
      text(d.pagina),
      text(d.font)
    ]);
    return pestanya.getLastRow();
  } finally {
    pany.releaseLock();
  }
}

/** Torna la pestanya del tipus demanat, i la crea amb capçalera si no hi és. */
function pestanyaPer(tipus) {
  var full = SpreadsheetApp.openById(FULL_ID);
  var nom = PESTANYES[String(tipus || '').toLowerCase()] || PESTANYA_PER_DEFECTE;
  var pestanya = full.getSheetByName(nom);

  if (!pestanya) {
    pestanya = full.insertSheet(nom);
    pestanya.appendRow(COLUMNES);
    var cap = pestanya.getRange(1, 1, 1, COLUMNES.length);
    cap.setFontWeight('bold');
    cap.setBackground('#F4F1EC');
    pestanya.setFrozenRows(1);
    pestanya.setColumnWidth(1, 90);   // Data
    pestanya.setColumnWidth(2, 60);   // Hora
    pestanya.setColumnWidth(10, 320); // Missatge
  }
  return pestanya;
}

function registraError(err, e) {
  var full = SpreadsheetApp.openById(FULL_ID);
  var pestanya = full.getSheetByName('Errors') || full.insertSheet('Errors');
  if (pestanya.getLastRow() === 0) pestanya.appendRow(['Quan', 'Error', 'Contingut rebut']);
  pestanya.appendRow([
    new Date(),
    String(err),
    e && e.postData ? String(e.postData.contents).slice(0, 800) : '(sense contingut)'
  ]);
}

// ═══════════════════════════════════════════════════════════════════════════
//  AVISAR
// ═══════════════════════════════════════════════════════════════════════════

function avisa(d) {
  var qui = [text(d.nom), text(d.cognoms)].join(' ').trim() || 'Algú sense nom';
  var etiqueta = PESTANYES[String(d.tipus || '').toLowerCase()] || PESTANYA_PER_DEFECTE;

  var files = [
    ['Nom', qui],
    ['Mòbil', text(d.mobil)],
    ['Correu', text(d.correu)],
    ['Club', text(d.club)],
    ['Interès', text(d.interes)],
    ['Missatge', text(d.missatge)],
    ['Pàgina', text(d.pagina)]
  ].filter(function (f) { return f[1]; });

  var cos =
    '<div style="font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;' +
    'max-width:520px;color:#10100E;line-height:1.6">' +
    '<p style="font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#A8040E;margin:0 0 6px">' +
    etiqueta + '</p>' +
    '<h2 style="font-size:21px;margin:0 0 18px">' + escapa(qui) + '</h2>' +
    '<table style="border-collapse:collapse;width:100%;font-size:14px">' +
    files.map(function (f) {
      return '<tr>' +
        '<td style="padding:7px 14px 7px 0;color:#6E6A63;white-space:nowrap;vertical-align:top;' +
        'border-bottom:1px solid #EAE6DE">' + f[0] + '</td>' +
        '<td style="padding:7px 0;border-bottom:1px solid #EAE6DE">' + escapa(f[1]) + '</td></tr>';
    }).join('') +
    '</table>' +
    '<p style="margin:20px 0 0"><a href="' + fullUrl() + '" ' +
    'style="color:#A8040E">Obrir el full de contactes →</a></p>' +
    '<p style="margin:16px 0 0;font-size:12px;color:#6E6A63">' +
    (d.consentiment ? 'Ha acceptat el tractament de dades.' : 'ATENCIÓ: sense consentiment marcat.') +
    '</p></div>';

  var opcions = {
    to: AVIS_A,
    subject: 'Nou contacte · ' + etiqueta + ' · ' + qui,
    htmlBody: cos,
    name: 'Web CB Grup Barna'
  };
  if (AVIS_CC) opcions.cc = AVIS_CC;
  if (d.correu) opcions.replyTo = String(d.correu);

  MailApp.sendEmail(opcions);
}

// ═══════════════════════════════════════════════════════════════════════════
//  AJUDES
// ═══════════════════════════════════════════════════════════════════════════

function text(v) {
  if (v === null || v === undefined) return '';
  if (Array.isArray(v)) return v.join(', ');
  return String(v).trim().slice(0, 2000);
}

function escapa(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function fullUrl() {
  try { return SpreadsheetApp.openById(FULL_ID).getUrl(); } catch (e) { return ''; }
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

// ═══════════════════════════════════════════════════════════════════════════
//  PROVA · executa-la des de l'editor per veure si tot funciona abans de
//  tocar la web. Escriu una fila de mentida i envia un correu de mentida.
// ═══════════════════════════════════════════════════════════════════════════

function prova() {
  var fals = {
    tipus: 'informacio',
    nom: 'Prova', cognoms: 'De Prova',
    mobil: '600000000', correu: AVIS_A,
    interes: 'Escoleta (4-7 anys)',
    missatge: 'Fila de prova. Es pot esborrar.',
    consentiment: true,
    pagina: '/', font: 'prova manual'
  };
  var fila = desa(fals);
  if (ENVIA_CORREU) avisa(fals);
  Logger.log('Escrita la fila ' + fila + ' i enviat l\'avís a ' + AVIS_A);
}
