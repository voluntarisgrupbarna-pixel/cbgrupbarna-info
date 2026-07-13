# PROMPT MESTRE — "LA PILOTA QUE VAS DEIXAR"
### Reel animat de captació · Escoleta CB Grup Barna · 9:16 · 35,4 s
**Tot el que cal per tornar-lo a fer de zero, o per fer-ne un altre igual.**

---

## 0. LES REGLES DURES (apreses a cops, avui)

| # | Regla | Per què |
|---|---|---|
| 1 | **VERMELL BARNA = `#E63329`** | No `#CC0000`. No `#E3001B`. Els tres surten a les teves skills — **unifica'ls**. |
| 2 | **Cap peça surt sense vermell Barna o escut VISIBLE** | Sense marca, un no-seguidor no sap de qui és. És el coll d'ampolla de conversió. |
| 3 | **La marca ha d'estar DINS del món dibuixat** | Samarreta, banderola, bufanda. Posar l'escut a la cantonada **no és suficient** — això ho vaig fer i no valia. |
| 4 | **Cap IA dibuixa l'escut. Mai.** | El deforma sempre. S'incrusta en post amb el PNG real (`reel-fotos-cbgb/assets/escut_transp.png`). |
| 5 | **Cap logo comercial a la pilota** | La IA el destrossa i és marca aliena. Costures reals sí; Wilson s'incrusta en post si cal. |
| 6 | **El grading NO crea color que no existeix** | Ho vaig provar amb LUT 3D. Si el vermell no és al prompt, no hi serà mai. |
| 7 | **Mai text-to-video amb personatges** | Deriven. Sempre: **imatge-primer** → animar el keyframe. |
| 8 | **Cap música amb copyright** | El compte del club és d'Empresa → només Meta Sound Collection. Exporta **mut** i posa el so des d'Instagram. |

---

## 1. FITXA TÈCNICA (costos REALS mesurats)

| Pas | Model | Params | Cost |
|---|---|---|---|
| Full de personatge | `nano_banana_pro` | 9:16 · 2k | **2 cr** |
| Keyframes (×8) | `nano_banana_pro` | 9:16 · 2k · `medias: [{role:"image", value:<full>}]` | **2 cr** c/u |
| Animacions (×5) | `kling3_0_turbo` | 9:16 · 1080p · `duration: 5` · `start_image` | **10 cr** c/u |
| Ken Burns (×3) | ffmpeg `zoompan` | — | **0** |
| Rètols, escut, muntatge | Pillow + ffmpeg | — | **0** |
| | | **TOTAL** | **~68 cr** |

> ⚠️ Si Higgsfield et suggereix un **preset** ("IN THE DARK" o similar) → **declina'l** amb `declined_preset_id`. Et trencarà l'estil.

---

## 2. STYLE BIBLE — enganxa-ho a TOTS els prompts

```
STYLE: 2D hand-drawn illustrated animation, a frame from an independent European
animated short film. Thick, confident ink linework. Flat, limited colour fills.
Visible paper grain, risograph print texture and subtle halftone. Warm, human,
slightly imperfect - contemporary Catalan / Barcelona editorial illustration.

BRAND (MANDATORY IN EVERY FRAME): the club's red is a HOT, PURE, SATURATED red -
RGB(230, 51, 41), hex #E63329. It must appear as a real object in the world:
a jersey, a wall banner, a scarf, a bench, a doorway. Never a muted brick red,
never terracotta, never orange-red.

NOT 3D. NOT Pixar. NOT Disney. NOT anime. NOT photorealistic. No gradients,
no glossy digital render.

NEGATIVE: no text, no captions, no labels, no logos, no watermark, no brand names;
no extra fingers, no distorted hands; no face drift; no gradients; no plastic shading.
```

---

## 3. L'ÀNCORA — full de personatge

> **Tot el reel depèn d'aquesta cara.** Es genera PRIMER i es passa com a `medias` a TOTS els keyframes. Si aquesta falla, tot falla.

`nano_banana_pro` · 9:16 · 2k

