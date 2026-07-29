#!/usr/bin/env bash
# subs.sh — genera subtítulos automáticos y los "quema" con estilo Barna.
# Uso: subs.sh -i in.mp4 -o out.mp4 [--lang ca|es] [--safe-zone] [--srt archivo.srt]
#   Si pasas --srt usa ese archivo. Si no, intenta transcribir con whisper
#   (pip install openai-whisper, requiere modelo). Sin whisper, avisa y sale.
#   --safe-zone sube los subtítulos para no chocar con la UI de IG.
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"

IN=""; OUT=""; LANG="ca"; SAFE=0; SRT=""
usage(){ grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }
while [ $# -gt 0 ]; do case "$1" in
  -i) IN="$2"; shift 2;; -o) OUT="$2"; shift 2;;
  --lang) LANG="$2"; shift 2;; --safe-zone) SAFE=1; shift;;
  --srt) SRT="$2"; shift 2;; -h|--help) usage 0;; *) die "opción: $1";; esac; done

need_ffmpeg
[ -n "$IN" ] && [ -f "$IN" ] || die "falta -i entrada válida"
[ -n "$OUT" ] || die "falta -o salida"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

# Transcribe si no hay SRT
if [ -z "$SRT" ]; then
  if command -v whisper >/dev/null 2>&1; then
    echo "Transcribiendo con whisper ($LANG)..."
    whisper "$IN" --language "$LANG" --model small --output_format srt --output_dir "$TMP" >/dev/null 2>&1
    SRT="$(ls "$TMP"/*.srt 2>/dev/null | head -1)"
  fi
fi
[ -n "$SRT" ] && [ -f "$SRT" ] || die "no hay subtítulos. Pasa --srt archivo.srt, o instala whisper (pip install openai-whisper), o usa los auto-subtítulos de CapCut."

# Estilo: blanco, contorno, posición en zona segura si se pide
MARGINV=60; [ "$SAFE" -eq 1 ] && MARGINV=380
COL="&H00FFFFFF"; OUTL="&H00000000"
STYLE="FontSize=22,PrimaryColour=${COL},OutlineColour=${OUTL},BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=${MARGINV}"

ffmpeg -y -i "$IN" -vf "subtitles='${SRT}':force_style='${STYLE}'" \
  -c:v libx264 -crf 19 -preset medium -c:a copy "$OUT"
echo "OK -> $OUT  (subtítulos quemados)"
