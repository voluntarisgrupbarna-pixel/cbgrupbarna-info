# Recepta tècnica — reel-fotos-cbgb

Aprenentatges reals del muntatge del reel de patrocinis. Llegir abans de renderitzar.

## Estructura i temps (27,0 s exactes)
| Tram | Plans | Durada | Frames @30fps |
|---|---|---|---|
| Hook | h1 + h2 | 1 s + 1 s | 30 + 30 |
| Ràfega beat | b1…b8 | 0,5 s c/u | 15 c/u |
| Emotiu | emo | 6 s | 180 |
| Build | build | 6 s | 180 |
| Drop / escut | drop | 6 s | 180 |
| CTA | cta | 3 s | 90 |

El bed d'àudio marca beats cada 0,5 s → els talls de la ràfega hi encaixen. Si es
canvia la música, usar ~120 BPM perquè els talls quadrin sense re-editar.

## Moviment (Ken Burns) — la manera FIABLE
- Usar `zoompan` amb **supersample moderat** `scale=1512:2688` (no 2160x3840: peta
  per memòria si es fan diversos clips) i **durada exacta per `-frames:v N`** (NO per
  `-t`, que dona 5 s en comptes de 6 s per arrodoniment).
- `z='min(zoom+0.0006,1.075)'` = push-in molt suau. Talls durs a la ràfega (0,5 s:
  el moviment no s'aprecia i alenteix).
- ⚠️ NO llançar diversos `zoompan` supersamplejats EN PARAL·LEL: esgota la RAM i el
  procés mor (exit 137). Un clip per crida; ~7 s cadascun a 1512x2688.

## Muntatge de fitxers (mount locks)
- Alguns fitxers grans del disc de l'usuari (logos a l'arrel, fotos >40 MB) donen
  `Resource deadlock avoided` en copiar. Solucions: copiar des de **subcarpetes**
  (funcionen), reintentar 2-3 cops, o triar una còpia alternativa del mateix asset.
- Escriure els mp4 intermedis a disc local ràpid i evitar renders concurrents que
  bloquegin el mount.

## Escut transparent des d'un logo amb fons blanc
Si només hi ha el logo sobre blanc, fer **flood-fill des de les 4 cantonades**
(BFS) substituint el blanc per alfa 0; així es treu el fons EXTERIOR però es manté
el blanc INTERIOR del triangle. Retallar amb `getbbox()`. (Codi al final.)

## Tractament de marca (grade)
- Near-black `#0E1116`, vermell `#E63329` (token oficial), text Inter/Anton.
- Per pla foto: desaturar ~0,72, contrast 1,08, vel fosc + degradat inferior fort
  (llegibilitat del text) i lleu tint vermell a ombres (5%).
- Escut: watermark ~132 px sobre chip fosc translúcid a dalt-esquerra (marge 80).
  Al drop, escut hèroe ~560 px centrat.

## Errors a evitar
- Jugador/a que ha marxat com a portada → sempre confirmar plantilla vigent.
- Fotos <500 px d'ample a plans llargs (6 s) → es veuen toves; reservar-les a
  ràfega (0,5 s). Per hook/emo/build/drop, mínim ~1200 px.
- Text massa llarg en castellà → el compositor auto-encongeix (fit_font); mantenir-ho.
- CTA només amb @handle → afegir contacte real de patrocinis quan es tingui.

## Snippet: retallar escut (fons blanc → transparent)
```python
from PIL import Image
from collections import deque
im=Image.open("logo_fons_blanc.png").convert("RGBA"); w,h=im.size; px=im.load()
white=lambda p: p[0]>238 and p[1]>238 and p[2]>238
vis=bytearray(w*h); dq=deque()
for x in range(w):
    for y in (0,h-1):
        if white(px[x,y]): dq.append((x,y))
for y in range(h):
    for x in (0,w-1):
        if white(px[x,y]): dq.append((x,y))
while dq:
    x,y=dq.popleft(); i=y*w+x
    if vis[i]: continue
    vis[i]=1
    if not white(px[x,y]): continue
    px[x,y]=(px[x,y][0],px[x,y][1],px[x,y][2],0)
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx,ny=x+dx,y+dy
        if 0<=nx<w and 0<=ny<h and not vis[ny*w+nx]: dq.append((nx,ny))
im.crop(im.getbbox()).save("escut_transp.png")
```
