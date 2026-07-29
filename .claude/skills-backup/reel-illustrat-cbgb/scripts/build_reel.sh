#!/usr/bin/env bash
# build_reel.sh — munta el reel il·lustrat: UNA il·lustració amb push-in continu +
# línies de text superposades en el seu tram horari + targeta de tancament.
# Requisits: ffmpeg. Prèviament cal haver corregut compose_overlays.py (genera
# ./overlays/line_XX.png + closing.png + manifest.json).
#
# Ús: ./build_reel.sh <illustracio.jpg> <lang: ca|es> [audio_bed.m4a]
# Sortida: reel_<lang>_SILENT.mp4 (per so de tendència) i reel_<lang>.mp4 (amb música,
# si s'ha passat àudio).
set -e
IMG="${1:?cal passar la il·lustració, p.ex. ./build_reel.sh illustracio.jpg ca}"
LANG_TAG="${2:-ca}"
AUDIO="${3:-}"
FPS=30
MANIFEST="overlays/manifest.json"
[[ -f "$MANIFEST" ]] || { echo "Falta $MANIFEST — corre primer compose_overlays.py"; exit 1; }

DUR_TOTAL=$(python3 -c "import json;print(json.load(open('$MANIFEST'))['duration_total'])")
DUR_CLOSING=$(python3 -c "import json;print(json.load(open('$MANIFEST'))['closing_duration'])")
FRAMES_TOTAL=$(python3 -c "print(round($DUR_TOTAL*$FPS))")
FRAMES_CLOSING=$(python3 -c "print(round($DUR_CLOSING*$FPS))")

mkdir -p clips

# 1) base amb push-in continu (Ken Burns) sobre la il·lustració, durada = part de línies
ffmpeg -y -loop 1 -i "$IMG" \
  -vf "scale=1512:2688,zoompan=z='min(zoom+0.0006,1.09)':d=$FRAMES_TOTAL:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=$FPS" \
  -frames:v "$FRAMES_TOTAL" -r $FPS -c:v libx264 -preset veryfast -pix_fmt yuv420p clips/base.mp4 -loglevel error
echo "base.mp4 (push-in, ${DUR_TOTAL}s) ok"

# 2) construir la cadena d'overlays: cada line_XX.png visible només al seu tram t0-t1
INPUTS=(-i clips/base.mp4)
N=$(python3 -c "import json;print(len(json.load(open('$MANIFEST'))['lines']))")
IDX=1
LAST="0:v"
STAGES=()
for i in $(seq 0 $((N-1))); do
  PNG=$(printf "overlays/line_%02d.png" "$i")
  T0=$(python3 -c "import json;print(json.load(open('$MANIFEST'))['lines'][$i]['t0'])")
  T1=$(python3 -c "import json;print(json.load(open('$MANIFEST'))['lines'][$i]['t1'])")
  INPUTS+=(-i "$PNG")
  NEXT="ov$i"
  STAGES+=("[${LAST}][${IDX}:v]overlay=0:0:enable='between(t,${T0},${T1})'[${NEXT}]")
  LAST="$NEXT"
  IDX=$((IDX+1))
done
FILTER=$(IFS=';'; echo "${STAGES[*]}")

ffmpeg -y "${INPUTS[@]}" -filter_complex "$FILTER" -map "[${LAST}]" \
  -r $FPS -c:v libx264 -preset veryfast -pix_fmt yuv420p clips/lined.mp4 -loglevel error
echo "lined.mp4 (text superposat) ok"

# 3) targeta de tancament (escut + programa + claim), push-in curt
ffmpeg -y -loop 1 -i overlays/closing.png \
  -vf "scale=1512:2688,zoompan=z='min(zoom+0.001,1.06)':d=$FRAMES_CLOSING:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=$FPS" \
  -frames:v "$FRAMES_CLOSING" -r $FPS -c:v libx264 -preset veryfast -pix_fmt yuv420p clips/closing.mp4 -loglevel error
echo "closing.mp4 (${DUR_CLOSING}s) ok"

# 4) concat
: > cat.txt
echo "file 'clips/lined.mp4'" >> cat.txt
echo "file 'clips/closing.mp4'" >> cat.txt
ffmpeg -y -f concat -safe 0 -i cat.txt -c copy "reel_${LANG_TAG}_SILENT.mp4" -loglevel error
echo "-> reel_${LANG_TAG}_SILENT.mp4 (per so de tendència)"

if [[ -n "$AUDIO" && -f "$AUDIO" ]]; then
  ffmpeg -y -i "reel_${LANG_TAG}_SILENT.mp4" -i "$AUDIO" -c:v copy -c:a aac -b:a 192k -shortest "reel_${LANG_TAG}.mp4" -loglevel error
  echo "-> reel_${LANG_TAG}.mp4 (amb música)"
fi
echo "durada total: $(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "reel_${LANG_TAG}_SILENT.mp4") s"
