---
name: video-estrella-cbgb
description: "Editor de video NIVELL ELIT (hype edits estil NBA/Nike/433): fitxatge epic, hype de jugadora, intro de temporada, MVP, homenatge/testimonial. Recepta exacta (hook, beat-sync, speed ramps, tipografia cinetica, color grade, so) executada en CapCut o ffmpeg. Carregar sempre que es demani un video \"epic/pro/cinematografic\", \"estil Nike\", \"hype\", \"homenatge/despedida de...\" encara que no es digui \"cinematografic\". Complementa video-club-cbgb, usa sistema-visual-cbgb."
---

# Vídeo estrella — CB Grup Barna

Objetivo: que un vídeo del club se confunda con el de un club profesional. La estética
de "estrella del deporte" no es un filtro: es **ritmo + momento + sonido + tipografía**.
Esta skill es la receta. El criterio de marca (rojo/negro, tipografía, logo) vive en
`sistema-visual-cbgb`; el flujo de trabajo general en `video-club-cbgb`.

## Qué hace que un edit parezca "de estrella" (los 6 ingredientes)

1. **Hook brutal en 0–1,5 s.** El frame más potente primero (un gesto, un tiro, una
   mirada a cámara), sin intro lenta. Texto corto y grande encima ("LA NUEVA 12",
   "ELLA NO PARA"). Si el primer segundo no para el scroll, se reedita.
2. **Beat-sync.** Cada corte cae en el golpe de la música. Marca los beats y corta ahí.
   Es lo que más sube la percepción de calidad. Sin beat-sync no es un edit estrella.
3. **Speed ramps.** Rampa de velocidad: entra rápido → cae a slow-mo en el momento
   clave (el tiro entra, el bote, la celebración) → vuelve a velocidad. Da dramatismo.
4. **Transiciones con energía** (no fundidos suaves): whip/zoom-blur, flash blanco,
   golpe a negro, glitch/RGB split en los cambios fuertes. Discretas dentro de una
   idea, fuertes al cambiar de bloque.
5. **Tipografía cinética.** Texto que aparece con pop/escala, condensada, mayúsculas,
   alto contraste, alineada a la rejilla. Pocas palabras, muy grandes. Acento rojo.
6. **Color grade + sound design.** Contraste alto, sombras profundas, rojos saturados
   (ADN Barna), un punto de glow. Audio: whoosh en los whips, impacto grave en los
   cortes fuertes, música a ~-14 LUFS.

## Antes de empezar — 4 decisiones

1. **Formato:** fichaje / hype jugadora / intro equipo / captación / recap / MVP /
   countdown. (Cada uno tiene su estructura abajo.)
2. **Material:** ¿fotos de estudio, clips de partido, o mezcla? Determina si hay
   movimiento real (clips) o hay que crearlo (Ken Burns + transiciones sobre fotos).
3. **Quién edita:** CapCut (Ana/equipo, toque creativo) o ffmpeg (Claude, lotes y
   repetición). Recomendado **híbrido**: Claude monta la base, persona da el remate.
4. **Derechos de imagen de menores.** Innegociable: si hay dudas, no se publica.

## Estructuras por formato (timeline)

**Hype de jugadora / fichaje (15–25 s, 9:16)**
- 0–1,5 s **Hook**: mejor frame + nombre/dorsal gigante, flash de entrada.
- 1,5–10 s **Subida**: 4–6 clips/fotos beat-sync, speed ramp en el mejor gesto.
- 10–18 s **Clímax**: el momento (canasta/celebración) en slow-mo + texto clave.
- 18–25 s **Cierre marca**: logo + hashtag + CTA, golpe final a beat.

**Intro de equipo / captación (20–30 s, 9:16)**
- Cover potente (foto hero + titular gigante + "mira hasta el final").
- Bloques por equipo/jugadora, 1,3–1,8 s cada uno, **corte a beat**, transición fuerte
  al cambiar de equipo (whip/flash), suave dentro del equipo.
- Cierre con identidad y llamada a la acción.

**Recap de partido/evento (30–60 s)**
- Hook con la mejor jugada del día → montaje beat-sync → pico emocional en slow-mo →
  marcador/resultado → cierre marca.

**Countdown / MVP / "jugada del día"**: 1 idea, 1 frase, 1 momento. 8–15 s.

