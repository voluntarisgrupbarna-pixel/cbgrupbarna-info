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
import functools
import json
import re
import sys
from pathlib import Path

import yaml

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
# Rutes relatives: src="img/foto.jpg" dins de /cistella-petita/ apunta a
# /cistella-petita/img/foto.jpg, però la mateixa línia dins de
# /es/cistella-petita/ apuntaria a /es/cistella-petita/img/foto.jpg, que no
# existeix. Es passen a absolutes abans de moure la pàgina de carpeta.
RE_RELATIU = re.compile(
    r'((?:src|href|poster|data-src)=["\'])(?!https?:|//|/|#|mailto:|tel:|data:|javascript:)'
    r'([^"\']+)(["\'])', re.I)
RE_CHROME_NAV = re.compile(r'(?is)<nav class="head-nav".*?</nav>')
# El peu, sol. No es pot demanar que vagi enganxat a </main> i a </body>:
# hi ha pàgines amb un <script> entremig i llavors no es reconeixeria, i el
# que quedaria publicat seria el peu català amb els enllaços reescrits.
RE_CHROME_FOOT = re.compile(r'(?is)<footer class="foot">.*?</footer>')
RE_SKIP = re.compile(r'(?is)(<a href="#main" class="skip">)(.*?)(</a>)')
RE_LD = re.compile(r'(?is)(<script[^>]*ld\+json[^>]*>)(.*?)(</script>)')
RE_ALTERNATE = re.compile(
    r'[ \t]*<link[^>]+rel=["\']alternate["\'][^>]*hreflang=["\'][^"\']+["\'][^>]*>[ \t]*\n?', re.I)


@functools.lru_cache(maxsize=1)
def _mapa_rutes():
    mapa = yaml.safe_load((ROOT / "i18n" / "routes.yml").read_text(encoding="utf-8")) or {}
    return {g["ca"]: g for g in mapa.get("rutes", []) if g.get("ca")}


def desti_del_mapa(ruta, idioma):
    """On viu la traducció d'aquesta pàgina, segons i18n/routes.yml."""
    return _mapa_rutes().get(ruta, {}).get(idioma)


def fitxer_de(url):
    resta = url.lstrip("/")
    return ROOT / (resta + "index.html" if url.endswith("/") else resta)


def per_camins(dades, cami, valor):
    node = dades
    for tros in cami[:-1]:
        node = node[tros]
    node[cami[-1]] = valor


MARCA_COMMUTADOR = "<!--i18n:commutador-->"


