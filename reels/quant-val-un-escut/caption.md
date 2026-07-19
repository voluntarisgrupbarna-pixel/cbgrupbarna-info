# Reel — "Quant val un escut?"

**Vídeo:** `reel_ca_SILENT.mp4` (24,2 s, 1080×1920). Subtítols en pantalla en
**català**; el guió de veu en off en **castellà** es va generar amb Higgsfield
(TTS, veu "Elena") i cada pla del vídeo està tallat a la durada EXACTA de la
seva frase perquè encaixi quan s'hi afegeixi l'àudio. **No porta l'àudio
incrustat** — vegeu "Limitació tècnica" més avall.

## Guió ple (veu ES / pantalla CA), amb durades reals

| Pla | Veu en off (castellà) | Pantalla (català) | Durada veu |
|---|---|---|---|
| Hook | "¿Cuánto vale un escudo?" | NO ES VEN. / QUANT VAL UN ESCUT? / La resposta, dins. | 3,10 s |
| 61 | "Sesenta y un años en el barrio." | 61 · ANYS AL BARRI (des de 1965) | 2,58 s |
| 34 | "Treinta y cuatro equipos." | 34 · EQUIPS (totes les categories) | 2,17 s |
| 450+ | "Más de cuatrocientas cincuenta familias. Cada sábado." | 450+ · FAMÍLIES (cada dissabte) | 3,08 s |
| Build | "Ningún número lo dice todo. Pero todos estamos ahí." | CAP NÚMERO HO DIU TOT. / PERÒ TOTS HI SOM. | 4,18 s |
| Drop | "Esto... vale un escudo." | AIXÒ VAL UN ESCUT. | 2,20 s |
| CTA | "Sigue la historia." + **espera de 2 s en silenci al final** (demanat explícitament) | SEGUEIX LA HISTÒRIA. @cbgrupbarna | 1,34 s + hold |

Dades verificades a `data.json` / `index.html` (fundació 1965 → 61 anys el
2026; +34 equips i 450+ famílies, ja publicat a la secció de patrocinis de la
web). No s'hi ha inventat cap xifra ("4 comerços del barri" d'una anàlisi
anterior era un exemple hipotètic, no una dada real — per això no hi és).

## ⚠️ Limitació tècnica important

Aquest entorn no pot descarregar els fitxers d'àudio generats per Higgsfield
(el proxy de xarxa de la sessió bloqueja per política l'host on es guarden —
`cloudfront.net` — codi 403, no és un error puntual, és una restricció
d'organització que no es pot saltar). Per tant **no he pogut incrustar la veu
en off dins del mp4**.

El que sí que tens:
1. El vídeo **mut però amb el timing exacte** de cada frase de la veu en off
   (cada pla dura literalment el mateix que triga a dir-se la seva frase).
2. Els **7 clips d'àudio ja generats** (veu "Elena", castellà) enllaçats als
   resultats de les crides `generate_audio`/`job_display` d'aquesta conversa
   — haurien d'aparèixer com a reproductors a la teva banda del xat. Si no
   et surten, digue-m'ho i te'ls torno a mostrar un per un.
3. Amb aquests dos elements, muntar-ho a CapCut és arrossegar cada clip
   d'àudio sobre el seu pla — ja quadren en durada, no cal retallar res.
4. Alternativa: si em puges els 7 .wav/.mp3 (o me'ls enganxes com a adjunt),
   els incrusto aquí mateix amb ffmpeg i et torno el mp4 final amb so.

## Caption per publicar (castellà — el text a pantalla és només en català)

¿Cuánto vale un escudo?

No lo vendemos. Pero te contamos por qué:
🔴 61 años en el barrio (desde 1965)
🔴 34 equipos, todas las categorías
🔴 450+ familias, cada sábado

Ningún número lo dice todo. Pero todos estamos ahí.

CB Grup Barna · El Clot
👉 Síguenos para la próxima.

#cbgrupbarna #elclot #basquetbase #santmartí

## Notes de producció

- Plantilla aplicada: marc vermell exterior, velo roig càlid (no negre), text amb
  ombra dura, escut sempre a dalt a la dreta (regla fixa d'aquesta sèrie),
  portada homologada pel filtre de qualitat de `portada-reels-cbgb` +
  `disseny-cartells-cbgb` (mateixa peça ja validada, sense tocar-la).
- Fotos reals del club (no generades per IA): jugadora premi dona esport,
  fotos d'equip temporada 25/26, foto d'esdeveniment amb famílies.
- Hold final explícit de 2 s en silenci abans de tallar (demanat: "que te
  esperes al final").
- Versió castellana en pantalla / catalana en veu: repetir
  `compose_scenes.py` traduint els textos i tornar a generar l'àudio amb
  `generate_audio` en l'idioma invers.
