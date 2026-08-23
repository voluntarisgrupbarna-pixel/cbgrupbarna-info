#!/usr/bin/env python3
"""Posa la crida de comunitat a totes les pàgines, just abans del peu.

Dues portes: seguir el club a Instagram i apuntar-se a la newsletter. Van a
totes les pàgines públiques perquè qui hi arriba per qualsevol porta acabi
sabent per on seguir el club, no només qui arriba a la portada.

És idempotent: si la pàgina ja la porta, no la duplica; si el text ha canviat,
el refà. Salta les pàgines internes (admin), les peces per imprimir i les que
no tenen el peu del sistema.

Ús:  python3 scripts/crida-comunitat.py [--dry-run]
"""

import re
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
EXCLOU = (
    "admin/", "/admin.html", "opina/print/", "briefing/admin.html",
    # Les presentacions són peces fosques amb el seu propi joc de tokens:
    # allà --ink és blanc i la crida hi sortiria blanca sobre blanc.
    "presentacions/", "presentacio/",
)

TEXTOS = {
    "ca": {
        "etiqueta": "Segueix el CB Grup Barna",
        "ig_t": "Segueix-nos a Instagram",
        "ig_s": "@cbgrupbarna · el dia a dia del club, cada setmana.",
        "nl_t": "Apunta't a la newsletter",
        "nl_s": "Un correu al mes amb el que val la pena saber. Res més.",
        "nl_url": "/newsletter/",
    },
    "es": {
        "etiqueta": "Sigue al CB Grup Barna",
        "ig_t": "Síguenos en Instagram",
        "ig_s": "@cbgrupbarna · el día a día del club, cada semana.",
        "nl_t": "Apúntate a la newsletter",
        "nl_s": "Un correo al mes con lo que vale la pena saber. Nada más.",
        "nl_url": "/es/newsletter/",
    },
    "en": {
        "etiqueta": "Follow CB Grup Barna",
        "ig_t": "Follow us on Instagram",
        "ig_s": "@cbgrupbarna · the club's week, as it happens.",
        "nl_t": "Join the newsletter",
        "nl_s": "One email a month with what's worth knowing. Nothing else.",
        "nl_url": "/en/newsletter/",
    },
}

INICI = "<!-- CRIDA DE COMUNITAT · scripts/crida-comunitat.py -->"
FI = "<!-- /CRIDA DE COMUNITAT -->"
RE_BLOC = re.compile(re.escape(INICI) + r".*?" + re.escape(FI) + r"\s*", re.S)


def bloc(idioma: str) -> str:
    t = TEXTOS[idioma]
    return f"""{INICI}
<section class="comunitat" aria-label="{t['etiqueta']}">
  <div class="comunitat-in">
    <a class="comunitat-porta" href="https://www.instagram.com/cbgrupbarna/" target="_blank" rel="noopener" data-cta="crida-instagram">
      <span class="comunitat-t">{t['ig_t']}</span>
      <span class="comunitat-s">{t['ig_s']}</span>
    </a>
    <a class="comunitat-porta comunitat-porta--red" href="{t['nl_url']}" data-cta="crida-newsletter">
      <span class="comunitat-t">{t['nl_t']}</span>
      <span class="comunitat-s">{t['nl_s']}</span>
    </a>
  </div>
</section>
{FI}
"""


def main() -> int:
    dry = "--dry-run" in sys.argv
    posades = 0
    for f in sorted(ARREL.rglob("*.html")):
        rel = "/" + str(f.relative_to(ARREL))
        if ".git" in f.parts or any(x in rel for x in EXCLOU):
            continue
        s = f.read_text(encoding="utf-8")
        if '<footer class="foot">' not in s:
            continue
        idioma = "ca"
        m = re.search(r'<html[^>]*\blang="([a-z]{2})', s)
        if m and m.group(1) in TEXTOS:
            idioma = m.group(1)
        # la newsletter no s'anuncia a ella mateixa
        nou = "" if f.parent.name == "newsletter" else bloc(idioma)
        net = RE_BLOC.sub("", s)
        resultat = net.replace('<footer class="foot">', nou + '<footer class="foot">', 1)
        if resultat == s:
            continue
        posades += 1
        if not dry:
            f.write_text(resultat, encoding="utf-8")
    print(f"{posades} pàgines {'a canviar' if dry else 'amb la crida'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
