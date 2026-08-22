# -*- coding: utf-8 -*-
"""Genera l'edicio de vacances escolars del campus que no te pagina propia
fora d'aquest generador: /campus/setmana-santa/. El Nadal viu a
/campus-nadal-basquet-barcelona/, fora d'aquest script. Es un producte
diferent de l'estiu —dura menys dies, te un altre preu i un altre public—, i
per aixo te pagina propia. Tot el que no tenim confirmat es diu que
s'anuncia, no s'inventa."""
import json, os
HDR = open('/tmp/claude-0/c_hdr.txt', encoding='utf-8').read()
FTR = open('/tmp/claude-0/c_ftr.txt', encoding='utf-8').read()
SITE = "https://cbgrupbarna.info"
WA = ("https://api.whatsapp.com/send?phone=+34698425153&amp;text=Hola!%20Vull%20informaci%C3%B3%20"
      "del%20campus%20de%20{q}%20del%20CB%20Grup%20Barna")
CATS = ("Escoleta, Premini, Mini, Preinfantil, Infantil, Cadet i Júnior")

SEASONS = [
 dict(slug="setmana-santa", q="Setmana%20Santa", nom="Campus de Setmana Santa",
   title="Campus de Setmana Santa de bàsquet a Barcelona | CB Grup Barna",
   h1="Campus de Setmana Santa de bàsquet a Barcelona",
   kw="campus Setmana Santa bàsquet Barcelona, campus Semana Santa baloncesto Barcelona, casal Setmana Santa Clot, tecnificació Setmana Santa",
   quan="Durant les vacances escolars de Setmana Santa, entre finals de març i mitjans d'abril.",
   dies="Una setmana, ajustada als dies festius.",
   preu="150",
   lede=("Setmana de tecnificació de bàsquet a La Nau del Clot durant les vacances de Setmana "
         "Santa. El <strong>Flow Camp</strong>, el mòdul de fluïdesa ofensiva i joc en moviment, "
         "és el que el club hi ha portat les darreres edicions."),
   perque=("Setmana Santa cau amb la temporada encarada al tram final, quan cada equip ja sap "
           "on es juga alguna cosa. És l'última finestra de l'any per guanyar centímetres tècnics "
           "abans dels partits que decideixen, i la porta d'entrada natural per a qui es planteja "
           "el campus d'estiu i vol provar-ho abans."),
   focus=[("Flow Camp","Fluïdesa ofensiva i joc en moviment: llegir l'espai sense aturar la pilota."),
          ("Maneig de pilota","Control sota pressió, que és on es trenca el joc a la primavera."),
          ("Finalitzacions","Resoldre a prop de cistella amb contacte.")]),
]

