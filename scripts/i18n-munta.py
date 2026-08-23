#!/usr/bin/env python3
"""
Munta la pàgina traduïda a partir de la feina de i18n/feina/.

    python3 scripts/i18n-munta.py /club/ es
    python3 scripts/i18n-munta.py --tot es          # totes les que estiguin llestes

Agafa la pàgina catalana, hi posa cada tros traduït al seu lloc exacte i
arregla tot el que no és text i que una traducció no sap tocar:

  · L'atribut `lang` de l'<html> i l'`inLanguage` del JSON-LD.
  · El canonical, l'og:url i les adreces de dins del JSON-LD, que han
    d'apuntar a la pàgina nova i no a la catalana.
  · L'og:locale.
  · Els enllaços interns: /escoleta/ passa a ser /es/escoleta/ **només si
    /es/escoleta/ existeix**. Si aquella pàgina encara no està traduïda,
    l'enllaç es queda apuntant a la catalana, que és millor que un 404.
  · La capçalera i el peu, que es tornen a dibuixar des del diccionari.

L'estructura de l'HTML no la toca ningú: el que s'ha mogut d'aquí és text i
el que torna és text. Per això una traducció no pot trencar la pàgina.

Després cal refer el mapa, els hreflang i el sitemap:

    python3 scripts/i18n-routes.py && python3 scripts/i18n-hreflang.py \\
        && python3 scripts/build-sitemap.py
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util as _u                                       # noqa: E402
from i18n_chrome import navegacio, peu, text as text_diccionari   # noqa: E402

# L'extractor s'importa a mà perquè el seu nom porta guions.
_spec = _u.spec_from_file_location("extreu", Path(__file__).resolve().parent / "i18n-extreu.py")
_extreu = _u.module_from_spec(_spec)
_spec.loader.exec_module(_extreu)

ROOT = Path(__file__).resolve().parents[1]
FEINA = ROOT / "i18n" / "feina"
SITE = "https://cbgrupbarna.info"
LOCALE = {"ca": "ca_ES", "es": "es_ES", "en": "en_US"}

RE_HTML_LANG = re.compile(r'(<html[^>]*\blang=["\'])([^"\']*)(["\'])', re.I)
RE_OG_LOCALE = re.compile(r'(<meta[^>]+property=["\']og:locale["\'][^>]+content=["\'])([^"\']*)(["\'])', re.I)
RE_ENLLAC = re.compile(r'((?:href|action)=["\'])(/[^"\'#?]*)([^"\']*)(["\'])', re.I)
RE_CHROME_NAV = re.compile(r'(?is)<nav class="head-nav".*?</nav>')
# El peu, sol. No es pot demanar que vagi enganxat a </main> i a </body>:
# hi ha pàgines amb un <script> entremig i llavors no es reconeixeria, i el
# que quedaria publicat seria el peu català amb els enllaços reescrits.
RE_CHROME_FOOT = re.compile(r'(?is)<footer class="foot">.*?</footer>')
RE_SKIP = re.compile(r'(?is)(<a href="#main" class="skip">)(.*?)(</a>)')
RE_LD = re.compile(r'(?is)(<script[^>]*ld\+json[^>]*>)(.*?)(</script>)')


def fitxer_de(url):
    resta = url.lstrip("/")
    return ROOT / (resta + "index.html" if url.endswith("/") else resta)


def per_camins(dades, cami, valor):
    node = dades
    for tros in cami[:-1]:
        node = node[tros]
    node[cami[-1]] = valor


def tradueix_enllacos(html, idioma):
    """Els enllaços interns, cap a la versió traduïda quan n'hi ha."""
    sense = set()

    def canvia(m):
        obre, ruta, cua, tanca = m.groups()
        if ruta.startswith(("/es/", "/en/")):
            return m.group(0)
        # Fitxers (imatges, PDF, .ics) i rutes tècniques no tenen versió.
        if re.search(r"\.[a-z0-9]{2,5}$", ruta) and not ruta.endswith(".html"):
            return m.group(0)
        candidat = f"/{idioma}{ruta}"
        if fitxer_de(candidat).exists():
            return f"{obre}{candidat}{cua}{tanca}"
        sense.add(ruta)
        return m.group(0)

    return RE_ENLLAC.sub(canvia, html), sense


