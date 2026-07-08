#!/usr/bin/env bash
# Talla un vídeo llarg de partit en segments per importar a CapCut
# Ús: ./partit-a-segments.sh video.mp4 [durada_segment_en_segons]
# Exemple: ./partit-a-segments.sh partit_senior_2025.mp4 120

INPUT="${1:?Indica el fitxer de vídeo com a primer argument}"
SEG="${2:-120}"  # durada per defecte: 2 minuts per segment
BASENAME="${INPUT%.*}"
OUTPUT_DIR="${BASENAME}_segments"

mkdir -p "$OUTPUT_DIR"

ffmpeg -i "$INPUT" \
  -c copy \
  -map 0 \
  -segment_time "$SEG" \
  -f segment \
  -reset_timestamps 1 \
  "${OUTPUT_DIR}/${BASENAME}_%03d.mp4"

echo "Segments guardats a: $OUTPUT_DIR"
echo "Importa la carpeta completa a CapCut amb 'Afegir' → seleccionar tots els clips"
