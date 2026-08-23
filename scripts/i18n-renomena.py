#!/usr/bin/env python3
"""
Aplica els renoms d'adreça de i18n/renoms.yml: mou la pàgina, hi deixa una
redirecció i actualitza tots els enllaços que hi portaven.

    python3 scripts/i18n-renomena.py --dry-run
    python3 scripts/i18n-renomena.py

Un article en anglès amb l'adreça en català no el troba ningú: qui busca
«what is 3x3 basketball» no escriu «que-es-basquet-3x3». Això ho arregla,
però amb una condició que no es pot saltar: **l'adreça vella ha de continuar
funcionant**. Hi ha enllaços publicats, gent que ho té guardat i cercadors que
encara hi porten.

Com que GitHub Pages no fa redireccions de servidor, a l'adreça vella hi queda
una pàgina que no fa res més que portar a la nova: un <meta http-equiv=refresh>
perquè el navegador hi vagi sol, un <link rel=canonical> a la nova perquè els
cercadors sàpiguen quina val, i un enllaç visible per si el salt no es fa.

No hi va cap `noindex`: el que ha de fer un cercador amb aquestes pàgines és
seguir-les i quedar-se la nova, i un `noindex` li diu que no se les miri, que
és una altra cosa. Del sitemap en queden fora perquè
scripts/build-sitemap.py salta les pàgines amb `http-equiv="refresh"`.

Què fa, per a cada renom:

  1. Mou la pàgina (amb `git mv`, perquè l'historial la segueixi).
  2. Hi corregeix el canonical i l'og:url, que encara diuen l'adreça vella.
  3. Deixa la redirecció a l'adreça vella.
  4. Reescriu tots els enllaços interns del lloc que hi portaven.
  5. Actualitza i18n/routes.yml.

Després cal refer els hreflang i el sitemap:

    python3 scripts/i18n-hreflang.py && python3 scripts/build-sitemap.py
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RENOMS = ROOT / "i18n" / "renoms.yml"
MAPA = ROOT / "i18n" / "routes.yml"
SITE = "https://cbgrupbarna.info"

REDIRECCIO = """<!doctype html>
<html lang="{idioma}">
<head>
<meta charset="UTF-8">
<title>{titol}</title>
<link rel="canonical" href="{nova}">
<meta http-equiv="refresh" content="0; url={desti}">
</head>
<body>
<p>{frase} <a href="{desti}">{desti}</a></p>
</body>
</html>
"""
FRASES = {
    "ca": ("Aquesta pàgina ha canviat d'adreça", "Aquesta pàgina és ara a"),
    "es": ("Esta página ha cambiado de dirección", "Esta página está ahora en"),
    "en": ("This page has moved", "This page is now at"),
}


def fitxer_de(url):
    resta = url.lstrip("/")
    return ROOT / (resta + "index.html" if url.endswith("/") else resta)


def idioma_de(url):
    return "es" if url.startswith("/es/") else "en" if url.startswith("/en/") else "ca"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    renoms = (yaml.safe_load(RENOMS.read_text(encoding="utf-8")) or {}).get("renoms", [])
    fets, ja_fets, enllacos = 0, 0, 0

    for r in renoms:
        vella, nova = r["de"], r["a"]
        f_vella, f_nova = fitxer_de(vella), fitxer_de(nova)

        if f_nova.exists() and not f_vella.exists():
            ja_fets += 1
            continue
        if not f_vella.exists():
            print(f"  ATENCIÓ: {vella} no existeix i {nova} tampoc. Salto.")
            continue
        if f_nova.exists():
            print(f"  ATENCIÓ: {nova} ja existeix i {vella} també. Salto: mireu-ho a mà.")
            continue

        print(f"  {vella}\n    → {nova}")
        if args.dry_run:
            fets += 1
            continue

        # 1. Moure. Amb git mv perquè l'historial de la pàgina no es perdi.
        f_nova.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "mv", str(f_vella.relative_to(ROOT)),
                        str(f_nova.relative_to(ROOT))], cwd=ROOT, check=True)

        # 2. El canonical i l'og:url encara diuen l'adreça vella.
        text = f_nova.read_text(encoding="utf-8")
        text = text.replace(SITE + vella, SITE + nova)
        f_nova.write_text(text, encoding="utf-8")

        # 3. La redirecció a l'adreça vella.
        idioma = idioma_de(vella)
        titol, frase = FRASES[idioma]
        f_vella.parent.mkdir(parents=True, exist_ok=True)
        f_vella.write_text(REDIRECCIO.format(
            idioma=idioma, titol=titol, frase=frase, nova=SITE + nova, desti=nova),
            encoding="utf-8")
        fets += 1

    # 4. Els enllaços interns. Es fa al final i d'una tirada, perquè una
    #    pàgina pot enllaçar-ne unes quantes de les que s'han mogut.
    parells = [(r["de"], r["a"]) for r in renoms if fitxer_de(r["a"]).exists()]
    if parells and not args.dry_run:
        for fitxer in ROOT.rglob("*.html"):
            if ".git" in fitxer.parts:
                continue
            text = original = fitxer.read_text(encoding="utf-8", errors="ignore")
            for vella, nova in parells:
                if fitxer == fitxer_de(vella):
                    continue                      # la redirecció ha d'apuntar-hi
                text = re.sub(rf'(href=["\'])({re.escape(SITE)})?{re.escape(vella)}',
                              rf'\1\g<2>{nova}', text)
            if text != original:
                enllacos += 1
                fitxer.write_text(text, encoding="utf-8")

    # 5. El mapa d'idiomes.
    if not args.dry_run and fets:
        mapa = MAPA.read_text(encoding="utf-8")
        for r in renoms:
            mapa = mapa.replace(f": {r['de']}\n", f": {r['a']}\n")
        MAPA.write_text(mapa, encoding="utf-8")

    print(f"\n{fets} pàgines mogudes"
          + (f", {ja_fets} que ja ho estaven" if ja_fets else "")
          + (f" · enllaços actualitzats en {enllacos} pàgines" if enllacos else "")
          + (" (no s'ha desat res)" if args.dry_run else ""))
    if fets and not args.dry_run:
        print("\nAra toca:  python3 scripts/i18n-hreflang.py && python3 scripts/build-sitemap.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
