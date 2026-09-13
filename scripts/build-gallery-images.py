#!/usr/bin/env python3
"""Genera les versions web de la galeria a partir dels originals.

Per cada foto de `fotos/uploads/<event>/` escriu dues versions a:

  fotos/web/<event>/<nom>.webp    2048 px  — el que es veu al visor
  fotos/thumb/<event>/<nom>.webp   400 px  — el que es veu a la graella

Amb això la galeria deixa de dependre de wsrv.nl, el proxy extern que fins ara
descarregava cada original de 14 MB i l'encongia al vol: d'aquí la lentitud, i
d'aquí que les fotos de les famílies passessin per un tercer.

Dues regles del sistema de disseny, aplicades aquí:

  · No s'amplia mai res. Si l'original és més petit que la mida de destí, es
    desa a la seva mida real i s'anota. El marc s'ha d'adaptar a la foto, no
    la foto al marc.
  · L'orientació de l'EXIF s'aplica abans de redimensionar, si no les fotos
    fetes en vertical surten tombades.

Els vídeos no es toquen: es serveixen tal com són.

Ús:
    python3 scripts/build-gallery-images.py            # només el que falta
    python3 scripts/build-gallery-images.py --force    # refà-ho tot
"""

import os
import sys
from PIL import Image, ImageOps

ORIGINALS = "fotos/uploads"
SORTIDES = [("fotos/web", 2048, 88), ("fotos/thumb", 400, 80)]

IMATGES = (".jpg", ".jpeg", ".png", ".webp", ".heic")
VIDEOS = (".mp4", ".mov", ".webm")

# El mateix sostre que fa complir scripts/pes-pressupost.py per a .webp: cap
# fitxer servit no hi pot passar per sobre. Una foto amb molt de detall a
# 2048 px i qualitat 88 s'hi pot enfilar; en lloc de descobrir-ho quan el
# CI ja ha fallat, el generador es limita sol.
SOSTRE_PES = 700_000
QUALITAT_MINIMA = 60
AMPLE_MINIM = 1400  # mai per sota d'això: encara s'ha de veure bé a pantalla completa

force = "--force" in sys.argv


def versions(origen, event, nom):
    """Escriu les dues versions d'una foto. Retorna (fetes, ampliacions_evitades)."""
    base = os.path.splitext(nom)[0]
    calen = []
    for arrel, ample, qualitat in SORTIDES:
        desti = os.path.join(arrel, event, base + ".webp")
        if force or not os.path.exists(desti):
            calen.append((desti, ample, qualitat))
    if not calen:
        return 0, 0

    with Image.open(origen) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        fetes = evitades = 0
        for desti, ample, qualitat in calen:
            os.makedirs(os.path.dirname(desti), exist_ok=True)
            copia = im.copy()
            ample_actual = ample
            if copia.width > ample:
                copia.thumbnail((ample, ample * 10), Image.LANCZOS)
            else:
                evitades += 1  # ja és més petita: es desa tal qual, mai s'amplia
            copia.save(desti, "WEBP", quality=qualitat, method=6)
            # Si una foto molt detallada s'enfila per sobre del sostre de pes,
            # es reintenta amb menys qualitat fins que hi cap. Si ni al mínim
            # de qualitat n'hi ha prou (fotos molt carregades de detall), es
            # retalla també l'amplada un 10% i es torna a provar tota la
            # gamma de qualitat, sense baixar mai del mínim publicable.
            q = qualitat
            while os.path.getsize(desti) > SOSTRE_PES:
                if q > QUALITAT_MINIMA:
                    q = max(QUALITAT_MINIMA, q - 8)
                elif ample_actual > AMPLE_MINIM and copia.width > AMPLE_MINIM:
                    ample_actual = max(AMPLE_MINIM, round(ample_actual * 0.9))
                    copia = im.copy()
                    copia.thumbnail((ample_actual, ample_actual * 10), Image.LANCZOS)
                    q = qualitat
                else:
                    break  # ja no es pot fer més petit sense passar-se
                copia.save(desti, "WEBP", quality=q, method=6)
            fetes += 1
    return fetes, evitades


def main():
    if not os.path.isdir(ORIGINALS):
        sys.exit(f"No trobo {ORIGINALS}. Executa'm des de l'arrel del repositori.")

    total = saltats = evitades = 0
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
            try:
                fetes, ev = versions(os.path.join(dir_event, nom), event, nom)
            except Exception as e:
                print(f"  ! {event}/{nom}: {e}")
                continue
            total += fetes
            evitades += ev
            n += 1
        if n:
            print(f"  {event[:52]:52} {n:4} fotos")

    print(f"\n{total} fitxers escrits · {saltats} vídeos intactes")
    if evitades:
        print(f"{evitades} versions desades a la mida real: l'original no arribava "
              f"a la mida de destí i no s'amplia mai.")


if __name__ == "__main__":
    main()
