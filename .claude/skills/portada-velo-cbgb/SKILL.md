---
name: portada-velo-cbgb
description: >
  La RECETA VALIDADA de la portada de los reels de CB Grup Barna que están
  funcionando, alineada con el Manual de Identitat Visual v1.1: foto del
  protagonista + VELO ROJO (Roig Barna #E31E24 semitransparente) + LÍNEA ROJA
  COLOR LOGO alrededor + ESCUDO ARRIBA A LA DERECHA + título Bebas Neue
  centrado, con letra y cabeza del jugador CENTRADAS para que quepan en la
  graella en formato post y en Reels se vea completo. Incluye script Python
  que la genera en un comando y el checklist de "lo que siempre me dejo".
  Cargar SIEMPRE que se haga la portada/carátula/miniatura de un reel, se diga
  "la portada como las que estamos haciendo", "con el velo rojo", "capa roja",
  "la línea roja alrededor", "logo arriba a la derecha", "el estilo de
  nuestros reels", o al publicar cualquier reel (la portada custom es parte
  del flujo). Es la EJECUCIÓN del estilo ganador; la teoría de conversión vive
  en `portada-reels-cbgb`, el contenido del reel en `reels-cbgb`.
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

## La receta — 6 capas, en este orden

Lienzo **1080×1920 (9:16), siempre vertical**. Las capas, de abajo arriba:

1. **FOTO protagonista a sangre.** Persona real del club (nunca IA — norma
   crítica del manual). Ligera desaturación (×0.85) y contraste (×1.05) para
   que el velo unifique fotos dispares.
2. **VELO ROJO** — la firma. Capa plana Roig Barna `#E31E24` sobre TODA la
   foto, **opacidad 38%** (rango útil 32–45%: menos = no se reconoce la serie,
   más = se pierde la cara). Es un velo, no un duotono: la foto respira debajo.
   (Es el "tractament roig" que el manual pide para foto de series.)
3. **CAPA OSCURA sutil.** `#0A0A0C` al **15%** global + degradado inferior
   suave, para que el texto blanco lea sobre cualquier foto.
4. **LÍNEA ROJA ALREDEDOR — color logo.** Marco rectangular interior **Roig
   Barna `#E31E24`, grosor 6 px, a 44 px del borde** por los cuatro lados.
   Es el "marc roig" del manual y cierra la pieza. Nada la pisa: todo el
   contenido vive dentro. **Va en TODAS las portadas de reel, sin excepción.**
5. **ESCUDO ARRIBA A LA DERECHA.** `assets/escut_transp.png` (archivo
   oficial), **altura 150 px**, esquina superior derecha, **a 80 px del borde
   derecho y 88 px del superior** (dentro de la línea). Mismo tamaño y
   posición en TODAS — es un sello, no decoración.
6. **TÍTULO Bebas Neue.** Mayúsculas, blanco `#FFFFFF`, gigante (arranca a
   190 pt y se auto-encoge hasta caber), **≤5 palabras, una idea**, dos líneas
   máximo (separar con `|`). Barra corta blanca de remate y subtítulo en
   Montserrat con la **firma fija del manual: "CB GRUP BARNA · EL CLOT"**.

## La regla de ORO del centrado (graella ↔ Reels)

**La letra Y la cabeza del jugador van CENTRADAS en el lienzo.** Motivo: la
graella en formato post recorta el 9:16 a la **franja central 1080×1350**
(se pierden ~285 px arriba y ~285 px abajo). Diseñando al centro:

- **En la graella (post)** → título y cara caben enteros en el recorte.
- **En Reels** → se ve el 9:16 completo, con la línea y el escudo.

Cómo cumplirla: el script ya centra el título; la cara se encuadra con
`--vbias` (0=arriba, 1=abajo) **hasta que la cabeza quede en el centro del
lienzo**, y se comprueba con `--guies`, que dibuja las dos líneas del recorte
de graella (solo QA — nunca publicar con guías). Nada crítico fuera de la
franja central.

## Generarla en un comando

```bash
python3 scripts/portada.py --foto jugadora.jpg --titulo "FITXATGE|26/27" --out portada.png
```

Opciones: `--sub` (default: firma "CB GRUP BARNA · EL CLOT"), `--velo 0.38`,
`--vbias 0.30` (subir/bajar la foto hasta centrar la cabeza), `--dark 0.15`,
`--logo-y 88`, `--guies` (dibuja el recorte de graella para comprobar el
centrado), `--sinlinia` / `--sinvelo` solo para pruebas A/B — la versión
publicada lleva SIEMPRE velo y línea.

Fuentes oficiales (Bebas Neue, Montserrat) y escudo en `assets/`. Revisar el
PNG a tamaño miniatura (~300 px de alto) antes de dar por buena.

## Checklist "lo que siempre me dejo" (repasar ANTES de publicar)

1. ¿Subida como **portada custom** en el editor de IG? (Nunca el frame
   automático — es el error nº1 y el más caro.)
2. ¿**Velo rojo** puesto? Sin velo la portada no pertenece a la serie.
3. ¿**Línea roja color logo** entera alrededor, sin nada pisándola?
4. ¿**Título y cabeza del jugador centrados** — caben en el recorte de
   graella (comprobado con `--guies` o mirando el preview de post)?
5. ¿**Escudo oficial arriba a la derecha**, 150 px, mismos márgenes que las
   demás portadas?
6. ¿Título **≤5 palabras**, Bebas Neue, legible a 300 px?
7. ¿Se reconoce como Barna **sin leer nada** (velo + línea + escudo)?
8. ¿Al lado de las 8 casillas vecinas de la graella parece la misma mano?
9. Portada decidida **antes** de montar el reel, no después (`reels-cbgb`).

Si fallan 2 o más → rehacer antes de publicar.

## El escudo y la graella

Con título y cara centrados, lo único que el recorte de graella puede comerse
es el escudo (está arriba) y la parte alta de la línea. Correcto y asumido: en
la graella la serie se reconoce por el velo + la línea lateral + el título
centrado; en Reels y feed el escudo se ve entero. Si una portada va a ser PIN
y el escudo debe verse sí o sí también en graella, bajarlo con `--logo-y 260`.

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
