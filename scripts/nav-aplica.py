#!/usr/bin/env python3
"""El menu de la capcalera, igual a totes les pagines, des de la font unica.

El 30/08 es va reorganitzar el menu (Equips · Club · Calendari · Escoleta ·
Campus · Empreses) pero nomes va arribar a una part del lloc: un centenar de
pagines conservaven l'antic de deu entrades (Magics, 3x3, Cistella Petita...)
escrit a ma dins del seu HTML, i amb deu entrades el nom del club i el menu
se solapaven.

Aquest script reescriu el bloc <nav class="head-nav"> de CADA pagina amb el
que diu scripts/i18n_chrome.py (que ho llegeix d'i18n/diccionari.yml,
estructura -> nav). A partir d'ara el menu es canvia ALLA i es passa aixo:
cap pagina no el porta escrit a ma.

Conserva l'aria-current="page" de la pagina on toca: si una de les entrades
del menu es la pagina mateixa, es marca.

Exclusions: admin, l'app de galeria, el mirall del Premi, les presentacions
(capçalera propia), les peces d'impressio i el 404 (es reescriu sol).

Idempotent. Us: python3 scripts/nav-aplica.py [--dry-run]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ARREL / "scripts"))
import i18n_chrome as chrome  # noqa: E402

EXCLOU = ("admin/", "/admin.html", "galeria/", "premidonaesport/",
          "presentacions/", "presentacio/", "presentaciones/", "presentacion/",
          "presentations/", "presentation/", "opina/print/", "flyer/",
          "404.html", "app.html", "cartell.html")

RE_NAV = re.compile(r'[ \t]*<nav class="head-nav".*?</nav>', re.S)


def ruta_publica(f: Path) -> str:
    rel = "/" + f.relative_to(ARREL).as_posix()
    return rel[:-len("index.html")] if rel.endswith("/index.html") else rel


def aplica(f: Path, sec: bool) -> bool:
    html = f.read_text(encoding="utf-8")
    if '<nav class="head-nav"' not in html:
        return False
    m = re.search(r'<html[^>]*\blang="([a-z]{2})', html)
    idioma = m.group(1) if m and m.group(1) in ("ca", "es", "en") else "ca"

    nou = chrome.navegacio(idioma)
    # La pagina mateixa, marcada com a actual.
    meva = ruta_publica(f)
    nou = nou.replace(f'href="{meva}">', f'href="{meva}" aria-current="page">')

    nou_html, canvis = RE_NAV.subn(nou, html, count=1)
    if canvis and nou_html != html:
        if not sec:
            f.write_text(nou_html, encoding="utf-8")
        return True
    return False


def main() -> int:
    sec = "--dry-run" in sys.argv
    tocats = 0
    per_idioma = {}
    for f in sorted(ARREL.rglob("*.html")):
        rel = f.relative_to(ARREL).as_posix()
        if any(x in rel for x in EXCLOU) or rel.startswith(".git"):
            continue
        if aplica(f, sec):
            tocats += 1
    print(f"{tocats} capçaleres {'que es tocarien' if sec else 'reescrites'} des de la font única")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
