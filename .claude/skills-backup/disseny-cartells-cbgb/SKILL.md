---
name: disseny-cartells-cbgb
description: >
  Playbook para diseñar carteles/pósters de CB Grup Barna a nivel élite (estilo
  Lakers, Bulls, Nike) adaptado al ADN del club. Cargar SIEMPRE que se cree o
  evalúe un cartel, póster o pieza gráfica clave: convocatoria de partido,
  resultado, MVP/jugada del día, cumpleaños, anuncio de evento/campus, welcome de
  fichaje, activación de sponsor. Cubre la anatomía de un cartel top, la
  deconstrucción de qué hacen las marcas referentes y cómo adaptarlo, el catálogo
  de plantillas del club y el filtro de calidad. Úsala aunque se diga solo "hazme
  el cartel de…". Depende de `sistema-visual-cbgb` (valores) y se ejecuta con
  `produccio-cartells`.
---

# Diseño de carteles élite — CB Grup Barna

Objetivo: que cualquier cartel del club se vea como el de un equipo profesional, no
como una plantilla genérica de Canva. Esta skill es el **criterio de diseño**; los
valores exactos están en `sistema-visual-cbgb` y la fabricación en
`produccio-cartells`.

## Las 5 leyes de un cartel top

Lo que separa un póster Nike/NBA de uno amateur:

1. **Un solo mensaje, gigante.** Una idea por cartel. El elemento principal
   (titular o protagonista) ocupa una parte enorme del lienzo. Si compite con tres
   cosas más, no es élite.
2. **Jerarquía brutal.** Lo importante, enorme; lo secundario, diminuto y ordenado.
   Nada "mediano". El ojo debe saber en 0,5 s qué mirar primero.
3. **Espacio negativo.** El aire comunica élite; el amontonamiento, amateur. Mejor
   vacío con intención que relleno.
4. **Tipografía protagonista.** Display condensada, mayúsculas, como elemento
   gráfico en sí. A menudo el titular *es* el diseño.
5. **Protagonista humano a alto contraste.** Recorte limpio del jugador/a sobre
   color plano de marca. Cara, gesto, emoción.

Detalle y ejemplos: `references/anatomia-cartell-elit.md`.

## Qué copiar (y qué no) de Lakers, Bulls, Nike

La clave es **traducir el principio, no copiar la estética** (lo dice el eje
benchmark de `ana-innovacio-barna`). Resumen rápido:

- **Nike:** tipografía enorme + frase corta y potente + mucho negro/espacio +
  atleta recortado. → Aplicar: titulares de impacto, menos elementos.
- **Lakers:** color icónico plano (púrpura/oro), identidad cromática reconocible a
  distancia. → Aplicar: disciplina de paleta, color de marca dominante.
- **Bulls:** alto contraste rojo/negro, energía agresiva, dinamismo. → Aplicar:
  contraste fuerte, diagonales, sensación de movimiento.

Deconstrucción completa y cómo adaptar al "formativo + élite + paridad real":
`references/benchmark-lakers-bulls-nike.md`.

## Catálogo de plantillas del club

Cada cartel recurrente es un **molde repetible** (misma estructura, cambia el
contenido) → consistencia + velocidad. Catálogo y especificación de cada uno en
`references/cataleg-plantilles.md`:

convocatoria · resultado (victoria/derrota) · MVP/jugada del día · cumpleaños ·
anuncio evento/campus · welcome fichaje · activación sponsor · quote.

Regla: si una plantilla se usa más de 2 veces, entra al sistema y se versiona.

## Proceso para un cartel

1. **Define el molde:** ¿qué plantilla del catálogo es? Si es nueva y se va a
   repetir, diséñala como sistema desde el principio.
2. **Carga los tokens:** colores, fuentes, retícula de `sistema-visual-cbgb`.
3. **Un mensaje:** decide el titular/dato protagonista. Recorta todo lo demás.
4. **Jerarquía y aire:** titular enorme, datos pequeños, margen generoso.
5. **Protagonista:** foto recortada a contraste o tipografía como héroe.
6. **Marca:** logo en su lockup; sponsors con jerarquía.
7. **Filtro de calidad** (abajo) antes de exportar.
8. **Producción:** fabricar con `produccio-cartells` (Canva/Figma/código).

## Filtro de calidad (antes de publicar)

1. ¿Se entiende el mensaje en menos de 1 segundo? (jerarquía)
2. ¿Se reconoce como Barna sin ver el logo? (sistema visible)
3. ¿Está al nivel técnico de un club top? (recorte, tipografía, alineación)
4. ¿Hay protagonista claro (humano o titular)?
5. ¿Respeta los tokens y la retícula? (consistencia con la serie)

Si no supera 4 de 5, se reedita. Anticipa además los filtros de
`mi-rol-coordinadora` (¿genera activo?, ¿lo defiendo en Junta?).

## Errores que rebajan el nivel al instante

- Amontonar información (varios mensajes compitiendo).
- Tipografías mezcladas sin sistema, o display pequeña y tímida.
- Foto sin recortar, borrosa o con horizonte torcido.
- Degradados/sombras/marcos "de plantilla genérica".
- Logos de sponsors pegados sin jerarquía.
- Emojis rompiendo titulares institucionales.
