---
name: web-cbgb
description: Sistema de disseny de les webs del CB Grup Barna (cbgrupbarna.info i satèl·lits). Carrega-la SEMPRE abans de tocar HTML, CSS o qualsevol peça visual del club: colors, tipografia, mida de lletra i de dit, fotografia, gràfics i dades, vocabulari, modes de color i les trampes tècniques del repositori. Diu quin dels tres vermells toca segons el fons que hi ha a sota i per què el de vídeo no val per a web; per què la display és sempre l'Anton i el text sempre la Inter, servides des del mateix domini; que cap text baixa d'11 px i que el que es prem fa 44, amb l'excepció dels enllaços enmig d'una frase; que /presentacions/ té mode fosc propi encara que la resta del lloc no en tingui; que mig lloc porta el CSS compartit copiat a dins, o sigui que arreglar css/barna.css només arriba a la meitat; on són els originals de foto i com passar-los pel script perquè cap surti ampliada; i quines pàgines generades encara no es poden regenerar sense perdre-hi contingut.
---

# Sistema de disseny · web CB Grup Barna

Val per a `cbgrupbarna.info` i per a tot el que en pengi. Si una peça respecta
aquestes regles, es reconeix com del club sense veure l'escut.

> ## La guia principal és «El Sistema Barna»
>
> **https://claude.ai/code/artifact/c22e9418-788b-43af-94c6-de7ab81b7f27**
>
> Del 30/08/2026. És la guia visual **definitiva** del lloc, i la que mana
> quan hi hagi dubte. Surt de les quatre portades i recull el que segueix
> viu dels tres documents anteriors —«L'estètica definitiva», «Franges i
> Extensa» i «Web + Instagram: dues propostes»—, que queden com a història.
>
> Aquest fitxer i aquella guia han de dir el mateix: **si en canvies un,
> canvia l'altre.** Aquí hi ha el detall d'enginyeria (generadors, trampes
> del repositori, circuit d'i18n); allà hi ha el sistema visual amb els
> contrastos mesurats per la pàgina mateixa i el destí decidit de cada
> portada.
>
> **El destí de cada portada** (decisió de l'Ana, 30/08/2026):
>
> | | Proposta | Va a | Estat |
> |---|---|---|---|
> | A | L'Afinat | La portada, `cbgrupbarna.info` | **Publicada** (v1.4.0) |
> | B | Dia de partit | **Tot el calendari**: `/partits/`, `/partits/calendaris/` i les fitxes de `/partits/equips/`, als tres idiomes | **Publicada** (30/08) · les fitxes d'equip esperen el generador |
> | C | La Jugada | L'Escoleta, `/escoleta/`, amb submenú «Història de l'escola» | **Publicada** (30/08) |
> | D | L'Edició | **La newsletter setmanal** (Brevo) | **Publicada** (30/08): `/newsletter/` als tres idiomes + `docs/newsletter/plantilla.html` per a Brevo |
>
> Dues precisions de l'Ana del 30/08 que canvien el que s'havia apuntat abans:
> la **B no és només la portada del calendari**, és tot el calendari amb la
> mateixa estètica; i la **D no és `/premsa/`**, és la newsletter que arriba
> per correu — **setmanal** (rectificat el mateix dia: es va apuntar
> «mensual» per un lapsus i s'ha corregit a «setmanal», que és la decisió
> bona). Les fitxes de `/partits/equips/` les genera
> `.github/scripts/generate-team-pages.py`: allà es toca el generador, no la
> sortida.
>
> **Com s'han aplicat C i D** (30/08, per si s'han de tocar):
>
> - **C** és `css/jugada.css` + `js/jugada.js`, plantats a les tres pàgines
>   per `scripts/jugada-aplica.py`. El rellotge de possessió es reparteix
>   sol entre les seccions que porten `data-jugada`: afegir o treure una
>   secció NO obliga a recalcular els segons. S'enganxa sota la `.langbar`
>   amb l'alçada mesurada (`--jug-top`), no amb un número escrit.
>   El contingut de l'Escoleta no s'ha tocat: hi ha SEO que hi depèn.
> - **D** són els components `.ed-*` de `css/barna.css`, plantats per
>   `scripts/edicio-aplica.py`, i la plantilla de correu
>   `docs/newsletter/plantilla.html`. La plantilla NO fa servir Anton ni
>   Inter ni duotò: al correu no hi ha tipografies carregades ni
>   `mix-blend-mode`, i un efecte a mitges és pitjor que cap.
>
> Les maquetes navegables:
> https://claude.ai/code/artifact/a4a53f45-e2d3-4e9a-aadb-ee89be001087

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
| Hero de la portada | Mateixa foto que la portada del post fixat |
| Fitxa d'entrenador/a | Sèrie «La feina que no es veu» |

**Els quatre destacats del perfil són els quatre pilars de la web.** Si canvien
al perfil, canvien a la web.

### Una sola velocitat de lectura: franges

**Decisió tancada (27/08/2026, v2.0.0): la portada és NOMÉS la vista de
franges.** Hi va haver un temps amb dues vistes intercanviables —Franges
(per defecte) i Extensa (editorial, portada de diari amb `.masthead`,
paritat, lema i articles)— i un botó de commutador a la capçalera. El
pla per decidir-ho era mesurar amb GA4 quanta gent canviava de vista
(l'esdeveniment `canvi_vista`) abans de triar-ne una; els secrets de GA4
mai es van arribar a donar d'alta, així que aquesta dada no ha existit
mai. L'Ana ha decidit sense esperar-la: «Quiero esta portada no dos».
El commutador, l'extensa sencera i tot el JS que hi anava (`data-view`,
`sessionStorage`, `canvi_vista`) surten de les tres portades.

La portada obre com la guia visual: barra de novetats, menú, el hero curt
(etiqueta vermella, «Bàsquet al Clot. / Des de 1965.» amb la segona línia
en vermell i una sola frase) i les nou franges, tancades amb la barra
`#SOMCLOT`. **No hi ha bloc fosc de marca**: el `.masthead` que abans hi
havia amagat per a l'extensa ha sortit del marcatge de les tres llengües.

**Les classes de franges viuen a `css/barna.css`**: `.franges`, `.franja`,
`.franja--red`, `.franja--ink`. Les de l'antiga extensa (`.e-sech`,
`.e-feat`/`.e-art`, `.e-guides`, `.e-par`, `.e-lema`) **ja no les fa servir
la portada**, però es queden a `css/barna.css` perquè una pàgina interior
que enllaci el full (blog, premsa…) encara les té — no en refacis cap de
nova. Els títols de secció d'un article (`.prose h2`) porten el mateix
filet vermell, que és el gest que lliga una interior amb la portada.

