#!/usr/bin/env python3
"""Al blog de cada idioma hi han de sortir TOTS els articles.

El blog en català els té tots. El castellà i l'anglès només ensenyaven els que
estan traduïts, i la resta no existien per a qui llegeix en aquell idioma.

Aquest script agafa les targetes del blog en català —que és la font— i, per a
cada idioma, refà la graella:

  · si l'article està traduït, la targeta hi va amb el títol i l'adreça de la
    traducció;
  · si no ho està, baixa a un bloc «Anteriores» / «Earlier», amb el títol en
    català i una etiqueta que ho diu, i l'enllaç va a l'original.

Així no se n'amaga cap i qui llegeix sap què es trobarà abans de clicar.

Ús:  python3 scripts/blog-tots-els-articles.py [--dry-run]
"""

import re
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent

IDIOMES = {
    "es": {
        "index": "es/blog/index.html",
        "titol_anteriors": "Anteriores",
        "nota": "Estos artículos están publicados en catalán.",
        "etiqueta": "En catalán",
        "llegir": "Leer",
    },
    "en": {
        "index": "en/blog/index.html",
        "titol_anteriors": "Earlier",
        "nota": "These articles are published in Catalan.",
        "etiqueta": "In Catalan",
        "llegir": "Read",
    },
}

RE_CARD = re.compile(r'<a class="card" href="(?P<url>[^"]+)".*?</a>', re.S)


def camps(bloc: str) -> dict:
    """Els camps d'una targeta, un a un: si en falta cap, la targeta no es
    perd, es queda amb el que hi ha."""
    def tros(patro, per_defecte=""):
        m = re.search(patro, bloc, re.S)
        return re.sub(r"\s+", " ", m.group(1)).strip() if m else per_defecte

    return {
        "tag": tros(r'<span class="card-tag">(.*?)</span>'),
        "titol": tros(r"<h3>(.*?)</h3>"),
        "text": tros(r"<p>(.*?)</p>"),
    }


RE_GRAELLA = re.compile(
    r'(?P<obre><div class="cards c3"[^>]*>)(?P<cos>.*?)(?P<tanca></div>\s*</div>)',
    re.S,
)


def llegeix_rutes() -> dict:
    """routes.yml sense dependre de cap llibreria: el format és pla i fix."""
    rutes = {}
    ca = None
    for línia in (ARREL / "i18n/routes.yml").read_text(encoding="utf-8").splitlines():
        línia = línia.strip()
        if línia.startswith("- ca:"):
            ca = línia[5:].strip()
            rutes[ca] = {}
        elif ca and línia.startswith(("es:", "en:")):
            idioma, valor = línia.split(":", 1)
            valor = valor.strip()
            trossos = valor.split()
            rutes[ca][idioma] = (
                None if not trossos or trossos[0] == "null" else trossos[0]
            )
    return rutes


def titol_de(cami: Path) -> tuple[str, str, str]:
    """Títol, etiqueta i entradeta d'una pàgina d'article ja traduïda."""
    s = cami.read_text(encoding="utf-8")
    h1 = re.search(r"<h1>(.*?)</h1>", s, re.S)
    tag = re.search(r'<p class="eyebrow red">(.*?)</p>', s, re.S)
    lede = re.search(r'<p class="lede">(.*?)</p>', s, re.S)
    net = lambda m, per_defecte="": re.sub(r"\s+", " ", m.group(1)).strip() if m else per_defecte
    return net(h1), net(tag), net(lede)


def targeta(url: str, tag: str, titol: str, text: str, cta: str) -> str:
    return (
        f'<a class="card" href="{url}"><div class="card-body">'
        f'<span class="card-tag">{tag}</span><h3>{titol}</h3><p>{text}</p>'
        f'<span class="cta">{cta}</span></div></a>'
    )


def main() -> int:
    dry = "--dry-run" in sys.argv
    font = (ARREL / "blog/index.html").read_text(encoding="utf-8")
    articles = []
    for m in RE_CARD.finditer(font):
        a = camps(m.group(0))
        a["url"] = m.group("url")
        articles.append(a)
    if not articles:
        print("No he trobat cap targeta al blog en català."); return 1
    rutes = llegeix_rutes()

    for idioma, cfg in IDIOMES.items():
        cami = ARREL / cfg["index"]
        pagina = cami.read_text(encoding="utf-8")
        traduits, pendents = [], []
        for a in articles:
            desti = (rutes.get(a["url"]) or {}).get(idioma)
            fitxer = ARREL / desti.strip("/") / "index.html" if desti else None
            if desti and fitxer.exists():
                titol, tag, lede = titol_de(fitxer)
                traduits.append(targeta(
                    desti, tag or a["tag"], titol or a["titol"],
                    lede or a["text"], cfg["llegir"]))
            else:
                pendents.append(targeta(
                    a["url"], cfg["etiqueta"], a["titol"], a["text"], cfg["llegir"]))

        bloc = "".join(traduits)
        if pendents:
            bloc += (
                '</div>\n'
                f'  <div class="e-sech" style="margin-top:clamp(20px,3vw,34px)">'
                f'<h2>{cfg["titol_anteriors"]}</h2><em>{cfg["nota"]}</em></div>\n'
                '  <div class="cards c3" style="padding-bottom:clamp(40px,6vw,80px)">'
                + "".join(pendents)
            )

        nova, n = RE_GRAELLA.subn(
            lambda m: m.group("obre") + bloc + m.group("tanca"), pagina, count=1
        )
        if not n:
            print("No he trobat la graella a", cfg["index"]); continue
        print(f'{cfg["index"]}: {len(traduits)} traduïts + {len(pendents)} en català')
        if not dry:
            cami.write_text(nova, encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
