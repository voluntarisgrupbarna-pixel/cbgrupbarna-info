# Player features (presentación de jugadores/as y equipos)

Piezas que ponen cara y nombre a la comunidad: fichajes, presentación de equipos,
"jugadora de la semana", entrevistas cortas, despedidas. Refuerzan el pilar
formativo y humanizan la marca. 20-45 s, 9:16 o 16:9.

## Tipos

- **Welcome / fichaje:** "Benvinguda al Grup Barna". Nombre, posición, foto/clip.
- **Presentación de equipo:** al inicio de temporada, uno por equipo.
- **Jugador/a destacado/a:** semanal, sobre la mejor actuación.
- **Mini-entrevista:** 1-2 preguntas, respuesta corta sobre acción de fondo.
- **Progreso/formación:** antes/después, evolución (pilar formativo puro).
- **Despedida/agradecimiento:** cuando alguien deja el club.

## Estructura (20-45 s)

1. **Identificación (0-3 s):** rostro + nombre + rol en rótulo claro. El protagonista
   humano es lo primero (filtro de marca nº4).
2. **Sustancia (3-35 s):** acción del jugador/a + dato o quote. Una sola idea.
3. **Cierre:** logo + hashtag. Si es fichaje, "Benvingut/da" + temporada.

## Reglas Barna

- **Plano corto cuando hay emoción** (criterio de fotografía del club).
- **Diversidad real:** alterna chicas y chicos, edades, equipos. La paridad es un
  diferencial del club; que se note en el contenido.
- Subtítulos siempre (entrevistas: subtitular toda la respuesta).
- Foto/clip de calidad: nada borroso ni con horizonte torcido.
- Rótulo de nombre con tipografía del sistema, consistente entre todas las piezas
  de la serie (si entra al sistema, se versiona).

## Vía A — CapCut

1. Lienzo según destino (9:16 reel / 16:9 web).
2. Abre con rostro + rótulo de nombre y rol.
3. Si hay entrevista: subtitula toda la respuesta, deja respirar el audio.
4. Acción de fondo o B-roll del jugador/a jugando.
5. Música suave de fondo si es entrevista (no tape la voz); con ritmo si es highlight.
6. Cierre con plantilla de marca.
7. Exporta.

## Vía B — automática

```
# Entrevista: subtitular respuesta + rótulo de nombre + marca
scripts/subs.sh -i entrevista.mp4 -o entrevista_subs.mp4
scripts/brand.sh -i entrevista_subs.mp4 -o jugadora_feature.mp4 \
  --lower-third "Maria G. · Base · Sénior femení" --hashtag "#SomGrupBarna"

# Welcome de fichaje a partir de foto + clip
scripts/montage.sh --preset feature --title "Benvinguda, Maria" \
  -m musica.mp3 -o welcome.mp4 foto.jpg clip_accio.mp4
scripts/vertical.sh -i welcome.mp4 -o welcome_9x16.mp4
```

## Serie y consistencia

Las player features funcionan como **serie**: mismo rótulo, misma estructura, mismo
cierre, cambia el protagonista. Eso construye un sistema reconocible. Guarda una
plantilla CapCut y/o reutiliza `brand.sh --lower-third` con el mismo estilo para
toda la temporada.
