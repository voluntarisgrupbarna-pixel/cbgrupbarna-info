#!/usr/bin/env python3
"""
Posa a les pàgines els noms canònics de i18n/etiquetes.yml.

    python3 scripts/i18n-aplica-etiquetes.py --dry-run   # què canviaria
    python3 scripts/i18n-aplica-etiquetes.py             # ho canvia

`scripts/i18n-lint.py` diu quins enllaços es diuen d'una manera que no toca;
aquest els arregla. Tots dos llegeixen el mateix fitxer, de manera que el
vocabulari s'escriu una vegada i des d'allà es comprova i s'aplica.

És deliberadament curt de mires: només toca el text que hi ha dins d'una
etiqueta <a> que apunti a una de les adreces del diccionari, i només si
aquest text és EXACTAMENT un dels sinònims que el diccionari dona per
prohibits. No endevina, no reescriu prosa i no toca cap adreça —les URL no
es tradueixen— ni cap <title>, on un terme de cerca hi és benvingut.

Dues formes d'enllaç, que al lloc conviuen:

    <a href="/es/partits/">Partidos y resultados</a>
    <a href="..."><span class="list-t">Partidos y resultados</span><span…

A la segona, el nom de la secció és el primer <span> i la resta és el
subtítol, que no es toca.
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ETIQUETES = ROOT / "i18n" / "etiquetes.yml"
SITE = "https://cbgrupbarna.info"

EXCLOU = re.compile(
    r"(^|/)(admin\.html|token\.html|app\.html|estadistiques\.html)$"
    r"|/admin/|/print/|/cartell\.html$|migrar-flickr"
)
RE_ENLLAC = re.compile(r'<a\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*>(.*?)</a>', re.I | re.S)
RE_LIST_T = re.compile(r'(<span class="list-t">)(.*?)(</span>)', re.I | re.S)


def idioma_de(ruta):
    return "es" if ruta.startswith("es/") else "en" if ruta.startswith("en/") else "ca"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    regles = (yaml.safe_load(ETIQUETES.read_text(encoding="utf-8")) or {}).get("enllacos", {})
    canvis, fitxers = [], 0

    for fitxer in sorted(ROOT.rglob("*.html")):
        rel = fitxer.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", "galeria/node_modules/", "tests/")) or EXCLOU.search(rel):
            continue
        idioma = idioma_de(rel)
        text = fitxer.read_text(encoding="utf-8", errors="ignore")
        original = text

        def arregla(m):
            desti, dins = m.group(1), m.group(2)
            clau = re.sub(r"^/(es|en)/", "/", desti.replace(SITE, "").split("#")[0].split("?")[0])
            regla = regles.get(clau)
            if not regla:
                return m.group(0)
            bo = (regla.get(idioma) or [None])[0]
            dolentes = (regla.get("prohibides") or {}).get(idioma, [])
            if not bo:
                return m.group(0)

            if dins.strip() in dolentes:
                canvis.append((rel, desti, dins.strip(), bo))
                return m.group(0).replace(f">{dins}</a>", f">{bo}</a>")

            def span(sm):
                if sm.group(2).strip() in dolentes:
                    canvis.append((rel, desti, sm.group(2).strip(), bo))
                    return sm.group(1) + bo + sm.group(3)
                return sm.group(0)

            nou = RE_LIST_T.sub(span, dins, count=1)
            return m.group(0).replace(dins, nou) if nou != dins else m.group(0)

        text = RE_ENLLAC.sub(arregla, text)
        if text != original:
            fitxers += 1
            if not args.dry_run:
                fitxer.write_text(text, encoding="utf-8")

    per_canvi = {}
    for rel, desti, vell, bo in canvis:
        per_canvi.setdefault((vell, bo), []).append(rel)
    for (vell, bo), llista in sorted(per_canvi.items(), key=lambda kv: -len(kv[1])):
        print(f"  «{vell}» → «{bo}»  ({len(llista)} pàgines)")
    print(f"\n{len(canvis)} enllaços en {fitxers} pàgines"
          + (" (no s'ha desat res)" if args.dry_run else " · desat"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