L'estructura de les franges està calcada de la guia visual. **Si canvies l'ordre
o els textos d'una, canvia'ls a l'altra**: la portada i la guia han de dir el
mateix.

### Les quatre decisions de l'«Estètica definitiva», vigents

«L'estètica definitiva» (25/08/2026) va substituir «Franges i Extensa», i des
del 30/08/2026 totes dues queden sota «El Sistema Barna» (vegeu el bloc de
dalt), que és la guia principal. Aquestes quatre decisions **segueixen
vigents** i estan recollides allà; es deixen aquí perquè és on es va apuntar
com s'apliquen al codi:

1. **Sense crema enlloc** — totes les superfícies clares són blanc pur.
2. **Groc `#EEFF00` només a la lletra, mai al fons**, i només als dos punts
   d'entrada a la campanya d'Escoleta (el ticker i el seu CTA). Sobre tinta
   17,2:1; sobre blanc no s'hi pot escriure (1,1:1). El botó groc va sobre
   `--red-dark` perquè sobre el vermell de l'escut es queda en 4,44:1.
3. **Quatre vestits, una sola marca** — mateixos tokens a tot arreu.
4. **Botó ≡ amb el mapa complet a totes les capçaleres** — `js/mapa.js`,
   generat per `scripts/build-mapa.py` des de `i18n/routes.yml`.

