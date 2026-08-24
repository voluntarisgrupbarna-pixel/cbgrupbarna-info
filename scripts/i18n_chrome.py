#!/usr/bin/env python3
"""
Capçalera i peu de pàgina, dibuixats des de i18n/diccionari.yml.

Fins ara aquests textos vivien escrits tres vegades, una per idioma, i a més
d'un lloc: dins de scripts/build-pages.py i a disc, pàgina per pàgina. Per
això el mateix enllaç va acabar dient-se «Team calendars» en una pàgina i
«Calendars by team» en una altra. Aquí cada text té una clau i tres valors.

    from i18n_chrome import navegacio, peu
    navegacio("ca")   # el <nav> de la capçalera
    peu("en")         # el <footer> sencer

Les rutes s'escriuen en català i cada idioma hi posa el seu prefix:
/escoleta/ és /es/escoleta/ i /en/escoleta/. Si una pàgina no existeix en un
idioma, el diccionari no l'ha de llistar a la seva estructura, i si ho fa,
això peta expressament: val més que s'aturi la generació que no pas publicar
un peu en castellà amb un enllaç que porta a una pàgina en català.
"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DICCIONARI = ROOT / "i18n" / "diccionari.yml"
SITE = "https://cbgrupbarna.info"

_dades = yaml.safe_load(DICCIONARI.read_text(encoding="utf-8"))
TEXTOS = _dades["textos"]
ESTRUCTURA = _dades["estructura"]


def text(clau, idioma):
    entrada = TEXTOS.get(clau)
    if entrada is None:
        raise KeyError(f"i18n: la clau «{clau}» no és al diccionari")
    if idioma not in entrada:
        raise KeyError(f"i18n: «{clau}» no té versió en {idioma}")
    return entrada[idioma]


def enllac(clau, idioma):
    """L'adreça d'una clau en un idioma, amb el prefix que li toca."""
    href = TEXTOS[clau].get("href")
    if href is None:
        raise KeyError(f"i18n: la clau «{clau}» no és un enllaç")
    if idioma == "ca" or href.startswith(("http", "mailto:")):
        return href
    return f"/{idioma}{href}"


def _comprova(clau, idioma):
    """Que l'enllaç porti a una pàgina que existeix de debò."""
    href = enllac(clau, idioma)
    if href.startswith(("http", "mailto:")):
        return href
    ruta = href.split("#")[0]
    if not ruta:
        return href
    fitxer = ROOT / (ruta.lstrip("/") + "index.html" if ruta.endswith("/") else ruta.lstrip("/"))
    if not fitxer.exists():
        raise FileNotFoundError(
            f"i18n: el peu de {idioma} enllaça {href} i aquesta pàgina no existeix. "
            f"O es tradueix la pàgina, o es treu la clau «{clau}» de l'estructura de {idioma}.")
    return href


def navegacio(idioma):
    """El <nav> de la capçalera. El sufix .opt d'una clau marca els enllaços
    secundaris, que són els primers que cauen quan el menú no hi cap."""
    linies = []
    for clau in ESTRUCTURA[idioma]["nav"]:
        clau, _, opcional = clau.partition(".")
        classe = ' class="opt"' if opcional else ''
        linies.append(f'      <a href="{_comprova(clau, idioma)}"{classe}>{text(clau, idioma)}</a>')
    return (f'    <nav class="head-nav" aria-label="{text("nav_aria", idioma)}">\n'
            + "\n".join(linies) + "\n    </nav>")


