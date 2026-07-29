# Recetas ffmpeg — edit estrella sobre fotos/clips

Colores marca: rojo `0xE3001B`, negro. Tipografía: condensada bold (sustituir por la
oficial del club cuando esté en disco).

## 1. Beat-sync por duración
Elige música y su BPM. Duración por foto = (60 / BPM) × beats_por_foto.
- 120 BPM, 2 beats/foto → 1.0 s · 128 BPM, 2 beats → 0.94 s · 90 BPM, 2 beats → 1.33 s.
Pon TODAS las fotos a esa duración para que los cortes caigan en el golpe.

## 2. Clip de foto con Ken Burns (zoom in)
```
ffmpeg -y -loop 1 -t 1.0 -i base.jpg -vf \
"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,\
zoompan=z='min(zoom+0.0012,1.16)':d=30:s=1080x1920:fps=30" \
-r 30 -c:v libx264 -pix_fmt yuv420p -crf 21 clip.mp4
```
Truco de velocidad: prepara primero una `base.jpg` ya recortada a 1080x1920 (un solo
frame) y aplica el zoompan sobre ella; evita re-decodificar el original pesado por frame.

## 3. Transiciones con energía (xfade, ffmpeg 4.4)
Válidas y con punch: `slideleft slideright slideup slidedown smoothleft smoothright
circleopen circleclose pixelize hrslice hlslice vuslice diagtl diagbr dissolve
fadeblack fadewhite`. (Nota: `zoomin` NO existe en 4.4; usar 5.x para eso.)
```
ffmpeg -i a.mp4 -i b.mp4 -filter_complex \
"[0][1]xfade=transition=fadewhite:duration=0.25:offset=OFFSET[v]" -map "[v]" out.mp4
```
`OFFSET` = duración de A menos la duración de la transición. Para cadenas largas, encadena
`[v1][2]xfade=...:offset=acumulado[v2]...`.

## 4. Flash blanco a beat (impacto)
Inserta 2 frames blancos en el golpe:
```
ffmpeg -f lavfi -i color=white:s=1080x1920:d=0.06:r=30 -c:v libx264 -pix_fmt yuv420p flash.mp4
```
Concaténalo en el punto del beat (o usa transición `fadewhite` muy corta, 0.12 s).

## 5. Whip / zoom-blur de cambio de bloque (aprox.)
Sobre el final de A: zoom rápido + desenfoque.
```
-vf "zoompan=z='min(zoom+0.03,1.5)':d=8:fps=30,boxblur=6:1"
```
en los últimos ~8 frames del clip de salida; el de entrada empieza ya nítido.

## 6. Velocidad / "slow-mo" sobre clip real (no foto)
```
ffmpeg -i clip.mp4 -vf "setpts=2.0*PTS" -an slow.mp4   # mitad de velocidad
ffmpeg -i clip.mp4 -vf "setpts=0.5*PTS" -an fast.mp4   # doble
```
Para slow suave conviene grabar a 60 fps. Rampa = concatenar tramo rápido + tramo lento.

## 7. Color grade marca (contraste + rojos)
```
-vf "eq=contrast=1.12:saturation=1.15:brightness=-0.02,curves=preset=increase_contrast"
```

## 8. Cierre con identidad (logo + hashtag)
```
ffmpeg -i in.mp4 -i logo.png -filter_complex \
"[1]scale=180:-1[lg];[0][lg]overlay=W-w-40:40:format=auto" out.mp4
```
Últimos 1–2 s: tarjeta negra con logo centrado + `#CBGrupBarna` + CTA, corte a beat.

## 9. Audio normalizado para IG
```
ffmpeg -i in.mp4 -i music.m4a -filter_complex "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
-map 0:v -map "[a]" -shortest -c:v copy -c:a aac out.mp4
```
(Para publicar en IG poniendo música oficial desde la app: exporta SIN audio.)

## Orden recomendado (automático)
base.jpg (1 frame) → clip Ken Burns por foto a duración de beat → cadena xfade con
transiciones variadas (fuertes en cambio de bloque) → flashes a beat → color grade →
cierre identidad → (audio o silencio para IG).

---

## 10. Homenaje / testimonial (voces a cámara + subtítulos)

Este formato NO es de fotos: son clips de gente hablando. Lo automatizable es quemar
subtítulos, cortar a beat y cerrar con marca; el orden emocional de las voces lo decide
la persona.

**Flujo recomendado**
1. **Selecciona y ordena** los cortes de voz (4–8), de menos a más emotivo. Guarda la
   frase potente para el final. Recorta "eeeh" y silencios (`cut.sh` de video-club-cbgb).
2. **Subtítulos.** Genera un `.srt` (auto en CapCut/Whisper) y **revísalo a mano**;
   luego quémalo con estilo grande y legible:
```
ffmpeg -i voces.mp4 -vf "subtitles=subs.srt:force_style=\
'FontName=Oswald,Fontsize=13,PrimaryColour=&H00FFFFFF,\
OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=1,\
Alignment=2,MarginV=90'" -c:a copy voces_sub.mp4
```
   (O usa `subs.sh` de `video-club-cbgb`, que ya aplica el estilo de marca.)
3. **Ducking** de la música bajo la voz (la música baja sola cuando alguien habla):
```
ffmpeg -i voces_sub.mp4 -i musica.m4a -filter_complex \
"[1:a]volume=0.5[m];[0:a][m]sidechaincompress=threshold=0.03:ratio=8:release=300[a]" \
-map 0:v -map "[a]" -shortest -c:v libx264 -crf 20 -c:a aac out.mp4
```
4. **Cierre:** tarjeta negra (#0E1116) con la frase clave + escudo + nombre + claim
   ("GRÀCIES, CAPITANA"), 2–3 s, y un respiro de silencio (usa `brand.sh`).
5. **Ritmo:** si intercalas planos de detalle/BTS/archivo entre voces, córtalos a beat
   (mismo criterio que el resto del skill).

**Errores típicos:** cortes demasiado largos (recorta), sin subtítulos (la mayoría lo
ve en mute), música tapando la voz (falta ducking), orden plano sin clímax.
