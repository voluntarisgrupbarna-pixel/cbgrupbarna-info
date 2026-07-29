# Recap de evento (3x3 Westfield, Campus de verano)

Vídeo resumen que captura la energía de un evento entero en 30-60 s. Doble salida:
versión 9:16 para reels/stories y versión 16:9 para web/YouTube y para enviar a
prensa, distrito y patrocinadores.

## Para qué sirve un recap

- **Memoria del evento** que se reutiliza todo el año.
- **Activo para patrocinadores:** demuestra alcance y calidad (mete sus logos con
  jerarquía en el cierre, no pegados de cualquier manera).
- **Material para prensa y distrito** (Comunicació Sant Martí).
- **Prueba social** para captar inscripciones la próxima edición.

## Qué grabar durante el evento (brief de captura)

Para que el recap salga bien, hay que grabar pensando en el montaje:

- Plano general del recinto lleno (alcance, ambiente).
- Detalles: balón, canasta, dorsales, cartelería con marca y sponsors.
- Caras: jugadores/as, familias, público, staff. Emoción real.
- Acción: las mejores jugadas del día.
- Momentos de comunidad: entrega de premios, celebraciones, backstage.
- Un par de planos con el logo del club y de Westfield/sponsors bien visibles.

## Estructura (30-60 s)

1. **Apertura (0-3 s):** rótulo con nombre + fecha del evento sobre el plano más
   espectacular. "3x3 Westfield · 4a edició".
2. **Energía (3-15 s):** ráfaga rápida de ambiente y acción, ritmo alto.
3. **Corazón (15-45 s):** mezcla acción + comunidad + emoción. Aquí respira un poco.
4. **Cierre (últimos 5-10 s):** logos (club + Westfield + sponsors con jerarquía),
   hashtag, agradecimiento, y CTA o "Ens veiem l'any que ve".

## Vía A — CapCut

1. Selecciona los 15-25 mejores clips. Menos es más.
2. Música que construya (empieza suave, sube). Cuadra cortes con el ritmo.
3. Rótulo de apertura con marca.
4. Monta por bloques: ambiente → acción → comunidad → cierre.
5. Subtítulos en frases clave / agradecimientos.
6. Cierre con bloque de logos (jerarquía: club grande, Westfield, sponsors).
7. Exporta dos versiones: 9:16 y 16:9 (reencuadra el texto en cada una).

## Vía B — automática

```
# Montaje con preset de recap (curva de música, apertura, cierre)
scripts/montage.sh --preset recap -m musica.mp3 \
  --title "3x3 Westfield · 4a edició" \
  -o recap_16x9.mp4 clip1.mp4 clip2.mp4 ... clipN.mp4

# Marca con bloque de logos (club + sponsors)
scripts/brand.sh -i recap_16x9.mp4 -o 2026-07-19_3x3-westfield_recap_v1.mp4 \
  --logos "logo_club.png,logo_westfield.png" --hashtag "#3x3GrupBarna"

# Versión vertical para IG
scripts/vertical.sh -i 2026-07-19_3x3-westfield_recap_v1.mp4 -o recap_9x16.mp4 --mode blur
```

## Timing (encaja con el playbook del evento)

- Teaser corto el mismo día del evento (genera FOMO para la próxima).
- Recap completo en 24-72 h, mientras la gente aún habla del evento.
- Versión "sponsor" (con sus logos destacados) para enviarles como retorno.

## Errores típicos

- Recap demasiado largo (>90 s): nadie lo termina.
- Logos de sponsors pegados sin jerarquía: queda amateur y molesta al sponsor.
- Solo acción, sin comunidad: pierdes el ángulo emocional que diferencia al club.
- Publicarlo una semana tarde: el momento ya pasó.