**Homenaje / despedida / testimonial (35–50 s, 9:16)** — voces a cámara, tipo tributo.
El ritmo aquí no es de acción sino **emocional**: cortes a beat entre testimonios que
construyen hacia una frase final. Referencia del género: los tributos de despedida
(varias personas hablando a cámara de alguien, subtítulos, y un remate emotivo).
- **Estructura:** 4–8 cortes cortos de gente hablando a cámara (compañeras, cuerpo
  técnico, familia, la propia protagonista), unidos por una **pregunta común** ("¿Qué
  es para ti Marina?") para que las respuestas tejan una historia.
- **Subtítulos quemados OBLIGATORIOS** (casi todo se ve en silencio): grandes, blancos,
  con contorno/sombra, fuente limpia. Usa `subs.sh` de `video-club-cbgb` o los
  auto-subtítulos de CapCut, siempre revisados a mano.
- **Ritmo:** corta a beat al cambiar de voz; recorta los "eeeh" y silencios muertos;
  intercala 1–2 planos de detalle/BTS/archivo (manos, escudo, un momento real) para
  respirar.
- **Construcción emocional:** ordena las respuestas de menos a más emotivo y **guarda la
  frase potente para el final**. Un cierre tipo "GRÀCIES, CAPITANA" / "SEMPRE DEL CLOT".
- **Audio:** las **voces mandan** (limpias, sin saturar); música por debajo con
  **ducking** (−8/−10 dB bajo la voz), un tema cálido pero con pulso.
- **Cierre:** la frase clave sobre negro + escudo + nombre + claim. Corte final + un
  respiro de silencio.
- **Casos Barna:** despedida de jugadora/entrenador, "leyenda del Barna", bienvenida
  emotiva de fichaje, reconocimiento, o el 60è aniversari (voces de socias históricas).
- Para el cuidado de la entrevista (planos, luz, cómo grabar los testimonios), empareja
  con `cinema-estrelles-cbgb`.

## Vía CapCut (manual) — receta exacta

1. Importa material. Pon la música primero y activa **"Marcar beats"** (icono de
   golpe). Corta cada clip para que el corte caiga en un beat.
2. **Speed ramp:** clip → Velocidad → Curva → preset "Montaje"/"Flash in". Ajusta para
   que el slow caiga en el momento clave.
3. **Transiciones:** entre bloques usa "Zoom", "Whip", "Glitch", "Flash". Mantén
   duración corta (0,2–0,4 s).
4. **Texto:** fuente condensada bold, mayúsculas, blanco con borde/sombra, acento rojo
   #E3001B. Animación de entrada "Escala" o "Pop". Pocas palabras.
5. **Color:** Ajustes → contraste +, luces -, sombras -, saturación + (sube rojos).
   Opcional viñeta sutil.
6. **Sonido:** añade whoosh en cada whip y un "impact" en los cortes fuertes
   (biblioteca de CapCut). Sube la música, baja -3/-4 dB en momentos con voz.
7. Cierre: logo + hashtag de campaña en los últimos 1–2 s, corte final a beat.
8. Exporta 1080×1920, 30 fps, calidad alta.

## Vía ffmpeg (automático) — qué puede montar Claude

Sobre fotos de estudio (sin clips de vídeo) se recrea el "movimiento":
- **Ken Burns** (zoom/pan lento) por foto para que no sea estática.
- **Transiciones** xfade variadas: `slideleft/right/up`, `circleopen/close`, `pixelize`,
  `hrslice`, `smoothleft`, `fadeblack/white` (flash). Fuertes en cambio de bloque.
- **Lower-third** y titulares con `drawtext` (condensada, acento rojo, panel translúcido).
- **Beat-sync aproximado:** fijar la duración de cada foto = duración entre beats de la
  música elegida (p. ej. 120 BPM → 0,5 s/beat; 2 beats por foto = 1,0 s).
- **Flash a beat:** insertar 1–2 frames blancos en los golpes fuertes.
- Cierre con identidad (logo + hashtag).
Ver recetas y comandos en `references/recetas-ffmpeg.md`.

Para el formato **homenaje/testimonial** (voz real, no fotos), lo automatizable es el
**quemado de subtítulos** (`subs.sh`), el **corte rítmico** (`cut.sh`) y el **cierre de
marca** (`brand.sh`) de `video-club-cbgb`; el montaje de las voces y su orden emocional
lo hace la persona (una máquina no sabe qué respuesta emociona más). Receta paso a paso
en `references/recetas-ffmpeg.md`.

Limitación real: con fotos fijas no hay slow-mo real ni acción; el "hype" se logra con
ritmo de cortes a beat + transiciones + tipografía. Para edits estrella de verdad,
graba **clips verticales** (móvil en mano, 60 fps para poder hacer slow-mo).

## Filtro de calidad (pasa 5/5 o se reedita)

1. ¿El primer segundo para el scroll?
2. ¿Los cortes caen en la música (beat-sync)?
3. ¿Hay al menos un momento en slow-mo / un pico?
4. ¿La tipografía es grande, limpia y de marca (rojo/negro)?
5. ¿Se reconoce como Barna y cierra con logo + CTA?

**Filtro extra para homenaje/testimonial:**
1. ¿Se **leen** los subtítulos en silencio? (pruébalo en mute)
2. ¿Se **entienden** las voces (audio limpio, no saturado, con ducking)?
3. ¿Hay una **frase final** que emociona (clímax guardado para el final)?
4. ¿Los cortes caen a **beat** y sin "eeeh"/silencios muertos?
5. **Consentimiento y derechos de imagen** (menores incluidos) confirmados.

## Specs de exportación

- IG Reel/Story: 1080×1920, H.264, 30 fps, AAC, audio ~-14 LUFS, <90 s, 8–12 Mbps.
- Nombre: `AAAA-MM-DD_equipo_formato_vX.mp4`.

## Nota de honestidad sobre referencias

Esta skill recoge las **técnicas del género** de hype edits de estrellas del deporte
(NBA/Nike/433/selecciones). Si quieres clonar un reel concreto, dime en texto qué tiene
(ritmo, tipo de transición, si hay slow-mo, estilo de texto) y se ajusta la receta, ya
que los enlaces de Instagram no se pueden abrir desde aquí.
