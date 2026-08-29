#!/usr/bin/env python3
"""Genera /avantatges-familia/ (i /es/ventajas-familia/, /en/family-benefits/):
la pàgina que empaqueta els avantatges reals que els partners ofereixen a les
famílies del club.

Cada una de les 22 fitxes de partner (`patrocinadors/partners/<slug>/`) porta
des de fa temps una secció «Oferta per a la família del Barna» amb un botó de
WhatsApp perquè la marca en proposi una. Aquesta pàgina no n'inventa cap: llegeix
aquella secció a les tres fitxes de cada partner (ca/es/en), descarta les que
encara diuen «no té cap avantatge publicat» (el text exacte és a PLACEHOLDER) i
publica només les que ja tenen un avantatge real escrit.

Avui (29/08/2026) cap partner en té cap de publicat: la pàgina surt amb la
graella de partners i la crida a oferir-ne un. El dia que una fitxa el tingui,
tornar a executar aquest script la hi treu.

    python3 scripts/build-avantatges-familia.py [--dry-run]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://cbgrupbarna.info"
DRY = "--dry-run" in sys.argv

# El text exacte del placeholder a cada idioma: si l'oferta d'una fitxa
# coincideix (parcialment) amb aquest text, no és una oferta real.
PLACEHOLDER = {
    "ca": "encara no té cap avantatge publicat",
    "es": "todavía no tiene ninguna oferta publicada",
    "en": "does not yet have any offer published",
}
# Nota: el text real de placeholder de cada fitxa és
# "<Nom> encara no té cap avantatge publicat per a la família del Barna."
# —singular «avantatge», no «oferta»— es normalitza igual amb la marca
# «encara no té» / «todavía no tiene» / «does not yet have».

OFERTA_H2 = {
    "ca": "Oferta per a la família del Barna",
    "es": "Oferta para la familia del Barna",
    "en": "Offer for Barna families",
}

LANGS = ("ca", "es", "en")
PREFIX = {"ca": "", "es": "/es", "en": "/en"}

TEXTOS = {
    "titol": {"ca": "Avantatges de la família Barna",
              "es": "Ventajas de la familia Barna",
              "en": "Barna family benefits"},
    "eyebrow": {"ca": "Empreses · Descomptes i avantatges",
                "es": "Empresas · Descuentos y ventajas",
                "en": "Companies · Discounts and perks"},
    "lede": {
        "ca": ("Els descomptes i avantatges que els partners del club ofereixen a les "
               "famílies del CB Grup Barna, en un sol lloc."),
        "es": ("Los descuentos y ventajas que los partners del club ofrecen a las "
               "familias del CB Grup Barna, en un solo sitio."),
        "en": ("The discounts and perks that the club's partners offer to CB Grup "
               "Barna families, in one place."),
    },
    "buit_titol": {"ca": "Encara no hi ha cap avantatge publicat",
                   "es": "Todavía no hay ninguna ventaja publicada",
                   "en": "No benefits published yet"},
    "buit_text": {
        "ca": ("Cada fitxa de partner porta una porta oberta perquè hi publiqui un "
               "descompte o un avantatge per a les famílies del club. Encara no n'hi "
               "ha cap de confirmat: quan un partner en publiqui un, apareix aquí "
               "automàticament."),
        "es": ("Cada ficha de partner lleva una puerta abierta para publicar un "
               "descuento o una ventaja para las familias del club. Todavía no hay "
               "ninguna confirmada: cuando un partner publique una, aparece aquí "
               "automáticamente."),
        "en": ("Every partner page carries an open door to publish a discount or "
               "perk for club families. None is confirmed yet: as soon as a partner "
               "publishes one, it appears here automatically."),
    },
    "partners_titol": {"ca": "Els partners del club",
                        "es": "Los partners del club",
                        "en": "The club's partners"},
    "partners_text": {
        "ca": "Les 22 empreses i entitats que col·laboren amb el CB Grup Barna aquesta temporada.",
        "es": "Las 22 empresas y entidades que colaboran con el CB Grup Barna esta temporada.",
        "en": "The 22 companies and organisations collaborating with CB Grup Barna this season.",
    },
    "cta_titol": {"ca": "Tens una empresa i vols oferir un avantatge?",
                  "es": "¿Tienes una empresa y quieres ofrecer una ventaja?",
                  "en": "Do you run a business and want to offer a perk?"},
    "cta_text": {
        "ca": ("Escriu al club per WhatsApp amb el nom de l'empresa i l'avantatge que "
               "hi vols oferir: el publiquem a la teva fitxa i a aquesta pàgina."),
        "es": ("Escribe al club por WhatsApp con el nombre de la empresa y la ventaja "
               "que quieres ofrecer: la publicamos en tu ficha y en esta página."),
        "en": ("Message the club on WhatsApp with your company's name and the perk "
               "you'd like to offer: we publish it on your page and on this one."),
    },
    "cta_wa": {"ca": "Escriure al club per WhatsApp",
               "es": "Escribir al club por WhatsApp",
               "en": "Message the club on WhatsApp"},
    "veure_fitxa": {"ca": "Veure fitxa", "es": "Ver ficha", "en": "View page"},
}

WA_OFERTA = ("https://api.whatsapp.com/send?phone=+34698425153&text=Hola%2C%20tinc%20una%20"
             "empresa%20i%20vull%20oferir%20un%20avantatge%20a%20la%20fam%C3%ADlia%20del%20"
             "CB%20Grup%20Barna.")


def carrega_partners():
    dades = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    return dades["patrocinadors"]["llistat"]


def extreu_oferta(slug, lang):
    """Torna el text de l'oferta d'una fitxa si és real, o None si és el
    placeholder o la fitxa no existeix en aquell idioma."""
    ruta = ROOT / PREFIX[lang].lstrip("/") / "patrocinadors" / "partners" / slug / "index.html"
    if not ruta.exists():
        return None
    html = ruta.read_text(encoding="utf-8")
    h2 = re.escape(OFERTA_H2[lang])
    m = re.search(h2 + r"</h2>\s*<p[^>]*>(.*?)</p>", html, re.S)
    if not m:
        return None
    text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    if PLACEHOLDER[lang] in text.lower() or "encara no té" in text.lower() or "todavía no tiene" in text.lower():
        return None
    return text


CRUMB_NAME = {"ca": "Avantatges de la família Barna", "es": "Ventajas de la familia Barna",
              "en": "Barna family benefits"}


def head(lang, canonical):
    alt = "".join(
        f'\n<link rel="alternate" hreflang="{c}" href="{SITE}{PREFIX[c]}{p}">'
        for c, p in (("ca", "/avantatges-familia/"), ("es", "/ventajas-familia/"),
                     ("en", "/family-benefits/"))
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/avantatges-familia/">'
    title = f"{TEXTOS['titol'][lang]} | CB Grup Barna"
    desc = TEXTOS["lede"][lang]
    locale = {"ca": "ca_ES", "es": "es_ES", "en": "en_US"}[lang]
    inici = {"ca": ("/", "Inici"), "es": ("/es/", "Inicio"), "en": ("/en/", "Home")}[lang]
    ld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "@id": canonical + "#page", "url": canonical,
             "name": TEXTOS["titol"][lang], "description": desc, "inLanguage": lang,
             "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#club"},
             "dateModified": "2026-08-29", "publisher": {"@id": SITE + "/#club"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": inici[1], "item": SITE + inici[0]},
                {"@type": "ListItem", "position": 2, "name": CRUMB_NAME[lang], "item": canonical},
            ]},
        ],
    }, ensure_ascii=False, indent=2)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#10100E">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">{alt}
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CB Grup Barna">
<meta property="og:locale" content="{locale}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@cbgrupbarna">
<link rel="icon" href="/logo.png">
<link rel="apple-touch-icon" href="/icon-192.png">
<link rel="manifest" href="/manifest.json">
<link rel="stylesheet" href="/css/fonts.css">
<link rel="stylesheet" href="/css/barna.css">
<script type="application/ld+json">
{ld}
</script>
<script src="/js/galetes.js" defer></script><script src="/js/xat-whatsapp.js" defer></script><script type="text/javascript">var Tawk_API=Tawk_API||{{}},Tawk_LoadStart=new Date();(function(){{var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];s1.async=true;s1.src='https://embed.tawk.to/6a9197107f2d2f343fa7fabd/1k14bc6i0';s1.charset='UTF-8';s1.setAttribute('crossorigin','*');s0.parentNode.insertBefore(s1,s0);}})();</script>
<link rel="stylesheet" href="/css/cerca.css">
<link rel="stylesheet" href="/css/a11y.css">
</head>
"""


