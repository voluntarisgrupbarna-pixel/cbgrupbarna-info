---
name: web-cbgb
description: Sistema de disseny de les webs del CB Grup Barna (cbgrupbarna.info i satèl·lits). Carrega-la SEMPRE abans de tocar HTML, CSS o qualsevol peça visual del club: colors, tipografia, fotografia, vocabulari, modes clar i fosc, i les trampes tècniques del repositori. Inclou el vermell oficial mostrejat de l'escut i per què no és el mateix que el de vídeo.
---

# Sistema de disseny · web CB Grup Barna

Val per a `cbgrupbarna.info` i per a tot el que en pengi. Si una peça respecta
aquestes regles, es reconeix com del club sense veure l'escut.

Aquesta skill dona el **sistema visual**. Per a l'**inventari de contingut i
l'arquitectura tècnica** (què hi ha, quin script genera què, quins robots
corren sols), veure `mapa-web-cbgb`.

---

## 0. Abans de tocar res

**Comprova que edites la font real.** Aquest repositori ha tingut còpies locals
desfasades. Compara el `<title>` del fitxer amb el del lloc publicat abans de
canviar res; si no coincideixen, atura't i pregunta.

---

## 0 bis. La web i l'Instagram són la mateixa marca

La tesi que ordena tota la resta: **qui salta del perfil a la web no ha de notar
que canvia de club.** L'Instagram ja té un sistema tancat i respectat; la web és
la que s'hi ha d'alinear, no al revés.

### El que l'Instagram ja fa bé

- **Tres colors i prou** — vermell, negre, blanc. La foto fa de quart color.
- Cadència sostinguda i **sèries reconeixibles**: «La feina que no es veu»,
  «Bàsquet femení», «Dies de partit».
- El que arriba és **història emocional**, no pòster informatiu. Els reels de
  l'escoleta femenina i de l'staff són els que més volen.
- Un reel mitjà toca ~96% dels seguidors: la base està sana.

### Els tres trencaments que separaven les dues cares

| | Trencament | Estat |
|---|---|---|
| 1 | **Color** — al CSS convivien groc, verd, blau i taronja, cap d'ells de l'IG | Resolt: punt 1 |
| 2 | **Vocabulari** — «Partits i events», «Partits i resultats» i «Calendari» com a tres entrades | Resolt: punt 5 |
| 3 | **Jerarquia** — 8.500 px d'alçada i un bloc «Tot a mà» amb 25+ enllaços plans | Resolt: les franges |

### Com es lliguen, peça a peça

| Web | Instagram |
|---|---|
| Pilar «Escoleta» | Destacada «Escoleta» |
| Bloc «Dies de partit» | Sèrie de stories del cap de setmana |
| Hero editorial de l'extensa | Mateixa foto que la portada del post fixat |
| Fitxa d'entrenador/a | Sèrie «La feina que no es veu» |

**Els quatre destacats del perfil són els quatre pilars de la web.** Si canvien
al perfil, canvien a la web.

### Les dues velocitats de lectura

No són propostes excloents: **la portada té les dues i un commutador**, perquè
serveixen públics diferents.

| | **Franges** (per defecte) | **Extensa** (editorial) |
|---|---|---|
| Per a qui | El dit que acaba de tocar l'enllaç de la bio: mòbil, tres segons de paciència | Qui investiga: famílies, premsa, patrocinadors |
| Forma | Rectangles amples, una porta per franja, tot a un toc | Portada de diari: foto gran, titular editorial, pilars |
| Guanya | Conversió. Menys d'un segon per entendre on tocar | Autoritat i SEO real: la web té contingut propi, no només enllaços |
| Costa | Gairebé res de manteniment | Una foto editorial bona cada temporada i el bloc de partits viu |
| Risc | Davant un patrocinador, una graella d'enllaços no sosté el discurs | Si l'IG canvia de sèries i la web no, es tornen a separar |

