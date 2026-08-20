#!/usr/bin/env python3
"""
Motor i18n del site. Genera les versions /es/ i /en/ d'una pàgina catalana
a partir d'un catàleg de traduccions, i hi injecta hreflang, canonical,
Open Graph i el selector d'idioma.

    python3 scripts/i18n.py extract <pagina>    # crea/actualitza el catàleg
    python3 scripts/i18n.py build [<pagina>…]   # genera /es/ i /en/
    python3 scripts/i18n.py check               # informe de cobertura

El catàleg viu a scripts/i18n/<slug>.json. Les claus són el text català
literal, de manera que si el català canvia la clau deixa d'existir i
`check` avisa que la traducció s'ha quedat obsoleta.

Les pàgines i el seu tier es declaren a PAGES. Tot el que no hi és queda
deliberadament només en català (vegeu README a scripts/i18n/README.md).
"""
import json
import os
import re
import sys
from urllib.parse import quote

import lxml.html as LH
from lxml import etree

BASE = 'https://cbgrupbarna.info'
CAT = 'scripts/i18n'

# slug -> (fitxer català, idiomes, prioritat sitemap)
PAGES = {
    'home':   ('index.html',        ('es', 'en'), '1.0'),
    'campus': ('campus/index.html', ('es', 'en'), '0.8'),
    '3x3':    ('3x3/index.html',    ('es', 'en'), '0.8'),
}

OG_LOCALE = {'ca': 'ca_ES', 'es': 'es_ES', 'en': 'en_GB'}
LABEL = {'ca': 'CA', 'es': 'ES', 'en': 'EN'}

# Elements el text dels quals mai s'ha de traduir (marques, dades, codi)
SKIP_TAGS = {'script', 'style', 'code', 'time'}
# Cadenes que són noms propis o dades i no s'han de tocar
KEEP = re.compile(
    r'^[\s·—\-–|/@#0-9.,:%€ºª+()]*$'          # només símbols o números
    r'|^(CB Grup Barna|Grup Barna|Instagram|TikTok|WhatsApp|FCBQ|ACB|FEB|LEB|NBA)$'
)


def slug_of(path):
    for s, (f, _, _) in PAGES.items():
        if f == path:
            return s
    raise SystemExit(f'pàgina no declarada a PAGES: {path}')


def urls_for(slug):
    src = PAGES[slug][0]
    d = '' if src == 'index.html' else src[:-len('index.html')]
    u = {'ca': f'{BASE}/{d}'}
    for lg in PAGES[slug][1]:
        u[lg] = f'{BASE}/{lg}/{d}'
    return u


def out_for(slug, lang):
    src = PAGES[slug][0]
    d = '' if src == 'index.html' else src[:-len('index.html')]
    return f'{lang}/{d}index.html'


# ---------------------------------------------------------------- extract
def translatable(doc):
    """Retorna la llista ordenada de cadenes catalanes traduïbles."""
    seen, out = set(), []

    def add(t):
        t = ' '.join((t or '').split())
        if not t or KEEP.match(t) or len(t) < 2 or t in seen:
            return
        seen.add(t)
        out.append(t)

    for el in doc.iter():
        if not isinstance(el.tag, str) or el.tag in SKIP_TAGS:
            continue
        add(el.text)
        add(el.tail)
        for a in ('alt', 'title', 'aria-label', 'placeholder', 'content', 'value'):
            if a in el.attrib and (el.tag != 'meta' or el.get('name') in
                                   ('description', 'keywords') or
                                   (el.get('property') or '').startswith('og:')):
                add(el.get(a))
    return out


def load_common():
    f = f'{CAT}/_common.json'
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else {}


def load_cat(slug):
    """Catàleg de la pàgina amb el comú com a base."""
    cat = dict(load_common())
    f = f'{CAT}/{slug}.json'
    if os.path.exists(f):
        cat.update(json.load(open(f, encoding='utf-8')))
    return cat