NAV = {
    "ca": ('<nav class="head-nav" aria-label="Navegació principal">\n'
           '      <a href="/empreses/">Empreses</a>\n'
           '      <a href="/patrocinadors/">Partners</a>\n'
           '      <a href="/club/" class="opt">Club</a>\n'
           '      <a href="/#info">Informació</a>\n    </nav>'),
    "es": ('<nav class="head-nav" aria-label="Navegación principal">\n'
           '      <a href="/es/empresas/">Empresas</a>\n'
           '      <a href="/es/patrocinadors/">Partners</a>\n'
           '      <a href="/es/#info">Información</a>\n    </nav>'),
    "en": ('<nav class="head-nav" aria-label="Main navigation">\n'
           '      <a href="/en/companies/">Companies</a>\n'
           '      <a href="/en/patrocinadors/">Partners</a>\n'
           '      <a href="/en/#info">Information</a>\n    </nav>'),
}
BRAND = {
    "ca": ("/", "CB Grup Barna · inici", "Escut del CB Grup Barna"),
    "es": ("/es/", "CB Grup Barna · inicio", "Escudo del CB Grup Barna"),
    "en": ("/en/", "CB Grup Barna · home", "CB Grup Barna crest"),
}
SKIP = {"ca": "Saltar al contingut", "es": "Saltar al contenido", "en": "Skip to content"}
CRUMB_INICI = {"ca": ("/", "Inici"), "es": ("/es/", "Inicio"), "en": ("/en/", "Home")}
CRUMB_ARIA = {"ca": "Fil d'Ariadna", "es": "Migas de pan", "en": "Breadcrumb"}


