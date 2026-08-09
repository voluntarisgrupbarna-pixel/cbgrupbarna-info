---
name: partners-outro-cbgb
description: >
  NORMA OBLIGATÒRIA del CB Grup Barna: TOT reel, story llarga, highlight, recap o
  vídeo del club es tanca amb la CARTELA DE PARTNERS (tots els partners i
  institucions, 3 s, 9:16). Aquesta skill conté la norma, l'especificació visual
  exacta de la cartela, els assets ja renderitzats (PNG + MP4, versió fosca i
  clara), el set de logos normalitzats i l'script que la regenera quan entra o
  surt un partner. Carregar SEMPRE que es munti, exporti, avaluï o planifiqui
  qualsevol peça de vídeo del club, quan es parli de logos de sponsors,
  contraprestacions visuals, "on poso els partners", "quins partners tenim" o
  "falta el logo de X". És ELIMINATÒRIA: sense cartela, la peça no es publica.
  Els valors de marca viuen a `sistema-visual-cbgb`, el criteri de contingut a
  `reels-cbgb`, l'execució a `video-club-cbgb` / `capcut-reels-cbgb`, i la
  relació comercial a `patrocinis-club`.
---

# partners-outro-cbgb — La cartela de partners

## La norma (curta i innegociable)

> **Cap peça de vídeo del CB Grup Barna surt sense la cartela de partners al final.**
> Tots els partners. Sempre. Encara que la peça sigui d'un altre tema, encara que
> tinguem pressa, encara que "aquest reel no va de sponsors".

Això no és estètica: és **contraprestació**. Un partner que veu el seu logo a cada
peça del club renova; un que hi surt "quan toca" no. És la manera més barata i més
constant d'entregar valor a qui ens finança, i converteix cada reel en una prova de
retorn que després es cita al dossier (`patrocinis-club`).

**Regla dura:** al filtre de qualitat de qualsevol peça de vídeo, la cartela és un
**criteri eliminatori**, al mateix nivell que el ganxo i el CTA de `reels-cbgb`.

## Excepcions (les úniques)

1. **Stories curtes del dia a dia** (<10 s, efímeres, no publicades al feed).
   Recomanable però no obligatori.
2. **Peces de crisi o comunicats sensibles** (lesió greu, dol, conflicte). Un logo
   comercial al costat d'un missatge delicat perjudica el partner. Sense cartela.
3. **Peces contractades per un únic partner** amb exclusivitat pactada per escrit.
   En aquest cas, cartela pròpia només d'aquell partner.

Fora d'aquests tres casos, no hi ha excepció.

## Especificació de la cartela

| Paràmetre | Valor |
|---|---|
| Format | 9:16, **1080×1920**, 30 fps |
| Durada | **3 s** (2,5 s mínim; per sota no dona temps a llegir) |
| Entrada | fade in 0,35 s + zoom lent 1,00 → 1,04 |
| Sortida | fade out 0,30 s |
| Fons | **negre #0A0A0A** (versió `dark`, per defecte) / **blanc** (versió `light`) |
| Logos | **monocrom blanc** a la versió fosca; **monocrom negre** a la clara |
| Per què monocrom | logos de 21 marques amb 21 paletes convertirien la cartela en un mosaic. El monocrom els iguala i fa que la cartela sembli **una peça del club**, no un taulell d'anuncis. Els partners hi guanyen: destaquen per forma, no competeixen per color. |
| Vermell Barna | **#FD030C** (mostrejat de l'escut oficial) |
| Tipografia | Anton (títol) + Inter (peus) — a `assets/` |
| Àudio | pista silenciosa AAC inclosa (perquè CapCut no la talli) |

### Anatomia (de dalt a baix)

1. **Escut del club** centrat.
2. **"GRÀCIES"** en Anton, vermell Barna.
3. **"ALS QUI FAN POSSIBLE EL CB GRUP BARNA"** en Inter, blanc.
4. **Graella de partners comercials** — 4 columnes, mateixa alçada òptica, última
   fila centrada. Ordre alfabètic per fitxer (no per import: cap partner ha de
   poder dir "per què ell primer").
