# Brevo · el CRM del club

Tots els formularis del web acaben a **Brevo**. Aquest document diu **què s'ha
de crear dins de Brevo** (atributs, llistes i formularis) i **què s'ha
d'enganxar al web** perquè es connectin. No cal tocar cap HTML: tot es
configura a **`/js/canals.js`**, al bloc `brevo`.

> ⚠️ **Aquí no hi va mai una clau d'API de Brevo.** La web és estàtica i
> qualsevol pot llegir els fitxers `.js`. Es fan servir els **formularis
> allotjats a Brevo** (`sibforms.com/serve/…`), que accepten un enviament
> normal i no necessiten cap clau.

---

## Estat actual

| Formulari del web | Canal a `canals.js` | Llista a Brevo | Estat |
|---|---|---|---|
| Portada · «Vull informació» | `portada` | Vull informació | ⬜ Falta l'`action` |
| `/escriu-nos/` (+ es/en) | `informacio` | Vull informació | ⬜ Falta l'`action` |
| `/portes-obertes/` (+ es/en) | `portesObertes` | Portes obertes | ⬜ Falta l'`action` |
| `/newsletter/` (+ es/en) | `newsletter` | Newsletter | ⬜ Falta l'`action` |
| `/bustia/` (+ es/en) | `bustia` | Bústia | ⬜ Falta l'`action` |
| `/opina/` | `ressenya` | Ressenyes | ⬜ Falta l'`action` |
| Finestra de descàrrega de documents | `descarrega` | Descàrregues | ⬜ Falta l'`action` |
| `/fotos/` i `/galeria-3x3-glories/` | `galeria` | Galeria | ⬜ Falta l'`action` |
| `/proteccio-menor/comunicar/` | — | **cap** | 🚫 No hi va, a posta |

Mentre una casella estigui buida, aquell formulari **segueix funcionant
exactament com fins ara** (full de càlcul, Formspree o WhatsApp): no es perd cap
alta, però no arriba al CRM. Es poden activar d'un en un, en qualsevol ordre.

Quan n'activis un, marca la fila amb ✅ perquè la taula segueixi dient la veritat.

---

## Pas 0 · El compte i el domini

Abans de tocar cap formulari:

1. **Un sol compte de Brevo per al club**, amb el correu genèric
   (`voluntarisgrupbarna@gmail.com`), no el personal de ningú. Convida-hi la
   resta des de **Configuració → Els meus usuaris**.
2. **Autentica el domini** a **Configuració → Emissors, dominis i IPs
   dedicades → Dominis**. Brevo et dona uns registres **DKIM, SPF i DMARC** que
   s'han d'afegir al DNS de `cbgrupbarna.info`. Sense això els correus del club
   acaben a la brossa de Gmail i Outlook. Es pot fer després de connectar els
   formularis, però **abans del primer enviament**.
3. **Emissor per defecte**: `hola@cbgrupbarna.info` (o el que faci servir el
   club), amb el nom «CB Grup Barna».

L'ordre de la feina: **pas 1 (atributs) → pas 2 (llistes) → pas 3 (formularis)**.
No es pot canviar: un formulari no pot fer servir un atribut que encara no
existeix.

## Pas 1 · Crear els atributs de contacte

