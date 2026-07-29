#!/usr/bin/env bash
# build_reel.sh — munta el reel a partir dels PNGs de ./scenes/ + un àudio bed.
# Requisits: ffmpeg. Els plans han d'estar a ./scenes/ (generats per compose_reel.py).
# Sortida: reel_${LANG}.mp4 (amb música) i reel_${LANG}_SILENT.mp4 (per so de tendència).
# Estructura fixa 27,0 s (beat-sync). Durades EXACTES per frames (no per -t).
set -e
LANG_TAG="${1:-ca}"
AUDIO="${2:-audio_bed.m4a}"          # opcional; si no hi és, surt versió muda igualment
FPS=30
mkdir -p clips

# durada en frames per pla:  id:frames
# hook 2x30 (1s) | ràfega 8x15 (0.5s) | emo/build/drop 180 (6s) | cta 90 (3s)
declare -A FR=( [h1]=30 [h2]=30 [b1]=15 [b2]=15 [b3]=15 [b4]=15 [b5]=15 [b6]=15 [b7]=15 [b8]=15 [emo]=180 [build]=180 [drop]=180 [cta]=90 )
MOTION="h1 h2 emo build drop"        # plans amb push-in (Ken Burns)
ORDER="h1 h2 b1 b2 b3 b4 b5 b6 b7 b8 emo build drop cta"

zoomclip(){ # $1=id $2=frames  -> push-in suau, durada exacta per -frames:v
  ffmpeg -y -loop 1 -i "scenes/$1.png" \
    -vf "scale=1512:2688,zoompan=z='min(zoom+0.0006,1.075)':d=$2:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=$FPS" \
    -frames:v "$2" -r $FPS -c:v libx264 -preset veryfast -pix_fmt yuv420p "clips/$1.mp4" -loglevel error
}
staticclip(){ # $1=id $2=frames -> pla fix
  ffmpeg -y -loop 1 -i "scenes/$1.png" -frames:v "$2" -r $FPS \
    -vf "scale=1080:1920,setsar=1,format=yuv420p" -c:v libx264 -preset veryfast -pix_fmt yuv420p "clips/$1.mp4" -loglevel error
}

for id in $ORDER; do
  if [[ " $MOTION " == *" $id "* ]]; then zoomclip "$id" "${FR[$id]}"; else staticclip "$id" "${FR[$id]}"; fi
  echo "clip $id (${FR[$id]}f) ok"
done

# concat
: > cat.txt; for id in $ORDER; do echo "file 'clips/$id.mp4'" >> cat.txt; done
ffmpeg -y -f concat -safe 0 -i cat.txt -c copy "reel_${LANG_TAG}_SILENT.mp4" -loglevel error
echo "-> reel_${LANG_TAG}_SILENT.mp4 (per so de tendència)"

if [[ -f "$AUDIO" ]]; then
  ffmpeg -y -i "reel_${LANG_TAG}_SILENT.mp4" -i "$AUDIO" -c:v copy -c:a aac -b:a 192k -shortest "reel_${LANG_TAG}.mp4" -loglevel error
  echo "-> reel_${LANG_TAG}.mp4 (amb música)"
fi
echo "durada: $(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 reel_${LANG_TAG}_SILENT.mp4) s"
