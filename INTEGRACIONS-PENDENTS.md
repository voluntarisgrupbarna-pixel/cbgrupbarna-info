# Integracions pendents · GBP, GEO baseline i CRM (19/08/2026)

Tres encàrrecs de l'Ana dins de la Fase 1 de la proposta "Web 10". Cap dels tres
el puc deixar acabat del tot sense una acció seva: aquí hi ha tot el que ja està
fet i exactament què falta i de qui depèn.

---

## 1. Google Business Profile

**No puc crear ni reclamar la fitxa jo mateix**: cal iniciar sessió a
business.google.com amb el compte de Google del club, i no tinc ni navegador
autenticat ni les credencials. El que sí que puc deixar llest és tot el
contingut, perquè sigui un copiar-i-enganxar de 10 minuts.

### Troballa important: el NAP no és consistent

Cercant "CB Grup Barna" a Google per preparar aquest paquet, han sortit **dues
fitxes institucionals amb dades desactualitzades**:

| Font | Adreça | Telèfon | Correu |
|---|---|---|---|
| **cbgrupbarna.info** (oficial, avui) | Carrer de la Llacuna, 172 | +34 698 425 153 | info@cbgrupbarna.com |
| [guia.barcelona.cat](https://guia.barcelona.cat/detall/club-de-basquet-grup-barna-centre-parroquial-sant-marti-del-clot_96290111616.html) | C/ Llacuna **170** | **688 26 52 30** | **coordinaciocbgrupbarna@gmail.com** |
| [barcelona.cat/metropolis](https://www.barcelona.cat/metropolis/ca/detall/club-de-basquet-grup-barna_96290111616) | C/ Llacuna **170** | **688 26 52 30** | (mateix) |

Un NAP (Nom-Adreça-Telèfon) inconsistent confon Google a l'hora de decidir quina
fitxa és la "de veritat" i debilita el SEO local (pilar 3 de la proposta). Abans
de donar d'alta el GBP, val la pena que l'Ana demani la correcció d'aquestes
dues fitxes de l'Ajuntament — són backlinks institucionals valuosos, no s'han
d'esborrar, s'han d'actualitzar.

**Canal oficial verificat**: les dues fitxes surten del *Fitxer General
d'Entitats Ciutadanes* de l'Ajuntament. Hi ha un tràmit exprés per demanar la
modificació de dades (nom, adreça, contacte) d'una entitat ja inscrita:

> **Modificació de dades del Fitxer General d'Entitats Ciutadanes**
> https://seuelectronica.ajuntament.barcelona.cat/oficinavirtual/es/tramit/20230001592

Normalment cal certificat digital / idCAT / Cl@ve de qui sigui el/la
representant legal inscrit/a del club, i el número d'inscripció al Fitxer (si
no es té a mà, el propi tràmit permet cercar l'entitat pel nom). **No he pogut
verificar aquest requisit de certificat amb el propi formulari** (el
fetch a la pàgina va tornar un error), així que cal confirmar-ho en obrir el
tràmit.

**Alternativa més ràpida** si el club ja té contacte habitual amb el Districte
de Sant Martí (l'organigrama del club en parla): demanar-los directament per
correu la correcció, adjuntant les tres dades bones. Text llest per enviar:

> Bon dia, us escrivim del CB Grup Barna (Club Bàsquet Grup Barna, antic
> Centre Parroquial de Sant Martí del Clot) per demanar l'actualització de les
> nostres dades a la fitxa de la Guia BCN i al portal de Barcelona.cat/metropolis,
> que estan desactualitzades. Dades correctes: adreça Carrer de la Llacuna,
> 172, 08018 Barcelona (la fitxa diu 170); telèfon +34 698 425 153 (la fitxa diu
> 688 26 52 30); correu info@cbgrupbarna.com (la fitxa diu
> coordinaciocbgrupbarna@gmail.com). Moltes gràcies.

### Paquet de contingut, llest per enganxar

```
Nom del negoci:     CB Grup Barna (Club Bàsquet Grup Barna)
Categoria principal: Club esportiu (o "Basketball club" si Google la proposa)
Categories addicionals: Escola d'esports, Club juvenil
Adreça:              Carrer de la Llacuna, 172, 08018 Barcelona
Àrea de servei:      Districte de Sant Martí, Barcelona
Telèfon:             +34 698 425 153
Web:                 https://cbgrupbarna.info
Correu (no públic):  info@cbgrupbarna.com
```

**Descripció (proposada, 750 caràcters màx. de Google):**
> Club de bàsquet base i acadèmia de bàsquet al barri del Clot, Barcelona, des
> de 1965. Més de 34 equips federats i 450 jugadores i jugadors, amb paritat
> real entre la línia femenina i la masculina. Escoleta des dels 4 anys,
> categories fins a sènior, campus d'estiu de tecnificació i sis instal·lacions
> al Districte de Sant Martí. Primer entrenament de prova sense compromís.

**Horaris**: no hi ha un "horari d'oficina" únic publicat — cada categoria
entrena a hores diferents a les sis instal·lacions. Recomanació: marcar "Obert
segons cita" o publicar l'horari de l'Escoleta (dc. 17:30–18:40 Escola Casas,
ds. 09:00–10:30 La Nau) com a referència, i que l'Ana decideixi si hi ha un
horari d'atenció telefònica/WhatsApp per posar-hi.

**Fotos**: calen almenys 3–5 fotos reals (façana/entrada de La Nau, un
entrenament, l'escut). Les de `img/` actuals fan 360–550 px — per sota del
mínim recomanat per Google (720×720). Cal repescar-ne originals en alta.

**Un cop creada**: enllaçar-la des de `/instal-lacions/` (secció "La Nau del
Clot", ja existent) i des del peu de la portada.

---

## 2. Baseline GEO (què diu la IA generativa del club)

**Limitació honesta**: no tinc accés directe a les interfícies de xat de
ChatGPT, Perplexity, Gemini ni Copilot des d'aquesta sessió — no hi ha
compte ni API connectats. El que sí que puc fer és preparar la bateria de
preguntes (la part que realment cal dissenyar bé) i mesurar el que és
consultable per cerca web normal, que és un senyal parcial però real.

### La bateria de 12 preguntes (per llançar manualment cada trimestre)

1. Millor club de bàsquet al Clot, Barcelona
2. Acadèmia de bàsquet a Barcelona per a nens de 5 anys
3. Clubs amb bàsquet femení a Barcelona
4. Escola de bàsquet al Districte de Sant Martí
5. Campus d'estiu de bàsquet a Barcelona
6. Club de bàsquet base amb paritat femení/masculí a Catalunya
7. On juga el CB Grup Barna
8. Quan es va fundar el CB Grup Barna i per què es diu així
9. Bàsquet 3x3 a Barcelona per a nens
10. Clubs de bàsquet al barri del Clot
11. Quantes instal·lacions té el CB Grup Barna
12. Patrocinadors del CB Grup Barna

Per a cada resposta: registrar si cita cbgrupbarna.info (sí/no), si surt en
primera posició, i si les dades que dona són correctes (1965, paritat,
6 instal·lacions) o velles.

### El que sí que he pogut comprovar avui (cerca web, no IA generativa)

Cercant "CB Grup Barna bàsquet Clot Barcelona", el club ja apareix ben
posicionat i amb fonts diverses i institucionals:

- [cbgrupbarna.info](https://cbgrupbarna.info/) — lloc oficial
- [Federació Catalana de Basquetbol](https://www.basquetcatala.cat/club/24/25481) i les fitxes d'equip
- [Ajuntament de Barcelona — guia.barcelona.cat](https://guia.barcelona.cat/detall/club-de-basquet-grup-barna-centre-parroquial-sant-marti-del-clot_96290111616.html)
- [Ajuntament de Barcelona — barcelona.cat/metropolis](https://www.barcelona.cat/metropolis/ca/detall/club-de-basquet-grup-barna_96290111616)
- [Instagram](https://www.instagram.com/cbgrupbarna/) i [X/Twitter](https://twitter.com/CBGRUPBARNA)
- L'antic domini [cbgrupbarna.com](https://cbgrupbarna.com/) encara indexa i apareix

És una base sòlida per a GEO: contingut divers i coherent és exactament el
que fa que un motor generatiu citi una font amb confiança. El forat detectat
al punt 1 (NAP inconsistent a les fitxes de l'Ajuntament) és també el
principal risc per a aquest pilar — es corregeix amb la mateixa acció.

**Recomanació**: llançar la bateria completa (12 preguntes × 4 eines) a mà, o
en una sessió que sí tingui accés a aquestes eines, i registrar-ho com a
línia base d'aquest trimestre.

---

## 3. CRM: tots els formularis cap a Brevo

L'Ana ja té compte de Brevo (base de dades de mailing, compte "voluntaris").
La pregunta correcta no és "quin CRM gratis triem", és **"fem servir el que ja
tenim"** — evita duplicar dades en dues eines i és el pas natural per tancar
alhora dos punts de la Fase 1: "Eina de correu triada i activada" i "CRM
lleuger unificat" (Fase 2) es converteixen en una sola peça de feina.

### Per què Brevo i no un CRM nou

| | **Brevo (ja actiu)** | HubSpot Free | Zoho Free |
|---|---|---|---|
| Contactes | Il·limitats (pla gratuït) | 1.000–1.000.000 segons la font, poc clar | 5.000 registres, 3 usuaris |
| API pròpia | REST completa + webhooks, ja disponible | Sí, però és una eina nova a aprendre | Sí, eina nova |
| Ja fem servir | Sí, per a mailing | No | No |
| Cost afegit | Cap | Cap (però un compte i un flux nous) | Cap (ídem) |

Conclusió: cap alternativa gratuïta justifica obrir un tercer sistema quan
Brevo ja cobreix contactes il·limitats i API completa. Es descarta HubSpot i
Zoho per aquest ús — es queden com a opció si el club algun dia necessita
pipeline de vendes real, que no és el cas.

### Arquitectura proposada

El repositori ja té un backend lleuger: **un Apps Script Web App** que reben
els formularis de `/fotos-3x3/`, `/galeria-3x3-glories/` i
`/fotos-esdeveniments/3x3-westfield-2026/` (`action=register` /
`action=subscribe`), que escriu a un full de càlcul. És exactament on ha
d'enganxar Brevo — sense exposar mai la clau API al navegador:

```
Formulari (web) → POST → Apps Script (ja existent)
                             ├── desa a Google Sheet (com ara)
                             └── NOU: POST a l'API de Brevo → contacte creat/actualitzat
```

**Codi a afegir dins de l'Apps Script existent** (funció nova, cridada des del
`doPost` que ja hi ha):

```javascript
// Clau API: Project Settings → Script Properties → BREVO_API_KEY
// (mai al codi ni al repositori)
function sincronitzaBrevo(dades) {
  const apiKey = PropertiesService.getScriptProperties().getProperty('BREVO_API_KEY');
  if (!apiKey) return; // no bloquegis el formulari si Brevo encara no està configurat

  const payload = {
    email: dades.email,
    attributes: {
      NOM: dades.nom || '',
      COGNOMS: dades.cognoms || '',
      SMS: dades.mobil || '',
      FONT: dades.font || 'web',      // d'on ve: /fotos/, /galeria-3x3-glories/...
    },
    listIds: [/* ID de llista Brevo a definir */],
    updateEnabled: true,               // si ja existeix, actualitza en lloc de fallar
  };

  UrlFetchApp.fetch('https://api.brevo.com/v3/contacts', {
    method: 'post',
    contentType: 'application/json',
    headers: { 'api-key': apiKey },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true,          // no petis el formulari si Brevo falla
  });
}
```

### Què necessito de l'Ana per acabar-ho

1. **Clau API de Brevo**: Brevo → SMTP & API → API Keys → crear-ne una de
   nova ("cbgrupbarna-web"). Es guarda a *Script Properties* de l'Apps Script,
   mai al repositori.
2. **Accés a l'Apps Script existent** (o el codi complet actual) per afegir-hi
   la funció de dalt sense trencar el que ja funciona.
3. **ID(s) de llista a Brevo**: una llista única "Web" o una per origen
   (Escoleta, 3x3, Newsletter…) — decisió d'Ana segons com vulgui segmentar
   els enviaments després.
4. **Decidir `/fotos/`**: avui fa servir formsubmit.co (envia un correu, no
   escriu enlloc). Migrar-lo al mateix Apps Script uniformitza les dades però
   és un canvi més gran — es proposa per a la Fase 2, no ara.

Un cop tingui la clau i l'accés, puc deixar-ho desplegat i provat en una
sessió.

---

**Resum de qui fa què ara mateix:**

| Peça | Jo | L'Ana |
|---|---|---|
| GBP | Contingut i correcció NAP identificada | Iniciar sessió i crear la fitxa, aportar fotos |
| GEO baseline | Bateria de preguntes dissenyada | Llançar-la a ChatGPT/Perplexity/Gemini (o donar-me accés) |
| CRM | Arquitectura i codi Apps Script llest | Clau API de Brevo + accés a l'Apps Script |