CRIDA = {}
for _idioma, _t in {
    "ca": ("Segueix el CB Grup Barna", "Segueix-nos a Instagram",
           "@cbgrupbarna · el dia a dia del club, cada setmana.",
           "Apunta't a la newsletter",
           "Un correu al mes amb el que val la pena saber. Res més.", "/newsletter/"),
    "es": ("Sigue al CB Grup Barna", "Síguenos en Instagram",
           "@cbgrupbarna · el día a día del club, cada semana.",
           "Apúntate a la newsletter",
           "Un correo al mes con lo que vale la pena saber. Nada más.", "/es/newsletter/"),
    "en": ("Follow CB Grup Barna", "Follow us on Instagram",
           "@cbgrupbarna · the club's week, as it happens.",
           "Join the newsletter",
           "One email a month with what's worth knowing. Nothing else.", "/en/newsletter/"),
}.items():
    _aria, _igt, _igs, _nlt, _nls, _nlurl = _t
    CRIDA[_idioma] = (
        "<!-- CRIDA DE COMUNITAT · scripts/crida-comunitat.py -->\n"
        f'<section class="comunitat" aria-label="{_aria}">\n'
        '  <div class="comunitat-in">\n'
        '    <a class="comunitat-porta" href="https://www.instagram.com/cbgrupbarna/"'
        ' target="_blank" rel="noopener" data-cta="crida-instagram">\n'
        f'      <span class="comunitat-t">{_igt}</span>\n'
        f'      <span class="comunitat-s">{_igs}</span>\n'
        '    </a>\n'
        f'    <a class="comunitat-porta comunitat-porta--red" href="{_nlurl}"'
        ' data-cta="crida-newsletter">\n'
        f'      <span class="comunitat-t">{_nlt}</span>\n'
        f'      <span class="comunitat-s">{_nls}</span>\n'
        '    </a>\n'
        '  </div>\n</section>\n'
        "<!-- /CRIDA DE COMUNITAT -->\n"
    )


def peu(idioma):
    """El <footer> sencer.

    Les tres primeres columnes surten del diccionari. Les dades de contacte i
    les xarxes no: un correu, un telèfon i una adreça són els mateixos en els
    tres idiomes, i posar-los al diccionari només afegiria tres còpies del
    mateix text a mantenir.
    """
    columnes = []
    for titol, claus in ESTRUCTURA[idioma]["peu"]:
        enllacos = "\n".join(
            f'        <a href="{_comprova(c, idioma)}">{text(c, idioma)}</a>' for c in claus)
        extra = ""
        if titol == "titol_contacte":
            extra = ('\n        <a href="mailto:marqueting@cbgrupbarna.info">'
                     'marqueting@cbgrupbarna.info</a>'
                     '\n        <a href="https://wa.me/34698425153">+34 698 425 153</a>'
                     '\n        <p>La Nau del Clot · Sant Martí<br>08018 Barcelona</p>')
        columnes.append('      <div class="foot-col">\n'
                        f'        <h3>{text(titol, idioma)}</h3>\n{enllacos}{extra}\n'
                        '      </div>')
    columnes.append(
        '      <div class="foot-col">\n'
        f'        <h3>{text("titol_xarxes", idioma)}</h3>\n'
        '        <a href="https://www.instagram.com/cbgrupbarna/" target="_blank" rel="noopener">Instagram</a>\n'
        '        <a href="https://www.tiktok.com/@cbgrupbarna" target="_blank" rel="noopener">TikTok</a>\n'
        '      </div>')
    # La crida de comunitat va abans del peu a totes les pàgines: la manté
    # scripts/crida-comunitat.py, i aquí s'emet ja posada perquè una pàgina
    # generada no neixi sense ella.
    crida = CRIDA[idioma]
    return ('</main>\n' + crida + '<footer class="foot">\n  <div class="wrap">\n    <div class="foot-grid">\n'
            + "\n".join(columnes) + '\n    </div>\n'
            '    <div class="foot-btm">\n'
            '      <div class="foot-mark">#Som<em>Clot</em></div>\n'
            f'      <div class="foot-legal">{text("peu_legal", idioma)}</div>\n'
            '    </div>\n  </div>\n</footer>\n</body>\n</html>\n')


def alternatives(url):
    """Les traduccions d'una pàgina, tal com les vol head(): una llista de
    (codi d'idioma, adreça absoluta), amb x-default al final.

    Surten de i18n/routes.yml, que és qui sap quina pàgina és quina en cada
    idioma. Abans cada article portava aquesta llista escrita a mà al costat,
    i per això n'hi havia que apuntaven a pàgines que ja no existien.
    """
    mapa = yaml.safe_load((ROOT / "i18n" / "routes.yml").read_text(encoding="utf-8")) or {}
    for grup in mapa.get("rutes", []):
        if url not in (grup.get("ca"), grup.get("es"), grup.get("en")):
            continue
        llista = [(idioma, SITE + grup[idioma])
                  for idioma in ("ca", "es", "en") if grup.get(idioma)]
        if len(llista) == 1:
            return []          # sense traduccions no cal declarar res
        return llista + [("x-default", SITE + grup["ca"])]
    return []


if __name__ == "__main__":
    for idioma in ("ca", "es", "en"):
        print(f"── {idioma} " + "─" * 60)
        print(navegacio(idioma))
        print(peu(idioma))