**Contactes → Configuració → Atributs de contacte.** Es fa **una sola vegada** i
serveix per a tots els formularis. Els noms han de ser **exactament** aquests
(si en poses uns altres, canvia'ls també a `canals.js` → `brevo.camps`):

| Atribut | Tipus | Què hi ha |
|---|---|---|
| `EMAIL` | ja existeix | Correu electrònic |
| `NOM` | Text | Nom de qui escriu |
| `TELEFON` | Text | Mòbil, si l'han deixat |
| `IDIOMA` | Text | `ca`, `es` o `en` — l'idioma en què navegava |
| `ORIGEN` | Text | Quin formulari ho ha enviat (`portada`, `portes-obertes`…) |
| `INTERES` | Text | Escoleta, Campus, 3x3, Patrocini… (separat per comes) |
| `TEMA` | Text | El desplegable de tema, o el document descarregat |
| `MISSATGE` | Text | El que han escrit |
| `ANY_NAIX` | Text | Any de naixement (portes obertes) |
| `CONTACTE` | Text | Nom de la criatura, quan qui escriu és la família |
| `ESTRELLES` | Text | Puntuació de la ressenya, d'1 a 5 |
| `CONSENT` | Text | `Sí` / `No` — si han marcat la casella comercial |

`TELEFON` és de text a posta i **no** és el camp `SMS` de Brevo: la gent hi
escriu el número de mil maneres i el camp `SMS` rebutja el que no sigui un
número internacional ben format, cosa que faria caure l'alta sencera.

## Pas 2 · Crear les llistes

**Contactes → Llistes → Crea una llista.** Una per canal. Separar-les no és
manía d'ordre: és el que permet enviar un correu comercial **només** a qui l'ha
demanat.

| Llista | Qui hi entra | Se li pot enviar publicitat? |
|---|---|---|
| Newsletter | Qui s'apunta a `/newsletter/` amb la casella marcada | **Sí** |
| Vull informació | Portada i `/escriu-nos/` | Només resposta a la seva consulta |
| Portes obertes | Qui demana provar un entrenament | Només l'organització de la prova |
| Bústia | Qui deixa el correu per rebre resposta | Només la resposta |
| Ressenyes | Qui deixa una ressenya a `/opina/` | No |
| Descàrregues | Qui es baixa un document | Només si `CONSENT` = `Sí` |
| Galeria | Qui entra a les fotos acceptant la newsletter | **Sí** |

## Pas 3 · Crear un formulari per canal

Per cada fila de la taula d'estat: **Contactes → Formularis → Crea un
formulari**.

1. Afegeix-hi els camps del canal (llista a baix). Marca **`EMAIL` com a
   obligatori** i **la resta com a opcionals**: si un camp és obligatori a Brevo
   i el web no l'envia, Brevo rebutja l'alta sencera.
2. A **«Llistes»**, tria la llista del canal.
3. A **«Confirmació»**:
   - Newsletter i Galeria → **doble opt-in** (Brevo envia el correu de
     confirmació ell mateix).
   - La resta → **simple**: qui demana informació no ha d'haver de confirmar
     res per rebre una resposta.
4. Publica'l i obre **«Comparteix → Codi HTML»**.
5. Del codi, copia el valor de `action="…"` de l'etiqueta `<form>`. Fa aquesta
   pinta: `https://sibforms.com/serve/MUIFAK…`
6. Enganxa'l a la línia del canal a `/js/canals.js` → `brevo.formularis` i desa.

El disseny del formulari a Brevo **és igual**: ningú el veurà mai. Qui l'omple
ho fa a la web del club; Brevo només rep les dades.

### Camps de cada formulari

| Canal | Camps que hi ha de posar |
|---|---|
| `portada` | `EMAIL`, `NOM`, `TELEFON`, `INTERES`, `MISSATGE`, `IDIOMA`, `ORIGEN`, `CONSENT` |
| `informacio` | `EMAIL`, `NOM`, `TELEFON`, `TEMA`, `MISSATGE`, `IDIOMA`, `ORIGEN` |
| `portesObertes` | `EMAIL`, `NOM`, `TELEFON`, `CONTACTE`, `ANY_NAIX`, `MISSATGE`, `IDIOMA`, `ORIGEN` |
| `newsletter` | `EMAIL`, `NOM`, `IDIOMA`, `ORIGEN`, `CONSENT` |
| `bustia` | `EMAIL`, `TEMA`, `IDIOMA`, `ORIGEN` |
| `ressenya` | `EMAIL`, `NOM`, `ESTRELLES`, `MISSATGE`, `IDIOMA`, `ORIGEN` |
| `descarrega` | `EMAIL`, `NOM`, `TELEFON`, `TEMA`, `IDIOMA`, `ORIGEN`, `CONSENT` |
| `galeria` | `EMAIL`, `NOM`, `TELEFON`, `TEMA`, `IDIOMA`, `ORIGEN`, `CONSENT` |

## Pas 4 · Comprovar-ho

Amb l'`action` enganxada i desada, omple el formulari del web amb un correu del
club i mira **Contactes → Llista del canal**: el contacte hi ha de ser, amb els
atributs plens, en menys d'un minut. Si no hi és:

- Torna a mirar que l'`action` sigui la del `<form>` i no la de cap `<script>`.
- Mira que `EMAIL` sigui l'únic camp obligatori del formulari de Brevo.
- Mira que els noms dels atributs de Brevo siguin els mateixos que a
  `canals.js` → `brevo.camps`.

---

## Coses que el codi fa a posta

**El canal de protecció del menor no passa mai per Brevo.** El que s'hi
comunica és la seguretat d'un infant, no una oportunitat comercial, i no ha de
viure en un CRM que veu tot el club. Aquelles pàgines ni tan sols carreguen
`/js/brevo.js`. Segueix les instruccions de `README-canals.md`.

**La bústia és anònima i ho continua sent.** Si qui escriu no deixa el correu,
a Brevo no hi arriba res. Si el deixa, hi arriba el contacte i el tema, **però
no el text del missatge**: aquell es queda a la full de càlcul, que és on el
llegeix qui l'ha de contestar.

**Qui només deixa un telèfon no arriba a Brevo.** A `/escriu-nos/` i a
`/portes-obertes/` el camp diu «telèfon o correu». Brevo identifica els
contactes **pel correu**, així que si només hi ha un número, el web l'envia a la
full de càlcul com sempre i no crea contacte al CRM. No es perd: simplement viu
en un altre lloc. Si algun dia volem que hi entrin tots, cal separar el camp en
dos (telèfon i correu) a les sis pàgines.

**Brevo no substitueix res, s'hi suma.** Cada formulari segueix enviant on
enviava (full de càlcul, Formspree, WhatsApp). Són dos destins alhora mentre no
tinguem l'històric sencer a Brevo i la confiança que no es perd res. El dia que
es vulgui apagar la full, es fa esborrant una branca `if` de cada handler.

**Si Brevo falla, l'usuari no se n'assabenta.** Les crides van amb
`mode: 'no-cors'` i no bloquegen res: si Brevo no respon, el formulari acaba
igual i l'alta segueix arribant per l'altre camí.

---

## Feina pendent al mateix Brevo

- **Migrar-hi l'històric.** A la full de càlcul hi ha altes de `/fotos/`,
  `/fotos-3x3/` i `/galeria-3x3-glories/` amb `newsletter: 'Sí'`. Exporta-les a
  CSV i importa-les a la llista **Newsletter** abans del primer enviament.
- **Automatització de `CONSENT`.** A **Automatitzacions**, crea'n una: si un
  contacte entra amb `CONSENT = Sí`, afegeix-lo també a la llista
  **Newsletter**. Així la casella de les descàrregues serveix de debò.
- **Correu de benvinguda** de la newsletter, que ara no existeix.