La portada de franges és la maqueta del document: hero de dues columnes amb
la foto de l'Escoleta (filet vermell a sota), botons «Vine a provar» /
«Entrenaments» / «Descarrega info», i **cinc franges grans** (`.fr2`):
Escoleta · Els sèniors (tinta, foto alta) · Femení · Calendari (vermell) ·
El club, tancades amb la barra fosca #SomClot. Si canvies l'ordre o els
textos, canvia'ls també a la guia.

### Nota sobre les guies antigues

Hi ha una guia anterior —«Web + Instagram: dues propostes», agost 2026— que
proposava **Bebas Neue** i el vermell **`#E31E24`**, amb negre `#050505` i
JetBrains Mono per a dades. **Aquells valors no manen.** La decisió tancada és
Anton i `#E20613` (punts 1 i 2), perquè el vermell està mostrejat de l'escut i
`#E31E24` no arriba al contrast mínim sobre crema. La resta d'aquella guia —la
tesi, el diagnòstic i les dues propostes— sí que val, i és el que hi ha aquí
sobre.

El llinatge sencer, per si algú es troba un d'aquests documents i no sap si
encara mana. **Només l'últim mana**, i els altres tres es guarden com a
història:

| | Document | Què en queda |
|---|---|---|
| 1 | Web + Instagram: dues propostes | La tesi i el diagnòstic. **Els valors, no.** |
| 2 | Franges i Extensa | Els valors de color. La part de les dues vistes va caducar a la v2.0.0. |
| 3 | L'estètica definitiva (25/08) | Les quatre decisions, totes vigents. |
| 4 | **El Sistema Barna (30/08)** | **La guia principal.** Ho recull tot. |

> Mesurat per la pàgina de la guia: `#E31E24` sobre la crema d'abans dona
> 4,16:1 i no passa —aquell era el motiu de descartar-lo—; sobre el blanc
> d'avui dona 4,69:1 i sí que passaria. Segueix fora igualment, perquè el
> color de marca és el de l'escut i no una tria de gust.

---

## 1. Un sol vermell: el de l'escut

El vermell és el mateix a tot arreu, i des de l'agost del 2026 **els valors
també**: els de la guia «Franges i Extensa». Hi ha un sol joc de números, amb
dos jocs de **noms** que conviuen com a àlies dins de `css/barna.css`.

**Sistema principal** — `css/barna.css`, i la portada, que porta el CSS a dins
però amb els mateixos valors. Cobreix blog, campus, 3x3, premsa, patrocinadors,
femení, `/es/`, `/en/` i `partits/equips/`.

| Token | Valor | Ús |
|---|---|---|
| `--red` | `#E20613` | L'únic accent. Mostrejat de `logo.png` i `icon-512.png`. |
| `--red-dark` / `--red-ink` | `#A8040E` | Text vermell sobre fons clar i estats de passar-hi el ratolí. |
| `--ink` | `#10100E` | Tinta. |
| `--ink-2` | `#46433f` | El text corrent. |
| `--muted` | `#6B6560` | Etiquetes petites i text secundari. Passa AA. |
| `--line` | `rgba(16, 16, 14, 0.14)` | Filets. |
| `--paper` | `#ffffff` | Paper. |
| `--paper-2` / `--cream` / `--ground` | `#FFFFFF` | Blanc pur. Era la crema `#F4F1EC` fins al 25/08/2026: l'«Estètica definitiva» la retira («sense crema enlloc») i les bandes alternes se separen amb filet, no amb fons. |

**Els noms de `/partits/` són àlies del mateix joc**: `--cream`, `--red-ink`,
`--panel` i `--ground` estan declarats a `css/barna.css` amb aquests valors, de
manera que copiar codi d'una banda a l'altra ja no obliga a traduir res.
`scripts/aplica-estetica.py` és qui manté la resta del lloc en aquests valors:
tradueix els vermells, les tintes i les cremes que no hi són, i deixa dues
famílies de lletra. Passa-l'hi després de qualsevol pàgina nova
(`python3 scripts/aplica-estetica.py --dry-run` primer).

Contrast mesurat sobre blanc: `#E20613` dona 4,92:1 i `#A8040E`, 7,81:1 — tots
dos passen el mínim AA per a text. Blanc sobre `--red` també dona 4,92:1.

