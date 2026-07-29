#!/usr/bin/env bash
# cinematic_grade.sh — aplica un look cinematográfico a un clip (athlete film).
# Uso: cinematic_grade.sh -i in.mp4 -o out.mp4 [--look calid|moody] [--grain]
#                         [--slowmo 0.5] [--bars]
#   --look calid : teal&orange suave, contrastado (estilo Nike). Por defecto.
#   --look moody : desaturado, alto contraste, sombras profundas.
#   --grain      : añade grano de film sutil.
#   --slowmo F   : ralentiza a factor F (0.5 = mitad) con interpolación de frames.
#   --bars       : barras negras cine 2.39:1 (letterbox).
# Pensado para clips cortos (planos héroe/detalle). Requiere ffmpeg.
set -euo pipefail
usage(){ grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }
command -v ffmpeg >/dev/null 2>&1 || { echo "Falta ffmpeg (brew install ffmpeg)"; exit 1; }

IN=""; OUT=""; LOOK="calid"; GRAIN=0; SLOWMO=""; BARS=0
while [ $# -gt 0 ]; do case "$1" in
  -i) IN="$2"; shift 2;; -o) OUT="$2"; shift 2;;
  --look) LOOK="$2"; shift 2;; --grain) GRAIN=1; shift;;
  --slowmo) SLOWMO="$2"; shift 2;; --bars) BARS=1; shift;;
  -h|--help) usage 0;; *) echo "opción: $1"; exit 1;; esac; done
[ -n "$IN" ] && [ -f "$IN" ] || { echo "falta -i entrada válida"; exit 1; }
[ -n "$OUT" ] || { echo "falta -o salida"; exit 1; }

VF=""
# 1) Slow-mo con interpolación (suaviza el movimiento ralentizado)
if [ -n "$SLOWMO" ]; then
  VF="minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:vsbmc=1,setpts=${SLOWMO}*PTS,"
fi
# 2) Look de color
case "$LOOK" in
  calid)  # teal&orange suave + contraste
    VF="${VF}eq=contrast=1.12:saturation=1.04:gamma=0.98,colorbalance=rs=.06:gs=-.02:bs=-.05:rh=-.04:bh=.06,"
    ;;
  moody)  # desaturado, contrastado, sombras densas
    VF="${VF}eq=contrast=1.2:saturation=0.82:brightness=-0.03:gamma=0.95,curves=preset=darker,"
    ;;
  *) echo "look no válido (calid|moody)"; exit 1;;
esac
# 3) Grano de film sutil
[ "$GRAIN" -eq 1 ] && VF="${VF}noise=alls=8:allf=t,"
# 4) Barras cine
[ "$BARS" -eq 1 ] && VF="${VF}crop=iw:ih*0.836,pad=iw:ih/0.836:0:(oh-ih)/2:color=black,"
# Limpia coma final
VF="${VF%,}"

ffmpeg -y -i "$IN" -vf "$VF" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -c:a aac "$OUT"
EXTRA=""
[ -n "$SLOWMO" ] && EXTRA="$EXTRA, slowmo $SLOWMO"
[ "$GRAIN" -eq 1 ] && EXTRA="$EXTRA, grain"
[ "$BARS" -eq 1 ] && EXTRA="$EXTRA, bars"
echo "OK ($LOOK$EXTRA) -> $OUT"
