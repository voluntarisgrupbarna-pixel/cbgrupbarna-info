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
      pista: 'per moure\'t · Enter per obrir · Esc per sortir',
      voliesDir: 'Volies dir', preguntaHo: 'Pregunta-ho i t\'ho diem',
      preguntaHoAra: 'Escriu-ho pel WhatsApp del club', deLaRuta: 'Potser buscaves',
      formTitol: 'Això no ho tenim escrit', 
      formPeu: 'Deixa\'ns un contacte i t\'ho responem nosaltres, normalment el mateix dia.',
      formNom: 'Com et dius', formVia: 'Telèfon o correu',
      formPregunta: 'Què vols saber', formEnvia: 'Envia-ho al club',
      formEnviant: 'Enviant…', formFalta: 'Això cal omplir-ho',
      formAvis: 'Només s\'envia si prems el botó, i és per respondre\'t. ',
      formPrivacitat: 'Política de privacitat',
      formGracies: 'Rebut. T\'escrivim de seguida.',
      formPressa: 'Tens pressa?', formWhatsApp: 'Digues-ho pel WhatsApp &rarr;',
      formError: 'No s\'ha pogut enviar. Prova pel WhatsApp.',
      privacitatRuta: '/politica-de-privacitat/'
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
      pista: 'para moverte · Enter para abrir · Esc para salir',
      voliesDir: '¿Querías decir', preguntaHo: 'Pregúntalo y te lo decimos',
      preguntaHoAra: 'Escríbelo por el WhatsApp del club', deLaRuta: 'Quizá buscabas',
      formTitol: 'Esto no lo tenemos escrito',
      formPeu: 'Déjanos un contacto y te lo respondemos nosotros, normalmente el mismo día.',
      formNom: 'Cómo te llamas', formVia: 'Teléfono o correo',
      formPregunta: 'Qué quieres saber', formEnvia: 'Enviarlo al club',
      formEnviant: 'Enviando…', formFalta: 'Esto hay que rellenarlo',
      formAvis: 'Solo se envía si pulsas el botón, y es para responderte. ',
      formPrivacitat: 'Política de privacidad',
      formGracies: 'Recibido. Te escribimos enseguida.',
      formPressa: '¿Tienes prisa?', formWhatsApp: 'Dilo por WhatsApp &rarr;',
      formError: 'No se ha podido enviar. Prueba por WhatsApp.',
      privacitatRuta: '/es/politica-de-privacidad/'
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
      pista: 'to move · Enter to open · Esc to close',
      voliesDir: 'Did you mean', preguntaHo: 'Ask us and we will tell you',
      preguntaHoAra: 'Message the club on WhatsApp', deLaRuta: 'Maybe you were looking for',
      formTitol: 'We have not written this one down',
      formPeu: 'Leave us a contact and we will answer you ourselves, usually the same day.',
      formNom: 'Your name', formVia: 'Phone or email',
      formPregunta: 'What would you like to know', formEnvia: 'Send it to the club',
      formEnviant: 'Sending…', formFalta: 'This one is required',
      formAvis: 'It is only sent if you press the button, and only so we can reply. ',
      formPrivacitat: 'Privacy policy',
      formGracies: 'Got it. We will be in touch shortly.',
      formPressa: 'In a hurry?', formWhatsApp: 'Say it on WhatsApp &rarr;',
      formError: 'It could not be sent. Try WhatsApp instead.',
      privacitatRuta: '/en/privacy-policy/'
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
      // El guionet, fora. En català les formes amb pronom en porten
      // («fer-se», «quedar-me», «apuntar-s'hi») i, sense separar-lo,
      // «fer-se» era una paraula que no surt a cap pregunta del web: la
      // consulta «cal fer-se una prova mèdica» es quedava sense resposta
      // perquè aquesta paraula inventada pesava més que «mèdica».
      // normalitzaPosicional ja el tractava com un separador: ara van
      // iguals.
      .replace(/[^a-z0-9\s]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  /* Paraules que no aporten res a cap dels tres idiomes. */
  var BUIDES = {};
  ('de del la el les els un una uns unes i o a al als amb per que quan com on ' +
   'els meu meva teu teva es se para por con del las los una unos unas y donde ' +
   'cuando como cuanto the of and for to in on at is are how what when where my ' +
   'your can i do does es en si no hi ha hay tiene tienen te tenim tenen have has ' +
   'sobre about esta este esta aquest aquesta cual quiere quiero vull want ' +
   // Verbs de tots els dies. Al corpus de preguntes en surten pocs, i per
   // això el pes per raresa els prenia per distintius: «com em FAIG
   // entrenador» exigia trobar «faig», i cap pregunta del web el diu.
   'faig fas fa fem feu fan fer puc pots pot podem podeu poden poder ' +
   'vols vol volem voleu volen voler ser soc som sou estar esta estan ' +
   'hago haces hace hacemos hacen hacer puedo puedes puede podemos pueden poder ' +
   'quieres quiere queremos quieren querer soy eres somos son estoy estas estan ' +
   'make makes made want wants get gets go goes am was were be been being ' +
   'should would could will shall may might must ' +
   // Aquestes són pitjor que inútils. El web escriu «Quants equips té el CB
   // Grup Barna?» i ningú no hi escriu mai «teniu»; la raresa la prenia,
   // doncs, per la paraula MÉS distintiva de la consulta i exigia trobar-la
   // a la pregunta. «Quantes entrenadores teniu» buscava «teniu» i deixava
   // «entrenadores» de banda. El mateix amb «on esteu» i «sou el millor
   // club». Una paraula que no surt enlloc no és rara: és buida.
   'tinc tens teniu tinguem tingueu tenir tinguin ' +
   'estic estas esteu estem estigui estic ' +
   'sereu serem series siguin fos fossin ' +
   'tengo tienes teneis tenemos tener tenga tengan ' +
   'estoy estais estamos estar seais sois fuera fueran ' +
   'haveis habeis hemos haber hay ' +
   'venc vens venem veneu venen vendre vendo vendes vendemos venden ' +
   // Pronoms i auxiliars. Són curts, surten poc a les preguntes del web i
   // arrossegaven la consulta cap avall: «quin metro EM VA bé» i «cómo doy
   // de baja a MI hijo» es quedaven sense resposta perquè aquestes paraules
   // comptaven tant com «metro» i «baja», i no són a cap pregunta.
   'em et ens us hi ho li me nos mi tu su sus mis tus le lo ' +
   'va van vaig vam vau anar voy vamos van ir').split(' ').forEach(function (p) { BUIDES[p] = 1; });

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
    patrocini: 'patrocini patrocinis patrocinar patrocinador patrocinadors patrocinio patrocinar sponsor sponsors sponsorship patrocinen partner partners empresa empreses empresas publicitat colaborar collaborate col.laborar',
    fotos: 'fotos foto fotografies fotografias photos gallery galeria imatges imagenes',
    documents: 'document documents documentos assegurança seguro insurance autoritzacio autorizacion certificat certificado proteccio proteccion protection menor',
    tresxtres: '3x3 3 x 3 tresxtres torneig torneo tournament glories westfield street',
    blog: 'blog article articles articulo noticies noticias news consells consejos tips guia guide',
    premsa: 'premsa prensa press briefing kit dossier mitjans medios media periodista journalist entrevista logotip logo materials nota',
    persones: 'julio torralba ainhoa lopez javier roger fornas mejia entrenador entrenadora president presidenta junta directiva coordinador coordinadora',
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
    blog: ['/blog/'],
    premsa: ['/briefing/', '/premsa/'],
    persones: ['/organigrama/', '/club/', '/jugadors/'],
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
  var pesFaq = {}, totalPreguntes = {}, pesPagina = {};
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

        // Quantes preguntes fan servir cada paraula. Serveix per saber què
        // pesa: «qui» surt a dues-centes preguntes i no distingeix res;
        // «president» surt a cap o a una i ho decideix tot.
        pesFaq = {};
        var totalFaq = {};
        preparatFaq.forEach(function (d) {
          var l = d.f.l;
          totalFaq[l] = (totalFaq[l] || 0) + 1;
          var vistes = {};
          d.q.split(' ').forEach(function (w) {
            if (!w || vistes[w]) return;
            vistes[w] = 1;
            (pesFaq[l] = pesFaq[l] || {})[w] = (pesFaq[l][w] || 0) + 1;
          });
        });
        totalPreguntes = totalFaq;

        // La importància de cada pàgina, que ja calcula el generador d'índex.
        pesPagina = {};
        dades.pagines.forEach(function (p) { pesPagina[p.u] = p.p; });

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
  // Mesurat amb tests/cerca/prova-contingut.mjs sobre 85 consultes reals.
  // Es va provar de pujar-lo a 11,5 per matar les respostes fluixes i NO ES
  // POT: les puntuacions se solapen. «Where do they train» és bona i fa 8,6;
  // «quant val la temporada» és dolenta i fa 9,5. Pujar el llindar costava
  // més respostes bones que dolentes.
  //
  // Qui separa les dues famílies són les regles d'aquí sota —el pes per
  // raresa i la paraula clau obligatòria—, que miren l'estructura de la
  // consulta. El llindar només fa de terra.
  var LLINDAR_FAQ = 9;

  /* Les interrogatives NO són paraules buides quan el que busques és una
     pregunta: «quan és el campus» i «quant costa el campus» es diferencien
     només per aquí. Per al text corrent sí que ho són, i per això la llista
     viu a part. */
  var INTERROGATIVES = {};
  ('que quan quant quanta quants quantes on com qui quina quines quin quins perque ' +
   'cuando cuanto cuanta cuantos cuantas donde como quien cual cuales porque ' +
   'when how where who what which why whose').split(' ').forEach(function (p) { INTERROGATIVES[p] = 1; });

  /* «Club», «Barna» i «bàsquet» surten a gairebé totes les preguntes del web.
     Comptar-les fa que qualsevol consulta sembli que encaixa amb tot. */
  var GENERIQUES = {};
  ('club clubs barna cb grup cbgrupbarna basquet baloncesto basket basketball ' +
   'equip equipo team').split(' ').forEach(function (p) { GENERIQUES[p] = 1; });

  /* Paraules que sí que compten, però que no poden decidir tota soles. */
  var NO_DECIDEIXEN = {};
  ('fill filla fills filles hijo hija hijos hijas nino nina child children ' +
   'son daughter kid kids nen nena nens nenes').split(' ').forEach(function (p) {
    NO_DECIDEIXEN[p] = 1;
  });

  function paraulesPregunta(s) {
    var fora = normalitza(s).split(' ').filter(function (p) {
      if (p.length < 2 || GENERIQUES[p]) return false;
      return INTERROGATIVES[p] || !BUIDES[p];
    });
    // «Club», «Barna» i «bàsquet» no compten perquè surten a gairebé totes
    // les preguntes. Però si la consulta NOMÉS en té —«per què es diu Grup
    // Barna»— llavors sí que són el tema, i descartar-les deixava la
    // consulta sense cap paraula i sense resposta possible.
    if (fora.length) return fora;
    return normalitza(s).split(' ').filter(function (p) {
      return p.length > 1 && (INTERROGATIVES[p] || !BUIDES[p]);
    });
  }

  /* El pes d'una paraula: 1 si no surt a cap pregunta, i cada vegada menys
     com més comuna sigui. Els extrems importen més que la fórmula exacta. */
  /* La paraula hi és, encara que estigui conjugada d'una altra manera?
     «porto» i «portar» són la mateixa paraula per a qui pregunta, i la
     distància d'edició no ho veu (hi ha dues lletres de diferència en una
     paraula de cinc). Comparar l'arrel sí que ho veu, i no confon
     «entrenador» amb «patrocinador», que és el que calia evitar. */
  /* Quantes lletres tenen en comú pel començament. */
  function prefixComu(a, b) {
    var n = 0, max = Math.min(a.length, b.length);
    while (n < max && a[n] === b[n]) n++;
    return n;
  }

  /* Dues paraules són LA MATEIXA paraula? No n'hi ha prou amb el
     començament. Comparar només les tres o quatre primeres lletres feia
     que el cercador contestés qualsevol cosa que comencés igual:

        instalacions → «inscripcions»      precio    → «premios»
        metro        → «Mètode Barna»      entranador → «entrar»
        equipasio    → «equips»            president  → «pressupost»

     Sis de les setze respostes equivocades de l'auditoria eren això. El
     començament compartit ha de valer per la MEITAT de la paraula llarga,
     i el que queda no pot ser una cua qualsevol: d'aquí el límit de mida.

     Aquí hi va haver una segona regla, de tres lletres, per als verbs que
     canvien pel mig («donem»/«donar»). No hi ha manera d'escriure-la sense
     que hi caiguin també «precio»/«previa» i «precio»/«premios»: són
     indistingibles mesurant lletres. Els verbs que calgui, doncs, van a
     SINONIMS, que és explícit i es pot llegir. */
  function mateixaParaula(m, terme) {
    if (m === terme) return true;
    var pref = prefixComu(m, terme);
    var llarg = Math.max(m.length, terme.length);
    var curt = Math.min(m.length, terme.length);
    if (pref * 2 < llarg) return false;
    // Amb sis lletres seguides iguals ja no cal mirar la cua: «mensual» i
    // «mensualitat» són la mateixa paraula i es diferencien en quatre.
    if (pref >= 6) return true;
    return pref >= 4 && llarg - curt <= 2;
  }

  /* El que les lletres no poden ajuntar, ho ajuntem a mà. Cada línia és
     una família de formes de la mateixa paraula: la primera és la que
     acostuma a sortir escrita al web, i la resta, com ho escriu la gent.
     Val més una taula que algú pot llegir i corregir que una fórmula que
     encerta el 80% i falla d'una manera que ningú pot preveure. */
  var EQUIVALENTS = [
    // El verb i el nom van per separat: ajuntant-los, «cómo DOY de baja»
    // casava amb qualsevol pregunta que digués «baja» o «hijo».
    'donar dona donem dono donen donat donarse',
    'dar da damos doy dan dado darse darnos',
    'baixa baixes',
    'baja bajas',
    'roba equipacio equipacions samarreta pantalo',
    'ropa equipacion equipaciones camiseta pantalon',
    'kit clothes shirt jersey shorts',
    'revisio reconeixement prova proves examen certificat',
    'revision reconocimiento prueba pruebas examen certificado',
    'check checkup test medical certificate',
    'lesio lesionar lesionat lesionada lesions trencar trencat',
    'lesion lesionarse lesionado lesionada lesiones romper roto',
    'injury injured injuries hurt',
    'plegar deixar deixo deixem abandonar marxar marxem anarsen',
    'dejar dejo dejamos abandonar irse irnos marcharse',
    'quit leave leaving stop stopping',
    'esperar espera llista cua torn',
    'esperar espera lista cola turno',
    'wait waiting list queue',
    'faltar falta falto faltem absencia absent avisar',
    'faltar falta falto faltamos ausencia ausente avisar',
    'miss missing absence absent',
    'jugar juga juguen jugo minuts estona banqueta banca convocatoria',
    'jugar juega juegan juego minutos rato banquillo convocatoria',
    'play plays playing minutes bench squad',
    'telefon numero trucar truco trucada contactar contacte',
    'telefono numero llamar llamo llamada contactar contacto',
    'phone number call calling contact',
    'adreca direccio ubicacio situat lloc pavello nau',
    'direccion ubicacion situado lugar pabellon nave',
    'address location located place venue'
  ];

  var GERMANES = {};
  EQUIVALENTS.forEach(function (linia) {
    var mots = linia.split(' ');
    mots.forEach(function (m) {
      GERMANES[m] = (GERMANES[m] || []).concat(mots);
    });
  });

  function teLArrel(camp, terme) {
    if (terme.length < 4) return camp.indexOf(terme) >= 0;
    var mots = camp.split(' ');
    var germanes = GERMANES[terme];
    for (var i = 0; i < mots.length; i++) {
      if (mateixaParaula(mots[i], terme)) return true;
      if (germanes && germanes.indexOf(mots[i]) >= 0) return true;
    }
    return false;
  }

  function pesTerme(t) {
    var comptes = pesFaq[lang] || {};
    var total = totalPreguntes[lang] || 1;
    var df = comptes[t] || 0;
    // Una paraula que no surt a CAP pregunta no és rara: és muda. No pot
    // casar amb res, i donar-li el pes màxim per raresa la convertia en la
    // paraula que decidia la consulta. «Quantes entrenadores TENIU» exigia
    // trobar «teniu», que el web no diu mai, i deixava «entrenadores» de
    // banda; «quin metro em VA bé» es quedava sense resposta perquè «va» i
    // «em» pesaven més que «metro». Al terra, doncs: que no faci nosa.
    // (Amb tolerància a faltes encara pot casar-hi alguna cosa —«quotta» amb
    // «quota»—, i per això el terra no és zero.)
    // Només les curtes: «president» tampoc no surt escrit enlloc (el web
    // diu «Qui presideix»), i és exactament la paraula que decideix.
    // …i sempre que no en tinguem una germana escrita a EQUIVALENTS: «ropa»
    // no surt a cap pregunta perquè el web escriu «equipació», i justament
    // per això és la paraula que la consulta té de distintiu.
    if (!df && t.length <= 5 && !GERMANES[t]) return 0.15;
    return Math.max(0.12, Math.log((total + 1) / (df + 1)) / Math.log(total + 1));
  }

  /* Com `puntuaCamp`, però amb l'arrel de recanvi. Les preguntes són text
     curt i escrit per una altra persona: qui busca «assegurança» es troba
     «estan assegurats», i qui busca «beques», «beca social». La distància
     d'edició no ho salva —hi ha tres lletres de diferència— i l'arrel sí. */
  function puntuaCampFaq(camp, terme, tol) {
    var p = puntuaCamp(camp, terme, tol);
    if (p) return p;
    // Gairebé tant com encertar-la: per a un text curt escrit per una altra
    // persona, «assegurats» és «assegurança». El que no val és confondre
    // arrels diferents, i d'això ja se n'ocupa teLArrel.
    return teLArrel(camp, terme) ? 0.85 : 0;
  }

  function cercaResposta(consulta, families) {
    if (!preparatFaq.length) return null;
    var termes = paraulesPregunta(consulta);
    if (!termes.length) return null;

    // Una paraula solta sol ser un TEMA i no una pregunta: qui escriu
    // «campus» vol la pàgina del campus, no una de les seves set preguntes.
    // Però hi ha paraules que soles ja SÓN la pregunta —«assegurança»,
    // «beques», «president», «quota»— i deixar-les sense resposta era pitjor
    // que el problema que volíem evitar. El que les separa és com de rares
    // siguin: «campus» surt a 23 preguntes, «assegurança» a cap.
    var solaINoDistintiva = termes.length === 1 && pesTerme(termes[0]) < 0.7;
    if (solaINoDistintiva) return null;
    // Amb una paraula sola no cal apujar el llistó: ja l'apuja la regla de
    // dalt (ha de ser rara) i la de sota (ha de sortir a la PREGUNTA, no
    // només a la resposta).
    var nomesUna = termes.length === 1;

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

    // El pes de cada paraula de la consulta: com més rara al corpus de
    // preguntes, més decideix. Comptar les paraules a pes igual era el que
    // feia que «qui és el president» respongués «Qui hi pot jugar?»: casava
    // «qui», que no vol dir res, i es donava per satisfeta amb mitja
    // consulta.
    var pesos = termes.map(function (t) { return pesTerme(t); });
    var pesTotal = pesos.reduce(function (a, b) { return a + b; }, 0) || 1;

    // La paraula que fa que la consulta sigui aquesta i no una altra. Si no
    // surt a la pregunta, no és la pregunta, per bé que casin les altres:
    //   «quant VAL la TEMPORADA»  →  «Quant valen les cistelles al 3x3?»
    //   «com em faig ENTRENADOR»  →  «Com em faig patrocinador?»
    //   «quiero APUNTAR a mi hija» → «¿Puedo pedir que mi hija no salga…?»
    // Totes tres casaven prou paraules per passar qualsevol llindar, i cap
    // de les tres responia el que s'havia preguntat.
    // Entre les paraules de debò: una de tres lletres pot ser rara al corpus
    // («pel») i no vol dir res. Si no n'hi ha cap de prou llarga, la regla
    // no s'aplica.
    // «El meu FILL», «mi HIJO»: diuen de qui es parla, no de què. Compten
    // per a la cobertura i per a la puntuació, però no poden ser la paraula
    // que decideix: al corpus surten poc i el pes per raresa les triava, i
    // llavors qualsevol pregunta que no digués «hijo» quedava descartada
    // («cómo doy de baja a mi hijo» no trobava la pregunta de la baixa).
    var rar = -1;
    for (var z = 0; z < termes.length; z++) {
      if (NO_DECIDEIXEN[termes[z]]) continue;
      if (termes[z].length >= 4 && (rar < 0 || pesos[z] > pesos[rar])) rar = z;
    }

    for (var i = 0; i < preparatFaq.length; i++) {
      var d = preparatFaq[i], punts = 0, encerts = 0, pesEncert = 0;

      var teElRar = (termes.length < 2 || rar < 0) ? 2 : 0;
      for (var j = 0; j < termes.length; j++) {
        var t = termes[j], tol = tolerancia(t);
        var aQ = puntuaCampFaq(d.q, t, tol);
        var aR = aQ ? 0 : puntuaCampFaq(d.r, t, tol);
        // Compta sobretot a la PREGUNTA: una resposta llarga acaba contenint
        // qualsevol paraula i el filtre deixaria de filtrar. Però a la
        // resposta també val, perquè hi ha preguntes que fan servir una
        // paraula i responen amb una altra («no surti a les fotos» a la
        // pregunta, «per treure una imatge» a la resposta).
        if (j === rar) {
          if (teLArrel(d.q, t)) teElRar = 2;
          else if (teElRar !== 2 && teLArrel(d.r, t)) teElRar = 1;
        }
        if (aQ || aR) {
          encerts++;
          pesEncert += pesos[j];
          // puntuaCamp ja dona 1 a la paraula sencera i 0.8 a un principi de
          // paraula. Elevat al quadrat, la diferència entre encertar-la
          // («entrena») i quedar-s'hi a prop («entrenar») deixa de ser un
          // matís i decideix.
          punts += (aQ * aQ * 3.5 + aR * 0.7) * pesos[j];
        }
      }
      if (!encerts || !teElRar) continue;
      // Una consulta d'una sola paraula ha de sortir a la pregunta: si només
      // és a la resposta, la relació és massa indirecta per donar-la per
      // bona sense res més que la sostingui.
      if (nomesUna && teElRar !== 2) continue;

      // Cobertura pesada: no quantes paraules s'han trobat, sinó quina part
      // del que la consulta té de distintiu. Trobar «qui» i no «president»
      // és no haver trobat res.
      var cobertura = pesEncert / pesTotal;
      if (cobertura < 0.5) continue;
      punts *= 0.6 + cobertura;

      // Si la paraula clau només surt a la resposta i no a la pregunta, la
      // parella és més fluixa: que ho hagi de compensar amb la resta. Ara bé,
      // si hi ha sortit TOT el que s'ha escrit, ja no és fluixa —només és una
      // pregunta redactada amb unes altres paraules— i penalitzar-la dues
      // vegades (aquí i al pes del camp) la deixava fora sense motiu.
      if (teElRar === 1 && cobertura < 0.95) punts *= 0.7;

      for (var k = 0; k < ampliats.length; k++) {
        if (d.q.indexOf(ampliats[k]) >= 0) punts += 0.5;
      }
      // La pregunta escrita gairebé igual guanya de llarg.
      if (termes.length > 1 && d.q.indexOf(frase) >= 0) punts += 6;
      // Una pregunta curta que conté tot el que s'ha demanat és més precisa
      // que una de llarga que ho conté de passada.
      punts += Math.max(0, 3 - d.q.split(' ').length / 8);

      // D'on surt la resposta importa: la mateixa puntuació treta de /faq/ o
      // de /escoleta/ val més que treta d'un article del blog, que sol
      // parlar del bàsquet en general i no del club. Era el cas de «quant
      // val la temporada», que responia amb quant valen les cistelles al
      // 3x3, d'un article sobre les regles del 3x3.
      punts *= 0.85 + (pesPagina[d.f.u] || 45) / 300;

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

  /* Quan no trobem res, la pregunta del web que més s'hi assembla.
     No és la resposta —no arriba al llindar, i per això no la donem com a
     bona—, però sovint és el que la persona volia i no sabia com dir. */
  function voliesDir(consulta) {
    var termes = paraulesPregunta(consulta);
    if (!termes.length || !preparatFaq.length) return null;
    var millor = null, millorPunts = 0;
    for (var i = 0; i < preparatFaq.length; i++) {
      var d = preparatFaq[i];
      if (d.f.l !== lang) continue;
      var n = 0;
      for (var j = 0; j < termes.length; j++) {
        if (teLArrel(d.q, termes[j])) n += pesTerme(termes[j]);
      }
      if (n > millorPunts) { millorPunts = n; millor = d.f; }
    }
    return millorPunts >= 0.55 ? millor : null;
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
  /* ============================================================
     7 · QUAN EL WEB NO HO DIU · el formulari
     Fins aquí res no ha sortit del navegador de qui cerca. Això és
     l'excepció, i és una excepció que decideix la persona: fins que no
     prem el botó no s'envia res. El que s'envia va a la mateixa Apps
     Script que la resta de formularis del web, marcat amb source
     'cerca' perquè al full es puguin llegir a part i, sobretot, perquè
     es puguin llegir com el que són: la llista del que la gent busca i
     el web encara no respon.
     ============================================================ */

  var WHATSAPP = '+34698425153';

  function enllacWhatsApp(text) {
    return 'https://api.whatsapp.com/send?phone=' + WHATSAPP +
      '&text=' + encodeURIComponent(text);
  }

  function formulariHTML(idPrefix, q) {
    var id = idPrefix + '-f';
    return '<form class="cerca-form" novalidate>' +
      '<p class="cerca-form-t"><strong>' + escapa(T.formTitol) + '</strong>' +
      '<span>' + escapa(T.formPeu) + '</span></p>' +
      '<div class="cerca-form-camps">' +
        '<label for="' + id + 'n">' + escapa(T.formNom) + '</label>' +
        '<input id="' + id + 'n" name="nom" type="text" autocomplete="name" required>' +
        '<label for="' + id + 'v">' + escapa(T.formVia) + '</label>' +
        '<input id="' + id + 'v" name="contacteVia" type="text" autocomplete="tel" required>' +
        '<label for="' + id + 'p">' + escapa(T.formPregunta) + '</label>' +
        '<textarea id="' + id + 'p" name="missatge" rows="2" required>' + escapa(q) + '</textarea>' +
      '</div>' +
      '<p class="cerca-form-err" hidden>' + escapa(T.formFalta) + '</p>' +
      '<button type="submit" class="cerca-form-btn">' + escapa(T.formEnvia) + '</button>' +
      '<p class="cerca-form-avis">' + escapa(T.formAvis) +
        '<a href="' + escapa(T.privacitatRuta) + '">' + escapa(T.formPrivacitat) + '</a></p>' +
      '</form>' +
      '<div class="cerca-form-fet" hidden role="status">' +
        '<strong>' + escapa(T.formGracies) + '</strong>' +
        '<a class="cerca-preguntaho" target="_blank" rel="noopener" href="' +
          escapa(enllacWhatsApp(q)) + '">' +
          '<strong>' + escapa(T.formPressa) + '</strong><span>' + T.formWhatsApp + '</span></a>' +
      '</div>';
  }

  /* L'adreça d'enviament viu a /js/canals.js, que és l'únic lloc del web on
     s'escriu. La majoria de pàgines no el carreguen, i carregar-lo a totes
     per un formulari que gairebé mai no surt seria pagar-lo sempre: es
     demana just quan cal. */
  function endpoint(quan) {
    var ja = (window.CANALS || {}).bustiaEndpoint;
    if (ja || window.CANALS) return quan(ja);
    var sc = document.createElement('script');
    sc.src = '/js/canals.js';
    sc.onload = function () { quan((window.CANALS || {}).bustiaEndpoint); };
    sc.onerror = function () { quan(null); };
    document.head.appendChild(sc);
  }

  function muntaFormulari(arrel, q) {
    var form = arrel.querySelector('.cerca-form');
    if (!form) return;
    var fet = arrel.querySelector('.cerca-form-fet');
    var err = arrel.querySelector('.cerca-form-err');
    var boto = form.querySelector('.cerca-form-btn');
    var camps = Array.prototype.slice.call(form.querySelectorAll('[required]'));

    // El formulari es demana abans de saber l'adreça: així, quan la persona
    // acaba d'escriure, ja hi és i l'enviament no espera cap descàrrega.
    var adreca;
    endpoint(function (a) { adreca = a; });

    camps.forEach(function (c) {
      c.addEventListener('input', function () {
        if (c.getAttribute('aria-invalid') === 'true' && c.value.trim()) {
          c.removeAttribute('aria-invalid');
        }
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var primer = null;
      camps.forEach(function (c) {
        var mal = !c.value.trim();
        c.setAttribute('aria-invalid', mal ? 'true' : 'false');
        if (mal && !primer) primer = c;
      });
      err.hidden = !primer;
      if (primer) { primer.focus(); return; }

      boto.disabled = true;
      boto.textContent = T.formEnviant;

      // Amb mode no-cors mai no sabem si ha arribat. Val més donar-ho per
      // enviat i ensenyar el WhatsApp que deixar la persona mirant un botó
      // apagat: el mateix criteri que a js/informacio.js.
      var tancat = false;
      function acaba() {
        if (tancat) return;
        tancat = true;
        form.hidden = true;
        fet.hidden = false;
        var wa = fet.querySelector('a');
        if (wa) wa.href = enllacWhatsApp(form.querySelector('textarea').value.trim() || q);
        fet.setAttribute('tabindex', '-1');
        fet.focus();
      }

      var dades = {
        source: 'cerca',
        idioma: lang,
        tema: 'Cerca sense resposta',
        cerca: q,
        nom: form.querySelector('[name=nom]').value.trim(),
        contacteVia: form.querySelector('[name=contacteVia]').value.trim(),
        missatge: form.querySelector('[name=missatge]').value.trim()
      };

      setTimeout(acaba, 6000);
      endpoint(function (a) {
        adreca = a || adreca;
        if (!adreca) { acaba(); return; }
        fetch(adreca, {
          method: 'POST', mode: 'no-cors',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(dades)
        }).then(acaba, acaba);
      });
      if (window.gtag) window.gtag('event', 'cerca_sense_resposta_enviada');
    });
  }

  function construeixHTML(idPrefix) {
    return '' +
      '<form class="cerca-camp" role="search" autocomplete="off">' +
        '<svg class="cerca-lupa" viewBox="0 0 24 24" aria-hidden="true"><path d="M10.5 3a7.5 7.5 0 1 1-4.6 13.4l-3.2 3.2a1 1 0 0 1-1.4-1.4l3.2-3.2A7.5 7.5 0 0 1 10.5 3Zm0 2a5.5 5.5 0 1 0 0 11 5.5 5.5 0 0 0 0-11Z"/></svg>' +
        '<input type="search" id="' + idPrefix + 'Input" class="cerca-input" ' +
          'placeholder="' + escapa(T.placeholder) + '" aria-label="' + escapa(T.titol) + '" ' +
          'aria-controls="' + idPrefix + 'Llista" spellcheck="false">' +
        '<button type="button" class="cerca-neteja" hidden aria-label="' + escapa(T.esborrar) + '">&times;</button>' +
      '</form>' +
      /* Sense role="listbox" ni combobox: el contenidor barreja títols,
         blocs de resposta i botons en tots els estats, i un listbox només
         admet opcions com a fills (axe-core: aria-required-children). Les
         fletxes segueixen funcionant com a drecera; el lector de pantalla
         hi veu enllaços normals i el recompte l'anuncia el role="status". */
      '<div class="cerca-cos" id="' + idPrefix + 'Llista" aria-label="' + escapa(T.resultats) + '"></div>' +
      '<p class="cerca-sr" role="status"></p>' +
      '<p class="cerca-pista"><kbd>&uarr;</kbd><kbd>&darr;</kbd> ' + escapa(T.pista) + '</p>';
  }

  function Cercador(arrel, idPrefix, esPagina) {
    var self = this;
    this.arrel = arrel;
    this.esPagina = esPagina;
    // pinta() viu al prototipus i no veu l'argument: els identificadors del
    // formulari els necessita per lligar cada etiqueta amb el seu camp.
    this.idPrefix = idPrefix;
    arrel.innerHTML = construeixHTML(idPrefix);
    this.input = arrel.querySelector('.cerca-input');
    this.cos = arrel.querySelector('.cerca-cos');
    this.sr = arrel.querySelector('.cerca-sr');
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
      if (sel && a.scrollIntoView) a.scrollIntoView({ block: 'nearest' });
    });
  };

  Cercador.prototype.recolliEnllacos = function () {
    this.enllacos = Array.prototype.slice.call(this.cos.querySelectorAll('a[data-cerca-r]'));
    this.actiu = this.enllacos.length ? 0 : -1;
    this.marcaActiu();
  };

  /* El que sent qui no veu la capa: el recompte de resultats, un cop per
     tecleig, sense llegir-li tota la llista. */
  Cercador.prototype.anuncia = function (text) {
    if (this.sr) this.sr.textContent = text || '';
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
    this.anuncia('');
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
    var teResposta = false;

    // 1r · La resposta escrita pel club, si n'hi ha cap que encaixi.
    var faq = cercaResposta(q, res.families);
    if (faq) {
      teResposta = true;
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
        teResposta = true;
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
        this.anuncia(T.cap + ' «' + q + '»');
      var buit = '<div class="cerca-bloc"><p class="cerca-estat"><strong>' +
        escapa(T.cap) + ' «' + escapa(q) + '»</strong><br>' + escapa(T.capAjuda) + '</p>';
      var proposta = voliesDir(q);
      if (proposta) {
        buit += '<p class="cerca-titol" style="margin-top:6px">' + escapa(T.voliesDir) + '</p>' +
          '<div class="cerca-fitxes"><button type="button" class="cerca-fitxa" ' +
          'data-pregunta="' + escapa(proposta.q) + '">' + escapa(proposta.q) + '</button></div>';
      }
      // I si el web de debò no ho diu enlloc, que no s'acabi aquí. Abans hi
      // havia només l'enllaç al WhatsApp; el problema d'aquell enllaç és que
      // qui no vol obrir el WhatsApp es quedava sense res, i el club es
      // quedava sense saber què s'havia buscat i no s'havia trobat. Ara la
      // pregunta ja escrita s'aprofita per obrir un formulari: qui deixa el
      // contacte rep resposta, i el WhatsApp queda per a qui té pressa,
      // després d'enviar-ho.
      buit += formulariHTML(this.idPrefix, q) + '</div>';
      this.cos.innerHTML = buit;
      muntaFormulari(this.cos, q);
      this.estatBuitSuggeriments();
      var self2 = this;
      Array.prototype.forEach.call(this.cos.querySelectorAll('[data-pregunta]'), function (b) {
        b.addEventListener('click', function () {
          self2.input.value = b.getAttribute('data-pregunta');
          self2.input.focus();
          self2.pinta();
        });
      });
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

    // Hi ha pàgines, però ningú no ha escrit la resposta: són vint-i-set de
    // cada cent consultes de l'auditoria. Enviar aquesta gent a llegir-se
    // tres pàgines és fer-los la feina a ells. Aquí el formulari va al peu i
    // plegat, que la llista de resultats continua sent el que han demanat.
    if (!teResposta && mostra.length) {
      html += '<details class="cerca-bloc cerca-plec"><summary>' +
        escapa(T.formTitol) + '</summary>' + formulariHTML(this.idPrefix, q) + '</details>';
    }

    this.cos.innerHTML = html;
    muntaFormulari(this.cos, q);
    Array.prototype.forEach.call(this.cos.querySelectorAll('[data-pregunta]'), function (b) {
      b.addEventListener('click', function () {
        self.input.value = b.getAttribute('data-pregunta');
        self.input.focus();
        self.pinta();
      });
    });
    this.recolliEnllacos();
    this.anuncia(this.enllacos.length === 1 ? T.unResultat : this.enllacos.length + ' ' + T.resultats);

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
    capa.addEventListener('keydown', atrapaFocus);
    return capa;
  }

  /* El focus no pot sortir d'una finestra modal: si en surt, qui va amb
     teclat o amb lector de pantalla acaba navegant per la pàgina de sota
     sense veure-la, i sense manera d'entendre on és. Ho va trobar
     tests/cerca/prova-ux.mjs: catorze tabulacions i el focus era al body. */
  function enfocables() {
    return Array.prototype.filter.call(
      capa.querySelectorAll('a[href], button, input, textarea, select, summary, [tabindex]:not([tabindex="-1"])'),
      function (e) {
        if (e.hasAttribute('disabled') || e.offsetParent === null) return false;
        // El contingut d'un <details> plegat, fora. Ni offsetParent ni
        // getClientRects no el descarten (el navegador l'amaga amb
        // content-visibility, no amb display), i la llista es pensava que
        // després del resum hi havia quatre camps més. Com que el tabulador
        // no els hi porta, el focus se saltava el final de la llista i
        // sortia de la capa.
        return !e.closest('details:not([open])') || e.tagName === 'SUMMARY';
      });
  }

  function atrapaFocus(e) {
    if (e.key !== 'Tab' || !capa || capa.hidden) return;
    var llista = enfocables();
    if (!llista.length) return;
    var primer = llista[0], ultim = llista[llista.length - 1];
    var actiu = document.activeElement;
    if (!capa.contains(actiu)) {
      e.preventDefault();
      primer.focus();
    } else if (e.shiftKey && actiu === primer) {
      e.preventDefault();
      ultim.focus();
    } else if (!e.shiftKey && actiu === ultim) {
      e.preventDefault();
      primer.focus();
    }
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
    // Però mai A DINS d'un .head-nav: per sota de 1080 px aquell menú es
    // torna una tira amb scroll ocult i el botó quedava retallat fora de
    // la vista, amb el punt de toc ocupat pel commutador d'idioma. Com a
    // germà, just després del menú, es veu a qualsevol amplada.
    if (costat.classList.contains('head-nav') && costat.parentElement) {
      costat.parentElement.insertBefore(b, costat.nextSibling);
    } else {
      costat.appendChild(b);
    }

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
      // A la pàgina de 404 no hi ha res a escriure: ja sabem què buscava,
      // ho diu l'adreça que no existeix. /escoleta-2026/ → «escoleta 2026».
      if (!q && pagina.hasAttribute('data-cerca-de-la-ruta')) {
        q = decodeURIComponent(location.pathname)
          .replace(/\.[a-z]{2,5}$/i, '')
          .replace(/[\/_-]+/g, ' ')
          .replace(/\b(es|en|index|html|404|www|amp)\b/g, ' ')
          .replace(/\s+/g, ' ').trim();
      }
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