> **`--muted` ja arriba a AA.** El gris antic, `#8a8681`, es quedava en 3,62:1
> sobre blanc i 3,29:1 sobre crema. El d'ara, `#6B6560`, dona 5,74:1 sobre blanc
> i 5,25:1 sobre crema: passa als dos fons i ja s'hi pot posar text de llegir.

**No facis servir `#FD030C`**, que és el vermell de la cartela de vídeo de
`sistema-visual-cbgb`. Sobre blanc dona 4,04:1 i sobre crema 3,59:1, per sota
del mínim. Per a vídeo és correcte; per a web, no.

### Quin dels tres vermells, segons el fons

No és una tria de gust: el fons la decideix. És l'error de contrast que més
vegades ha sortit al lloc —la tanda del 30/08/2026 en va trobar **2.012
avisos**, i el vermell mal triat sobre fons fosc n'era la causa principal.

| Fons | Vermell | Contrast |
|---|---|---|
| Blanc o clar, **text gran** o filet | `--red` `#E20613` | 4,92:1 |
| Blanc o clar, **text per llegir** | `--red-dark` / `--red-ink` `#A8040E` | 7,81:1 |
| **Fosc** (tinta, negre) | `#FF3B41` | 5,81:1 sobre `#040404` |

Amb `#E20613` sobre un fons gairebé negre en surten **4,17:1**, per sota del
mínim. Els llocs on havia passat: la porta d'accés de `/premidonaesport/` (72
pàgines), `/admin/marca/`, el diàleg de `scripts/admin-gate.js` i
`/docs/welcome-pack/` —aquest últim, a sobre, encara feia servir `#E31E24`,
el vermell de la guia vella que la decisió del club va descartar
expressament.

I el revés també mossega: el diàleg d'accés va sobre **blanc**, i aclarir-hi
el vermell «perquè és un diàleg fosc» el deixava en 3,53:1. Mira el fons de
debò, no el que et sembla que hi ha.

### Un component que viatja ha de dir de quin color va

L'avís de portes obertes (`js/avis-portes-obertes.js`) s'injecta a pàgines que
no controla. El seu paràgraf no declarava color i comptava d'heretar el blanc
de la barra vermella. A `/presentacions/`, que defineix `p{color:var(--cos)}`,
la regla de la pàgina guanya per especificitat i el text quedava **gris damunt
del vermell, 2,52:1**.

**Cap peça que s'injecti amb JavaScript pot heretar el color, la mida ni la
família de la pàgina que la rep.** Ha de declarar-ho tot, i amb el selector
prou específic (`.cbgb-po p`, no `p`).


### El que no hi va
Groc, verd, blau i taronja **no són colors de marca**. Excepcions, i només
aquestes:
- **Semàntics de resultat**: `--win` i `--loss` a `/partits/`. Serveixen per dir
  si un partit s'ha guanyat o s'ha perdut, mai per decorar.
- **Marques d'altri**: Instagram, WhatsApp i TikTok porten el seu color.
- **La bandera de l'Orgull** a `/orgull/`. No s'hi toca.

---

## 2. Tipografia: una de display i una de text

Dues famílies, i prou. **Anton** per a display i **Inter** per a tota la resta.
No hi ha cap tercera: Jost, Bebas Neue, Outfit, Cormorant Garamond i Fraunces
han sortit del lloc.

> **Fins al 30/08/2026 això era una intenció, no un fet.** Les famílies
> retirades seguien demanades a vuit llocs, tots fora del camí que es mira
> quan es toca el disseny: `/admin/`, `/admin/marca/`, `/admin/token.html`,
> `/briefing/admin.html`, `/jugadors/admin.html`, `js/descarrega.js`,
> `scripts/admin-gate.js` i `premidonaesport/assets/js/auth.js`. Com que cap
> d'aquelles pàgines carregava la família, el navegador queia a la lletra del
> sistema i cada telèfon les ensenyava d'una manera. **`/admin/marca/` era, a
> més, l'única pàgina del lloc que demanava tipografies a
> `fonts.googleapis.com`** —justament la pàgina de la MARCA, i contra el
> criteri RGPD de dos paràgrafs més avall. Tot corregit; si tornes a veure
> «Bebas», «Outfit» o «Jost» en un diff, ve d'una d'aquestes peces.
>
> Comprovació d'una línia:
> ```bash
> grep -rn "Bebas\|Outfit\|Jost\|googleapis" --include=*.html --include=*.css --include=*.js . | grep -v tests/
> ```

