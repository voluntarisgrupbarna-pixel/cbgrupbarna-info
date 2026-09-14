/**
 * CB Grup Barna · Portes Obertes (Escoleta + nenes 2018) · reserva de plaça
 *                 + Proves d'accés de Setmana Santa · sol·licitud
 * ──────────────────────────────────────────────────────────────────────────
 * Aquest fitxer NO s'executa al web: és el codi que ha de viure a Google
 * Apps Script. El web només hi envia un POST amb JSON (js/portes-obertes.js
 * i js/proves-acces.js). Un sol desplegament serveix els dos formularis: el
 * camp `source` diu quin és ('portes-obertes' o 'proves-acces').
 *
 * DES DEL 13/09/2026 les Portes Obertes només admeten dos grups:
 *   · Escoleta (4 a 8 anys, nascuts del 2018 al 2022)
 *   · Nenes nascudes el 2018 (generació Premini femení)
 * La resta de categories no reserva aquí: demana prova d'accés per a la
 * Setmana Santa de 2027 a /proves-acces/, que arriba al mateix script amb
 * source: 'proves-acces' i va a un full a part («Proves d'accés»).
 *
 * Per a una reserva de Portes Obertes fa quatre coses, per aquest ordre:
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
var AVIS_A = 'voluntarisgrupbarna@gmail.com';

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
  '2026-09-19': 45,
  '2026-09-26': 45
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
  'Missatge', 'Idioma', 'Origen', 'Grup'
];

/** Els dissabtes que ofereix el formulari. Les Portes Obertes arrenquen el
    19 de setembre a les 9 h; els dissabtes anteriors no s'ofereixen. */
var DISSABTES = {
  '2026-09-19': { etiqueta: '19 de setembre', hora: 9 },
  '2026-09-26': { etiqueta: '26 de setembre', hora: 9 }
};

/**
 * Els dos únics grups que poden reservar a Portes Obertes, i quins anys de
 * naixement accepta cadascun. El navegador ja ho comprova, però el que
 * passa pel navegador es pot falsejar: aquesta és la comprovació que mana.
 */
var GRUPS = {
  'escoleta':   { etiqueta: 'Escoleta (4 a 8 anys)',            anys: [2018, 2019, 2020, 2021, 2022] },
  'nenes-2018': { etiqueta: 'Nenes 2018 · Premini femení',      anys: [2018] }
};

/** Full on van les sol·licituds de prova d'accés (Setmana Santa 2027). */
var PROVES_FULLA = 'Proves d\'accés';

var PROVES_CAPCALERES = [
  'Data de la sol·licitud', 'Nom del jugador/a', 'Any de naixement', 'Equip',
  'Categoria orientativa 27-28', 'Club actual', 'Anys jugant', 'Posició',
  'Disponibilitat', 'Qui apunta', 'Correu', 'Telèfon', 'Missatge', 'Idioma', 'Origen'
];

/**
 * Categoria orientativa per a la temporada 2027-28 segons l'any de
 * naixement (model FCBQ: Premini 2 anys, Mini 2, Preinfantil 1, Infantil 1,
 * Cadet 2, Júnior 2). Només orienta: l'equip definitiu el decideix la
 * direcció esportiva després de la prova.
 */
function categoria2728(any) {
  var a = parseInt(any, 10);
  if (!a) return '';
  if (a >= 2019) return 'Escoleta';
  if (a >= 2018) return 'Premini';
  if (a >= 2016) return 'Mini';
  if (a === 2015) return 'Preinfantil';
  if (a === 2014) return 'Infantil';
  if (a >= 2012) return 'Cadet';
  if (a >= 2010) return 'Júnior';
  if (a >= 2005) return 'Sub-22 / Sènior';
  return 'Sènior';
}

/**
 * Obrir l'URL /exec al navegador respon aquí: diu si l'script veu la full,
 * si pot enviar correu, si arriba al calendari i quantes places queden.
 */