5. **Filet vermell** + **"AMB EL SUPORT DE"** + **logos institucionals**
   (Districte de Sant Martí, esportcat/Generalitat). Els institucionals van
   **separats** dels comercials: és una exigència habitual dels convenis públics.
6. **@cbgrupbarna** en vermell (decoratiu: la UI d'Instagram pot tapar-lo).

### Zones segures

Tot el contingut viu entre y=150 i y=1560 px. **Res essencial per sota del 22 %
inferior** (el caption d'Instagram el tapa) ni als ~180 px de la dreta (botons).
Coherent amb `sistema-visual-cbgb` → ZONES SEGURES.

## On són els arxius

Els vídeos finals **NO viuen dins d'aquesta skill** (pesarien massa i no es podria
desar): viuen al Mac, a

```
Desktop / reel despres partit / LOGOS PARTNERS / CARTELA PARTNERS /
    outro_partners_dark.mp4      ← el que s'usa el 90 % de les vegades
    outro_partners_light.mp4
    outro_partners_dark.png / _light.png
```

Els logos originals són a `Desktop / reel despres partit / LOGOS PARTNERS`.
Dins d'aquesta skill hi ha només `assets/outro_partners_dark.png` com a
**referència visual** del disseny correcte.

## Com fer-la servir

### A CapCut (el flux normal d'Ana)
1. Munta el reel com sempre (`capcut-reels-cbgb`).
2. Al final del timeline, **importa `CARTELA PARTNERS/outro_partners_dark.mp4`**
   i enganxa'l després de l'últim clip.
3. La música: **abaixa-la 3-4 dB** durant la cartela, no la talles de cop.
4. Exporta 1080×1920 / 30 fps.

**Truc:** desa la cartela com a **material fixat** a CapCut ("Afegir a preferits")
perquè estigui a un clic a cada projecte nou.

### Amb ffmpeg (execució automàtica, `video-club-cbgb`)
```bash
# concatenar reel + cartela (mateix codec, sense recodificar el reel si coincideix)
ffmpeg -i reel.mp4 -i assets/outro_partners_dark.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 128k \
  reel_amb_partners.mp4
```

### Quan la peça és fosca o cinematogràfica
Versió `dark` (per defecte). Quan la peça acaba en blanc o és molt clara
(cartells clars, campus, contingut lluminós), versió `light`.

## Quan entra o surt un partner

1. Deixa el logo nou a `Desktop / reel despres partit / LOGOS PARTNERS`.
2. Digues-li a Claude: **"ha entrat [PARTNER], regenera la cartela"**. Claude
   afegeix el logo als scripts, els executa i torna el MP4 i el PNG nous.
3. Actualitza `references/partners.md` amb l'alta o la baixa.
4. **Avisa el partner** que ja surt a la cartela — és una trucada de renovació
   gratuïta.

Si es vol executar a mà (requereix Python amb Pillow, numpy i scipy):

```bash
python3 scripts/prep_logos.py && python3 scripts/build_outro.py
```

`prep_logos.py` neteja el fons, retalla i genera la versió monocrom blanca de cada
logo automàticament. `build_outro.py` recompon la graella i el vídeo.

## Filtre de qualitat de la cartela

1. Hi són **tots** els partners vigents? (comprovar contra `references/partners.md`)
2. Cap logo deformat, pixelat o amb halo de fons?
3. Els institucionals van separats i amb la fórmula "amb el suport de"?
4. Es llegeix en un mòbil a mida real? (mirar-la al telèfon, no a l'ordinador)
5. Dura ≥2,5 s?
6. Hi ha algun partner que ja no ho és? (un logo caducat és pitjor que cap logo)

## Deute pendent d'assets

Aquests logos venen de captures de pantalla o JPG amb fons; funcionen però no són
òptims. **Demanar el vector (SVG/AI/EPS) o PNG amb transparència** al partner:

- ARMAND · TOT SALUT · FOTO JANÉ · ROMEO ABOGADOS · BAC DE RODA · MULLOR

És una petició de 30 segons per WhatsApp i millora la cartela per sempre.