```
Character reference sheet, 2D hand-drawn illustration. A SIX-year-old Mediterranean/
Catalan girl - small, round-cheeked, unmistakably a little kid, not a pre-teen. Dark
wavy hair in a messy ponytail, freckles across the nose, a missing front milk tooth,
a stubborn chin. She wears a baggy 1990s tracksuit (faded navy and white), hand-me-down,
slightly too big, and worn trainers. She carries a worn orange basketball with deep black
seam channels in the classic eight-panel pattern - no branding - that is CLEARLY TOO BIG
FOR HER HANDS.

Show the SAME character FOUR times, evenly spaced on plain cream paper:
(1) full body, front, hugging the ball to her chest; (2) full body, three-quarter,
mid-bounce; (3) head and shoulders, neutral; (4) head and shoulders, laughing with
the gap in her teeth.
Identical proportions and facial features across all four.

COLOUR: drained and nostalgic - dusty blue-grey, faded sepia, cream. The ONLY saturated
object is the orange basketball.
```

*(+ STYLE BIBLE)*

---

## 4. ELS 8 KEYFRAMES

> Tots amb `medias: [{role:"image", value:<full de personatge>}]` i la frase:
> *"Use the girl from the reference image as the character, and match its illustration style, linework and colour palette EXACTLY."*
>
> **✅ = on entra la marca. Cap pla se'n salva.**

### PLA 1 · GANXO *(3,0 s · animat)*

```
The six-year-old girl stands alone, mid-bounce, in an empty concrete schoolyard in the
Clot neighbourhood of Barcelona, 1997. Old brick apartment blocks, laundry on balconies,
a rusty netless hoop. The ball is almost too big for her hands. Chin up, absorbed, happy.
Late afternoon.
✅ BRAND: she wears a faded red #E63329 scarf tied around her wrist - the only saturated
   colour besides the ball. It is clearly a football/basketball club scarf, worn to death.
COLOUR: everything else drained - dusty blue-grey, sepia, cream.
Vertical 9:16. Upper third clear for a title.
```

### PLA 2 · LA TANCA ★★★ *(4,0 s · animat · ÉS LA PORTADA)*

```
Wide vertical shot. FOREGROUND, small and alone: the girl bouncing her ball in a dark
empty concrete schoolyard at dusk, 1997. BACKGROUND, across a chain-link fence: a warmly
lit sports hall, doors wide open, golden light spilling out. Inside, a team of BOYS plays
basketball together - coached, cheered, belonging. She has paused to look through the
fence. Then she keeps bouncing. Alone.
✅ BRAND: the boys inside wear RED #E63329 jerseys. A big RED #E63329 banner hangs on the
   hall's brick wall. The red is INSIDE the hall - and she is outside it. The red is
   literally what she is excluded from.
COLOUR: her side cold, drained, grey. The hall warm, golden, RED.
Vertical 9:16. Loneliness and exclusion - but never pity. She is proud and keeps bouncing.
```

> **Aquest és el pla del reel.** El vermell és el que li neguen. Genial i gratuït.

### PLA 3 · LA PILOTA ABANDONADA *(3,5 s · Ken Burns)*

```
No people. The worn orange basketball lies still and dusty, wedged in the dark corner of a
storage cupboard behind cardboard boxes and a folded 1990s tracksuit. A thin blade of light
falls across it. Cobwebs.
✅ BRAND: the faded RED #E63329 club scarf from the first shot is folded beside it, also
   forgotten, also covered in dust.
COLOUR: almost fully drained to grey and sepia. Even the ball has lost its warmth.
Vertical 9:16. Quiet. Still. Over.
```

### PLA 4 · PRESENT *(3,5 s · Ken Burns)*

```
A small modern Barcelona flat, today. A 35-year-old woman slumped on the sofa, tired,
phone in hand. She is UNMISTAKABLY the girl from the reference image thirty years later:
same dark wavy hair (shorter, tied back), same freckles, same chin. In the foreground her
SIX-year-old daughter crosses the room, blurred by motion. The daughter looks strikingly
like the girl in the reference image.
✅ BRAND: the daughter is wearing an oversized RED #E63329 club t-shirt as pyjamas - too
   big for her, obviously borrowed. The only saturated colour in the room.
COLOUR: muted, everyday, grey-blue evening light. The world is still asleep.
Vertical 9:16.
```

