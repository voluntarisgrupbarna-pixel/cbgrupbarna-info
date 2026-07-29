# Guía de scripts ffmpeg (Vía B — automática)

Estos scripts permiten a Claude editar vídeo del club sin abrir CapCut. Viven en
`scripts/`, leen la marca de `assets/brand.conf` y necesitan `ffmpeg`
(`brew install ffmpeg`). Para subtítulos automáticos, además whisper
(`pip install openai-whisper`); si no, se pasan subtítulos con `--srt` o se usan
los auto-captions de CapCut.

Antes de usarlos, dales permiso de ejecución una vez:
`chmod +x scripts/*.sh`

## Tabla rápida

| Script | Qué hace | Ejemplo mínimo |
|---|---|---|
| `cut.sh` | Recorta un clip por tiempos | `cut.sh -i p.mp4 -s 00:12:30 -e 00:12:38 -o j.mp4` |
| `montage.sh` | Une clips + música + título | `montage.sh --preset highlight -m m.mp3 -o h.mp4 a.mp4 b.mp4` |
| `vertical.sh` | Pasa a 9:16 | `vertical.sh -i h.mp4 -o v.mp4 --mode crop` |
| `subs.sh` | Subtítulos quemados | `subs.sh -i v.mp4 -o s.mp4 --lang ca --safe-zone` |
| `brand.sh` | Logo + cierre + lower-third | `brand.sh -i s.mp4 -o final.mp4 --hashtag "#SomGrupBarna"` |

## Detalles por script

### cut.sh
Recorta con re-encode (corte preciso al frame). `-s` inicio, `-e` fin o `-d`
duración. Acepta `HH:MM:SS` o segundos.

### montage.sh
Normaliza todos los clips a la misma resolución/fps antes de unir — esto evita el
fallo clásico de `concat` cuando los clips vienen de cámaras distintas. Acepta
imágenes (`.jpg/.png`) y las convierte en 3 s de vídeo (útil para welcome de
fichaje a partir de foto). Presets: `highlight`/`reel`/`feature` → 1080×1920;
`recap` → 1920×1080. `-m` añade música mezclada y normaliza el audio a -14 LUFS.
`--title` rotula los primeros 3 s.

### vertical.sh
`--mode crop` (recorte centrado, rellena pantalla), `blur` (vídeo entero sobre su
fondo difuminado, no recorta acción), `pad` (barras de color de marca). Para
deporte, `crop` suele ser mejor si la acción está centrada; `blur` si no quieres
perder los lados.

### subs.sh
Transcribe con whisper si está instalado (idioma por defecto `ca`). `--safe-zone`
sube los subtítulos ~380 px para que la UI de Instagram no los tape. Revisa
siempre la transcripción automática: nombres propios y términos de baloncesto
suelen salir mal.

### brand.sh
Pone la marca de agua (logo de `brand.conf`), un cierre con hashtag + CTA en los
últimos 2 s, y opcionalmente un lower-third (`--lower-third "Nombre · Rol"`). Para
recaps con varios logos de sponsors (`--logos`), pídele a Claude que componga el
bloque de cierre a medida con la jerarquía correcta.

## Recetas completas

**Highlight de partido para IG (de un vídeo largo):**
```
chmod +x scripts/*.sh
scripts/cut.sh -i partido.mp4 -s 00:05:10 -e 00:05:18 -o j1.mp4
scripts/cut.sh -i partido.mp4 -s 00:18:02 -e 00:18:12 -o j2.mp4
scripts/montage.sh --preset highlight -m musica.mp3 -o bruto.mp4 j1.mp4 j2.mp4
scripts/subs.sh -i bruto.mp4 -o subs.mp4 --safe-zone
scripts/brand.sh -i subs.mp4 -o 2026-06-21_senior-A_highlight_v1.mp4
```

**Clip horizontal → reel vertical limpio:**
```
scripts/vertical.sh -i clip.mp4 -o v.mp4 --mode crop
scripts/brand.sh -i v.mp4 -o reel.mp4 --hashtag "#SomGrupBarna" --cta "Apúntate al Campus"
```

**Recap de evento (doble salida):**
```
scripts/montage.sh --preset recap -m musica.mp3 --title "3x3 Westfield · 4a edició" -o recap_16x9.mp4 c1.mp4 c2.mp4 c3.mp4
scripts/brand.sh -i recap_16x9.mp4 -o 2026-07-19_3x3_recap_v1.mp4 --hashtag "#3x3GrupBarna"
scripts/vertical.sh -i 2026-07-19_3x3_recap_v1.mp4 -o recap_9x16.mp4 --mode blur
```

## Cómo se lo pides a Claude

No hace falta que escribas los comandos. Basta con: "tengo el partido del sábado
en la carpeta, sácame 4 highlights de estos momentos [lista de tiempos] en
vertical con subtítulos y logo". Claude ejecuta los scripts por ti y te devuelve
los archivos listos.
