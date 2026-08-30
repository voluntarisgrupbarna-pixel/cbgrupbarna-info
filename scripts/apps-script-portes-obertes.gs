/**
 * CB Grup Barna · Portes Obertes de l'Escoleta · reserva de plaça
 * ──────────────────────────────────────────────────────────────────────────
 * Aquest fitxer NO s'executa al web: és el codi que ha de viure a Google
 * Apps Script. El web només hi envia un POST amb JSON (js/portes-obertes.js).
 *
 * Fa quatre coses, per aquest ordre:
 *   1. Escriu una fila a la full de càlcul de reserves.
 *   2. Envia un avís al club (AVIS_A) amb TOTES les dades i un botó
 *      «Obrir al WhatsApp» amb el missatge ja escrit.
 *   3. Crea un esdeveniment al calendari del club per al dissabte triat.
 *   4. Envia la confirmació a la família.
 *
 * L'ordre importa: si el calendari o la confirmació peten, la fila ja és a
 * la full i l'avís al club ja ha sortit. No es perd cap reserva.
 *
 * ─── COM ES POSA EN MARXA (10 minuts, una sola vegada) ────────────────────
 *  1. Crea un full de càlcul nou a Google Drive amb el compte del club i
 *     posa-li de nom «Portes Obertes · reserves».
 *  2. Dins del full: Extensions → Apps Script.
 *  3. Esborra el que hi hagi i enganxa TOT aquest fitxer.
 *  4. Repassa la configuració de sota: AVIS_A, WHATSAPP_CLUB,
 *     PLACES_PER_DISSABTE i CALENDARI_ID.
 *  5. Desa i fes Desplega → Nou desplegament → tipus «Aplicació web»:
 *        Executa com a:        jo (el compte del club)
 *        Qui hi té accés:      Qualsevol
 *     Google demanarà permisos (full, correu i calendari): accepta'ls.
 *  6. Copia l'URL que acaba en /exec i enganxa'l a js/canals.js, al camp
 *     `portesObertesEndpoint`.
 *
 * Per comprovar-ho sense omplir res: obre l'URL /exec al navegador. Ha de
 * respondre "ok": true i dir quantes places queden. Per provar els correus
 * de veritat, tria provaReserva a l'editor i clica Executa.
 * ─────────────────────────────────────────────────────────────────────────
 */

/** On arriba l'avís de cada reserva nova. */
var AVIS_A = 'marqueting@cbgrupbarna.info';

/** El WhatsApp del club, en format internacional sense + ni espais.
    Serveix per muntar l'enllaç wa.me del correu d'avís. */
var WHATSAPP_CLUB = '34698425153';

/** Nom que veurà qui rebi els correus. */
var REMITENT = 'CB Grup Barna';

/** Full de dins del document on s'escriuen les files. */
var FULLA = 'Reserves';

/** Places PER DISSABTE (no en total): cada torn admet 50 nens i nenes.
    Quan un dissabte s'omple, deixa d'acceptar reserves per aquell dia però
    els altres segueixen oberts. */
var PLACES_PER_DISSABTE = 50;

/**
 * Places de cada torn que ja estan compromeses fora del web: les que s'han
 * apuntat per WhatsApp, al pavelló o de la temporada passada. El comptador
 * les suma a les files de la full, de manera que el que surt publicat («en
 * queden 15») és la disponibilitat REAL i baixa sola a cada reserva nova.
 *
 * Actualitza aquests números quan es tanqui alguna plaça fora del web; si
 * un dia no n'hi ha cap de compromesa, posa-hi 0 i el comptador dirà 50.
 */
var RESERVES_FORA_DEL_WEB = {
  '2026-09-19': 35,
  '2026-09-26': 35
};

/** Calendari on es creen els esdeveniments. 'primary' és l'agenda principal
    del compte que desplega l'script. Si el club té un calendari propi per a
    l'Escoleta, enganxa-hi el seu ID (Configuració del calendari → ID). */
var CALENDARI_ID = 'primary';

/** Durada de la sessió de prova, en hores, per a l'esdeveniment. */
var DURADA_HORES = 1.5;

var CAPCALERES = [
  'Data de la reserva', 'Nom del nen/a', 'Edat', 'Any de naixement',
  'Ha jugat abans', 'Dissabtes triats', 'Qui apunta', 'Correu', 'Telèfon',
  'Missatge', 'Idioma', 'Origen'
];

/** Els dissabtes que ofereix el formulari. Les Portes Obertes arrenquen el
    19 de setembre a les 9 h; els dissabtes anteriors no s'ofereixen. */
