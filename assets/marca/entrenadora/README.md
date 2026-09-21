# Marca «ENTRENADORA» · CB Grup Barna

Símbol de la **dona entrenadora de bàsquet**. Tres signes fosos en una sola peça:

- **♀** — el signe de dona fa d'estructura (cercle + creu).
- **Pilota** — el cercle del símbol és una pilota de bàsquet, amb les costures
  buidades (transparents), no pintades de blanc: la marca funciona sobre
  qualsevol fons sense retallar-la.
- **Xiulet** — el broc a l'esquerra i l'anella a dalt converteixen la pilota en
  el cos d'un xiulet. És el signe d'entrenar.

## Fitxers

| Fitxer | Quan |
|---|---|
| `marca-entrenadora-color` | Ús general sobre fons clar |
| `marca-entrenadora-negatiu` | Sobre fons fosc (pilota vermella, peces blanques) |
| `marca-entrenadora-tinta` | Una sola tinta, fons clar |
| `marca-entrenadora-blanc` | Una sola tinta blanca, sobre foto o color |
| `marca-xiulet-*` | Versió curta (només xiulet-pilota): avatar, favicon, segell |
| `lockup-horitzontal-*` | Marca + paraula, per capçaleres i signatures |
| `lockup-vertical-*` | Marca + paraula, per cartells i formats verticals |

SVG per a tot (web, impressió, retolació). PNG amb fons transparent a 192, 512,
1024 px (marques) i 1200/2000 px (lockups).

## Valors

Els del sistema del club (`css/barna.css`), sense excepcions:

- Vermell `--red` **#E20613** — el mostrejat de l'escut.
- Tinta `--ink` **#10100E**.
- Gris del peu `--muted` **#6B6560**.
- Display **Anton**, text **Inter**. Als lockups les dues van **incrustades dins
  l'SVG** (woff2 en base64), o sigui que el fitxer es veu igual fora del domini
  del club i sense CDN de Google — el mateix criteri RGPD de `css/fonts.css`.

## Regles d'ús

- **Mida mínima:** 40 px d'alt la marca principal, 28 px la versió xiulet. Per
  sota, l'anella i les costures es tanquen.
- **Zona de protecció:** el radi de la pilota per tots quatre costats.
- No recolorir, no inclinar, no posar-hi ombres ni degradats.
- No la fem servir com a escut del club: l'escut és `assets/marca/club/`. Aquesta
  marca identifica la **figura de l'entrenadora**, no l'entitat.
- La paraula «ENTRENADORA» és idèntica en català i castellà: un sol lockup per a
  les dues llengües.

## Com es regenera

Els fitxers surten de codi, no d'un editor. Els scripts viuen al directori de
treball de la sessió (`final.js`, `lock.js`, `png.js`): generen les marques,
mesuren la tipografia al navegador per calcular el `viewBox` exacte dels lockups
i exporten els PNG amb Chromium.
