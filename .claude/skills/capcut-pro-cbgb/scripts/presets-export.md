# Presets d'exportació CapCut — CB Grup Barna

## Preset A — Reel estàndard (Instagram / TikTok / YouTube Shorts)
- Resolució: 1080 × 1920 (vertical 9:16)
- FPS: 30
- Format: H.264 / MP4
- Qualitat: Alta (CapCut → "Recomanada" o "1080p")
- Quan usar: highlights, reels de fichatge, clips de campus

## Preset B — Vídeo horitzontal llarg (YouTube / pantalla pavelló)
- Resolució: 1920 × 1080 (horitzontal 16:9)
- FPS: 60 (acció viva) / 30 (contingut institucional)
- Format: H.264 / MP4
- Qualitat: Alta
- Quan usar: vídeos de temporada, cerimònies, resums institucionals

## Preset C — WhatsApp / distribució interna
- Resolució: 1280 × 720
- FPS: 30
- Format: H.264 / MP4
- Mida objectiu: <50 MB
- Quan usar: comunicats interns, contingut per al grup de WhatsApp del club

## Preset D — Web (cbgrupbarna.info)
- Resolució: 1280 × 720
- FPS: 30
- Format: H.264 / MP4
- Mida objectiu: <20 MB (comprimir amb ffmpeg si cal)
- Comanda ffmpeg de compressió:
  `ffmpeg -i entrada.mp4 -vcodec libx264 -crf 28 -preset slow sortida_web.mp4`

## Nomenclatura de fitxers exportats
Format: `AAAAMMDD_tipus_equip_versio.mp4`
Exemples:
- `20250915_highlight_senior-fem_v1.mp4`
- `20250920_fichatge_junior-masc_v1.mp4`
- `20251001_campus_escoles_v2.mp4`
