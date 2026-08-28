# Canals d'entrada · newsletter, bústia i protecció del menor

Tres formularis, tres destins diferents. Tot es configura a **`/js/canals.js`**;
no cal tocar cap HTML.

| Pàgina | Va a | Estat |
|---|---|---|
| `/newsletter/` · `/es/newsletter/` · `/en/newsletter/` | Apps Script compartida, `source: 'newsletter-web'` | Funciona |
| `/bustia/` · `/es/buzon/` · `/en/suggestions/` | Apps Script compartida, `source: 'bustia'` | Funciona |
| `/proteccio-menor/comunicar/` (+ es/en) | Apps Script **pròpia** de la Delegada | Desactivat a posta |

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
