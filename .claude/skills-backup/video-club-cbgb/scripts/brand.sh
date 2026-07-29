#!/usr/bin/env bash
# brand.sh — aplica marca de agua (logo), cierre con hashtag y lower-third.
# Uso: brand.sh -i in.mp4 -o out.mp4 [--hashtag "#..."] [--cta "Texto"]
#               [--lower-third "Nombre · Rol"] [--logos "a.png,b.png"]
#   Lee assets/brand.conf (LOGO_PATH, BRAND_COLOR, opacidad, posición).
#   --logos sobreescribe el logo único por una fila de logos (recap con sponsors).
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"

IN=""; OUT=""; HASHTAG=""; CTA=""; LOWER=""; LOGOS=""
usage(){ grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }
while [ $# -gt 0 ]; do case "$1" in
  -i) IN="$2"; shift 2;; -o) OUT="$2"; shift 2;;
  --hashtag) HASHTAG="$2"; shift 2;; --cta) CTA="$2"; shift 2;;
  --lower-third) LOWER="$2"; shift 2;; --logos) LOGOS="$2"; shift 2;;
  -h|--help) usage 0;; *) die "opción desconocida: $1";; esac; done

need_ffmpeg
[ -n "$IN" ] && [ -f "$IN" ] || die "falta -i entrada válida"
[ -n "$OUT" ] || die "falta -o salida"
[ -z "$HASHTAG" ] && HASHTAG="$DEFAULT_HASHTAG"
FONT="$(font_arg)"; BC=$(hex2ff "$BRAND_COLOR"); XY="$(overlay_xy "$WATERMARK_POS")"

# Construye filtros encadenados
FILTERS=""
INPUTS=(-i "$IN")
LAST="0:v"

# 1) Marca de agua (logo único)
if [ -n "$LOGO_PATH" ] && [ -f "$LOGO_PATH" ] && [ -z "$LOGOS" ]; then
  INPUTS+=(-i "$LOGO_PATH")
  FILTERS+="[1:v]format=rgba,colorchannelmixer=aa=${WATERMARK_OPACITY}[wm];[${LAST}][wm]overlay=${XY}[v1];"
  LAST="v1"
fi

# 2) Lower-third (nombre · rol) abajo a la izquierda en zona segura
if [ -n "$LOWER" ]; then
  ESC=$(printf '%s' "$LOWER" | sed "s/:/\\\:/g; s/'/\\\\\\\'/g")
  FILTERS+="[${LAST}]drawbox=x=0:y=ih-300:w=iw:h=110:color=${BC}@0.55:t=fill,"
  FILTERS+="drawtext=${FONT}:text='${ESC}':fontcolor=white:fontsize=46:x=60:y=h-275[v2];"
  LAST="v2"
fi

# 3) Cierre: hashtag + CTA sobre franja de marca en el último 1.5 s
ESC_H=$(printf '%s' "$HASHTAG" | sed "s/:/\\\:/g")
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN" 2>/dev/null | cut -d. -f1)
[ -z "$DUR" ] && DUR=10
T0=$(( DUR > 2 ? DUR - 2 : 0 ))
FILTERS+="[${LAST}]drawtext=${FONT}:text='${ESC_H}':fontcolor=white:fontsize=54:box=1:boxcolor=${BC}@0.7:boxborderw=20:x=(w-text_w)/2:y=h-220:enable='gte(t,${T0})'[v3];"
LAST="v3"
if [ -n "$CTA" ]; then
  ESC_C=$(printf '%s' "$CTA" | sed "s/:/\\\:/g")
  FILTERS+="[${LAST}]drawtext=${FONT}:text='${ESC_C}':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=h-150:enable='gte(t,${T0})'[v4];"
  LAST="v4"
fi

# Quita el ; final
FILTERS="${FILTERS%;}"

ffmpeg -y "${INPUTS[@]}" -filter_complex "$FILTERS" -map "[${LAST}]" -map 0:a? \
  -c:v libx264 -crf 19 -preset medium -c:a aac "$OUT"
echo "OK -> $OUT"
[ -n "$LOGOS" ] && echo "Nota: --logos (fila de sponsors) requiere componer la barra de logos; para >1 logo, pídeselo a Claude para montar el bloque de cierre a medida."
