#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Omple les traduccions que falten a i18n/faq.yml amb el mateix traductor que
ja fa servir la resta del web.

  export ANTHROPIC_API_KEY=...
  python3 scripts/faq-tradueix.py es       # només el castellà
  python3 scripts/faq-tradueix.py --tot    # castellà i anglès
  python3 scripts/faq-tradueix.py --que-falta   # només diu què falta, sense clau

NO ÉS UN TRADUCTOR NOU. Reutilitza `scripts/i18n-tradueix.py`: el mateix
glossari (i18n/glossari.yml), el mateix to per idioma, els mateixos noms
propis que no es toquen mai i la mateixa comprovació que aquests noms no
s'han perdut pel camí. Si un dia es canvia el glossari, això canvia amb ell.

El motiu de tenir-ho a part és que aquell tradueix PÀGINES d'HTML, i les
preguntes freqüents ja no viuen a l'HTML: viuen a i18n/faq.yml, que és la
seva font única des del 23/08/2026.

Com la resta del sistema, sense clau no falla: diu què falta i marxa. I mai
publica res directament — omple el YAML, i qui escriu a les pàgines és
`.github/scripts/generate-faq.py`, que continua sent un pas a part. Entre les
dues coses hi ha d'haver algú mirant-s'ho.

Una entrada amb `pendent:` no es tradueix: encara no té resposta en cap
idioma, i traduir un buit no serveix de res.
"""

import argparse
import os
import sys
import importlib.util

try:
    import yaml
except ImportError:
    sys.exit("Cal PyYAML:  pip install pyyaml")

ARREL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ARREL, "i18n", "faq.yml")


def carrega_traductor():
    """Importa scripts/i18n-tradueix.py, que porta guionet al nom i per tant
    no es pot importar amb un `import` normal."""
    ruta = os.path.join(ARREL, "scripts", "i18n-tradueix.py")
    spec = importlib.util.spec_from_file_location("i18n_tradueix", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def que_falta(entrades, idiomes):
    fora = []
    for e in entrades:
        if e.get("pendent"):
            continue
        ca = e.get("ca") or {}
        if not (ca.get("q") and ca.get("r")):
            continue
        for idioma in idiomes:
            tros = e.get(idioma) or {}
            if not (tros.get("q") and tros.get("r")):
                fora.append((e, idioma))
    return fora


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("idioma", nargs="?", choices=["es", "en"])
    ap.add_argument("--tot", action="store_true", help="els dos idiomes")
    ap.add_argument("--que-falta", action="store_true",
                    help="només informa; no demana res a ningú")
    ap.add_argument("--model", default=None)
    args = ap.parse_args()

    idiomes = ["es", "en"] if args.tot else ([args.idioma] if args.idioma else ["es", "en"])

    with open(FONT, encoding="utf-8") as f:
        dades = yaml.safe_load(f) or {}
    entrades = dades.get("preguntes", [])

    falten = que_falta(entrades, idiomes)
    if not falten:
        print("Cap traducció pendent: totes les preguntes publicables tenen "
              "els tres idiomes.")
        return 0

    print(f"{len(falten)} traduccions falten:")
    for e, idioma in falten:
        print(f"  {idioma}  [{e['id']}]  {(e.get('ca') or {}).get('q', '')[:60]}")

    if args.que_falta:
        return 0

    clau = os.environ.get("ANTHROPIC_API_KEY")
    if not clau:
        print("\nFalta ANTHROPIC_API_KEY. No s'ha traduït res.\n"
              "Es poden omplir a mà a i18n/faq.yml, o donar d'alta el secret\n"
              "del repositori (el mateix que fa servir i18n-tradueix.yml).")
        return 0

    trad = carrega_traductor()
    model = args.model or trad.MODEL
    avisos = []

    for idioma in idiomes:
        lot = [(e, i) for e, i in falten if i == idioma]
        if not lot:
            continue
        # La pregunta i la resposta es tradueixen juntes, en el mateix
        # encàrrec: si van per separat, el model perd de vista que la segona
        # respon la primera i canvia el tractament pel camí.
        trossos = []
        for e, _ in lot:
            trossos.append(e["ca"]["q"])
            trossos.append(e["ca"]["r"])

        print(f"\nTraduint {len(lot)} preguntes al {idioma}…")
        traduits = trad.demana(trossos, idioma, model, clau)
        if len(traduits) != len(trossos):
            print(f"  El model ha tornat {len(traduits)} trossos i n'esperàvem "
                  f"{len(trossos)}. No es desa res del {idioma}.")
            continue
        avisos += trad.revisa_noms(trossos, traduits)

        for n, (e, _) in enumerate(lot):
            e[idioma] = {"q": traduits[n * 2], "r": traduits[n * 2 + 1]}

    with open(FONT, "w", encoding="utf-8") as f:
        yaml.safe_dump(dades, f, allow_unicode=True, sort_keys=False, width=88)

    print(f"\ni18n/faq.yml desat.")
    if avisos:
        print("\n  Noms propis perduts per la traducció, cal mirar-s'ho:")
        for a in avisos:
            print("    " + a)
    print("\n  Repassa-ho i, quan estigui bé:\n"
          "    python3 .github/scripts/generate-faq.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
