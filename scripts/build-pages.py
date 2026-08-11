#!/usr/bin/env python3
"""
Generador de les pàgines interiors de cbgrupbarna.info (campus, 3x3, blog).

Totes comparteixen capçalera, peu, JSON-LD i /css/barna.css, de manera que
afegir una pàgina o un article nou és afegir una entrada aquí i executar:

    python3 scripts/build-pages.py

No toca ni la portada ni /partits/ ni /escoleta/: aquelles pàgines es mantenen
a mà perquè tenen lògica pròpia.
"""
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://cbgrupbarna.info"
WA_CLUB = "https://api.whatsapp.com/send?phone=+34698425153"
WA_ESCOLETA = "https://wa.me/34646205526"
WEB_3X3 = "https://cbgrupbarna-3x3timechamber.com"
WEB_3X3_INSCRIPCIO = WEB_3X3 + "/#inscripcio"


def wa(text):
    """Text codificat per a un enllaç de WhatsApp (?text=...)."""
    return quote(text)

# ─────────────────────────────────────────────────────────────── esquelet ────

def head(title, desc, url, image, extra_ld=None, keywords=None):
    ld = json.dumps(extra_ld, ensure_ascii=False, indent=2) if extra_ld else None
    kw = f'\n<meta name="keywords" content="{keywords}">' if keywords else ''
    return f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0A0A0A">
<title>{title}</title>
<meta name="description" content="{desc}">{kw}
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta property="og:type" content="article">
<meta property="og:site_name" content="CB Grup Barna">
<meta property="og:locale" content="ca_ES">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@cbgrupbarna">
<link rel="icon" href="/logo.png">
<link rel="apple-touch-icon" href="/icon-192.png">
<link rel="manifest" href="/manifest.json">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@200;300;400;500&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/barna.css">
{'<script type="application/ld+json">' + chr(10) + ld + chr(10) + '</script>' if ld else ''}
</head>
<body>
<a href="#main" class="skip">Saltar al contingut</a>
<header class="head">
  <div class="head-in">
    <a class="head-brand" href="/" aria-label="CB Grup Barna · inici">
      <img src="/logo.png" alt="Escut del CB Grup Barna" width="30" height="30">
      <span>CB Grup Barna</span>
    </a>
    <nav class="head-nav" aria-label="Navegació principal">
      <a href="/escoleta/">Escoleta</a>
      <a href="/campus/" class="opt">Campus</a>
      <a href="/3x3/" class="opt">3x3</a>
      <a href="/blog/" class="opt">Blog</a>
      <a href="/premsa/" class="opt">Premsa</a>
      <a href="/patrocinadors/" class="opt">Patrocinadors</a>
      <a href="/#info">Informació</a>
    </nav>
  </div>
</header>
<main id="main">"""


def crumbs(items):
    parts = []
    for i, (name, href) in enumerate(items):
        parts.append(f'<a href="{href}">{name}</a>' if href else f'<span>{name}</span>')
    return '<div class="wrap"><nav class="crumb" aria-label="Fil d\'Ariadna">' + ' · '.join(parts) + '</nav></div>'


FOOT = f"""</main>
<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-col">
        <h3>El Barna</h3>
        <a href="/escoleta/">Escola de bàsquet</a>
        <a href="/campus/">Campus de bàsquet</a>
        <a href="/3x3/">Torneig 3x3</a>
        <a href="/patrocinadors/">Patrocinadors i partners</a>
        <a href="/grup-barna-dades-oficials/">Dades oficials</a>
      </div>
      <div class="foot-col">
        <h3>Temporada</h3>
        <a href="/partits/">Partits i resultats</a>
        <a href="/partits/calendaris/">Calendaris per equip</a>
        <a href="/fotos/">Galeria de fotos</a>
        <a href="/premidonaesport/">Premi Dona i Esport</a>
        <a href="/blog/">Blog</a>
        <a href="/premsa/">Articles i premsa</a>
      </div>
      <div class="foot-col">
        <h3>Contacte</h3>
        <a href="/#info">Demanar informació</a>
        <a href="mailto:info@cbgrupbarna.com">info@cbgrupbarna.com</a>
        <a href="https://wa.me/34698425153">+34 698 425 153</a>
        <p>La Nau del Clot · Sant Martí<br>08018 Barcelona</p>
      </div>
      <div class="foot-col">
        <h3>Xarxes</h3>
        <a href="https://www.instagram.com/cbgrupbarna/" target="_blank" rel="noopener">Instagram</a>
        <a href="https://www.tiktok.com/@cbgrupbarna" target="_blank" rel="noopener">TikTok</a>
        <a href="https://www.cbgrupbarna.com" target="_blank" rel="noopener">cbgrupbarna.com</a>
      </div>
    </div>
    <div class="foot-btm">
      <div class="foot-mark">#Som<em>Clot</em></div>
      <div class="foot-legal">© 2026 CB Grup Barna · Bàsquet base al Clot des de 1965</div>
    </div>
  </div>
</footer>
</body>
</html>
"""


def faq_block(pairs):
    """FAQ visible + el JSON-LD corresponent, sempre sincronitzats."""
    html = '<div class="faq">' + ''.join(
        f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in pairs) + '</div>'
    ld = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}} for q, a in pairs]}
    return html, ld


EXT = ' target="_blank" rel="noopener"'


def closer(title, text, buttons):
    b = ''
    for t, u, c, d in buttons:
        ext = EXT if u.startswith('http') else ''
        b += f'<a href="{u}" class="btn {c}"{ext} data-cta="{d}">{t}</a>'
    return f'<div class="closer"><h2>{title}</h2><p>{text}</p><div class="btn-row">{b}</div></div>'


def write(path, html):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding='utf-8')
    return f"  {path}  ({len(html)//1024} KB)"


BREADCRUMB = lambda items: {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + h}
    for i, (n, h) in enumerate(items)]}


# ════════════════════════════════════════════════════════════ /campus/ ════

def build_campus():
    url = SITE + "/campus/"
    title = "Campus de bàsquet a Barcelona · CB Grup Barna | Estiu al Clot"
    desc = ("Campus de bàsquet a Barcelona per a nens i nenes de base. El campus d'estiu del "
            "CB Grup Barna al Clot, Districte de Sant Martí: setmanes intensives de tecnificació, "
            "grups per edat i places limitades. Informació i llista d'espera.")
    faq_html, faq_ld = faq_block([
        ("Per a quines edats és el campus de bàsquet?",
         "El campus del CB Grup Barna és per a jugadors i jugadores de base, des de l'edat de "
         "l'Escoleta fins a categories cadet i júnior. Els grups es fan per edat i nivell, de manera "
         "que un nen o nena que comença no entrena amb qui ja porta anys competint."),
        ("Cal jugar al CB Grup Barna per apuntar-s'hi?",
         "No. El campus és obert a jugadors i jugadores de qualsevol club de Barcelona i de la "
         "província. Cada setmana hi ha places per a gent del Barna i places per a gent de fora."),
        ("Quantes places hi ha per setmana?",
         "El campus treballa amb un límit aproximat de 50 places per setmana per mantenir la ràtio "
         "d'entrenador per jugador. Les setmanes s'omplen per ordre d'inscripció i les darreres "
         "edicions s'han completat abans de començar."),
        ("On es fa el campus?",
         "Al barri del Clot, Districte de Sant Martí de Barcelona. La Nau del Clot és el punt "
         "esportiu principal del CB Grup Barna."),
        ("Quan obren les inscripcions de la propera edició?",
         "Les dates de la propera edició s'anuncien a aquesta pàgina i a Instagram (@cbgrupbarna). "
         "Qui vulgui rebre l'avís abans que s'obri al públic pot demanar-ho pel WhatsApp del club "
         "(+34 698 425 153) i entra a la llista d'avisos."),
    ])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "@id": url + "#campus",
         "name": "Campus de bàsquet · CB Grup Barna",
         "alternateName": ["Campus de baloncesto en Barcelona", "Campus d'estiu de bàsquet Barcelona",
                           "Grup Barna Campus"],
         "description": desc, "serviceType": "Campus de bàsquet",
         "url": url, "provider": {"@id": SITE + "/#club"},
         "areaServed": [{"@type": "City", "name": "Barcelona"},
                        {"@type": "AdministrativeArea", "name": "Província de Barcelona"}],
         "audience": {"@type": "PeopleAudience", "suggestedMinAge": 5, "suggestedMaxAge": 17},
         "availableChannel": {"@type": "ServiceChannel", "serviceUrl": url,
                              "servicePhone": {"@type": "ContactPoint", "telephone": "+34698425153",
                                               "contactType": "Inscripcions campus"}}},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title,
         "description": desc, "inLanguage": ["ca-ES", "es-ES"],
         "about": {"@id": url + "#campus"}, "isPartOf": {"@id": SITE + "/#website"}},
        faq_ld,
        BREADCRUMB([("CB Grup Barna", "/"), ("Campus de bàsquet", "/campus/")]),
    ]}

    body = f"""
{crumbs([("Inici", "/"), ("Campus de bàsquet", None)])}
<div class="wrap">
  <div class="phead">
    <p class="eyebrow red">Campus de bàsquet · El Clot · Barcelona</p>
    <h1>Campus de bàsquet a Barcelona</h1>
    <p class="lede">Setmanes intensives de bàsquet i tecnificació al Clot, Districte de Sant Martí,
    obertes a jugadors i jugadores de qualsevol club de Barcelona i de la província. Grups per edat
    i nivell, places limitades per setmana.</p>
    <div class="btn-row" style="margin-top:28px">
      <a href="{WA_CLUB}&amp;text=Hola!%20Vull%20informaci%C3%B3%20del%20Campus%20de%20b%C3%A0squet%20del%20CB%20Grup%20Barna"
         class="btn red" target="_blank" rel="noopener" data-cta="campus-wa">Demanar informació</a>
      <a href="/#info" class="btn ghost" data-cta="campus-form">Avisa'm de la propera edició</a>
    </div>
    <div class="phead-media">
      <img src="/img/campus-hero.webp" alt="Jugadores del campus de bàsquet del CB Grup Barna amb la samarreta del campus" width="1200" height="675" fetchpriority="high">
    </div>
  </div>

  <div class="narrow prose">
    <h2>Què és el campus del Barna</h2>
    <p>El campus de bàsquet del <strong>CB Grup Barna</strong> és el programa d'entrenament intensiu
    que el club organitza durant les vacances escolars al barri del Clot. No és una activitat de
    lleure amb pilota: és <strong>tecnificació</strong>, amb sessions dedicades a un aspecte concret
    del joc i grups fets per edat i nivell.</p>
    <p>El club el treballa amb <strong>Time Chamber</strong>, que aporta la metodologia de treball
    individual. La combinació és la que defineix el campus: el volum de repeticions d'una escola de
    tecnificació amb l'ambient d'equip d'un club de barri amb seixanta anys d'història.</p>

    <h2>Com s'organitza</h2>
    <p>Cada setmana té un focus propi, de manera que qui ve més d'una setmana no repeteix continguts.
    Aquests són els mòduls que ha treballat el club en les darreres edicions:</p>
    <ul>
      <li><strong>Flow Camp</strong> — lectura de joc i presa de decisions.</li>
      <li><strong>TC Basics</strong> — fonaments: peus, equilibri, mecànica.</li>
      <li><strong>Shooting Academy</strong> — tir, en totes les seves situacions.</li>
      <li><strong>One &amp; One Mastery</strong> — el joc d'un contra un.</li>
      <li><strong>Ballhandling Lab</strong> — maneig de pilota i bot sota pressió.</li>
      <li><strong>Skills Lab Experience</strong> — treball combinat d'habilitats.</li>
    </ul>

    <div class="facts">
      <div><b><em>50</em></b><span>Places per setmana</span></div>
      <div><b>1965</b><span>Any de fundació del club</span></div>
      <div><b>+34</b><span>Equips federats</span></div>
      <div><b>BCN</b><span>El Clot · Sant Martí</span></div>
    </div>

    <h2>A qui va dirigit</h2>
    <p>A nens i nenes que juguen a bàsquet o que hi volen començar, tant si són del CB Grup Barna com
    si vénen d'un altre club. Cada setmana el club reserva places per als seus jugadors i places
    obertes a jugadors i jugadores de fora, i els grups es tanquen per edat i nivell perquè ningú no
    entreni per sobre ni per sota del que li toca.</p>
    <p>Si el vostre fill o filla encara no ha començat i té entre 4 i 7 anys, el camí natural no és el
    campus sinó <a href="/escoleta/">l'Escoleta</a>, l'escola de bàsquet del club, que funciona tot
    l'any amb en Julio Torralba.</p>

    <h2>Propera edició</h2>
    <p>Les dates de la propera edició i l'obertura d'inscripcions s'anuncien en aquesta pàgina i a
    <a href="https://www.instagram.com/cbgrupbarna/" target="_blank" rel="noopener">@cbgrupbarna</a>.
    Les darreres edicions s'han omplert abans de començar, així que la manera segura d'entrar-hi és
    demanar l'avís previ: el club escriu a qui és a la llista quan s'obren les places, un dia abans
    de publicar-ho.</p>

    <h2>Preguntes freqüents</h2>
    {faq_html}

    <div style="margin-top:clamp(34px,5vw,60px)">
    {closer("Vull que m'aviseu del proper campus",
            "Deixa'ns el contacte i t'escrivim quan s'obrin les inscripcions, abans de publicar-les.",
            [("Demanar informació", "/#info", "red", "campus-closer-form"),
             ("WhatsApp del club", WA_CLUB + "&amp;text=Hola!%20Vull%20info%20del%20Campus%20de%20b%C3%A0squet", "ghost", "campus-closer-wa")])}
    </div>
  </div>
