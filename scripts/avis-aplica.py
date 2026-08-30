#!/usr/bin/env python3
"""Posa l'avís de campanya (js/avis-portes-obertes.js) a totes les pàgines.

Mateixa mecànica i mateixes exclusions que scripts/mapa-aplica.py, del qual
és germà: afegeix una sola línia abans de </body> i es pot tornar a passar
sempre sense duplicar res.

    <script src="/js/avis-portes-obertes.js" defer></script>

Què salta, i per què:
  · admin i eines internes — no són cara pública
  · peces per imprimir (opina/print, escoleta/flyer, partits/cartell) —
    generen una imatge, i una barra vermella a sobre l'espatllaria
  · redireccions amb <meta http-equiv="refresh"> — no es veuen
  · galeria/ (app Next.js) — té la seva pròpia capçalera compilada
  · premidonaesport/ — mirall d'una web externa amb navegació pròpia

El propi script ja decideix si es pinta o no (caduca sol el 27/09/2026, no
surt a /portes-obertes/ i recorda si l'has tancat), així que aquí només cal
posar-lo a tot arreu i oblidar-se'n.

QUAN ACABI LA CAMPANYA no cal desfer res: el script deixa de pintar-se sol
el 28 de setembre. Per a la campanya següent, es canvien les dates i la
clau de dins de js/avis-portes-obertes.js i es torna a passar aquest script
per a les pàgines noves.

Ús:
    python3 scripts/avis-aplica.py --dry-run
    python3 scripts/avis-aplica.py
"""

import argparse
import re
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent

EXCLOU_DIRS = {".git", "node_modules", "galeria", "tests"}
EXCLOU_PATRONS = (
    "/admin/",
    "/admin.html",
    "admin-",
    "/opina/print/",
    "/escoleta/flyer/",
    "/premidonaesport/",
    "cartell.html",
    "migrar-flickr",
)

MARCA = '<script src="/js/avis-portes-obertes.js" defer></script>'
REDIRECCIO = re.compile(r'http-equiv=["\']refresh["\']', re.I)


def cal_saltar(cami: Path, text: str) -> str | None:
    rel = "/" + str(cami.relative_to(ARREL))
    if any(p in rel for p in EXCLOU_PATRONS):
        return "exclosa"
    if REDIRECCIO.search(text[:2000]):
        return "redirecció"
    if "</body>" not in text:
        return "sense </body>"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    fets = saltats = ja = 0
    for cami in sorted(ARREL.rglob("*.html")):
        parts = cami.relative_to(ARREL).parts
        if any(p in EXCLOU_DIRS for p in parts):
            continue
        text = cami.read_text(encoding="utf-8", errors="surrogateescape")
        if MARCA in text:
            ja += 1
            continue
        motiu = cal_saltar(cami, text)
        if motiu:
            saltats += 1
            continue
        nou = text.replace("</body>", MARCA + "\n</body>", 1)
        if not args.dry_run:
            cami.write_text(nou, encoding="utf-8", errors="surrogateescape")
        fets += 1

    accio = "a posar" if args.dry_run else "posats"
    print(f"{fets} {accio} · {ja} ja el tenien · {saltats} saltats amb motiu")
    return 0


if __name__ == "__main__":
    sys.exit(main())
