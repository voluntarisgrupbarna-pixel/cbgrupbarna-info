---
name: efecto-brutalismo-cbgb
description: "Efecto brutalismo (anillos concentricos +-40 grados, Python/ffmpeg) INVERTIDO: la jugadora SE RECOMPONE del caos = reveal de fichaje potente. Cargar ante \"efecto brutalismo\", \"que se recomponga\", \"reveal de jugadora\", \"algo mas agresivo/premium\", \"esto queda plano\". Script scripts/brutalisme.py. Usa sistema-visual-cbgb + codis-lux-cbgb; monta con video-club-cbgb/reel-fotos-cbgb; portada con portada-reels-cbgb."
---

# Efecto Brutalismo — la imagen se recompone

Anillos concéntricos de la misma foto, cada uno girado en dirección alterna. Crudo,
pesado, alto contraste: es **literalmente nuestro ADN** (#0E1116 + #E63329 + Anton +
plano). No es un filtro de moda, es nuestra estética con movimiento.

## El truco (por qué funciona)

Un **círculo rotado sobre su propio centro es el mismo círculo**. Así que si
enmascaras una capa con una elipse y giras la capa entera: **la máscara no se mueve,
la imagen de dentro sí.** Apilas discos cada vez más pequeños y lo que ves son
anillos girando cada uno a su aire. Eso es todo el efecto.

## El giro estratégico (lo que no dice el tutorial)

El original lo enseña como **romper** (intacto → fracturado). Bonito, y se olvida.
El valor para el club está en **reproducirlo al revés**:

> **`reveal`: empieza fracturado, converge, la jugadora aparece entera.**

Eso no es un efecto: es un **relato**. Del caos sale la persona. Es exactamente lo
que compra un fichaje, una renovación o un homenaje. **Ese es el modo por defecto.**

## Ejecución

### Ruta A — Código (default: es tu pipeline, es repetible)

```bash
# Reveal de jugadora — el que convierte
python3 scripts/brutalisme.py --img jugadora.jpg --out reveal.mp4 --cy 0.38

# Portada de reel (el pico de fractura, congelado). Ver portada-reels-cbgb
python3 scripts/brutalisme.py --img jugadora.jpg --out portada.png --still --crest

# Romper para cortar a negro / entrar al siguiente plano
python3 scripts/brutalisme.py --img foto.jpg --out out.mp4 --mode explode --angle 55
```

**Los 3 parámetros que deciden si queda bien o queda a chapuza:**

| Param | Por qué importa |
|---|---|
| `--cx --cy` | **Centra el efecto en la CARA**, no en el medio del lienzo. Default `0.5 / 0.42`. Si el reveal converge sobre un codo, no significa nada. |
| `--layers` | **4–7.** Menos = flojo. Más = ruido ilegible. |
| `--angle` | **40** (el del tutorial) ya es agresivo. Sube a 55 solo para `explode`. |

Sale 1080×1920, fondo #0E1116, escudo opcional. Salida muda: el sonido se pone
después (`reels-cbgb`).

### Ruta B — DaVinci (el original, a mano) → `references/recepta-davinci.md`
### Ruta C — CapCut (para el resto del equipo) → misma referencia, al final

## Dónde usarlo (y dónde no)

**SÍ** — cuando hay **una persona y un momento**:
- Presentación de fichaje / renovación (`reveal` + Anton encima al converger).
- MVP de la jornada. Homenaje / despedida.
- Portada de reel que tiene que parar el scroll (`--still`).
- 60 años: foto de archivo que se recompone. Ahí el efecto *significa* algo.

**NO**:
- **Activaciones de sponsor.** Romper el logo de quien te paga es un no. Nunca.
- Coberturas de partido, resultados, convocatorias: es rutina, no ritual.
- Fotos de grupo o de equipo: sin un rostro que converja, es solo ruido bonito.
- Contenido de menores del planter donde la cara es lo único que hay: cuidado, la
  fractura sobre la cara de un niño se lee raro. Úsalo sobre la acción, no sobre él.

## La regla que protege el efecto (escasez de gesto — `codis-lux-cbgb`)

Un efecto fuerte usado en todo **deja de significar nada** y pasa a ser plantilla.

> **Máximo 1 uso por pieza. Máximo ~1 pieza al mes.**

Si el brutalismo aparece, el público debe entender sin que se lo digan que **esto es
importante.** Ese es todo su valor. Quemarlo es gratis; recuperarlo, no.

## Filtro de calidad (antes de publicar)

- [ ] El efecto **converge sobre la cara**, no sobre el fondo.
- [ ] Acaba **limpio**: el último frame es la foto intacta, nítida, sin restos.
- [ ] Se lee en **9:16 sin sonido** y con la UI de IG encima (zonas seguras:
      `sistema-visual-cbgb` — nada esencial en el 22% inferior).
- [ ] Foto de origen **buena**: el brutalismo amplifica una foto mala, no la salva.
- [ ] ¿Justifica el gesto? Si la respuesta es "queda chulo" → **no lo uses**.

## Cómo encaja

- **Criterio de deseo/ritual:** `codis-lux-cbgb`, `luxury-logic-cbgb`.
- **Valores exactos** (hex, Anton, márgenes): `sistema-visual-cbgb`.
- **Montaje de la pieza final** (audio, rótulos, export): `video-club-cbgb`,
  `reel-fotos-cbgb`, `video-estrella-cbgb`.
- **Portada / conversión** del reel: `portada-reels-cbgb`, `crecimiento-ig-cbgb`.
- **A mano, por el equipo:** `capcut-reels-cbgb`.

## Fuente

Tutorial "Efecto Brutalismo en DaVinci Resolve" — @oscarmeriino (TikTok, jun 2026,
43 s). La técnica es suya; el uso, el criterio y la implementación en código son del
club. Receta original fiel en `references/recepta-davinci.md`.
