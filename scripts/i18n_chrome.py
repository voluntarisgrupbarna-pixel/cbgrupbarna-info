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
SITE = "https://linksbio.cbgrupbarna.info"

_dades = yaml.safe_load(DICCIONARI.read_text(encoding="utf-8"))
TEXTOS = _dades["textos"]
ESTRUCTURA = _dades["estructura"]

# Japonès i coreà: només tenen les presentacions. El vocabulari va a part
# (i18n/diccionari-cjk.yml) i l'estructura de menú i peu és la de l'anglès.
CJK = ("ja", "ko", "de", "it", "nl", "fr", "ar", "tr", "pt")   # idiomes sense pàgines pròpies: enllacen a l'anglès
_cjk = yaml.safe_load((ROOT / "i18n" / "diccionari-cjk.yml").read_text(encoding="utf-8"))
_ar = yaml.safe_load((ROOT / "i18n" / "diccionari-ar.yml").read_text(encoding="utf-8"))
_eur = yaml.safe_load((ROOT / "i18n" / "diccionari-eur.yml").read_text(encoding="utf-8"))
_trpt = yaml.safe_load((ROOT / "i18n" / "diccionari-trpt.yml").read_text(encoding="utf-8"))
for _clau, _valors in _cjk["textos"].items():
    TEXTOS[_clau].update(_valors)
    TEXTOS[_clau].update(_eur["textos"][_clau])
    TEXTOS[_clau].update(_ar["textos"][_clau])
    TEXTOS[_clau].update(_trpt["textos"][_clau])
for _idioma in CJK:
    ESTRUCTURA[_idioma] = ESTRUCTURA["en"]


def text(clau, idioma):
    entrada = TEXTOS.get(clau)
    if entrada is None:
        raise KeyError(f"i18n: la clau «{clau}» no és al diccionari")
    if idioma not in entrada:
        raise KeyError(f"i18n: «{clau}» no té versió en {idioma}")
    return entrada[idioma]


def enllac(clau, idioma):
    """L'adreça d'una clau en un idioma, amb el prefix que li toca.

    La regla general és que la traducció viu a /es/ o /en/ amb la mateixa
    adreça. Les pàgines que tenen l'adreça traduïda —les legals, per exemple:
    /avis-legal/ és /es/aviso-legal/ i /en/legal-notice/— ho diuen amb un
    `href_es` o `href_en` propi al diccionari, que es fa servir tal com és.
    """
    if idioma != "ca":
        propi = TEXTOS[clau].get(f"href_{idioma}")
        if propi:
            return propi
    href = TEXTOS[clau].get("href")
    if href is None:
        raise KeyError(f"i18n: la clau «{clau}» no és un enllaç")
    if idioma == "ca" or href.startswith(("http", "mailto:")):
        return href
    if idioma in CJK:
        # Pàgina en ja/ko si n'hi ha; si no, l'anglesa. Mai un 404.
        propi = f"/{idioma}{href}"
        if _existeix(propi):
            return propi
        return TEXTOS[clau].get("href_en") or f"/en{href}"
    return f"/{idioma}{href}"


def _existeix(href):
    ruta = href.split("#")[0]
    if not ruta:
        return True
    return (ROOT / (ruta.lstrip("/") + "index.html" if ruta.endswith("/") else ruta.lstrip("/"))).exists()


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
           "Un correu la setmana amb el que val la pena saber. Res més.", "/newsletter/"),
    "es": ("Sigue al CB Grup Barna", "Síguenos en Instagram",
           "@cbgrupbarna · el día a día del club, cada semana.",
           "Apúntate a la newsletter",
           "Un correo a la semana con lo que vale la pena saber. Nada más.", "/es/newsletter/"),
    "en": ("Follow CB Grup Barna", "Follow us on Instagram",
           "@cbgrupbarna · the club's week, as it happens.",
           "Join the newsletter",
           "One email a week with what's worth knowing. Nothing else.", "/en/newsletter/"),
    "ja": ("CB Grup Barnaをフォロー", "Instagramでフォロー",
           "@cbgrupbarna · クラブの毎日を、毎週お届けします。",
           "ニュースレターに登録",
           "知っておきたいことを週に1通。それだけです。", "/en/newsletter/"),
    "ko": ("CB Grup Barna 팔로우", "인스타그램에서 팔로우",
           "@cbgrupbarna · 클럽의 일상을 매주 전해 드립니다.",
           "뉴스레터 구독",
           "알아둘 만한 소식을 일주일에 한 통. 그게 전부입니다.", "/en/newsletter/"),
    "de": ("Folge dem CB Grup Barna", "Folge uns auf Instagram",
           "@cbgrupbarna · der Vereinsalltag, jede Woche.",
           "Newsletter abonnieren",
           "Eine E-Mail pro Woche mit dem, was man wissen sollte. Sonst nichts.", "/en/newsletter/"),
    "it": ("Segui il CB Grup Barna", "Seguici su Instagram",
           "@cbgrupbarna · la vita del club, ogni settimana.",
           "Iscriviti alla newsletter",
           "Una email a settimana con ciò che vale la pena sapere. Nient'altro.", "/en/newsletter/"),
    "nl": ("Volg CB Grup Barna", "Volg ons op Instagram",
           "@cbgrupbarna · het clubleven, elke week.",
           "Schrijf je in voor de nieuwsbrief",
           "Eén e-mail per week met wat het weten waard is. Niets meer.", "/en/newsletter/"),
    "fr": ("Suivez le CB Grup Barna", "Suivez-nous sur Instagram",
           "@cbgrupbarna · la vie du club, chaque semaine.",
           "Abonnez-vous à la newsletter",
           "Un e-mail par semaine avec ce qui vaut la peine d'être su. Rien de plus.", "/en/newsletter/"),
    "tr": ("CB Grup Barna'yı takip edin", "Instagram'da bizi takip edin",
           "@cbgrupbarna · kulübün hayatı, her hafta.",
           "Bültene abone olun",
           "Haftada bir e-posta, bilmeye değer olanlarla. Başka hiçbir şey.", "/en/newsletter/"),
    "pt": ("Siga o CB Grup Barna", "Siga-nos no Instagram",
           "@cbgrupbarna · o dia a dia do clube, todas as semanas.",
           "Subscreva a newsletter",
           "Um e-mail por semana com o que vale a pena saber. Mais nada.", "/en/newsletter/"),
    "ar": ("تابع CB Grup Barna", "تابعنا على إنستغرام",
           "@cbgrupbarna · حياة النادي كل أسبوع.",
           "اشترك في النشرة البريدية",
           "رسالة واحدة في الأسبوع بما يستحق المعرفة. لا شيء آخر.", "/en/newsletter/"),
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


