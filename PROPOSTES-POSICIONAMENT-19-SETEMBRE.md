# Propostes perquè el 19 de setembre es posicioni a Google

Document de treball de màrqueting (no és una pàgina publicada). Continua
`POSICIONAMENT-PORTES-OBERTES-SEO.md`, que cobria el que es podia arreglar dins
del web. Això és el que hi falta, ordenat **per impacte real**, no per esforç.

*Escrit l'11/09/2026, a vuit dies de la jornada. Tot el que s'hi afirma està
comprovat aquest mateix dia; cada punt diu com.*

---

## El titular

La feina d'ahir (Event, landing, GEO) era necessària i està feta. Però mirant
què passa **fora** del repositori hi ha un problema que pesa més que tot el
SEO de la pàgina junt:

> **El club té tres adreces, dos telèfons i tres correus diferents circulant
> per Internet, i una segona web sencera que encara respon.** Mentre això duri,
> Google no sap quina és l'entitat «CB Grup Barna», i una entitat borrosa no
> guanya cerques locals ni surt al mapa.

No és una hipòtesi. És el que Google i les IA responen avui.

---

## P0 · Les tres coses que decideixen si el 19 es posiciona

### P0.1 — `cbgrupbarna.com` encara respon 200. La redirecció mai s'ha fet.

**Comprovat l'11/09/2026:** `curl -I https://cbgrupbarna.com/` torna **HTTP
200**, no un 301. La web antiga de WordPress **segueix publicada i servint-se
sencera**, amb:

| | Web antiga (`.com`, viva avui) | Web bona (`.info`) |
|---|---|---|
| Adreça | C/ Llacuna 170, Parc del Clot 08018 | Carrer de la Llacuna, 170-172, 08018 |
| Telèfon | **688 26 52 31** | **698 425 153** |
| Correu | **cbgrupbarna@gmail.com** | **marqueting@cbgrupbarna.info** |
| Temporada | **2025-26** | 2026-27 |
| Portes obertes del 19 de setembre | **no se n'hi diu ni una paraula** | tota la campanya |

A `MIGRACIO-WEB-ANTIGA.md`, punt 7, hi consta: *«Confirmat per l'Ana
(23/08/2026): `cbgrupbarna.com` es queda com a redirecció cap a
`cbgrupbarna.info`»*, i que la 301 «és una configuració de DNS/allotjament del
domini `.com`, fora d'aquest repositori». **Fa dinou dies d'això i la
redirecció no s'ha arribat a configurar.** Tota la part que era feina del
repositori sí que es va fer; la que era del panell del domini, no.

**Per què és el punt número 1.** Dos llocs vius amb el mateix contingut i el
mateix nom es reparteixen l'autoritat: els enllaços que algú faci cap al `.com`
no compten per al `.info`, i Google ha de triar quin ensenya. Ara mateix, per a
una família que arribi al `.com`, **la jornada del 19 de setembre no existeix**
i el telèfon que hi troba no és el que contesta.

**Què cal fer:** al panell del registrador o de l'allotjament del `.com`,
**301 permanent de `cbgrupbarna.com/*` cap a `cbgrupbarna.info/*`**, incloent-hi
`www`. No és una feina de codi i no es pot fer des d'aquí. És, de llarg, la
millor hora de feina que es pot invertir aquesta setmana.

**Com comprovar que ha funcionat:** `curl -I https://cbgrupbarna.com/` ha de
tornar `301` i un `Location:` cap a `cbgrupbarna.info`.

---

### P0.2 — La guia oficial de l'Ajuntament dona una adreça que no és la nostra

**Comprovat l'11/09/2026**, cercant el club a Google: la fitxa de
**`guia.barcelona.cat`** —el directori d'activitats de l'Ajuntament de
Barcelona, un domini institucional amb molta autoritat— publica el club amb:

- **Adreça: Plaça Canonge Rodó, 2 — 08026.** No és La Nau del Clot, i ni tan
  sols és el mateix codi postal.