var DISSABTES = {
  '2026-09-19': { etiqueta: '19 de setembre', hora: 9 },
  '2026-09-26': { etiqueta: '26 de setembre', hora: 9 }
};

/**
 * Obrir l'URL /exec al navegador respon aquí: diu si l'script veu la full,
 * si pot enviar correu, si arriba al calendari i quantes places queden.
 */
function doGet() {
  var estat = { ok: true, servei: 'Portes Obertes de l\'Escoleta · CB Grup Barna' };
  try {
    var full = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(FULLA);
    estat.full = full ? 'sí' : 'encara no (es crea a la primera reserva)';
    estat.reserves = full ? Math.max(0, full.getLastRow() - 1) : 0;
    estat.places_per_dissabte = PLACES_PER_DISSABTE;
    estat.places_lliures = placesLliures();
    estat.ocupacio_percent = ocupacio();
  } catch (err) {
    estat.ok = false;
    estat.full = 'ERROR: ' + err;
  }
  try {
    estat.correus_que_puc_enviar_avui = MailApp.getRemainingDailyQuota();
  } catch (err) {
    estat.ok = false;
    estat.correus_que_puc_enviar_avui = 'ERROR: ' + err;
  }
  try {
    var cal = CalendarApp.getCalendarById(CALENDARI_ID);
    estat.calendari = cal ? cal.getName() : 'no el trobo: revisa CALENDARI_ID';
    if (!cal) estat.ok = false;
  } catch (err) {
    estat.ok = false;
    estat.calendari = 'ERROR: ' + err;
  }
  estat.avis_a = AVIS_A;
  estat.seguent_pas = estat.ok
    ? 'Tot correcte. Enganxa aquest URL a portesObertesEndpoint de js/canals.js.'
    : 'Alguna cosa falla: mira els ERROR de sobre.';
  return resposta(estat);
}

/**
 * Prova completa, per executar-la des de l'editor d'Apps Script. Escriu una
 * fila, envia els dos correus a AVIS_A i crea l'esdeveniment de calendari.
 * Esborra després la fila i l'esdeveniment de prova a mà.
 */
function provaReserva() {
  var fals = {
    nom: 'PROVA · esborra aquesta fila', edat: '6', any: '2020',
    jugat: 'no', dissabtes: '2026-09-19', tutor: 'Prova',
    correu: AVIS_A, telefon: '600000000', missatge: 'Fila de prova.',
    idioma: 'ca', source: 'prova'
  };
  desa(filaDe(fals));
  avisaClub(fals);
  try { creaEsdeveniments(fals); } catch (err) { Logger.log('calendari: ' + err); }
  confirmaFamilia(fals);
  Logger.log('Fet: fila, dos correus a ' + AVIS_A + ' i esdeveniment de calendari.');
}

function doPost(e) {
  var d = {};
  try {
    d = JSON.parse(e.postData.contents) || {};
  } catch (err) {
    return resposta({ ok: false, error: 'json' });
  }

  // El taulell de places es mira aquí i no al navegador: el comptador del
  // web és informatiu i es podria falsejar. Aquesta és la comprovació que
  // mana, i evita acceptar la plaça 51 de cap torn.
  var lliures = placesLliures();
  var triats = String(net(d.dissabtes) || '').split(',').map(function (s) { return s.trim(); })
                 .filter(function (s) { return DISSABTES[s]; });
  if (!triats.length) {
    return resposta({ ok: false, error: 'cap_dissabte', places_lliures: lliures });
  }
  var plens = triats.filter(function (c) { return lliures[c] <= 0; });
  if (plens.length === triats.length) {
    return resposta({ ok: false, error: 'sense_places', places_lliures: lliures });
  }

  desa(filaDe(d));

  // L'avís al club va primer: encara que la resta peti, el club se
  // n'assabenta i pot trucar a mà.
  try { avisaClub(d); } catch (err) {}
  try { creaEsdeveniments(d); } catch (err) {}
  try { confirmaFamilia(d); } catch (err) {}

  return resposta({ ok: true, places_lliures: placesLliures(), ocupacio_percent: ocupacio() });
}

function filaDe(d) {
  return [
    new Date(),
    net(d.nom), net(d.edat), net(d.any), net(d.jugat),
    etiquetaDissabtes(d.dissabtes), net(d.tutor), net(d.correu), net(d.telefon),
    net(d.missatge), net(d.idioma), net(d.source)
  ];
}

/**
 * Places lliures de cada dissabte. Compta la columna «Dissabtes triats» de
 * la full: una reserva que ha triat els dos dies ocupa una plaça a cadascun.
 * Retorna { '2026-09-19': 48, '2026-09-26': 50 }.
 */