</div>
"""
    return write("campus/index.html",
                 head(title, desc, url, SITE + "/img/campus-hero.webp", ld,
                      "campus bàsquet Barcelona, campus baloncesto Barcelona, campus estiu bàsquet, "
                      "grup barna campus, campus tecnificació bàsquet Barcelona") + body + FOOT)


# ═══════════════════════════════════════════════════════ /patrocinadors/ ════

# (fitxer del logo, nom, Instagram real si el tenim confirmat — si no, None
#  i es mostra sense enllaç. Verificat a partners-mapa/index.html.)
PARTNERS = [
    ("aquamiga.png", "Aquamiga", "https://www.instagram.com/aquamiga_oficial/"),
    ("armand-optics.png", "Armand Òptics", "https://www.instagram.com/armandoptics/"),
    ("clinica-dental-bac-de-roda.png", "Clínica Dental Bac de Roda", "https://www.instagram.com/clinicadentalbacderoda/"),
    ("eix-clot.png", "Eix Clot", "https://www.instagram.com/eixclot/"),
    ("eix-comercial-sant-marti.png", "Eix Comercial Sant Martí", None),
    ("foto-jane.png", "Foto Jané", None),
    ("fundacio-mullor.png", "Fundació Mullor", None),
    ("gbk-globabasket.png", "GBK · Globasket", "https://www.instagram.com/globasket/"),
    ("herbolaris-montserrat.png", "Herbolaris Montserrat", "https://www.instagram.com/herbolari.montserrat/"),
    ("illa-fantasia.png", "Illa Fantasia", "https://www.instagram.com/illafantasia/"),
    ("instax-fujifilm.png", "instax · Fujifilm España", "https://www.instagram.com/instaxcamara/"),
    ("l-aquarium-de-barcelona.png", "L'Aquàrium de Barcelona", None),
    ("manual-colors.png", "Manual Color", "https://www.instagram.com/manualcolor/"),
    ("melosa-hamburgueseria.png", "Melosa Hamburgueseria", "https://www.instagram.com/melosahamburgueseria/"),
    ("mercat-dels-encants.png", "Mercat dels Encants", None),
    ("ovella-negra.png", "Ovella Negra", "https://www.instagram.com/ovellanegrabcn/"),
    ("panteres-grogues.png", "Panteres Grogues", None),
    ("romeo-abogados.png", "Romeo Abogados", "https://www.instagram.com/romeoabogados/"),
    ("stepback-podologia.png", "Stepback Podologia", "https://www.instagram.com/stepback.podologia/"),
    ("time-chamber.png", "Time Chamber", "https://www.instagram.com/timechamber_es/"),
    ("tot-salut.png", "Tot Salut", None),
    ("westfield-glories.png", "Westfield Glòries", "https://www.instagram.com/westfieldglories/"),
    ("zapic-ai.png", "Zapic AI", None),
]


def build_patrocinadors():
    url = SITE + "/patrocinadors/"
    title = "Patrocina el CB Grup Barna · Patrocinadors i partners a Barcelona"
    desc = ("Fes que la teva marca formi part del CB Grup Barna: un club de base de +450 jugadores i "
            "jugadores i famílies al Clot, Barcelona. Nivells Or, Plata i Bronze, col·laboració en "
            "espècie i contacte directe amb l'equip comercial per WhatsApp.")

    faq_html, faq_ld = faq_block([
        ("Com em faig patrocinador o partner del CB Grup Barna?",
         "Escriu a l'equip comercial de patrocinis per WhatsApp (+34 698 425 153) o omple el "
         "formulari de contacte del club. Ens reunim, coneixem la vostra marca i us proposem el "
         "nivell que encaixi amb els vostres objectius, sense compromís."),
        ("Quins nivells de patrocini hi ha?",
         "Tres nivells —Or, Plata i Bronze— segons implicació i contraprestacions, més la "
         "col·laboració a mida o en espècie per a empreses que aporten producte o servei en lloc "
         "de diners. El nivell Or és exclusiu: només una marca per temporada."),
        ("Puc col·laborar amb producte o servei en lloc de diners?",
         "Sí. Bona part de les col·laboracions del club són en espècie: material esportiu, "
         "transport per a desplaçaments, fisioteràpia, càtering d'esdeveniments, impremta o "
         "fotografia. Ho valorem igual que una aportació econòmica."),
        ("Què rep la meva empresa a canvi del patrocini?",
         "Segons el nivell: logo al web i al mur de partners, mencions a Instagram, presència a "
         "la cartelleria d'esdeveniments, logo a l'equipació o al calentament, activació al 3x3 o "
         "al campus i, al nivell Or, naming a la samarreta de joc i exclusivitat de sector."),
        ("Amb qui parlo per tancar un patrocini?",
         "Amb l'equip comercial del club per WhatsApp (+34 698 425 153). Responem en menys de 24 "
         "hores i, si encaixa, agafem una reunió per conèixer-vos abans de parlar de xifres."),
    ])

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "@id": url + "#patrocini",
         "name": "Patrocini i partners · CB Grup Barna",
         "alternateName": ["Patrocinadors CB Grup Barna", "Sponsoring club de bàsquet Barcelona",
                           "Patrocini esportiu Barcelona"],
         "description": desc, "serviceType": "Patrocini esportiu",
         "url": url, "provider": {"@id": SITE + "/#club"},
         "areaServed": [{"@type": "City", "name": "Barcelona"},
                        {"@type": "AdministrativeArea", "name": "Província de Barcelona"}],
         "availableChannel": {"@type": "ServiceChannel", "serviceUrl": url,
                              "servicePhone": {"@type": "ContactPoint", "telephone": "+34698425153",
                                               "contactType": "Patrocinis i col·laboracions"}}},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title,
         "description": desc, "inLanguage": ["ca-ES", "es-ES"],
         "about": {"@id": url + "#patrocini"}, "isPartOf": {"@id": SITE + "/#website"}},
        faq_ld,
        BREADCRUMB([("CB Grup Barna", "/"), ("Patrocinadors", "/patrocinadors/")]),
    ]}

    why_cards = ''.join(f"""<div class="card"><div class="card-media"><img src="/patrocinis/photos/{img}" alt="{alt}" loading="lazy"></div><div class="card-body"><span class="card-tag">{tag}</span><h3>{h}</h3><p>{p}</p></div></div>""" for img, alt, tag, h, p in [
        ("s2c_entrada.jpg", "Grada plena a un partit del CB Grup Barna",
         "Comunitat", "Comunitat físico-emocional",
         "Més de 450 jugadores i jugadors i les seves famílies, presents cada setmana al Clot. "
         "No és abast fred a una pantalla: és gent real que ve, s'asseu a la grada i torna."),
        ("club_cbgb016.jpg", "Nena amb una pilota de bàsquet amb representants del club",
         "Valors", "Valors i espai segur",
         "Formació, cantera, secció femenina real i “espai segur” com a norma. Una marca "
         "que hi entra compra reputació de barri, no impressions."),
        ("instax_banner.jpg", "Lona d'un patrocinador al pavelló del CB Grup Barna",
         "Audiència pròpia", "Moments amb audiència pròpia",
         "El 3x3 de Glòries, el campus d'estiu, la presentació de temporada: “mitjans” "
         "propis del club amb públic ja fet, on el patrocinador s'hi puja."),
    ])

    def wa_btn(label, text, css, cta):
        return f'<a href="{WA_CLUB}&amp;text={wa(text)}" class="btn {css}" target="_blank" rel="noopener" data-cta="{cta}">{label}</a>'

    tiers = ''.join(f"""<div class="card"><div class="card-body"><span class="card-tag">{tag}</span><h3>{h}</h3><p>{p}</p><ul>{''.join(f'<li>{li}</li>' for li in items)}</ul>{wa_btn('Vull parlar del nivell ' + h, f"Hola! Sóc d'una empresa i vull informació del nivell {h} de patrocini del CB Grup Barna", 'ghost', 'tier-' + h.lower())}</div></div>""" for tag, h, p, items in [
        ("Nivell Or · Partner principal · Exclusiu, 1 sola marca", "Or",
         "El patrocinador principal del Barna. Naming a la samarreta de joc i exclusivitat de sector.",
         ["Logo principal a la samarreta de joc", "Exclusivitat de sector (cap competidor hi entra)",
          "Co-branding d'un esdeveniment propi (3x3 o campus)",
          "Vídeo de marca anual i presència a tota la comunicació de temporada",
          "Reunió de balanç amb la Junta del club", "Tot el que inclou el nivell Plata"]),
        ("Nivell Plata · Partner · 3-4 marques", "Plata",
         "Per a marques de barri consolidades que volen presència real i contingut propi.",
         ["Logo a l'equipació d'un equip o al calentament", "Un reel anual dedicat al partner",
          "Activació al 3x3 o al campus (stand, sampling, categoria patrocinada)",
          "Pack de fotos i vídeo del club per a les xarxes del partner",
          "Tot el que inclou el nivell Bronze"]),
        ("Nivell Bronze · Col·laborador · 6-8 marques", "Bronze",
         "La porta d'entrada per a comerços i pimes del barri: presència i pertinença.",
         ["Logo al web i al mur de partners", "Menció de benvinguda a Instagram (post i story)",
          "Presència a la cartelleria dels esdeveniments del club",
          "Invitació a un esdeveniment del club cada temporada"]),
        ("A mida · Col·laboració en espècie", "A mida",
         "Material, servei o producte en lloc de diners: igual de valuós per al club.",
         ["Material esportiu, transport, fisioteràpia o càtering d'esdeveniments",
          "Impremta, fotografia o altres serveis professionals",
          "Es valora i es reconeix igual que una aportació econòmica",
          "Nivell de contraprestació segons l'encaix"]),
    ])

    partners_grid = ''.join(
        (f'<a class="partner-logo" href="{ig}" target="_blank" rel="noopener" title="{nom} · Segueix a Instagram"><img src="/partners/{img}" alt="{nom}" loading="lazy"></a>'
         if ig else
         f'<span class="partner-logo" title="{nom}"><img src="/partners/{img}" alt="{nom}" loading="lazy"></span>')
        for img, nom, ig in PARTNERS)

    body = f"""
{crumbs([("Inici", "/"), ("Patrocinadors", None)])}
<div class="wrap">
  <div class="phead">
    <p class="eyebrow red">Patrocini · Partners · El Clot</p>
    <h1>Fes que la teva marca formi part del Barna</h1>
    <p class="lede">No venem espai publicitari: obrim la porta d'un club de +450 jugadores i famílies
    al barri del Clot, seixanta anys d'història i una comunitat que es reconeix en el que fem.
    El teu negoci no hi <em>paga</em>, hi <strong>entra</strong>.</p>
    <div class="btn-row" style="margin-top:28px">
      {wa_btn("Vull ser patrocinador", "Hola! Sóc d'una empresa i vull informació per ser patrocinador o partner del CB Grup Barna", 'red', 'patro-wa-hero')}
      <a href="#nivells" class="btn ghost" data-cta="patro-nivells">Veure els nivells</a>
    </div>
    <div class="phead-media">
      <img src="/patrocinis/photos/team_sf17.jpg" alt="Jugadores del CB Grup Barna amb el logo d'instax Fujifilm a la samarreta de joc" width="1200" height="1800" fetchpriority="high">
    </div>
  </div>

  <div class="cards c3">{why_cards}</div>

  <div class="narrow prose">
    <div class="facts">
      <div><b>1965</b><span>Fundació del club</span></div>
      <div><b>+450</b><span>Jugadores i jugadors</span></div>
      <div><b><em>34</em>+</b><span>Equips federats</span></div>
      <div><b>68%</b><span>Dones a l'staff tècnic</span></div>
    </div>
  </div>