- **Web: `cbgrupbarna.com`** (la vella).
- **Correu: `coordinaciocbgrupbarna@gmail.com`** (un tercer correu).
- **Escoleta: «de 4 a 7 anys».** El web diu de 4 a 8.

O sigui que la font institucional que Google més es creu del barri **ens
contradiu en els quatre camps alhora**. I no és teoria: en fer aquesta
comprovació, el resum automàtic del cercador va acabar dient que per saber-ne
més calia anar a `cbgrupbarna.com` i escriure a aquell gmail. Això és
exactament el que passarà a una família que pregunti a una IA.

**Què cal fer:** demanar la correcció de la fitxa a `guia.barcelona.cat` (i, ja
que hi som, mirar la fitxa del Districte de Sant Martí). Adreça, web, correu i
edats **exactament com al web**: *Carrer de la Llacuna, 170-172, 08018
Barcelona · cbgrupbarna.info · marqueting@cbgrupbarna.info · 4 a 8 anys*.

**Per què val la pena aquesta setmana:** una fitxa d'Ajuntament corregida és un
senyal de confirmació d'entitat molt fort, i és gratis.

---

### P0.3 — Fitxa de Google: la publicació d'esdeveniment

Ja era a la llista d'ahir i segueix sent el camí més curt perquè la data surti
al mapa i al panell de la dreta. **Però ara té un requisit previ**: si l'adreça
de la fitxa de Google no coincideix amb la del web —i acabem de veure que hi ha
tres adreces circulant—, la publicació no arreglarà res.

**L'ordre correcte és:** (1) comprovar l'adreça i el telèfon de la fitxa de
Google, (2) corregir-los si cal, (3) **després** publicar l'esdeveniment amb
data, hora i enllaç a `/portes-obertes/`.

---

## P1 · El que encara es pot guanyar dins del web

### P1.4 — «Portes obertes», en català i a Barcelona, vol dir *escola*

**Comprovat l'11/09/2026.** Buscant «portes obertes escoleta bàsquet Barcelona
setembre 2026», el que surt a dalt és: `edubcn.cat` («Jornades de portes
obertes als centres»), Institut Pedralbes, escoles de l'`xtec`, la Penya… Els
clubs de bàsquet que hi apareixen són de **Tarragona** (TGN Bàsquet), no de
Barcelona.

La conclusió és incòmoda però útil: **«portes obertes» a Barcelona és un terme
del sistema educatiu**, i competir-hi de cara és competir contra
l'Ajuntament, la Generalitat i tots els instituts de la ciutat alhora. No es
guanya en vuit dies ni en vuit mesos.

**La proposta no és rendir-se, és canviar de porta.** Les consultes que sí que
es poden guanyar, perquè gairebé ningú les treballa:

- «**provar un entrenament de bàsquet Barcelona**» — intenció idèntica, zero
  competència institucional.
- «**bàsquet per a nenes Barcelona**», «**equip de bàsquet de nenes**» — la
  landing nova ja hi apunta, i el buit és real.
- «**extraescolar de bàsquet Clot / Sant Martí / Camp de l'Arpa**» — geogràfic,
  poc volum, conversió altíssima.
- «**on pot jugar a bàsquet una nena de 8 anys**» — cua llarga, és una pregunta,
  i és or per a IA.

*Feina de repositori, la puc fer jo:* reequilibrar títols, descripcions i
encapçalaments cap a aquest vocabulari, sense perdre «portes obertes», que
segueix sent la marca de la campanya i la paraula que fan servir les famílies
que ja ens coneixen.

---

### P1.5 — Els títols fan 82 caràcters i Google en talla cap a 60

**Mesurat:** el `<title>` de `/portes-obertes/` fa **82 caràcters** i la
`meta description`, **235**. Google talla el títol cap als 60 i la descripció
cap als 160. La data sobreviu al tall per poc, però el nom del club no, i mitja
descripció no s'arriba a llegir mai.

*Feina de repositori, la puc fer jo:* escurçar-los als tres idiomes mantenint
la data al davant. Per exemple: «Portes obertes 19 de setembre · bàsquet al
Clot | Barna».

