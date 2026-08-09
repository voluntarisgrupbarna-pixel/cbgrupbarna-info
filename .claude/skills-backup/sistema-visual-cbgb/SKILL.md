---
name: sistema-visual-cbgb
description: >
  Sistema visual con valores EXACTOS (design tokens) de CB Grup Barna: paleta hex,
  tipografías y escala, retícula, lockups de logo, espaciado y tratamiento de foto.
  Cargar SIEMPRE que se cree o evalúe cualquier pieza gráfica (cartel, post, story,
  deck, dossier, web) para garantizar consistencia exacta, no solo "principios".
  Es la fuente de verdad de los valores; `disseny-estetic-club` define los
  principios de uso y esta skill los números literales. Combinar con
  `disseny-cartells-cbgb` y `produccio-cartells` para diseño y producción de carteles.
  NORMA OBLIGATORIA: tota peca de video del club es tanca amb la CARTELA DE PARTNERS de `partners-outro-cbgb` (tots els partners, 3 s, 9:16). Sense cartela, no es publica.
---

# Sistema visual CB Grup Barna — tokens exactos

La consistencia es lo que hace que una marca se vea de élite (Lakers, Bulls, Nike
son reconocibles por repetir el mismo sistema mil veces). Esta skill fija los
valores literales para que cada pieza salga idéntica en ADN, hecha por quien sea.

Los valores oficiales viven en el knowledge "Barna" y en `assets/tokens.conf`.
**Antes de la primera pieza de una sesión, abrir `tokens.conf` y usar esos valores.**
Si un valor está como placeholder, pedírselo a Ana o usar la alternativa libre
indicada (no inventar).

## Color

Regla: **pocos colores, usados con disciplina.** Un color de marca dominante, uno
de acento, neutros para texto/fondo. El color plano y atrevido (sin degradados de
plantilla) es lo que da aire "élite".

- Primario, acento, tinta y fondo: ver `tokens.conf`.
- Contraste siempre legible (texto sobre color: comprobar AA).
- Nada de gradientes "Canva genérico" ni sombras blandas por defecto.

## Tipografía

La tipografía es el arma nº1 del look Nike/NBA: **display condensada, en mayúsculas,
gigante, como protagonista.** Jerarquía clara: un titular enorme, todo lo demás
pequeño y ordenado.

- **Display/titular:** una condensada de carácter. Si no hay licencia, alternativas
  libres excelentes: Anton, Archivo Black, Oswald, Bebas Neue, Teko (Google Fonts).
- **Texto/datos:** una sans neutra y legible (Inter, Archivo, Roboto).
- Escala tipográfica y pesos exactos: ver `tokens.conf`.
- Mayúsculas para titulares de impacto; tracking ligeramente negativo en display
  grande.
- Máximo 2 familias por pieza. Mezclar sin sistema rompe marca al instante.

## Retícula y espaciado

- Trabajar con **margen de seguridad** generoso: el espacio negativo comunica élite;
  el amontonamiento comunica amateur.
- Retícula y unidad de espaciado base: ver `tokens.conf`.
- Alinear todo a la retícula. Nada "a ojo".

## Logo (lockups)

- Versiones, tamaños mínimos y zona de protección: ver `tokens.conf`.
- Posición consistente entre piezas de una misma serie.
- Logo presente pero sin competir con el mensaje principal.
- Logos de sponsors: jerarquía clara, nunca pegados sin orden (un sponsor mal
  colocado no renueva). Coordinar con `disseny-cartells-cbgb`.

## Tratamiento de foto

El "efecto póster NBA": foto del protagonista **recortada del fondo**, a alto
contraste, sobre color plano de marca; opcional duotono con la paleta.

- Recorte limpio del jugador/a (sin halos).
- Alto contraste, protagonismo de cara/gesto.
- Duotono o tinte de marca para unificar fotos dispares en una serie.
- Calidad técnica innegociable: nada borroso, nada con horizonte torcido.

## Zonas seguras (reel / story 9:16)

La UI de Instagram **tapa los bordes** del vídeo: arriba el perfil, a la derecha los
botones (like/comentar/compartir/audio) y abajo el caption + usuario + CTA. Si el hook
o los subtítulos caen ahí, el no-seguidor los pierde en el primer segundo — y ahí es
donde se juega la conversión de alcance a seguidor (nuestro cuello de botella real).

Regla de oro: **nada esencial en el 22% inferior ni en los ~180 px de la derecha.**

- **Hook / titular:** tercio superior. Alto y visible, nunca escondido abajo.
- **Mirada del sujeto:** ojos sobre la línea del tercio superior, mirando a cámara.
- **Subtítulos:** banda central-baja, **nunca pegados al borde inferior** (los come el caption).
- Bandas y márgenes reservados (valores literales): ver `tokens.conf` → ZONES SEGURES.
- Plantilla visual para superponer al montar: `assets/safe-zones-9x16.png`.

Vale para reel, story y cualquier pieza 9:16 con texto.

## Filtro de consistencia (antes de exportar)

1. ¿Usa exactamente los colores y fuentes de `tokens.conf`?
2. ¿Respeta retícula, márgenes y zona de protección del logo?
3. ¿Se reconoce como Barna sin ver el logo?
4. ¿Encaja con la serie a la que pertenece (mismo sistema)?
5. Si es 9:16: ¿hook y subtítulos dentro de la zona segura, sin que los tape la UI de IG?

Si falla uno, corregir antes de publicar. La inconsistencia es el error que más
rebaja el nivel percibido.


## Cartela de partners (cierre de vídeo) — valores

Pieza fija del sistema visual: la cartela que cierra **toda** pieza de vídeo del
club. Playbook completo y assets en **`partners-outro-cbgb`**.

| Token | Valor |
|---|---|
| Lienzo | 1080×1920 (9:16), 30 fps, 3 s |
| Fondo por defecto | negro `#0A0A0A` (variante clara: blanco `#FFFFFF`) |
| **Vermell Barna** | **`#FD030C`** — muestreado del escudo oficial `LOGO_BARNA_HD.png` |
| Tipografía título | Anton, mayúsculas, en rojo Barna |
| Tipografía pies | Inter, 22-26 px |
| Logos partner | **monocromo blanco** sobre fondo oscuro; color original sobre claro |
| Retícula | 4 columnas, márgenes 70 px, última fila centrada |
| Institucionales | bloque separado, bajo filete rojo, con la fórmula "amb el suport de" |
| Zona segura | contenido entre y=150 y y=1560; nada esencial bajo el 22 % inferior |

**Jerarquía de logos de sponsor (regla general del sistema):** los partners
comerciales van en una retícula de igual peso óptico (nadie destaca sobre nadie
salvo pacto por escrito); los institucionales van **separados** y precedidos de
"amb el suport de", como exigen los convenios públicos.

Añadir al **filtro de consistencia** un punto 6: si la pieza es vídeo, ¿cierra
con la cartela de partners actualizada?
