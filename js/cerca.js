/* ============================================================
   CB GRUP BARNA · Cercador
   ------------------------------------------------------------
   Cerca a tot el web sense servidor ni servei de tercers: es
   baixa /cerca-index.json (generat per
   .github/scripts/generate-search-index.py) la primera vegada
   que algú obre el cercador, i tota la resta passa al navegador.
   Cap consulta surt cap enfora: no cal consentiment de galetes
   ni s'envia res a Google, com a la resta del lloc.

   És «intel·ligent» en tres sentits, per aquest ordre:
     1. ENTÉN LA INTENCIÓ. «quant costa», «cuánto vale», «how much»
        i «preu» porten tots al mateix lloc, encara que la paraula
        no surti escrita a la pàgina.
     2. PERDONA. Accents, majúscules, «ç», «l·l» i una lletra mal
        posada («basquet», «escoleta», «entrenemant») no trenquen res.
     3. RESPON, no només enllaça. El web ja porta 460 preguntes
        amb la resposta escrita pel club, dins del JSON-LD de 98
        pàgines. El cercador les indexa i ensenya la que toca a
        dalt de tot, TAL QUAL està escrita, amb l'enllaç a la
        pàgina d'on surt. No hi ha cap model de llenguatge pel
        mig: no s'inventa res, no costa res i la pregunta no surt
        del navegador. Per sota hi ha les respostes escrites a mà
        d'aquest fitxer, per a les intencions que cap FAQ cobreix
        (contacte, portes obertes).

   Es pot fer servir de dues maneres:
     - Superposat: qualsevol pàgina que carregui aquest fitxer té
       el botó a la capçalera, ⌘K/Ctrl+K i la tecla «/».
     - A pàgina sencera: /cerca/ (element #cercaPagina).
   ============================================================ */
