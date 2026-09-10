# EL COMPTADOR DEL SETEMBRE · campanya web

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

## 2. La idea · JA PUBLICADA

**Un comptador a la portada, dins del bloc de la prova del 19 de setembre.**

Tres xifres i una barra: **els dies que falten** (els compta el navegador sol),
**les places lliures del grup del 2018** —el grup surt amb 5 i ara en queden
3— i el **90% de les 50 places** de portes obertes del setembre. Quan arriba a zero s'atura sol, i el 20 de setembre el
bloc passa a ser arxiu.

Tres coses que això fa i un cartell no fa:

| | Cartell | Comptador |
|---|---|---|
| **Prova social** | Ningú sap si algú s'hi ha apuntat | Es veu que 45 famílies ja hi són |
| **Urgència** | «Setembre» | «Queden 3 places i 9 dies» |
| **Motiu per tornar-hi** | Cap | Els dies baixen sols cada matinada |

I una quarta, la important: **dona a Instagram una notícia diària sense produir
contingut nou**. Una story amb el número i prou. El contingut car (reels) es
reserva per als tres o quatre moments que ho mereixen.

## 3. Com es viu, dia a dia

| Dia | Web | Instagram |
|---|---|---|
| D-9 | El comptador s'obre: 9 dies · 3 places · 90% | Reel ja publicat, amb l'enllaç a la bio |
| D-7 | | Reel «el primer bot»: com és una sessió de l'Escoleta |
| D-6 a D-1 | Els dies baixen sols | Story diària amb el comptador. Sense disseny nou |
| D-3 | | Vídeo de 20 s d'en Julio a càmera: qui hi entrena i per què |
| D-1 | Compte enrere a hores | «Demà. Queden N» |
| **D · 19 set** | El comptador arriba a zero | Stories en directe des de la pista |
| D+1 | El bloc passa a foto de grup | Reel del dia: cares, no gràfics |

## 4. La palanca que multiplica: «porta una amiga»

Al formulari hi ha una casella: **«ve amb una amiga»**. Si s'hi marca, s'encenen
dues camisetes de cop i el web ho diu («2 de cop, gràcies Ana!»).

És la palanca més barata que té el club: una nena de vuit anys no decideix
provar un esport llegint un web, ho decideix perquè hi va la seva amiga. Costa
una línia de codi i canvia la mida del grup.

## 5. Què no farem

- **Cap cara ni cap nom de menor al comptador.** Només xifres. La foto de grup
  del D+1 surt amb els permisos de sempre.
- **Cap número inventat.** Els 45 surten del full de reserves i s'hi
  actualitzen. Un comptador inflat es nota i és exactament el contrari de la
  confiança que ven un club de barri.
- **Cap compte enrere que caduqui malament.** Quan arriba a zero s'atura sol; el
  20 de setembre el bloc ja no és una crida, és un arxiu.

## 6. Què costa fer-ho

Tot al repositori que ja tenim. No cal cap servei nou ni cap plataforma de pagament.

| Peça | On | Feina |
|---|---|---|
| El comptador a les tres portades | `index.html` (ca/es/en) + CSS del bloc `#prova-2018` | **fet** |
| Número en directe | Apps Script del formulari: retorna `{apuntats: N}`; el web el llegeix. Ara els 45 es canvien a mà als `data-` del bloc | ~1 h · **pendent** |
| Casella «porta una amiga» | `js/reserva-prova.js` i el formulari | ~20 min |
| Compte enrere | Calculat des de `data-fins` | **fet** |
| Imatge per compartir per estat | `generate-og-image.py`, un paràmetre nou | ~1 h |
| Comptador → foto de grup | Canvi d'una variable el D+1 | 5 min |

**Queda una tarda.** Zero euros de mitjans pagats.

## 7. Com sabrem si ha funcionat

No amb visualitzacions. Amb això:

1. **Places del 2018 cobertes el 19 de setembre.** Objectiu: les 5. Avui en
   queden 3. I, de fons, les 50 places de setembre: avui 45.
2. **Quantes segueixen entrenant el 15 d'octubre.** És l'única xifra que importa
   de veritat: una prova no és una jugadora.
3. **% d'abast a no-seguidors** dels reels de la campanya, i **seguidors nous**.
4. **Del web**: sessions a `/#prova-2018`, formularis començats i formularis
   enviats. La diferència entre les dues últimes diu si el formulari fa nosa.

## 8. I després: «el comptador de cada any»

Si funciona, **no és una campanya: és un sistema**. Cada temporada hi ha un o
dos anys de naixement que van justos, i cada un pot tenir el seu comptador, amb
la seva data i les seves places. El club deixa de demanar jugadores en general i comença
a omplir buits concrets, a la vista de tothom.

Això és el que cap club de barri de Barcelona fa avui.

---

*Estat: el comptador ja és a la portada (9 dies · 3 places lliures del 2018 · 90%). L'única
cosa pendent és que els 45 surtin sols del full de reserves en comptes de
canviar-se a mà.*
