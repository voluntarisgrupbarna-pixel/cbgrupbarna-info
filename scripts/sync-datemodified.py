#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fa que el "dateModified" del JSON-LD de cada pagina digui la data real del
darrer commit que la va tocar -- la mateixa font que ja fa servir
build-sitemap.py per al <lastmod>. Abans d'aquest script hi havia 169
pagines sense el camp i 132 amb una data que no coincidia amb el sitemap
(sobretot versions /en/, allunyades del "2026-08-25" que porta el sitemap a
gairebe tot arreu perque es va tocar en bloc sense repassar cada pagina).

Nomes toca el node WebPage / BlogPosting / Article / CollectionPage del
PRIMER bloc <script type="application/ld+json"> que en tingui un -- mai el
FAQPage ni cap bloc de Person, que son coses diferents. Quan el camp ja hi
es, nomes se li canvia el valor (substitucio de text, sense retocar la
resta del bloc). Quan no hi es, s'insereix parsejant nomes AQUELL bloc com a
JSON i tornant-lo a escriure amb el mateix indent=2 que ja fan servir tots
els generadors del lloc -- la resta de la pagina no es toca.

  python3 scripts/sync-datemodified.py --dry-run   # mostra que faria
  python3 scripts/sync-datemodified.py             # ho fa
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXCLOU = re.compile(
    r"(^|/)(admin\.html|token\.html|app\.html|estadistiques\.html|404\.html)$"
    r"|/admin/|/print/|/cartell\.html$|migrar-flickr"
)

TIPUS_PAGINA = {"WebPage", "BlogPosting", "Article", "CollectionPage"}

RE_SCRIPT = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>', re.S
)


def data_git(fitxer):
    try:
        sortida = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(fitxer)],
            cwd=ROOT, capture_output=True, text=True, timeout=20,
        ).stdout.strip()
        if sortida:
            return sortida
    except Exception:
        pass
    return None


def troba_node(dades):
    """Torna el node de tipus pagina dins d'un bloc JSON-LD, si n'hi ha."""
    candidats = dades.get("@graph") if isinstance(dades, dict) and "@graph" in dades else [dades]
    if not isinstance(candidats, list):
        return None
    for node in candidats:
        if not isinstance(node, dict):
            continue
        tipus = node.get("@type")
        tipus = tipus if isinstance(tipus, list) else [tipus]
        if TIPUS_PAGINA.intersection(tipus):
            return node
    return None


def processa(fitxer, dry):
    text = fitxer.read_text(encoding="utf-8", errors="ignore")
    blocs = list(RE_SCRIPT.finditer(text))
    if not blocs:
        return None

    for m in blocs:
        cru = m.group(1)
        try:
            dades = json.loads(cru)
        except Exception:
            continue
        node = troba_node(dades)
        if node is None:
            continue

        data_real = data_git(fitxer)
        if not data_real:
            return None

        actual = node.get("dateModified")
        if actual == data_real:
            return "al-dia"

        if actual is not None:
            # Ja hi es: nomes canvia el valor, com a substitucio de text
            # dins d'AQUEST bloc, sense retocar-ne la resta.
            patro_valor = re.compile(
                r'("dateModified"\s*:\s*")' + re.escape(actual) + r'(")'
            )
            nou_bloc, n = patro_valor.subn(r"\g<1>" + data_real + r"\g<2>", cru, count=1)
            if n != 1:
                return "no-tocat (no s'ha trobat el valor exacte)"
        else:
            # No hi es: insereix-lo just despres de "description" (o
            # "name", o "url") i torna a escriure NOMES aquest node.
            keys = list(node.keys())
            pos = None
            for clau in ("description", "name", "url"):
                if clau in keys:
                    pos = keys.index(clau) + 1
                    break
            if pos is None:
                pos = 1
            nou_node = {}
            for i, k in enumerate(keys):
                nou_node[k] = node[k]
                if i + 1 == pos:
                    nou_node["dateModified"] = data_real
            if "dateModified" not in nou_node:
                nou_node["dateModified"] = data_real
            node.clear()
            node.update(nou_node)
            nou_bloc = json.dumps(dades, ensure_ascii=False, indent=2)

        if not dry:
            nou_text = text[: m.start(1)] + nou_bloc + text[m.end(1):]
            fitxer.write_text(nou_text, encoding="utf-8")
        return f"{'(prova) ' if dry else ''}dateModified {actual!r} -> {data_real!r}"

    return None


def main():
    dry = "--dry-run" in sys.argv
    tocades, al_dia, sense_node, problemes = 0, 0, 0, []
    for fitxer in sorted(ROOT.rglob("*.html")):
        rel = "/" + fitxer.relative_to(ROOT).as_posix()
        if ".git" in fitxer.parts or EXCLOU.search(rel):
            continue
        resultat = processa(fitxer, dry)
        if resultat is None:
            sense_node += 1
        elif resultat == "al-dia":
            al_dia += 1
        elif resultat.startswith("no-tocat"):
            problemes.append((rel, resultat))
        else:
            tocades += 1
            if len(sys.argv) > 2 or "--verbose" in sys.argv:
                print(rel, resultat)

    print(f"\n{tocades} pagines actualitzades · {al_dia} ja estaven al dia · "
          f"{sense_node} sense node de pagina")
    if problemes:
        print(f"\n{len(problemes)} amb un problema (revisar a ma):")
        for rel, motiu in problemes:
            print(" ", rel, "—", motiu)


if __name__ == "__main__":
    main()