def pagina(lang):
    ruta_relativa = {"ca": "/avantatges-familia/", "es": "/ventajas-familia/",
                     "en": "/family-benefits/"}[lang]
    canonical = SITE + ruta_relativa
    lang_links = "".join(
        f'<a href="{SITE}{PREFIX[c]}{p}" hreflang="{c}" lang="{c}" aria-label="{n}"'
        + (' class="active" aria-current="true"' if c == lang else '') + f'>{c.upper()}</a>'
        + ('<span class="sep" aria-hidden="true">·</span>' if i < 2 else '')
        for i, (c, p, n) in enumerate([
            ("ca", "/avantatges-familia/", "Català"),
            ("es", "/ventajas-familia/", "Castellano"),
            ("en", "/family-benefits/", "English"),
        ])
    )

    partners = carrega_partners()
    amb_oferta = []
    for p in partners:
        text = extreu_oferta(p["slug"], lang)
        if text:
            amb_oferta.append((p, text))

    if amb_oferta:
        cards = "".join(
            f'<div class="p-card"><img src="{p["logo"]}" alt="{p["nom"]}" loading="lazy" '
            f'decoding="async" width="120" height="68" style="object-fit:contain;'
            f'max-width:100%"><p>{text}</p><a class="cta" href="{PREFIX[lang]}{p["fitxa"]}" '
            f'data-cta="avantatges-fitxa">{TEXTOS["veure_fitxa"][lang]}</a></div>'
            for p, text in amb_oferta)
        bloc_avantatges = (f'<div class="p-grid">{cards}</div>')
    else:
        bloc_avantatges = (
            f'<div class="buit"><h2>{TEXTOS["buit_titol"][lang]}</h2>'
            f'<p>{TEXTOS["buit_text"][lang]}</p></div>')

    directori = "".join(
        f'<a class="dir-item" href="{PREFIX[lang]}{p["fitxa"]}">'
        f'<img src="{p["logo"]}" alt="{p["nom"]}" loading="lazy" decoding="async" '
        f'width="90" height="50" style="object-fit:contain;max-width:100%"></a>'
        for p in partners)

    body = f"""<body>
<a href="#main" class="skip">{SKIP[lang]}</a>
<header class="head">
  <div class="head-in">
    <a class="head-brand" href="{BRAND[lang][0]}" aria-label="{BRAND[lang][1]}">
      <img src="/logo.png" alt="{BRAND[lang][2]}" width="30" height="30">
      <span>CB Grup Barna</span>
    </a>
    {NAV[lang]}
    <nav class="lang-switch" aria-label="Canvia d'idioma · Cambiar idioma · Change language">
      {lang_links}
    </nav>
  </div>
</header>
<main id="main">
<div class="wrap"><nav class="crumb" aria-label="{CRUMB_ARIA[lang]}"><a href="{CRUMB_INICI[lang][0]}">{CRUMB_INICI[lang][1]}</a> · <span>{TEXTOS['titol'][lang]}</span></nav></div>
<div class="wrap">
  <div class="phead narrow">
    <p class="eyebrow red">{TEXTOS['eyebrow'][lang]}</p>
    <h1>{TEXTOS['titol'][lang]}</h1>
    <p class="lede">{TEXTOS['lede'][lang]}</p>
  </div>
</div>
<div class="wrap section">
  <div class="narrow">
    {bloc_avantatges}
  </div>
</div>
<div class="wrap section">
  <div class="narrow">
    <h2>{TEXTOS['partners_titol'][lang]}</h2>
    <p class="lede">{TEXTOS['partners_text'][lang]}</p>
    <div class="dir-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:14px;margin-top:24px">{directori}</div>
  </div>
</div>
<div class="wrap section">
  <div class="narrow closer">
    <h2>{TEXTOS['cta_titol'][lang]}</h2>
    <p>{TEXTOS['cta_text'][lang]}</p>
    <div class="btn-row"><a href="{WA_OFERTA}" class="btn red" target="_blank" rel="noopener" data-cta="avantatges-oferir-wa">{TEXTOS['cta_wa'][lang]}</a></div>
  </div>
</div>
"""
    return head(lang, canonical) + body + "<!--PEU-->"


