# Canals d'entrada · newsletter, bústia i protecció del menor

Tres formularis, tres destins diferents. Tot es configura a **`/js/canals.js`**;
no cal tocar cap HTML.

| Pàgina | Va a | Estat |
|---|---|---|
| `/newsletter/` · `/es/newsletter/` · `/en/newsletter/` | Apps Script compartida, `source: 'newsletter-web'` | Funciona |
| `/bustia/` · `/es/buzon/` · `/en/suggestions/` | Apps Script compartida, `source: 'bustia'` | Funciona |
| `/proteccio-menor/comunicar/` (+ es/en) | Apps Script **pròpia** de la Delegada | Desactivat a posta |
| `/campus/#llista-espera` (+ es/en) | Apps Script **pròpia** del campus, `source: 'campus-llista-espera'` | Cal desplegar-la |

---

## 1 · Newsletter

**Decisió del club (28/08/2026): sense eina externa d'enviament (Brevo,
Mailchimp...).** Totes les altes —de `/newsletter/` i de la casella de
butlletí a la porta de descàrrega de PDF— van a la mateixa full de càlcul
que la resta de formularis, amb `source: 'newsletter-web'`. L'enviament del
correu mensual es fa a mà des d'aquesta full.

Si mai es vol automatitzar l'enviament sense sortir de Sheets, l'eina a
mirar és **Google Apps Script + Gmail** (enviar des del mateix full amb
`MailApp`/`GmailApp`), no un ESP extern: manté tot al mateix lloc i sense
donar les dades a un tercer nou.

---

## 2 · Bústia de suggeriments

Ja funciona, no cal fer res. Arriba a la full de sempre amb `source: 'bustia'`.

És **anònima**: si qui escriu no omple el camp del correu, el missatge s'envia
sense cap dada que l'identifiqui. El camp del correu només viatja si l'ha escrit.

---

## 3 · Canal de protecció del menor

> ⚠️ `proteccioEndpoint` és buit **a posta**. No hi enganxis l'endpoint de la
> bústia. El codi ho comprova i, si són el mateix, es nega a activar el formulari.

Mentre estigui buit, la pàgina amaga el formulari i mostra el correu de la
Delegada de Protecció al Menor. **No hi ha res trencat**: aquest és el
comportament segur, i el canal segueix obert.

Per activar el formulari cal muntar una tuberia separada, perquè el que hi entra
són comunicacions sobre la seguretat d'infants i no poden compartir full amb les
inscripcions:

1. Crea un **full de càlcul nou**, a part. Comparteix-lo **només** amb la
   Delegada de Protecció al Menor. Ningú més.
2. **Extensions → Apps Script** dins d'aquell full, i publica un desplegament web
   (*Qualsevol persona*, executant-se com tu).
3. Enganxa la URL del desplegament a `proteccioEndpoint` a `/js/canals.js`.
4. Prova-ho enviant-te una comunicació de prova i mirant que arriba al full nou i
   **no** al compartit.

### Dues coses que no s'han de canviar de la pàgina

- **Els telèfons externs** (112, 116 111, 900 202 010). Han de ser visibles a
  dalt i abans del formulari. La LOPIVI espera que qui necessita ajuda urgent la
  trobi sense haver de passar pel club.
- **L'avís sobre la Delegada i la Junta.** La Delegada de Protecció és alhora
  membre de la Junta Directiva; un canal intern no pot ser jutge de si mateix.
  Per això la pàgina diu explícitament què fer si la comunicació va sobre elles.

### El que la pàgina promet, i s'ha de complir

- Resposta **abans de 7 dies** si qui escriu ha deixat un contacte.
- Ho llegeix **només** la Delegada.
- Si hi ha indici de risc per a un infant, es comunica a les autoritats encara
  que qui ho envia demani que no. Això la pàgina ja ho diu obertament: no és una
  lletra petita.

---

## 4 · Llista d'espera del campus

**Estat: les altes es guarden, però encara no surt cap correu.**

Mentre `campusEndpoint` estigui buit, el formulari cau a la mateixa Apps Script
de la bústia amb `source: 'campus-llista-espera'`. Això vol dir que **no es perd
ningú** —la fila hi és, es pot filtrar per aquell `source`— però ni el club rep
l'avís ni la família rep la confirmació. S'han d'escriure a mà.

Per activar-ho cal una Apps Script pròpia, perquè aquesta fa dues coses que la de
la bústia no fa: enviar correu al club i enviar confirmació a qui s'apunta, en el
seu idioma. El codi sencer, comentat, és a **`scripts/apps-script-campus.gs`**.

Això no ho pot fer un agent: Google demana que una persona autoritzi amb el seu
compte els permisos de full de càlcul i d'enviament de correu. Hi ha dos camins.

### Camí curt (tres passos, recomanat)

Aprofitar l'Apps Script que el club **ja té desplegada** —la de la bústia— en
comptes de crear-ne una de nova. Les instruccions són a dalt de
**`scripts/apps-script-bustia-afegit.gs`**: enganxar el fitxer al final del codi
que ja hi ha, afegir una línia al `doPost` existent i tornar a desplegar. L'URL
no canvia i no cal tocar `js/canals.js`.

Les altes van a la full de sempre amb `source: 'campus-llista-espera'`. No és cap
novetat de protecció de dades: `/portes-obertes/` ja hi envia nom i any de
naixement de criatures.

### Camí llarg (full i projecte propis)

Si es vol la llista d'espera separada de la resta, són sis passos:

1. Full de càlcul nou al Drive del club, de nom **«Campus · llista d'espera»**.
2. Dins del full: **Extensions → Apps Script**.
3. Esborra el que hi hagi i enganxa tot `scripts/apps-script-campus.gs`.
4. Revisa `AVIS_A` a dalt de tot (ara mateix, `marqueting@cbgrupbarna.info`).
5. **Desplega → Nou desplegament → Aplicació web**, amb
   *Executa com a:* **jo** i *Qui hi té accés:* **qualsevol**.
   Google demanarà els permisos: accepta'ls.
6. Copia l'URL que acaba en `/exec` i enganxa'l a `campusEndpoint` de
   `js/canals.js`.

### Com saber si ha anat bé

Obre l'URL `/exec` al navegador, tal qual. Ha de respondre un JSON amb
`"ok": true`, si veu la full i quants correus pot enviar avui. Si vols provar
els correus de debò, a l'editor d'Apps Script tria la funció **`provaCorreu`**
al desplegable i clica Executa: envia els dos correus a `AVIS_A` i escriu una
fila de prova que després pots esborrar a mà.

### Si algú fa servir una versió pròpia de l'script

Els noms dels camps són un contracte amb `js/llista-espera.js`. El formulari
envia sempre aquest JSON, i qualsevol script que el rebi ha de llegir aquestes
claus exactes:

```
nom · any · tutor · correu · telefon · edicions · missatge · idioma · source
```

`edicions` arriba com a text separat per comes (`nadal, estiu`), `idioma` és
`ca`, `es` o `en` —serveix per triar l'idioma del correu de confirmació— i
`source` sempre val `campus-llista-espera`. Si es canvia un nom d'aquests a
l'script, cal canviar-lo també al JavaScript, o les files sortiran buides.

**Compte amb una cosa:** el correu de confirmació surt del compte de Google que
desplega l'script, amb el seu límit diari d'enviaments (100 al dia en un compte
gratuït, 1.500 en un de Workspace). Per a una llista d'espera de campus sobra de
llarg, però si algun dia s'omple, la fila es desa igualment i el que falla és
només el correu.