### PLA 5 · EL BOT QUE ENCÉN EL COLOR ★★ *(5,0 s · animat · SENSE TEXT)*

```
The six-year-old girl of today - who looks strikingly like the girl in the reference image
but wears a RED #E63329 and black basketball kit - kneels on the tiled floor of a small
Barcelona flat. She has just pulled the old worn orange basketball from the back of a
cupboard. She bounces it once against the tiles.
At the EXACT INSTANT of impact, COLOUR EXPLODES OUTWARD from the point of contact in a
radial burst: the drained grey world floods with warmth and HOT SATURATED RED #E63329.
Dust and light scatter in the shockwave. Her face lights up.
✅ BRAND: the red of the explosion IS the club red #E63329. Her kit is that same red.
Vertical 9:16. The emotional detonation of the film. A heartbeat restarting.
```

### PLA 6 · EL MATEIX PAVELLÓ, ARA SEU ★★★ *(7,0 s · animat, ralentit 1,4×)*

```
Interior of THE SAME sports hall seen earlier from outside the fence - same brick walls,
same doors, same hoops - but now it is FULL OF GIRLS. A six-year-old girl (who looks like
the reference image) drives with the ball among her teammates, all girls aged four to eight.
A FEMALE COACH kneels at their height, mid-instruction, pointing. The stands are full of
families. Honey-coloured parquet.
✅ BRAND (this is THE brand shot - do not hold back):
   - Every girl wears a RED #E63329 and black basketball kit.
   - Large RED #E63329 banners hang across the brick walls.
   - Parents in the stands wear RED #E63329 scarves.
   - The coach wears a RED #E63329 tracksuit.
COLOUR: fully alive - near-black shadows, HOT SATURATED RED #E63329 everywhere, warm amber
light from the high windows. The exact opposite of the cold, drained schoolyard.
Vertical 9:16. Joy, noise, belonging. This is what she never had.
```

### PLA 7 · EL CLÍMAX ★★★ *(6,5 s · animat, ralentit 1,3×)*

```
NO GLASS. NO REFLECTION. NO BARRIER of any kind.
A 35-year-old woman sits on a wooden bench in the stands of a warm, packed sports hall,
watching the court, one hand pressed over her mouth, eyes wet, smiling. She is the girl
from the reference image, thirty years later.
Sitting RIGHT BESIDE HER on the same bench, TRANSLUCENT and ghostly - semi-transparent,
you can see the bench through her - is HER OWN SIX-YEAR-OLD SELF: exactly the girl from the
reference image, in the faded 1990s tracksuit, the orange ball in her lap. The child is also
watching the court, calm and content. They are simply sitting together. Nobody sees her but us.
✅ BRAND: the woman wears a RED #E63329 club scarf around her neck. RED #E63329 banners
   behind her. The ghost child wears her old faded red wrist-scarf - the same one.
COLOUR: the hall fully alive, hot red, warm amber. The ghost in faded blue-sepia, glowing.
Vertical 9:16. Deeply emotional but restrained. Not sentimental.
```

### PLA 8 · LA PORTA OBERTA *(6,0 s · Ken Burns)*

```
The wide open doors of the neighbourhood sports hall in the Clot, Barcelona, seen from
OUTSIDE at dusk. Warm golden light pours out onto the pavement. Nobody blocks the way.
The worn orange basketball rests just inside the threshold, waiting. The chain-link fence
from the schoolyard shot is now BEHIND the camera - we are inside it at last.
✅ BRAND: a large RED #E63329 banner hangs above the open doorway. The doorframe itself is
   painted club red.
COLOUR: street in cool blue dusk; the doorway warm gold and HOT RED #E63329.
Invitation, not nostalgia.
Vertical 9:16. Lower-middle third clean and simple for the CTA text.
```

---

## 5. ANIMACIÓ (plans 1, 2, 5, 6, 7)

`kling3_0_turbo` · `start_image` = keyframe · 9:16 · `duration: 5` · `resolution: 1080p`

```
Animate this 2D illustration with restrained, hand-drawn motion. [UNA acció concreta].
Subtle parallax between foreground and background. Slow, gentle camera push-in.

Keep the drawing style, the linework, the character design and the colour palette
IDENTICAL to the source image. Animate on twos, like traditional hand-drawn animation.

NEGATIVE: no morphing, no drifting or changing facial features, no warping of the linework,
no camera distortion, no added characters, no style change, no photorealism, no text.
```

