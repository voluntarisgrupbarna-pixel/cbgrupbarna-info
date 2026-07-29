#!/usr/bin/env bash
# montage.sh — concatena varios clips en un montaje, con música y preset.
# Uso: montage.sh --preset highlight|reel|recap|feature [-m musica.mp3]
#                 [--title "Texto apertura"] -o salida.mp4 clip1 clip2 ...
#   Normaliza todos los clips a la misma resolución/fps antes de unir
#   (evita el fallo típico de concat con clips de fuentes distintas).
#   Presets ajustan resolución base y si lleva título de apertura.
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"

PRESET="reel"; MUSIC=""; TITLE=""; OUT=""; CLIPS=()
usage(){ grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }
while [ $# -gt 0 ]; do case "$1" in
  --preset) PRESET="$2"; shift 2;; -m) MUSIC="$2"; shift 2;;
  --title) TITLE="$2"; shift 2;; -o) OUT="$2"; shift 2;;
  -h|--help) usage 0;; -*) die "opción desconocida: $1";;
  *) CLIPS+=("$1"); shift;; esac; done

need_ffmpeg
[ "${#CLIPS[@]}" -ge 1 ] || die "indica al menos un clip"
[ -n "$OUT" ] || die "falta -o salida"

case "$PRESET" in
  reel|feature)   W=1080; H=1920;;
  highlight)      W=1080; H=1920;;
  recap)          W=1920; H=1080;;
  *) die "preset no válido: $PRESET (highlight|reel|recap|feature)";;
esac
FPS=30
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

# Normaliza cada clip (imágenes -> 3 s de vídeo)
i=0; LIST="$TMP/list.txt"; : > "$LIST"
for c in "${CLIPS[@]}"; do
  [ -f "$c" ] || die "no existe: $c"
  out="$TMP/norm_$i.mp4"
  ext="${c##*.}"; ext="$(echo "$ext" | tr 'A-Z' 'a-z')"
  if [[ "$ext" =~ ^(jpg|jpeg|png|webp)$ ]]; then
    ffmpeg -y -loop 1 -t 3 -i "$c" -vf "scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},setsar=1" \
      -r $FPS -pix_fmt yuv420p -f lavfi -t 3 -i anullsrc=channel_layout=stereo:sample_rate=44100 \
      -c:v libx264 -crf 20 -c:a aac -shortest "$out"
  else
    ffmpeg -y -i "$c" -vf "scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},setsar=1,fps=${FPS}" \
      -af "aresample=44100" -c:v libx264 -crf 20 -c:a aac "$out" 2>/dev/null || \
    ffmpeg -y -i "$c" -vf "scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},setsar=1,fps=${FPS}" \
      -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -shortest -c:v libx264 -crf 20 -c:a aac "$out"
  fi
  echo "file '$out'" >> "$LIST"
  i=$((i+1))
done

# Concatena
JOIN="$TMP/joined.mp4"
ffmpeg -y -f concat -safe 0 -i "$LIST" -c:v libx264 -crf 20 -c:a aac "$JOIN"

# Título de apertura (recap/feature) los primeros 3 s
CUR="$JOIN"
if [ -n "$TITLE" ]; then
  FONT="$(font_arg)"; BC=$(hex2ff "$BRAND_COLOR")
  ESC=$(printf '%s' "$TITLE" | sed "s/:/\\\:/g")
  TITLED="$TMP/titled.mp4"
  ffmpeg -y -i "$CUR" -vf "drawtext=${FONT}:text='${ESC}':fontcolor=white:fontsize=64:box=1:boxcolor=${BC}@0.6:boxborderw=24:x=(w-text_w)/2:y=(h-text_h)/2:enable='lte(t,3)'" \
    -c:v libx264 -crf 20 -c:a copy "$TITLED"
  CUR="$TITLED"
fi

# Música de fondo (mezcla con audio existente, baja el original)
if [ -n "$MUSIC" ] && [ -f "$MUSIC" ]; then
  ffmpeg -y -i "$CUR" -i "$MUSIC" -filter_complex \
    "[0:a]volume=0.6[a0];[1:a]volume=0.8[a1];[a0][a1]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:TP=-1.5[aout]" \
    -map 0:v -map "[aout]" -c:v copy -c:a aac -shortest "$OUT"
else
  ffmpeg -y -i "$CUR" -af "loudnorm=I=-14:TP=-1.5" -c:v copy -c:a aac "$OUT"
fi
echo "OK ($PRESET, ${W}x${H}) -> $OUT"
