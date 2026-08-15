# Bústia única de formularis

**Un sol full de càlcul. Una pestanya per formulari. Cap altre destí.**

Tots els formularis de la web escriuen al mateix full, cadascun a la seva
pestanya, i cada enviament avisa per correu a **voluntarisgrupbarna@gmail.com**.

> Dins d'un full de càlcul, les divisions es diuen **pestanyes** (o fulls): són
> les etiquetes de sota de tot. Fan la mateixa feina que unes carpetes —cada
> formulari té la seva— però tot viu en **un únic fitxer**, que és el que
> permet buscar una persona a tot arreu i donar-la de baixa d'una sola vegada.
> Les carpetes de Google Drive contenen fitxers separats, i això és justament
> el que estem desfent.

Es fa una vegada i ja no s'hi torna. Uns quinze minuts.

---

## Què hi ha en aquesta carpeta

| Fitxer | Què és |
|---|---|
| `Codi.gs` | El programa que va a Google. Es copia i s'enganxa. |
| `README.md` | Això. |

I fora d'aquí, a `/scripts/formularis.js`, hi ha la peça de la web. **La URL del
desplegament s'escriu només allà**, en una línia. Cap pàgina la repeteix.

---

## Posar-ho en marxa

### 1 · Crear el full

Entra a [sheets.new](https://sheets.new) **amb el compte del club** (el mateix
que rebrà els avisos) i posa-li de nom `Contactes web · CB Grup Barna`.

No cal crear cap pestanya a mà: el programa les crea soles, amb capçalera i
tot, la primera vegada que arriba un formulari de cada tipus.

Copia l'**ID del full**: és el tros llarg de la URL, entre `/d/` i `/edit`.

```
https://docs.google.com/spreadsheets/d/AQUÍ_HI_HA_L_ID/edit
```

### 2 · Enganxar el programa

Al mateix full: menú **Extensions → Apps Script**.

Esborra el que hi hagi i enganxa-hi tot el contingut de `Codi.gs`. A dalt de
tot, omple:

```javascript
var FULL_ID = 'l_id_que_acabes_de_copiar';
var AVIS_A  = 'voluntarisgrupbarna@gmail.com';
```

Desa (icona del disquet).

### 3 · Provar-ho abans de tocar la web

Al selector de funcions de dalt, tria **`prova`** i clica **Executar**.

La primera vegada Google demanarà permisos: *Revisar permisos → tria el compte
→ Configuració avançada → Anar a (nom del projecte) → Permetre*. És normal:
Google avisa així de tots els programes que no ha revisat ell, i aquest és
vostre.

Si tot va bé: apareix una fila de prova a la pestanya **Informació** i arriba un
correu a voluntaris. Esborra la fila quan l'hagis vist.

**Si això no funciona, no continuïs**: el problema és aquí, no a la web.

### 4 · Publicar-lo

**Desplega → Desplegament nou → tipus: Aplicació web**, i:

| Camp | Valor |
|---|---|
| Descripció | `Bústia de formularis` |
| Executa com a | **Jo** (el compte del club) |
| Qui hi té accés | **Qualsevol** |

«Qualsevol» és imprescindible: qui omple el formulari a la web no té sessió de
Google iniciada. El programa només sap escriure files, no llegir res.

Copia la **URL de l'aplicació web**. Acaba en `/exec`.

### 5 · Comprovar la URL

Enganxa-la al navegador. Ha de sortir això:

```json
{"ok":true,"servei":"Bústia de formularis · CB Grup Barna","full":"Contactes web · CB Grup Barna","pestanyes":["Informació"]}
```

Si surt `"ok":false` o una pàgina d'error, el desplegament no està bé. Repassa
el pas 4 abans de seguir.

### 6 · Connectar la web

Obre `/scripts/formularis.js` i enganxa la URL a la primera línia de
configuració:

```javascript
var ENDPOINT = 'https://script.google.com/macros/s/.../exec';
```

