#!/usr/bin/env python3
"""
Posa JA i KO al commutador d'idioma de les pàgines que tenen versió en
japonès o coreà, i hi marca l'idioma d'ara.

    python3 scripts/i18n-commutador-cjk.py

Llegeix i18n/routes.yml: només toca els grups on hi ha `ja` o `ko`. És
idempotent — es pot repetir després de muntar les pàgines amb
scripts/i18n-munta.py, que deixa el commutador de la pàgina catalana
(CA·ES·EN) tal com era.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
IDIOMES = [("ca", "CA", "Català"), ("es", "ES", "Castellano"), ("en", "EN", "English"),
           ("ja", "JA", "日本語"), ("ko", "KO", "한국어"),
           ("de", "DE", "Deutsch"), ("it", "IT", "Italiano"), ("nl", "NL", "Nederlands"), ("fr", "FR", "Français"), ("ar", "AR", "العربية"), ("tr", "TR", "Türkçe"), ("pt", "PT", "Português")]
ARIA = "Canvia d'idioma · Cambiar idioma · Change language · 言語を変更 · 언어 변경 · Sprache ändern · Cambia lingua · Taal wijzigen · Changer de langue · تغيير اللغة"
RE_BLOC = re.compile(r'(?is)<(div|nav)(\s+class="lang-switch"[^>]*)>(.*?)</\1>')
# Amb nou idiomes el commutador ja no cap en un mòbil: sense separadors i amb
# menys marge ocupa uns 200 px en lloc de 330.
ESTIL = ('<style id="lang-switch-compact">@media(max-width:640px){'
         '.lang-switch .sep{display:none}'
         '.lang-switch a{min-width:22px;padding:7px 2px}'
         '.lang-switch{flex-shrink:1;flex-wrap:wrap;justify-content:flex-end;letter-spacing:0}}</style>')
RE_ESTIL = re.compile(r'<style id="lang-switch-compact">.*?</style>')
SEP = '<span class="sep" aria-hidden="true">·</span>'


def fitxer_de(url):
    return ROOT / (url.lstrip("/") + "index.html" if url.endswith("/") else url.lstrip("/"))


def main():
    rutes = (yaml.safe_load((ROOT / "i18n" / "routes.yml").read_text(encoding="utf-8")) or {}).get("rutes", [])
    tocades = 0
    for grup in rutes:
        if not any(grup.get(i) for i in ("ja", "ko", "de", "it", "nl", "fr", "ar", "tr", "pt")):
            continue
        for idioma, _, _ in IDIOMES:
            url = grup.get(idioma)
            if not url or not fitxer_de(url).exists():
                continue
            fitxer = fitxer_de(url)
            text = fitxer.read_text(encoding="utf-8")
            enllacos = []
            for codi, etiqueta, nom in IDIOMES:
                if not grup.get(codi) or not fitxer_de(grup[codi]).exists():
                    continue
                actiu = ' class="active" aria-current="true"' if codi == idioma else ""
                enllacos.append(f'<a href="{grup[codi]}" hreflang="{codi}" lang="{codi}" '
                                f'aria-label="{nom}"{actiu}>{etiqueta}</a>')

            def canvia(m):
                obre = re.sub(r'aria-label="[^"]*"', f'aria-label="{ARIA}"', m.group(2))
                return f'<{m.group(1)}{obre}>\n      {SEP.join(enllacos)}\n    </{m.group(1)}>'

            nou, n = RE_BLOC.subn(canvia, text, count=1)
            if n and "</head>" in nou:
                nou = RE_ESTIL.sub("", nou)
                nou = nou.replace("</head>", ESTIL + "\n</head>", 1)
            if n and nou != text:
                fitxer.write_text(nou, encoding="utf-8")
                tocades += 1
            elif not n:
                print(f"  avís: {url} no té commutador d'idioma")
    print(f"{tocades} pàgines amb el commutador al dia")
    return 0


if __name__ == "__main__":
    sys.exit(main())
