# Integracions pendents · GBP, GEO baseline i CRM (19/08/2026)

Tres encàrrecs de l'Ana dins de la Fase 1 de la proposta "Web 10". Cap dels tres
el puc deixar acabat del tot sense una acció seva: aquí hi ha tot el que ja està
fet i exactament què falta i de qui depèn.

---

## 1. Google Business Profile — treballat en paral·lel en una altra sessió (19/08/2026)

L'Ana ho ha portat molt més lluny del que aquest document deixava preparat, en
una altra conversa: NAP canònic tancat, escrit a l'Ajuntament llest per
signar, missatgeria de Google activada amb missatge de benvinguda i 5
respostes desades, i horari especial d'agost resolt. Aquell treball viu en
tres documents (**01 NAP canònic i GBP**, **02 Auditoria NAP i pla de
neteja**, **03 Blocs web i schema**) que aquesta sessió no ha vist encara.

**Dades canòniques confirmades** (substitueixen la taula anterior d'aquest
document):
- Carrer de la Llacuna, 172 · 08018 Barcelona
- +34 698 425 153 (també WhatsApp — és el mateix número)
- marqueting@cbgrupbarna.info
- Secretaria: dl., dc. i dv. de 18 a 20 h — **tancada per vacances, reobre
  dilluns 24 d'agost**
- Fora d'horari de secretaria, el canal real és WhatsApp al mateix 698

**Pendent per aquesta sessió**: rebre el contingut real de l'**arxiu 03
"Blocs web i schema"** per aplicar-lo a `cbgrupbarna.info` — és el pas que
toca a aquest repositori i que no puc endevinar sense veure'l. Si també es
comparteix el 02 (auditoria NAP), es pot contrastar amb la taula d'aquest
document i tancar-la com a duplicat.

**Ja fet, no cal repetir-ho**: crear la fitxa GBP, activar missatgeria,
carregar horaris especials i preparar l'escrit al Fitxer d'Entitats — tot allò
que les seccions següents encara donaven per pendent.

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

---

## Llista completa del que necessito de l'Ana

No només el mínim per desbloquejar la Fase 1 — tot el que, si l'Ana me'l dona,
accelera qualsevol punt de la proposta "Web 10". Marcat per fase perquè no
sembli que tot cal avui.

### 🔑 Accessos i credencials

| Què | Per a què | Fase |
|---|---|---|
| Clau API de Brevo (SMTP & API → API Keys, compte "voluntaris") | Sincronitzar els formularis amb el CRM | 1 |
| Codi actual (o accés d'editor) de l'Apps Script que ja reben els formularis | Afegir-hi la funció de Brevo sense trencar el que funciona | 1 |
| Login de Google del club (business.google.com) | Crear/reclamar el Google Business Profile | 1 |
| Nombre d'inscripció del club al Fitxer General d'Entitats Ciutadanes, i qui n'és el/la representant legal | Agilitzar el tràmit de correcció del NAP | 1 |
| Accés de lectura a Google Search Console del domini | Mesurar posició SEO local i CWV (KPIs de la proposta) | 1–2 |
| Accés de lectura a la propietat GA4 (Data API) | Construir el dashboard analític a `/admin/` | 2 |
| Accés al panell de R2/Cloudflare (o a qui gestiona el hosting de fotos) | Treure les fotos del repositori (bloqueja desplegaments) | 2 |
| Compte Apple Developer Program i Google Wallet API | Emetre el carnet digital (Pass Type ID / Google Wallet) | 2–3 |
| Accés al domini/DNS si cal moure res (subdominis, redireccions) | Qualsevol canvi d'infraestructura de Fase 2–3 | 2–3 |

### 📄 Contingut i dades que només té l'Ana

| Què | Per a què | Fase |
|---|---|---|
| Fotos en alta (mínim 720 px, ideal 1500+) de La Nau, un entreno, l'escut | GBP i qualsevol marc ampli de la web (avui les de `img/` són massa petites) | 1 |
| Horaris per equip de les 5 instal·lacions que encara no en tenen | Landings d'instal·lació completes | 2 |
| Nivell Or/Plata/Bronze dels 22 patrocinadors (pendent des de l'auditoria original) | Dashboard de patrocinadors per nivell | 2 |
| Instagram de Foto Jané, Ovella Negra, Fundació Mullor, Tot Salut, Eix Comercial Sant Martí, Panteres Grogues (pendent des de l'auditoria original) | Fitxes de patrocinador completes | 2 |
| Càrrecs actuals de la Junta | Recuperar la pàgina d'Organigrama | 2 |
| Decisió: llista única de Brevo o una per origen (Escoleta, 3x3, Newsletter…) | Segmentació dels enviaments | 1 |
| Qui escriu/aprova el blog cada mes | Fixar la cadència mensual | 1 |
| URL de la botiga d'equipació, quan es decideixi llançar-la | Enllaçar-la (ja fora de Fase 1) | 3 |

### ✅ Decisions estratègiques

| Decisió | Per a què | Fase |
|---|---|---|
| Confirmar el generador estàtic (Astro proposat) o preferir-ne un altre | Migració d'arquitectura | 3 |
| ~~Quantes hores de voluntariat tècnic hi ha realment disponibles per setmana~~ **Resposta: 2 h/dia, cada dia (≈14 h/setmana)** | Ajustar el ritme del full de ruta | Totes |
| Ordre de prioritat si cal triar u entre carnet digital / àrea de família / cercador intern | Fase 3, si el temps no dona per als tres alhora | 3 |

Res d'aquesta llista bloqueja res per si sol: la Fase 1 avança amb els tres
primers ítems de "Accessos" i les dues primeres files de "Contingut". La resta
és perquè, quan hi hagi temps o l'Ana ho tingui a mà, ja estigui demanat una
sola vegada en lloc de gota a gota.

---

**Resum de qui fa què ara mateix:**

| Peça | Jo | L'Ana |
|---|---|---|
| GBP | Contingut i correcció NAP identificada | Iniciar sessió i crear la fitxa, aportar fotos |
| GEO baseline | Bateria de preguntes dissenyada | Llançar-la a ChatGPT/Perplexity/Gemini (o donar-me accés) |
| CRM | Arquitectura i codi Apps Script llest | Clau API de Brevo + accés a l'Apps Script |
