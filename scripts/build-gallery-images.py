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

# El sostre de pes per fitxer servit, el mateix que vigila
# scripts/pes-pressupost.py. Hi és perquè aquest script el respecti: fins
# ara en generava de fins a 1,2 MB i el CI els rebutjava després, o sigui
# que el pipeline produïa el que la comprovació no deixava passar.
SOSTRE = 700_000
QUALITATS_DE_REPESCA = (82, 76, 70, 64)

IMATGES = (".jpg", ".jpeg", ".png", ".webp", ".heic")
VIDEOS = (".mp4", ".mov", ".webm")

force = "--force" in sys.argv


def versions(origen, event, nom):
    """Escriu les dues versions d'una foto.
    Retorna (fetes, ampliacions_evitades, repescades)."""
    base = os.path.splitext(nom)[0]
    calen = []
    for arrel, ample, qualitat in SORTIDES:
        desti = os.path.join(arrel, event, base + ".webp")
        # Es refà també si la que hi ha passa del sostre: així el dia que
        # s'apuja el sostre o es canvia la qualitat, una passada ho posa al
        # dia sense haver de recordar-se de --force.
        massa_gran = (os.path.exists(desti) and os.path.getsize(desti) > SOSTRE)
        if force or not os.path.exists(desti) or massa_gran:
            calen.append((desti, ample, qualitat))
    if not calen:
        return 0, 0, 0

    with Image.open(origen) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        fetes = evitades = repescades = 0
        for desti, ample, qualitat in calen:
            os.makedirs(os.path.dirname(desti), exist_ok=True)
            copia = im.copy()
            if copia.width > ample:
                copia.thumbnail((ample, ample * 10), Image.LANCZOS)
            else:
                evitades += 1  # ja és més petita: es desa tal qual, mai s'amplia
            copia.save(desti, "WEBP", quality=qualitat, method=6)
            # Una foto amb molt detall (una grada plena, una pista sencera)
            # no baixa del sostre a qualitat 88. Abans d'encongir-la —que és
            # el que es nota— es prova de baixar la qualitat: a 82 la
            # diferència no es veu, i el pes cau a la meitat.
            if os.path.getsize(desti) > SOSTRE:
                for q in QUALITATS_DE_REPESCA:
                    copia.save(desti, "WEBP", quality=q, method=6)
                    if os.path.getsize(desti) <= SOSTRE:
                        break
                repescades += 1
            fetes += 1
    return fetes, evitades, repescades


def main():
    if not os.path.isdir(ORIGINALS):
        sys.exit(f"No trobo {ORIGINALS}. Executa'm des de l'arrel del repositori.")

    total = saltats = evitades = repescades = 0
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
                fetes, ev, rep = versions(os.path.join(dir_event, nom), event, nom)
            except Exception as e:
                print(f"  ! {event}/{nom}: {e}")
                continue
            total += fetes
            evitades += ev
            repescades += rep
            n += 1
        if n:
            print(f"  {event[:52]:52} {n:4} fotos")

    print(f"\n{total} fitxers escrits · {saltats} vídeos intactes")
    if repescades:
        print(f"{repescades} han passat del sostre de {SOSTRE // 1000} KB a qualitat "
              f"88 i s'han tornat a desar amb menys qualitat, sense encongir-les.")
    if evitades:
        print(f"{evitades} versions desades a la mida real: l'original no arribava "
              f"a la mida de destí i no s'amplia mai.")


if __name__ == "__main__":
    main()
