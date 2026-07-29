---
name: transicions-virals-cbgb
description: "Tècnica de TRANSICIÓ PER ACCIÓ (el moviment del protagonista amaga el tall de càmera/ubicació) + ganxo de LLISTA numerada ('Top 3 X'), destil·lada d'un reel de referència d'un creador de contingut. Aplicable a QUALSEVOL peça d'Instagram i TikTok del CB Grup Barna: reels, TikToks, stories, recaps, presentacions de jugadora, campus, aniversari. Carregar SEMPRE que es munti una peça amb diverses escenes/ubicacions, es vulgui un ganxo tipus 'Top X'/llista, o una transició que no es noti com un tall sinó com un truc de producció. Complementa guions-virals-cbgb (estructura narrativa de 5 blocs) i ganxos-cbgb (copy del ganxo verbal). Executa amb video-club-cbgb, reel-fotos-cbgb i capcut-reels-cbgb; tipografia/color amb sistema-visual-cbgb."
---

# transicions-virals-cbgb — Transició per acció + ganxo de llista numerada

## Origen i límit
Destil·lat de l'anàlisi d'un reel de referència (creador de contingut extern,
format "Top 3 transicions virals"). **No es reprodueix cap text, imatge ni
metratge original** — només el patró estructural i tècnic que fa que la peça
funcioni, traduït a jugades pel Barna. Com `codis-dior-cbgb` o
`codis-vogue-cbgb`: criteri, no còpia.

## La tesi (dues palanques combinades)

1. **La transició és una ACCIÓ, no un tall.** En lloc de canviar de pla amb un
   simple "cut" (que l'ull detecta com edició), el protagonista fa un
   moviment físic complet — girar-se, travessar una porta, asseure's,
   arrencar a caminar — i just en el frame de màxima velocitat/oclusió del
   cos, la càmera canvia d'ubicació. El cervell interpreta el salt com a
   *continuïtat del gest*, no com un tall. Resultat: es noten com "efectes"
   encara que són muntatge pur, cosa que genera comentaris i guardats
   (la gent vol saber "com s'ha fet").
2. **El ganxo és un LLISTAT numerat anunciat d'entrada** ("Top 3 de X").
   Promet estructura + quantitat tancada: l'espectador sap que hi ha un
   final concret i quants punts falten, cosa que redueix la fricció de
   mirar-ho sencer (retenció més alta que un relat obert).

## Anatomia del reel (es repeteix un cop per punt de la llista)

| Bloc | Què passa | Funció |
|---|---|---|
| **0. Hook frontal** | Protagonista a càmera, pla ample, declara el tema + la promesa numèrica ("Top 3 de...") | Marca el contracte: què veuràs i quant durarà |
| **1. Reveal del punt** | Tipografia MOLT grossa, majúscules, entra partida en síl·labes/paraules, color de marca | Ritme visual — funciona sense so |
| **2. Demostració en acció** | El protagonista executa un moviment complet exactament en el frame on canvia d'ubicació | Aquí viu la transició — és el "truc" |
| **3. Explicació verbal per sobre** | Mentre veus l'acció, sents/llegeixes per què funciona aquell recurs | Justifica el valor — no és només estètic |

Es repeteix N vegades (en aquest cas 3) i tanca amb un pla en moviment
(caminant) + tancament/CTA.

## Traducció a jugades del Barna

| Format Barna | Ganxo de llista | Transicions per acció possibles |
|---|---|---|
| Presentació de fitxatge/renovació | "3 motius pels quals torna X" | Entrar per la porta del pavelló → seure al banquet → agafar la pilota |
| Recap de campus/3x3 | "Top 3 moments del Campus" | Córrer cap a la cistella → xocar la mà → aixecar el trofeu |
| Aniversari/60è | "3 coses que no sabies del Barna" | Obrir l'arxiu → passar la pàgina → sortir a la pista actual |
| Secció femenina | "Top 3 raons per venir a veure-les" | Botar la pilota → girar-se → entrar en calfament |
| Captació de sponsors | "3 motius per patrocinar un club de barri" | Assenyalar el logo → estrènyer la mà → mostrar la samarreta |

**Regla de marca (no negociable):** cada bloc numerat ha de tenir vermell
Barna `#E63329` o l'escut visible dins el món de la imatge (samarreta,
bufanda, rètol) — si no, el reel no es publica sense corregir-ho
(veure regla de visibilitat de marca).

## Execució tècnica

**Opció A — CapCut (manual, recomanat per començar):**
1. Grava cada acció de transició en DUES ubicacions consecutives, amb el
   mateix moviment corporal iniciat a la primera i acabat/continuat a la
   segona (mateixa roba, mateix ritme de moviment).
2. Talla just en el punt de màxima oclusió (el cos tapa la càmera un
   instant: girar d'esquena, travessar un marc de porta, ajupir-se).
2. Speed ramp lleuger (×1.2–1.5) just abans del tall perquè el moviment
   "empenyi" la transició — veure `capcut-reels-cbgb`.
3. Rètol Anton per al número/paraula clau, entrada per síl·labes —
   veure `sistema-visual-cbgb` per mida/color exactes.

**Opció B — Python/Pillow + FFmpeg (pipeline actual del club):**
- Si les transicions són entre fotos/il·lustracions fixes (no vídeo en
  directe), es pot simular el mateix efecte amb un *whip-pan* (blur de
  moviment horitzontal ràpid) entre frame i frame — veure
  `reel-illustrat-cbgb` per al push-in/Ken Burns i adaptar-hi un blur de
  transició als canvis d'escena.
- Script de referència: `references/whip-transition-ffmpeg.md`.

## Aplicació a IG Reels vs TikTok

Un mateix tall serveix per als dos amb ajustos mínims:

| | Instagram Reels | TikTok |
|---|---|---|
| Subtítols | Cremats en pantalla (regla de marca: sempre) | Cremats + auto-captions natius com a reforç |
| Durada òptima | 15–30 s si és llista de 3 punts | Pot allargar-se una mica més (fins 45 s) sense perdre retenció |
| Portada | Frame del hook frontal (bloc 0), mai un frame de transició | Mateixa lògica — TikTok no té "portada" fixa però el primer frame compta igual |
| CTA final | Seguir + veure destacada (aparador-perfil-cbgb) | Seguir + comentar (l'algoritme de TikTok pesa més el comentari) |
| So | Original o tendència, però amb el ganxo repetit en text | Igual — pujar-ho natiu a TikTok, no reexportar des d'IG (penalitza abast) |

## Checklist abans de publicar

1. El ganxo frontal declara quants punts hi ha i de què van? Si no → no és
   un ganxo de llista, és un títol pla.
2. Cada transició s'amaga darrere un moviment real, no és un tall sec?
3. Cada bloc numerat té vermell Barna o escut visible?
4. L'explicació verbal aporta un PERQUÈ, no només descriu l'acció?
5. El tancament té CTA (seguir/destacada) i no s'apaga en sec?

Si falla el punt 1 o 2 → torna a `ganxos-cbgb` i `guions-virals-cbgb` abans
de muntar.
