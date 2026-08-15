---
name: web-cbgb
description: Sistema de disseny de les webs del CB Grup Barna (cbgrupbarna.info i satèl·lits). Carrega-la SEMPRE abans de tocar HTML, CSS o qualsevol peça visual del club: colors, tipografia, fotografia, vocabulari, modes clar i fosc, i les trampes tècniques del repositori. Inclou el vermell oficial mostrejat de l'escut i per què no és el mateix que el de vídeo.
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

Les fotos ja retallades de `img/` fan entre 360 i 550 px d'ample: serveixen per a
marcs petits i prou. **Els originals grans sí que hi són**, a `fotos/uploads/`:

| Àlbum | Què hi ha | Mida |
|---|---|---|
| `summer-camp-2526-…` | Campus: entrenaments, tir, grups, entrenadors | fins a 3648 × 5472 |
| `fotos-equips-temporada-25-26-records` | Foto oficial de cada equip, Escola inclosa | 1200 × 900 |
| `cistella-petita-2a-edicio-2026` | Dia de la Cistella Petita | petites, de mòbil |

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

## 3b. Gràfics i dades

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
- **Marges automàtics dins d'una graella**: un fill de `grid` amb
  `margin-inline: auto` i sense `width` s'encongeix fins al contingut. Si el
  contingut és una imatge en `position: absolute`, el marc queda a **zero** i no
  se'n veu res. Posa-hi `width: 100%` al costat del `max-width`.
- **Especificitat dins de `.prose`**: `.prose p` (0,1,1) guanya a una classe sola
  (0,1,0). Qualsevol `<p>` d'un component que visqui dins d'un article s'ha
  d'escriure `.chart p.la-classe`, si no s'hi perden la mida i el color.

## 9. Abans de publicar

1. Els colors surten de la taula del punt 1?
2. Cap cara tallada i cap foto ampliada?
3. Res amb data passada, `og-image.jpg` inclosa?
4. Les etiquetes fan servir el vocabulari del punt 5?
5. Funciona en clar i en fosc, i es veu en quin mode s'està?
6. Si has tocat una pàgina generada, has editat el generador?
7. Sense desbordament horitzontal, i amb focus visible al teclat?
8. Si hi ha gràfics: cap dada es distingeix només pel color?
9. Si hi ha versió en castellà o en anglès de la pàgina, l'has tocada també?