</div>

<div class="wrap section band-soft" id="nivells">
  <p class="eyebrow red center">Contraprestacions</p>
  <h2 class="center" style="margin-top:14px">Nivells de col·laboració</h2>
  <p class="narrow center lede" style="margin:18px auto 0">Tres nivells segons implicació, més la
  col·laboració a mida per a qui aporta producte o servei en lloc de diners. Sense catàleg tancat:
  cada proposta s'adapta al que la vostra marca vulgui aconseguir.</p>
  <div class="cards" style="margin-top:clamp(28px,4vw,46px)">{tiers}</div>
</div>

<div class="wrap section">
  <div class="narrow prose center">
    <p class="eyebrow red">Partners actuals</p>
    <h2>Qui ja forma part del Barna</h2>
    <p>Comerços del barri i col·laboradors de fora que ja hi són. Segueix-los: cada follow que els
    arriba des del club és part del que reben a canvi.</p>
  </div>
  <div class="partners-grid">{partners_grid}</div>
  <div class="btn-row center" style="justify-content:center;margin-top:24px">
    <a href="https://www.instagram.com/cbgrupbarna/" class="btn ghost" target="_blank" rel="noopener" data-cta="patro-follow-club">Segueix @cbgrupbarna</a>
  </div>

  <div class="narrow prose" style="margin-top:clamp(40px,6vw,72px)">
    <h2>Avantatges per a la família del Barna</h2>
    <p>Alguns partners activen descomptes i avantatges exclusius per a jugadores, jugadors, famílies
    i seguidors del club: aquí és on aniran apareixent, partner a partner, a mesura que es confirmin.
    Si ja ets partner i vols oferir-ne un, escriu-nos i el publiquem.</p>
    {wa_btn("Quins avantatges tinc com a família del Barna?", "Hola! Quins avantatges o descomptes tinc com a família o seguidor del CB Grup Barna?", 'ghost', 'patro-avantatges-wa')}
  </div>

  <div class="narrow prose">
    <h2>Preguntes freqüents</h2>
    {faq_html}
  </div>

  <div style="margin-top:clamp(34px,5vw,60px)">
  {closer("Parlem del teu patrocini",
          "Cap catàleg tancat: expliquem el projecte, escoltem què busca la vostra marca i us "
          "proposem un o dos nivells que encaixin. Contacte directe amb l'equip comercial.",
          [("WhatsApp de patrocinis", WA_CLUB + "&amp;text=" + wa("Hola! Vull parlar del patrocini del CB Grup Barna"), "red", "patro-closer-wa"),
           ("Escriu-nos un correu", "mailto:info@cbgrupbarna.com", "ghost", "patro-closer-mail")])}
  </div>
</div>
"""
    return write("patrocinadors/index.html",
                 head(title, desc, url, SITE + "/patrocinis/photos/team_sf17.jpg", ld,
                      "patrocinadors CB Grup Barna, patrocini bàsquet Barcelona, partners club bàsquet, "
                      "esponsorització esportiva Barcelona, col·laboradors bàsquet base") + body + FOOT)


# ═══════════════════════════════════════════════════════════════ /3x3/ ════

def build_3x3():
    url = SITE + "/3x3/"
    title = "3x3 Barcelona · Torneig de bàsquet 3x3 a Glòries | CB Grup Barna"
    desc = ("Torneig de bàsquet 3x3 a Barcelona organitzat pel CB Grup Barna a Westfield Glòries. "
            "Categories de base i obertes, format urbà i inscripció per equips. Informació de la "
            "propera edició i galeries de les anteriors.")
    faq_html, faq_ld = faq_block([
        ("Què és el 3x3 de Westfield Glòries?",
         "És el torneig urbà de bàsquet 3x3 que el CB Grup Barna organitza al centre comercial "
         "Westfield Glòries de Barcelona, amb Time Chamber i l'entorn comercial del Clot-Glòries. "
         "Es juga a pista exterior, en format 3 contra 3 a una cistella."),
        ("Qui hi pot jugar?",
         "Hi ha categories de base i categories obertes, de manera que hi poden jugar tant equips "
         "de clubs com colles d'amics. No cal estar federat per apuntar-se a les categories obertes."),
        ("Com és el format 3x3?",
         "Tres jugadors per equip a una sola cistella, en mitja pista. Els partits són curts i "
         "seguits, així que en un mateix dia un equip juga diverses eliminatòries. És el format "
         "olímpic del bàsquet des dels Jocs de Tòquio."),
        ("Quan és la propera edició?",
         "Les dates s'anuncien en aquesta pàgina, a la web oficial cbgrupbarna-3x3timechamber.com i a "
         "Instagram (@cbgrupbarna). El torneig se sol fer a l'inici de l'estiu. Qui vulgui rebre "
         "l'avís d'obertura d'inscripcions pot demanar-ho pel WhatsApp del club."),
        ("On és exactament?",
         "A Westfield Glòries, a la plaça de les Glòries Catalanes de Barcelona, a tocar del barri "
         "del Clot i del Districte de Sant Martí."),
    ])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "SportsEvent", "@id": url + "#torneig",
         "name": "3x3 Barcelona · Torneig de bàsquet 3x3 a Westfield Glòries",
         "alternateName": ["3x3 Westfield Glòries", "Torneo 3x3 Barcelona", "Bàsquet 3x3 Barcelona"],
         "description": desc, "url": url, "sport": "Bàsquet 3x3",
         "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
         "eventStatus": "https://schema.org/EventScheduled",
         "organizer": {"@id": SITE + "/#club"},
         "location": {"@type": "Place", "name": "Westfield Glòries",
                      "address": {"@type": "PostalAddress", "streetAddress": "Av. Diagonal, 208",
                                  "addressLocality": "Barcelona", "postalCode": "08018",
                                  "addressRegion": "Catalunya", "addressCountry": "ES"}},
         "offers": {"@type": "Offer", "url": WEB_3X3_INSCRIPCIO,
                    "availability": "https://schema.org/InStock", "category": "Inscripció per equip"}},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title,
         "description": desc, "inLanguage": ["ca-ES", "es-ES"],
         "about": {"@id": url + "#torneig"}, "isPartOf": {"@id": SITE + "/#website"}},
        faq_ld,
        BREADCRUMB([("CB Grup Barna", "/"), ("3x3 Barcelona", "/3x3/")]),
    ]}

    body = f"""
{crumbs([("Inici", "/"), ("3x3 Barcelona", None)])}
<div class="wrap">
  <div class="phead">
    <p class="eyebrow red">Torneig urbà · Westfield Glòries · Barcelona</p>
    <h1>3x3 Barcelona</h1>
    <p class="lede">El torneig de bàsquet 3x3 que el CB Grup Barna organitza a Westfield Glòries, a
    tocar del Clot. Format urbà, partits curts i seguits, categories de base i categories obertes
    per a colles d'amics.</p>
    <div class="btn-row" style="margin-top:28px">
      <a href="{WEB_3X3_INSCRIPCIO}" class="btn red" target="_blank" rel="noopener"
         data-cta="3x3-inscripcio">Inscriu el teu equip</a>
      <a href="{WA_CLUB}&amp;text=Hola!%20Vull%20informaci%C3%B3%20del%20torneig%203x3%20de%20Barcelona"
         class="btn ghost" target="_blank" rel="noopener" data-cta="3x3-wa">Demanar informació</a>
    </div>
  </div>

  <div class="narrow prose">
    <h2>Què és el bàsquet 3x3</h2>
    <p>El 3x3 és bàsquet a mitja pista: <strong>tres jugadors per equip i una sola cistella</strong>.
    Els partits són curts, el marcador va de pressa i en una jornada un equip pot jugar diverses
    eliminatòries seguides. És el format que va entrar als Jocs Olímpics a Tòquio i el que millor
    funciona al carrer, perquè només necessita mitja pista i una tarda.</p>

    <h2>El 3x3 del Barna, a Glòries</h2>
    <p>El CB Grup Barna porta el torneig a <strong>Westfield Glòries</strong>, a la plaça de les
    Glòries Catalanes, amb <strong>Time Chamber</strong> i el teixit comercial del Clot i de Glòries.
    La idea és senzilla: treure el bàsquet del pavelló i posar-lo on hi ha gent, en un lloc pel qual
    passen milers de persones un dissabte al matí.</p>
    <p>El torneig té categories de base, pensades per als equips dels clubs, i categories obertes on
    s'hi pot apuntar qualsevol colla sense estar federada. Aquesta barreja és el que li dona
    l'ambient: al mateix parquet hi ha equips de club i grups d'amics del barri.</p>

    <div class="facts">
      <div><b><em>3</em></b><span>Jugadors per equip</span></div>
      <div><b>10</b><span>Categories</span></div>
      <div><b>60</b><span>Equips per edició</span></div>
      <div><b>BCN</b><span>Westfield Glòries</span></div>
    </div>

    <h2>Edicions anteriors</h2>
    <p>Les galeries de les edicions que ja s'han jugat estan obertes a tothom:</p>
    <ul>
      <li><a href="/galeria-3x3-glories/">Galeria del 3x3 Westfield Glòries</a></li>
      <li><a href="/fotos-3x3/">Fotos del torneig 3x3</a></li>
      <li><a href="/fotos/">Galeria general del club</a></li>
    </ul>

    <h2>Com apuntar-hi un equip</h2>
    <p>Les inscripcions es fan directament a la web oficial del torneig,
    <a href="{WEB_3X3}" target="_blank" rel="noopener">cbgrupbarna-3x3timechamber.com</a>, per equip
    i no per jugador. Les places són limitades i les darreres edicions s'han omplert abans de
    començar, així que com més aviat es formalitzi la inscripció, més segur. Si encara no s'han
    obert les inscripcions de la propera edició, es pot demanar l'avís previ pel WhatsApp del club
    o deixant el contacte al <a href="/#info">formulari d'informació</a>.</p>

    <h2>Preguntes freqüents</h2>
    {faq_html}

    <div style="margin-top:clamp(34px,5vw,60px)">
    {closer("Vull apuntar un equip al proper 3x3",
            "La inscripció es fa per equip a la web oficial del torneig.",
            [("Inscriure's a cbgrupbarna-3x3timechamber.com", WEB_3X3_INSCRIPCIO, "red", "3x3-closer-inscripcio"),
             ("WhatsApp del club", WA_CLUB + "&amp;text=Hola!%20Vull%20apuntar%20un%20equip%20al%203x3", "ghost", "3x3-closer-wa")])}
    </div>
  </div>