**UNA acció per pla. Res més.** L'animació IA es deforma si li demanes massa.

| Pla | L'acció |
|---|---|
| 1 | Bota dues vegades. La roba estesa oneja. |
| 2 | S'atura, gira el cap cap a la tanca, torna a botar. |
| 5 | El bot → l'ona de color s'expandeix. |
| 6 | Bota dos passos, l'entrenadora aplaudeix, la grada respira. |
| 7 | Ella parpelleja; la nena fantasma la mira un instant i torna al partit. |

---

## 6. RÈTOLS (Pillow · Anton · `#E63329` · zones segures IG)

**Zones segures:** text entre **x = 80 i 900**. Res sota **y = 1440**. Ganxo al terç superior.

| Pla | Text |
|---|---|
| 1 | **TU TAMBÉ / JUGAVES.** |
| 2 | **PERÒ L'EQUIP / ERA PER A ELLS.** *("ERA PER A ELLS" en #E63329)* |
| 3 | UN DIA VAS / DEIXAR DE BOTAR. // NINGÚ ET VA / PREGUNTAR PER QUÈ. *(última línia en #E63329)* |
| 4 | HAN PASSAT / GAIREBÉ TRENTA ANYS. |
| 5 | **— cap text —** *(el bot parla sol)* |
| 6 | ARA EL PAVELLÓ / TAMBÉ ÉS SEU. // HI HA EQUIP. HI HA ENTRENADORES. HI HA CAMÍ. *("TAMBÉ ÉS SEU" en #E63329)* |
| 7 | **A TU ET VAN / DEIXAR FORA.** // **A ELLA, NO.** *("A ELLA, NO." en #E63329)* |
| 8 | ESCOLETA / CB GRUP BARNA / DE 4 A 8 ANYS · EL CLOT / **PORTES OBERTES** / Reserva un entrenament de prova *("CB GRUP BARNA" en #E63329)* |

> 🔴 **PENDENT:** l'àudio del club diu **4 a 7**, el rètol diu **4 a 8**. Un dels dos és fals. **CONFIRMAR ABANS DE PUBLICAR.**

---

## 7. MUNTATGE (ffmpeg · 35,4 s)

| Pla | Durada | Transició sortint |
|---|---|---|
| 1 | 3,0 s | `fade` 0,4 |
| 2 | 4,0 s | `fadeblack` 0,5 |
| 3 | 3,5 s (Ken Burns) | `fadeblack` 0,5 |
| 4 | 3,5 s (Ken Burns) | `fade` 0,4 |
| 5 | 5,0 s | ⚡ **`fadewhite` 0,3** |
| 6 | 7,0 s (`setpts=1.4*PTS`) | `fade` 0,5 |
| 7 | 6,5 s (`setpts=1.3*PTS`) | `fadeblack` 0,5 |
| 8 | 6,0 s (Ken Burns) | — |

> ⚡ **El flaix blanc del segon 17 és l'única transició forta de tot el reel.** La resta són fosos. Per això funciona: el *drop* té on caure.

**Ken Burns:** `zoompan=z='min(1+0.0011*on,1.13)':s=1080x1920:fps=30` sobre la imatge escalada a 2160×3840.

**Export:** `libx264 · crf 20 · yuv420p · 30 fps · high@4.1 · +faststart · SENSE àudio`

---

## 8. POST (zero crèdits)

- **Escut a la cantonada:** PNG real, 210 px d'alt, `overlay=W-w-48:58`, els 35 s sencers.
- **Cloenda:** escut gran (520 px) centrat al pla 8 + barra `#E63329`.
- **Portada:** fotograma del **pla 2** (la tanca). És el pla que atura el dit.

---

## 9. PUBLICACIÓ

- **So:** exporta MUT. Posa l'àudio des d'Instagram (**Meta Sound Collection** — el compte és d'Empresa, no pot fer servir música comercial).
- **Caption:** *"A quantes de vosaltres us van deixar fora?"* → comenta **PROVA** i t'enviem l'enllaç.
- **Col·laboració** amb el compte del sènior femení.