STYLE = """<style>
.p-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 18px; margin-top: 22px; }
.p-card { border: 1px solid var(--line); padding: 18px; background: var(--paper); }
.p-card img { margin-bottom: 12px; }
.p-card p { font-size: 14px; color: var(--ink-2); line-height: 1.6; }
.p-card .cta { display: inline-block; margin-top: 10px; font-family: var(--display); font-size: 9px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--red); }
.buit { border: 1px dashed var(--line); padding: clamp(26px,4vw,40px); text-align: center; }
.buit h2 { margin-bottom: 10px; }
.buit p { color: var(--ink-2); max-width: 56ch; margin: 0 auto; }
.dir-item { display: flex; align-items: center; justify-content: center; border: 1px solid var(--line); padding: 10px; background: var(--paper); }
</style>
"""


def escriu(lang, contingut, peu_html):
    slug = {"ca": "avantatges-familia", "es": "ventajas-familia",
            "en": "family-benefits"}[lang]
    fitxer = ROOT / PREFIX[lang].lstrip("/") / slug / "index.html" if PREFIX[lang] \
        else ROOT / slug / "index.html"
    html = contingut.replace("</head>", STYLE + "</head>").replace("<!--PEU-->", peu_html)
    if DRY:
        print(f"  {fitxer.relative_to(ROOT)}  ({len(html)//1024} KB, dry-run)")
        return
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    fitxer.write_text(html, encoding="utf-8")
    print(f"  {fitxer.relative_to(ROOT)}  ({len(html)//1024} KB)")


def main():
    sys.path.insert(0, str(ROOT / "scripts"))
    from i18n_chrome import peu
    print("Generant /avantatges-familia/:")
    for lang in LANGS:
        escriu(lang, pagina(lang), peu(lang))


if __name__ == "__main__":
    main()
