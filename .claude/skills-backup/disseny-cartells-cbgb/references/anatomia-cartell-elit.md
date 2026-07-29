# Anatomía de un cartel de élite

Desglose de las partes de un póster deportivo top y cómo tratarlas. Pensar el
cartel por **capas**, de fondo a frente.

## Capa 1 — Fondo

- Color plano de marca (de `tokens.conf`), no degradado genérico.
- Para look NBA/Nike: fondo oscuro (`COLOR_FONS_FOSC`) que hace saltar al
  protagonista y a la tipografía.
- Opcional: textura sutil, patrón geométrico de marca, o foto de pista muy
  desaturada. Sutil = élite; saturado = ruido.

## Capa 2 — Protagonista

- Foto del jugador/a **recortada del fondo**, sin halos.
- Alto contraste; opcional duotono con la paleta para unificar la serie.
- Tamaño grande: ocupa una porción dominante. Sangra por un borde si hace falta
  (más dinámico que flotando en el centro).
- Si no hay foto buena, el protagonista pasa a ser la **tipografía**.

## Capa 3 — Tipografía

- **Titular:** display condensada, mayúsculas, enorme (`TYPE_TITULAR`). Es el
  elemento gráfico principal. Una frase corta y potente, no un párrafo.
- **Dato clave:** marcador, hora, fecha, dorsal — grande y claro (`TYPE_DADA`).
- **Secundario:** rival, lugar, patrocinador — pequeño, ordenado, alineado a
  retícula.
- Tracking ligeramente negativo en display grande. Interlineado ajustado en
  titulares de varias líneas (se leen como bloque).

## Capa 4 — Marca y sistema

- Logo del club en su lockup y posición consistente.
- Hashtag de campaña / handle.
- Sponsors con jerarquía clara (nunca una fila desordenada).
- Elemento de sistema reconocible (banda de color, marco fino, motivo) que repita
  en toda la serie.

## Composición

- **Jerarquía:** un único foco. Tamaño + contraste + posición dirigen el ojo.
- **Diagonal y movimiento** (truco Bulls): elementos en diagonal o cuerpos en
  acción dan energía frente a una rejilla estática.
- **Regla del aire:** márgenes generosos (`MARGE_SEGURETAT`). Si dudas, quita
  elementos, no los encojas.
- **Punto focal fuera del centro:** suele ser más dinámico que centrado.

## Mini-receta "póster de jugador estilo NBA"

1. Fondo oscuro de marca.
2. Jugador/a recortado, a contraste, sangrando por abajo, ocupando el 60% de alto.
3. Nombre del jugador/a en display gigante vertical u horizontal detrás/junto a la
   figura.
4. Dorsal grande como elemento gráfico.
5. Logo + un acento de color de marca.
6. Nada más. El vacío es parte del diseño.