- **Anton** (`--display`, amb `Haettenschweiler` i `Arial Narrow` de recanvi) va
  en caixa alta. És la de la portada, la de `css/barna.css` i la de les pàgines
  autònomes: `/escoleta/`, `/partits/`, `/briefing/`, `/jugadors/`, `/premsa/`,
  `/premidonaesport/`, `/presentacions/`… No té cursiva ni pes negreta: si en
  demanes, el navegador se les inventa i es nota.
- **Inter** per a text, dades i etiquetes. És variable: un sol fitxer per
  subconjunt cobreix del pes 100 al 900. Les etiquetes van en caixa alta amb
  interlletratge de `0.18em` a `0.28em`.

**Les dues s'allotgen al mateix domini**, a `/fonts/`, i es carreguen amb
`<link rel="stylesheet" href="/css/fonts.css">` (o via `css/barna.css`, que ja
porta l'Anton a dins). Cap pàgina demana res a `fonts.googleapis.com`: així no
es transfereixen IPs de les famílies a tercers, que és el criteri RGPD del club.
Si fas una pàgina nova, enllaça `/css/fonts.css` i prou.

Els `.ttf` de `.github/scripts/fonts/` (`anton.ttf`, `inter-*.ttf`) **no són per
al web**: els fan servir `generate-og-image.py` i `generate-calendaris.py` per
dibuixar imatges amb Pillow.

### El terra: res per sota d'11 px

**Cap text del lloc baixa d'11 px**, i el graó de sobre és 11,5. És una regla
d'aquest repositori, no un estàndard: la WCAG no fixa cap mida mínima.

Ve d'una tanda de proves del 30/08/2026 que va trobar **46.382 avisos de text
per sota d'11 px** a 501 pàgines, amb el més petit a **7,7 px** —en caixa alta
i amb `0,3em` d'interlletratge, que és el pitjor cas possible per llegir. Hi
havia titolets (`h3`), el peu legal i etiquetes de formulari a 8,5 px.

El sistema d'etiquetes petites del club **no canvia**: segueixen sent en caixa
alta, amb interlletratge, i el que les distingeix entre elles és el color i
l'interlletratge, no la mida. El que va canviar és el terra. Els cinc graons
de sota (8,5 · 9 · 9,5 · 10 · 10,5) es van repartir en dos:

| Abans | Ara |
|---|---|
| 8,5 px · 9 px | **11 px** |
| 9,5 px · 10 px · 10,5 px | **11,5 px** |

En `rem` amb l'arrel a 16 px, el terra és `.69rem`; en `clamp()`, **el mínim és
el que mana al mòbil** i és el que s'ha de mirar.

> **Trampa.** Pujar-ho a `css/barna.css` només arriba a mitja web: vegeu la
> trampa del CSS copiat, al punt 9.

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
| Dies de partit | **Calendari** — decisió de la direcció del club, agost del 2026, i **igual en castellà i en anglès**: «Calendario» i «Calendar». Abans era «Dies de partit»; ara aquest, i «Partits i resultats» i «Partits i events», són els prohibits. Als `<title>` i les descripcions s'hi pot deixar «dies de partit» com a terme de cerca, però l'etiqueta hi va davant. |
| — | **Calendari per equip** per a `/partits/calendaris/` · «Calendario por equipo» · «Team calendars» |
| Escoleta | Escoleta |
| El club | El club |

Els `<title>` i les descripcions sí que poden portar termes de cerca
(«dies de partit», «resultats»); les **etiquetes i els enllaços**, no. La
llista viva és `i18n/etiquetes.yml`, i `scripts/i18n-aplica-etiquetes.py`
l'aplica a disc: si canvies el vocabulari, canvia'l allà i executa'l, o el
lint te'l revertirà. Les **adreces no es toquen** —`/partits/` i
`/partits/calendaris/` es queden com són— perquè d'aquesta última en pengen
els `.ics` que les famílies ja tenen subscrits al mòbil.

---

## 6 bis. Els tres idiomes van junts, i ho comprova una màquina

**Un canvi de text es fa als tres idiomes alhora.** No és una bona pràctica:
és una comprovació que atura la fusió.

Cada traducció és un fitxer HTML independent —no hi ha framework d'i18n—, i
`i18n/routes.yml` és qui diu quines tres pàgines són la mateixa. Toca'n una i
has de tocar les tres; esborra'n una i has d'esborrar les tres.

| Quan | Què hi ha | Què fa |
|---|---|---|
| A la proposta de canvi | `.github/workflows/i18n-paritat.yml` | Compara què toca el canvi amb el trio de cada pàgina. Si en falta un idioma, **la marca en vermell** i escriu a la proposta quins fitxers falten. Quan es resol, esborra l'avís sol. |
| A cada push a `main` | `.github/workflows/i18n-tradueix.yml` | Torna a extreure el text de les pàgines tocades conservant el que no ha canviat, i manté **una sola incidència** amb la llista viva del que queda endarrerit. Es tanca sola quan es buida. |
| Sempre que vulguis | `python3 scripts/i18n-paritat.py --tot` | La mateixa foto, a mà i al moment. |
| A cada proposta, a part | `scripts/i18n-contingut.py` | **Obre** l'original i la traducció i els compara: seccions, llargada, paraules catalanes i `<title>`. La paritat mira fitxers i dates i no en veu cap; això va trobar `/3x3/` amb 6 de 12 seccions i 21 de 23 fitxes de partner amb 1 de 4. Avisa, no atura. Les excepcions, amb el motiu, a `i18n/excepcions-contingut.yml`. |

El circuit per posar una pàgina al dia:

```bash
python3 scripts/i18n-extreu.py <ruta-catalana> es en   # conserva el ja traduït
# omplir i18n/feina/{es,en}/<pàgina>.json
python3 scripts/i18n-munta.py <ruta-catalana> es
python3 scripts/i18n-munta.py <ruta-catalana> en
python3 scripts/i18n-hreflang.py && python3 scripts/build-sitemap.py
```

`i18n-extreu.py` busca cada tros pel text català, de manera que **només et
demana traduir el que ha canviat**: si has tocat un paràgraf, la resta de la
pàgina conserva la traducció que ja tenia.

**El català és l'original.** Si toques `/es/` o `/en/` directament, aquell text
no queda a cap fitxer de `i18n/feina/` i la propera vegada que es munti la
pàgina desapareixerà. El canvi de text es fa a la pàgina catalana i baixa cap
a les altres dues.

**Les dues excepcions**, i són diferents a propòsit:

| Cas | On es diu |
|---|---|
| Aquesta **pàgina** va per lliure sempre | `i18n/excepcions-paritat.yml`, amb la ruta catalana i el motiu |
| Aquest **canvi concret** hi va, un cop | Una línia a la descripció de la proposta: `i18n-nomes-un-idioma: <motiu>` |

La segona és per a arreglos d'una vegada —«el castellà deia `noindex` i el
català no, només cal tocar el castellà»—. Fer-ne una excepció permanent de
pàgina ompliria el fitxer de casos morts; així caduca sola amb la proposta.

Cap de les dues deixa passar res sense un motiu escrit, i és a propòsit: una
llista d'excepcions sense motius acaba sent la regla.

---

## 7. Modes clar i fosc

**Correcció del 30/08/2026.** Fins avui aquesta secció deia que no n'hi havia
cap i que cap fitxer del repositori tenia `data-theme`. **No era cert**, i qui
s'ho hagués cregut hauria pogut trencar divuit pàgines sense saber-ho:

- **La major part del lloc sí que és només clara**, i el fosc hi surt com a
  superfície puntual (`.foot`, `.franja--ink`). Aquí la regla es manté: no
  afegeixis mig mode fosc a una pàgina solta.
- **`/presentacions/` és una excepció que ja existia**: divuit pàgines (les
  sis catalanes i les seves traduccions) són **fosques de mena** i porten un
  commutador propi que les passa a clar, amb `:root[data-theme="light"]` i
  la tria desada a `localStorage`. Cap fitxer del lloc fa servir
  `prefers-color-scheme`.

Aquell commutador **no compleix el que demana la resta d'aquesta secció**, i es
deixa dit perquè es decideixi, no perquè s'imiti:

| | Què hauria de fer | Què fa |
|---|---|---|
| Estats | tres: sistema, clar, fosc | dos: fosc (per defecte) i clar |
| Punt de partida | el del dispositiu | sempre fosc, ignora el telèfon |
| Etiqueta | diu en quin estat s'és | ho diu, però estava en català a les pàgines en castellà i en anglès (corregit el 30/08) |

Que ignori el mode del telèfon és defensable en un micro-lloc de presentació,
que és una peça de marca amb un vestit triat; convertir-lo en el mode fosc del
sistema, no. **Si algun dia el mode fosc es fa de debò, es fa a
`css/barna.css` per a tot el lloc**, i llavors això és el que ha de complir.
La pàgina s'adapta al mode del dispositiu, però **qui la llegeix ha de saber
en quin està i poder-lo canviar**: un control visible amb tres estats,
*sistema*, *clar* i *fosc*. «Sistema» no és el mateix que «clar» —pot canviar
sol al vespre—, i per això s'ha d'anomenar a part i indicar a què resol ara
mateix.

Defineix la paleta clara al `:root` pelat, i redefineix **només els tokens** dins
de `@media (prefers-color-scheme: dark)` amb el guard
`:root:not([data-theme="light"])`, i un altre cop a `:root[data-theme="dark"]`.
Cap color pot tenir la seva única definició dins d'un bloc de mode. I el vermell
s'hi ha d'aclarir a `#FF3B41`, com diu el punt 1.

> No ho confonguis amb «el commutador» de la portada: existia, triava entre
> dues maquetacions (Franges i Extensa) i no tenia res a veure amb el color.
> Va desaparèixer el 27/08/2026 (v2.0.0, vegeu §0 bis): ara la portada només
> té la vista de franges.

---

## 7 bis. Mida de dit

**44 px d'alçada per a tot el que es prem.** El mínim de la WCAG 2.2 (criteri
2.5.8, nivell AA) és 24×24 px; 44 és la mida de dit que fa servir la resta del
sistema i el que hi ha d'haver per defecte. Entre els dos números, el criteri
és: **24 és el terra que no es pot baixar mai; 44 és el que s'ha de posar si
no costa res.**