</div>
"""
    return write("3x3/index.html",
                 head(title, desc, url, SITE + "/og-image.jpg", ld,
                      "3x3 Barcelona, bàsquet 3x3 Barcelona, torneig 3x3, baloncesto 3x3 Barcelona, "
                      "3x3 Westfield Glòries, torneo 3x3 Barcelona") + body + FOOT)


# ═══════════════════════════════════════════════════════════════ /blog/ ════

ARTICLES = [
 {
  "slug": "a-quina-edat-comencar-basquet",
  "date": "2026-08-05",
  "tag": "Guia per a famílies",
  "title": "A quina edat pot començar un nen o nena a jugar a bàsquet?",
  "seo_title": "A quina edat començar a jugar a bàsquet? Guia per edats | CB Grup Barna",
  "desc": ("Als 4 anys ja es pot començar a jugar a bàsquet en una escola d'iniciació. Guia per edats "
           "—escoleta, premini, mini i categories federades— per a famílies de Barcelona que no saben "
           "quan apuntar el seu fill o filla."),
  "kw": "a quina edat començar bàsquet, edad para empezar baloncesto, escoleta bàsquet 4 anys, "
        "minibàsquet edats, categories bàsquet base",
  "lede": ("És la pregunta que més ens fan les famílies del barri. La resposta curta: als quatre anys. "
           "La llarga té matisos, i val la pena conèixer-los abans d'apuntar ningú enlloc."),
  "body": """
<h2>La resposta curta: als 4 anys</h2>
<p>Un nen o una nena pot començar a jugar a bàsquet als <strong>quatre anys</strong>, però no a
l'esport que veiem per televisió. A aquesta edat el que es treballa és <strong>motricitat</strong>:
córrer i parar, saltar, llançar, rebre, coordinar-se amb algú altre. La pilota és l'excusa, i és una
excusa boníssima, perquè el bot obliga a controlar el cos i la mirada alhora.</p>
<p>Per això els clubs no els posen a competir. Els posen a jugar. A
<a href="/escoleta/">l'Escoleta del CB Grup Barna</a>, per exemple, els grups són de 4 a 7 anys,
mixtos i separats per edat, i el calendari no són partits de lliga sinó trobades amb altres clubs.</p>

<h2>Les edats, categoria a categoria</h2>
<p>Aquest és el recorregut habitual al bàsquet català. Les edats són orientatives: el que mana és
l'any de naixement, no el curs escolar.</p>
<ul>
  <li><strong>4 a 7 anys · Escoleta o escola de bàsquet</strong> — iniciació. Sense competició
  federada. Equips mixtos.</li>
  <li><strong>8 i 9 anys · Premini</strong> — primera competició, encara molt formativa.</li>
  <li><strong>10 i 11 anys · Mini</strong> — minibàsquet: cistella més baixa i pilota més petita.</li>
  <li><strong>12 i 13 anys · Preinfantil i infantil</strong> — es passa a mesures d'adult.</li>
  <li><strong>14 i 15 anys · Cadet</strong> — l'etapa on el joc es fa reconeixible.</li>
  <li><strong>16 i 17 anys · Júnior</strong> — l'última categoria de formació.</li>
  <li><strong>A partir de 18 · Sub-22 i sènior</strong> — competició adulta.</li>
</ul>

<h2>I si comença més tard?</h2>
<p>Passa constantment i no és cap problema. Un nen que arriba als deu o als dotze anys sense haver
tocat una pilota s'incorpora a la seva categoria per edat, no per nivell, i s'hi posa al dia en una
temporada. El bàsquet base no és un embut: cap club de barri que funcioni bé deixa fora ningú per
haver començat tard.</p>
<p>El que sí que canvia és el <strong>motiu</strong> pel qual entra. Als quatre anys s'apunta perquè
els pares hi veuen una activitat; als dotze s'apunta perquè ell o ella ho vol. La segona motivació
sol aguantar més.</p>

<blockquote>El millor moment per començar és quan el nen o la nena té ganes. La resta —edat,
categoria, nivell— ho resol el club.</blockquote>

<h2>Com saber si li agradarà</h2>
<p>No es pot saber des de casa. Per això gairebé tots els clubs deixen fer un
<strong>entrenament de prova sense compromís</strong>: s'hi va un dia, es fa la sessió sencera amb el
grup que li tocaria i després es decideix. És l'única manera honesta de saber-ho, i no costa res.</p>
<p>Si sou de Barcelona i us hi voleu acostar, a l'Escoleta del Barna la porta en
<strong>Julio Torralba</strong> i es pot reservar dia directament amb ell al 646 205 526.</p>
""",
  "faq": [
   ("A quina edat pot començar un nen a jugar a bàsquet?",
    "Als 4 anys ja es pot començar en una escola d'iniciació o escoleta, on es treballa motricitat i "
    "coordinació amb pilota sense competició federada. La competició comença als 8 anys, a premini."),
   ("Quina és l'edat del minibàsquet?",
    "El minibàsquet és per a nens i nenes de 10 i 11 anys. Es juga amb cistella més baixa i pilota "
    "més petita que les d'adult. Abans hi ha el premini, de 8 i 9 anys."),
   ("És tard per començar a jugar a bàsquet als 12 anys?",
    "No. Un jugador o jugadora que comença als 12 anys s'incorpora a la categoria que li toca per "
    "any de naixement i es posa al dia en una temporada. Als clubs de base l'entrada no depèn del nivell."),
   ("Nens i nenes entrenen junts?",
    "A les edats d'iniciació (4 a 7 anys) els equips solen ser mixtos. A partir de la competició "
    "federada es divideixen en categories masculines i femenines."),
  ],
 },
 {
  "slug": "com-triar-escola-basquet-barcelona",
  "date": "2026-08-05",
  "tag": "Guia per a famílies",
  "title": "Com triar una escola de bàsquet a Barcelona",
  "seo_title": "Com triar una escola de bàsquet a Barcelona · 7 coses a mirar | CB Grup Barna",
  "desc": ("Set criteris per triar escola de bàsquet a Barcelona: ràtio d'entrenadors, grups per edat, "
           "proximitat, quota, competició i continuïtat. Guia per a famílies amb nens de 4 a 12 anys."),
  "kw": "escola bàsquet Barcelona, escuela baloncesto Barcelona, escola de bàsquet nens, "
        "club bàsquet base Barcelona, escoleta bàsquet",
  "lede": ("A Barcelona hi ha desenes de clubs i tots diuen el mateix al web. Aquests són els set punts "
           "que de veritat diferencien una escola de bàsquet d'una altra."),
  "body": """
<h2>1. Quants entrenadors hi ha per grup</h2>
<p>És el primer que s'ha de preguntar i el que menys es pregunta. Un grup de vint criatures de cinc
anys amb un sol entrenador no és una escola de bàsquet: és una guarderia amb pilotes. Amb dos
adults per grup, la sessió canvia completament.</p>

<h2>2. Si els grups es fan per edat o per comoditat</h2>
<p>Un nen de quatre anys i un de set no poden entrenar junts: ni tenen el mateix cos ni la mateixa
capacitat d'atenció. Els clubs que se'l prenen seriosament separen <strong>tres grups</strong> dins
de la franja d'iniciació. Els que no, ajunten tothom i ho anomenen «treball per nivells».</p>

<h2>3. La distància de casa</h2>
<p>Sona prosaic i és decisiu. Una activitat que implica creuar mitja ciutat dos cops per setmana
s'abandona al febrer. Un club <strong>del barri</strong> aguanta anys, perquè el nen hi va sol quan
creix i perquè els companys d'equip són els mateixos de l'escola i del parc.</p>

<h2>4. Què passa quan compleix vuit anys</h2>
<p>Aquesta és la pregunta que separa una escola d'una acadèmia. Si el club té equips federats a
<strong>totes les categories</strong>, el nen passa de l'escoleta al premini sense canviar de lloc ni
d'amics. Si no en té, als vuit anys tocarà buscar club nou i començar de zero.</p>

<h2>5. Si hi ha línia femenina de veritat</h2>
<p>No val el «tenim un equip de noies». Val mirar <strong>quants</strong> equips femenins hi ha, en
quines categories i si arriben a sènior. Un club amb noies només a les edats petites és un club on
les noies pleguen.</p>

<h2>6. La quota, i què inclou</h2>
<p>Demaneu el preu anual complet: quota, equipació, fitxa federativa i desplaçaments. La diferència
entre clubs sol ser menor del que sembla un cop es compara el mateix.</p>

