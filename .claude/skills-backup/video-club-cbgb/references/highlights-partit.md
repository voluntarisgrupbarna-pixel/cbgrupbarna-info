# Highlights de partido

El pan de cada semana. Regla de oro: **se publica el mismo día o, como muy tarde,
al día siguiente.** Un highlight tardío pierde casi todo su valor. La velocidad
gana a la perfección aquí.

## Qué entra en un highlight

- Canastas (especialmente triples, bandejas, mates si los hay).
- Jugadas de esfuerzo: robos, tapones, rebotes ofensivos, asistencias bonitas.
- Reacción de banquillo y grada en momentos clave (construye comunidad).
- Marcador final o momento decisivo.
- Diversidad real: que salgan distintos jugadores/as, no siempre el mismo.

Lo que NO entra: jugadas borrosas, fallos largos, tiempos muertos, nada que deje
en evidencia a un menor.

## Estructura (30-90 s)

1. **Hook (0-2 s):** la mejor jugada del partido va PRIMERO, no al final. O un
   rótulo de marcador con tensión ("Quedan 12 s, empate").
2. **Cuerpo:** 4-8 jugadas en ritmo, ordenadas por intensidad creciente.
3. **Clímax:** la jugada decisiva o el triple ganador.
4. **Cierre (1-2 s):** marcador final + logo + hashtag.

## Vía A — CapCut paso a paso

1. Importa todos los clips del partido.
2. Recorta cada jugada dejando ~0,5 s antes y después (respiración).
3. Ordena por intensidad; pon la mejor la primera (hook).
4. Música con ritmo: marca el "beat" y cuadra los cortes con el golpe musical.
   CapCut → "Coincidir ritmo" ayuda.
5. Texto: rótulo de marcador arriba, nombre del jugador/a en la jugada clave.
6. Subtítulos si hay audio narrado (auto-captions de CapCut, revisa errores).
7. Transiciones mínimas: corte seco > transiciones recargadas. Evita el zoom
   "plantilla genérica".
8. Cierre con plantilla de marca (logo + hashtag).
9. Exporta 1080×1920 si va a reel; 1920×1080 para YouTube.

## Vía B — automática con ffmpeg

Si los clips están en una carpeta accesible:

```
# 1. Recorta cada jugada (repite por jugada)
scripts/cut.sh -i partido.mp4 -s 00:12:30 -e 00:12:38 -o jugada1.mp4

# 2. Monta todo con preset de highlight (música + ritmo + cierre)
scripts/montage.sh --preset highlight -m musica.mp3 -o highlight_bruto.mp4 jugada1.mp4 jugada2.mp4 jugada3.mp4

# 3. A vertical para IG (recorte centrado en la acción)
scripts/vertical.sh -i highlight_bruto.mp4 -o highlight_9x16.mp4

# 4. Subtítulos (si hay narración) y marca
scripts/subs.sh -i highlight_9x16.mp4 -o highlight_subs.mp4
scripts/brand.sh -i highlight_subs.mp4 -o 2026-06-21_senior-A_highlight_v1.mp4 --hashtag "#SomGrupBarna"
```

Para lotes (toda la jornada): pídeselo a Claude con la lista de marcas de tiempo
por partido y genera todos los highlights de una pasada.

## Errores típicos

- Highlight demasiado largo: si pasa de 90 s, sobra. Corta sin piedad.
- Mejor jugada al final: nadie llega. Va primero.
- Sin marcador/contexto: una canasta sin saber el momento no emociona.
- Publicarlo dos días tarde: ya no es noticia.
