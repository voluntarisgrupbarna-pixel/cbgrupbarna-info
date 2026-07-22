---
name: portada-velo-cbgb
description: >
  La RECETA VALIDADA de la portada de los reels de CB Grup Barna que están
  funcionando: foto del protagonista + VELO ROJO (#E63329 semitransparente
  sobre toda la foto) + LÍNEA ALREDEDOR (marco blanco fino) + ESCUDO ARRIBA A
  LA DERECHA + título Anton gigante en el centro. Incluye script Python que la
  genera en un comando y el checklist de "lo que siempre me dejo". Cargar
  SIEMPRE que se haga la portada/carátula/miniatura de un reel, se diga "la
  portada como las que estamos haciendo", "con el velo rojo", "capa roja",
  "logo arriba a la derecha", "línea alrededor", "el estilo de nuestros reels",
  o al publicar cualquier reel (la portada custom es parte del flujo). Es la
  EJECUCIÓN del estilo ganador; la teoría de conversión y zonas de recorte vive
  en `portada-reels-cbgb`, los tokens en `sistema-visual-cbgb`, el contenido
  del reel en `reels-cbgb`.
---

# portada-velo-cbgb — La portada que está funcionando (receta exacta)

Skill de EJECUCIÓN nacida de los reels reales del club que están convirtiendo.
No es teoría: es la receta literal, con números, del estilo que Ana valida en
cada pieza — para que salga idéntica siempre, la haga quien la haga, y no se
olvide ningún detalle.

Por qué existe: la coherencia de la graella es lo que convierte alcance en
seguidores (`portada-reels-cbgb`). El velo rojo + la línea + el escudo en el
mismo sitio hacen que TODAS las portadas se reconozcan como Barna de un
vistazo, incluso a 300 px. Un detalle olvidado en una portada rompe la serie.

## La receta — 6 capas, en este orden

Lienzo **1080×1920 (9:16), siempre vertical**. Las capas, de abajo arriba:

1. **FOTO protagonista a sangre.** Cara o gesto reconocible, encuadre que deje
   la cara en el tercio superior-centro (vbias ≈ 0.30). Ligera desaturación
   (×0.85) y contraste (×1.05) para que el velo unifique fotos dispares.
2. **VELO ROJO** — la firma. Capa plana `#E63329` sobre TODA la foto,
   **opacidad 38%** (rango útil 32–45%: menos = no se reconoce la serie,
   más = se pierde la cara). Es un velo, no un duotono: la foto respira debajo.
3. **CAPA OSCURA sutil.** `#0E1116` al **15%** global + degradado inferior
   suave, para que el texto blanco lea sobre cualquier foto.
4. **LÍNEA ALREDEDOR.** Marco rectangular interior **blanco `#F5F5F7`,
   grosor 6 px, a 44 px del borde** por los cuatro lados. Cierra la pieza y da
   el look "cartel premium". Nada puede pisar la línea excepto nada: todo el
   contenido vive dentro.
5. **ESCUDO ARRIBA A LA DERECHA.** `assets/escut_transp.png`, **altura 150 px**,
   esquina superior derecha, **a 80 px del borde derecho y 88 px del superior**
   (dentro de la línea). Mismo tamaño y posición en TODAS las portadas — es un
   sello, no decoración.
6. **TÍTULO Anton.** Mayúsculas, blanco `#F5F5F7`, gigante (arranca a 170 pt y
   se auto-encoge hasta caber), **centrado en el centro vertical** del lienzo,
   **≤5 palabras, una idea**. Dos líneas máximo (separar con `|`). Barra corta
   blanca debajo como remate. Subtítulo opcional en Inter 46, tracking ancho.

## Generarla en un comando

```bash
python3 scripts/portada.py --foto jugadora.jpg --titulo "FITXATGE|26/27" \
    --sub "SEGUEIX EL BARNA" --out portada.png
```

Opciones: `--velo 0.38` (opacidad del velo), `--vbias 0.30` (encuadre vertical
de la foto, 0=arriba 1=abajo), `--dark 0.15`, `--logo-y 88`, `--sinlinia` /
`--sinvelo` solo para pruebas A/B — la versión publicada lleva SIEMPRE ambos.

El script vive en `scripts/portada.py` con fuentes y escudo en `assets/`.
Revisar el PNG a tamaño miniatura (~300 px de alto) antes de dar por buena.

## Checklist "lo que siempre me dejo" (repasar ANTES de publicar)

1. ¿Subida como **portada custom** en el editor de IG? (Nunca el frame
   automático — es el error nº1 y el más caro.)
2. ¿**Velo rojo** puesto? Sin velo la portada no pertenece a la serie.
3. ¿**Línea alrededor** entera, sin nada pisándola?
4. ¿**Escudo arriba a la derecha**, mismo tamaño (150 px) y márgenes que las
   demás portadas?
5. ¿Título **≤5 palabras**, legible a 300 px, en el centro vertical?
6. ¿Se reconoce como Barna **sin leer nada** (por velo + línea + escudo)?
7. ¿Al lado de las 8 casillas vecinas de la graella parece la misma mano?
8. Portada decidida **antes** de montar el reel, no después (`reels-cbgb`).

Si fallan 2 o más → rehacer antes de publicar.

## Aviso honesto sobre la graella

La graella de IG recorta el 9:16 a 3:4: se pierden ~240 px arriba y abajo. El
escudo arriba a la derecha se ve perfecto en la pestaña Reels y en el feed,
pero **en la graella puede quedar cortado**. No pasa nada: en la graella la
serie se reconoce por el velo + la línea + el título centrado. Si una portada
va a ser PIN del perfil y el escudo debe verse sí o sí en graella, bajarlo con
`--logo-y 260`. Detalle completo de recortes: `portada-reels-cbgb` →
`references/especificacions-portada.md`.

## Los detalles del reel que acompañan a esta portada

La portada es la cara del sistema que está funcionando. El reel detrás sigue
su propia receta (no repetir aquí, cargar la skill):

- **Gancho en 2 s con cara mirando a cámara** y qué grabar → `reels-cbgb`,
  primera frase → `ganxos-cbgb`.
- **Texto en pantalla Anton mayúsculas, un mensaje por plano**, a prueba de
  silencio, estructura a beat → `reel-fotos-cbgb` / `capcut-reels-cbgb`.
- **Zonas seguras 9:16** (la UI de IG tapa bordes) → `sistema-visual-cbgb`.
- **Qué medir después** (guardados/compartidos, no likes) → `arrencada-reels-cbgb`.
- Versión bilingüe CA/ES y muda para sonido de tendencia cuando aplique.

## Relación con las skills hermanas

- `portada-reels-cbgb` — el POR QUÉ (conversión, recortes, graella). Esta
  skill es el CÓMO exacto del estilo actual; si chocan en un detalle de
  estilo, **manda esta** (es lo validado con resultados).
- `sistema-visual-cbgb` — tokens: `#E63329`, `#0E1116`, `#F5F5F7`, Anton/Inter,
  margen 80.
- `produccio-cartells` / `disseny-cartells-cbgb` — si la portada se hace a mano
  en Canva/Figma, replicar estas mismas capas y números.