<h2>7. Que us deixin provar</h2>
<p>Qualsevol club que confiï en el que fa us deixarà anar un dia a fer una sessió sencera. Si
posen pegues, ja teniu la resposta.</p>

<h2>I l'Escoleta del Barna?</h2>
<p>Al <a href="/escoleta/">CB Grup Barna</a>, al barri del Clot, l'escola de bàsquet és per a nens i
nenes de <strong>4 a 7 anys</strong>, amb equips mixtos, <strong>tres grups per edat</strong> i
trobades amb altres clubs de Barcelona i de la província. En complir vuit anys es passa als equips
federats del mateix club, que en té més de trenta-quatre. La porta en
<strong>Julio Torralba</strong> (646 205 526) i el primer entrenament és de prova, sense compromís.</p>
<p>D'aquesta pista han sortit jugadors i jugadores que han arribat a l'ACB, a la Lliga Femenina
Endesa i al FC Barcelona. No és el motiu per apuntar-hi ningú als cinc anys, però diu alguna cosa
sobre la continuïtat del lloc.</p>
""",
  "faq": [
   ("Què s'ha de mirar en una escola de bàsquet?",
    "Els punts que de debò diferencien són: nombre d'entrenadors per grup, si els grups estan "
    "separats per edat, la proximitat de casa, si el club té equips federats a totes les categories "
    "per continuar-hi, si té línia femenina real, el cost anual complet i si deixen fer un "
    "entrenament de prova."),
   ("Quant costa una escola de bàsquet a Barcelona?",
    "Varia per club. Cal demanar sempre el cost anual complet —quota, equipació, fitxa federativa i "
    "desplaçaments— perquè la comparació entre clubs sigui real."),
   ("Quina escola de bàsquet hi ha al Clot o a Sant Martí?",
    "El CB Grup Barna té la seva Escoleta al barri del Clot, Districte de Sant Martí, per a nens i "
    "nenes de 4 a 7 anys, amb continuïtat als equips federats del club a partir dels 8 anys."),
   ("Es pot provar abans d'apuntar-s'hi?",
    "Sí, i és molt recomanable. Al CB Grup Barna el primer entrenament és de prova i sense "
    "compromís; es reserva dia amb en Julio Torralba al 646 205 526."),
  ],
 },
 {
  "slug": "campus-basquet-barcelona-guia",
  "date": "2026-08-05",
  "tag": "Guia per a famílies",
  "title": "Campus de bàsquet a Barcelona: què mirar abans d'apuntar-hi ningú",
  "seo_title": "Campus de bàsquet a Barcelona · Guia per triar-ne un | CB Grup Barna",
  "desc": ("Guia per triar campus de bàsquet a Barcelona: diferència entre campus de lleure i de "
           "tecnificació, ràtios, grups per edat, horaris i preu. Amb la informació del campus del "
           "CB Grup Barna al Clot."),
  "kw": "campus bàsquet Barcelona, campus baloncesto Barcelona, campus estiu bàsquet, "
        "campus tecnificació bàsquet, grup barna campus",
  "lede": ("Tots els campus prometen el mateix en el cartell. La diferència es veu en tres o quatre "
           "detalls que no surten a la publicitat."),
  "body": """
<h2>Primer: campus de lleure o campus de tecnificació?</h2>
<p>Són dues coses diferents i totes dues legítimes. Un <strong>campus de lleure</strong> combina
bàsquet amb piscina, jocs i excursions; l'objectiu és que el nen passi la setmana bé. Un
<strong>campus de tecnificació</strong> dedica les hores a entrenar aspectes concrets del joc: tir,
bot, un contra un, lectura de situacions.</p>
<p>Ni un és millor que l'altre: depèn de què vulgui la criatura. El que no s'hi val és pagar un de
tecnificació i trobar-se un de lleure, o a l'inrevés. Pregunteu-ho directament.</p>

<h2>Quants jugadors hi ha per entrenador</h2>
<p>És l'indicador que ho explica gairebé tot. En tecnificació, per sobre de dotze o catorze jugadors
per entrenador no hi ha correcció individual possible: hi ha vigilància. Els campus seriosos limiten
les places precisament per això, i per això s'omplen.</p>

<h2>Com fan els grups</h2>
<p>Un campus que ajunta tothom en un sol grup gran està organitzat per a la comoditat de qui el fa,
no per al nen. Els grups s'han de fer per <strong>edat i nivell</strong>: qui comença ha de poder
fallar sense sentir-se ridícul, i qui ja competeix ha de poder exigir-se.</p>

<h2>Els horaris reals</h2>
<p>Mireu l'hora d'entrada, la de sortida i si hi ha acollida. Un campus que acaba a la una i mitja
quan tots dos pares treballen fins a les sis és un problema logístic disfressat d'activitat.</p>

<h2>Què inclou el preu</h2>
<p>Dinar, samarreta, assegurança, material. Dos campus amb el mateix preu poden ser molt diferents un
cop s'hi suma el que no estava inclòs.</p>

<h2>El campus del CB Grup Barna</h2>
<p>El <a href="/campus/">campus del Barna</a> es fa al barri del Clot, Districte de Sant Martí, i és
de tecnificació: cada setmana té un focus propi —fonaments, tir, un contra un, maneig de pilota,
lectura de joc— de manera que qui repeteix setmana no repeteix continguts. Treballa amb un límit
aproximat de <strong>cinquanta places per setmana</strong> per mantenir la ràtio.</p>
<p>És obert a jugadors i jugadores de qualsevol club de Barcelona i de la província, no només als del
Barna. Les darreres edicions s'han omplert abans de començar, així que si us interessa el més pràctic
és <a href="/#info">deixar el contacte</a> i rebre l'avís quan s'obrin les inscripcions.</p>
""",
  "faq": [
   ("Quina diferència hi ha entre un campus de lleure i un de tecnificació?",
    "Un campus de lleure combina bàsquet amb piscina, jocs i excursions i busca que el nen passi bé "
    "la setmana. Un campus de tecnificació dedica les hores a entrenar aspectes concrets del joc "
    "—tir, bot, un contra un— amb grups reduïts i correcció individual."),
   ("Quantes places hauria de tenir un campus de bàsquet?",
    "El que importa no és el total sinó la ràtio: per sobre de dotze o catorze jugadors per "
    "entrenador ja no hi ha correcció individual possible. Els campus de tecnificació limiten les "
    "places per aquest motiu."),
   ("Cal ser d'un club per anar a un campus de bàsquet?",
    "Als campus oberts, no. El campus del CB Grup Barna, per exemple, accepta jugadors i jugadores "
    "de qualsevol club de Barcelona i de la província."),
   ("On es fa el campus de bàsquet del CB Grup Barna?",
    "Al barri del Clot, Districte de Sant Martí de Barcelona. Es pot demanar informació i entrar a "
    "la llista d'avisos pel WhatsApp del club, al +34 698 425 153."),
  ],
 },
 {
  "slug": "que-es-basquet-3x3",
  "date": "2026-08-05",
  "tag": "Bàsquet",
  "title": "Què és el bàsquet 3x3 i on jugar-hi a Barcelona",
  "seo_title": "Bàsquet 3x3: regles i on jugar-hi a Barcelona | CB Grup Barna",
  "desc": ("El 3x3 és bàsquet a mitja pista amb tres jugadors per equip i és esport olímpic des de "
           "Tòquio. Com funciona, en què es diferencia del 5x5 i on jugar torneigs 3x3 a Barcelona."),
  "kw": "3x3 Barcelona, bàsquet 3x3, baloncesto 3x3 Barcelona, torneig 3x3, regles 3x3, "
        "3x3 Westfield Glòries",
  "lede": ("Mitja pista, una cistella, tres contra tres i un partit que dura el que dura un descans. "
           "El format que ha portat el bàsquet al carrer i als Jocs Olímpics."),
  "body": """
<h2>Com funciona</h2>
<p>El 3x3 es juga a <strong>mitja pista amb una sola cistella</strong>. Cada equip té tres jugadors
a pista i un suplent. No hi ha temps morts llargs ni descansos: quan un equip anota, l'altre treu
des de darrere de l'arc i el joc continua.</p>
<p>Les cistelles valen <strong>1 punt</strong> dins de l'arc i <strong>2 punts</strong> fora, no 2 i
3 com al bàsquet de sempre. El partit s'acaba quan un equip arriba a <strong>21 punts</strong> o
quan passen <strong>10 minuts</strong>, el que arribi abans.</p>

<h2>Per què enganxa</h2>
<p>Perquè tothom toca la pilota. Amb tres jugadors no hi ha on amagar-se: en cada possessió has
d'atacar, defensar o alliberar l'espai. I perquè els partits són curts, cosa que en un torneig vol dir
que en una tarda un equip pot jugar-ne sis o set.</p>
<p>També perquè el 3x3 necessita molt poc: mitja pista i sis persones. És el format que ja jugàvem
al pati sense saber que tenia nom, i és el que va convertir-lo en <strong>esport olímpic</strong>
als Jocs de Tòquio.</p>

<h2>En què es diferencia del 5x5</h2>
<ul>
  <li><strong>Espai</strong> — mitja pista, i tothom ataca i defensa la mateixa cistella.</li>
  <li><strong>Puntuació</strong> — 1 i 2 punts, no 2 i 3.</li>
  <li><strong>Durada</strong> — 10 minuts o 21 punts, no quatre quarts.</li>
  <li><strong>Ritme</strong> — sense treta de fons després de cistella: el joc no s'atura.</li>
  <li><strong>Físic</strong> — molt més exigent per minut jugat.</li>
</ul>

<h2>On jugar 3x3 a Barcelona</h2>
<p>A Barcelona el 3x3 s'ha instal·lat sobretot en format de torneig d'un dia, a places i espais
públics. El <a href="/3x3/">3x3 del CB Grup Barna</a> es juga a <strong>Westfield Glòries</strong>,
a la plaça de les Glòries Catalanes, a tocar del barri del Clot, amb categories de base per als
equips de clubs i <strong>categories obertes</strong> on s'hi pot apuntar qualsevol colla sense estar
federada.</p>
<p>Aquesta barreja és el que li dona l'ambient: al mateix parquet hi ha equips de club i grups
d'amics del barri. Les inscripcions són per equip i les places, limitades. Qui vulgui saber quan
s'obren pot <a href="/#info">deixar el contacte</a> o escriure al WhatsApp del club.</p>
""",
  "faq": [
   ("Quantes persones són necessàries per jugar a 3x3?",
    "Tres jugadors per equip a pista, més un suplent opcional. En total, sis persones a mitja pista "
    "amb una sola cistella."),
   ("Quant dura un partit de bàsquet 3x3?",
    "Un partit acaba quan un equip arriba a 21 punts o quan es compleixen 10 minuts de joc, el que "
    "passi primer."),
   ("Quant valen les cistelles al 3x3?",
    "Un punt les cistelles de dins de l'arc i dos punts les de fora, a diferència del bàsquet 5x5, "
    "on valen 2 i 3 punts."),
   ("El 3x3 és esport olímpic?",
    "Sí. El bàsquet 3x3 va debutar als Jocs Olímpics de Tòquio i és disciplina olímpica des d'aleshores."),
   ("On es juga un torneig 3x3 a Barcelona?",
    "El CB Grup Barna organitza el seu torneig 3x3 a Westfield Glòries, a la plaça de les Glòries "
    "Catalanes de Barcelona, amb categories de base i categories obertes per a colles d'amics."),
  ],
 },
 {
  "slug": "basquet-base-sant-marti-clot",
  "date": "2026-08-05",
  "tag": "El barri",
  "title": "Bàsquet base al Clot i a Sant Martí: com funciona un club de barri",
  "seo_title": "Bàsquet base al Clot i Sant Martí, Barcelona | CB Grup Barna",
  "desc": ("Com funciona el bàsquet base al Districte de Sant Martí de Barcelona: categories, fitxa "
           "federativa, calendari i què significa jugar en un club de barri amb seixanta anys d'història."),
  "kw": "bàsquet base Barcelona, bàsquet Sant Martí, club bàsquet Clot, baloncesto base Barcelona, "
        "club bàsquet barri Barcelona",
  "lede": ("Un club de barri no és una versió petita d'un club gran. És una altra cosa, i val la pena "
           "entendre-la abans de decidir on juga el vostre fill o filla."),
  "body": """