L'estructura de les franges està calcada de la guia visual. **Si canvies l'ordre
o els textos d'una, canvia'ls a l'altra**: la portada i la guia han de dir el
mateix.

### Nota sobre les guies antigues

Hi ha una guia anterior —«Web + Instagram: dues propostes», agost 2026— que
proposava **Bebas Neue** i el vermell **`#E31E24`**, amb negre `#050505` i
JetBrains Mono per a dades. **Aquells valors no manen.** La decisió tancada és
Anton i `#E20613` (punts 1 i 2), perquè el vermell està mostrejat de l'escut i
`#E31E24` no arriba al contrast mínim sobre crema. La resta d'aquella guia —la
tesi, el diagnòstic i les dues propostes— sí que val, i és el que hi ha aquí
sobre.

---

## 1. Un sol vermell: el de l'escut

| Token | Valor | Ús |
|---|---|---|
| `--red` | `#E20613` | L'únic accent. Mostrejat de `logo.png` i `icon-512.png`. |
| `--red-ink` | `#A8040E` | Text vermell sobre fons clar i estats de passar-hi el ratolí. |
| `--ink` | `#10100E` | Tinta. |
| `--paper` / `--cream` | `#FFFFFF` / `#F4F1EC` | Fons. |

Contrast sobre blanc: `#E20613` dona 4,92:1 i `#A8040E`, 7,81:1. Tots dos passen
el mínim AA per a text.

**No facis servir `#FD030C`**, que és el vermell de la cartela de vídeo de
`sistema-visual-cbgb`. Sobre blanc dona 4,04:1 i sobre crema 3,59:1, per sota
del mínim. Per a vídeo és correcte; per a web, no.

Sobre fons fosc el vermell s'aclareix a `#FF3B41`, que hi recupera contrast.

### El que no hi va
Groc, verd, blau i taronja **no són colors de marca**. Excepcions, i només
aquestes:
- **Semàntics de resultat**: `--win` i `--loss` a `/partits/`. Serveixen per dir
  si un partit s'ha guanyat o s'ha perdut, mai per decorar.
- **Marques d'altri**: Instagram, WhatsApp i TikTok porten el seu color.
- **La bandera de l'Orgull** a `/orgull/`. No s'hi toca.

---

## 2. Dues tipografies, i prou

- **Anton** per a display: caixa alta, gran, atapeïda, interlineat curt.
- **Inter** per a text, dades i etiquetes. Les etiquetes van en caixa alta amb
  molt interlletratge (`0.18em`–`0.28em`).

Els fitxers són a `.github/scripts/fonts/`. Incrusta'ls com a `data:` URI si la
peça ha de funcionar sense xarxa. Màxim dues famílies per peça.

---

## 3. Fotografia

**Cap cara tallada.** Totes les fotos s'enquadren des de dalt
(`object-position: center top`). El que es perd en retallar és el terra, mai el cap.

**Cap foto ampliada.** Una imatge no s'ha de mostrar mai més gran del que és, i
en pantalla retina calen el doble de píxels dels que ocupa. Si el fitxer no hi
arriba, hi ha dues sortides honestes: canviar la foto o **fer més petit el marc**.
Ampliar-la es nota sempre.

**Només fotos de qualitat.** Nítides, ben exposades i sense gra ni desenfocament
de moviment. Una foto fluixa abaixa tota la pàgina: si no n'hi ha cap de bona
per a una peça, val més una franja de color pla que una foto dolenta.

> Estat actual: les fotos de `img/` fan entre 360 i 550 px d'ample. No hi ha
> originals més grans al repositori. Qualsevol maqueta amb marcs amples les
> delatarà. I no hi ha **cap foto moderna en alta de l'Escoleta (4-7 anys)**:
> això es resol amb una sessió de fotos, no amb codi.

---

## 4. Res caducat a la portada

El que ja ha passat no obre la web. Rotació per estació:

