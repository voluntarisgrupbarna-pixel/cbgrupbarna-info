# PROMPT MESTRE — "NINGÚ ET VA DIR QUE PODIAS ENTRAR"
### Reel animat de captació · Escoleta CB Grup Barna · 9:16 · 35,4 s
**Tot el que cal per tornar-lo a fer de zero, o per fer-ne un altre igual.**

---

## EIX EMOCIONAL

**No és un drama. No hi ha culpables. No hi ha llàgrimes.**

La mare no va ser exclosa — simplement ningú la va avisar que hi havia lloc per a ella.
Inèrcia, silenci, una porta sense cartell. I un dia va deixar de botar.

El reel no repara una injustícia. **Obre una porta que abans no tenia rètol.**

La mare que el veu pensa: *"Ah, sí. A mi tampoc em van dir res."*
I la CTA es llegeix com una invitació, no com una disculpa.

---

## 0. LES REGLES DURES

| # | Regla | Per què |
|---|---|---|
| 1 | **VERMELL BARNA = `#E63329`** | No `#CC0000`. No `#E3001B`. **Unifica'ls** als prompts. |
| 2 | **Cap peça surt sense vermell Barna o escut VISIBLE** | Sense marca, un no-seguidor no sap de qui és. |
| 3 | **La marca ha d'estar DINS del món dibuixat** | Samarreta, banderola, bufanda. L'escut a la cantonada no és suficient. |
| 4 | **Cap IA dibuixa l'escut. Mai.** | El deforma sempre. S'incrusta en post amb el PNG real. |
| 5 | **Cap logo comercial a la pilota** | La IA el destrossa. Costures reals sí. |
| 6 | **El grading NO crea color que no existeix** | Si el vermell no és al prompt, no hi serà mai. |
| 7 | **Mai text-to-video amb personatges** | Deriven. Sempre: imatge-primer → animar el keyframe. |
| 8 | **Cap música amb copyright** | Compte d'Empresa → només Meta Sound Collection. Exporta mut. |
| 9 | **Les instal·lacions són dignes** | El pavelló és normal, net, de barri. El problema no eren les instal·lacions — era el silenci. |

---

## 1. FITXA TÈCNICA

| Pas | Model | Paràmetres | Cost |
|---|---|---|---|
| Full de personatge | `nano_banana_pro` | 9:16 · 2k | **2 cr** |
| Keyframes (×8) | `nano_banana_pro` | 9:16 · 2k · `medias: [{role:"image", value:<full>}]` | **2 cr** c/u |
| Animacions (×5) | `kling3_0_turbo` | 9:16 · 1080p · `duration: 5` · `start_image` | **10 cr** c/u |
| Ken Burns (×3) | ffmpeg `zoompan` | — | **0** |
| Rètols, escut, muntatge | Pillow + ffmpeg | — | **0** |
| | | **TOTAL** | **~68 cr** |

> ⚠️ Si Higgsfield suggereix un **preset** → **declina'l** amb `declined_preset_id`. Trencarà l'estil.

---

## 2. BIBLIA D'ESTIL — enganxa-ho a TOTS els prompts

```
ESTIL: animació il·lustrada 2D feta a mà, com un fotograma d'un curtmetratge europeu
independent. Traç de tinta gruixut i segur. Colors plans i limitats. Gra de paper
visible, textura de impressió risogràfica i semitrama subtil. Càlid, humà, lleugerament
imperfecte. Il·lustració editorial contemporània catalana / de Barcelona.

MARCA (OBLIGATÒRIA A CADA FOTOGRAMA): el vermell del club és un vermell VIU, PUR i
SATURAT — RGB(230, 51, 41), hex #E63329. Ha d'aparèixer com un objecte real dins del
món: una samarreta, una banderola a la paret, una bufanda, un banc, un marc de porta.
Mai vermell terracota. Mai vermell maó esmorteït. Mai taronja-vermell.

NO és 3D. NO és Pixar. NO és Disney. NO és anime. NO és fotorealista.
Sense degradats. Sense acabats digitals brillants.

NEGATIU: sense text, sense llegendes, sense etiquetes, sense logos, sense marques
d'aigua, sense noms comercials; sense dits de més, sense mans distorsionades;
sense deriva de faccions; sense degradats; sense ombres plàstiques.
```

---

## 3. L'ÀNCORA — full de personatge

> **Tot el reel depèn d'aquesta cara.** Es genera PRIMER i es passa com a `medias` a TOTS els keyframes.

`nano_banana_pro` · 9:16 · 2k

