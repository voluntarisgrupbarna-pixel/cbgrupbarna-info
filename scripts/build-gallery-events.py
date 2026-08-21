#!/usr/bin/env python3
"""Refa `fotos/events.js` a partir del que hi ha realment a `fotos/web/`.

El manifest es mantenia a ma i s'havia quedat curt: hi havia albums amb la
llista de fotos buida, albums sencers sense declarar i fitxers declarats que
no existeixen. Com que `fotos/index.html` NOMES llegeix aquest fitxer i no
escaneja cap carpeta, tota foto que no hi surti es invisible al web.

Que fa:
  - Recorre `fotos/web/<album>/` i recull els fitxers que hi ha de debo.
  - Conserva els metadades ja escrites de cada album (titol, descripcio, data,
    temporada, lloc, portada, allow_download): nomes en refresca la llista de
    fotos. Les dades editades a ma no es perden.
  - Declara els albums nous que trobi a disc i que no hi eren.

Dues trampes que ja ens han mossegat, i per aixo l'script les respecta:

  1. A `fotos/web/` tot es `.webp`, perque hi passa
     `scripts/build-gallery-images.py`. Pero el manifest declara els noms
     ORIGINALS (`.jpg`, `.jpeg`) i es la galeria qui canvia l'extensio al
     vol —mireu `derivada()` a `fotos/index.html`—, perque els originals de
     `fotos/uploads/` es descarreguen amb el nom de debo. Per tant es compara
     pel nom SENSE extensio i, si ja hi era, es conserva el nom declarat.

  2. No tots els albums viuen al repositori: el del 3x3 Westfield es
     Drive i les seves referencies no tenen ni extensio. Un album sense
     carpeta a `fotos/web/` NO es un album trencat: es un album de fora.
     L'script no el toca ni el treu.

Us:
    python3 scripts/build-gallery-events.py            # escriu i informa
    python3 scripts/build-gallery-events.py --dry-run  # nomes informa
"""

import json
import os
import re
import sys

WEB = "fotos/web"
THUMB = "fotos/thumb"
UPLOADS = "fotos/uploads"
DESTI = "fotos/events.js"

IMATGES = (".jpg", ".jpeg", ".png", ".webp")
VIDEOS = (".mp4", ".mov", ".webm")
MEDIA = IMATGES + VIDEOS

CAPCALERA = (
    "// CB Grup Barna · Galeria · Dades d'esdeveniments\n"
    "// Generat per scripts/build-gallery-events.py a partir de fotos/web/.\n"
    "// No l'editis a ma per afegir fotos: posa-les a fotos/web/<album>/ i torna\n"
    "// a executar l'script. Els metadades (titol, data, lloc...) si que es\n"
    "// conserven entre execucions.\n\n"
    "window.GALERIA_EVENTS = "
)


def titol_per_defecte(slug):
    """Un titol llegible a partir del slug, sense el sufix aleatori de pujada."""
    net = re.sub(r"-[a-z0-9]{8,}$", "", slug)
    return net.replace("-", " ").upper()


def llegeix_existents(cami):
    if not os.path.isfile(cami):
        return []
    text = open(cami, encoding="utf-8").read()
    try:
        inici = text.index("[")
        final = text.rindex("]") + 1
    except ValueError:
        sys.exit(f"No trobo l'array dins de {cami}.")
    return json.loads(text[inici:final])


def main():
    dry = "--dry-run" in sys.argv

    if not os.path.isdir(WEB):
        sys.exit(f"No trobo {WEB}. Executa'm des de l'arrel del repositori.")

    previs = {e["id"]: e for e in llegeix_existents(DESTI)}
    ordre_previ = [e["id"] for e in llegeix_existents(DESTI)]

    albums_disc = sorted(
        d for d in os.listdir(WEB) if os.path.isdir(os.path.join(WEB, d))
    )

    sortida = []
    afegides = tretes = nous = intactes = 0

    # Primer els que ja hi eren, en el mateix ordre; despres els nous.
    for slug in ordre_previ + [s for s in albums_disc if s not in previs]:
        previ = previs.get(slug)

        # Album de fora del repositori (Drive): es queda tal com esta.
        if slug not in albums_disc:
            intactes += 1
            print(f"  album de fora, no el toco: {slug}  ({len(previ.get('photos') or [])} refs)")
            sortida.append(previ)
            continue

        fitxers = sorted(
            f
            for f in os.listdir(os.path.join(WEB, slug))
            if f.lower().endswith(MEDIA) and not f.startswith(".")
        )
        if not fitxers:
            print(f"  carpeta buida, l'ometo:    {slug}")
            continue

        if previ is None:
            nous += 1
            print(f"  album NOU:                 {slug}  ({len(fitxers)} fitxers)")
            ev = {
                "id": slug,
                "title": titol_per_defecte(slug),
                "description": None,
                "date": None,
                "season": None,
                "location": None,
                "cover": None,
                "cover_url": None,
                "photos": [],
                "allow_download": True,
                "source": "repo",
            }
            ev["photos"] = fitxers
        else:
            ev = dict(previ)
            declarades = list(previ.get("photos") or [])
            # Es compara sense extensio; si ja hi era, es conserva el nom declarat.
            per_arrel = {os.path.splitext(f)[0]: f for f in declarades}
            arrels_disc = {os.path.splitext(f)[0] for f in fitxers}

            noves = [f for f in fitxers if os.path.splitext(f)[0] not in per_arrel]
            # Els videos no passen per `fotos/web/`: es serveixen tal com son des
            # de `fotos/uploads/`. Nomes son fantasma si tampoc hi son alla.
            fantasma = [
                f
                for f in declarades
                if os.path.splitext(f)[0] not in arrels_disc
                and not (
                    f.lower().endswith(VIDEOS)
                    and os.path.isfile(os.path.join(UPLOADS, slug, f))
                )
            ]
            # Un video que si existeix a uploads es conserva.
            videos_ok = [
                f
                for f in declarades
                if f.lower().endswith(VIDEOS) and f not in fantasma and f not in fitxers
            ]

            if noves:
                afegides += len(noves)
                print(f"  +{len(noves):4} fotos recuperades:   {slug}")
            if fantasma:
                tretes += len(fantasma)
                print(
                    f"  -{len(fantasma):4} declarades sense fitxer: {slug}"
                    f"  ({', '.join(fantasma[:3])}{'...' if len(fantasma) > 3 else ''})"
                )

            ev["photos"] = sorted(
                [per_arrel.get(os.path.splitext(f)[0], f) for f in fitxers] + videos_ok
            )

        # La portada ha d'existir; si no, la primera imatge de l'album.
        if ev.get("cover") not in ev["photos"]:
            imatges = [f for f in ev["photos"] if f.lower().endswith(IMATGES)]
            ev["cover"] = imatges[0] if imatges else None

        sortida.append(ev)

    total = sum(len(e["photos"]) for e in sortida)
    print(
        f"\n{len(sortida)} albums · {total} refs declarades"
        f"  (+{afegides} recuperades, -{tretes} sense fitxer, {nous} albums nous,"
        f" {intactes} de fora intactes)"
    )

    if dry:
        print("--dry-run: no he escrit res.")
        return

    with open(DESTI, "w", encoding="utf-8") as f:
        f.write(CAPCALERA)
        json.dump(sortida, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print(f"Escrit {DESTI}.")


if __name__ == "__main__":
    main()
