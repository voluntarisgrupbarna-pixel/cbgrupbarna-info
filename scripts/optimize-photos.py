#!/usr/bin/env python3
"""Recomprimeix in-place les fotos de fotos/uploads/ que superen els 500KB.

Redueix la mida maxima a 2000px pel costat llarg, reencodifica JPEG a
qualitat 82 (progressive + optimize) i elimina EXIF (baking prèviament
l'orientacio als pixels, per privadesa: cap geolocalitzacio de fotos de
menors quedi al fitxer publicat).

Us: pip install --break-system-packages Pillow && python3 scripts/optimize-photos.py [--dry-run]
"""
import os
import sys

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_EDGE = 2000
QUALITY = 82
THRESHOLD = 500 * 1024


def find_targets():
    targets = []
    for dirpath, _, files in os.walk(os.path.join(ROOT, 'fotos')):
        for fn in files:
            if fn.lower().endswith(('.jpg', '.jpeg')):
                p = os.path.join(dirpath, fn)
                if os.path.getsize(p) > THRESHOLD:
                    targets.append(p)
    return targets


def optimize(path, dry_run=False):
    before = os.path.getsize(path)
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    w, h = im.size
    if max(w, h) > MAX_EDGE:
        scale = MAX_EDGE / max(w, h)
        im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    if not dry_run:
        im.save(path, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
    after = os.path.getsize(path) if not dry_run else None
    return before, after


if __name__ == '__main__':
    dry = '--dry-run' in sys.argv
    targets = find_targets()
    print(f'{len(targets)} fitxers a processar (dry_run={dry})')
    total_before = total_after = 0
    for i, p in enumerate(targets):
        before, after = optimize(p, dry_run=dry)
        total_before += before
        if after is not None:
            total_after += after
        print(f'[{i + 1}/{len(targets)}] {os.path.relpath(p, ROOT)} {before / 1024:.0f}KB -> {(after or 0) / 1024:.0f}KB')
    print(f'TOTAL abans: {total_before / 1024 / 1024:.1f} MB')
    if not dry:
        print(f'TOTAL despres: {total_after / 1024 / 1024:.1f} MB')
        print(f'Estalvi: {(total_before - total_after) / 1024 / 1024:.1f} MB ({100 * (1 - total_after / total_before):.1f}%)')
