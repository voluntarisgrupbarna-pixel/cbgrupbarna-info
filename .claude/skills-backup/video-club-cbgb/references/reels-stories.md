# Reels y Stories (9:16)

Prioridad absoluta del funnel top. Formato vertical 1080×1920. Duración 7-30 s
para reels; stories pueden ser fragmentos sueltos de 5-15 s.

## La regla de los 2 segundos

Si no engancha en los 2 primeros segundos, se reescribe. El hook puede ser:
movimiento fuerte, una pregunta en texto, una cifra ("+450 famílies"), un rostro
con emoción, o el momento más espectacular puesto al principio.

## Estructura de un reel (7-30 s)

1. **Hook (0-2 s):** lo más potente. Nunca una intro lenta.
2. **Desarrollo (2-20 s):** 3-6 planos cortos, ritmo alto, un solo mensaje.
3. **Cierre (últimos 2 s):** logo + hashtag + CTA si aplica ("Apúntate al Campus").

Un reel = una idea. Si quieres contar tres cosas, son tres reels.

## Reglas de estilo Barna

- **Subtítulos siempre**, grandes, legibles, en zona segura (ni muy arriba ni
  tapados por la UI de IG). Tipografía del sistema del club.
- **Música actual y con ritmo.** Cuadra los cortes con el beat. Nada de música
  "de stock genérica".
- **Texto en zona segura:** deja ~250 px arriba y ~350 px abajo libres de texto
  importante (los tapan los iconos de IG).
- **Vertical nativo.** Si el material es 16:9, usa recorte centrado en la acción
  (`vertical.sh`), no barras negras. Fondo difuminado solo si el plano lo pide.
- Cierre con identidad visible.

## Vía A — CapCut

1. Lienzo 9:16. Importa clips.
2. Coloca el hook primero. Recorta agresivo: fuera todo lo que no aporte.
3. "Coincidir ritmo" para cuadrar cortes con la música.
4. Auto-subtítulos → revisa errores → aplica estilo de marca (color, tamaño,
   posición en zona segura).
5. Añade rótulos de apoyo solo si suman.
6. Cierre con plantilla de marca.
7. Exporta 1080×1920, 30 fps.

## Vía B — automática

```
# De un clip horizontal a reel vertical con subtítulos y marca
scripts/vertical.sh -i clip.mp4 -o clip_9x16.mp4 --mode crop
scripts/subs.sh -i clip_9x16.mp4 -o clip_subs.mp4 --safe-zone
scripts/brand.sh -i clip_subs.mp4 -o reel.mp4 --hashtag "#SomGrupBarna" --cta "Apúntate"

# O montar varios planos cortos en un reel con música
scripts/montage.sh --preset reel -m musica.mp3 -o reel.mp4 plano1.mp4 plano2.mp4 plano3.mp4
```

## Tipos de reel que funcionan para el club

- Jugada espectacular suelta + reacción.
- "Behind the scenes": vestuario, calentamiento, viaje (construye comunidad y marca).
- Antes/después, progreso de un jugador/a (formación).
- Cobertura de evento en caliente (3x3, Campus).
- Quote de coach o jugador/a sobre vídeo de acción.
- Anuncio (Campus, evento) con CTA claro.
