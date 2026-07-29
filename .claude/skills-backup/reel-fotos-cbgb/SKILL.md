---
name: reel-fotos-cbgb
description: Munta un REEL vertical (9:16) del CB Grup Barna a partir de FOTOS REALS del club amb tipografia cinètica Anton, escut de marca i estructura de gancho viral, executat per codi (Python/Pillow + ffmpeg) sense CapCut. Neix del reel de captació de patrocinadors "Això no es ven amb un logo". Carregar SEMPRE que es demani "fes-me un reel amb fotos", "munta un reel de captació/patrocinis", "un manifest en vídeo", "reel amb el meu material", "posa aquesta jugadora/foto al reel", "afegeix l'escut", "posa-hi moviment", "treu-ne la versió en castellà o sense música". Cobreix; selecció de fotos, tractament de marca, tipografia, escut (overlay fix dalt-dreta + hèroe), línia vermella perimetral, portada custom, sincronia a beat, moviment (push-in), i export bilingüe + muda per a so de tendència. Aporta el COM tècnic; el CRITERI de contingut viu a reels-cbgb, els valors de marca a sistema-visual-cbgb, i l'edició manual a capcut-reels-cbgb/video-club-cbgb.
---

# reel-fotos-cbgb — Reels de fotos reals per codi

Skill d'EXECUCIÓ. Converteix un grapat de fotos del club + un guió curt en un
reel 9:16 publicable, 100% amb codi (Pillow per compondre cada pla, ffmpeg per
al muntatge). Pensada per a peces tipus **manifest / captació / anunci** on el
text és el protagonista i les fotos donen ànima i prova social.

## Quan fer-la servir
- "Munta'm un reel amb aquestes fotos", "reel de patrocinis", "un manifest".
- "Posa aquesta jugadora de portada", "quan surti una noia posa aquesta foto".
- "Afegeix l'escut", "posa-hi moviment", "versió en castellà", "sense música".

## Regla d'or (per què funciona)
1. **Gancho en 2 s amb cara** — obrir amb un/a jugador/a mirant a càmera (millor
   si assenyala). Contacte visual = atura el scroll (`reels-cbgb`).
2. **El text ÉS el subtítol** — Anton gegant en majúscules, un missatge per pla.
   A prova de silenci; no calen subtítols separats.
3. **Estructura fixa** (27 s base, ampliable amb plans "line" de 4 s):
   `hook (2s, 2 talls) → [línies narratives 4s] → ràfega beat (8×0,5s) →
   emotiu (5-6s) → build (5-6s) → drop/escut (5-6s) → CTA (3s)`.
4. **Marca**: near-black `#0E1116`, vermell `#E63329`, marge 80 px, escut hèroe
   al tancament.
5. **Moviment**: push-in suau (Ken Burns) als plans llargs; talls durs a beat.

## ⭐ Regles fixes de marca del reel (decisió Ana, jul-2026 — SEMPRE)
1. **Línia vermella perimetral** `#E63329`, gruix 14 px, a tot el vídeo i a la
   portada. S'aplica com a OVERLAY per ffmpeg sobre el vídeo final, mai
   incrustada als PNGs dels plans (el push-in la faria ballar).
2. **Escut SEMPRE a dalt a la DRETA, NU** — sense cap quadrat, chip ni marc:
   escut transparent ~138 px amb ombra suau (GaussianBlur 8) perquè es llegeixi
   sobre qualsevol foto. Com a OVERLAY fix: no es mou amb el zoom. PROHIBIT
   posar-lo dins d'una caixa (decisió Ana, jul-2026).
3. **Portada custom OBLIGATÒRIA i DINS DEL VÍDEO** per a cada reel (criteri a
   `portada-reels-cbgb`): 1080×1920 vertical, títol Anton al CENTRE (zona
   segura ~1080×1350), línia vermella i escut nu dalt-dreta. A més del PNG,
   la portada es PREPÈN com a primers 9 frames (0,3 s) del vídeo perquè el
   frame 0 sigui la portada (doctrina `arrencada-reels-cbgb`); l'àudio es
   retarda 300 ms (`adelay=300|300`).
