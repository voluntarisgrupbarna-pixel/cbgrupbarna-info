#!/usr/bin/env bash
# cut.sh — recorta un clip por marcas de tiempo (re-encode preciso).
# Uso: cut.sh -i entrada.mp4 -s 00:12:30 -e 00:12:38 -o jugada.mp4
#   -s/-e aceptan HH:MM:SS o segundos. Con -d en vez de -e usas duración.
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"

IN=""; OUT=""; START=""; END=""; DUR=""
usage(){ grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }
while getopts "i:o:s:e:d:h" opt; do case $opt in
  i) IN="$OPTARG";; o) OUT="$OPTARG";; s) START="$OPTARG";;
  e) END="$OPTARG";; d) DUR="$OPTARG";; h) usage 0;; *) usage 1;; esac; done

need_ffmpeg
[ -n "$IN" ] && [ -f "$IN" ] || die "falta -i entrada válida"
[ -n "$OUT" ] || die "falta -o salida"
[ -n "$START" ] || die "falta -s inicio"

if [ -n "$DUR" ]; then
  ffmpeg -y -ss "$START" -i "$IN" -t "$DUR" -c:v libx264 -crf 18 -preset medium -c:a aac "$OUT"
elif [ -n "$END" ]; then
  ffmpeg -y -ss "$START" -to "$END" -i "$IN" -c:v libx264 -crf 18 -preset medium -c:a aac "$OUT"
else
  die "indica -e fin o -d duración"
fi
echo "OK -> $OUT"
