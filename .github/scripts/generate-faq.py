#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Escriu les preguntes freqüents a les pàgines, en els tres idiomes, des d'una
sola font: i18n/faq.yml.

  python3 .github/scripts/generate-faq.py --dry-run   # mira què faria
  python3 .github/scripts/generate-faq.py             # ho fa
  python3 .github/scripts/generate-faq.py --pendents  # què falta per escriure

PER QUÈ EXISTEIX
----------------
Una pregunta freqüent ha de constar a DOS llocs de la mateixa pàgina: al
`<details>` que llegeix la gent i al `FAQPage` del JSON-LD que llegeixen
Google i el cercador del web. I la pàgina existeix tres vegades: català,
castellà i anglès. Són sis llocs per pregunta, mantinguts a mà.

No aguanta. El 23/08/2026, comptades sobre l'índex del cercador, hi havia
**28 pàgines amb les tres versions desquadrades** (la portada anava 15/11/11
i /grup-barna-dades-oficials/, 8/0/0). El comentari que hi ha escrit a
escoleta/index.html —«FAQ visible · ha de coincidir sempre amb el FAQPage del
JSON-LD»— era una regla de bona voluntat, no un mecanisme.

Ara la pregunta s'escriu UN cop, amb els seus tres idiomes, i aquest script la
reparteix. És el mateix patró de marcadors que ja fa servir
generate-seo-snapshot.py a /partits/: fora dels marcadors, la pàgina és teva i
no s'hi toca res.

COM S'AFEGEIX UNA PREGUNTA
--------------------------
1. Una entrada nova a `i18n/faq.yml`, amb `pagina:` en català (la ruta
   canònica) i els blocs `ca:`, `es:` i `en:`.
2. La pàgina de destí ha de portar els dos parells de marcadors (vegeu
   `MARCADORS` aquí sota). Si no els porta, l'script t'ho diu i no la toca.
3. Executa'l. El cercador se n'assabenta tot sol: llegeix el JSON-LD.

Una entrada amb `pendent:` no es publica enlloc —ni tan sols en català— i surt
a `--pendents`. Serveix per deixar escrita una pregunta que encara espera una
dada (un preu, una data) sense publicar-ne mitja resposta.
"""

import argparse
import html
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("Cal PyYAML:  pip install pyyaml")

ARREL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONT = os.path.join(ARREL, "i18n", "faq.yml")
RUTES = os.path.join(ARREL, "i18n", "routes.yml")
IDIOMES = ("ca", "es", "en")

# (marcador visible, marcador del JSON-LD)
MARCADORS = ("FAQ", "FAQ-LD")

BASE = "https://cbgrupbarna.info"


def carrega_rutes():
    with open(RUTES, encoding="utf-8") as f:
        dades = yaml.safe_load(f) or {}
    mapa = {}
    for r in dades.get("rutes", []):
        if not r.get("ca"):
            continue
        mapa[r["ca"]] = {i: r.get(i) for i in IDIOMES}
        mapa[r["ca"]]["ca"] = r["ca"]
    return mapa


def cami_de(url):
    """De la URL pública al fitxer del disc."""
    net = url.strip("/")
    if not net:
        return os.path.join(ARREL, "index.html")
    if net.endswith(".html"):
        return os.path.join(ARREL, *net.split("/"))
    return os.path.join(ARREL, *net.split("/"), "index.html")


def bloc_visible(parells):
    """Els <details> que llegeix la gent. Sense salts de línia entremig:
    el marcatge d'aquestes seccions al repositori va tot seguit."""
    fora = []
    for q, r in parells:
        fora.append(
            '<details class="faq-q"><summary>%s</summary><p>%s</p></details>'
            % (html.escape(q, quote=False), html.escape(r, quote=False))
        )
    return "".join(fora)


def bloc_ld(parells, url, idioma):
    """El FAQPage del JSON-LD. Va en un <script> propi, no dins del @graph que
    ja tingui la pàgina: així no cal reescriure un JSON aliè per afegir-hi una
    pregunta, i Google accepta més d'un bloc ld+json per pàgina."""
    dades = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": BASE + url + "#faq",
        "inLanguage": idioma,
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": r},
            }
            for q, r in parells
        ],
    }
    return ('<script type="application/ld+json">%s</script>'
            % json.dumps(dades, ensure_ascii=False, indent=2))


