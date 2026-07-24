---
name: portada-velo-cbgb
description: >
  La RECETA VALIDADA de la portada de los reels de CB Grup Barna que están
  funcionando, alineada con el Manual de Identitat Visual v1.1: foto del
  protagonista + VELO ROJO (Roig Barna #E31E24 semitransparente) + LÍNEA ROJA
  COLOR LOGO alrededor + ESCUDO ARRIBA A LA DERECHA + título Bebas Neue
  grande alineado a la IZQUIERDA + etiqueta-gancho arriba a la izquierda, con
  título y cabeza del jugador dentro de la franja central para que quepan en la
  graella en formato post y en Reels se vea completo. Incluye script Python y
  plantilla PowerPoint editable, y el checklist de "lo que siempre me dejo".
  Cargar SIEMPRE que se haga la portada/carátula/miniatura de un reel, se diga
  "la portada como las que estamos haciendo", "con el velo rojo", "capa roja",
  "la línea roja alrededor", "logo arriba a la derecha", "el estilo de
  nuestros reels", o al publicar cualquier reel (la portada custom es parte
  del flujo). Es la EJECUCIÓN del estilo ganador; la teoría vive en
  `portada-reels-cbgb` y el contenido del reel en `reels-cbgb`.
---

# portada-velo-cbgb — La portada que está funcionando (receta exacta)

Skill de EJECUCIÓN nacida de los reels reales del club que están convirtiendo,
alineada con el **Manual d'Identitat Visual CB Grup Barna v1.1 (juliol 2026)**,
que es la fuente de verdad de los valores. No es teoría: es la receta literal,
con números, para que salga idéntica siempre y no se olvide ningún detalle.

Por qué existe: la coherencia de la graella es lo que convierte alcance en
seguidores (`portada-reels-cbgb`). El velo rojo + la línea roja + el escudo en
el mismo sitio hacen que TODAS las portadas se reconozcan como Barna de un
vistazo, incluso a 300 px. Un detalle olvidado en una portada rompe la serie.

## Tokens oficiales (manual v1.1 — mandan sobre valores antiguos)

- **Roig Barna `#E31E24`** — "energia · CTA · marcs". El rojo es identidad.
- **Negre `#0A0A0C`** · **Blanc pur `#FFFFFF`** · Gris metadades `#6B6F76`.
- **Tipografías: Bebas Neue** (titulares, nombres, cifras) + **Montserrat
  SemiBold/Regular** (texto, información, CTA). Máximo 2 familias.
- **Escudo: siempre el archivo oficial**, nunca recreado ni redibujado con IA.
  En piezas editoriales: **esquina superior derecha**. Altura 150 px a 1080 px
  de ancho. Mínimo digital 64 px.
- Proporción de color: 55% negro/fondo · 30% rojo/acento · 15% blanco/aire.

## El layout validado (el de las portadas reales del club)

Lienzo **1080×1920 (9:16), siempre vertical**. Los elementos, por zonas:

**Fondo (de abajo arriba):**
1. **FOTO protagonista a sangre.** Persona real del club (nunca IA — norma
   crítica del manual). Ligera desaturación + contraste para que el velo
   unifique fotos dispares.
2. **VELO ROJO** — la firma. Capa plana Roig Barna `#E31E24` sobre TODA la
   foto, **opacidad 38–42%** (rango útil 32–45%: menos = no se reconoce la
   serie, más = se pierde la cara). Es un velo, no un duotono. En portadas
   institucionales/tentpole el velo puede ir más fuerte (~55–60%) para el
   look de "bandera roja".
3. **CAPA OSCURA** `#0A0A0C` ~15% + viñeta inferior, para que el texto blanco
   lea sobre cualquier foto.
4. **LÍNEA ROJA ALREDEDOR — color logo.** Marco Roig Barna `#E31E24`, 6 px, a
   44 px del borde. Es el "marc roig" del manual. Va en TODAS, sin excepción.

**Arriba a la izquierda (el gancho):**
5. **ETIQUETA** — caja roja rellena con frase corta en Bebas blanco:
   "L'EFECTE CLARK.", "JA LA CONEIXEU.", "DUES ESTRELLES." Es el hook que para
   el scroll.
6. **CHIP "CAP. 01"** (caja negra) debajo, solo en series.

**Arriba a la derecha:**
7. **ESCUDO** oficial `assets/escut_transp.png`, **altura 150 px**, a 80 px
   del borde derecho y 88 px del superior. Mismo tamaño y sitio en TODAS.

**Centro-abajo (el mensaje), TODO alineado a la IZQUIERDA:**
8. **ANTETÍTULO** — línea pequeña en Montserrat gris con tracking:
   "SUBCAMPIONES I CAMPIONS DEL MÓN", "SÈRIE · BÀSQUET FEMENÍ".
9. **TÍTULO Bebas Neue** gigante, blanco, **alineado a la izquierda**, 2–4
   líneas cortas (separar con `|`). El título grande manda.
