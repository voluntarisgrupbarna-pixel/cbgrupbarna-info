#!/usr/bin/env python3
"""
Construeix i refresca i18n/routes.yml: el mapa de quina pàgina catalana
correspon a quina castellana i a quina anglesa.

    python3 scripts/i18n-routes.py           # refresca el mapa
    python3 scripts/i18n-routes.py --dry-run # només diu què canviaria

Per què cal. Fins ara aquesta correspondència no vivia enlloc. Estava
escampada en dos llocs incòmodes: els <link rel="alternate"> de cada pàgina
—escrits a mà, article per article— i la coincidència de ruta, que funciona
per a /campus/ però no per a /proteccio-menor/, que en anglès es diu
/en/child-protection/. Resultat: ningú podia respondre "quines pàgines no
estan traduïdes?" sense obrir-les una a una.

D'aquest fitxer en surten després els hreflang, el commutador d'idioma i el
sitemap, i és el que llegeix scripts/i18n-lint.py per saber què hi falta.

Com dedueix les parelles, en aquest ordre:

  1. Els hreflang que la pàgina ja declara, i també els que una pàgina en
     castellà o anglès declara apuntant a la catalana. Són la font més
     fiable: algú els va escriure expressament.
  2. La mateixa ruta sota /es/ i /en/.
  3. Res. L'entrada queda amb `null` i el lint la comptarà com a pendent.

El fitxer es pot editar a mà, i les edicions manen: aquest script no
sobreescriu mai una parella escrita per una persona. Només afegeix pàgines
noves i corregeix les que apunten a un fitxer que ja no existeix. Per dir
"aquesta pàgina no es traduirà mai", posa-hi `es: null` amb un `nota:` al
costat; s'hi mantindrà.
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAPA = ROOT / "i18n" / "routes.yml"
IDIOMES = ("ca", "es", "en")

# Les mateixes rutes que robots.txt manté fora de l'índex, i que
# scripts/build-sitemap.py ja exclou. Aquí valen igual: un panell d'admin o
# un cartell d'impressió no té versió en anglès ni l'ha de tenir.
EXCLOU = re.compile(
    r"(^|/)(admin\.html|token\.html|app\.html|estadistiques\.html|404\.html)$"
    r"|/admin/|/print/|/cartell\.html$|migrar-flickr"
)

RE_REDIRECCIO = re.compile(r'<meta[^>]+http-equiv=["\']refresh["\']', re.I)
RE_ALTERNATE = re.compile(
    r'<link[^>]+rel=["\']alternate["\'][^>]*hreflang=["\']([^"\']+)["\'][^>]*href=["\']([^"\']+)["\']',
    re.I,
)
SITE = "https://cbgrupbarna.info"


def url_de(fitxer):
    """Ruta del fitxer → URL pública, amb barra final i sense index.html."""
    rel = fitxer.relative_to(ROOT).as_posix()
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    if rel == "index.html":
        return "/"
    return "/" + rel


def idioma_de(url):
    if url.startswith("/es/"):
        return "es"
    if url.startswith("/en/"):
        return "en"
    return "ca"


def sense_prefix(url):
    """/es/campus/ → /campus/. La clau amb què s'aparellen per ruta."""
    return re.sub(r"^/(es|en)/", "/", url)


def pagines():
    """Totes les URLs públiques del lloc, per idioma."""
    fora = {"ca": set(), "es": set(), "en": set()}
    for fitxer in sorted(ROOT.rglob("*.html")):
        rel = fitxer.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", "galeria/node_modules/", "tests/")):
            continue
        url = url_de(fitxer)
        if EXCLOU.search(url):
            continue
        # Una adreça vella que només porta a la nova (i18n/renoms.yml) no és
        # una pàgina: si comptés, sortiria al mapa com a òrfena per sempre.
        if RE_REDIRECCIO.search(fitxer.read_text(encoding="utf-8", errors="ignore")):
            continue
        fora[idioma_de(url)].add(url)
    return fora


def fitxer_de(url):
    resta = url.lstrip("/")
    return ROOT / (resta + "index.html" if url.endswith("/") else resta)


def alternates_declarats(url):
    """Els hreflang que la pàgina porta escrits, com a {idioma: url}."""
    fitxer = fitxer_de(url)
    if not fitxer.exists():
        return {}
    text = fitxer.read_text(encoding="utf-8", errors="ignore")
    trobats = {}
    for codi, href in RE_ALTERNATE.findall(text):
        codi = codi.lower()
        if codi in IDIOMES:
            trobats[codi] = href.replace(SITE, "") or "/"
    return trobats