def absolutitza(html, ruta):
    """Les rutes relatives, a absolutes des d'on era la pàgina catalana."""
    base = ruta if ruta.endswith("/") else ruta.rsplit("/", 1)[0] + "/"
    return RE_RELATIU.sub(lambda m: m.group(1) + base + m.group(2) + m.group(3), html)


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
        # La ruta traduïda es LLEGEIX del mapa; només si no hi consta es prova
        # amb el prefix. Endevinant-la, /posicionament/ donava
        # /es/posicionament/, que no existeix, i l'enllaç es quedava apuntant
        # al català tot i que /es/posicionamiento/ sí que hi és.
        candidat = desti_del_mapa(ruta, idioma) or f"/{idioma}{ruta}"
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
    # L'inLanguage del JSON-LD s'escriu de tres maneres pel repositori i abans
    # només se'n traduïa una: la curta. Les pàgines generades del blog, dels
    # partners i de premsa fan servir la llarga ("ca-ES") i deien a Google que
    # la versió anglesa era en català; les portades fan servir una llista.
    # BCP-47: el castellà d'aquí és es-ES i l'anglès el servim com a en-US.
    llarg = {"ca": "ca-ES", "es": "es-ES", "en": "en-US"}[idioma]
    html = html.replace('"inLanguage": "ca"', f'"inLanguage": "{idioma}"')
    html = html.replace('"inLanguage":"ca"', f'"inLanguage":"{idioma}"')
    html = html.replace('"inLanguage": "ca-ES"', f'"inLanguage": "{llarg}"')
    html = html.replace('"inLanguage":"ca-ES"', f'"inLanguage":"{llarg}"')
    # La llista sencera només té sentit al node WebSite —el lloc sí que és
    # trilingüe—; a una pàgina concreta hi va el seu idioma i prou. Es fa
    # llegint el JSON, no amb una expressió regular, per no tocar el WebSite.
    def _idioma_del_jsonld(m):
        cos = m.group(1)
        if '"inLanguage"' not in cos:
            return m.group(0)
        try:
            dades = json.loads(cos)
        except ValueError:
            return m.group(0)

        canviat = [False]

        def recorre(node):
            if isinstance(node, dict):
                if isinstance(node.get("inLanguage"), list) and node.get("@type") != "WebSite":
                    node["inLanguage"] = llarg
                    canviat[0] = True
                for valor in node.values():
                    recorre(valor)
            elif isinstance(node, list):
                for valor in node:
                    recorre(valor)

        recorre(dades)
        if not canviat[0]:
            return m.group(0)
        return m.group(0).replace(cos, json.dumps(dades, ensure_ascii=False, indent=2))

    html = re.sub(r'(?s)<script[^>]*ld\+json[^>]*>(.*?)</script>', _idioma_del_jsonld, html)

    # 4. Les adreces pròpies: canonical, og:url i les de dins del JSON-LD.
    #
    # Els hreflang es treuen abans, i no es toquen: si es deixessin, el canvi
    # d'adreça d'aquesta línia se'ls emportaria també i la versió catalana
    # acabaria dient que la seva pàgina en català és la castellana. Els
    # torna a escriure scripts/i18n-hreflang.py des del mapa, que és qui sap
    # com es diu cada versió.
    html = RE_ALTERNATE.sub("", html)
    html = html.replace(SITE + ruta, SITE + f"/{idioma}{ruta}")

    # 5. Les rutes relatives i després els enllaços interns.
    html = absolutitza(html, ruta)

    # El commutador d'idioma queda fora de la traducció d'enllaços. És l'únic
    # lloc de la pàgina on un enllaç a la versió CATALANA hi és a propòsit: si
    # el deixéssim passar per tradueix_enllacos, el «CA» acabaria apuntant a la
    # pàgina castellana i totes tres pestanyes anirien al mateix lloc. Es guarda
    # sencer, es tradueix la resta, i es torna a posar marcant l'idioma d'ara.
    # (Vist el 24/08/2026: /es/3x3/ i /es/premsa/ tenien el «CA» apuntant-se a
    # si mateixes i marcat com a actiu.)
    commutador = re.search(r'(?is)<(div|nav) class="lang-switch".*?</\1>', html)
    if commutador:
        html = html.replace(commutador.group(0), MARCA_COMMUTADOR, 1)

    html, sense_versio = tradueix_enllacos(html, idioma)

    if commutador:
        bloc = commutador.group(0)
        net = bloc.replace(' class="active"', '').replace(' aria-current="true"', '')
        net = re.sub(r'(<a [^>]*hreflang="' + idioma + r'"[^>]*)(>)',
                     r'\1 class="active" aria-current="true"\2', net, count=1)
        html = html.replace(MARCA_COMMUTADOR, net, 1)

    # 6. La capçalera i el peu, des del diccionari.
    html = RE_CHROME_NAV.sub(lambda m: navegacio(idioma).lstrip(), html, count=1)
    html = RE_SKIP.sub(lambda m: m.group(1) + text_diccionari("salta", idioma) + m.group(3), html)
    # L'escut i l'enllaç d'inici no són text visible i per això no s'extreuen
    # com a trossos: es quedaven en català a la pàgina traduïda, i qui fa
    # servir un lector de pantalla els sentia en un idioma que no és el seu.
    for clau, patro in (("escut_alt", r'(alt=")%s(")'),
                        ("inici_aria", r'(aria-label=")%s(")')):
        html = re.sub(patro % re.escape(text_diccionari(clau, "ca")),
                      lambda m: m.group(1) + text_diccionari(clau, idioma) + m.group(2),
                      html, count=1)
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
    ap.add_argument("--ruta-desti", help="ruta de la pàgina traduïda si no ha de dur el nom "
                                         "català: --ruta-desti /en/history/")
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
        # Una pàgina nova ha de néixer amb el nom que li toca. Renomenar-la
        # després vol dir deixar una redirecció enrere per sempre; fer-ho bé
        # ara no costa res, perquè encara no hi ha ningú que hi enllaci.
        #
        # Si el mapa ja diu on viu la traducció, mana el mapa: així el
        # workflow que refà una pàgina no la torna a deixar amb el nom
        # català al costat de la que ja té el nom traduït.
        desti_url = args.ruta_desti or desti_del_mapa(ruta, args.idioma) \
            or f"/{args.idioma}{ruta}"
        html = html.replace(SITE + f"/{args.idioma}{ruta}", SITE + desti_url)
        desti = fitxer_de(desti_url)
        print(f"  {desti_url}  ({len(html) // 1024} KB)"
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