function doGet() {
  var estat = { ok: true, servei: 'Portes Obertes (Escoleta + nenes 2018) i Proves d\'accés · CB Grup Barna' };
  estat.grups_portes_obertes = Object.keys(GRUPS);
  try {
    var full = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(FULLA);
    estat.full = full ? 'sí' : 'encara no (es crea a la primera reserva)';
    estat.reserves = full ? Math.max(0, full.getLastRow() - 1) : 0;
    estat.places_per_dissabte = PLACES_PER_DISSABTE;
    estat.places_lliures = placesLliures();
    estat.ocupacio_percent = ocupacio();
    var proves = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(PROVES_FULLA);
    estat.proves_acces_rebudes = proves ? Math.max(0, proves.getLastRow() - 1) : 0;
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
    nom: 'PROVA · esborra aquesta fila', edat: '6', any: '2020', grup: 'escoleta',
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

  // Les sol·licituds de prova d'accés (/proves-acces/) entren pel mateix
  // desplegament però són una altra cosa: full propi, sense places ni
  // calendari. Es despatxen aquí i no toquen res de les Portes Obertes.
  if (net(d.source) === 'proves-acces') {
    return desaProvaAcces(d);
  }

  // Només poden reservar l'Escoleta i les nenes del 2018. Un any de
  // naixement que no quadri amb el grup es rebutja aquí, encara que el
  // navegador ja ho hagi filtrat.
  //
  // GRUP_OBLIGATORI: mentre la web antiga (sense el camp `grup`) sigui live,
  // una reserva sense grup passa igual, perquè si no cap família podria
  // reservar entre el desplegament de l'script i la publicació del web nou.
  // Quan la web nova sigui a main, posa-ho a true i torna a desplegar.
  var GRUP_OBLIGATORI = false;
  if (net(d.grup) || GRUP_OBLIGATORI) {
    var grup = GRUPS[net(d.grup)];
    if (!grup) {
      return resposta({ ok: false, error: 'grup' });
    }
    if (grup.anys.indexOf(parseInt(net(d.any), 10)) === -1) {
      return resposta({ ok: false, error: 'any_fora_del_grup', grup: net(d.grup) });
    }
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
    net(d.missatge), net(d.idioma), net(d.source), etiquetaGrup(d.grup)
  ];
}

/** De 'nenes-2018' a 'Nenes 2018 · Premini femení'. */
function etiquetaGrup(valor) {
  var g = GRUPS[net(valor)];
  return g ? g.etiqueta : net(valor);
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
  // El full es va crear amb 12 columnes; la 13a («Grup») és del 13/09/2026.
  // Si la capçalera és curta, s'hi escriuen les que falten sense moure res.
  if (full.getLastColumn() < CAPCALERES.length) {
    full.getRange(1, 1, 1, CAPCALERES.length).setValues([CAPCALERES]).setFontWeight('bold');
  }
  full.appendRow(fila);
}

/**
 * L'avís al club, amb totes les dades i un botó per reenviar-ho al WhatsApp.
 * Un Apps Script no pot enviar WhatsApp per si sol: el que fa és deixar
 * l'enllaç wa.me amb el missatge ja escrit, a un clic.
 */
function avisaClub(d) {
  var assumpte = 'Portes Obertes · ' + net(d.nom) + ' (' + net(d.edat) + ' anys · ' + etiquetaGrup(d.grup) + ')';
  var linies = [
    'Reserva nova per a les Portes Obertes de l\'Escoleta.',
    '',
    'Nen/a:        ' + net(d.nom),
    'Edat:         ' + net(d.edat) + ' anys',
    'Any:          ' + net(d.any),
    'Grup:         ' + etiquetaGrup(d.grup),
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
    ' · ' + etiquetaGrup(d.grup) +
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
      'Grup: ' + etiquetaGrup(d.grup) + '\n' +
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
    .replace('{grup}', (t.grups && t.grups[net(d.grup)]) || t.grups.escoleta)
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
    grups: { 'escoleta': 'Escoleta', 'nenes-2018': 'nenes nascudes el 2018 (Premini femení)' },
    assumpte: 'Plaça reservada · Portes Obertes del CB Grup Barna',
    cap_dia: 'el dia que ens diguis',
    wa_boto: 'Escriu-nos al WhatsApp',
    wa_text: 'Hola! Tinc una pregunta sobre les Portes Obertes ({nom}).',
    cos:
      'Hola {tutor},\n\n' +
      'Ja tenim la plaça de {nom} ({edat} anys) reservada per a les Portes ' +
      'Obertes · {grup}. Dies que ens has dit: {dissabtes}.\n\n' +
      'On i quan: La Nau del Clot, Carrer de la Llacuna 170-172, a les 9 h. ' +
      'Veniu deu minuts abans i pregunteu per les Portes Obertes.\n\n' +
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
    grups: { 'escoleta': 'Escoleta', 'nenes-2018': 'niñas nacidas en 2018 (Premini femenino)' },
    assumpte: 'Plaza reservada · Puertas Abiertas del CB Grup Barna',
    cap_dia: 'el día que nos digas',
    wa_boto: 'Escríbenos al WhatsApp',
    wa_text: '¡Hola! Tengo una pregunta sobre las Puertas Abiertas ({nom}).',
    cos:
      'Hola {tutor}:\n\n' +
      'Ya tenemos la plaza de {nom} ({edat} años) reservada para las Puertas ' +
      'Abiertas · {grup}. Días que nos has dicho: {dissabtes}.\n\n' +
      'Dónde y cuándo: La Nau del Clot, Carrer de la Llacuna 170-172, a las ' +
      '9 h. Venid diez minutos antes y preguntad por las Puertas Abiertas.\n\n' +
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
    grups: { 'escoleta': 'Escoleta', 'nenes-2018': 'girls born in 2018 (U10 girls)' },
    assumpte: 'Place reserved · CB Grup Barna Open Days',
    cap_dia: 'the day you tell us',
    wa_boto: 'Message us on WhatsApp',
    wa_text: 'Hi! I have a question about the Open Days ({nom}).',
    cos:
      'Hi {tutor},\n\n' +
      '{nom} ({edat} years old) has a place reserved for the Open Days · ' +
      '{grup}. Days you told us about: {dissabtes}.\n\n' +
      'Where and when: La Nau del Clot, Carrer de la Llacuna 170-172, at ' +
      '9 am. Come ten minutes early and ask for the Open Days.\n\n' +
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

/* ══════════════════════════════════════════════════════════════════════════
   PROVES D'ACCÉS · Setmana Santa 2027
   Sol·licituds del formulari /proves-acces/ (source: 'proves-acces').
   Full propi, sense comptador de places ni esdeveniment de calendari: les
   dates concretes de cada prova les confirma el club per correu.
   ══════════════════════════════════════════════════════════════════════════ */

function desaProvaAcces(d) {
  var any = parseInt(net(d.any), 10);
  if (!net(d.nom) || !net(d.tutor) || !net(d.correu) || !any) {
    return resposta({ ok: false, error: 'camps' });
  }
  // L'Escoleta i les nenes del 2018 van a Portes Obertes, no aquí.
  if (any >= 2019 || (any === 2018 && net(d.equip) === 'femeni')) {
    return resposta({ ok: false, error: 'va_a_portes_obertes' });
  }

  var fila = [
    new Date(), net(d.nom), net(d.any), etiquetaEquip(d.equip), categoria2728(any),
    net(d.club), net(d.anysJugant), net(d.posicio), net(d.disponibilitat),
    net(d.tutor), net(d.correu), net(d.telefon), net(d.missatge), net(d.idioma), net(d.source)
  ];
  var doc = SpreadsheetApp.getActiveSpreadsheet();
  var full = doc.getSheetByName(PROVES_FULLA);
  if (!full) {
    full = doc.insertSheet(PROVES_FULLA);
    full.appendRow(PROVES_CAPCALERES);
    full.getRange(1, 1, 1, PROVES_CAPCALERES.length).setFontWeight('bold');
    full.setFrozenRows(1);
  }
  full.appendRow(fila);

  try { avisaClubProva(d); } catch (err) {}
  try { confirmaFamiliaProva(d); } catch (err) {}
  return resposta({ ok: true, categoria: categoria2728(any) });
}

function etiquetaEquip(v) {
  v = net(v);
  return v === 'femeni' ? 'Femení' : v === 'masculi' ? 'Masculí' : v;
}

function avisaClubProva(d) {
  var cat = categoria2728(net(d.any));
  var assumpte = 'Prova d\'accés · ' + net(d.nom) + ' (' + net(d.any) + ' · ' + etiquetaEquip(d.equip) + ' · ' + cat + ')';
  var linies = [
    'Sol·licitud nova de prova d\'accés per a la Setmana Santa 2027.',
    '',
    'Jugador/a:      ' + net(d.nom),
    'Any:            ' + net(d.any) + '  →  ' + cat + ' (orientatiu 27-28)',
    'Equip:          ' + etiquetaEquip(d.equip),
    'Club actual:    ' + (net(d.club) || '—'),
    'Anys jugant:    ' + (net(d.anysJugant) || '—'),
    'Posició:        ' + (net(d.posicio) || '—'),
    'Disponibilitat: ' + (net(d.disponibilitat) || '—'),
    'Qui apunta:     ' + net(d.tutor),
    'Correu:         ' + net(d.correu),
    'Telèfon:        ' + (net(d.telefon) || '—'),
    'Idioma web:     ' + net(d.idioma),
    '',
    'Missatge:',
    (net(d.missatge) || '—')
  ];
  var text = linies.join('\n');
  var resum =
    'Prova d\'accés SS27 · ' + net(d.nom) + ' (' + net(d.any) + ', ' + etiquetaEquip(d.equip) + ', ' + cat + ')' +
    (net(d.club) ? ' · ve de ' + net(d.club) : ' · sense club') +
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
    'La fila és al full «' + escapaHtml(PROVES_FULLA) + '». Cal respondre amb el dia i l\'hora de la prova.</p>';
  MailApp.sendEmail({
    to: AVIS_A, subject: assumpte, body: text + '\n\nWhatsApp: ' + wa,
    htmlBody: html, name: REMITENT, replyTo: net(d.correu) || AVIS_A
  });
}

function confirmaFamiliaProva(d) {
  var correu = net(d.correu);
  if (!correu) return;
  var t = TEXTOS_PROVES[net(d.idioma)] || TEXTOS_PROVES.ca;
  var cos = t.cos
    .replace('{tutor}', net(d.tutor) || '')
    .replace('{nom}', net(d.nom) || '')
    .replace('{any}', net(d.any) || '')
    .replace('{categoria}', categoria2728(net(d.any)) || '');
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

var TEXTOS_PROVES = {
  ca: {
    assumpte: 'Sol·licitud rebuda · Prova d\'accés Setmana Santa 2027 · CB Grup Barna',
    wa_boto: 'Escriu-nos al WhatsApp',
    wa_text: 'Hola! Tinc una pregunta sobre la prova d\'accés de Setmana Santa ({nom}).',
    cos:
      'Hola {tutor},\n\n' +
      'Hem rebut la sol·licitud de prova d\'accés de {nom} (any {any}) per a la ' +
      'temporada 2027-28. Categoria orientativa: {categoria}.\n\n' +
      'Les proves es fan durant les vacances de Setmana Santa de 2027 a La Nau ' +
      'del Clot (Carrer de la Llacuna 170-172). Abans de Setmana Santa t\'escriurem ' +
      'amb el dia i l\'hora que li toquen: no cal que facis res més ara.\n\n' +
      'Què cal portar el dia de la prova: roba d\'esport, esportives de pista i ' +
      'una ampolla d\'aigua. La pilota la posem nosaltres.\n\n' +
      'Si tens qualsevol dubte, respon aquest correu o escriu-nos al ' +
      'WhatsApp del club: +34 698 425 153.\n\n' +
      'CB Grup Barna · La Nau del Clot\n' +
      'Carrer de la Llacuna 170-172, 08018 Barcelona'
  },
  es: {
    assumpte: 'Solicitud recibida · Prueba de acceso Semana Santa 2027 · CB Grup Barna',
    wa_boto: 'Escríbenos al WhatsApp',
    wa_text: '¡Hola! Tengo una pregunta sobre la prueba de acceso de Semana Santa ({nom}).',
    cos:
      'Hola {tutor}:\n\n' +
      'Hemos recibido la solicitud de prueba de acceso de {nom} (año {any}) para la ' +
      'temporada 2027-28. Categoría orientativa: {categoria}.\n\n' +
      'Las pruebas se hacen durante las vacaciones de Semana Santa de 2027 en La Nau ' +
      'del Clot (Carrer de la Llacuna 170-172). Antes de Semana Santa te escribiremos ' +
      'con el día y la hora que le tocan: ahora no hace falta que hagas nada más.\n\n' +
      'Qué hay que traer el día de la prueba: ropa de deporte, zapatillas de pista y ' +
      'una botella de agua. El balón lo ponemos nosotros.\n\n' +
      'Si tienes cualquier duda, responde a este correo o escríbenos al ' +
      'WhatsApp del club: +34 698 425 153.\n\n' +
      'CB Grup Barna · La Nau del Clot\n' +
      'Carrer de la Llacuna 170-172, 08018 Barcelona'
  },
  en: {
    assumpte: 'Request received · Easter 2027 tryout · CB Grup Barna',
    wa_boto: 'Message us on WhatsApp',
    wa_text: 'Hi! I have a question about the Easter tryout ({nom}).',
    cos:
      'Hi {tutor},\n\n' +
      'We have received the tryout request for {nom} (born {any}) for the ' +
      '2027-28 season. Indicative age group: {categoria}.\n\n' +
      'Tryouts take place during the Easter school holidays of 2027 at La Nau ' +
      'del Clot (Carrer de la Llacuna 170-172). We will email you before Easter ' +
      'with the day and time: there is nothing else to do for now.\n\n' +
      'What to bring on the day: sports clothes, indoor trainers and a water ' +
      'bottle. We provide the ball.\n\n' +
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
