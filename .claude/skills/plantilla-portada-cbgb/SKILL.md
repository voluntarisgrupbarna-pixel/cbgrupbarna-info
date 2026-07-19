---
name: plantilla-portada-cbgb
description: >
  LA plantilla oficial de portada de reels del CBGB (estil "capítol"): marc
  vermell perimetral, fons en duotò vermell d'un frame del reel, ticker gegant
  tallat a dalt, badge "CAP. XX", titular Anton apilat en blanc amb ombra,
  punch en cursiva amb barra vermella, peu "CB GRUP BARNA · EL CLOT" i escut
  a dalt a la dreta. S'executa per codi (Python/Pillow) amb scripts/portada.py.
  Carregar SEMPRE que es faci la portada/caràtula d'un reel: "fes-me la portada
  del reel", "la portada com sempre", "una altra de la sèrie", "CAP. 02 de...",
  o quan es publiqui qualsevol reel (tot reel surt amb aquesta portada). El
  criteri de conversió viu a portada-reels-cbgb; els valors de marca a
  sistema-visual-cbgb; el ganxo del text a ganxos-cbgb.
---

# plantilla-portada-cbgb — La portada oficial dels reels (estil "capítol")

Plantilla ÚNICA perquè totes les portades de reel surtin de la mateixa mà i la
graella es llegeixi com una sèrie (la coherència és el que converteix, segons
`portada-reels-cbgb`). Aquesta skill és el COM exacte: layout, valors i script.

## Anatomia de la portada (1080×1920, 9:16 vertical)

De dalt a baix, sobre un fons de **frame del reel en duotò vermell**:

1. **Marc vermell perimetral** (36px) — fa de firma de sèrie a la graella.
2. **Ticker tallat** — final d'una frase en Anton gegant, color salmó sobre
   bloc vermell, que entra TALLAT des de fora del llenç per l'esquerra (efecte
   marquesina: "...CABEN AIXÍ."). És la segona veu de la portada: no repeteix
   el titular, el complementa o el contradiu amb ironia.
3. **Escut** a dalt a la dreta, dins del marc.
4. **Badge de capítol** ("CAP. 01") — blanc sobre vermell. Converteix el reel
   en sèrie: el no-seguidor entén que n'hi ha més i té motiu per seguir.
5. **Kicker** — el titular repetit en petit (Inter, caps, tracking) just a
   sobre. Dona ritme editorial de revista.
6. **TITULAR** — Anton blanc apilat en 2-4 línies amb ombra càlida.
   **3-5 paraules, una idea, llegible a 300px** (regla de `portada-reels-cbgb`).
7. **Punch** — la rèplica del titular, en cursiva amb barra vermella a
   l'esquerra ("EL RESULTAT, SÍ."). El gir que fa somriure o picar.
8. **Peu** — "CB GRUP BARNA · EL CLOT" en petit. Sempre igual.

Tot el bloc de text viu al **centre vertical** (zona segura de les 3
retallades: pestanya Reels 9:16, feed 4:5, graella 3:4) i res crític cau al
22% inferior que menja la UI d'Instagram.

## Com generar-la

```bash
python3 scripts/portada.py \
  --bg frame.jpg \                        # o: --video reel.mp4 --t 12.5
  --ticker "CABEN AIXÍ." \
  --cap "CAP. 01" \
  --kicker "LA FEINA QUE NO ES VEU" \
  --title "LA FEINA|QUE NO|ES VEU" \
  --punch "EL RESULTAT, SÍ." \
  --out portada.jpg
```

- `--title`: línies separades amb `|`. La mida s'auto-ajusta a l'amplada.
- `--ticker`, `--cap`, `--kicker`, `--punch`: opcionals — sense `--cap` serveix
  per a peces soltes fora de sèrie; la resta d'elements no es toquen.
- `--video --t`: extreu el frame directament del reel amb ffmpeg.
- Dependència: `pip install pillow` (i ffmpeg només si s'usa `--video`).
- Fonts i escut van a `assets/` dins de la skill (Anton, Inter, escut
  transparent), com mana `sistema-visual-cbgb`.

## Com triar el frame de fons

- **Emoció, no jugada:** cara/gest de celebració o esforç amb qui
  projectar-se (l'estrella ÉS el contingut). Mai un frame borrós a mig moviment.
- El duotò vermell unifica qualsevol foto amb el sistema: no cal que la foto
  original "combini", la plantilla ja la fa de marca.
- Cares millor al **terç superior o costat dret**: el titular ocupa
  l'esquerra-centre i tapa el que hi hagi a sota.

## Com escriure els textos (amb `ganxos-cbgb`)

- **Titular** = el ganxo: què està EN JOC, 3-5 paraules ("LA FEINA QUE NO ES
  VEU", "NINGÚ HI CREIA", "60 ANYS DE CLOT").
- **Punch** = la rèplica que tanca ("EL RESULTAT, SÍ.", "NOSALTRES SÍ.",
  "I ELS QUE VENEN.").
- **Ticker** = final d'una altra frase de la mateixa idea, tallada perquè
  intrigui ("...CABEN AIXÍ.", "...ES GUANYA AQUÍ.").
- **CAP. XX** = numeració contínua de la sèrie. Cada temàtica recurrent pot
  ser una sèrie pròpia; mantenir el compte a la descripció del reel anterior.

## Filtre abans de publicar (resum de `portada-reels-cbgb`)

1. Llegible a 300px (mira-la a mida de miniatura)?
2. Titular ≤5 paraules, una idea?
3. Text i escut dins del centre (cap element crític a dalt/baix on retalla la graella)?
4. Es reconeix com a Barna sense veure l'escut?
5. Pujar-la SEMPRE com a **portada custom** del reel, mai el frame automàtic.

## Relació amb les altres skills

- `portada-reels-cbgb` — el PER QUÈ i el criteri de conversió (aquesta skill n'és l'execució).
- `ganxos-cbgb` — escriure titular/ticker/punch.
- `sistema-visual-cbgb` — valors de marca (aquesta plantilla els aplica).
- `reels-cbgb` / `capcut-reels-cbgb` — el contingut del reel en si.
- `arrencada-reels-cbgb` — control de qualitat del reel sencer abans de publicar.
