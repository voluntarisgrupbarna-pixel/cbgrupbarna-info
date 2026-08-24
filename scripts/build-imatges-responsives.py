#!/usr/bin/env python3
"""Versions responsives de les fotos grans que es serveixen senceres.

Per que existeix: aquelles fotos es servien en JPG, a mida completa i sense
`srcset`. La mes gran, `hero-equip.jpg`, fa 2100 px d'ample i 468 KB, i mai es
mostra a mes de 689 px de CSS: a un mobil es baixaven tres vegades els pixels
que calien. Es la regla del sistema de disseny —cap foto no es mostra mai mes
gran del que es, i en retina en calen el doble dels que ocupa— aplicada a la
banda contraria: tampoc no se n'han de baixar mes dels que caben.

Genera, per a cada foto, un WebP a 400, 800 i 1400 px (o a l'amplada original,
si es mes petita: mai s'amplia res). Els fitxers surten al costat de l'original,
amb el mateix nom i el sufix de l'amplada.

Les tres amplades no son arbitraries: la foto es mostra com a molt a 689 px de
CSS, i en una pantalla retina de 390 px en calen uns 780 de reals. Amb nomes
700 i 1400, aquell mobil es baixava el de 1400.

    python3 scripts/build-presentacio-images.py
    python3 scripts/build-presentacio-images.py --dry-run
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

# Carpetes i fitxers solts que encara servien la foto sencera. La llista es
# curta a proposit: la resta del lloc ja fa servir srcset, i aixo nomes son
# els que van quedar fora.
CARPETES = [ROOT / "presentacio" / "img"]
FITXERS = [
    ROOT / "patrocinis" / "photos" / "hero_sf16.jpg",
    ROOT / "presentacions" / "fons-barna-8m" / "img" / "staff-06.jpg",
    ROOT / "3x3" / "img" / "hero-bg-1.jpg",
    ROOT / "premsa" / "img" / "article-guia-clot-pagina-1.webp",
]
AMPLADES = (400, 800, 1400)
QUALITAT = 82


def variants(fitxer: Path):
    with Image.open(fitxer) as im:
        original = im.width
        fetes = []
        for ample in AMPLADES:
            # Mai per sobre de l'original: ampliar una foto es nota sempre.
            objectiu = min(ample, original)
            desti = fitxer.with_name(f"{fitxer.stem}-{objectiu}.webp")
            if desti.exists() and desti.stat().st_mtime >= fitxer.stat().st_mtime:
                fetes.append((desti, objectiu, None))
                continue
            if "--dry-run" in sys.argv:
                fetes.append((desti, objectiu, "escriuria"))
                continue
            copia = im.convert("RGB")
            if objectiu < original:
                alt = round(im.height * objectiu / original)
                copia = copia.resize((objectiu, alt), Image.LANCZOS)
            copia.save(desti, "WEBP", quality=QUALITAT, method=6)
            fetes.append((desti, objectiu, "escrit"))
        return original, fetes


def main():
    origens = []
    for carpeta in CARPETES:
        if carpeta.is_dir():
            origens += sorted(carpeta.glob("*.jpg"))
    origens += [f for f in FITXERS if f.is_file()]
    if not origens:
        sys.exit("No trobo cap imatge d'origen.")
    vistes = set()
    for fitxer in origens:
        original, fetes = variants(fitxer)
        for desti, ample, estat in fetes:
            if desti.name in vistes:
                continue
            vistes.add(desti.name)
            pes = desti.stat().st_size // 1024 if desti.exists() else 0
            marca = estat or "ja hi era"
            print(f"  {marca:9} {desti.name:32} {ample:>5} px  {pes:>5} KB"
                  f"   (original {original} px, {fitxer.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
