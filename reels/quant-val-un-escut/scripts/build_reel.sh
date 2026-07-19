#!/usr/bin/env bash
# Ús: ./build_reel.sh   (executa compose_scenes.py abans si cal regenerar les escenes)
set -e
cd "$(dirname "$0")/.."   # arrel de reels/quant-val-un-escut/
FPS=30
mkdir -p clips

# durades ajustades EXACTAMENT a la veu en off (ES) generada amb Higgsfield seed_audio:
# s0=3.10s s1=2.58s s2=2.17s s3=3.08s s4=4.18s s5=2.20s s6=1.34s (+ marges + espera final de 2s a s6)
declare -A FR=( [s0_hook]=114 [s1_stat61]=92 [s2_stat34]=80 [s3_stat450]=107 [s4_build]=140 [s5_drop]=87 [s6_cta]=106 )
declare -A ZMAX=( [s0_hook]=1.09 [s1_stat61]=1.10 [s2_stat34]=1.10 [s3_stat450]=1.08 [s4_build]=1.04 [s5_drop]=1.06 [s6_cta]=1.00 )
ORDER="s0_hook s1_stat61 s2_stat34 s3_stat450 s4_build s5_drop s6_cta"

zoomclip(){ # $1=id $2=frames $3=zmax
  ffmpeg -y -loop 1 -i "scenes/$1.png" \
    -vf "scale=1512:2688,zoompan=z='min(zoom+0.0007,$3)':d=$2:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=$FPS" \
    -frames:v "$2" -r $FPS -c:v libx264 -preset veryfast -pix_fmt yuv420p "clips/$1.mp4" -loglevel error
}

for id in $ORDER; do
  zoomclip "$id" "${FR[$id]}" "${ZMAX[$id]}"
  echo "clip $id (${FR[$id]}f) ok"
done

: > cat.txt; for id in $ORDER; do echo "file 'clips/$id.mp4'" >> cat.txt; done
ffmpeg -y -f concat -safe 0 -i cat.txt -c copy "reel_ca_SILENT.mp4" -loglevel error
echo "-> reel_ca_SILENT.mp4"
echo "durada: $(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 reel_ca_SILENT.mp4) s"
