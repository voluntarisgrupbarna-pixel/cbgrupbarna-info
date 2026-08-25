#!/usr/bin/env python3
"""Posa el botó ≡ (js/mapa.js) a totes les pàgines reals del web.

Idempotent: es pot tornar a passar sempre; si la pàgina ja el carrega, no
fa res. Afegeix una sola línia abans de </body>:

    <script src="/js/mapa.js" defer></script>

Què salta, i per què:
  · admin i eines internes — no són cara pública
  · peces per imprimir (opina/print, escoleta/flyer, partits/cartell) —
    generen una imatge
  · redireccions amb <meta http-equiv="refresh"> — no es veuen
  · galeria/ (app Next.js) — té la seva pròpia capçalera compilada
  · premidonaesport/ — mirall d'una web externa amb la seva pròpia
    navegació lateral i porta amb PIN

Ús:
    python3 scripts/mapa-aplica.py --dry-run
    python3 scripts/mapa-aplica.py
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

MARCA = '<script src="/js/mapa.js" defer></script>'
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