function placesLliures() {
  var lliures = {};
  for (var clau in DISSABTES) {
    lliures[clau] = PLACES_PER_DISSABTE - (RESERVES_FORA_DEL_WEB[clau] || 0);
  }

  var full = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(FULLA);
  if (!full || full.getLastRow() < 2) {
    for (var k0 in lliures) lliures[k0] = Math.max(0, lliures[k0]);
    return lliures;
  }

  // Columna 6 = «Dissabtes triats», segons CAPCALERES.
  var COL_DISSABTES = 6;
  var files = full.getRange(2, COL_DISSABTES, full.getLastRow() - 1, 1).getValues();
  for (var i = 0; i < files.length; i++) {
    var text = String(files[i][0] || '');
    for (var c in DISSABTES) {
      // A la full hi ha l'etiqueta llegible («19 de setembre»), no la clau.
      if (text.indexOf(DISSABTES[c].etiqueta) !== -1) lliures[c]--;
    }
  }
  for (var k in lliures) lliures[k] = Math.max(0, lliures[k]);
  return lliures;
}

/** Escriu la fila, creant el full i les capçaleres el primer cop. */
function desa(fila) {
  var doc = SpreadsheetApp.getActiveSpreadsheet();
  var full = doc.getSheetByName(FULLA);
  if (!full) {
    full = doc.insertSheet(FULLA);
    full.appendRow(CAPCALERES);
    full.getRange(1, 1, 1, CAPCALERES.length).setFontWeight('bold');
    full.setFrozenRows(1);
  }
  full.appendRow(fila);
}

/**
 * L'avís al club, amb totes les dades i un botó per reenviar-ho al WhatsApp.
 * Un Apps Script no pot enviar WhatsApp per si sol: el que fa és deixar
 * l'enllaç wa.me amb el missatge ja escrit, a un clic.
 */
function avisaClub(d) {
  var assumpte = 'Portes Obertes · ' + net(d.nom) + ' (' + net(d.edat) + ' anys)';
  var linies = [
    'Reserva nova per a les Portes Obertes de l\'Escoleta.',
    '',
    'Nen/a:        ' + net(d.nom),
    'Edat:         ' + net(d.edat) + ' anys',
    'Any:          ' + net(d.any),
    'Ha jugat:     ' + (net(d.jugat) === 'si' ? 'sí, ja ha jugat abans' : 'no, comença de zero'),
    'Dissabtes:    ' + etiquetaDissabtes(d.dissabtes),
    'Qui apunta:   ' + net(d.tutor),
    'Correu:       ' + net(d.correu),
    'Telèfon:      ' + (net(d.telefon) || '—'),
    'Idioma web:   ' + net(d.idioma),
    '',
    'Missatge:',
    (net(d.missatge) || '—'),
    '',
    'Places lliures per torn: ' + resumLliures()
  ];
  var text = linies.join('\n');

  // El mateix resum, comprimit, per enviar-lo pel WhatsApp d'un clic.
  var resum =
    'Portes Obertes · ' + net(d.nom) + ' (' + net(d.edat) + ' anys, ' + net(d.any) + ')' +
    ' · ' + etiquetaDissabtes(d.dissabtes) +
    ' · ' + (net(d.jugat) === 'si' ? 'ja ha jugat' : 'comença de zero') +
    ' · ' + net(d.tutor) + ' · ' + net(d.correu) +
    (net(d.telefon) ? ' · ' + net(d.telefon) : '');
  var wa = 'https://wa.me/' + WHATSAPP_CLUB + '?text=' + encodeURIComponent(resum);

  var html =
    '<pre style="font:14px/1.6 -apple-system,BlinkMacSystemFont,system-ui,sans-serif;' +
    'white-space:pre-wrap;margin:0 0 20px">' + escapaHtml(text) + '</pre>' +
    '<a href="' + wa + '" style="display:inline-block;background:#25D366;color:#fff;' +
    'font:600 14px/1 -apple-system,BlinkMacSystemFont,system-ui,sans-serif;' +
    'text-decoration:none;padding:14px 22px;border-radius:6px">' +
    'Obrir al WhatsApp amb les dades</a>' +
    '<p style="font:12px/1.6 -apple-system,system-ui,sans-serif;color:#6B6560;margin-top:16px">' +
    'La fila ja és a la full de càlcul i l\'esdeveniment, al calendari del club.</p>';

  MailApp.sendEmail({
    to: AVIS_A, subject: assumpte, body: text + '\n\nWhatsApp: ' + wa,
    htmlBody: html, name: REMITENT, replyTo: net(d.correu) || AVIS_A
  });
}