---

### P1.6 — La portada, que és la pàgina forta, no diu la data i no porta l'Event

**Comprovat:** `index.html` enllaça `/portes-obertes/` **una sola vegada**, i
la franja diu *«Tot el setembre. Vine a provar un entrenament»* — **sense la
data**. A més, la portada **no porta cap `Event`** al seu JSON-LD.

La portada és la pàgina amb més autoritat del domini i la que Google rastreja
més sovint. És el millor lloc per dir «dissabte 19».

*Feina de repositori, la puc fer jo:* posar la data a la franja de la portada
als tres idiomes i afegir-hi l'`Event` del 19 referenciant
`/portes-obertes/#event-19`, perquè el senyal surti també de la pàgina forta.

---

## P2 · Amplificació, si queda temps

### P2.7 — Que ho publiquin altres, no només nosaltres
Un esdeveniment es posiciona molt més de pressa si el declaren **tercers amb
autoritat**. Gratuïts i realistes en vuit dies: l'**agenda del Districte de
Sant Martí**, l'**agenda de `guia.barcelona.cat`** (el mateix lloc del P0.2, un
cop corregida la fitxa), el **web de la FCBQ** i els **canals de les AFA** de
les escoles del barri. Cada un és un enllaç i una confirmació de la data.

### P2.8 — IndexNow i Search Console, el mateix dia de publicar
El repositori ja porta `scripts/indexnow.py` i la clau verificada a l'arrel.
Google no fa servir IndexNow, però **Bing sí, i el que indexa Bing és el que
acaben citant ChatGPT i Copilot**. A Google, inspecció d'URL a mà a Search
Console, una per una: són sis pàgines i a vuit dies val la pena.

### P2.9 — Ressenyes: el senyal local que no caduca
El club ja té `/opina/`. Les ressenyes de Google són un dels factors del paquet
local, i una tanda de famílies actuals aquesta setmana ajuda la fitxa a
sortir al mapa per «bàsquet nens Clot» molt més enllà del 19.

---

## El que NO recomano, i per què

- **No comprar anuncis per a «portes obertes».** Competiries amb escoles i
  instituts pel mateix terme, car i mal orientat. Si es vol invertir, a
  Instagram i amb el públic per barri, que és on el club ja funciona.
- **No fer una pàgina nova per a cada consulta** de la llista del P1.4. La
  regla del club és una intenció, una pàgina; ja tenim les dues que calen.
- **No esperar posicions a Google el 19.** Vuit dies no hi arriben, i qui digui
  el contrari t'està venent alguna cosa. El que sí pot passar abans del 19 és
  que l'`Event` entri als resultats d'esdeveniments, que la fitxa de Google
  mostri la data i que les IA ja tinguin què citar.

---

## Ordre de feina suggerit, si només hi ha una tarda

1. **301 del `.com`** (P0.1) — panell del domini. La més important, i no és codi.
2. **Adreça de la fitxa de Google** (P0.3) i **publicació de l'esdeveniment**.
3. **Correcció de la fitxa de `guia.barcelona.cat`** (P0.2) — un correu.
4. Em dius que sí i faig P1.5 i P1.6 (títols i portada) en una estona.
5. IndexNow i Search Console el dia que es publiqui.

---

## Com sabrem si ha funcionat

- `curl -I https://cbgrupbarna.com/` torna **301**. Binari: o hi és o no hi és.
- Cercar «CB Grup Barna» i que **l'adreça i el telèfon siguin els mateixos** a
  la fitxa de Google, a `guia.barcelona.cat` i al web.
- A Search Console, consultes noves amb «nenes», «niñas», «2018» o «19 de
  setembre»: avui són zero.
- Preguntar a ChatGPT, Perplexity i l'AI Mode de Google, el 18 i el 25: «on pot
  jugar a bàsquet una nena de 8 anys al Clot?». Si contesten amb
  `cbgrupbarna.info` i el telèfon bo, la cadena sencera funciona.
