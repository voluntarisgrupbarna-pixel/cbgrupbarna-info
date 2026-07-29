---
name: reel-illustrat-cbgb
description: >
  Genera reels d'una sola il·lustració fixa amb push-in (Ken Burns) i línies de
  text que entren en seqüència construint un argument, tancant amb escut+programa+
  claim. Format del reel #1 de la sèrie "No cal res" (Escoleta). Parametritzable
  per qualsevol temàtica: femení, Pissarra, Màgics, 60è aniversari, campus.
  Carregar sempre que Ana digui "fes-me un reel il·lustrat de...", "el mateix
  estil del reel de l'escoleta", "una altra peça de la sèrie", o vulgui repetir
  aquest format per un tema nou. Aporta el criteri i l'execució tècnica
  (Python/Pillow + ffmpeg). Usa sistema-visual-cbgb; germana de reel-fotos-cbgb.
---

# Reel il·lustrat CB Grup Barna

## El format, en una frase

Una sola il·lustració aguanta 12-15 segons de reel si té push-in + text cinètic
ben seqüenciat. No cal vídeo real, no calen múltiples plans — un dibuix ben triat
+ moviment de càmera + paraules que van entrant fan tota la feina.

Neix del reel #1 de la sèrie **"No cal res"** (Escoleta): una nena jugant a una
pista de barri degradada, amb la bufanda del Barna penjada de la cistella
oxidada. Funciona per tres motius, i val la pena recordar-los perquè són els que
fan que aquest format encaixi amb QUALSEVOL tema nou:

1. **És barat i escalable.** Una il·lustració = una peça sencera. No cal gravació,
   ni equip, ni edició complexa. Es pot produir una sèrie sencera en una tarda.
2. **El contrast fa la feina de marca.** Barri real/degradat + un sol element de
   marca (bufanda, escut) resol el problema de conversió (que un no-seguidor sàpiga
   de qui és la peça) sense trair l'estètica cruda que la fa creïble.
3. **El text seqüenciat crea tensió.** Cada línia que entra és un pas d'un
   argument — no és informació estàtica, és un guió amb ritme, encara que la
   imatge no es mogui.

## Quan usar aquest format (i quan NO)

Usar-lo quan:
- Es vol continuar o encetar una **sèrie basada en una sola il·lustració** (com
  "No cal res" a l'escoleta, o una futura sèrie del femení, Pissarra, Màgics, 60è
  aniversari...)
- El material disponible és una il·lustració/cartell, no vídeo ni fotos de partit
- Es necessita produir contingut ràpid i barat però amb nivell (no un post estàtic)

NO usar-lo per:
- Cobertura de partit, highlights o material amb vídeo real → `video-club-cbgb`
- Reels amb fotos reals múltiples (fitxatge, captació) → `reel-fotos-cbgb`
- Un cartell estàtic sense animació → `disseny-cartells-cbgb` / `produccio-cartells`

## Els 3 inputs que cal definir per a cada peça nova

Per fer una peça nova d'aquest format només cal decidir tres coses — la resta
(estructura, timing, tipografia, marca) és fixa i ja està resolta als scripts:

**1. Tema / sèrie.** A quina sèrie pertany aquesta peça i quin és el seu lloc
dins d'ella (p.ex. peça 2/6 de "No cal res": "No cal saber jugar").

**2. Il·lustració.** Descripció de l'escena + l'element de marca OBLIGATORI
visible enlloc de l'escut sencer (una bufanda, un detall de color, un objecte amb
el vermell del club). Regla d'or: **si un pare del Clot la veu passar sense so, ha
de poder intuir que és del Barna.** Sense marca visible a la il·lustració, la
peça no compleix la seva funció encara que el text sigui bo.

**3. Guió de línies.** 3-5 frases curtes (una idea per línia, en majúscules,
llegibles en <2s) que construeixen un argument. La ÚLTIMA línia sol ser la
resolució/CTA implícit ("Només cal una pilota. I ganes."). Deixa forats entre
línies (no se solapen) i reserva la línia clau en vermell — mai més d'una per
peça.

## Estructura fixa (no canvia entre peces)

