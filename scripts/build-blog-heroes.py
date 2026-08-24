#!/usr/bin/env python3
"""
Converteix les fotos de portada dels articles del blog (img/blog/*-hero.jpg)
a WebP, seguint la mateixa regla que build-blog-images.py: retall des de dalt
(mai es talla un cap) i mai amplada per sobre de l'original (mai s'amplia
una foto).

Aquests 17 originals eren fotos verticals (retrat) servides senceres i sense
comprimir (fins a 420 KB), i el navegador les retallava soles amb
`object-fit: cover` a la caixa 16:9 de `.phead-media` — descarregant sempre
tota l'alçada del retrat per ensenyar-ne només una franja. Aquí es fa el
mateix retall en origen i es treuen dues mides WebP, com la resta del lloc.

    python3 scripts/build-blog-heroes.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "img" / "blog"

# Amplada màxima a pantalla: el contenidor de l'article (.narrow) fa 780px.
W_1X = 780
W_2X = 1560
ANCHOR_TOP = 0.0  # retall des de dalt: mai es perd un cap, es perd el terra


def crop_16_9(im, anchor=ANCHOR_TOP):
    w, h = im.size
    ratio = 16 / 9
    if w / h > ratio:
        nw, nh = int(round(h * ratio)), h
        left, top = (w - nw) // 2, 0
    else:
        nw, nh = w, int(round(w / ratio))
        left, top = 0, int(round((h - nh) * anchor))
    return im.crop((left, top, left + nw, top + nh))


def main():
    heroes = sorted(SRC.glob("*-hero.jpg"))
    if not heroes:
        print("Cap *-hero.jpg trobat a img/blog/.")
        return

    for src in heroes:
        slug = src.name[: -len("-hero.jpg")]
        im = Image.open(src).convert("RGB")
        cropped = crop_16_9(im)
        cw, ch = cropped.size

        for label, target_w in (("", W_1X), ("@2x", W_2X)):
            w = min(target_w, cw)  # mai s'amplia per sobre de l'original
            h = round(w * 9 / 16)
            out = cropped.resize((w, h), Image.LANCZOS) if w != cw else cropped
            dest = SRC / f"{slug}-hero{label}.webp"
            out.save(dest, "WEBP", quality=82, method=6)
            print(f"{dest.relative_to(ROOT)}  {w}x{h}  {dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