Puja el canvi. En dos minuts els formularis ja escriuen al full.

---

## D'on ve cada pestanya

| Pestanya | Formulari | On és |
|---|---|---|
| Informació | «Vols informació?» | Portada |
| Galeria 3x3 | Porta d'accés a les 522 fotos | `/galeria-3x3-glories/` |
| Fotos 3x3 | Porta d'accés per descarregar | `/fotos-3x3/` i la galeria de l'esdeveniment |
| Altres | Qualsevol tipus que no reconegui | — |

Les pestanyes `Campus`, `Patrocini` i `Entrenadors` ja estan previstes al
programa i es crearan soles el dia que es connectin aquests formularis.

També apareixerà una pestanya **Errors** si mai en falla algun: hi queda el que
va arribar, de manera que un contacte no es perd encara que el programa peti.

---

## Coses que val la pena saber

**Si Google està caigut, no es perd ningú.** La web guarda l'enviament al
navegador de qui l'ha fet i el torna a provar sol quan aquella persona obre
qualsevol pàgina del web.

**Els robots no omplen el full.** Cada formulari porta un camp invisible que
només omplen els programes automàtics, i els enviaments fets en menys de dos
segons es descarten. Cap de les dues coses molesta a ningú real.

**Els mòbils no perden el zero.** Es desen com a text; si no, Google es menja
el 6 del davant en alguns formats.

**El correu no és obligatori.** Si algun dia molesta, `ENVIA_CORREU = false` a
dalt de `Codi.gs` i para, sense tocar res més. Les files se segueixen desant.

**Límit de correus**: 100 al dia amb un compte de Gmail normal. Molt per sobre
del que rep el club.

---

## Quan calgui donar de baixa algú

Ho ha de poder demanar, i el formulari ja ho promet. Amb tot en un sol full és
buscar el correu a totes les pestanyes i esborrar-ne les files. Abans d'això
estava repartit en cinc llocs.

Val la pena decidir també **quant de temps es guarda**. Una idea raonable: les
files de galeries, una temporada; les de l'Escoleta i el Campus, mentre la
família tingui relació amb el club.

---

## Portar-hi els formularis que no són de la web

Els de la web ja hi apunten sols. Els que viuen fora també poden acabar en
aquest mateix full, sense duplicar-lo:

**Google Forms** (el d'Entrenador/a). Obre el formulari → pestanya
**Respostes** → icona verda de full de càlcul → **Seleccionar un full de càlcul
existent** → tria `Contactes web · CB Grup Barna`. Google hi afegeix una
pestanya amb les respostes i la manté al dia sola. Cal ser-ne propietari o
editor: per això primer s'ha de saber de quin compte és.

**JotForm** (el Campus antic). A *Settings → Integrations → Google Sheets*,
apuntant al mateix full. Els enviaments que ja hi ha es poden baixar en CSV i
enganxar-los a la pestanya `Campus`.

**Fillout**, si finalment és l'eina del Campus: té la mateixa integració amb
Google Sheets. Mateix full, pestanya `Campus`.

---

## El que encara no hi passa

- **Campus.** Avui la inscripció és un enllaç de WhatsApp: no hi ha cap
  formulari que es pugui redirigir. El dia que n'hi hagi un, `tipus: 'campus'`
  i ja té pestanya reservada.
- **Entrenador/a** i **JotForm**: vegeu l'apartat de sobre. Són dos clics
  cadascun, però els ha de fer qui en sigui propietari.

## Què s'ha tret

Les galeries del 3x3 enviaven a **dos scripts de Google diferents**, un per
galeria, amb destins que no es podien veure des del repositori. Aquestes
crides s'han eliminat: ara les tres portes de fotos escriuen només aquí.

Si algun d'aquells scripts alimentava alguna altra cosa (una llista de correu,
per exemple), deixarà de rebre files noves. El que ja tenia s'hi queda; només
cal exportar-ho i enganxar-ho a la pestanya que toqui d'aquest full.