<h2>Què vol dir «bàsquet base»</h2>
<p>Bàsquet base és tot el bàsquet formatiu: des de l'escola d'iniciació fins a la categoria júnior.
No és bàsquet «de segona»: és on es forma tothom, inclosos els que després arriben a l'ACB o a la
Lliga Femenina Endesa. La diferència amb el bàsquet professional no és la qualitat de la feina, és
l'objectiu: aquí l'objectiu és <strong>formar persones que segueixin jugant</strong>.</p>

<h2>Com s'estructura la temporada</h2>
<p>La temporada va de setembre a juny. Els equips es federen a la
<strong>Federació Catalana de Basquetbol (FCBQ)</strong>, que assigna grup i publica el calendari.
Es juga cada cap de setmana, alternant camp propi i camp contrari, per tot Barcelona i sovint per la
província: Mataró, Sabadell, Granollers, Tarragona.</p>
<p>Cada jugador necessita <strong>fitxa federativa</strong>, que el club tramita, i que inclou
l'assegurança esportiva. Al CB Grup Barna, el calendari i els resultats de tots els equips es poden
consultar a <a href="/partits/">la pàgina de partits</a>, que es nodreix del calendari oficial de la
FCBQ.</p>

<h2>Un club de barri al Districte de Sant Martí</h2>
<p>El <strong>CB Grup Barna</strong> és del <strong>Clot</strong> des del <strong>1965</strong>.
Seixanta anys al mateix barri vol dir una cosa molt concreta: hi ha entrenadors que van jugar-hi de
petits i pares que hi van jugar abans que els seus fills. Això no surt en cap classificació, però es
nota en com funciona el vestidor.</p>
<p>Avui són més de <strong>trenta-quatre equips federats</strong> i unes <strong>450 jugadores i
jugadors</strong>, des de <a href="/escoleta/">l'Escoleta de 4 a 7 anys</a> fins als sèniors. El club
manté <strong>paritat real</strong>: el mateix nombre de jugadores i jugadors, i el mateix pressupost
per a la línia femenina i la masculina. El model femení està documentat al dossier del
<a href="/premidonaesport/">Premi Dona i Esport</a>.</p>

<h2>Què hauríeu de preguntar a qualsevol club del districte</h2>
<ul>
  <li>Quants equips té a la categoria del vostre fill o filla, i si n'hi ha de nivells diferents.</li>
  <li>Si té continuïtat fins a sènior o si l'itinerari es talla als setze anys.</li>
  <li>Quants equips femenins té, i fins a quina categoria arriben.</li>
  <li>On entrena i quants dies per setmana.</li>
  <li>Cost anual complet, amb fitxa i equipació incloses.</li>
</ul>

<h2>Per on començar</h2>
<p>Si el nen o la nena té entre 4 i 7 anys, el camí és l'escola d'iniciació: al Barna, l'Escoleta amb
en <strong>Julio Torralba</strong> (646 205 526). A partir dels 8, l'entrada és directament a un
equip federat. En tots dos casos, el primer pas és el mateix: anar a fer un
<a href="/#info">entrenament de prova</a> i veure-ho des de dins.</p>
""",
  "faq": [
   ("Què és el bàsquet base?",
    "És tot el bàsquet formatiu, des de l'escola d'iniciació fins a la categoria júnior. L'objectiu "
    "no és el resultat sinó formar jugadors i jugadores que segueixin jugant."),
   ("Quin club de bàsquet hi ha al barri del Clot?",
    "El CB Grup Barna, fundat el 1965, és el club de bàsquet base del Clot, al Districte de Sant "
    "Martí de Barcelona, amb més de 34 equips federats i unes 450 jugadores i jugadors."),
   ("Cal fitxa federativa per jugar a bàsquet base?",
    "Sí, per a la competició federada. La tramita el club davant la Federació Catalana de Basquetbol "
    "i inclou l'assegurança esportiva. A l'escola d'iniciació (4 a 7 anys) no cal."),
   ("Quan comença i acaba la temporada de bàsquet base?",
    "De setembre a juny. Es juga cada cap de setmana, alternant camp propi i camp contrari, dins de "
    "Barcelona i de la província."),
  ],
 },
]


def build_article(a):
    url = f"{SITE}/blog/{a['slug']}/"
    faq_html, faq_ld = faq_block(a["faq"])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": url + "#article",
         "headline": a["title"], "description": a["desc"], "url": url,
         "datePublished": a["date"], "dateModified": a["date"],
         "inLanguage": "ca-ES",
         "author": {"@id": SITE + "/#club"}, "publisher": {"@id": SITE + "/#club"},
         "image": SITE + "/og-image.jpg",
         "isPartOf": {"@id": SITE + "/blog/#blog"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": url}},
        faq_ld,
        BREADCRUMB([("CB Grup Barna", "/"), ("Blog", "/blog/"), (a["title"], "/blog/" + a["slug"] + "/")]),
    ]}
    others = [x for x in ARTICLES if x["slug"] != a["slug"]][:3]
    rel = ''.join(
        f'<a class="card" href="/blog/{o["slug"]}/"><div class="card-body">'
        f'<span class="card-tag">{o["tag"]}</span><h3>{o["title"]}</h3>'
        f'<span class="cta">Llegir</span></div></a>' for o in others)
    body = f"""
{crumbs([("Inici", "/"), ("Blog", "/blog/"), (a["title"][:38] + "…", None)])}
<div class="wrap">
  <div class="phead narrow">
    <p class="eyebrow red">{a["tag"]}</p>
    <h1>{a["title"]}</h1>
    <p class="lede">{a["lede"]}</p>
    <p class="eyebrow" style="margin-top:20px">CB Grup Barna · <time datetime="{a["date"]}">{a["date"]}</time></p>
  </div>
  <article class="narrow prose">
    {a["body"]}
    <h2>Preguntes freqüents</h2>
    {faq_html}
    <div style="margin-top:clamp(34px,5vw,60px)">
    {closer("Voleu informació del club?",
            "Deixa'ns el nom i el contacte i us escrivim amb la informació de l'Escoleta, el campus o l'equip que us toqui.",
            [("Demanar informació", "/#info", "red", "blog-closer-form"),
             ("WhatsApp del club", WA_CLUB, "ghost", "blog-closer-wa")])}
    </div>
  </article>
  <div class="section">
    <p class="eyebrow center">Continua llegint</p>
    <div class="rule"></div>
    <div class="cards c3">{rel}</div>
  </div>
</div>
"""
    return write(f"blog/{a['slug']}/index.html",
                 head(a["seo_title"], a["desc"], url, SITE + "/og-image.jpg", ld, a["kw"]) + body + FOOT)


def build_blog_index():
    url = SITE + "/blog/"
    title = "Blog del CB Grup Barna · Guies de bàsquet base a Barcelona"
    desc = ("Guies per a famílies sobre bàsquet base a Barcelona: a quina edat començar, com triar "
            "escola de bàsquet, campus, bàsquet 3x3 i com funciona un club de barri al Districte de "
            "Sant Martí.")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "@id": url + "#blog", "name": title, "description": desc, "url": url,
         "inLanguage": "ca-ES", "publisher": {"@id": SITE + "/#club"},
         "blogPost": [{"@type": "BlogPosting", "headline": a["title"],
                       "url": f"{SITE}/blog/{a['slug']}/", "datePublished": a["date"],
                       "description": a["desc"]} for a in ARTICLES]},
        BREADCRUMB([("CB Grup Barna", "/"), ("Blog", "/blog/")]),
    ]}
    cards = ''.join(
        f'<a class="card" href="/blog/{a["slug"]}/"><div class="card-body">'
        f'<span class="card-tag">{a["tag"]}</span><h3>{a["title"]}</h3>'
        f'<p>{a["lede"]}</p><span class="cta">Llegir</span></div></a>' for a in ARTICLES)
    body = f"""
{crumbs([("Inici", "/"), ("Blog", None)])}
<div class="wrap">
  <div class="phead narrow center">
    <p class="eyebrow red">Guies per a famílies</p>
    <h1 style="margin-left:auto;margin-right:auto">Blog del Barna</h1>
    <p class="lede" style="margin-left:auto;margin-right:auto">El que ens pregunten les famílies del
    barri, respost sense embuts: a quina edat es comença, com es tria un club, què és un campus de
    tecnificació i com funciona el bàsquet base a Barcelona.</p>
  </div>
  <div class="cards c3" style="padding-bottom:clamp(40px,6vw,80px)">{cards}</div>
</div>
"""
    return write("blog/index.html", head(title, desc, url, SITE + "/og-image.jpg", ld,
                 "bàsquet base Barcelona, blog bàsquet, escola bàsquet, campus bàsquet, 3x3 Barcelona")
                 + body + FOOT)


# ═══════════════════════════════════════════════════════════════ /premsa/ ════

PRESS = [
 {
  "slug": "guia-clot-seixanta-anys-fent-bategar-el-clot",
  "date": "2026-08-08",
  "outlet": "Guia Clot · Camp de l'Arpa",
  "publisher": "Eix Clot",
  "publisher_url": "https://www.eixclot.cat/",
  "publisher_ig": "https://www.instagram.com/eixclot/",
  "author": "Gemma Collell",
  "title": "«El CB Grup Barna: seixanta anys fent bategar el Clot», a Guia Clot",
  "seo_title": "El CB Grup Barna a Guia Clot · Gràcies, Eix Clot i Gemma Collell",
  "desc": ("Gràcies a Eix Clot i a la periodista Gemma Collell per l'article que la revista Guia Clot "
           "ha dedicat al CB Grup Barna pels seus 60 anys. Article complet i fotos de la revista."),
  "kw": "CB Grup Barna premsa, Guia Clot, Eix Clot, Gemma Collell, revista Camp de l'Arpa, "
        "60 anys CB Grup Barna, bàsquet Clot premsa",
  "lede": ("La revista Guia Clot, editada per Eix Clot, ha dedicat el seu article més destacat al "
           "CB Grup Barna pels 60 anys del club. Gràcies, Eix Clot. Gràcies, Gemma Collell."),
  "images": [
    ("article-guia-clot-pagina-1.webp",
     "Portada de l'article «El CB Grup Barna: seixanta anys fent bategar el Clot» a la revista Guia Clot, amb foto de l'equip infantil davant el bàner del club"),
    ("article-guia-clot-pagina-2.webp",
     "Segona pàgina de l'article a Guia Clot, amb foto de l'equip sènior masculí i el text sobre el compromís social del club"),
  ],
  "body": """