I gairebé mai costa res en vertical. La fila de la capçalera ja fa 44 px:
posar-hi la barra d'idiomes, l'enllaç d'administració o el botó de cerca a
44 d'alçada **no mou res de lloc**. En horitzontal sí que costa, i per això la
barra d'idiomes es queda a 26 px d'ample: eixamplar-la a 34 es menjava 27 px
de la tira de navegació, que a 360 px ja només n'ensenya 110 de 278.

### L'excepció que cal respectar: els enllaços dins d'una frase

La WCAG 2.5.8 **excusa expressament els enllaços «inline»**: un enllaç enmig
d'un paràgraf no té mida pròpia —l'hi dona la línia de text— i no se n'hi pot
demanar. Forçar-los a 44 px trencaria la interlínia de tots els articles.

La distinció que val, i que la bateria de proves ja aplica:

| | Mida de dit |
|---|---|
| Enllaç enmig d'una frase (el pare té text al voltant) | **no**, es queda com va |
| Enllaç que ocupa el paràgraf sencer, o va sol dins d'un `<dd>`, un `<li>`, una targeta o el peu | **sí** |
| Molla de pa, menú, barra d'idiomes, botons, pins de mapa | **sí**, sempre |

Els llocs on això havia fallat, per si tornen a sortir: les molles de pa
(15 px), els enllaços del peu de les pàgines amb el peu copiat a dins (21 px),
el web/telèfon/correu de cada fitxa de partner (19 px), els pins del mapa de
partners (16×16) i els botons del consentiment de galetes, que es quedaven en
43,59 px per un `min-height:42px` en un bloc estret.

