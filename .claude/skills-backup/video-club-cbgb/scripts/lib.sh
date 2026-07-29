#!/usr/bin/env bash
# Funciones comunes para los scripts de video-club-cbgb.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRAND_CONF="${SCRIPT_DIR}/../assets/brand.conf"

# Carga la config de marca si existe (valores por defecto si no)
LOGO_PATH=""; BRAND_COLOR="#1B2A4A"; BRAND_COLOR_2="#E63329"; FONT_PATH=""
DEFAULT_HASHTAG="#SomGrupBarna"; WATERMARK_OPACITY="0.85"; WATERMARK_POS="BR"
[ -f "$BRAND_CONF" ] && source "$BRAND_CONF"

die() { echo "Error: $*" >&2; exit 1; }

need_ffmpeg() {
  command -v ffmpeg >/dev/null 2>&1 || die "ffmpeg no está instalado. Instala con: brew install ffmpeg"
}

# Convierte #RRGGBB a 0xRRGGBB para ffmpeg drawtext/drawbox
hex2ff() { echo "0x${1#\#}"; }

# Devuelve una fuente válida para drawtext
font_arg() {
  if [ -n "$FONT_PATH" ] && [ -f "$FONT_PATH" ]; then
    echo "fontfile='${FONT_PATH}'"
  else
    # Fuentes habituales en macOS
    for f in /System/Library/Fonts/Helvetica.ttc /Library/Fonts/Arial.ttf \
             /System/Library/Fonts/Supplemental/Arial.ttf; do
      [ -f "$f" ] && { echo "fontfile='${f}'"; return; }
    done
    echo "font='sans-serif'"
  fi
}

# Posición de overlay según TL/TR/BL/BR con margen m
overlay_xy() {
  local pos="$1" m="${2:-40}"
  case "$pos" in
    TL) echo "${m}:${m}" ;;
    TR) echo "W-w-${m}:${m}" ;;
    BL) echo "${m}:H-h-${m}" ;;
    BR|*) echo "W-w-${m}:H-h-${m}" ;;
  esac
}