def escriu_entre(text, marcador, contingut):
    """Substitueix el que hi ha entre <!-- X:START --> i <!-- X:END -->.

    Torna (text_nou, trobat). Si els marcadors no hi són, no s'inventa on
    posar-ho: aquesta decisió és de qui fa la pàgina, no d'un script.
    """
    patro = re.compile(
        r"(<!--\s*%s:START\s*-->)(.*?)(<!--\s*%s:END\s*-->)" % (
            re.escape(marcador), re.escape(marcador)),
        re.S)
    if not patro.search(text):
        return text, False
    return patro.sub(lambda m: m.group(1) + contingut + m.group(3), text, count=1), True


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="no desa res")
    ap.add_argument("--pendents", action="store_true",
                    help="només llista les preguntes que esperen una dada")
    args = ap.parse_args()

    with open(FONT, encoding="utf-8") as f:
        font = yaml.safe_load(f) or {}
    entrades = font.get("preguntes", [])
    rutes = carrega_rutes()

    pendents = [e for e in entrades if e.get("pendent")]
    if args.pendents:
        if not pendents:
            print("Cap pregunta pendent: totes tenen resposta.")
            return 0
        print(f"{len(pendents)} preguntes esperen una dada per poder-se publicar:\n")
        for e in pendents:
            print(f"  · [{e.get('id')}] {(e.get('ca') or {}).get('q', '(sense text)')}")
            print(f"      cal: {e['pendent']}")
            print(f"      aniria a: {e.get('pagina')}")
        return 0

    # Agrupa per pàgina canònica, respectant l'ordre del fitxer.
    per_pagina = {}
    for e in entrades:
        if e.get("pendent"):
            continue
        per_pagina.setdefault(e["pagina"], []).append(e)

    tocats, iguals = [], 0
    sense_marcadors, sense_traduccio = [], []

    for pagina_ca, grup in sorted(per_pagina.items()):
        mapa = rutes.get(pagina_ca) or {"ca": pagina_ca}
        for idioma in IDIOMES:
            url = mapa.get(idioma)
            if not url:
                sense_traduccio.append((pagina_ca, idioma))
                continue

            parells = []
            for e in grup:
                tros = e.get(idioma) or {}
                q, r = (tros.get("q") or "").strip(), (tros.get("r") or "").strip()
                if q and r:
                    parells.append((q, r))
            if not parells:
                sense_traduccio.append((pagina_ca, idioma))
                continue

            cami = cami_de(url)
            if not os.path.exists(cami):
                sense_marcadors.append((url, "el fitxer no existeix"))
                continue

            with open(cami, encoding="utf-8") as f:
                original = f.read()

            nou, te_v = escriu_entre(original, MARCADORS[0], bloc_visible(parells))
            nou, te_ld = escriu_entre(nou, MARCADORS[1], bloc_ld(parells, url, idioma))

            if not te_v or not te_ld:
                falten = []
                if not te_v:
                    falten.append(MARCADORS[0])
                if not te_ld:
                    falten.append(MARCADORS[1])
                sense_marcadors.append((url, "falten els marcadors " + " i ".join(falten)))
                continue

            if nou == original:
                iguals += 1
                continue
            if not args.dry_run:
                with open(cami, "w", encoding="utf-8") as f:
                    f.write(nou)
            tocats.append((url, len(parells)))

    cap = "(prova) " if args.dry_run else ""
    print(f"{cap}{len(tocats)} pàgines actualitzades · {iguals} ja estaven al dia")
    for url, n in tocats:
        print(f"    {n:2} preguntes  {url}")

    if sense_traduccio:
        print(f"\n  {len(sense_traduccio)} versions sense text (la pregunta no hi surt):")
        for pagina, idioma in sense_traduccio:
            print(f"    {idioma}  de  {pagina}")
    if sense_marcadors:
        print(f"\n  {len(sense_marcadors)} pàgines que no s'han pogut escriure:")
        for url, motiu in sense_marcadors:
            print(f"    {url} — {motiu}")
    if pendents:
        print(f"\n  {len(pendents)} preguntes pendents d'una dada "
              f"(--pendents per veure quines). No s'han publicat.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