A11Y_ETIQUETA = {
    "ca": "Accessibilitat — WCAG 2.2 AA",
    "es": "Accesibilidad — WCAG 2.2 AA",
    "en": "Accessibility — WCAG 2.2 AA",
    "ja": "アクセシビリティ — WCAG 2.2 AA",
    "ko": "접근성 — WCAG 2.2 AA",
    "de": "Barrierefreiheit — WCAG 2.2 AA",
    "it": "Accessibilità — WCAG 2.2 AA",
    "nl": "Toegankelijkheid — WCAG 2.2 AA",
    "fr": "Accessibilité — WCAG 2.2 AA",
    "ar": "إمكانية الوصول — WCAG 2.2 AA",
    "tr": "Erişilebilirlik — WCAG 2.2 AA",
    "pt": "Acessibilidade — WCAG 2.2 AA",
}


def _enllac_peu(clau, idioma):
    """Un enllaç normal del peu. El d'accessibilitat porta a més la icona i
    el nivell de conformitat: és l'única prova visible que el lloc compleix
    WCAG 2.2 AA, i val la pena que es vegi sense haver-hi de clicar."""
    href = _comprova(clau, idioma)
    if clau == "accessibilitat":
        return (f'<a href="{href}" class="foot-a11y">'
                 '<span class="foot-a11y-i" aria-hidden="true">&#9855;</span>'
                 f'{A11Y_ETIQUETA[idioma]}</a>')
    return f'<a href="{href}">{text(clau, idioma)}</a>'


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
            f'        {_enllac_peu(c, idioma)}' for c in claus)
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
            '    </div>\n  </div>\n</footer>\n'
            '<script src="/js/cerca.js" defer></script>\n'
            '<script src="/js/mapa.js" defer></script>\n'
            '</body>\n</html>\n')


def alternatives(url):
    """Les traduccions d'una pàgina, tal com les vol head(): una llista de
    (codi d'idioma, adreça absoluta), amb x-default al final.

    Surten de i18n/routes.yml, que és qui sap quina pàgina és quina en cada
    idioma. Abans cada article portava aquesta llista escrita a mà al costat,
    i per això n'hi havia que apuntaven a pàgines que ja no existien.
    """
    mapa = yaml.safe_load((ROOT / "i18n" / "routes.yml").read_text(encoding="utf-8")) or {}
    for grup in mapa.get("rutes", []):
        if url not in (grup.get(i) for i in ("ca", "es", "en", "ja", "ko", "de", "it", "nl", "fr", "ar", "tr", "pt")):
            continue
        llista = [(idioma, SITE + grup[idioma])
                  for idioma in ("ca", "es", "en", "ja", "ko", "de", "it", "nl", "fr", "ar", "tr", "pt") if grup.get(idioma)]
        if len(llista) == 1:
            return []          # sense traduccions no cal declarar res
        return llista + [("x-default", SITE + grup["ca"])]
    return []


if __name__ == "__main__":
    for idioma in ("ca", "es", "en"):
        print(f"── {idioma} " + "─" * 60)
        print(navegacio(idioma))
        print(peu(idioma))