> **Un truc que serveix sovint.** Si créixer taparia el dibuix —els pins del
> mapa— no facis créixer el dibuix: fes créixer **la caixa que respon**. El
> pin es dibuixa de 16 px dins d'una caixa transparent de 44×44, i el mapa
> segueix llegible.

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
- **Mig lloc porta el CSS compartit copiat a dins.** És la trampa que més
  temps fa perdre, i no es veu mirant `css/barna.css`. La barra d'idiomes és
  a dins del `<style>` de **118 pàgines**; el peu, de **27**; la capçalera i
  la molla de pa de `/presentacions/`, de 18; i les tres portades no
  carreguen `css/barna.css` en absolut —porten el seu propi full sencer.
  Arreglar una cosa al full compartit i donar-la per feta deixa **la meitat
  del lloc igual**, i el resultat és pitjor que no tocar res: el que es prova
  funciona i el que no es prova, no.

  Abans de donar per bo un arreglo de CSS compartit, compta quantes còpies
  n'hi ha:
  ```bash
  grep -rl "\.lang-switch a" --include=*.html . | grep -v tests/ | wc -l
  ```
  I comprova'l en tres pàgines de famílies diferents: la portada,
  una interior que carregui `css/barna.css` (`/avis-legal/`) i una de
  `/presentacions/` o `/premidonaesport/`, que tenen full propi.