/**
 * Un esdeveniment per cada dissabte triat, al calendari del club. Hi posa la
 * família com a convidada perquè li aparegui a la seva agenda.
 */
function creaEsdeveniments(d) {
  var cal = CalendarApp.getCalendarById(CALENDARI_ID);
  if (!cal) return;
  var triats = String(net(d.dissabtes) || '').split(',');
  for (var i = 0; i < triats.length; i++) {
    var clau = triats[i].trim();
    var dia = DISSABTES[clau];
    if (!dia) continue;
    var parts = clau.split('-');
    var inici = new Date(+parts[0], +parts[1] - 1, +parts[2], dia.hora, 0, 0);
    var fi = new Date(inici.getTime() + DURADA_HORES * 3600 * 1000);
    var titol = 'Portes Obertes · ' + net(d.nom) + ' (' + net(d.edat) + ' anys)';
    var detall =
      'Nen/a: ' + net(d.nom) + ' · ' + net(d.edat) + ' anys (' + net(d.any) + ')\n' +
      'Ha jugat abans: ' + (net(d.jugat) === 'si' ? 'sí' : 'no') + '\n' +
      'Qui apunta: ' + net(d.tutor) + '\n' +
      'Correu: ' + net(d.correu) + '\n' +
      'Telèfon: ' + (net(d.telefon) || '—');
    var opcions = { description: detall, location: 'La Nau del Clot · Carrer de la Llacuna 170-172, 08018 Barcelona' };
    var correu = net(d.correu);
    if (correu) opcions.guests = correu;
    cal.createEvent(titol, inici, fi, opcions);
  }
}

/**
 * La confirmació a la família, amb un botó per escriure'ns al WhatsApp: si
 * tenen un dubte, que no hagin de buscar el número enlloc.
 */
function confirmaFamilia(d) {
  var correu = net(d.correu);
  if (!correu) return;
  var t = TEXTOS[net(d.idioma)] || TEXTOS.ca;
  var cos = t.cos
    .replace('{tutor}', net(d.tutor) || '')
    .replace('{nom}', net(d.nom) || '')
    .replace('{edat}', net(d.edat) || '')
    .replace('{dissabtes}', etiquetaDissabtes(d.dissabtes) || t.cap_dia);

  var salutacio = t.wa_text.replace('{nom}', net(d.nom) || '');
  var wa = 'https://wa.me/' + WHATSAPP_CLUB + '?text=' + encodeURIComponent(salutacio);
  var html =
    '<div style="font:15px/1.65 -apple-system,BlinkMacSystemFont,system-ui,sans-serif;color:#46433f">' +
    '<pre style="font:inherit;white-space:pre-wrap;margin:0 0 22px">' + escapaHtml(cos) + '</pre>' +
    '<a href="' + wa + '" style="display:inline-block;background:#25D366;color:#fff;' +
    'font:600 14px/1 -apple-system,BlinkMacSystemFont,system-ui,sans-serif;' +
    'text-decoration:none;padding:14px 22px;border-radius:6px">' +
    escapaHtml(t.wa_boto) + '</a></div>';

  MailApp.sendEmail({ to: correu, subject: t.assumpte, body: cos + '\n\n' + t.wa_boto + ': ' + wa,
                      htmlBody: html, name: REMITENT, replyTo: AVIS_A });
}

/**
 * Percentatge de places ocupades de cada torn, per publicar-lo al web.
 * Retorna { '2026-09-19': 70, ... } — enter, per no ensenyar decimals.
 */
function ocupacio() {
  var l = placesLliures();
  var pct = {};
  for (var c in DISSABTES) {
    pct[c] = Math.round((PLACES_PER_DISSABTE - l[c]) / PLACES_PER_DISSABTE * 100);
  }
  return pct;
}

/** '19 de setembre: 15 lliures (70% ple) · 26 de setembre: 15 lliures (70% ple)' */
function resumLliures() {
  var l = placesLliures(), o = ocupacio();
  var trossos = [];
  for (var c in DISSABTES) {
    trossos.push(DISSABTES[c].etiqueta + ': ' + l[c] + ' lliures (' + o[c] + '% ple)');
  }
  return trossos.join(' · ');
}

