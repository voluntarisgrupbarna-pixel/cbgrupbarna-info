---
name: web-cbgb
description: Sistema de disseny de les webs del CB Grup Barna (cbgrupbarna.info i satèl·lits). Carrega-la SEMPRE abans de tocar HTML, CSS o qualsevol peça visual del club: colors, tipografia, fotografia, gràfics i dades, vocabulari, modes de color i les trampes tècniques del repositori. Diu quin és el vermell oficial mostrejat de l'escut i per què no és el de vídeo; quins dos jocs de tokens i quines dues tipografies de display hi conviuen, i com no barrejar-los; on són els originals de foto i com passar-los pel script perquè cap surti ampliada; i quines pàgines generades encara no es poden regenerar sense perdre-hi contingut.
---

# Sistema de disseny · web CB Grup Barna

Val per a `cbgrupbarna.info` i per a tot el que en pengi. Si una peça respecta
aquestes regles, es reconeix com del club sense veure l'escut.

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

El vermell és el mateix a tot arreu. Els **noms dels tokens, no**: al repositori
hi conviuen dos jocs, i confondre'ls fa que una regla no s'apliqui.

**Sistema principal** — `css/barna.css`, i la portada, que porta el CSS a dins
però amb els mateixos valors. Cobreix blog, campus, 3x3, premsa, patrocinadors,
femení, `/es/`, `/en/` i `partits/equips/`.

| Token | Valor | Ús |
|---|---|---|
| `--red` | `#E20613` | L'únic accent. Mostrejat de `logo.png` i `icon-512.png`. |
| `--red-dark` | `#A8040E` | Text vermell sobre fons clar i estats de passar-hi el ratolí. |
| `--ink` | `#0a0a0a` | Tinta. |
| `--ink-2` | `#46433f` | El text corrent. |
| `--muted` | `#8a8681` | Etiquetes petites. Vegeu l'avís de sota. |
| `--line` | `#e4e1dd` | Filets. |
| `--paper` / `--paper-2` | `#ffffff` / `#f6f4f1` | Fons. |

**`/partits/` té el seu propi joc**, perquè és una pàgina autònoma: allà el
vermell fosc es diu `--red-ink`, el fons crema `--cream` (`#F4F1EC`), la tinta
`--ink` val `#0E1116` i el gris `--muted` és `#6B6560`. El vermell d'accent és
el mateix. Si copies codi d'una banda a l'altra, tradueix els noms.

Contrast mesurat sobre blanc: `#E20613` dona 4,92:1 i `#A8040E`, 7,81:1 — tots
dos passen el mínim AA per a text. Blanc sobre `--red` també dona 4,92:1.

> **`--muted` no arriba a AA.** `#8a8681` sobre blanc dona 3,62:1, i sobre
> `--paper-2`, 3,29:1: per sota del 4,5:1 que demana el text. Al sistema només
> s'hi posen etiquetes en caixa alta de 8,5 a 10 px, que és justament la mida on
> més es nota. **No hi posis mai text que s'hagi de llegir de debò.** El dia que
> es refaci, `#706c67` dona 5,21:1 sobre blanc i 4,75:1 sobre crema, i passa als
> dos fons. `--muted` de `/partits/` (`#6B6560`) ja hi arriba.

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

## 2. Tipografia: Anton i Inter, i prou

Dues famílies, i les mateixes a tot arreu.

- **Anton** és la display: `--display: 'Anton', 'Haettenschweiler', 'Arial Narrow', sans-serif`.
  Caixa alta, un sol gruix (400), interlletratge gairebé nul (`0.02em`) i
  interlineat curt (`1.04`). Anton **no té pesos**: si veus `font-weight: 300`
  en una regla de display, és codi antic de quan hi havia Jost.
- **Inter** per a text, dades i **etiquetes**. Les etiquetes petites en caixa
  alta amb molt interlletratge (`0.18em`–`0.28em`) van en Inter, **no** en
  Anton: Anton amb `letter-spacing: 0.2em` queda malament.

Aquesta és la separació que costa de veure i la que més s'equivoca: *display
gran → Anton; etiqueta petita amb tracking → Inter*.

### Anton s'auto-allotja

Els dos subconjunts són a **`/fonts/`** i es declaren amb `@font-face` a
`css/barna.css` i al `<style>` de la portada. **No es demana a Google Fonts**, i
és a posta: així no s'envien les IP de les famílies a un tercer. `/escoleta/`
fa el mateix des de `escoleta/fonts/` i ho documenta igual.

Inter sí que ve encara de Google Fonts. És el següent a auto-allotjar.