| Temporada | Què mana a la portada |
|---|---|
| Set – Des | Escoleta, portes obertes, dies de partit |
| Gen – Mar | Dies de partit, sèniors, femení |
| Abr – Jun | Final de temporada, 3x3, inscripcions |
| Jul – Ago | Campus, temporada nova |

Això inclou `og-image.jpg`: es regenera amb
`python3 .github/scripts/generate-og-image.py` després de canviar-hi el contingut.

---

## 5. El mateix nom a tot arreu

Una cosa es diu igual a Instagram i a la web.

| Destacada d'IG | Etiqueta a la web |
|---|---|
| Dies de partit | **Dies de partit** (mai «Calendari», «Partits i resultats» ni «Partits i events») |
| — | **Dies de partit per equip** per a `/partits/calendaris/` |
| Escoleta | Escoleta |
| El club | El club |

Els `<title>` i les descripcions sí que poden portar termes de cerca
(«calendari», «resultats»); les **etiquetes i els enllaços**, no.

---

## 6. Modes clar i fosc

La pàgina s'adapta al mode del dispositiu, però **qui la llegeix ha de saber en
quin està i poder-lo canviar**. Posa-hi un control visible amb tres estats:
*sistema*, *clar* i *fosc*. «Sistema» no és el mateix que «clar»: pot canviar sol
al vespre, i per això s'ha d'anomenar a part i indicar a què resol ara mateix.

Defineix la paleta clara al `:root` pelat, i redefineix **només els tokens** dins
de `@media (prefers-color-scheme: dark)` amb el guard
`:root:not([data-theme="light"])`, i un altre cop a `:root[data-theme="dark"]`.
Cap color pot tenir la seva única definició dins d'un bloc de mode.

---

## 7. Trampes d'aquest repositori

- **`scripts/build-pages.py` genera** blog, campus, 3x3, premsa i patrocinadors.
  Edita el generador, no la sortida. **Avís: el generador està desfasat respecte
  al que hi ha publicat** — executar-lo revertirà un repàs d'SEO i un article del
  blog reescrits a mà. Comprova el `git diff` sencer abans de desar.
- **`.github/scripts/generate-team-pages.py`** genera `partits/equips/`.
- **`.github/scripts/generate-seo-snapshot.py`** només reescriu entre els
  marcadors `SEO-SNAPSHOT`, `SEO-EVENTS` i `SEO-EQUIPS`. Fora d'aquí és segur.
- **`partits/data.json`** el refresca un robot diari. Els canvis manuals hi duren poc.

## 8. Trampes de CSS que ja ens han mossegat

- `aspect-ratio` **no s'aplica a elements en línia**. Un `<span>` que faci de marc
  d'imatge necessita `display:block`, si no la imatge es desboca. Els fills de
  grid i flex ja es converteixen en bloc sols.
- **Especificitat**: `.bands .band:nth-child(even)` (0,3,0) guanya a `.band.solid`
  (0,2,0) i deixa text blanc sobre fons clar. Exclou els casos amb `:not()`.
- **Codificació**: si el servidor no declara UTF-8, els accents es trenquen. En
  peces que han de viatjar, converteix els accents a entitats numèriques — i
  recorda que `textContent` **no** interpreta entitats: allà fes servir `·`.
- **Amplada del menú**: un text llarg pot partir la navegació en tres línies.
  Els enllaços secundaris porten `.opt` i cauen primer entre 1080 i 1280 px.

## 9. Abans de publicar

1. Els colors surten de la taula del punt 1?
2. Cap cara tallada i cap foto ampliada?
3. Res amb data passada, `og-image.jpg` inclosa?
4. Les etiquetes fan servir el vocabulari del punt 5?
5. Funciona en clar i en fosc, i es veu en quin mode s'està?
6. Si has tocat una pàgina generada, has editat el generador?
7. Sense desbordament horitzontal, i amb focus visible al teclat?
