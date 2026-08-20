# Canals d'entrada · newsletter, bústia i protecció del menor

Tres formularis, tres destins diferents. Tot es configura a **`/js/canals.js`**;
no cal tocar cap HTML.

| Pàgina | Va a | Estat |
|---|---|---|
| `/newsletter/` · `/es/newsletter/` · `/en/newsletter/` | Brevo | Cal enganxar l'`action` |
| `/bustia/` · `/es/buzon/` · `/en/suggestions/` | Apps Script compartida, `source: 'bustia'` | Funciona |
| `/proteccio-menor/comunicar/` (+ es/en) | Apps Script **pròpia** de la Delegada | Desactivat a posta |

---

## 1 · Newsletter (Brevo)

Mentre `brevoAction` estigui buit **les altes no es perden**: van a la mateixa
full de càlcul que la resta de formularis, amb `source: 'newsletter-web'`. El que
no hi ha és enviament automàtic ni baixa amb un clic.

Per activar-ho:

1. Entra a [brevo.com](https://www.brevo.com) amb el compte del club.
2. **Contactes → Formularis → Crea un formulari**.
3. Posa-hi només dos camps: `EMAIL` (obligatori) i `NOM` (opcional).
4. Publica'l i obre **Comparteix → Codi HTML**.
5. Del codi que et dona, copia el valor de `action="…"` de l'etiqueta `<form>`.
   Fa aquesta pinta: `https://sibforms.com/serve/MUIFAK…`
6. Enganxa'l a `brevoAction` dins de `/js/canals.js` i desa.

Si a Brevo has anomenat els atributs d'una altra manera, canvia-ho a `brevoCamps`.

**Abans del primer enviament**, migra a Brevo els correus que ja hi ha a la full
de càlcul: hi ha altes des de `/fotos/`, `/fotos-3x3/` i `/galeria-3x3-glories/`,
totes amb `newsletter: 'Sí'`.

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
