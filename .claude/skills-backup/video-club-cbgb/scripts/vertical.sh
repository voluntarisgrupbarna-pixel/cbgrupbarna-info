#!/usr/bin/env bash
# vertical.sh — convierte vídeo a 9:16 (1080x1920) para reels/stories.
# Uso: vertical.sh -i entrada.mp4 -o salida.mp4 [--mode crop|blur|pad]
#   crop  : recorte centrado (rellena pantalla, recomendado si la acción va centrada)
#   blur  : vídeo entero encajado sobre su propio fondo difuminado (no recorta acción)
#   pad   : barras de color de marca arriba/abajo
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"

IN=""; OUT=""; MODE="crop"
usage(){ grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }
while [ $# -gt 0 ]; do case "$1" in
  -i) IN="$2"; shift 2;; -o) OUT="$2"; shift 2;;
  --mode) MODE="$2"; shift 2;; -h|--help) usage 0;; *) die "opción desconocida: $1";; esac; done

need_ffmpeg
[ -n "$IN" ] && [ -f "$IN" ] || die "falta -i entrada válida"
[ -n "$OUT" ] || die "falta -o salida"
W=1080; H=1920

case "$MODE" in
  crop)
    VF="scale=-2:${H},crop=${W}:${H}:(iw-${W})/2:0"
    ;;
  blur)
    VF="[0:v]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},gblur=sigma=25[bg];[0:v]scale=${W}:-2:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2"
    ;;
  pad)
    BC=$(hex2ff "$BRAND_COLOR")
    VF="scale=${W}:-2:force_original_aspect_ratio=decrease,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2:color=${BC}"
    ;;
  *) die "modo no válido: $MODE (crop|blur|pad)";;
esac

if [ "$MODE" = "blur" ]; then
  ffmpeg -y -i "$IN" -filter_complex "$VF" -c:v libx264 -crf 20 -preset medium -c:a aac -r 30 "$OUT"
else
  ffmpeg -y -i "$IN" -vf "$VF" -c:v libx264 -crf 20 -preset medium -c:a aac -r 30 "$OUT"
fi
echo "OK ($MODE) -> $OUT"
