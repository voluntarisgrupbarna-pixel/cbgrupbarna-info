#!/usr/bin/env python3
"""Pressupost de pes: cap fitxer servit per sobre del sostre del seu tipus.

La regla del sistema de disseny llegida per l'altra banda: si cap foto no
s'ha de mostrar mes gran del que es, tampoc no s'ha de publicar cap fitxer
mes pesat del que el seu tipus necessita. Aquest script es el que impedeix
que un original de 14 MB, un PDF sense comprimir o un video sencer es colin
al repositori sense que ningu ho vegi.

Sortida 0 si tot passa; 1 amb la llista del que s'ha passat de pes.

Excepcions: `pes-excepcions.txt` a l'arrel, una per linia, `ruta: motiu`.
Una excepcio sense motiu no val.
"""
from __future__ import annotations

import os
import sys

ARREL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Sostre per tipus, en bytes. Calibrats sobre el pes real del lloc el
# 26/08/2026: el fitxer legitim mes gran de cada tipus hi cap amb marge
# (foto de galeria 680 KB, portada 172 KB, presentacio 2,1 MB, index de
# cerca 748 KB), i el que voldriem aturar (originals de camera, exports
# sense comprimir) no.
SOSTRES = {
    ".html": 250_000,
    ".webp": 700_000, ".jpg": 700_000, ".jpeg": 700_000, ".png": 700_000,
    ".gif": 700_000, ".avif": 700_000, ".svg": 300_000,
    ".pdf": 2_500_000,
    ".mp4": 12_000_000, ".webm": 12_000_000, ".mov": 12_000_000,
    ".js": 800_000, ".css": 800_000, ".json": 800_000,
    ".woff2": 400_000, ".woff": 400_000, ".ttf": 400_000,
    ".ics": 500_000,
    ".mp3": 5_000_000, ".m4a": 5_000_000,
}

# Carpetes que no son el lloc servit o que tenen el seu propi cicle:
# el mirall del Premi (font externa), l'app de galeria (build propi),
# els originals de fotos (masters, no es serveixen enllacats) i la cuina.
EXCLOSES = {
    ".git", "node_modules", "premidonaesport", "galeria",
    os.path.join("fotos", "uploads"), "scripts", "tests", "i18n",
    os.path.join(".github",),
}


def excepcions() -> dict[str, str]:
    fitxer = os.path.join(ARREL, "pes-excepcions.txt")
    res: dict[str, str] = {}
    if not os.path.exists(fitxer):
        return res
    with open(fitxer, encoding="utf-8") as f:
        for linia in f:
            linia = linia.strip()
            if not linia or linia.startswith("#"):
                continue
            ruta, _, motiu = linia.partition(":")
            ruta, motiu = ruta.strip(), motiu.strip()
            if ruta and motiu:
                res[ruta] = motiu
    return res


def exclosa(rel: str) -> bool:
    parts = rel.split(os.sep)
    for n in range(1, len(parts)):
        if os.path.join(*parts[:n]) in EXCLOSES or parts[n - 1] in EXCLOSES:
            return True
    return False


def main() -> int:
    exc = excepcions()
    errors = []
    usades = set()
    for carpeta, dirs, fitxers in os.walk(ARREL):
        rel_dir = os.path.relpath(carpeta, ARREL)
        dirs[:] = [d for d in dirs
                   if not exclosa(os.path.normpath(os.path.join(rel_dir, d)))]
        for nom in fitxers:
            rel = os.path.normpath(os.path.join(rel_dir, nom))
            ext = os.path.splitext(nom)[1].lower()
            sostre = SOSTRES.get(ext)
            if sostre is None:
                continue
            pes = os.path.getsize(os.path.join(carpeta, nom))
            if pes <= sostre:
                continue
            ruta = rel.replace(os.sep, "/")
            if ruta in exc:
                usades.add(ruta)
                continue
            errors.append((ruta, pes, sostre))

    for ruta in sorted(set(exc) - usades):
        print(f"  ·  excepcio que ja no cal (el fitxer no hi es o ja passa): {ruta}")

    if errors:
        print("Fitxers per sobre del pressupost de pes:")
        for ruta, pes, sostre in sorted(errors, key=lambda e: -e[1]):
            print(f"  ✗  {ruta} — {pes/1_000_000:.1f} MB (sostre {sostre/1_000_000:.1f} MB)")
        print("\nO es comprimeix (imatges: scripts/build-imatges-responsives.py;"
              " PDF: ghostscript /ebook), o s'afegeix a pes-excepcions.txt amb el motiu.")
        return 1
    print("Pressupost de pes: tot dins del sostre.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