<p>Al Clot ens coneixem tots, i quan algú del barri es fixa en la feina que fas cada dia, això
val més que qualsevol titular. Per això volem donar-li les gràcies, amb nom i cognoms, a
<a href="https://www.eixclot.cat/" target="_blank" rel="noopener"><strong>Eix Clot</strong></a>
—l'associació de comerciants i emprenedors del barri— i a la periodista
<strong>Gemma Collell</strong>, que ha escrit l'article més destacat de la revista
<em>Guia Clot · Camp de l'Arpa</em> sobre el CB Grup Barna: seixanta anys de bàsquet base al
barri, explicats amb cura i amb dades certes.</p>
<p>Reproduïm aquí el text complet de l'article, tal com va sortir publicat, perquè qui no hagi
tingut la revista a les mans també el pugui llegir.</p>
""",
  "quote_title": "El CB Grup Barna · Seixanta anys fent bategar el Clot",
  "quote_lede": ("El Club Bàsquet Grup Barna s'ha convertit en un autèntic pilar social i esportiu "
                 "dins del districte de Sant Martí. Amb la inclusió i l'arrelament com a bandera, "
                 "l'entitat fa accessible l'esport a tothom des de la mítica pista de la Nau del Clot."),
  "quote_paras": [
    ("Parlar del Club Bàsquet Grup Barna és parlar de la història viva del Clot. Fundat l'any 1965, "
     "aquest emblemàtic club celebra ja seixanta anys de trajectòria, consolidant-se com un dels "
     "clubs de bàsquet de base més grans i actius de tot el districte de Sant Martí. Al llarg de sis "
     "dècades, l'entitat no només ha vist créixer milers de jugadors i jugadores a les seves pistes, "
     "sinó que ha sabut transformar l'esport en una eina d'articulació social inestimable per a tot "
     "el veïnat. Amb prop de 450 sòcies i socis i prop de 40 equips federats en competició, destaca "
     "a més per una paritat total entre les seves seccions masculina i femenina."),
    ("La clau de l'èxit i de la longevitat del Grup Barna rau en la seva manera única d'entendre la "
     "pràctica esportiva. Lluny de centrar-se exclusivament en els marcadors o la pressió "
     "competitiva, el club s'ha regit sempre per principis innegociables: l'accés universal al "
     "bàsquet, la igualtat real d'oportunitats, la diversitat i un profund arrelament al barri. Per "
     "al Barna, el bàsquet és un dret de tothom i un espai idoni on fer amistats per a tota la vida, "
     "compartint valors com el respecte, la cooperació, la salut, la constància i el compromís "
     "col·lectiu."),
    ("Aquesta ferma filosofia inclusiva es tradueix en fets concrets que omplen d'orgull el "
     "territori. El millor exemple d'això és el projecte del Barna Màgics, un equip de bàsquet "
     "especialment dissenyat per a persones amb discapacitat intel·lectual. Aquesta secció demostra "
     "setmana rere setmana que les barreres no existeixen quan hi ha passió i ganes de fer pinya, "
     "esdevenint un referent d'integració a la ciutat. A més, el club manté un lligam constant amb "
     "la vida comunitària del barri, col·laborant de forma habitual amb l'Eix Comercial del Clot, "
     "les escoles de la zona i l'associacionisme local, participant en activitats solidàries i "
     "festives que dinamitzen el teixit veïnal."),
    ("Aquest valuós i constant compromís social va rebre un important reconeixement oficial per "
     "part de les institucions de la ciutat de Barcelona. El febrer de 2026, l'alcalde de Barcelona, "
     "Jaume Collboni, va visitar personalment la seu oficial del club a la coneguda Nau del Clot. "
     "Durant aquesta trobada formal, l'alcalde va voler conèixer de primera mà els detalls d'aquest "
     "gran projecte esportiu, celebrar formalment els seus 60 anys d'història i lloar la gran "
     "implantació comunitària que l'entitat manté al barri."),
    ("La seva activitat no s'atura mai i es manté ben viva en qualsevol època de l'any. Aquest "
     "mateix estiu, el club s'ha convertit un cop més en el gran dinamitzador dels mesos de calor "
     "gràcies a l'organització del seu aclamat Campus d'Estiu «Time Chamber», on els infants "
     "combinen la millora tècnica de les seves habilitats amb tallers de convivència, a més "
     "d'impulsar els espectaculars torneigs de bàsquet 3x3 al recinte de Westfield Glòries, "
     "dinamitzant tot l'entorn. Si voleu conèixer més a fons la seva tasca, formar part de la seva "
     "gran família de bàsquet base o consultar els seus propers esdeveniments, no dubteu a visitar "
     "el seu lloc web oficial a cbgrupbarna.com. El bàsquet al Clot té un passat gloriós, un present "
     "vibrant i un futur que no para de créixer."),
  ],
  "after": """
<p>El club també apareix al directori de <em>Comerços i serveis de referència</em> de la mateixa
revista, amb l'adreça oficial —Llacuna, 172— i el WhatsApp del club, al costat d'altres negocis i
entitats del barri. Un article i una fitxa al mateix número: gràcies per fer-nos costat,
<a href="https://www.eixclot.cat/" target="_blank" rel="noopener">Eix Clot</a>.</p>
<p class="eyebrow">
  <a href="https://www.eixclot.cat/" target="_blank" rel="noopener">eixclot.cat</a> ·
  <a href="https://www.instagram.com/eixclot/" target="_blank" rel="noopener">@eixclot</a>
</p>
""",
  "faq": [
   ("Qui ha escrit l'article sobre el CB Grup Barna a Guia Clot?",
    "L'article «El CB Grup Barna: seixanta anys fent bategar el Clot» l'ha escrit la periodista "
    "Gemma Collell, per a la revista Guia Clot · Camp de l'Arpa, editada per Eix Clot."),
   ("On es va publicar l'article?",
    "A la revista Guia Clot · Camp de l'Arpa (número 1), editada per l'associació de comerciants "
    "Eix Clot, dins la secció de reportatges destacats del barri."),
   ("De què parla l'article?",
    "Explica els 60 anys d'història del CB Grup Barna com a pilar social i esportiu del Clot i de "
    "Sant Martí: la paritat entre la secció masculina i la femenina, el projecte inclusiu Barna "
    "Màgics, la relació del club amb el barri i el reconeixement de l'Ajuntament de Barcelona."),
   ("El club surt en algun altre lloc de la revista?",
    "Sí. A més de l'article, el CB Grup Barna apareix al directori de comerços i serveis de "
    "referència del mateix número, amb l'adreça del club (Llacuna, 172) i el contacte de WhatsApp."),
  ],
 },
]


def build_press_article(a):
    url = f"{SITE}/premsa/{a['slug']}/"
    faq_html, faq_ld = faq_block(a["faq"])

    gallery = ''.join(
        f'<figure><img src="/premsa/img/{fn}" alt="{alt}" loading="lazy" decoding="async" '
        f'width="1400" height="1750"><figcaption>{alt}</figcaption></figure>'
        for fn, alt in a["images"])

    quote_paras = ''.join(f'<p>{p}</p>' for p in a["quote_paras"])
    quote = f"""
<div class="press-quote">
  <p class="eyebrow red">Article complet · {a["outlet"]}</p>
  <h3 style="margin-bottom:14px">{a["quote_title"]}</h3>
  <p style="font-weight:500;margin-bottom:14px">{a["quote_lede"]}</p>
  {quote_paras}
  <span class="press-quote-by">Text de <b>{a["author"]}</b> · {a["outlet"]} ({a["publisher"]})</span>
</div>
"""

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article",
         "headline": a["title"], "description": a["desc"], "url": url,
         "datePublished": a["date"], "dateModified": a["date"], "inLanguage": "ca-ES",
         "author": {"@id": SITE + "/#club"}, "publisher": {"@id": SITE + "/#club"},
         "image": SITE + f"/premsa/img/{a['images'][0][0]}",
         "isPartOf": {"@id": SITE + "/premsa/#premsa"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": url},
         "citation": {
           "@type": "Article",
           "name": a["quote_title"],
           "author": {"@type": "Person", "name": a["author"]},
           "isPartOf": {"@type": "Periodical", "name": a["outlet"]},
           "publisher": {"@type": "Organization", "name": a["publisher"],
                        "url": a["publisher_url"], "sameAs": [a["publisher_ig"]]},
         },
         "about": {"@id": SITE + "/#club"}},
        faq_ld,
        BREADCRUMB([("CB Grup Barna", "/"), ("Premsa", "/premsa/"), (a["title"], "/premsa/" + a["slug"] + "/")]),
    ]}

    body = f"""
{crumbs([("Inici", "/"), ("Premsa", "/premsa/"), (a["title"][:34] + "…", None)])}
<div class="wrap">
  <div class="phead narrow">
    <p class="eyebrow red">Premsa · {a["outlet"]}</p>
    <h1>Gràcies, Eix Clot</h1>
    <p class="lede">{a["lede"]}</p>
    <div class="press-badge">Text de <b>{a["author"]}</b> · {a["outlet"]} · <time datetime="{a["date"]}">{a["date"]}</time></div>
    <div class="phead-media">
      <img src="/premsa/img/gracies-eix-clot-portada.webp"
           alt="Gràcies, Eix Clot: gràfica d'agraïment del CB Grup Barna per l'article de la revista Guia Clot pels 60 anys del club"
           width="1400" height="1750" fetchpriority="high">
    </div>
  </div>
  <article class="narrow prose">
    {a["body"]}
    <div class="press-grid two">{gallery}</div>
    {quote}
    {a["after"]}
    <figure>
      <img src="/premsa/img/reconeixement-60-anys.webp"
           alt="El CB Grup Barna amb la revista Guia Clot i el reconeixement de la Federació Catalana de Basquetbol pel 60è aniversari del club, Barcelona 2025"
           loading="lazy" decoding="async" width="1400" height="1750">
      <figcaption>Un curs ple d'agraïments: la revista Guia Clot d'Eix Clot i, per una altra banda,
      el reconeixement de la Federació Catalana de Basquetbol pel 60è aniversari del club.</figcaption>
    </figure>
    <h2>Preguntes freqüents</h2>
    {faq_html}
    <div style="margin-top:clamp(34px,5vw,60px)">
    {closer("Vols saber més del CB Grup Barna?",
            "Seixanta anys de bàsquet base al Clot, explicats amb dades oficials.",
            [("Dades oficials del club", "/grup-barna-dades-oficials/", "red", "premsa-closer-dades"),
             ("Demanar informació", "/#info", "ghost", "premsa-closer-info")])}
    </div>
  </article>