- **Un panell tancat amb `opacity:0` segueix a l'ordre de tabulació.** El xat
  de WhatsApp s'amagava així, i els seus sis controls es podien enfocar amb el
  teclat a **totes** les pàgines del lloc, just al començament i amb
  `aria-hidden="true"` a sobre —que damunt d'elements enfocables és una
  contradicció que els lectors de pantalla no saben resoldre. `visibility:
  hidden` els en treu i es pot animar igual (`transition: … , visibility .2s`).
  El mateix val per a `pointer-events:none`: amaga del dit, no del teclat.

---

## 10. Abans de publicar

1. Els colors surten de la taula del punt 1, amb els noms del joc que toca?
2. La display és l'Anton, sense cursiva, i la de text és la Inter, totes dues
   servides des de `/fonts/` i no des de Google?
3. Cap cara tallada i cap foto ampliada? Res de `--muted` en text de llegir?
4. Res amb data passada, `og-image.jpg` inclosa?
5. Les etiquetes fan servir el vocabulari del punt 6?
6. Si hi ha gràfics: són HTML i CSS, i cap dada es distingeix només pel color?
7. Si has tocat una pàgina generada, has editat el generador **i** has mirat el
   `git diff` sencer abans de desar?
8. Si la pàgina té versió en castellà o en anglès, l'has tocada també?
   Comprova-ho amb `python3 scripts/i18n-paritat.py --tot` (punt 6 bis); si no,
   t'ho aturarà la comprovació de la proposta de canvi.
9. Sense desbordament horitzontal a 390 px, i amb focus visible al teclat?
10. Cap text per sota d'11 px, i el que es prem a 44 px d'alçada (punts 2 i
    7 bis)? Els enllaços enmig d'una frase no compten.
11. El vermell que toca per al fons que hi ha a sota (punt 1)?
12. Si has tocat CSS compartit, l'has tocat també a les còpies que en porten
    les pàgines amb full propi (punt 9)?

Val la pena obrir-ho de debò abans de donar-ho per fet, i **no cal fer-ho a
mà**: el repositori porta la seva pròpia bateria de proves a `tests/`, que
serveix el lloc amb Chromium i el mira a quatre amplades de mòbil i tauleta.

```bash
node tests/audit-browser.mjs --viewports mobil,tauleta --pages 40   # una tanda curta
node tests/aggrega.mjs tests/out/chunks --out tests/out/browser.json
```

La tanda sencera (500 pàgines) no cap en una sola execució —el navegador es
queda sense memòria cap a la pàgina 250—, i per això s'hi passa per trossos
amb `--skip`; `tests/aggrega.mjs` els ajunta i en treu el resum per famílies
de problema. Els detalls, a `tests/README.md`.

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