4. **Sèrie "EL CLUB ES MOU"**: els anuncis es publiquen com a sèrie per
   capítols. A la portada, sota l'escut nu de dalt-dreta van DUES etiquetes
   JUNTES i alineades a la dreta: chip vermell "EL CLUB ES MOU" + chip fosc
   "CAP. NN" (numeració consecutiva; jul-2026: Gerard Hereter = CAP. 03).
   El TÍTOL de la portada NO és el tema/càrrec (mai "Coordinador"): és el
   mateix GANXO DE RETENCIÓ del vídeo (p. ex. "HEM PRES UNA DECISIÓ… / ESPERA'T
   FINS AL FINAL"), perquè la portada empenyi a mirar el reel sencer, no a
   quedar-se amb la graella. Un element gràfic il·lustrat de cistella (aro +
   xarxa + tauler, línia fina translúcida) va com a ACCENT DISCRET en una
   cantonada (mai al centre, mai sobre la cara del protagonista) — vegeu
   `make_hoop.py` / `draw_hoop()` del reel Gerard Hereter com a patró
   reutilitzable.
5. **Si l'anunci té cartell oficial** (peça dissenyada a part), el cartell va
   COM A PLA FINAL del reel (abans del CTA), full-bleed sense tractament
   `brand()` i amb push-in suau. Sobre el cartell, l'escut de dalt-dreta va
   sempre nu (el mateix overlay únic de tot el vídeo). El GANXO inicial NO revela la
   notícia i demana retenció explícita ("HEM PRES UNA DECISIÓ… / ESPERA'T FINS
   AL FINAL"): el càrrec/reveal es coneix al final. El CTA tanca amb el nom +
   càrrec complet en petit.

### Overlay (com es fa)
- Generar `overlay.png` 1080×1920 RGBA: 14 rectangles concèntrics vermells al
  perímetre + chip d'escut a dalt-dreta.
- Aplicar DESPRÉS del concat: `ffmpeg -i reel.mp4 -i overlay.png
  -filter_complex "[0:v][1:v]overlay=0:0,format=yuv420p" …` i després muxar
  l'àudio. La mateixa `overlay.png` es composa sobre la portada.
- Nota: sobre el pla CTA de fons vermell la línia es fon amb el fons — correcte,
  no canviar el color de la línia.

## Flux de treball (8 passos)
1. **Reunir fotos** per tram (o de la carpeta que passi l'Ana). Fer contact
   sheet i triar per nitidesa i cara. ⚠️ Veure `references/recepta-tecnica.md`
   § "muntatge locks". Fotos <1200 px d'ample: només a ràfega (0,5 s).
2. **Escut transparent**: `assets/escut_transp.png` (ja retallat).
3. **Editar el guió** dins `scripts/compose_reel.py` (diccionari `SCENES`): foto,
   línia de text, tram, biaix de retall (`vbias` i `hbias` per centrar la
   persona), idioma.
4. **Compondre plans**: `python3 scripts/compose_reel.py` → PNGs a `scenes/`.
   Revisar un contact sheet abans de renderitzar. (Sense watermark als plans:
   l'escut va a l'overlay.)
5. **Muntar vídeo**: `bash scripts/build_reel.sh` → clips amb moviment + ràfega
   estàtica + concat. Després **aplicar overlay.png** (línia + escut) i muxar
   àudio → `reel_CA.mp4`, `reel_SILENT.mp4`.
6. **Portada**: generar `portada_reel_*.png` amb les regles fixes de dalt i
   pujar-la com a portada custom del reel (mai el frame automàtic).
7. **Bilingüe**: canviar `LANG=es` i re-executar si cal versió castellà.
8. **QA**: durada exacta en múltiples de 0,5 s (beat-sync a 120 BPM),
   llegibilitat de cada pla, línia vermella visible, escut dalt-dreta fix,
   portada legible a 300 px. Entregar amb SendUserFile + còpia a la carpeta
   de l'Ana.

## Música
- No hi ha generador de música als connectors (Higgsfield només fa veu).
- Opció A (recomanada per abast): entregar `reel_SILENT.mp4` i posar so de
  tendència emotiu ~120 BPM dins d'IG (els talls quadren al beat).
- Opció B: llit sonor sintetitzat per codi (numpy → WAV: piano + pad en menor,
  kick al beat a ràfega/build, riser 2,5 s abans del drop, impacte al drop,
  fade-out final). Vegeu `make_music.py` del reel Gerard Hereter com a patró.
- Entregar SEMPRE les dues versions (MUSICA + SILENT).

## Dependència d'altres skills
- `reels-cbgb` — QUÈ gravar i per què (gancho, formats).
- `portada-reels-cbgb` — criteri complet de la portada.
- `sistema-visual-cbgb` — tokens exactes (color/tipografia/marge/escut).
- `luxury-logic-cbgb` / `codis-lux-cbgb` — to premium i lògica de desig.
- `patrocinis-club` — si el reel és de captació, alinear missatge i CTA.
- `capcut-reels-cbgb` — si es prefereix acabar a mà (subtítols auto, so tendència).

## Filtre de qualitat (abans d'exportar)
- Gancho amb cara/acció als primers 2 s? · Un sol missatge per pla?
- **Línia vermella perimetral a tot el reel i a la portada?**
- **Escut fix a dalt a la dreta (overlay, no incrustat)?**
- **Portada custom feta i legible a 300 px, títol al centre?**
- Vermell #E63329 i near-black? · Durada en múltiples de 0,5 s?
- CTA amb contacte real (no només @handle)? · Versió muda entregada?

Si falla >1, refer abans de publicar.