```
Full de referència de personatge, il·lustració 2D feta a mà. Una nena mediterrània /
catalana de SIS ANYS — petita, galtes rodones, clarament una criatura, no una
preadolescent. Cabell arrissat fosc en cua de cavall descuidada, pigues al nas,
un queixal de llet que falta, una barbeta tossuda. Porta un xandall dels anys 90
ample (blau marí esmorteït i blanc), de segona mà, lleugerament massa gran, i
sabatilles gastades. Porta una pilota de bàsquet taronja gastada amb canals de
costura negres profunds en el patró clàssic de vuit panells — sense cap marca —
que és CLARAMENT MASSA GRAN PER A LES SEVES MANS.

Mostra el MATEIX personatge QUATRE vegades, espaiades uniformement sobre paper
crema llis:
(1) cos sencer, frontal, abraçant la pilota al pit;
(2) cos sencer, tres quarts, a mig bot;
(3) cap i espatlles, neutre;
(4) cap i espatlles, rient amb el forat a les dents.
Proporcions i trets facials idèntics a les quatre.

COLOR: esmorteït i nostàlgic — blau-gris polsós, sèpia esvaïda, crema. L'ÚNIC
objecte saturat és la pilota de bàsquet taronja.
```

*(+ BIBLIA D'ESTIL)*

---

## 4. ELS 8 KEYFRAMES

> Tots amb `medias: [{role:"image", value:<full de personatge>}]` i la frase:
> *"Fes servir la nena de la imatge de referència com a personatge, i reprodueix exactament el seu estil d'il·lustració, el traç i la paleta de colors."*
>
> **✅ = on entra la marca. Cap pla se'n salva.**

---

### PLA 1 · GANXO *(3,0 s · animat)*

```
La nena de sis anys està sola, a mig bot, en un pati escolar de formigó al barri del
Clot de Barcelona, 1997. Blocs de pisos de maó vell, roba estesa als balcons, una
cistella rovellada sense xarxa. La pilota és gairebé massa gran per a les seves mans.
Mentó enlaire, absorbida, feliç.
Tarda tardana. La llum és daurada i suau. El pati és vell però no depressiu.

✅ MARCA: porta una bufanda vermella #E63329 lligada al canell — l'únic color saturat
   a banda de la pilota. És clarament una bufanda d'un club esportiu, molt gastada.

COLOR: tot la resta esmorteït — blau-gris polsós, sèpia, crema.
Vertical 9:16. Terç superior lliure per al títol.
```

---

### PLA 2 · LA PORTA SENSE RÈTOL ★★★ *(4,0 s · animat · ÉS LA PORTADA)*

```
Pla vertical ample. PRIMER PLA, petita i sola: la nena botant la pilota en un pati
de barri al capvespre, 1997. AL FONS, a l'altra banda d'una reixa de filferro: un
pavelló esportiu de barri amb les portes obertes, llum interior daurada que surt a
l'exterior. A dins, un equip de NENS juga a bàsquet — entrenat, animat, pertanyent
a alguna cosa.

La nena s'atura. Mira. El pavelló és proper, normal, accessible. Però no hi ha cap
cartell que digui que ella pot entrar. No hi ha cap senyal per a ella.
Encongeix lleugerament les espatlles — no amb tristesa, sinó com qui passa davant
d'una tenda i no sap si és per a ella — i torna a botar. Segueix endavant.

NO és exclusió activa. NO hi ha ningú dient-li que no passi. Simplement
la porta no té rètol que la cridi.

✅ MARCA: els nens de dins porten samarretes vermelles #E63329. Una gran banderola
   vermella #E63329 penja a la paret del pavelló. El vermell és DINS del pavelló —
   i ella és fora, no perquè l'hagin expulsada, sinó perquè ningú li va dir que entrés.

COLOR: el seu costat fred, esmorteït, gris. El pavelló càlid, daurat, VERMELL.
Vertical 9:16. Curiosa, no trista. Orgullosa i segueix botant.
```

> **Aquest és el pla del reel.** La porta és oberta. Ningú li diu que no. Simplement ningú li diu que sí.

---

### PLA 3 · LA PILOTA ABANDONADA *(3,5 s · Ken Burns)*

```
Sense persones. La pilota de bàsquet taronja gastada jau quieta i polsosa, encallada
al racó fosc d'un traster darrere caixes de cartró i un xandall dels anys 90 plegat.
Un filet prim de llum hi cau a sobre. Teranyines.

✅ MARCA: la bufanda vermella #E63329 del primer pla és plegada al costat, també
   oblidada, també coberta de pols.

COLOR: quasi completament esmorteït a grisos i sèpia. Fins i tot la pilota ha
perdut la seva calidesa.
Vertical 9:16. Silenciós. Quiet. Acabat.
```

---

### PLA 4 · PRESENT *(3,5 s · Ken Burns)*

```
Un pis petit modern de Barcelona, avui. Una dona de 35 anys enfonsar-se al sofà,
cansada, el mòbil a la mà. És INCONFUSIBLEMENT la nena de la imatge de referència
trenta anys més tard: el mateix cabell arrissat fosc (més curt, recollit), les
mateixes pigues, la mateixa barbeta. Al primer pla, la seva filla de SIS ANYS creua
l'habitació, desenfocada pel moviment. La filla s'assembla molt a la nena de la
imatge de referència.

✅ MARCA: la filla porta una samarreta del club vermella #E63329 com a pijama — massa
   gran per a ella, evidentment prestada. L'únic color saturat de l'habitació.

COLOR: esmorteït, quotidià, llum de vespre blau-grisosa.
Vertical 9:16.
```

---

### PLA 5 · EL BOT QUE ENCÉN EL COLOR ★★ *(5,0 s · animat · SENSE TEXT)*

```
La nena de sis anys d'avui — que s'assembla molt a la nena de la imatge de referència
però porta una equipació de bàsquet vermella #E63329 i negra — s'agenolla al terra
de rajoles d'un pis petit de Barcelona. Acaba de treure la pilota de bàsquet taronja
vella del fons d'un armari. La bota una vegada contra les rajoles.

En el MOMENT EXACTE de l'impacte, EL COLOR EXPLOTA CAP A FORA des del punt de contacte
en un esclat radial: el món gris esmorteït s'omple de calidesa i VERMELL SATURAT VIU
#E63329. Pols i llum s'escampen en l'ona expansiva. La seva cara s'il·lumina.

✅ MARCA: el vermell de l'explosió ÉS el vermell del club #E63329. La seva equipació
   és aquest mateix vermell.

Vertical 9:16. La detonació emocional de la pel·lícula. Un cor que torna a bategar.
```

---

### PLA 6 · EL MATEIX PAVELLÓ, ARA SEU ★★★ *(7,0 s · animat, ralentit 1,4×)*

```
Interior del MATEIX pavelló esportiu vist anteriorment des de fora de la reixa —
les mateixes parets de maó, les mateixes portes, les mateixes cistelles — però ara
és PLE DE NENES. Una nena de sis anys (que s'assembla a la imatge de referència)
avança amb la pilota entre les seves companyes, totes nenes d'entre quatre i vuit
anys. UNA ENTRENADORA DONA s'agenolla a la seva alçada, a mig instrucció, assenyalant.
Les graderies estan plenes de famílies. Parquet de color mel.

✅ MARCA (aquest és EL pla de marca — sense contenció):
   - Cada nena porta una equipació vermella #E63329 i negra.
   - Grans banderoles vermelles #E63329 pengen a les parets de maó.
   - Els pares a les graderies porten bufandes vermelles #E63329.
   - L'entrenadora porta un xandall vermell #E63329.

COLOR: completament viu — ombres quasi negres, VERMELL SATURAT VIU #E63329 a tot
arreu, llum àmbar càlida de les finestres altes. L'oposat exacte del pati fred i
esmorteït.
Vertical 9:16. Alegria, soroll, pertinença. Això és el que ella no va tenir.
```

---

### PLA 7 · EL CLÍMAX ★★★ *(6,5 s · animat, ralentit 1,3×)*

```
SENSE VIDRE. SENSE REFLEXOS. SENSE CAP BARRERA.

Una dona de 35 anys seu en un banc de fusta a les graderies d'un pavelló càlid i
ple, mirant la pista, una mà premuda sobre la boca, ulls brillants, SOMRIENT. Somriu
com qui troba una foto antiga i pensa "Mira que bé que era tot això." No plora.
Té tendresa i una mica de gràcia. És la nena de la imatge de referència, trenta
anys més tard.

Asseguda JUST AL SEU COSTAT al mateix banc, TRANSLÚCIDA i fantasmal — semitransparent,
es pot veure el banc a través d'ella — és LA SEVA PRÒPIA JO DE SIS ANYS: exactament
la nena de la imatge de referència, amb el xandall esmorteït dels anys 90, la pilota
taronja a la falda. La nena també mira la pista, tranquil·la i contenta. Senzillament
seuen juntes. Ningú la veu excepte nosaltres.

✅ MARCA: la dona porta una bufanda del club vermella #E63329 al coll. Banderoles
   vermelles #E63329 darrere seu. La nena fantasma porta la seva vella bufanda
   vermella al canell — la mateixa.

COLOR: el pavelló completament viu, vermell viu, àmbar càlid. El fantasma en
blau-sèpia esmorteït, lluminós.
Vertical 9:16. Profundament emotiu però contingut. Tendresa, no sentiment.
```

---

### PLA 8 · LA PORTA OBERTA *(6,0 s · Ken Burns)*

```
Les portes obertes de bat a bat del pavelló esportiu del barri al Clot, Barcelona,
vistes des de FORA al capvespre. Llum daurada càlida surt cap a la vorera. Ningú
bloqueja el pas. La pilota de bàsquet taronja gastada descansa just a l'interior del
llindar, esperant. La reixa de filferro del pla del pati és ara DARRERE LA CÀMERA —
hem entrat per fi.

✅ MARCA: una gran banderola vermella #E63329 penja sobre el marc de la porta oberta.
   El marc de la porta mateix és pintat de vermell de club.

COLOR: carrer en blau capvespre fred; el portal càlid daurat i VERMELL VIU #E63329.
Invitació, no nostàlgia.
Vertical 9:16. Terç inferior lliure i net per al text de CTA.
```

---

## 5. ANIMACIÓ (plans 1, 2, 5, 6, 7)

`kling3_0_turbo` · `start_image` = keyframe · 9:16 · `duration: 5` · `resolution: 1080p`

```
Anima aquesta il·lustració 2D amb moviment contingut, fet a mà. [UNA acció concreta].
Paral·laxi subtil entre primer pla i fons. Moviment de càmera lent i suau cap a dins.

Mantén l'estil del dibuix, el traç, el disseny del personatge i la paleta de colors
IDÈNTICS a la imatge original. Anima en dos fotogrames, com l'animació tradicional
feta a mà.

NEGATIU: sense morfing, sense deriva ni canvi de faccions, sense distorsió del traç,
sense distorsió de càmera, sense personatges afegits, sense canvi d'estil, sense
fotorealisme, sense text.
```

**UNA acció per pla. Res més.**

| Pla | L'acció |
|---|---|
| 1 | Bota dues vegades. La roba estesa oneja. |
| 2 | S'atura, gira el cap cap a la reixa, encongeix les espatlles, torna a botar. |
| 5 | El bot → l'ona de color s'expandeix. |
| 6 | Bota dos passos, l'entrenadora aplaudeix, la grada respira. |
| 7 | Ella parpelleja i somriu; la nena fantasma la mira un instant i torna al partit. |

---

## 6. RÈTOLS (Pillow · Anton · `#E63329` · zones segures IG)

**Zones segures:** text entre **x = 80 i 900**. Res sota **y = 1440**. Ganxo al terç superior.

| Pla | Text | Notes |
|---|---|---|
| 1 | **TU TAMBÉ / JUGAVES.** | Blanc |
| 2 | **PERÒ NINGÚ ET VA DIR / <span style="color:#E63329">QUE PODIAS ENTRAR.</span>** | Última línia en #E63329 |
| 3 | I UN DIA / VAS DEIXAR DE BOTAR. | Blanc · sense acusació |
| 4 | HAN PASSAT / GAIREBÉ TRENTA ANYS. | Blanc |
| 5 | **— cap text —** | El bot parla sol |
| 6 | ARA EL PAVELLÓ / <span style="color:#E63329">TAMBÉ ÉS SEU.</span> // HI HA EQUIP. HI HA ENTRENADORES. HI HA CAMÍ. | "TAMBÉ ÉS SEU" en #E63329 |
| 7 | A TU / NINGÚ ET VA TRUCAR. // <span style="color:#E63329">ARA ET TRUQUEM NOSALTRES.</span> | Última línia en #E63329 |
| 8 | ESCOLETA / <span style="color:#E63329">CB GRUP BARNA</span> / DE 4 A 8 ANYS · EL CLOT // **PORTES OBERTES** / Reserva un entrenament de prova | "CB GRUP BARNA" en #E63329 |

> 🔴 **PENDENT:** confirmar si l'edat és **4 a 7** o **4 a 8 anys** abans de publicar.

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

> ⚡ **El flaix blanc del segon 17 és l'única transició forta.** La resta són fosos. Per això funciona.

**Ken Burns:** `zoompan=z='min(1+0.0011*on,1.13)':s=1080x1920:fps=30` sobre imatge escalada a 2160×3840.

**Export:** `libx264 · crf 20 · yuv420p · 30 fps · high@4.1 · +faststart · SENSE àudio`

---

## 8. POST (zero crèdits)

- **Escut a la cantonada:** PNG real, 210 px d'alt, `overlay=W-w-48:58`, els 35 s sencers.
- **Cloenda:** escut gran (520 px) centrat al pla 8 + barra `#E63329`.
- **Portada:** fotograma del **pla 2** (la porta sense rètol). És el pla que atura el dit.

---

## 9. PUBLICACIÓ

- **So:** exporta MUT. Posa l'àudio des d'Instagram (Meta Sound Collection — compte d'Empresa).
- **Caption:** *"A quantes de vosaltres ningú us va dir que podíeu entrar?"* → comenta **PROVA** i t'enviem l'enllaç.
- **Col·laboració** amb el compte del sènior femení.
