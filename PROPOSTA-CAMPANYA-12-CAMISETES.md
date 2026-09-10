# 12 CAMISETES · proposta de campanya web

**Setembre 2026 · les nascudes el 2018**
Proposta de l'àrea de màrqueting. Es construeix sobre el que ja hi ha al web
(`/#prova-2018`, `/escoleta/#noies-2018`, l'article del blog i la newsletter).

---

## 1. El problema, dit clar

El club no té un problema d'abast: **~439.000 visualitzacions al mes** a
Instagram. Té un problema de **conversió**: de tota aquella gent, gairebé ningú
fa el pas següent. Una crida com «busquem les del 2018» publicada com un cartell
més es perd entre la resta de contingut i no deixa cap rastre mesurable.

I té un problema de **fondària**: un any de naixement curt de jugadores
arrossega el problema deu temporades. Això no es resol amb un post: es resol
omplint un grup concret abans d'una data concreta.

## 2. La idea

**Un mur de 12 camisetes al web que s'omple en directe.**

A la portada (i a `/escoleta/`) hi ha dotze samarretes numerades del club,
totes apagades. **Cada reserva de la prova n'encén una.** El comptador és
públic: «7 de 12». Quan s'omple, el mur passa a ser la foto del grup del 2018.

Tres coses que això fa i un cartell no fa:

| | Cartell | Mur de 12 |
|---|---|---|
| **Prova social** | Ningú sap si algú s'hi ha apuntat | Es veu que set famílies ja hi són |
| **Urgència** | «Setembre» | «Queden 5 camisetes i falten 4 dies» |
| **Motiu per tornar-hi** | Cap | El número canvia cada dia |

I una quarta, la important: **dona a Instagram una notícia diària sense produir
contingut nou**. Una story amb el número i prou. El contingut car (reels) es
reserva per als tres o quatre moments que ho mereixen.

## 3. Com es viu, dia a dia

| Dia | Web | Instagram |
|---|---|---|
| D-9 | El mur s'obre amb 0 de 12 | Reel ja publicat, amb l'enllaç a la bio |
| D-7 | | Reel «el primer bot»: com és una sessió de l'Escoleta |
| D-6 a D-1 | El número puja sol | Story diària amb el comptador. Sense disseny nou |
| D-3 | | Vídeo de 20 s d'en Julio a càmera: qui hi entrena i per què |
| D-1 | Compte enrere a hores | «Demà. Queden N» |
| **D · 19 set** | El mur es tanca | Stories en directe des de la pista |
| D+1 | El mur passa a foto de grup | Reel del dia: cares, no gràfics |

## 4. La palanca que multiplica: «porta una amiga»

Al formulari hi ha una casella: **«ve amb una amiga»**. Si s'hi marca, s'encenen
dues camisetes de cop i el web ho diu («2 de cop, gràcies Ana!»).

És la palanca més barata que té el club: una nena de vuit anys no decideix
provar un esport llegint un web, ho decideix perquè hi va la seva amiga. Costa
una línia de codi i canvia la mida del grup.

## 5. Què no farem

- **Cap cara ni cap nom de menor al mur.** Les camisetes porten número i, com a
  molt, la inicial. La foto de grup del D+1 surt amb els permisos de sempre.
- **Cap comptador fals.** Si hi ha tres reserves, el mur en diu tres. Un
  comptador inflat es nota i és exactament el contrari de la confiança que ven
  un club de barri.
- **Cap compte enrere que caduqui malament.** El 20 de setembre el mur ja no és
  una crida: és un arxiu. Ho fa sol.

## 6. Què costa fer-ho

Tot al repositori que ja tenim. No cal cap servei nou ni cap plataforma de pagament.

| Peça | On | Feina |
|---|---|---|
| El mur i el comptador | `index.html` (ca/es/en) + CSS del bloc `#prova-2018` | ~3 h |
| Número en directe | Apps Script del formulari: retorna `{reservades: N}`; el web el llegeix | ~1 h |
| Casella «porta una amiga» | `js/reserva-prova.js` i el formulari | ~20 min |
| Compte enrere | Un `<time>` i quatre línies de JS | ~20 min |
| Imatge per compartir per estat | `generate-og-image.py`, un paràmetre nou | ~1 h |
| Mur → foto de grup | Canvi d'una variable el D+1 | 5 min |

**Mig dia de feina.** Zero euros de mitjans pagats.

## 7. Com sabrem si ha funcionat

No amb visualitzacions. Amb això:

1. **Camisetes enceses el 19 de setembre.** Objectiu: 12. Mínim digne: 8.
2. **Quantes segueixen entrenant el 15 d'octubre.** És l'única xifra que importa
   de veritat: una prova no és una jugadora.
3. **% d'abast a no-seguidors** dels reels de la campanya, i **seguidors nous**.
4. **Del web**: sessions a `/#prova-2018`, formularis començats i formularis
   enviats. La diferència entre les dues últimes diu si el formulari fa nosa.

## 8. I després: «el mur dels anys»

Si funciona, **no és una campanya: és un sistema**. Cada temporada hi ha un o
dos anys de naixement que van justos, i cada un pot tenir el seu mur, amb la
seva data i el seu grup. El club deixa de demanar jugadores en general i comença
a omplir buits concrets, a la vista de tothom.

Això és el que cap club de barri de Barcelona fa avui.

---

*Per aprovar: la Junta només ha de dir sí al mur públic amb número real. La
resta ja està escrit i construït a mitges.*