</div>
"""
    return write(f"premsa/{a['slug']}/index.html",
                 head(a["seo_title"], a["desc"], url, SITE + f"/premsa/img/{a['images'][0][0]}", ld, a["kw"])
                 + body + FOOT)


def build_premsa_index():
    url = SITE + "/premsa/"
    title = "Articles i premsa · CB Grup Barna"
    desc = ("El CB Grup Barna als mitjans del barri: articles, reportatges i mencions de premsa sobre "
            "el club de bàsquet base del Clot, Districte de Sant Martí de Barcelona.")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#premsa", "name": title, "description": desc, "url": url,
         "inLanguage": "ca-ES", "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#club"},
         "hasPart": [{"@type": "Article", "headline": a["title"], "url": f"{SITE}/premsa/{a['slug']}/",
                      "datePublished": a["date"]} for a in PRESS]},
        BREADCRUMB([("CB Grup Barna", "/"), ("Premsa", "/premsa/")]),
    ]}
    cards = ''.join(
        f'<a class="card" href="/premsa/{a["slug"]}/">'
        f'<div class="card-media"><img src="/premsa/img/{a["images"][0][0]}" alt="{a["images"][0][1]}" loading="lazy" decoding="async"></div>'
        f'<div class="card-body"><span class="card-tag">{a["outlet"]}</span><h3>{a["title"]}</h3>'
        f'<p>{a["lede"]}</p><span class="cta">Llegir l\'article</span></div></a>' for a in PRESS)
    body = f"""
{crumbs([("Inici", "/"), ("Premsa", None)])}
<div class="wrap">
  <div class="phead narrow center">
    <p class="eyebrow red">El Barna als mitjans</p>
    <h1 style="margin-left:auto;margin-right:auto">Articles i premsa</h1>
    <p class="lede" style="margin-left:auto;margin-right:auto">Reportatges i mencions del club a la
    premsa del barri. Gràcies a qui ens dedica el seu temps i la seva feina per explicar el Barna.</p>
  </div>
  <div class="cards" style="padding-bottom:clamp(40px,6vw,80px)">{cards}</div>
</div>
"""
    return write("premsa/index.html", head(title, desc, url, SITE + f"/premsa/img/{PRESS[0]['images'][0][0]}", ld,
                 "premsa CB Grup Barna, Guia Clot, Eix Clot, articles bàsquet Clot") + body + FOOT)


# ═══════════════════════════════════════════════════════════ /partits/calendaris/ ════
#
# La pàgina és una carcassa estàtica: la llista d'equips es dibuixa amb JS a
# partir de partits/data.json (sempre al dia, actualitzat cada dia pel robot
# de la FCBQ) i partits/calendaris/manifest.json (què hi ha generat per a
# cada equip). Així un equip nou —o un de promoció que acaba de rebre
# calendari— apareix sol, sense haver de tornar a executar aquest script.

CATEGORY_PREFIXES = ["Sènior", "Júnior", "Cadet", "Infantil", "Preinfantil", "Mini", "Premini"]


def build_calendaris():
    url = SITE + "/partits/calendaris/"
    title = "Calendaris per equip · descarrega'l en PDF | CB Grup Barna"
    desc = ("Descarrega el calendari complet de la temporada del teu equip: sèniors, júniors, cadets i "
            "infantils del CB Grup Barna. Es genera cada dia a partir del calendari oficial de la FCBQ.")

    faq_html, faq_ld = faq_block([
        ("Com descarrego el calendari del meu equip?",
         "Busca l'equip a la llista, toca la imatge o el botó de descàrrega i es desa al mòbil o ordinador: "
         "una imatge per als equips amb una sola fitxa, un PDF de diverses pàgines per als sèniors, que juguen "
         "lliga d'ida i tornada."),
        ("Per què no hi ha calendari del meu equip?",
         "Els equips de promoció (premini, mini, preinfantil) reben el calendari de la FCBQ més tard que la "
         "resta de categories. Es publicarà aquí en el moment que la federació el faci oficial."),
        ("Què faig si un partit ha canviat d'hora o de pista?",
         "Si la Federació Catalana de Basquetbol modifica un partit després que s'hagi fet la fitxa descarregable, "
         "la targeta de l'equip mostra un avís perquè comprovis les dades actualitzades a "
         "l'aplicació de partits del club, que es revisa cada dia."),
        ("Amb quina freqüència s'actualitzen els calendaris?",
         "El calendari en directe de /partits/ es sincronitza cada dia amb el calendari oficial de la FCBQ. "
         "Les fitxes descarregables són fixes: si un partit concret canvia, l'app sempre té la dada correcta."),
    ])

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#calendaris", "name": title, "description": desc, "url": url,
         "inLanguage": "ca-ES", "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#club"}},
        faq_ld,
        BREADCRUMB([("CB Grup Barna", "/"), ("Partits i resultats", "/partits/"), ("Calendaris per equip", "/partits/calendaris/")]),
    ]}

    body = f"""
{crumbs([("Inici", "/"), ("Partits i resultats", "/partits/"), ("Calendaris per equip", None)])}
<div class="wrap">
  <div class="phead narrow">
    <p class="eyebrow red" id="cal-temporada">Temporada</p>
    <h1>Calendaris per equip</h1>
    <p class="lede">El calendari complet de cada equip, llest per descarregar i desar. Es genera cada dia a
    partir del calendari oficial de la FCBQ: els equips de promoció (premini, mini, preinfantil) hi apareixen
    sols en el moment que la federació en publiqui el calendari.</p>
  </div>

  <div id="cal-groups"></div>
  <p id="cal-loading" class="narrow lede">Carregant els calendaris…</p>
  <p id="cal-error" class="narrow lede" style="display:none">No s'han pogut carregar els calendaris ara mateix.
    Torna-ho a provar més tard o consulta'ls directament a <a href="/partits/">l'app de partits</a>.</p>

  <div class="narrow">
    <h2 style="font-family:var(--display);font-size:clamp(16px,2.1vw,22px);margin:0 0 18px">Preguntes freqüents</h2>
    {faq_html}
    <div style="margin-top:clamp(34px,5vw,60px)">
    {closer("Vols el calendari en directe?",
            "L'aplicació de partits es sincronitza cada dia amb la FCBQ: resultats, ratxes i classificacions.",
            [("Veure l'app de partits", "/partits/", "red", "cal-closer-app"),
             ("Demanar informació", "/#info", "ghost", "cal-closer-info")])}
    </div>
  </div>
</div>

<script>
(function () {{
  var CATEGORIES = {json.dumps(CATEGORY_PREFIXES, ensure_ascii=False)};
  var t = Math.floor(Date.now() / 3600000);

  function esc(s) {{
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {{
      return {{ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }}[c];
    }});
  }}

  function categoria(nom) {{
    for (var i = 0; i < CATEGORIES.length; i++) {{
      if (nom.indexOf(CATEGORIES[i]) === 0) return CATEGORIES[i] === 'Sènior' ? 'Sènior' : CATEGORIES[i];
    }}
    return 'Altres';
  }}

  function card(equipId, nom, info) {{
    var fitxer = '/partits/calendaris/descarrega/' + equipId + '.' + info.tipus;
    var etiqueta = info.tipus === 'pdf'
      ? "Descarrega el PDF · " + info.pagines + " pàgines"
      : 'Desa la imatge';
    return '<div class="cal-card" data-equip="' + equipId + '">'
      + '<a href="' + fitxer + '" target="_blank" rel="noopener" data-cta="cal-img-' + equipId + '">'
      + '<img src="/partits/calendaris/img/' + equipId + '.webp?v=' + t + '" alt="Calendari de ' + esc(nom)
      + '" loading="lazy" decoding="async"></a>'
      + '<div class="cal-card-body">'
      + '<span class="cal-card-tag">CB Grup Barna</span><h3>' + esc(nom) + '</h3>'
      + '<span class="cal-card-meta">' + info.jornades + ' jornades</span>'
      + '<div class="cal-notice" data-notice="' + equipId + '">⚠ La FCBQ ha canviat l\\'hora o la pista d\\'algun '
      + 'partit d\\'aquest equip després de fer aquesta fitxa. <a href="/partits/#equips">Comprova-ho a l\\'app</a>.</div>'
      + '<a href="' + fitxer + '" target="_blank" rel="noopener" class="btn ghost" data-cta="cal-dl-' + equipId
      + '">' + etiqueta + '</a></div></div>';
  }}

  Promise.all([
    fetch('/partits/data.json?t=' + t).then(function (r) {{ return r.ok ? r.json() : null; }}),
    fetch('/partits/calendaris/manifest.json?t=' + t).then(function (r) {{ return r.ok ? r.json() : {{}}; }}),
  ]).then(function (res) {{
    var d = res[0], manifest = res[1] || {{}};
    document.getElementById('cal-loading').style.display = 'none';
    if (!d) {{ document.getElementById('cal-error').style.display = 'block'; return; }}

    var seasonEl = document.getElementById('cal-temporada');
    if (seasonEl && d.temporada) seasonEl.textContent = 'Temporada ' + d.temporada.replace('-', ' · ');

    var equips = d.equips || [];
    var groups = {{}};
    equips.forEach(function (e) {{
      if (!manifest[e.id]) return;
      var cat = categoria(e.nom);
      (groups[cat] = groups[cat] || []).push(e);
    }});

    var order = CATEGORIES.concat(['Altres']);
    var html = '';
    order.forEach(function (cat) {{
      var list = groups[cat];
      if (!list || !list.length) return;
      var cards = list.map(function (e) {{ return card(e.id, e.nom, manifest[e.id]); }}).join('');
      html += '<div class="cal-group"><h2>' + esc(cat) + '</h2><div class="cal-grid">' + cards + '</div></div>';
    }});
    document.getElementById('cal-groups').innerHTML = html || '<p class="narrow lede">Encara no hi ha cap '
      + 'calendari publicat. Torna-hi properament.</p>';

    var avui = new Date().toISOString().slice(0, 10);
    var canvis = {{}};
    (d.partits || []).forEach(function (p) {{
      if (p.avis && p.avis.expira >= avui) canvis[p.equipId] = true;
    }});
    Object.keys(canvis).forEach(function (equipId) {{
      var el = document.querySelector('.cal-notice[data-notice="' + equipId + '"]');
      if (el) el.classList.add('on');
    }});
  }}).catch(function () {{
    document.getElementById('cal-loading').style.display = 'none';
    document.getElementById('cal-error').style.display = 'block';
  }});
}})();
</script>
"""
    return write("partits/calendaris/index.html",
                 head(title, desc, url, SITE + "/partits/calendaris/img/scf.webp", ld,
                      "calendari CB Grup Barna, calendari bàsquet base, descarregar calendari equip") + body + FOOT)


if __name__ == "__main__":
    print("Generant pàgines:")
    print(build_campus())
    print(build_patrocinadors())
    print(build_3x3())
    print(build_blog_index())
    for a in ARTICLES:
        print(build_article(a))
    print(build_premsa_index())
    for a in PRESS:
        print(build_press_article(a))
    print(build_calendaris())
    print(f"\n{len(ARTICLES) + len(PRESS) + 5} pàgines generades.")
