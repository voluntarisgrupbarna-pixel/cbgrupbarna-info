#!/usr/bin/env python3
"""Genera la versio d'ARXIU de la galeria: 2560 px, qualitat 92.

Es la copia mestra. Un cop pujada a R2 i verificada, els originals de la
camera es poden treure del repositori: a 2560 px la foto encara s'imprimeix
en A4 a qualitat d'impremta (un A4 a 300 dpi son 2480 px) i no es distingeix
de l'original en cap pantalla.

Escriu a `fotos/arxiu/<event>/<nom>.webp`. Els videos no es toquen: van a R2
tal com son, sense transcodificar.

Les dues regles de sempre: no s'amplia mai res, i l'orientacio EXIF s'aplica
abans de redimensionar.

Us:
    python3 scripts/build-gallery-archive.py            # nomes el que falta
    python3 scripts/build-gallery-archive.py --force    # refa-ho tot
"""

import os
import sys
from PIL import Image, ImageOps

ORIGINALS = "fotos/uploads"
DESTI = "fotos/arxiu"
AMPLE = 2560
QUALITAT = 92

IMATGES = (".jpg", ".jpeg", ".png", ".webp", ".heic")
VIDEOS = (".mp4", ".mov", ".webm")

force = "--force" in sys.argv


def main():
    if not os.path.isdir(ORIGINALS):
        sys.exit(f"No trobo {ORIGINALS}. Executa'm des de l'arrel del repositori.")

    fets = saltats = evitades = 0
    bytes_out = 0

    for event in sorted(os.listdir(ORIGINALS)):
        dir_event = os.path.join(ORIGINALS, event)
        if not os.path.isdir(dir_event):
            continue
        n = 0
        for nom in sorted(os.listdir(dir_event)):
            baix = nom.lower()
            if baix.endswith(VIDEOS):
                saltats += 1
                continue
            if not baix.endswith(IMATGES):
                continue

            desti = os.path.join(DESTI, event, os.path.splitext(nom)[0] + ".webp")
            if not force and os.path.exists(desti):
                bytes_out += os.path.getsize(desti)
                continue

            os.makedirs(os.path.dirname(desti), exist_ok=True)
            try:
                with Image.open(os.path.join(dir_event, nom)) as im:
                    im = ImageOps.exif_transpose(im).convert("RGB")
                    if im.width > AMPLE:
                        im.thumbnail((AMPLE, AMPLE * 10), Image.LANCZOS)
                    else:
                        evitades += 1   # ja es mes petita: mai s'amplia
                    im.save(desti, "WEBP", quality=QUALITAT, method=6)
            except Exception as e:
                print(f"  ! {event}/{nom}: {e}")
                continue

            bytes_out += os.path.getsize(desti)
            fets += 1
            n += 1
        if n:
            print(f"  {event[:52]:52} {n:4} fotos")

    print(f"\n{fets} fitxers nous · {saltats} videos intactes · "
          f"{bytes_out / 1073741824:.2f} GB d'arxiu en total")
    if evitades:
        print(f"{evitades} desades a la mida real: l'original no arribava als {AMPLE} px.")


if __name__ == "__main__":
    main()