def construeix():
    totes = pagines()
    existents = {i: set(totes[i]) for i in IDIOMES}

    # Els hreflang de tot el lloc, llegits una sola vegada. Serveixen en les
    # dues direccions: la pàgina catalana que anomena la seva traducció, i la
    # traducció que anomena la catalana — que és com es troben les parelles
    # amb el nom canviat, com /proteccio-menor/ i /en/child-protection/.
    declarats = {u: alternates_declarats(u) for i in IDIOMES for u in totes[i]}
    inversos = {"es": {}, "en": {}}
    for idioma in ("es", "en"):
        for url in totes[idioma]:
            ca_declarat = declarats[url].get("ca")
            if ca_declarat in existents["ca"]:
                inversos[idioma].setdefault(ca_declarat, url)

    # El mapa que ja hi ha, si n'hi ha. Les entrades manuals no es toquen.
    previ = {}
    if MAPA.exists():
        dades = yaml.safe_load(MAPA.read_text(encoding="utf-8")) or {}
        for entrada in dades.get("rutes", []):
            previ[entrada["ca"]] = entrada

    rutes, avisos = [], []
    for ca in sorted(totes["ca"]):
        entrada = dict(previ.get(ca) or {})
        entrada["ca"] = ca
        for idioma in ("es", "en"):
            # Una parella escrita a mà mana, tret que el fitxer hagi desaparegut.
            anterior = entrada.get(idioma)
            if anterior and anterior in existents[idioma]:
                continue
            if anterior and anterior not in existents[idioma]:
                avisos.append(f"{ca}: {idioma} apuntava a {anterior}, que ja no hi és")
            if ca in previ and idioma in previ[ca] and previ[ca][idioma] is None \
                    and previ[ca].get("nota"):
                entrada[idioma] = None   # declarada expressament com a no traduïble
                continue

            declarat = declarats[ca].get(idioma) or inversos[idioma].get(ca)
            if declarat and declarat in existents[idioma]:
                entrada[idioma] = declarat
                continue
            per_ruta = f"/{idioma}{ca}"
            entrada[idioma] = per_ruta if per_ruta in existents[idioma] else None
        rutes.append({k: entrada[k] for k in ("ca", "es", "en") if k in entrada}
                     | ({"nota": entrada["nota"]} if entrada.get("nota") else {}))

    # Pàgines en castellà o anglès que no pengen de cap catalana: o són
    # òrfenes, o la seva parella té un altre nom i cal escriure-la a mà.
    aparellades = {i: {r.get(i) for r in rutes} for i in ("es", "en")}
    orfes = {i: sorted(existents[i] - aparellades[i]) for i in ("es", "en")}
    return rutes, orfes, avisos


CAPCALERA = """\
# Mapa d'idiomes de cbgrupbarna.info — quina pàgina és quina en cada idioma.
#
# El genera scripts/i18n-routes.py i el llegeix scripts/i18n-lint.py. D'aquí
# n'han de sortir, més endavant, els hreflang i el commutador d'idioma, que
# ara s'escriuen a mà pàgina per pàgina.
#
# ES EDITA A MÀ i les edicions manen: l'script no sobreescriu mai una parella
# que hi hagi escrita, només afegeix pàgines noves i avisa de les que apunten
# a un fitxer que ja no existeix.
#
#   - ca: /proteccio-menor/
#     es: /es/proteccion-menor/
#     en: /en/child-protection/     ← ruta diferent: només es pot saber d'aquí
#
# `null` vol dir "encara no traduïda" i el lint la compta com a pendent. Si
# una pàgina no s'ha de traduir mai, posa-hi `null` amb una `nota:` al
# costat: amb la nota, l'script la respecta i el lint la deixa estar.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="no desa res")
    args = ap.parse_args()

    rutes, orfes, avisos = construeix()
    dades = {"rutes": rutes}
    if any(orfes.values()):
        dades["orfes"] = {i: v for i, v in orfes.items() if v}

    sortida = CAPCALERA + yaml.safe_dump(
        dades, allow_unicode=True, sort_keys=False, default_flow_style=False, width=200)

    pendents = {i: sum(1 for r in rutes if r.get(i) is None) for i in ("es", "en")}
    print(f"{len(rutes)} pàgines catalanes")
    print(f"  sense castellà: {pendents['es']}")
    print(f"  sense anglès:   {pendents['en']}")
    for idioma, llista in orfes.items():
        if llista:
            print(f"  òrfenes en {idioma}: {len(llista)} (sense parella catalana)")
    for avis in avisos:
        print(f"  · {avis}")

    if args.dry_run:
        canvia = not MAPA.exists() or MAPA.read_text(encoding="utf-8") != sortida
        print("\nEl mapa canviaria." if canvia else "\nEl mapa ja està al dia.")
        return 0
    MAPA.parent.mkdir(exist_ok=True)
    MAPA.write_text(sortida, encoding="utf-8")
    print(f"\nDesat a {MAPA.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