def cmd_extract(path):
    slug = slug_of(path)
    doc = LH.parse(path).getroot()
    strings = translatable(doc)
    common = load_common()
    f = f'{CAT}/{slug}.json'
    old = json.load(open(f, encoding='utf-8')) if os.path.exists(f) else {}
    cat = {}
    for s in strings:
        if s in common:      # ja resolta al catàleg compartit
            continue
        cat[s] = old.get(s, {'es': '', 'en': ''})
    os.makedirs(CAT, exist_ok=True)
    json.dump(cat, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    done = sum(1 for v in cat.values() if v.get('es') and v.get('en'))
    print(f'{f}: {len(cat)} cadenes · {done} traduïdes · {len(cat)-done} pendents')


# ---------------------------------------------------------------- build
def apply_lang(doc, cat, lang):
    def tr(t):
        k = ' '.join((t or '').split())
        v = cat.get(k, {}).get(lang)
        return v if v else None

    for el in doc.iter():
        if not isinstance(el.tag, str) or el.tag in SKIP_TAGS:
            continue
        for attr in ('text', 'tail'):
            v = getattr(el, attr)
            if v and v.strip():
                n = tr(v)
                if n:
                    lead = v[:len(v) - len(v.lstrip())]
                    trail = v[len(v.rstrip()):]
                    setattr(el, attr, lead + n + trail)
        for a in ('alt', 'title', 'aria-label', 'placeholder', 'content', 'value'):
            if a in el.attrib:
                n = tr(el.get(a))
                if n:
                    el.set(a, n)


LANGSEL_CSS = """
/* selector d'idioma · injectat per scripts/i18n.py */
.langsel{display:inline-flex;gap:4px;align-items:center;margin-left:14px;white-space:nowrap}
.langsel a{display:inline-flex;align-items:center;justify-content:center;
  min-height:30px;padding:0 8px;border:1px solid currentColor;border-radius:2px;
  font-size:10px;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;
  opacity:.55;line-height:1}
.langsel a:hover{opacity:1}
.langsel a[aria-current="true"]{opacity:1;background:#E31E24;border-color:#E31E24;color:#fff}
.langsel a::after{display:none!important}
@media (max-width:820px){.langsel{margin-left:8px}.langsel a{padding:0 6px;font-size:9px}}
/* en pantalles estretes el marc no hi cap: enllaços nus, separats per punt */
@media (max-width:560px){
  .langsel{gap:0;margin-left:6px}
  .langsel a{border:0;padding:0 4px;min-height:34px;font-size:10px;letter-spacing:.06em}
  .langsel a[aria-current="true"]{background:none;color:#E31E24}
  .langsel a+a{border-left:1px solid currentColor;border-radius:0}
}
"""


# Cadenes de cara a l'usuari que viuen dins de <script> (missatge de WhatsApp
# que munta el formulari). Es tradueixen per literal exacte, mai per patró:
# tota la resta del JS queda intacta.
JS_STRINGS = {
    '"Hola! Vull informació del CB Grup Barna.\\n\\n"': {
        'es': '"¡Hola! Quiero información del CB Grup Barna.\\n\\n"',
        'en': '"Hello! I would like information about CB Grup Barna.\\n\\n"'},
    '"Nom: "': {'es': '"Nombre: "', 'en': '"Name: "'},
    '"Mòbil: "': {'es': '"Móvil: "', 'en': '"Mobile: "'},
    '"Correu: "': {'es': '"Correo: "', 'en': '"Email: "'},
}
# Missatge prellistat dels enllaços wa.me / api.whatsapp.com, per idioma
WA_TEXT = {
    'Hola!%20Vull%20info%20del%20CB%20Grup%20Barna':
        {'es': '%C2%A1Hola!%20Quiero%20info%20del%20CB%20Grup%20Barna',
         'en': 'Hello!%20I%27d%20like%20info%20about%20CB%20Grup%20Barna'},
    'Hola!%20Vull%20informaci%C3%B3%20del%20club':
        {'es': '%C2%A1Hola!%20Quiero%20informaci%C3%B3n%20del%20club',
         'en': 'Hello!%20I%27d%20like%20information%20about%20the%20club'},
    'Hola%20Julio!%20Vull%20informaci%C3%B3%20de%20l%27Escoleta':
        {'es': '%C2%A1Hola%20Julio!%20Quiero%20informaci%C3%B3n%20de%20la%20Escoleta',
         'en': 'Hello%20Julio!%20I%27d%20like%20information%20about%20the%20basketball%20school'},
    'Hola%20Julio!%20Vull%20info%20de%20l%27Escoleta':
        {'es': '%C2%A1Hola%20Julio!%20Quiero%20info%20de%20la%20Escoleta',
         'en': 'Hello%20Julio!%20I%27d%20like%20info%20about%20the%20basketball%20school'},
}


def localize_scripts(doc, lang):
    for sc in doc.xpath('//script[not(@src)]'):
        if not sc.text:
            continue
        t = sc.text
        for src, tr in JS_STRINGS.items():
            if src in t:
                t = t.replace(src, tr[lang])
        sc.text = t
    for el in doc.xpath('//a[@href]'):
        h = el.get('href')
        if 'wa.me' in h or 'api.whatsapp.com' in h:
            for src, tr in WA_TEXT.items():
                if src in h:
                    el.set('href', h.replace(src, tr[lang]))
                    break


def lang_switcher(doc, urls, lang):
    """Insereix (o actualitza) el selector d'idioma dins la navegació."""
    for old in doc.xpath('//*[@data-langsel]'):
        old.getparent().remove(old)
    for old in doc.xpath('//style[@data-langsel-css]'):
        old.getparent().remove(old)
    # El selector ha de sobreviure als media queries que amaguen .head-nav en
    # mòbil, així que va al contenidor de la capçalera, no dins del <nav>.
    host = (doc.xpath('//*[contains(@class,"head-side") and contains(@class,"r")]')
            or doc.xpath('//nav[contains(@class,"head-nav")]')
            or doc.xpath('//header//nav'))
    if not host:
        return
    st = etree.SubElement(doc.xpath('//head')[0], 'style')
    st.set('data-langsel-css', '1')
    st.text = LANGSEL_CSS
    box = etree.SubElement(host[0], 'span')
    box.set('data-langsel', '1')
    box.set('class', 'langsel')
    for code, u in urls.items():
        a = etree.SubElement(box, 'a')
        a.text = LABEL[code]
        a.set('href', u.replace(BASE, '') or '/')
        a.set('hreflang', code)
        if code == lang:
            a.set('aria-current', 'true')


def head_meta(doc, urls, lang, cat):
    head = doc.xpath('//head')[0]
    doc.set('lang', lang)
    for el in doc.xpath('//link[@rel="canonical"] | //link[@rel="alternate"][@hreflang]'):
        el.getparent().remove(el)
    c = etree.SubElement(head, 'link')
    c.set('rel', 'canonical'); c.set('href', urls[lang])
    for code, u in urls.items():
        l = etree.SubElement(head, 'link')
        l.set('rel', 'alternate'); l.set('hreflang', code); l.set('href', u)
    x = etree.SubElement(head, 'link')
    x.set('rel', 'alternate'); x.set('hreflang', 'x-default'); x.set('href', urls['ca'])
    for m in doc.xpath('//meta[@property="og:url"]'):
        m.set('content', urls[lang])
    for m in doc.xpath('//meta[@property="og:locale"]'):
        m.set('content', OG_LOCALE[lang])
    for m in doc.xpath('//meta[@property="og:locale:alternate"]'):
        m.getparent().remove(m)
    for code in urls:
        if code != lang:
            m = etree.SubElement(head, 'meta')
            m.set('property', 'og:locale:alternate'); m.set('content', OG_LOCALE[code])


def fix_paths(doc):
    """Les subcarpetes /es/ i /en/ no poden fer servir rutes relatives."""
    for el in doc.xpath('//*[@src] | //*[@href] | //*[@srcset] | //*[@data-src]'):
        for attr in ('src', 'href', 'srcset', 'data-src'):
            v = el.get(attr)
            if v and not v.startswith(('http', '/', '#', 'data:', 'mailto:', 'tel:', 'javascript:')):
                el.set(attr, '/' + v.lstrip('./'))
    for st in doc.xpath('//style'):
        if st.text:
            st.text = re.sub(r'url\((?![\'"]?(?:https?:|/|data:))[\'"]?([^)\'"]+)[\'"]?\)',
                             r'url(/\1)', st.text)


def localize_jsonld(doc, lang, urls, cat):
    """Tradueix els camps de text del JSON-LD i hi ajusta url/inLanguage."""
    tag = {'ca': 'ca-ES', 'es': 'es-ES', 'en': 'en'}[lang]

    def walk(o):
        if isinstance(o, dict):
            r = {}
            for k, v in o.items():
                if k in ('name', 'description', 'headline', 'alternateName',
                         'jobTitle', 'serviceType', 'articleSection'):
                    r[k] = walk_text(v)
                elif k == 'inLanguage':
                    r[k] = tag
                elif k in ('url', 'item', '@id') and isinstance(v, str) and v.startswith(BASE):
                    r[k] = swap(v)
                else:
                    r[k] = walk(v)
            return r
        if isinstance(o, list):
            return [walk(v) for v in o]
        return o

    def walk_text(v):
        if isinstance(v, str):
            k = ' '.join(v.split())
            return cat.get(k, {}).get(lang) or v
        if isinstance(v, list):
            return [walk_text(x) for x in v]
        return walk(v)

    def swap(u):
        if u == urls['ca'] or u == urls['ca'].rstrip('/'):
            return urls[lang]
        if u.startswith(urls['ca']):
            return urls[lang] + u[len(urls['ca']):]
        return u

    for sc in doc.xpath('//script[@type="application/ld+json"]'):
        try:
            data = json.loads(sc.text)
        except Exception:
            continue
        sc.text = json.dumps(walk(data), ensure_ascii=False, indent=2)


def build_page(slug):
    src, langs, _ = PAGES[slug]
    urls = urls_for(slug)
    cat = load_cat(slug)
    made = []

    # el català també es reescriu, per rebre hreflang i el selector
    for lang in ('ca',) + tuple(langs):
        doc = LH.parse(src).getroot()
        if lang != 'ca':
            apply_lang(doc, cat, lang)
            localize_jsonld(doc, lang, urls, cat)
            localize_scripts(doc, lang)
            fix_paths(doc)
        head_meta(doc, urls, lang, cat)
        lang_switcher(doc, urls, lang)
        out = src if lang == 'ca' else out_for(slug, lang)
        os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
        html = '<!DOCTYPE html>\n' + LH.tostring(doc, encoding='unicode')
        open(out, 'w', encoding='utf-8').write(html)
        made.append(out)
    return made


def cmd_check():
    total = pend = 0
    for slug in PAGES:
        f = f'{CAT}/{slug}.json'
        if not os.path.exists(f):
            print(f'{slug:8s} · sense catàleg'); continue
        cat = json.load(open(f, encoding='utf-8'))
        miss = [k for k, v in cat.items() if not (v.get('es') and v.get('en'))]
        total += len(cat); pend += len(miss)
        print(f'{slug:8s} · {len(cat):4d} cadenes · {len(miss):4d} pendents')
        for m in miss[:5]:
            print(f'           ↳ {m[:70]}')
    print(f'\nTOTAL {total} cadenes · {pend} pendents')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if cmd == 'extract':
        for p in sys.argv[2:] or [f for f, _, _ in PAGES.values()]:
            cmd_extract(p)
    elif cmd == 'build':
        for s in sys.argv[2:] or PAGES:
            print(f'{s}: ' + ', '.join(build_page(s)))
    else:
        cmd_check()