(function () {
  'use strict';

  var RUTA_INDEX = '/cerca-index.json';
  var MAX_RESULTATS = 12;
  var CLAU_RECENTS = 'cbgb-cerques';

  /* ---------- Idioma de la pàgina on som ---------- */
  var lang = (document.documentElement.lang || 'ca').slice(0, 2).toLowerCase();
  if (location.pathname.indexOf('/es/') === 0) lang = 'es';
  if (location.pathname.indexOf('/en/') === 0) lang = 'en';
  if (['ca', 'es', 'en'].indexOf(lang) < 0) lang = 'ca';

  /* ---------- Textos de la interfície ---------- */
  var T = {
    ca: {
      obrir: 'Cerca', titol: 'Què busques?',
      placeholder: 'Escoleta, horaris, un equip, com apuntar-s\'hi…',
      tancar: 'Tancar', cap: 'Cap resultat per',
      capAjuda: 'Prova amb menys paraules: «escoleta», «cadet», «campus», «preu».',
      suggeriments: 'Les més buscades', altresIdiomes: 'En altres idiomes',
      recents: 'Les teves darreres cerques', esborrar: 'esborrar',
      resposta: 'Resposta ràpida', respostaFaq: 'La resposta',
      fontFaq: 'Ho explica', relacionades: 'També s\'hi pregunta', carregant: 'Un moment…',
      error: 'Ara mateix no es pot cercar. Prova el menú de dalt.',
      resultats: 'resultats', unResultat: '1 resultat', veure: 'Veure-ho tot',
      pista: 'per moure\'t · Enter per obrir · Esc per sortir'
    },
    es: {
      obrir: 'Buscar', titol: '¿Qué buscas?',
      placeholder: 'Escoleta, horarios, un equipo, cómo apuntarse…',
      tancar: 'Cerrar', cap: 'Sin resultados para',
      capAjuda: 'Prueba con menos palabras: «escoleta», «cadete», «campus», «precio».',
      suggeriments: 'Lo más buscado', altresIdiomes: 'En otros idiomas',
      recents: 'Tus últimas búsquedas', esborrar: 'borrar',
      resposta: 'Respuesta rápida', respostaFaq: 'La respuesta',
      fontFaq: 'Lo explica', relacionades: 'También se pregunta', carregant: 'Un momento…',
      error: 'Ahora mismo no se puede buscar. Prueba el menú de arriba.',
      resultats: 'resultados', unResultat: '1 resultado', veure: 'Verlo todo',
      pista: 'para moverte · Enter para abrir · Esc para salir'
    },
    en: {
      obrir: 'Search', titol: 'What are you looking for?',
      placeholder: 'Escoleta, schedules, a team, how to join…',
      tancar: 'Close', cap: 'No results for',
      capAjuda: 'Try fewer words: “escoleta”, “under-16”, “camp”, “price”.',
      suggeriments: 'Most searched', altresIdiomes: 'In other languages',
      recents: 'Your recent searches', esborrar: 'clear',
      resposta: 'Quick answer', respostaFaq: 'The answer',
      fontFaq: 'Explained in', relacionades: 'People also ask', carregant: 'One moment…',
      error: 'Search is unavailable right now. Try the menu above.',
      resultats: 'results', unResultat: '1 result', veure: 'See everything',
      pista: 'to move · Enter to open · Esc to close'
    }
  }[lang];

  /* ============================================================
     1 · NORMALITZACIÓ
     «Bàsquet», «BASQUET», «basquet» i «Bâsquet» han de ser la
     mateixa paraula. La «l·l» catalana i la «ñ» castellana també.
     ============================================================ */
  function normalitza(s) {
    return (s || '')
      .toLowerCase()
      .replace(/l·l/g, 'll')
      .replace(/[·‧∙]/g, ' ')
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/ç/g, 'c')
      .replace(/[''’‘"“”]/g, ' ')
      .replace(/[^a-z0-9\s-]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  /* Paraules que no aporten res a cap dels tres idiomes. */
  var BUIDES = {};
  ('de del la el les els un una uns unes i o a al als amb per que quan com on ' +
   'els meu meva teu teva es se para por con del las los una unos unas y donde ' +
   'cuando como cuanto the of and for to in on at is are how what when where my ' +
   'your can i do does es en si no hi ha').split(' ').forEach(function (p) { BUIDES[p] = 1; });

  function paraules(s) {
    return normalitza(s).split(' ').filter(function (p) {
      return p.length > 1 && !BUIDES[p];
    });
  }

  // Per endevinar la intenció sí que compten les paraules buides: «quant»,
  // «cuánto» i «how much» no serveixen per casar text, però són justament
  // les que diuen què vol qui pregunta.
  function paraulesAmbBuides(s) {
    return normalitza(s).split(' ').filter(function (p) { return p.length > 1; });
  }

  /* ============================================================
     2 · VOCABULARI · el que la gent escriu → el que diu la web
     Aquesta taula és el cor del cercador. La web parla en la
     llengua del club («escoleta», «formatiu», «tecnificació»);
     les famílies escriuen «escuela», «mi hijo de 7 años»,
     «cuánto cuesta». Aquí es fa la traducció, en els tres idiomes.
     Afegir-hi una fila és la manera barata de millorar la cerca.
     ============================================================ */
  var SINONIMS = {
    escoleta: 'escoleta escuela escola school babybasket iniciacio pequenos petits little kids 4 5 6 7 8 anys anos years',
    apuntar: 'apuntar apuntarse inscripcio inscripcion inscribir inscribirse matricula matricular alta join sign signup register enrol enroll provar probar try prova',
    preu: 'preu preus precio precios cost coste costa cuesta cuestan vale valen val cuota quota quotes fee fees price prices tarifa tarifes pagar pagament pago payment quant cuanto much barat gratis gratuit',
    horari: 'horari horaris horario horarios schedule timetable hora hores dia dies entrenament entrenaments entrenamiento training quan cuando when',
    partit: 'partit partits partido partidos match matches game games calendari calendario calendar jornada resultat resultats resultado result classificacio clasificacion standings',
    equip: 'equip equips equipo equipos team teams plantilla roster categoria categories',
    campus: 'campus camp camps estiu verano summer nadal navidad christmas setmana santa vacances vacaciones holiday tecnificacio tecnificacion',
    femeni: 'femeni femenino femenina women womens girls noies chicas nenes basquet femeni',
    magics: 'magics magicos inclusiu inclusivo inclusive adaptat adaptado diversitat discapacitat especial',
    contacte: 'contacte contacto contact telefon telefono phone whatsapp mail correu email escriure hablar parlar',
    pista: 'pista pistes pavello pabellon poliesportiu polideportivo installacions instalaciones facilities gym gimnas adreca direccion address on donde where mapa arribar llegar',
    club: 'club qui som quienes somos about historia history 1965 anys aniversari junta directiva organigrama entrenador entrenadors coach coaches staff tecnic',
    patrocini: 'patrocini patrocinis patrocinador patrocinadors patrocinio sponsor sponsors partner partners empresa empreses empresas publicitat colaborar collaborate',
    fotos: 'fotos foto fotografies fotografias photos gallery galeria imatges imagenes',
    documents: 'document documents documentos assegurança seguro insurance autoritzacio autorizacion certificat certificado proteccio proteccion protection menor',
    tresxtres: '3x3 3 x 3 tresxtres torneig torneo tournament glories westfield street',
    blog: 'blog article articles articulo noticies noticias news consells consejos tips guia guide',
    edat: 'edat edad age anys anos years mini premini benjami infantil cadet junior senior sub categoria nen nena hijo hija fill filla nino'
  };

  /* De la intenció a la porta d'entrada: quan la consulta cau en
     una d'aquestes famílies, aquestes pàgines pugen. */
  var DESTINS = {
    escoleta: ['/escoleta/', '/cistella-petita/', '/basquet-formatiu/'],
    apuntar: ['/portes-obertes/', '/escoleta/', '/faq/'],
    preu: ['/faq/', '/escoleta/', '/campus/'],
    horari: ['/partits/calendaris/', '/partits/', '/partits/equips/'],
    partit: ['/partits/', '/partits/calendaris/', '/partits/equips/'],
    equip: ['/partits/equips/', '/basquet-formatiu/', '/femeni/'],
    campus: ['/campus/', '/tecnificacio-basquet-barcelona/'],
    femeni: ['/femeni/', '/premidonaesport/'],
    magics: ['/magics/'],
    contacte: ['/faq/', '/club/'],
    pista: ['/instal-lacions/', '/partits/calendaris/'],
    club: ['/club/', '/historia/', '/organigrama/'],
    patrocini: ['/patrocinadors/', '/empreses/', '/partners-mapa/'],
    fotos: ['/fotos/', '/galeria/'],
    documents: ['/documents/', '/proteccio-menor/'],
    tresxtres: ['/3x3/'],
    blog: ['/blog/', '/premsa/'],
    edat: ['/basquet-formatiu/', '/partits/equips/']
  };

  /* Índex invertit del vocabulari: paraula → famílies on surt. */
  var FAMILIA_DE = {};
  Object.keys(SINONIMS).forEach(function (fam) {
    SINONIMS[fam].split(' ').forEach(function (p) {
      if (!p) return;
      (FAMILIA_DE[p] = FAMILIA_DE[p] || []).push(fam);
    });
  });

  function familiesDe(termes) {
    var fam = {};
    termes.forEach(function (t) {
      (FAMILIA_DE[t] || []).forEach(function (f) { fam[f] = (fam[f] || 0) + 1; });
    });
    return fam;
  }

  /* ============================================================
     3 · RESPOSTES RÀPIDES
     Preguntes que mereixen una resposta, no una llista d'enllaços.
     ============================================================ */
  var RESPOSTES = [
    {
      quan: ['contacte'],
      ca: { t: 'Parla amb el club', d: 'WhatsApp +34 698 425 153 · @cbgrupbarna · El Clot, Barcelona', a: 'Escriure per WhatsApp' },
      es: { t: 'Habla con el club', d: 'WhatsApp +34 698 425 153 · @cbgrupbarna · El Clot, Barcelona', a: 'Escribir por WhatsApp' },
      en: { t: 'Talk to the club', d: 'WhatsApp +34 698 425 153 · @cbgrupbarna · El Clot, Barcelona', a: 'Message on WhatsApp' },
      href: 'https://api.whatsapp.com/send?phone=+34698425153'
    },
    {
      quan: ['apuntar', 'escoleta'],
      ca: { t: 'Vine a provar un entrenament', d: 'Portes obertes tot el setembre. Sense compromís i sense pagar res.', a: 'Portes obertes' },
      es: { t: 'Ven a probar un entrenamiento', d: 'Puertas abiertas todo septiembre. Sin compromiso y sin pagar nada.', a: 'Puertas abiertas' },
      en: { t: 'Come and try a training session', d: 'Open days all through September. No commitment, nothing to pay.', a: 'Open days' },
      href: '/portes-obertes/'
    },
    {
      quan: ['horari', 'partit'],
      ca: { t: 'Dia i hora de cada partit', d: 'El calendari s\'actualitza cada dia des de la Federació Catalana.', a: 'Veure el calendari' },
      es: { t: 'Día y hora de cada partido', d: 'El calendario se actualiza cada día desde la Federación Catalana.', a: 'Ver el calendario' },
      en: { t: 'Date and time of every game', d: 'The calendar updates daily from the Catalan Federation.', a: 'See the calendar' },
      href: '/partits/'
    },
    {
      quan: ['pista'],
      ca: { t: 'On juguem i entrenem', d: 'Totes les pistes del club, amb adreça i com arribar-hi.', a: 'Instal·lacions' },
      es: { t: 'Dónde jugamos y entrenamos', d: 'Todas las pistas del club, con dirección y cómo llegar.', a: 'Instalaciones' },
      en: { t: 'Where we play and train', d: 'Every court, with address and directions.', a: 'Facilities' },
      href: '/instal-lacions/'
    },
    {
      quan: ['edat'],
      ca: { t: 'Quina categoria li toca?', d: 'De l\'escoleta al sènior, per any de naixement.', a: 'Bàsquet formatiu' },
      es: { t: '¿Qué categoría le toca?', d: 'De la escoleta al sénior, por año de nacimiento.', a: 'Baloncesto formativo' },
      en: { t: 'Which age group?', d: 'From escoleta to senior, by year of birth.', a: 'Development basketball' },
      href: '/basquet-formatiu/'
    },
    {
      quan: ['preu'],
      ca: { t: 'Quotes i què inclouen', d: 'Les preguntes de diners, resoltes a les preguntes freqüents.', a: 'Preguntes freqüents' },
      es: { t: 'Cuotas y qué incluyen', d: 'Las preguntas de dinero, resueltas en las preguntas frecuentes.', a: 'Preguntas frecuentes' },
      en: { t: 'Fees and what they cover', d: 'Money questions, answered in the FAQ.', a: 'FAQ' },
      href: '/faq/'
    },
    {
      quan: ['patrocini'],
      ca: { t: 'La teva empresa al Barna', d: 'Què hi guanya una empresa del barri i qui hi és avui.', a: 'Empreses' },
      es: { t: 'Tu empresa en el Barna', d: 'Qué gana una empresa del barrio y quién está hoy.', a: 'Empresas' },
      en: { t: 'Your company at Barna', d: 'What a local business gets, and who is already in.', a: 'Companies' },
      href: '/empreses/'
    }
  ];

  /* Suggeriments de l'estat buit: les portes d'entrada reals. */
  var SUGGERIMENTS = {
    ca: [['Escoleta 4-8 anys', '/escoleta/'], ['Dies de partit', '/partits/calendaris/'],
         ['Els equips', '/partits/equips/'], ['Campus', '/campus/'],
         ['Bàsquet femení', '/femeni/'], ['Preguntes freqüents', '/faq/']],
    es: [['Escoleta 4-8 años', '/es/escoleta/'], ['Días de partido', '/partits/calendaris/'],
         ['Los equipos', '/partits/equips/'], ['Campus', '/es/campus/'],
         ['Baloncesto femenino', '/femeni/'], ['Preguntas frecuentes', '/es/faq/']],
    en: [['Escoleta, ages 4-8', '/en/escoleta/'], ['Match days', '/partits/calendaris/'],
         ['The teams', '/partits/equips/'], ['Camps', '/en/campus/'],
         ["Women's basketball", '/femeni/'], ['FAQ', '/en/faq/']]
  }[lang];

  /* ============================================================
     4 · MOTOR
     ============================================================ */
  var index = null, carregant = null, preparat = null, preparatFaq = [], equivalents = {};
  var teTraduccio = function () { return false; };
  var traduccio = function () { return null; };

  function carregaIndex() {
    if (carregant) return carregant;
    carregant = fetch(RUTA_INDEX, { credentials: 'omit' })
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (dades) {
        index = dades;

        // Equivalents entre idiomes (i18n/routes.yml). Serveixen per a dues
        // coses: no ensenyar la pàgina en català a qui llegeix en castellà
        // quan la castellana existeix, i —al revés— no amagar-la quan és
        // l'única que hi ha.
        var existeix = {};
        dades.pagines.forEach(function (p) { existeix[p.u] = p.l; });
        equivalents = {};
        (dades.rutes || []).forEach(function (r) {
          ['ca', 'es', 'en'].forEach(function (a) {
            if (r[a]) equivalents[r[a]] = r;
          });
        });
        teTraduccio = function (url, aIdioma) {
          var r = equivalents[url];
          return !!(r && r[aIdioma] && existeix[r[aIdioma]]);
        };
        traduccio = function (url, aIdioma) {
          var r = equivalents[url];
          return r && r[aIdioma] && existeix[r[aIdioma]] ? r[aIdioma] : null;
        };

        // Les preguntes que ja tenen resposta escrita. Es normalitzen un cop
        // i prou: n'hi ha 460 i es repassen a cada tecla.
        preparatFaq = (dades.faq || []).map(function (f) {
          return {
            f: f,
            q: normalitza(f.q),
            r: normalitza(f.r)
          };
        });

        preparat = dades.pagines.map(function (p) {
          var titol = normalitza(p.t);
          var enc = normalitza((p.h || []).join(' '));
          var desc = normalitza(p.d);
          var cos = normalitza(p.c);
          return {
            p: p,
            titol: titol, enc: enc, desc: desc, cos: cos,
            // Un sol sac per descartar de pressa el que no toca.
            tot: titol + ' ' + enc + ' ' + desc + ' ' + cos + ' ' + normalitza(p.u.replace(/[/-]/g, ' ')),
            paraulesTitol: titol.split(' ')
          };
        });
        return preparat;
      })
      .catch(function (e) {
        carregant = null;
        throw e;
      });
    return carregant;
  }

  /* Distància d'edició limitada: només ens interessa saber si dues
     paraules es diferencien en una lletra o dues, no la xifra exacta. */
  function proper(a, b, max) {
    if (a === b) return true;
    if (Math.abs(a.length - b.length) > max) return false;
    var fila = [], i, j;
    for (j = 0; j <= b.length; j++) fila[j] = j;
    for (i = 1; i <= a.length; i++) {
      var ant = fila[0], minFila = fila[0] = i;
      for (j = 1; j <= b.length; j++) {
        var tmp = fila[j];
        fila[j] = Math.min(fila[j] + 1, fila[j - 1] + 1, ant + (a[i - 1] === b[j - 1] ? 0 : 1));
        ant = tmp;
        if (fila[j] < minFila) minFila = fila[j];
      }
      if (minFila > max) return false;
    }
    return fila[b.length] <= max;
  }

  /* Quantes faltes perdonem, segons la llargada de la paraula. */
  function tolerancia(t) { return t.length <= 4 ? 0 : (t.length <= 7 ? 1 : 2); }

  /* Puntua un terme dins d'un camp. Compta el començament de paraula
     (qui escriu «esco» vol «escoleta») i, si cal, la falta d'ortografia. */
  function puntuaCamp(camp, terme, tol) {
    if (!camp) return 0;
    var pos = camp.indexOf(terme);
    if (pos >= 0) {
      var inici = pos === 0 || camp[pos - 1] === ' ';
      var sencera = inici && (pos + terme.length === camp.length || camp[pos + terme.length] === ' ');
      return sencera ? 1 : (inici ? 0.8 : 0.45);
    }
    if (!tol) return 0;
    var trossos = camp.split(' ');
    for (var i = 0; i < trossos.length; i++) {
      if (trossos[i].length > 2 && proper(trossos[i], terme, tol)) return 0.55;
    }
    return 0;
  }

  function cerca(consulta) {
    var termes = paraules(consulta);
    if (!termes.length || !preparat) return { llista: [], families: {} };

    var families = familiesDe(paraulesAmbBuides(consulta));
    // Cada família aporta les seves paraules a la consulta, amb menys pes:
    // així «cuánto cuesta» troba una pàgina que només diu «quota».
    var ampliats = [];
    Object.keys(families).forEach(function (f) {
      SINONIMS[f].split(' ').forEach(function (p) {
        if (p.length > 2 && termes.indexOf(p) < 0 && ampliats.indexOf(p) < 0) ampliats.push(p);
      });
    });

    // Les portes d'entrada de cada família, en tots els idiomes: DESTINS
    // les té escrites en català, però qui cerca en castellà ha d'arribar a
    // la versió castellana de la mateixa pàgina.
    // L'ordre de DESTINS mana: la primera pàgina de cada família és la
    // resposta, les altres són el context.
    var destins = {}, hiHaDestins = false;
    Object.keys(families).forEach(function (f) {
      (DESTINS[f] || []).forEach(function (u, ordre) {
        var valor = [22, 16, 12][ordre] || 10;
        [u].concat(['ca', 'es', 'en'].map(function (a) { return traduccio(u, a); }))
          .forEach(function (url) {
            if (!url) return;
            hiHaDestins = true;
            if ((destins[url] || 0) < valor) destins[url] = valor;
          });
      });
    });

    // Quantes paraules de la consulta han de sortir a la pàgina. Amb una o
    // dues, totes. Amb una pregunta sencera («a quina hora juga el cadet»)
    // ser estricte no té sentit: cap pàgina diu la frase tal qual.
    var minim = termes.length <= 2 ? termes.length
              : Math.min(3, Math.max(2, Math.ceil(termes.length * 0.5)));

    var resultats = [];
    for (var i = 0; i < preparat.length; i++) {
      var d = preparat[i], punts = 0, encerts = 0;

      for (var j = 0; j < termes.length; j++) {
        var t = termes[j], tol = tolerancia(t);
        if (d.tot.indexOf(t) < 0 && !tol) continue;
        var s = puntuaCamp(d.titol, t, tol) * 10
              + puntuaCamp(d.enc, t, tol) * 4
              + puntuaCamp(d.desc, t, tol) * 3
              + puntuaCamp(d.cos, t, tol) * 1.2;
        if (s > 0) { punts += s; encerts++; }
      }

      var desti = hiHaDestins ? (destins[d.p.u] || 0) : 0;
      // La porta d'entrada de la intenció detectada no passa el filtre de
      // cobertura: «com apuntar el meu fill» ha de portar a portes obertes
      // encara que la pàgina no digui enlloc «fill» ni «apuntar». Fora
      // d'aquest cas, sense cap paraula de la consulta no hi pinta res.
      if (!desti) {
        if (!encerts) continue;
        if (encerts < minim) continue;
      }

      for (var k = 0; k < ampliats.length; k++) {
        if (d.tot.indexOf(ampliats[k]) >= 0) punts += 0.9;
      }

      punts += desti;

      // Frase sencera: qui escriu «portes obertes» vol la pàgina que
      // es diu així, no una que digui «portes» per un costat i
      // «obertes» per l'altre.
      var frase = termes.join(' ');
      if (termes.length > 1) {
        if (d.titol.indexOf(frase) >= 0) punts += 18;
        else if (d.tot.indexOf(frase) >= 0) punts += 6;
      }

      punts += d.p.p / 12;                         // importància de la pàgina

      // Idioma. Si la pàgina és en un altre idioma però n'hi ha versió en el
      // teu, baixa (ja sortirà la bona). Si no n'hi ha cap altra versió, no
      // se la penalitza: és l'única que respon.
      if (d.p.l === lang) punts *= 1.6;
      else if (teTraduccio(d.p.u, lang)) punts *= 0.4;

      resultats.push({ d: d, punts: punts });
    }

    resultats.sort(function (a, b) { return b.punts - a.punts; });
    return { llista: resultats, families: families };
  }

  /* ============================================================
     4 bis · LA RESPOSTA
     De les 460 preguntes que ja tenen resposta escrita, quina
     respon la que s'acaba d'escriure? Aquí es decideix.

     La regla que mana és la de no fer el ridícul: val més no
     ensenyar cap resposta que ensenyar-ne una que no toca. Per
     això hi ha un llindar, i per sota d'ell la resposta no surt
     encara que sigui la millor de les dolentes.
     ============================================================ */
  var LLINDAR_FAQ = 9;

  /* Les interrogatives NO són paraules buides quan el que busques és una
     pregunta: «quan és el campus» i «quant costa el campus» es diferencien
     només per aquí. Per al text corrent sí que ho són, i per això la llista
     viu a part. */
  var INTERROGATIVES = {};
  ('quan quant quanta quants quantes on com qui quina quines quin quins perque ' +
   'cuando cuanto cuanta cuantos cuantas donde como quien cual cuales porque ' +
   'when how where who what which why').split(' ').forEach(function (p) { INTERROGATIVES[p] = 1; });

  /* «Club», «Barna» i «bàsquet» surten a gairebé totes les preguntes del web.
     Comptar-les fa que qualsevol consulta sembli que encaixa amb tot. */
  var GENERIQUES = {};
  ('club clubs barna cb grup cbgrupbarna basquet baloncesto basket basketball ' +
   'equip equipo team').split(' ').forEach(function (p) { GENERIQUES[p] = 1; });

  function paraulesPregunta(s) {
    return normalitza(s).split(' ').filter(function (p) {
      if (p.length < 2 || GENERIQUES[p]) return false;
      return INTERROGATIVES[p] || !BUIDES[p];
    });
  }

  function cercaResposta(consulta, families) {
    if (!preparatFaq.length) return null;
    var termes = paraulesPregunta(consulta);
    // Una paraula solta és un TEMA, no una pregunta. Qui escriu «fotos» vol
    // la galeria, no la resposta sobre el dret a la pròpia imatge; qui escriu
    // «campus» vol la pàgina del campus, no una de les seves set preguntes.
    // Amb enllaços n'hi ha prou: la resposta és per a qui pregunta.
    if (termes.length < 2) return null;

    // Les paraules de la família detectada ajuden a casar la pregunta encara
    // que estigui escrita amb unes altres («quotes» ↔ «quant costa»).
    var ampliats = [];
    Object.keys(families).forEach(function (f) {
      SINONIMS[f].split(' ').forEach(function (p) {
        if (p.length > 2 && termes.indexOf(p) < 0 && ampliats.indexOf(p) < 0) ampliats.push(p);
      });
    });

    var frase = termes.join(' ');
    var millors = [];

    for (var i = 0; i < preparatFaq.length; i++) {
      var d = preparatFaq[i], punts = 0, encerts = 0;

      for (var j = 0; j < termes.length; j++) {
        var t = termes[j], tol = tolerancia(t);
        var aQ = puntuaCamp(d.q, t, tol);
        var aR = aQ ? 0 : puntuaCamp(d.r, t, tol);
        if (aQ || aR) {
          encerts++;
          // puntuaCamp ja dona 1 a la paraula sencera i 0.8 a un principi de
          // paraula. Elevat al quadrat, la diferència entre encertar-la
          // («entrena») i quedar-s'hi a prop («entrenar») deixa de ser un
          // matís i decideix.
          punts += aQ * aQ * 3.5 + aR * 0.7;
        }
      }
      if (!encerts) continue;

      // Cobertura: quina part del que s'ha escrit surt a la pregunta. Una
      // pregunta que respon la meitat del que es demana no la respon.
      var cobertura = encerts / termes.length;
      if (cobertura < 0.5) continue;
      punts *= 0.6 + cobertura;

      for (var k = 0; k < ampliats.length; k++) {
        if (d.q.indexOf(ampliats[k]) >= 0) punts += 0.5;
      }
      // La pregunta escrita gairebé igual guanya de llarg.
      if (termes.length > 1 && d.q.indexOf(frase) >= 0) punts += 6;
      // Una pregunta curta que conté tot el que s'ha demanat és més precisa
      // que una de llarga que ho conté de passada.
      punts += Math.max(0, 3 - d.q.split(' ').length / 8);

      if (d.f.l === lang) punts *= 1.5;
      else if (teTraduccio(d.f.u, lang)) punts *= 0.35;

      millors.push({ d: d, punts: punts });
    }

    if (!millors.length) return null;
    millors.sort(function (a, b) { return b.punts - a.punts; });
    if (millors[0].punts < LLINDAR_FAQ) return null;

    // Preguntes veïnes: només les de la mateixa collita, per no oferir
    // «i també et pot interessar» d'una cosa que no hi té res a veure.
    var veines = [];
    for (var n = 1; n < millors.length && veines.length < 2; n++) {
      if (millors[n].punts < millors[0].punts * 0.55) break;
      if (millors[n].d.f.q !== millors[0].d.f.q) veines.push(millors[n].d.f);
    }

    return { resposta: millors[0].d.f, punts: millors[0].punts, veines: veines };
  }

  /* Tall del text on surt el que s'ha buscat, amb el terme marcat. */
  function fragment(dades, termes) {
    var font = dades.p.d || dades.p.c || '';
    var norm = normalitza(font), pos = -1, trobat = '';
    for (var i = 0; i < termes.length && pos < 0; i++) {
      pos = norm.indexOf(termes[i]);
      if (pos >= 0) trobat = termes[i];
    }
    var inici = 0;
    if (pos > 90) {
      inici = font.lastIndexOf(' ', pos - 70);
      if (inici < 0) inici = pos - 70;
    }
    var tall = font.slice(inici, inici + 190).trim();
    if (inici > 0) tall = '…' + tall;
    if (inici + 190 < font.length) tall += '…';
    return marca(tall, termes.concat(trobat ? [trobat] : []));
  }

  function escapa(s) {
    return (s || '').replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  /* Versió normalitzada que conserva les posicions: cada lletra de l'original
     dona exactament una lletra a la sortida. `normalitza` no serveix per a
     marcar perquè ajunta espais i escurça la cadena, i llavors el subratllat
     cau damunt d'una altra paraula (s'ha vist marcant «Grup» en cercar
     «costa»). */
  function normalitzaPosicional(text) {
    var fora = '';
    for (var i = 0; i < text.length; i++) {
      var c = text[i].toLowerCase();
      if (c === 'ç') c = 'c';
      c = c.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      if (c.length !== 1 || !/[a-z0-9]/.test(c)) c = ' ';
      fora += c;
    }
    return fora;
  }

  /* Marca els termes damunt del text original, amb accents i tot. */
  function marca(text, termes) {
    var norm = normalitzaPosicional(text);
    var trams = [];
    termes.forEach(function (t) {
      if (t.length < 3) return;
      var des = 0, p;
      while ((p = norm.indexOf(t, des)) >= 0) {
        trams.push([p, p + t.length]);
        des = p + t.length;
      }
    });
    if (!trams.length) return escapa(text);
    trams.sort(function (a, b) { return a[0] - b[0]; });
    var sortida = '', cursor = 0;
    trams.forEach(function (tr) {
      if (tr[0] < cursor) return;
      sortida += escapa(text.slice(cursor, tr[0])) + '<mark>' + escapa(text.slice(tr[0], tr[1])) + '</mark>';
      cursor = tr[1];
    });
    return sortida + escapa(text.slice(cursor));
  }

  /* Títol net per al resultat: fora el «· CB Grup Barna» de cada pàgina. */
  function titolNet(t) {
    return (t || '').replace(/\s*[·|–-]\s*CB Grup Barna.*$/i, '').trim() || t;
  }

  /* Per a l'enllaç de sota la resposta cal un nom curt, no el títol sencer
     d'SEO: «Escola de bàsquet a Barcelona · Escoleta CB Grup Barna (4-8 anys)»
     ocupa tres línies al mòbil i no diu res que no digui «Escoleta». */
  function titolCurt(t) {
    var curt = titolNet(t).split(/\s+[·|]\s+/)[0].trim();
    if (curt.length > 42) curt = curt.slice(0, 40).replace(/\s+\S*$/, '') + '…';
    return curt;
  }

  var NOM_IDIOMA = { ca: 'Català', es: 'Castellano', en: 'English' };

  /* ---------- Cerques recents (només al navegador de qui cerca) ---------- */
  function recents(afegir) {
    var llista = [];
    try { llista = JSON.parse(localStorage.getItem(CLAU_RECENTS) || '[]'); } catch (e) { llista = []; }
    if (afegir === null) {
      try { localStorage.removeItem(CLAU_RECENTS); } catch (e) {}
      return [];
    }
    if (afegir) {
      llista = llista.filter(function (x) { return x !== afegir; });
      llista.unshift(afegir);
      llista = llista.slice(0, 5);
      try { localStorage.setItem(CLAU_RECENTS, JSON.stringify(llista)); } catch (e) {}
    }
    return llista;
  }

  /* ============================================================
     5 · INTERFÍCIE
     ============================================================ */
  function construeixHTML(idPrefix) {
    return '' +
      '<form class="cerca-camp" role="search" autocomplete="off">' +
        '<svg class="cerca-lupa" viewBox="0 0 24 24" aria-hidden="true"><path d="M10.5 3a7.5 7.5 0 1 1-4.6 13.4l-3.2 3.2a1 1 0 0 1-1.4-1.4l3.2-3.2A7.5 7.5 0 0 1 10.5 3Zm0 2a5.5 5.5 0 1 0 0 11 5.5 5.5 0 0 0 0-11Z"/></svg>' +
        '<input type="search" id="' + idPrefix + 'Input" class="cerca-input" ' +
          'placeholder="' + escapa(T.placeholder) + '" aria-label="' + escapa(T.titol) + '" ' +
          'role="combobox" aria-expanded="false" aria-autocomplete="list" ' +
          'aria-controls="' + idPrefix + 'Llista" spellcheck="false">' +
        '<button type="button" class="cerca-neteja" hidden aria-label="' + escapa(T.esborrar) + '">&times;</button>' +
      '</form>' +
      '<div class="cerca-cos" id="' + idPrefix + 'Llista" role="listbox" aria-label="' + escapa(T.resultats) + '"></div>' +
      '<p class="cerca-pista"><kbd>&uarr;</kbd><kbd>&darr;</kbd> ' + escapa(T.pista) + '</p>';
  }

  function Cercador(arrel, idPrefix, esPagina) {
    var self = this;
    this.arrel = arrel;
    this.esPagina = esPagina;
    arrel.innerHTML = construeixHTML(idPrefix);
    this.input = arrel.querySelector('.cerca-input');
    this.cos = arrel.querySelector('.cerca-cos');
    this.neteja = arrel.querySelector('.cerca-neteja');
    this.form = arrel.querySelector('.cerca-camp');
    this.actiu = -1;
    this.enllacos = [];

    this.form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (self.enllacos.length) self.obre(self.enllacos[Math.max(0, self.actiu)]);
    });
    this.input.addEventListener('input', function () { self.pinta(); });
    this.neteja.addEventListener('click', function () {
      self.input.value = '';
      self.input.focus();
      self.pinta();
    });
    arrel.addEventListener('keydown', function (e) { self.tecla(e); });
    this.cos.addEventListener('click', function (e) {
      var a = e.target.closest('a[data-cerca-r]');
      if (a) recents(self.input.value.trim());
    });
  }

  Cercador.prototype.obre = function (a) {
    if (!a) return;
    recents(this.input.value.trim());
    if (a.target === '_blank') window.open(a.href, '_blank', 'noopener');
    else location.href = a.href;
  };

  Cercador.prototype.tecla = function (e) {
    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp' && e.key !== 'Enter') return;
    if (!this.enllacos.length) return;
    if (e.key === 'Enter') {
      if (this.actiu >= 0) { e.preventDefault(); this.obre(this.enllacos[this.actiu]); }
      return;
    }
    e.preventDefault();
    this.actiu += (e.key === 'ArrowDown' ? 1 : -1);
    if (this.actiu < 0) this.actiu = this.enllacos.length - 1;
    if (this.actiu >= this.enllacos.length) this.actiu = 0;
    this.marcaActiu();
  };

  Cercador.prototype.marcaActiu = function () {
    var self = this;
    this.enllacos.forEach(function (a, i) {
      var sel = i === self.actiu;
      a.classList.toggle('es-actiu', sel);
      a.setAttribute('aria-selected', sel ? 'true' : 'false');
      if (sel) {
        self.input.setAttribute('aria-activedescendant', a.id);
        if (a.scrollIntoView) a.scrollIntoView({ block: 'nearest' });
      }
    });
  };

  Cercador.prototype.recolliEnllacos = function () {
    this.enllacos = Array.prototype.slice.call(this.cos.querySelectorAll('a[data-cerca-r]'));
    this.enllacos.forEach(function (a, i) {
      a.id = a.id || 'cerca-r-' + i;
      a.setAttribute('role', 'option');
      a.setAttribute('aria-selected', 'false');
    });
    this.actiu = this.enllacos.length ? 0 : -1;
    this.input.setAttribute('aria-expanded', this.enllacos.length ? 'true' : 'false');
    this.marcaActiu();
  };

  Cercador.prototype.estatBuit = function () {
    var recs = recents();
    var html = '';
    if (recs.length) {
      html += '<div class="cerca-bloc"><h2 class="cerca-titol">' + escapa(T.recents) +
        ' <button type="button" class="cerca-esborra-recents">' + escapa(T.esborrar) + '</button></h2><div class="cerca-fitxes">';
      recs.forEach(function (r) {
        html += '<button type="button" class="cerca-fitxa" data-recent="' + escapa(r) + '">' + escapa(r) + '</button>';
      });
      html += '</div></div>';
    }
    html += '<div class="cerca-bloc"><h2 class="cerca-titol">' + escapa(T.suggeriments) + '</h2><div class="cerca-fitxes">';
    SUGGERIMENTS.forEach(function (s) {
      html += '<a class="cerca-fitxa" data-cerca-r href="' + escapa(s[1]) + '">' + escapa(s[0]) + '</a>';
    });
    html += '</div></div>';
    this.cos.innerHTML = html;

    var self = this;
    var esb = this.cos.querySelector('.cerca-esborra-recents');
    if (esb) esb.addEventListener('click', function () { recents(null); self.pinta(); });
    Array.prototype.forEach.call(this.cos.querySelectorAll('[data-recent]'), function (b) {
      b.addEventListener('click', function () {
        self.input.value = b.getAttribute('data-recent');
        self.input.focus();
        self.pinta();
      });
    });
    this.recolliEnllacos();
  };

  Cercador.prototype.pinta = function () {
    var self = this;
    var q = this.input.value.trim();
    this.neteja.hidden = !q;

    if (!q) { this.estatBuit(); return; }

    if (!preparat) {
      this.cos.innerHTML = '<p class="cerca-estat">' + escapa(T.carregant) + '</p>';
      carregaIndex().then(function () { self.pinta(); })
        .catch(function () { self.cos.innerHTML = '<p class="cerca-estat">' + escapa(T.error) + '</p>'; });
      return;
    }

    var res = cerca(q);
    var termes = paraules(q);
    var html = '';

    // 1r · La resposta escrita pel club, si n'hi ha cap que encaixi.
    var faq = cercaResposta(q, res.families);
    if (faq) {
      var titolNetFont = null;
      for (var z = 0; z < preparat.length; z++) {
        if (preparat[z].p.u === faq.resposta.u) { titolNetFont = titolCurt(preparat[z].p.t); break; }
      }
      html += '<div class="cerca-bloc"><h2 class="cerca-titol">' + escapa(T.respostaFaq) + '</h2>' +
        '<div class="cerca-faq">' +
          '<p class="cerca-faq-q">' + marca(faq.resposta.q, termes) + '</p>' +
          '<p class="cerca-faq-r">' + marca(faq.resposta.r, termes) + '</p>' +
          '<a class="cerca-faq-font" data-cerca-r href="' + escapa(faq.resposta.u) + '">' +
            escapa(T.fontFaq) + ' <b>' + escapa(titolNetFont || faq.resposta.u) + '</b> &rarr;</a>' +
        '</div>';
      if (faq.veines.length) {
        html += '<p class="cerca-titol" style="margin-top:12px">' + escapa(T.relacionades) + '</p>' +
          '<div class="cerca-fitxes">';
        faq.veines.forEach(function (v) {
          html += '<button type="button" class="cerca-fitxa" data-pregunta="' + escapa(v.q) + '">' +
            escapa(v.q) + '</button>';
        });
        html += '</div>';
      }
      html += '</div>';
    }

    // 2n · Les respostes escrites a mà, per a les intencions que cap pregunta
    // del web cobreix (contacte, portes obertes). Si ja hem respost, no cal.
    var families = faq ? [] : Object.keys(res.families);
    if (families.length) {
      for (var i = 0; i < RESPOSTES.length; i++) {
        var r = RESPOSTES[i];
        var encerta = r.quan.some(function (f) { return families.indexOf(f) >= 0; });
        if (!encerta) continue;
        var txt = r[lang];
        var extern = r.href.indexOf('http') === 0;
        html += '<div class="cerca-bloc"><h2 class="cerca-titol">' + escapa(T.resposta) + '</h2>' +
          '<a class="cerca-resposta" data-cerca-r href="' + escapa(r.href) + '"' +
          (extern ? ' target="_blank" rel="noopener"' : '') + '>' +
          '<strong>' + escapa(txt.t) + '</strong><span>' + escapa(txt.d) + '</span>' +
          '<em>' + escapa(txt.a) + ' &rarr;</em></a></div>';
        break;
      }
    }

    var mostra = res.llista.slice(0, MAX_RESULTATS);

    if (!mostra.length && !html) {
      this.cos.innerHTML = '<div class="cerca-bloc"><p class="cerca-estat"><strong>' +
        escapa(T.cap) + ' «' + escapa(q) + '»</strong><br>' + escapa(T.capAjuda) + '</p></div>';
      this.estatBuitSuggeriments();
      return;
    }

    if (mostra.length) {
      var total = res.llista.length;
      html += '<div class="cerca-bloc"><h2 class="cerca-titol">' +
        (total === 1 ? escapa(T.unResultat) : total + ' ' + escapa(T.resultats)) + '</h2><ul class="cerca-llista">';
      mostra.forEach(function (x) {
        var p = x.d.p;
        var altre = p.l !== lang;
        html += '<li><a data-cerca-r href="' + escapa(p.u) + '">' +
          '<span class="cerca-r-t">' + marca(titolNet(p.t), termes) + '</span>' +
          '<span class="cerca-r-d">' + fragment(x.d, termes) + '</span>' +
          '<span class="cerca-r-u">' + escapa(p.u) +
            (altre ? ' <b class="cerca-idioma">' + escapa(NOM_IDIOMA[p.l]) + '</b>' : '') +
          '</span></a></li>';
      });
      html += '</ul></div>';
    }

    this.cos.innerHTML = html;
    Array.prototype.forEach.call(this.cos.querySelectorAll('[data-pregunta]'), function (b) {
      b.addEventListener('click', function () {
        self.input.value = b.getAttribute('data-pregunta');
        self.input.focus();
        self.pinta();
      });
    });
    this.recolliEnllacos();

    if (this.esPagina) {
      var url = new URL(location.href);
      url.searchParams.set('q', q);
      history.replaceState(null, '', url);
    }
  };

  // Si no hi ha resultats, encara donem portes on anar.
  Cercador.prototype.estatBuitSuggeriments = function () {
    var html = '<div class="cerca-bloc"><h2 class="cerca-titol">' + escapa(T.suggeriments) + '</h2><div class="cerca-fitxes">';
    SUGGERIMENTS.forEach(function (s) {
      html += '<a class="cerca-fitxa" data-cerca-r href="' + escapa(s[1]) + '">' + escapa(s[0]) + '</a>';
    });
    html += '</div></div>';
    this.cos.insertAdjacentHTML('beforeend', html);
    this.recolliEnllacos();
  };

  /* ============================================================
     6 · MUNTATGE · superposat a totes les pàgines
     ============================================================ */
  var capa = null, cercador = null, ultimFocus = null;

  function creaCapa() {
    if (capa) return capa;
    capa = document.createElement('div');
    capa.className = 'cerca-capa';
    capa.id = 'cercaCapa';
    capa.setAttribute('role', 'dialog');
    capa.setAttribute('aria-modal', 'true');
    capa.setAttribute('aria-label', T.titol);
    capa.hidden = true;
    capa.innerHTML = '<div class="cerca-fons" data-tanca></div>' +
      '<div class="cerca-panell">' +
        '<button type="button" class="cerca-tanca" data-tanca aria-label="' + escapa(T.tancar) + '">&times;</button>' +
        '<div class="cerca-motor"></div>' +
      '</div>';
    document.body.appendChild(capa);
    cercador = new Cercador(capa.querySelector('.cerca-motor'), 'capa', false);
    capa.addEventListener('click', function (e) {
      if (e.target.hasAttribute('data-tanca')) tanca();
    });
    return capa;
  }

  function obre(text) {
    creaCapa();
    ultimFocus = document.activeElement;
    capa.hidden = false;
    document.documentElement.classList.add('cerca-oberta');
    carregaIndex().catch(function () {});
    if (text) cercador.input.value = text;
    cercador.pinta();
    setTimeout(function () { cercador.input.focus(); cercador.input.select(); }, 30);
  }

  function tanca() {
    if (!capa || capa.hidden) return;
    capa.hidden = true;
    document.documentElement.classList.remove('cerca-oberta');
    if (ultimFocus && ultimFocus.focus) ultimFocus.focus();
  }

  /* El botó de la capçalera. Si la pàgina ja en porta un de propi
     (data-cerca-obrir), es respecta i no se n'afegeix cap altre. */
  function muntaBoto() {
    if (document.querySelector('[data-cerca-obrir]')) return;
    // A /cerca/ el camp ja és el contingut de la pàgina: una lupa a la
    // capçalera que obrís una capa a sobre només faria nosa.
    if (document.getElementById('cercaPagina')) return;
    var costat = document.querySelector('.head .head-side.r .head-nav') ||
                 document.querySelector('.head .head-side.r') ||
                 document.querySelector('.head-nav');
    if (!costat) return;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'cerca-boto';
    b.setAttribute('data-cerca-obrir', '');
    b.setAttribute('aria-label', T.obrir);
    b.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10.5 3a7.5 7.5 0 1 1-4.6 13.4l-3.2 3.2a1 1 0 0 1-1.4-1.4l3.2-3.2A7.5 7.5 0 0 1 10.5 3Zm0 2a5.5 5.5 0 1 0 0 11 5.5 5.5 0 0 0 0-11Z"/></svg>' +
      '<span>' + escapa(T.obrir) + '</span>';

    // Les capçaleres del lloc no són totes iguals i algunes van justes: a
    // /portes-obertes/ a 1280 px, la paraula «Cerca» empenyia el commutador
    // d'idioma 3 px fora de la pantalla. En comptes d'endevinar un punt de
    // ruptura per a cada maquetació, es mira si la pàgina desbordava ABANS
    // d'entrar el botó; si no ho feia i ara sí, el botó es queda amb la lupa.
    var arrelDoc = document.documentElement;
    var desbordavaAbans = arrelDoc.scrollWidth > arrelDoc.clientWidth + 1;
    // Al final de la navegació, no al principi: a les pàgines amb la
    // capçalera llarga (deu enllaços i el commutador d'idioma), posat al
    // principi el botó se solapava amb el nom del club.
    costat.appendChild(b);

    var ajusta = function () {
      b.classList.remove('cerca-boto--icona');
      if (!desbordavaAbans && arrelDoc.scrollWidth > arrelDoc.clientWidth + 1) {
        b.classList.add('cerca-boto--icona');
      }
    };
    ajusta();
    var espera;
    window.addEventListener('resize', function () {
      clearTimeout(espera);
      espera = setTimeout(ajusta, 150);
    });
  }

  function inicia() {
    var pagina = document.getElementById('cercaPagina');
    if (pagina) {
      var c = new Cercador(pagina, 'pag', true);
      var q = new URLSearchParams(location.search).get('q') || '';
      c.input.value = q;
      carregaIndex().then(function () { c.pinta(); })
        .catch(function () { c.cos.innerHTML = '<p class="cerca-estat">' + escapa(T.error) + '</p>'; });
      c.pinta();
      c.input.focus();
    }

    muntaBoto();

    document.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cerca-obrir]');
      if (!b) return;
      e.preventDefault();
      obre(b.getAttribute('data-cerca-text') || '');
    });

    document.addEventListener('keydown', function (e) {
      if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        capa && !capa.hidden ? tanca() : obre('');
        return;
      }
      if (e.key === 'Escape' && capa && !capa.hidden) { tanca(); return; }
      // La tecla «/» obre la cerca, però no mentre s'escriu en un camp.
      if (e.key === '/' && !e.metaKey && !e.ctrlKey && !e.altKey) {
        var t = e.target;
        if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
        e.preventDefault();
        obre('');
      }
    });

    // Es baixa l'índex quan el navegador no té res més a fer, perquè la
    // primera cerca ja el trobi a punt. Mai a xarxes lentes o amb estalvi
    // de dades: primer va la pàgina.
    var conn = navigator.connection || {};
    if (!conn.saveData && !/2g/.test(conn.effectiveType || '')) {
      var precarrega = function () { carregaIndex().catch(function () {}); };
      if (window.requestIdleCallback) requestIdleCallback(precarrega, { timeout: 6000 });
      else setTimeout(precarrega, 4000);
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inicia);
  else inicia();

  // Perquè qualsevol pàgina pugui obrir la cerca amb text ja posat,
  // i perquè tests/cerca/prova-motor.mjs pugui provar el motor sol.
  window.CBGBCerca = {
    obre: obre,
    tanca: tanca,
    _motor: {
      carrega: carregaIndex,
      normalitza: normalitza,
      paraules: paraules,
      cerca: function (q) {
        return cerca(q).llista.map(function (x) {
          return { u: x.d.p.u, l: x.d.p.l, t: x.d.p.t, punts: Math.round(x.punts * 10) / 10 };
        });
      },
      families: function (q) { return Object.keys(cerca(q).families); },
      resposta: function (q) {
        var r = cercaResposta(q, cerca(q).families);
        return r ? { q: r.resposta.q, r: r.resposta.r, u: r.resposta.u, l: r.resposta.l,
                     punts: Math.round(r.punts * 10) / 10 } : null;
      }
    }
  };
})();