10. **ACENTO**, una de dos:
    - **Caja roja con palabra clave** ("SUPERCOPA."), o
    - **Barra roja vertical + subtítulo** en Bebas ("| DOBLE HISTÒRIA AL
      MUNDIAL.", "| AQUÍ, TAMBÉ.").

**Abajo:**
11. **FIRMA fija** del manual: "CB GRUP BARNA · EL CLOT", Montserrat, izquierda.

## La regla de ORO: título y cara dentro de la franja central

La graella en formato post recorta el 9:16 a la **franja central 1080×1350**
(se pierden ~285 px arriba y ~285 px abajo). Por eso el **bloque de título va
en la banda central** y la **cara del protagonista se encuadra con `--vbias`**
hasta quedar también en esa banda. Así:

- **En la graella (post)** → título y cara caben enteros.
- **En Reels** → se ve el 9:16 completo, con etiqueta, línea y escudo.

Lo único que el recorte de graella puede comerse es la etiqueta y el escudo
(están arriba); asumido, porque en la graella la serie ya se reconoce por el
velo + la línea + el título. `--vbias`: 0 = foto arriba, 1 = foto abajo.

## Generarla en un comando

```bash
python3 scripts/portada.py --foto jugadora.jpg \
    --etiqueta "L'EFECTE CLARK." --cap "CAP. 01" \
    --antetitol "SÈRIE · BÀSQUET FEMENÍ" \
    --titol "QUÈ ESTÀ|PASSANT AL|BÀSQUET|FEMENÍ?" \
    --caixa "AQUÍ, TAMBÉ." --barra --out portada.png
```

- `--caixa "SUPERCOPA."` sin `--barra` → palabra clave en caja roja.
- `--caixa "AQUÍ, TAMBÉ." --barra` → barra roja vertical + subtítulo.
- `--cap`, `--antetitol`, `--caixa` son opcionales.
- `--sub` (default: firma), `--velo`, `--vbias`, `--dark`, `--logo-y`.

Fuentes oficiales (Bebas Neue, Montserrat) y escudo en `assets/`.

## Plantilla PowerPoint editable

Para editar a mano en vez de por código, `assets/Portades_Reel_CBGB.pptx`
trae las 3 portadas (institucional, serie con palabra clave, serie con
protagonista) como slides 9:16 editables: duplicar una, cambiar foto, etiqueta
y título. Mismos valores del manual. Revisar el PNG a tamaño miniatura
(~300 px de alto) antes de dar por buena.

## Checklist "lo que siempre me dejo" (repasar ANTES de publicar)

1. ¿Subida como **portada custom** en el editor de IG? (Nunca el frame
   automático — es el error nº1 y el más caro.)
2. ¿**Velo rojo** puesto? Sin velo la portada no pertenece a la serie.
3. ¿**Línea roja color logo** entera alrededor, sin nada pisándola?
4. ¿**Etiqueta-gancho** arriba a la izquierda, en caja roja?
5. ¿**Título (izquierda) y cabeza del jugador** dentro de la franja central —
   caben en el recorte de graella?
6. ¿**Escudo oficial arriba a la derecha**, 150 px, mismos márgenes?
7. ¿Título en **Bebas Neue**, 2–4 líneas cortas, legible a 300 px?
8. ¿**Firma "CB GRUP BARNA · EL CLOT"** abajo?
9. ¿Se reconoce como Barna **sin leer nada** (velo + línea + escudo)?
10. ¿Al lado de las 8 casillas vecinas de la graella parece la misma mano?
11. Portada decidida **antes** de montar el reel, no después (`reels-cbgb`).

Si fallan 2 o más → rehacer antes de publicar.

## Los detalles del reel que acompañan a esta portada

La portada es la cara del sistema. El reel detrás sigue su receta (cargar la
skill, no repetir aquí):

- **Gancho en 2 s con cara mirando a cámara** y qué grabar → `reels-cbgb`,
  primera frase → `ganxos-cbgb`.
- **Texto en pantalla en mayúsculas, un mensaje por plano**, a prueba de
  silencio → `reel-fotos-cbgb` / `capcut-reels-cbgb`.
- **Zonas seguras 9:16** (la UI de IG tapa bordes: ~180 px arriba, ~260 px
  abajo según manual v1.1) → `sistema-visual-cbgb`.
- **Qué medir después** (guardados/compartidos, no likes) → `arrencada-reels-cbgb`.
- Versión bilingüe CA/ES y muda para sonido de tendencia cuando aplique.

## Relación con las skills hermanas

- **Manual d'Identitat Visual v1.1** — fuente de verdad de los valores. Ojo:
  skills antiguas usan tokens pre-manual (`#E63329`, `#0E1116`, Anton/Inter);
  para piezas nuevas mandan los del manual (`#E31E24`, `#0A0A0C`, Bebas
  Neue/Montserrat).
- `portada-reels-cbgb` — el POR QUÉ (conversión, recortes, graella). Esta
  skill es el CÓMO exacto del estilo actual; si chocan en un detalle de
  estilo, **manda esta**.
- `produccio-cartells` / `disseny-cartells-cbgb` — si la portada se hace a
  mano en Canva/Figma, replicar estas mismas capas y números.
