#!/usr/bin/env python3
"""
Genera les imatges del blog (/img/blog/) a partir dels originals del repositori.

Cada entrada de ASSETS diu quina foto original s'usa, quina proporció ha de tenir
el marc i quina amplada ocupa a pantalla. El script en treu dos fitxers WebP:

    img/blog/<nom>.webp      · amplada de pantalla (1x)
    img/blog/<nom>@2x.webp   · el doble (pantalles retina)

Regla del sistema de disseny: cap foto no es mostra mai més gran del que és. Per
això `w` (amplada CSS) mai pot demanar més píxels dels que té l'original: si
l'original no arriba a 2x, el script avisa i no genera el fitxer.

El retall és per defecte des de dalt (anchor=0), de manera que el que es perd és
el terra i mai els caps. Amb `anchor` es pot baixar el punt de tall (0 = dalt,
0.5 = centre, 1 = baix).

    python3 scripts/build-blog-images.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "img" / "blog"

CAMP = "fotos/uploads/summer-camp-2526-grup-barna-time-chamber-experience-mslvztq9"
EQUIPS = "fotos/uploads/fotos-equips-temporada-25-26-records"

# nom, origen, proporció (w/h), amplada CSS, punt de tall vertical
ASSETS = [
    # ── targetes de /blog/ (graella de tres columnes: 353 px d'amplada) ──
    ("card-formacio", "photos/team_sf17.jpg", 16 / 10, 353, 0.10),
    ("card-edat", f"{EQUIPS}/1781613069472-40zhy.jpg", 16 / 10, 353, 0.30),
    ("card-triar", "img/club@2x.webp", 16 / 10, 353, 0.15),
    ("card-campus", f"{CAMP}/1786285898345-5e3nv.jpg", 16 / 10, 353, 0.35),
    ("card-3x3", "photos/team_sf20.jpg", 16 / 10, 353, 0.35),
    ("card-clot", "photos/s2c_entrada.jpg", 16 / 10, 353, 0.10),

    # ── a quina edat començar ──
    ("edat-escoleta", "img/escoleta@2x.webp", 3 / 4, 375, 0.00),
    ("edat-gran", f"{CAMP}/1786285472311-o8kwm.jpg", 3 / 4, 375, 0.06),
    ("edat-escola", f"{EQUIPS}/1781613069472-40zhy.jpg", 3 / 2, 600, 0.05),

    # ── escola, club o acadèmia ──
    ("triar-club", "img/club@2x.webp", 3 / 2, 540, 0.00),
    ("triar-femeni", f"{EQUIPS}/1781613057622-7atav.jpg", 3 / 2, 600, 0.05),

    # ── campus ──
    ("campus-pista", f"{CAMP}/1786285898345-5e3nv.jpg", 16 / 9, 780, 0.30),
    ("campus-tir", f"{CAMP}/1786288242180-7jqeu.jpg", 3 / 4, 375, 0.10),
    ("campus-entrenador", f"{CAMP}/1786288527688-2gxo9.jpg", 3 / 4, 375, 0.08),

    # ── 3x3 ──
    ("tres-glories", "photos/club_cbgb006.jpg", 3 / 2, 450, 0.05),

    # ── bàsquet base al Clot ──
    ("clot-entrada", "photos/s2c_entrada.jpg", 3 / 2, 375, 0.05),
    ("clot-mascota", "photos/s2b_mascota.jpg", 3 / 2, 375, 0.05),

    # ── el Barna entre els grans ──
    ("formacio-senior", "photos/hero_sf16.jpg", 16 / 9, 780, 0.16),
    ("formacio-junior", f"{EQUIPS}/1781613084063-x60f3.jpg", 3 / 2, 600, 0.05),
]


def crop_to(im, ratio, anchor):
    """Retalla la imatge a la proporció demanada sense deformar-la."""
    w, h = im.size
    if w / h > ratio:                      # sobra amplada → retallem als costats
        nw, nh = int(round(h * ratio)), h
        left = (w - nw) // 2
        top = 0
    else:                                  # sobra alçada → retallem a dalt/baix
        nw, nh = w, int(round(w / ratio))
        left = 0
        top = int(round((h - nh) * anchor))
    return im.crop((left, top, left + nw, top + nh))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, src, ratio, width, anchor in ASSETS:
        path = ROOT / src
        if not path.exists():
            print(f"  !  falta l'original {src}")
            continue
        im = Image.open(path).convert("RGB")
        cropped = crop_to(im, ratio, anchor)
        if cropped.width < width * 2:
            print(f"  !  {name}: l'original només dona {cropped.width} px i "
                  f"en calen {width * 2}. Cal una foto més gran o un marc més petit.")
            continue
        for suffix, w in ((f"{name}.webp", width), (f"{name}@2x.webp", width * 2)):
            h = int(round(w / ratio))
            out = OUT / suffix
            cropped.resize((w, h), Image.LANCZOS).save(
                out, "WEBP", quality=80, method=6)
            print(f"  img/blog/{suffix}  ({w}×{h}, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