Els `.ttf` de `.github/scripts/fonts/` **no són per al web**: els fan servir
`generate-og-image.py` i `generate-calendaris.py` per dibuixar imatges amb
Pillow.

> **Jost ja no s'usa enlloc.** Era la display fins a l'agost del 2026; es va
> substituir per Anton a les 100 pàgines perquè la guia i aquesta skill sempre
> havien dit Anton i el web no ho complia. Si trobes `Jost` en algun fitxer, és
> un residu: treu-lo, no el propaguis.

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

Les fotos ja retallades de `img/` fan entre 360 i 550 px d'ample: serveixen per a
marcs petits i prou. Les fotos de la galeria són a `fotos/web/<album>/` (versió
web) i `fotos/thumb/<album>/` (miniatura); els originals grans només queden a
`fotos/uploads/` per als àlbums més nous, la resta viuen fora del repositori.
També hi ha `photos/` (retrats d'estudi, sèniors, entrada de la pista, mascota),
entre 700 i 1600 px.

**No enllacis mai un original**: pesen fins a 14 MB. Passa'ls per
`scripts/build-blog-images.py`, que retalla des de dalt, comprimeix a WebP i en
treu dues mides (`nom.webp` i `nom@2x.webp`). Aquell script **es nega a generar**
qualsevol peça que hagi de mostrar-se més gran del que és: si t'avisa, no forcis
res, fes més petit el marc.

> El que segueix faltant és **una foto moderna en alta de l'Escoleta (4-7 anys)**:
> l'única que hi ha és `img/escoleta@2x.webp`, de 750 px. Això es resol amb una
> sessió de fotos, no amb codi.

---

## 4. Gràfics i dades

**Un gràfic es fa amb HTML i CSS, no amb una imatge.** Una captura d'un gràfic
es veu borrosa, no es pot seleccionar, no la llegeix un lector de pantalla i el
text se n'hi fa il·legible al mòbil. Un SVG amb text a dins té el mateix
problema: si l'SVG escala, la lletra escala amb ell.

L'SVG només val per a **geometria pura i sense text** —una pista, un plànol— i
amb `vector-effect: non-scaling-stroke` perquè les línies no s'aprimin.

Els components ja fets viuen a `css/barna.css`: `.bars` (barres comparades),
`.scale` (trams proporcionals: edats, mesos, setmanes), `.ratio` amb `.dots`
(comptar persones d'una en una), `.gauge` (una escala amb la franja on la cosa
es trenca), `.split` (un repartiment en dos trams), `table.vs` (comparativa) i
`.court` (la pista). N'hi ha exemples de tots a `/blog/`.

Tres regles que no es negocien:
- **Un sol accent, el vermell**, i marca'n *una* cosa. Cinc barres vermelles no
  destaquen res.
- **Cap dada distingida només pel color.** Sempre porta el número o l'etiqueta al
  costat: qui no distingeix el vermell del gris ha de poder llegir el gràfic.
- **Cap llegenda que no correspongui al dibuix.** Si el vermell marca un llindar,
  no el facis servir també per dir «per sota del llindar».

---

## 5. Res caducat a la portada

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

## 6. El mateix nom a tot arreu

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

## 7. Modes clar i fosc

**Avui no n'hi ha cap.** Cap fitxer del repositori té `prefers-color-scheme` ni
`data-theme`: tot el lloc és clar, i el fosc només hi surt com a superfície
puntual (`.foot`, `.franja--ink`). No afegeixis mig mode fosc a una pàgina
solta: o es fa a `css/barna.css` per a tot el sistema, o no es fa.

Si algun dia s'hi posa, això és el que ha de complir. La pàgina s'adapta al mode
del dispositiu, però **qui la llegeix ha de saber en quin està i poder-lo
canviar**: un control visible amb tres estats, *sistema*, *clar* i *fosc*.
«Sistema» no és el mateix que «clar» —pot canviar sol al vespre—, i per això
s'ha d'anomenar a part i indicar a què resol ara mateix.

Defineix la paleta clara al `:root` pelat, i redefineix **només els tokens** dins
de `@media (prefers-color-scheme: dark)` amb el guard
`:root:not([data-theme="light"])`, i un altre cop a `:root[data-theme="dark"]`.
Cap color pot tenir la seva única definició dins d'un bloc de mode. I el vermell
s'hi ha d'aclarir a `#FF3B41`, com diu el punt 1.

> **No ho confonguis amb «el commutador» de la portada**, que sí que existeix i
> no té res a veure amb el color: tria entre dues maquetacions, *Light* (les
> franges apilades, per defecte per sota de 900 px) i *Extensa* (la portada
> llarga, per defecte a escriptori). Totes dues són clares.

---

## 8. Trampes d'aquest repositori

- **`scripts/build-pages.py` genera** blog, campus, 3x3, premsa i patrocinadors.
  Edita el generador, no la sortida. Ara bé, **només la part de `/blog/` està al
  dia** (agost 2026): aquella es pot regenerar sense por. La resta va endarrerida
  i executar-lo sencer, avui, esborra coses reals:
  - a `/patrocinadors/`, l'apartat sencer de posicionament competitiu;
  - a `/partits/calendaris/`, la instantània SEO i els botons de subscripció `.ics`;
  - a `/campus/` i `/premsa/`, paraules clau i noms alternatius d'SEO.

  El procediment segur: executa'l, mira el **`git diff` sencer** i restaura amb
  `git checkout --` tot el que no volguessis tocar. Si el que fas afecta només el
  blog, restaura la resta sempre.
- **El peu de pàgina va per dues velocitats.** El generador ja emet els enllaços
  de Protecció del Menor i Bàsquet femení, però `/campus/`, `/premsa/`, `/3x3/`,
  `partits/calendaris/` i les fitxes de partners encara tenen a disc el peu antic
  de 17 enllaços. S'igualarà el dia que es puguin regenerar sense pèrdues.
- **`.github/scripts/generate-team-pages.py`** genera `partits/equips/`.
- **`.github/scripts/generate-seo-snapshot.py`** només reescriu entre els
  marcadors `SEO-SNAPSHOT`, `SEO-EVENTS` i `SEO-EQUIPS`. Fora d'aquí és segur.
- **`partits/data.json`** el refresca un robot diari. Els canvis manuals hi duren poc.

---

## 9. Trampes de CSS que ja ens han mossegat

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
- **Marges automàtics dins d'una graella**: un fill de `grid` amb
  `margin-inline: auto` i sense `width` s'encongeix fins al contingut. Si el
  contingut és una imatge en `position: absolute`, el marc queda a **zero** i no
  se'n veu res. Posa-hi `width: 100%` al costat del `max-width`.
- **Especificitat dins de `.prose`**: `.prose p` (0,1,1) guanya a una classe sola
  (0,1,0). Qualsevol `<p>` d'un component que visqui dins d'un article s'ha
  d'escriure `.chart p.la-classe`, si no s'hi perden la mida i el color.

---

## 10. Abans de publicar

1. Els colors surten de la taula del punt 1, amb els noms del joc que toca?
2. La display és la que li pertoca a aquella pàgina —Jost o Anton— i no n'hi ha
   dues de barrejades?
3. Cap cara tallada i cap foto ampliada? Res de `--muted` en text de llegir?
4. Res amb data passada, `og-image.jpg` inclosa?
5. Les etiquetes fan servir el vocabulari del punt 6?
6. Si hi ha gràfics: són HTML i CSS, i cap dada es distingeix només pel color?
7. Si has tocat una pàgina generada, has editat el generador **i** has mirat el
   `git diff` sencer abans de desar?
8. Si la pàgina té versió en castellà o en anglès, l'has tocada també?
9. Sense desbordament horitzontal a 390 px, i amb focus visible al teclat?

Val la pena obrir-ho de debò abans de donar-ho per fet. Amb Chromium ja
instal·lat, `python3 -m http.server` i Playwright n'hi ha prou per mirar una
pàgina a 1280 i a 390 px i comprovar d'una tirada que no desborda, que no hi ha
cap imatge trencada i que cap no es mostra més gran del que és.

---

## 11. Per què de vegades el web no es desplega

Quan es pugen fotos des de `/fotos/admin.html`, cada foto és **un commit**. Una
tanda de 200 fotos són 200 commits en pocs minuts.

El `[skip ci]` del missatge atura els workflows del repositori, però **no atura
el build de GitHub Pages**, que és un workflow gestionat per GitHub. Resultat:
cada commit engega un build que cancel·la l'anterior, i **mentre dura la pujada
no es publica res**. Ni les fotos, ni cap altre canvi que hi hagi pendent.

No està trencat: està afamat. Es desbloqueja sol quan para la pujada.

Si has fusionat alguna cosa i no surt, mira-ho abans de tocar res:

```
git log origin/main --since="15 minutes ago" --oneline | wc -l
```

Si el número és alt, només cal esperar. La solució de fons és que les fotos
deixin de viure al repositori: llavors pujar-ne no genera cap commit ni cap
build.