/** De '2026-09-19,2026-09-26' a '19 de setembre i 26 de setembre'. */
function etiquetaDissabtes(valor) {
  var triats = String(net(valor) || '').split(',');
  var noms = [];
  for (var i = 0; i < triats.length; i++) {
    var dia = DISSABTES[triats[i].trim()];
    if (dia) noms.push(dia.etiqueta);
  }
  if (!noms.length) return '';
  if (noms.length === 1) return noms[0];
  return noms.slice(0, -1).join(', ') + ' i ' + noms[noms.length - 1];
}

/* Confirmació en els tres idiomes del web: qui reserva en anglès no ha de
   rebre un correu en català. */
var TEXTOS = {
  ca: {
    assumpte: 'Plaça reservada · Portes Obertes de l\'Escoleta del CB Grup Barna',
    cap_dia: 'el dia que ens diguis',
    wa_boto: 'Escriu-nos al WhatsApp',
    wa_text: 'Hola! Tinc una pregunta sobre les Portes Obertes de l\'Escoleta ({nom}).',
    cos:
      'Hola {tutor},\n\n' +
      'Ja tenim la plaça de {nom} ({edat} anys) reservada per a les Portes ' +
      'Obertes de l\'Escoleta. Dies que ens has dit: {dissabtes}.\n\n' +
      'On i quan: La Nau del Clot, Carrer de la Llacuna 170-172, a les 9 h. ' +
      'Veniu deu minuts abans i pregunteu per l\'Escoleta.\n\n' +
      'Què cal portar: roba d\'esport, esportives i una ampolla d\'aigua. La ' +
      'pilota la posem nosaltres.\n\n' +
      'Si un dissabte no podeu venir, no cal avisar amb antelació: podeu ' +
      'provar qualsevol dissabte de setembre.\n\n' +
      'Si tens qualsevol dubte, respon aquest correu o escriu-nos al ' +
      'WhatsApp del club: +34 698 425 153.\n\n' +
      'CB Grup Barna · La Nau del Clot\n' +
      'Carrer de la Llacuna 170-172, 08018 Barcelona'
  },
  es: {
    assumpte: 'Plaza reservada · Puertas Abiertas de la Escoleta del CB Grup Barna',
    cap_dia: 'el día que nos digas',
    wa_boto: 'Escríbenos al WhatsApp',
    wa_text: '¡Hola! Tengo una pregunta sobre las Puertas Abiertas de la Escoleta ({nom}).',
    cos:
      'Hola {tutor}:\n\n' +
      'Ya tenemos la plaza de {nom} ({edat} años) reservada para las Puertas ' +
      'Abiertas de la Escoleta. Días que nos has dicho: {dissabtes}.\n\n' +
      'Dónde y cuándo: La Nau del Clot, Carrer de la Llacuna 170-172, a las ' +
      '9 h. Venid diez minutos antes y preguntad por la Escoleta.\n\n' +
      'Qué hay que traer: ropa de deporte, zapatillas y una botella de agua. ' +
      'El balón lo ponemos nosotros.\n\n' +
      'Si un sábado no podéis venir, no hace falta avisar: podéis probar ' +
      'cualquier sábado de septiembre.\n\n' +
      'Si tienes cualquier duda, responde a este correo o escríbenos al ' +
      'WhatsApp del club: +34 698 425 153.\n\n' +
      'CB Grup Barna · La Nau del Clot\n' +
      'Carrer de la Llacuna 170-172, 08018 Barcelona'
  },
  en: {
    assumpte: 'Place reserved · CB Grup Barna Escoleta Open Days',
    cap_dia: 'the day you tell us',
    wa_boto: 'Message us on WhatsApp',
    wa_text: 'Hi! I have a question about the Escoleta Open Days ({nom}).',
    cos:
      'Hi {tutor},\n\n' +
      '{nom} ({edat} years old) has a place reserved for the Escoleta Open ' +
      'Days. Days you told us about: {dissabtes}.\n\n' +
      'Where and when: La Nau del Clot, Carrer de la Llacuna 170-172, at ' +
      '9 am. Come ten minutes early and ask for the Escoleta.\n\n' +
      'What to bring: sports clothes, trainers and a water bottle. We bring ' +
      'the ball.\n\n' +
      'If you cannot make it one Saturday, no need to tell us in advance: ' +
      'you can try any Saturday in September.\n\n' +
      'Any questions, reply to this email or write to the club on WhatsApp: ' +
      '+34 698 425 153.\n\n' +
      'CB Grup Barna · La Nau del Clot\n' +
      'Carrer de la Llacuna 170-172, 08018 Barcelona'
  }
};

function net(v) {
  return String(v === undefined || v === null ? '' : v).slice(0, 2000).trim();
}

function escapaHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function resposta(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