| Tram | Contingut |
|---|---|
| 0.0 – 2.4s | Línia 1: primer argument/excusa desmuntada |
| 3.0 – 5.4s | Línia 2 |
| 6.0 – 8.4s | Línia 3 (sovint la de color vermell, la que fa mal a l'excusa) |
| 9.0 – 12.6s | Línia de resolució (pot ser 2 línies curtes) |
| 12.6 – 15.6s | Targeta de tancament: escut + nom del programa + claim |

Aquest timing ve de `scripts/compose_overlays.py::GUIO` — és el punt de partida,
no un motlle rígid. Si el guió d'una peça necessita 4 línies en comptes de 3-4,
ajusta els trams mantenint ~2-2.5s per línia i el forat de ~0.6s entre elles.

## Execució tècnica

1. **Il·lustració base.** Genera-la o adapta-la amb `disseny-cartells-cbgb` /
   `canvas-design` (si es fa amb IA generativa, cal aprovació d'Ana abans —
   veure nota Higgsfield al fil de treball). Guarda-la com a JPG/PNG vertical
   (mínim 1512×2688 recomanat perquè el push-in no perdi qualitat).

2. **Genera les capes de text:**
   ```bash
   cd reel-illustrat-cbgb/scripts
   LANG_REEL=ca python3 compose_overlays.py   # i LANG_REEL=es per la versió castellana
   ```
   Això edita `GUIO` i `CLOSING` dins `compose_overlays.py` (l'únic que cal tocar
   per a una peça nova) i genera `overlays/line_XX.png` (transparents) +
   `overlays/closing.png` + `overlays/manifest.json`.

3. **Munta el reel:**
   ```bash
   ./build_reel.sh <illustracio.jpg> ca [audio_bed.m4a]
   ```
   Fa push-in continu sobre la il·lustració (filtre `zoompan`, mateix patró que
   `reel-fotos-cbgb`), hi superposa cada `line_XX.png` només durant el seu tram
   (`overlay=...:enable='between(t,t0,t1)'`), i hi concatena la targeta de
   tancament. Surt `reel_ca_SILENT.mp4` (per posar-hi so de tendència a IG) i,
   si es passa un àudio, `reel_ca.mp4` amb música ja incrustada.

4. Repeteix el pas 2-3 amb `LANG_REEL=es` per la versió castellana.

Colors, tipografia i marges surten de `sistema-visual-cbgb`
(`#0E1116` fons, `#E63329` vermell, `#F5F5F7` blanc, Anton per als titulars,
Inter per al text petit, marge 80px) — ja estan fixats als scripts, no cal
tocar-los.

## Zona segura (obligatori revisar)

El text de línia va al terç superior (regla de `sistema-visual-cbgb`): la UI
d'Instagram tapa el 22% inferior i la banda dreta. Els scripts ja col·loquen el
text a `y0 = H*0.20`, però si canvies mides de fonts o afegeixes línies extra,
comprova que no baixin de `H*0.75` abans d'exportar.

## Caption i estructura de sèrie

Cada peça d'una sèrie ha de tancar amb la mateixa fórmula perquè la gent la
reconegui i vulgui seguir-la:

```
[TITULAR EN MAJÚSCULES DE LA PEÇA]
[3-5 línies del guió, una per frase]

🏀 [PROGRAMA] · [detall: edat/lloc/temporada]
👉 Segueix la sèrie.
[frase que tanca l'enganxada, p.ex. "Cada peça, una excusa menys"]
```

Cadència recomanada: cada 2-3 setmanes, evitant coincidir amb notícia gran del
club. Si la sèrie alimenta una campanya d'inscripcions/captació posterior, deixa
la peça final de la sèrie ("resum"/CTA directe) per just abans que s'obri la
inscripció.

## Referència

`references/exemple-serie-no-cal-res.md` — guió complet de les 6 peces de la
sèrie "No cal res" (Escoleta), a mode d'exemple ja resolt: cada peça desarma una
excusa concreta d'un pare/mare. Fes servir aquest document com a plantilla quan
Ana digui "la peça 2 de la sèrie" o vulgui adaptar l'estructura a un tema nou.
