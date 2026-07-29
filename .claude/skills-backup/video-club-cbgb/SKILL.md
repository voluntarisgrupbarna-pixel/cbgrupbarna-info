---
name: video-club-cbgb
description: >
  Edición de vídeo para CB Grup Barna: highlights de partido, reels/stories de
  Instagram (9:16), recaps de evento (3x3 Westfield, Campus) y player features.
  Cubre las dos vías de trabajo: (A) edición manual en CapCut con recetas paso a
  paso y (B) edición automática que Claude ejecuta con ffmpeg (cortar, montar,
  pasar a vertical, poner logo/marca de agua, subtítulos, música). Úsala SIEMPRE
  que se hable de editar, montar o exportar vídeo del club: "monta un highlight",
  "pásame esto a reel vertical", "haz un recap del 3x3", "ponle el logo y
  subtítulos a este clip", "vídeo de presentación de jugadora", aunque no se diga
  la palabra "editar". Combinar con disseny-estetic-club para criterio visual.
---

# Edición de vídeo — CB Grup Barna

Convierte material en bruto (clips de móvil, cámara, grabaciones de partido) en
piezas publicables que se reconocen como Barna en 0,5 segundos. La estética es
posicionamiento: una pieza floja rompe el relato "formativo + élite". El criterio
visual vive en `disseny-estetic-club`; **esta skill es el cómo de la ejecución**.

## Dos vías de trabajo

Elige según quién tiene el material y quién edita:

- **Vía A — CapCut (Ana/equipo edita).** Recetas paso a paso, plantillas y ajustes
  exactos para montar rápido en CapCut móvil o escritorio. Úsala cuando el material
  está en el teléfono o cuando quien edita es una persona del club.
- **Vía B — Automática (Claude edita con ffmpeg).** Si los archivos de vídeo están
  en una carpeta accesible (workspace o carpeta conectada), Claude corta, monta,
  pasa a vertical, pone logo, subtítulos y música ejecutando `scripts/`. Úsala para
  lotes (10 highlights de la jornada), para tareas repetitivas y cuando se quiere
  el resultado sin tocar CapCut.

Casi siempre conviene un **flujo híbrido**: Claude hace el trabajo pesado y
repetitivo (cortar, formatear, marca de agua a 30 clips), y la persona da el toque
final creativo en CapCut. Propón el híbrido cuando encaje.

## Antes de empezar — 4 preguntas

1. **¿Qué formato?** highlight de partido / reel-story / recap de evento / player
   feature. Cada uno tiene su `references/`.
2. **¿Dónde se publica?** IG feed (1:1 o 4:5), IG reel/story (9:16), YouTube/web
   (16:9). Define relación de aspecto y duración.
3. **¿Dónde está el material y quién edita?** decide Vía A o B (ver arriba).
4. **¿Hay derechos de imagen de los menores que salen?** Si hay dudas, no se
   publica hasta confirmarlo. El club trabaja con menores; esto es innegociable.

## Identidad de marca (config del club)

Los valores oficiales (paleta exacta, tipografía, logo) están en el knowledge
"Barna" y en `disseny-estetic-club`. Antes de la primera edición de una sesión,
rellena `assets/brand.conf` con las rutas y colores reales. Los scripts lo leen.
Si no existe el logo en disco, pídeselo a Ana o usa solo el lower-third de texto.

Reglas no negociables de marca en vídeo:

- **Subtítulos siempre.** La mayoría ve sin sonido. Sin subtítulos, no se publica.
- **Cierre con identidad:** logo + hashtag de campaña en los últimos 1-2 s.
- **Logo/marca de agua** presente pero discreto (esquina, opacidad ~85%).
- **Hook en los 2 primeros segundos** o el reel se reescribe.
- **Mismo ADN visual** entre feed y reels (misma paleta, misma tipografía de
  subtítulo). La inconsistencia rompe marca más que un error puntual.

## Routing por formato

Lee el reference del formato que toque antes de editar:

| Formato | Reference | Aspecto | Duración típica |
|---|---|---|---|
| Highlights de partido | `references/highlights-partit.md` | 9:16 (IG) o 16:9 (YouTube) | 30-90 s |
| Reels / Stories | `references/reels-stories.md` | 9:16 | 7-30 s |
| Recap de evento | `references/recap-esdeveniment.md` | 9:16 + 16:9 | 30-60 s |
| Player features | `references/player-features.md` | 9:16 o 16:9 | 20-45 s |

## Scripts (Vía B — automática)

En `scripts/`. Todos imprimen ayuda con `-h`. Requieren `ffmpeg` instalado
(`brew install ffmpeg`). Claude los ejecuta desde el sandbox sobre archivos de la
carpeta conectada. Detalle de uso en `references/scripts-ffmpeg.md`.

- `cut.sh` — recorta un clip por marcas de tiempo (la jugada limpia).
- `montage.sh` — concatena varios clips + intro/outro + música en un montaje.
- `vertical.sh` — pasa 16:9 a 9:16 (recorte centrado o fondo difuminado).
- `brand.sh` — aplica logo/marca de agua y cierre con identidad.
- `subs.sh` — genera y quema subtítulos (transcripción automática + estilo Barna).

Flujo típico de un highlight automático:
`cut.sh` (cada jugada) → `montage.sh` (unir + música) → `vertical.sh` (si va a IG)
→ `subs.sh` → `brand.sh`. O todo de una con `montage.sh --preset highlight`.

## Filtro mínimo antes de exportar (de disseny-estetic-club)

1. ¿Se reconoce como Barna sin ver el logo? (sistema visible)
2. ¿Aporta al pilar de contenido que toca?
3. ¿Está al nivel técnico de un club top? (sin horizonte torcido, sin clips borrosos)
4. ¿Hay protagonista humano identificable?
5. ¿Engancha en los 2 primeros segundos?

Si no supera 4 de 5, se reedita antes de publicar.

## Especificaciones de exportación

- **IG Reel/Story (9:16):** 1080×1920, H.264, 30 fps, audio AAC, <90 s, ~8-12 Mbps.
- **IG Feed (4:5):** 1080×1350. **(1:1):** 1080×1080.
- **YouTube/web (16:9):** 1920×1080, 24-30 fps.
- Audio normalizado a ~ -14 LUFS para que no suene bajo en IG.
- Nombre de archivo: `AAAA-MM-DD_equipo_formato_vX.mp4` (ej.
  `2026-06-21_3x3-westfield_recap_v1.mp4`) para el DAM por temporada > equipo > evento.