for S in SEASONS:
    url = f"{SITE}/campus/{S['slug']}/"
    preu_txt = (f"{S['preu']} € la setmana." if S['preu']
                else "El preu de cada edició s'anuncia en obrir inscripcions.")
    desc = (f"{S['nom']} de bàsquet del CB Grup Barna a La Nau del Clot, Barcelona. "
            f"Tecnificació en vacances escolars per a {CATS}. "
            + (f"{S['preu']} € la setmana. " if S['preu'] else "")
            + "Obert a jugadors i jugadores de qualsevol club.")
    course = {"@type":"Course","@id":url+"#course","name":f"{S['nom']} de bàsquet · CB Grup Barna",
      "description":desc,"url":url,"provider":{"@id":SITE+"/#club"},"inLanguage":["ca","es"],
      "teaches":[f[0] for f in S['focus']],
      "audience":{"@type":"PeopleAudience","suggestedMinAge":5,"suggestedMaxAge":17},
      "coursePrerequisites":"Cap. Obert a jugadors i jugadores de qualsevol club.",
      "location":{"@type":"Place","name":"La Nau del Clot","address":{"@type":"PostalAddress",
        "streetAddress":"Carrer de la Llacuna, 170-172","addressLocality":"Barcelona",
        "addressRegion":"Barcelona","postalCode":"08018","addressCountry":"ES"}},
      "hasCourseInstance":{"@type":"CourseInstance","courseMode":"onsite",
        "name":f"{S['nom']} · CB Grup Barna",
        "location":{"@type":"Place","name":"La Nau del Clot","address":{"@type":"PostalAddress",
          "streetAddress":"Carrer de la Llacuna, 170-172","addressLocality":"Barcelona",
          "postalCode":"08018","addressCountry":"ES"}}}}
    if S['preu']:
        course["offers"]={"@type":"Offer","price":S['preu'],"priceCurrency":"EUR",
          "description":"Preu per setmana.","availability":"https://schema.org/LimitedAvailability","url":url}
    faqs=[(f"Quan es fa el {S['nom'].lower()} del CB Grup Barna?", S['quan']+" "+S['dies']+
             " Les dates exactes de cada edició s'anuncien en aquesta pàgina i a @cbgrupbarna."),
          (f"Quant costa el {S['nom'].lower()}?", preu_txt+" Els jugadors i jugadores del club tenen prioritat d'inscripció."),
          (f"Cal jugar al CB Grup Barna per apuntar-s'hi?",
             "No. És obert a jugadors i jugadores de qualsevol club de Barcelona i de la província. "
             "Els del club tenen prioritat quan s'obren les places."),
          ("Per a quines edats és?", f"Set categories: {CATS}. Els grups es fan per categoria i nivell."),
          ("On es fa?", "A La Nau del Clot, Carrer de la Llacuna 170-172, 08018 Barcelona. "
             "Metro L1 Glòries i L2 Clot, i Rodalies Clot-Aragó.")]
    ld={"@context":"https://schema.org","@graph":[course,
      {"@type":"WebPage","@id":url+"#webpage","url":url,"name":S['title'],"description":desc,
       "inLanguage":"ca","about":{"@id":url+"#course"},"isPartOf":{"@id":SITE+"/#website"},
       "dateModified":"2026-08-20","publisher":{"@id":SITE+"/#club"}},
      {"@type":"FAQPage","@id":url+"#faq","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]},
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Inici","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"Campus de bàsquet","item":SITE+"/campus/"},
        {"@type":"ListItem","position":3,"name":S['nom'],"item":url}]}]}

    focus_html="\n".join(
      f'    <div class="card"><div class="card-body"><span class="card-tag">{i:02d}</span>'
      f'<h3>{n}</h3><p>{d}</p></div></div>' for i,(n,d) in enumerate(S['focus'],1))
    faq_html="\n".join(f'    <details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)
    preu_row=(f'<div class="dl-row"><dt>Preu</dt><dd>{S["preu"]} € la setmana. '
              f'Els jugadors i jugadores del club tenen prioritat d\'inscripció.</dd></div>'
              if S['preu'] else
              '<div class="dl-row"><dt>Preu</dt><dd>S\'anuncia en obrir les inscripcions de cada edició.</dd></div>')

    html = f'''<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0A0A0A">
<title>{S['title']}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{S['kw']}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CB Grup Barna">
<meta property="og:locale" content="ca_ES">
<meta property="og:title" content="{S['title']}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/campus-hero.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@cbgrupbarna">
<link rel="icon" href="/logo.png">
<link rel="apple-touch-icon" href="/icon-192.png">
<link rel="manifest" href="/manifest.json">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/barna.css">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
</head>
<body>
<a href="#main" class="skip">Saltar al contingut</a>
{HDR}
<main id="main">
<div class="wrap"><nav class="crumb" aria-label="Fil d'Ariadna"><a href="/">Inici</a> · <a href="/campus/">Campus de bàsquet</a> · <span>{S['nom']}</span></nav></div>
<div class="wrap">
  <div class="phead narrow">
    <p class="eyebrow red">{S['nom']} · El Clot · Barcelona</p>
    <h1>{S['h1']}</h1>
    <p class="lede">{S['lede']}</p>
    <div class="btn-row" style="margin-top:28px">
      <a href="{WA.format(q=S['q'])}" class="btn red" target="_blank" rel="noopener" data-cta="{S['slug']}-wa">Demanar informació</a>
      <a href="/campus/" class="btn ghost" data-cta="{S['slug']}-campus">El campus d'estiu &rarr;</a>
    </div>
  </div>

  <div class="narrow prose">
    <h2>Per què aturar-se a {S['q'].replace('%20',' ')}</h2>
    <p>{S['perque']}</p>
  </div>

  <div class="narrow prose">
    <h2>Fitxa</h2>
  </div>
  <div class="dl narrow">
    <div class="dl-row"><dt>Què és</dt><dd>Setmana de tecnificació de bàsquet en vacances escolars. Mateixa metodologia que el campus d'estiu, en format curt.</dd></div>
    <div class="dl-row"><dt>Qui l'organitza</dt><dd>CB Grup Barna, amb la metodologia de Time Chamber.</dd></div>
    <div class="dl-row"><dt>On</dt><dd>La Nau del Clot · Carrer de la Llacuna, 170-172 · 08018 Barcelona.</dd></div>
    <div class="dl-row"><dt>Com arribar-hi</dt><dd>Metro L1 Glòries i L2 Clot · Rodalies Clot-Aragó · a peu des de Westfield Glòries.</dd></div>
    <div class="dl-row"><dt>Quan</dt><dd>{S['quan']} {S['dies']}</dd></div>
    <div class="dl-row"><dt>Per a qui</dt><dd>Set categories: {CATS}. Nens i nenes, per categoria i nivell.</dd></div>
    <div class="dl-row"><dt>Cal ser del Barna?</dt><dd>No. Obert a qualsevol club de Barcelona i de la província; els del club tenen prioritat d'inscripció.</dd></div>
    {preu_row}
    <div class="dl-row"><dt>Idioma</dt><dd>Català i castellà.</dd></div>
    <div class="dl-row"><dt>Com inscriure-s'hi</dt><dd>Per WhatsApp al <a href="https://wa.me/34698425153">+34 698 425 153</a>. Places limitades per mantenir la ràtio de treball.</dd></div>
  </div>

  <div class="narrow prose">
    <h2>Què s'hi treballa</h2>
  </div>
  <div class="cards">
{focus_html}
  </div>

  <div class="narrow prose">
    <h2>Preguntes freqüents</h2>
  </div>
  <div class="faq narrow">
{faq_html}
  </div>

  <div class="closer">
    <h2>Avisa'm de la propera edició</h2>
    <p>Les darreres edicions s'han omplert abans de començar. El club escriu a qui és a la llista
    quan s'obren les places, un dia abans de publicar-ho.</p>
    <div class="btn-row">
      <a href="{WA.format(q=S['q'])}" class="btn red" target="_blank" rel="noopener" data-cta="{S['slug']}-closer-wa">Escriure pel WhatsApp</a>
      <a href="/#info" class="btn ghost" data-cta="{S['slug']}-form">Deixar el contacte</a>
    </div>
  </div>

  <div class="narrow prose">
    <h2>La resta del campus</h2>
    <ul>
      <li><a href="/campus/">Campus de bàsquet a Barcelona</a> — l'edició d'estiu, sis setmanes amb focus propi, i tota la fitxa de dades.</li>
      <li><a href="/campus-nadal-basquet-barcelona/">Campus de Nadal</a> — l'altra setmana de vacances escolars.</li>
      <li><a href="/tecnificacio-basquet-barcelona/">Tecnificació de bàsquet a Barcelona</a> — què vol dir tecnificar i com ho treballa el club.</li>
      <li><a href="/blog/campus-basquet-barcelona-guia/">Com triar un campus de bàsquet a Barcelona</a> — la guia per a famílies.</li>
      <li><a href="/escoleta/">Escoleta</a> — per als de 4 a 8 anys, tot l'any.</li>
    </ul>
  </div>
</div>
</main>
{FTR}
<script src="/js/galetes.js"></script>
</body>
</html>
'''
    os.makedirs(f"campus/{S['slug']}", exist_ok=True)
    open(f"campus/{S['slug']}/index.html", 'w', encoding='utf-8').write(html)
    print('creat campus/'+S['slug']+'/index.html', len(html), 'bytes')
