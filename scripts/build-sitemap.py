#!/usr/bin/env python3
"""
Generador del sitemap.xml de cbgrupbarna.info.

Fins ara el sitemap es mantenia a mà, i per això anava quedant enrere: hi
havia pàgines publicades que no hi sortien (i per tant Google no les trobava
si ningú hi enllaçava) i dates de <lastmod> inventades que no corresponien a
cap canvi real. Aquest script el reconstrueix des del que hi ha al disc:

    python3 scripts/build-sitemap.py

Què inclou i què no:

  · Només pàgines indexables. Si una pàgina porta <meta name="robots"
    content="noindex">, queda fora — que és el cas de /patrocinis/,
    /presentacio/, /dossier-patrocinis/ i /basquet-femeni/.
  · Fora també els panells d'admin, les pàgines d'impressió i els cartells:
    les mateixes rutes que ja bloqueja robots.txt.
  · La <loc> surt del <link rel="canonical"> de cada pàgina quan n'hi ha, no
    de la ruta del fitxer. Així el sitemap i el canonical no es contradiuen
    mai, que és un dels motius pels quals Google descarta URLs.
  · El <lastmod> és la data de l'últim commit que va tocar el fitxer. Si el
    fitxer no és a git encara, s'agafa la data de modificació del disc.
  · Les versions en castellà i anglès s'enllacen amb <xhtml:link hreflang>,
    llegint els <link rel="alternate"> de la pàgina. Google entén així que
    /blog/, /es/blog/ i /en/blog/ són la mateixa pàgina en tres idiomes i no
    les tracta com a contingut duplicat.
"""
import html
import re
import subprocess
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://cbgrupbarna.info"

# Les mateixes rutes que robots.txt manté fora de l'índex.
EXCLOU = re.compile(
    r"(^|/)(admin\.html|token\.html|app\.html|estadistiques\.html|404\.html)$"
    r"|/admin/|/print/|/cartell\.html$|migrar-flickr"
)

RE_NOINDEX = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)
RE_CANONICAL = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', re.I)
RE_ALTERNATE = re.compile(
    r'<link[^>]+rel=["\']alternate["\'][^>]*hreflang=["\']([^"\']+)["\'][^>]*href=["\']([^"\']+)["\']',
    re.I,
)

# Amb quina freqüència canvia de veritat cada zona, i quin pes té per al club.
PRIORITATS = [
    (re.compile(r"^/$"),                              "daily",   "1.0"),
    (re.compile(r"^/partits/"),                       "daily",   "0.8"),
    (re.compile(r"^/(es|en)/partits/"),               "daily",   "0.6"),
    (re.compile(r"^/(campus|escoleta|3x3)/"),         "monthly", "0.9"),
    (re.compile(r"^/blog/"),                          "monthly", "0.8"),
    (re.compile(r"^/(es|en)/blog/"),                  "monthly", "0.6"),
    (re.compile(r"^/patrocinadors/"),                 "monthly", "0.7"),
    (re.compile(r"^/(es|en)/"),                       "monthly", "0.5"),
]


def data_git(fitxer):
    """Data de l'últim commit que va tocar el fitxer (YYYY-MM-DD)."""
    try:
        sortida = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(fitxer)],
            cwd=ROOT, capture_output=True, text=True, timeout=20,
        ).stdout.strip()
        if sortida:
            return sortida
    except Exception:
        pass
    return datetime.fromtimestamp(fitxer.stat().st_mtime).strftime("%Y-%m-%d")


def url_de(fitxer):
    """Ruta del fitxer → URL pública, amb barra final i sense index.html."""
    rel = fitxer.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return SITE + "/"
    if rel.endswith("/index.html"):
        return SITE + "/" + rel[: -len("index.html")]
    return SITE + "/" + rel


def pes(cami):
    for patro, freq, prio in PRIORITATS:
        if patro.search(cami):
            return freq, prio
    return "monthly", "0.6"


def recollir():
    pagines = {}
    for fitxer in sorted(ROOT.rglob("*.html")):
        rel = "/" + fitxer.relative_to(ROOT).as_posix()
        if ".git" in fitxer.parts or EXCLOU.search(rel):
            continue
        text = fitxer.read_text(encoding="utf-8", errors="ignore")
        if RE_NOINDEX.search(text):
            continue

        canonic = RE_CANONICAL.search(text)
        loc = html.unescape(canonic.group(1)).strip() if canonic else url_de(fitxer)
        if not loc.startswith(SITE):
            continue                      # canonical cap a fora: no és pàgina nostra
        if loc in pagines:
            continue                      # dues rutes amb el mateix canonical

        alternates = [
            (idioma, html.unescape(href))
            for idioma, href in RE_ALTERNATE.findall(text)
            if html.unescape(href).startswith(SITE)
        ]
        cami = loc[len(SITE):] or "/"
        freq, prio = pes(cami)
        pagines[loc] = {
            "lastmod": data_git(fitxer),
            "changefreq": freq,
            "priority": prio,
            "alternates": alternates,
        }
    return pagines


def escriure(pagines):
    linies = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!-- Generat per scripts/build-sitemap.py · no editar a mà -->',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    # Primer les de més pes, que és l'ordre en què volem que les llegeixi.
    for loc in sorted(pagines, key=lambda u: (-float(pagines[u]["priority"]), u)):
        d = pagines[loc]
        linies.append("  <url>")
        linies.append(f"    <loc>{html.escape(loc)}</loc>")
        linies.append(f"    <lastmod>{d['lastmod']}</lastmod>")
        linies.append(f"    <changefreq>{d['changefreq']}</changefreq>")
        linies.append(f"    <priority>{d['priority']}</priority>")
        for idioma, href in d["alternates"]:
            linies.append(
                f'    <xhtml:link rel="alternate" hreflang="{html.escape(idioma)}" '
                f'href="{html.escape(href)}"/>'
            )
        linies.append("  </url>")
    linies.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(linies) + "\n", encoding="utf-8")
    return len(pagines)


if __name__ == "__main__":
    total = escriure(recollir())
    print(f"sitemap.xml · {total} URLs · {date.today()}")
