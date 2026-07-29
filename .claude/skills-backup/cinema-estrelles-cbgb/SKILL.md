---
name: cinema-estrelles-cbgb
description: >
  Creación de vídeo CINEMATOGRÁFICO de jugadores/as como si fueran estrellas del
  deporte — el género "athlete film / hype reel" estilo Nike, NBA player edits,
  B/R. Para piezas premium: presentación de fichaje épica, intro de temporada,
  feature de una jugadora, vídeo de marca. Cubre el lenguaje cinematográfico
  (slow-mo, speed ramps, grading, planos de detalle), la estructura narrativa
  (hook → build → drop → cierre), el diseño de sonido y el brief de captura (cómo
  GRABAR para que quede cine). Cargar SIEMPRE que se pida un vídeo "épico/pro/
  cinematográfico", "estilo Nike", "presentación de estrella", "hype", "tráiler"
  de un jugador/a o equipo, aunque no se diga "cinematográfico". Es el criterio de
  alto nivel; se EJECUTA con los scripts de `video-club-cbgb` y usa
  `sistema-visual-cbgb` para tipografía/color.
---

# Athlete film — vídeo de estrella para CB Grup Barna

`video-club-cbgb` hace el vídeo operativo del día a día (highlights, reels, recaps).
Esta skill sube un escalón: convierte a un jugador/a de cantera en **una estrella en
pantalla**, con el lenguaje de los mejores edits de atleta del mundo. El diferencial
del Barna: tratar a una chica o un chico de formación con la misma épica con la que
la NBA trata a sus estrellas. Eso es, a la vez, calidad top y posicionamiento.

## Verdad nº1: lo cine se GRABA, no se rescata en edición

El 70% del resultado depende del material. No se puede grading-ear a estrella un
clip plano de móvil. Antes de prometer un vídeo épico, asegurar (o planificar) la
captura: alta velocidad de fotogramas, b-roll de detalle, planos héroe. Brief
completo en `references/brief-captura.md`. Si el material ya existe y es limitado,
decirlo y ajustar la ambición — no fingir cine.

## Los 6 ingredientes del athlete film

Lo que separa un edit de estrella de un montaje normal. Detalle y recetas en
`references/llenguatge-cinematografic.md`.

1. **Movimiento intencional:** slow-motion y **speed ramps** (rampa suave de cámara
   lenta a tiempo real). La firma del género. Requiere 60-120 fps o interpolación.
2. **Planos de detalle:** manos, zapatillas, balón, sudor, mirada, red. El detalle
   construye épica; el plano abierto, no.
3. **Grading cinematográfico:** un look de color consistente (cálido contrastado, o
   desaturado moody), alto contraste, textura/grano de film. Sin grade no hay cine.
4. **Diseño de sonido:** el sonido es el 50%. No solo música: whooshes, impactos
   (bote, swish de red, chirrido de zapatilla), una voz/quote, y la música ducking
   bajo la voz. Ver `references/llenguatge-cinematografic.md`.
5. **Tipografía cinética:** revelado del nombre, dato/dorsal, frase potente — al
   ritmo, mínima, con la tipografía de `sistema-visual-cbgb`.
6. **Transiciones invisibles:** whip pan, match cut, máscara, speed-blur. Nunca
   transiciones "preset" de plantilla.

## Estructura narrativa

Un athlete film cuenta UNA historia, no enseña clips. Estructura base (8-30 s) en
`references/estructura-narrativa.md`:

1. **Hook (0-2 s):** el plano más potente o una frase que abre tensión.
2. **Build:** sube la intensidad, planos de detalle, la música crece.
3. **Drop:** el momento — la jugada, el revelado del nombre — cuadrado con el golpe
   musical. Cortes rápidos.
4. **Cierre:** respiro + identidad (logo, nombre, temporada, hashtag).

Una pieza = una emoción (el esfuerzo, la llegada, la promesa). Si quieres contar
tres cosas, son tres piezas.

## Proceso

1. **Concepto:** define la historia y la emoción en una frase antes de tocar nada.
2. **Selecciona música** primero: el ritmo manda el montaje. Marca el "drop".
3. **Captura/selección:** aplica el brief; elige los planos héroe y el b-roll.
4. **Montaje al ritmo:** cuadra cortes y speed ramps con el beat.
5. **Grade:** aplica el look (`scripts/cinematic_grade.sh` o CapCut/DaVinci).
6. **Sonido:** capas de efectos + voz + música con ducking.
7. **Tipografía y cierre** con `sistema-visual-cbgb`.
8. **Formato y export** con `video-club-cbgb` (vertical 9:16, subtítulos si hay voz,
   marca). Filtro de calidad antes de publicar.

## Ejecución: con qué se hace

- **CapCut:** speed ramp (curva de velocidad), keyframes, filtros — para edición ágil.
- **DaVinci Resolve:** grading serio y control fino — para la pieza premium.
- **Automático (Claude + ffmpeg):** `scripts/cinematic_grade.sh` aplica look +
  grano + slow-mo, y el resto de la cadena (cortar, vertical, subs, marca, música)
  con los scripts de `video-club-cbgb`. Ideal para dar el look cine a un clip rápido.

## Filtro de calidad (antes de publicar)

1. ¿Engancha en el primer segundo? (hook real)
2. ¿Tiene un look de color consistente y a nivel? (grade)
3. ¿El sonido está diseñado, no solo "música encima"?
4. ¿Hay al menos un plano héroe y planos de detalle?
5. ¿Se reconoce como Barna (tipografía, cierre) y respeta la paridad real?

Si no supera 4 de 5, no es "estrella" todavía: reeditar. Y siempre derechos de
imagen del menor confirmados antes de publicar.

## Anti-patrones

- Grading fuerte sobre material plano (no salva un mal plano).
- Speed ramps sin fps suficiente (queda a tirones) — usar interpolación o no forzar.
- Transiciones preset llamativas (gritan "amateur").
- Música sin diseño de sonido (se queda a medias).
- Épica vacía: estética sin historia ni emoción no emociona.