def munta(ruta, idioma):
    feina_fitxer = FEINA / idioma / ((ruta.strip("/").replace("/", "__") or "portada") + ".json")
    if not feina_fitxer.exists():
        return None, f"no hi ha feina a {feina_fitxer.relative_to(ROOT)}"
    feina = json.loads(feina_fitxer.read_text(encoding="utf-8"))
    buits = [t["id"] for t in feina["trossos"] if not t.get(idioma, "").strip()]
    if buits:
        return None, f"{len(buits)} trossos sense traduir ({', '.join(buits[:5])}…)"

    html = fitxer_de(ruta).read_text(encoding="utf-8")

    # Les posicions es tornen a calcular ARA, sobre la pàgina catalana tal com
    # és en aquest moment. Les que hi ha desades a la feina són de quan es va
    # extreure, i qualsevol canvi posterior —afegir-hi un hreflang, per
    # exemple— les mou totes: aplicar-les a cegues escriuria la traducció al
    # mig d'un atribut. La feina aporta el text traduït; l'ordre i la posició,
    # la pàgina d'ara.
    ara = _extreu.extreu(html)
    if [t["ca"] for t in ara] != [t["ca"] for t in feina["trossos"]]:
        return None, ("la pàgina catalana ha canviat des que es va extreure "
                      f"({len(ara)} trossos ara, {len(feina['trossos'])} a la feina). "
                      f"Torna a executar:  python3 scripts/i18n-extreu.py {ruta} {idioma}")
    trossos = [dict(nou, **{idioma: vell[idioma]})
               for nou, vell in zip(ara, feina["trossos"])]

    # 1. El JSON-LD, clau per clau, abans de tocar les posicions del text.
    per_ld = {}
    for t in trossos:
        if t["tipus"] == "json-ld":
            per_ld.setdefault(t["json_ld"], []).append(t)
    if per_ld:
        def canvia_ld(m):
            trossets = per_ld.get(m.start(2))
            if not trossets:
                return m.group(0)
            dades = json.loads(m.group(2))
            for t in trossets:
                per_camins(dades, t["cami"], t[idioma])
            return m.group(1) + json.dumps(dades, ensure_ascii=False, indent=2) + m.group(3)
        html = RE_LD.sub(canvia_ld, html)

    # 2. El text i els atributs, de darrere cap endavant perquè les posicions
    #    de davant no es moguin a mesura que se'n canvia la llargada.
    #    (El JSON-LD ja no hi és: les seves posicions han canviat i per això
    #    va primer, amb un mecanisme que no depèn de comptar caràcters.)
    catala = fitxer_de(ruta).read_text(encoding="utf-8")
    plans = sorted((t for t in trossos if t["tipus"] != "json-ld"),
                   key=lambda t: t["de"], reverse=True)
    if per_ld:
        # Si s'ha tocat el JSON-LD, les posicions ja no valen: es refà des del
        # català i s'hi torna a aplicar el JSON-LD al final.
        cos = catala
        for t in plans:
            cos = cos[:t["de"]] + t[idioma] + cos[t["a"]:]
        for m in RE_LD.finditer(catala):
            trossets = per_ld.get(m.start(2))
            if not trossets:
                continue
            dades = json.loads(m.group(2))
            for t in trossets:
                per_camins(dades, t["cami"], t[idioma])
            cos = cos.replace(m.group(2), json.dumps(dades, ensure_ascii=False, indent=2))
        html = cos
    else:
        for t in plans:
            html = html[:t["de"]] + t[idioma] + html[t["a"]:]

    # 3. L'idioma de la pàgina.
    html = RE_HTML_LANG.sub(lambda m: m.group(1) + idioma + m.group(3), html, count=1)
    html = RE_OG_LOCALE.sub(lambda m: m.group(1) + LOCALE[idioma] + m.group(3), html)
    html = html.replace('"inLanguage": "ca"', f'"inLanguage": "{idioma}"')

    # 4. Les adreces pròpies: canonical, og:url i les de dins del JSON-LD.
    html = html.replace(SITE + ruta, SITE + f"/{idioma}{ruta}")

    # 5. Els enllaços interns.
    html, sense_versio = tradueix_enllacos(html, idioma)

    # 6. La capçalera i el peu, des del diccionari.
    html = RE_CHROME_NAV.sub(lambda m: navegacio(idioma).lstrip(), html, count=1)
    html = RE_SKIP.sub(lambda m: m.group(1) + text_diccionari("salta", idioma) + m.group(3), html)
    peu_sol = re.search(r'(?is)<footer class="foot">.*</footer>', peu(idioma)).group(0)
    if RE_CHROME_FOOT.search(html):
        html = RE_CHROME_FOOT.sub(lambda _: peu_sol, html, count=1)
    else:
        print(f"  avís: {ruta} no té un <footer class=\"foot\">; el peu s'ha deixat com era")

    return (html, sense_versio), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ruta", nargs="?", help="ruta catalana, p. ex. /club/")
    ap.add_argument("idioma", choices=["es", "en"])
    ap.add_argument("--tot", action="store_true", help="totes les que tinguin la feina feta")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.tot:
        rutes = [json.loads(f.read_text(encoding="utf-8"))["origen"]
                 for f in sorted((FEINA / args.idioma).glob("*.json"))]
    elif args.ruta:
        rutes = [args.ruta]
    else:
        print("Cal una ruta, o --tot")
        return 1

    fets, pendents = 0, []
    for ruta in rutes:
        resultat, error = munta(ruta, args.idioma)
        if error:
            pendents.append(f"{ruta}: {error}")
            continue
        html, sense_versio = resultat
        desti = fitxer_de(f"/{args.idioma}{ruta}")
        print(f"  /{args.idioma}{ruta}  ({len(html) // 1024} KB)"
              + (f" · {len(sense_versio)} enllaços encara cap al català" if sense_versio else ""))
        if not args.dry_run:
            desti.parent.mkdir(parents=True, exist_ok=True)
            desti.write_text(html, encoding="utf-8")
        fets += 1

    print(f"\n{fets} pàgines muntades" + (" (no s'ha desat res)" if args.dry_run else ""))
    for p in pendents:
        print(f"  pendent · {p}")
    if fets and not args.dry_run:
        print("\nAra toca:  python3 scripts/i18n-routes.py && python3 scripts/i18n-hreflang.py"
              " && python3 scripts/build-sitemap.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
