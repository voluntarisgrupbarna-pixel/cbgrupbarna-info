# El cercador de cbgrupbarna.info

Cerca a tot el web **sense servidor i sense servei de tercers**. La consulta no
surt del navegador de qui cerca: no s'envia a Google, no cal consentiment de
galetes i no queda registrada enlloc.

**Respon, no només enllaça.** El web ja portava **460 preguntes amb la resposta
escrita pel club**, dins del JSON-LD `FAQPage` de 98 pàgines. El cercador les
indexa i ensenya la que toca a dalt de tot, **tal com està escrita**, amb
l'enllaç a la pàgina d'on surt.

> No hi ha cap model de llenguatge pel mig, i és a posta: no s'inventa res, no
> costa res per consulta, no hi ha cap clau d'API que mantenir, contesta a
> l'instant i la pregunta no surt del navegador —o sigui que la política de
> privacitat no s'ha de tocar. El preu és que només sap respondre el que algú
> del club ja ha escrit. Quan cap pregunta encaixa prou bé (llindar
> `LLINDAR_FAQ` a `js/cerca.js`), **no ensenya res**: una resposta que no toca
> fa més mal que no respondre.

## Les peces

| Fitxer | Què fa |
|---|---|
| `.github/scripts/generate-search-index.py` | Llegeix tots els `.html` i escriu `/cerca-index.json`: 354 pàgines **i les 460 preguntes amb resposta del JSON-LD** (uns 575 KB, ~150 KB per la xarxa). Salta `noindex`, redireccions, `/admin/`, `/galeria/` i els residus de `/patrocinis/`. |
| `/cerca-index.json` | L'índex. **No s'edita a mà**: es regenera. |
| `js/cerca.js` | El motor i la interfície. |
| `css/cerca.css` | L'estil, amb els tokens del sistema visual. |
| `/cerca/`, `/es/busqueda/`, `/en/search/` | La versió a pàgina sencera, amb `?q=`. `noindex, follow`, i per això no entren al `sitemap.xml`. |
| `scripts/afegeix-cerca.py` | Posa les dues línies del cercador a totes les pàgines amb capçalera del club. |
| `i18n/faq.yml` | **La font única de les preguntes freqüents**: una entrada per pregunta, amb els tres idiomes i la pàgina on va. |
| `.github/scripts/generate-faq.py` | Les reparteix al `<details>` i al JSON-LD de les tres versions de cada pàgina, entre marcadors. |
| `scripts/faq-migra.py` | Va passar a la font única les preguntes que vivien dins de l'HTML. Ja no queda res per migrar, però serveix si algun dia n'apareix una pàgina nova amb FAQ escrites a mà. |
| `scripts/faq-tradueix.py` | Omple les traduccions que falten amb el traductor del web. |
| `tests/cerca/prova-motor.mjs` | 45 casos de prova del motor contra l'índex real, sense navegador: quins resultats surten, quina resposta es dona i quines consultes no n'han de treure cap. |

## Com s'obre

Des de qualsevol pàgina: la **lupa de la capçalera**, **⌘K / Ctrl+K**, o la tecla
**`/`**. El botó no s'escriu a l'HTML de cada pàgina: el planta `js/cerca.js`
dins de la capçalera que hi trobi. Una pàgina nova només necessita:

```html
<link rel="stylesheet" href="/css/cerca.css">   <!-- abans de </head> -->
<script src="/js/cerca.js" defer></script>      <!-- abans de </body> -->
```

I això ja ho posa sol `python3 scripts/afegeix-cerca.py` (té `--dry-run`). Els
dos generadors de pàgines —`scripts/build-pages.py` i
`.github/scripts/generate-team-pages.py`— ja les emeten, o sigui que el que
generen surt amb cerca sense fer res més.

## Com es manté al dia

El workflow **`.github/workflows/sitemap.yml`** refà el sitemap **i** l'índex
cada cop que es publica un `.html` a `main`, en un sol commit. El robot diari de
partits (`update-partits.yml`) també el refà després de generar les fitxes
d'equip, perquè el seu commit porta `[skip ci]` i no engegaria l'altre.

A mà, si cal:

```bash
python3 .github/scripts/generate-search-index.py
node tests/cerca/prova-motor.mjs
```

## Com es fa més llest

Gairebé tot el que fa que la cerca encerti viu en **dues taules de `js/cerca.js`**,
i afegir-hi una fila és la manera barata de millorar-la:

- **`SINONIMS`** — famílies de paraules. Tot el que hi ha en una fila és la
  mateixa cosa, en els tres idiomes. Per això «cuánto cuesta», «quant costa» i
  «how much» arriben al mateix lloc encara que la pàgina no ho digui així.
- **`DESTINS`** — la porta d'entrada de cada família, **per ordre**: la primera
  és la resposta, les altres el context. Es tradueixen soles als altres idiomes
  amb `i18n/routes.yml`.
- **`RESPOSTES`** — el pla B escrit a mà, per a les intencions que **cap** FAQ
  del web cobreix (contacte, portes obertes). Només surt si no s'ha trobat cap
  pregunta que encaixi.

**La millor manera de fer-lo més llest, però, no és tocar codi: és escriure
preguntes freqüents.** I això ja no es fa pàgina per pàgina: s'escriuen a
**`i18n/faq.yml`**, un sol cop, amb els seus tres idiomes, i
`.github/scripts/generate-faq.py` les reparteix al `<details>` i al JSON-LD de
les tres versions de la pàgina.

```bash
python3 .github/scripts/generate-faq.py --dry-run   # què faria
python3 .github/scripts/generate-faq.py             # ho fa
python3 .github/scripts/generate-faq.py --pendents  # què espera una dada
```

La pàgina de destí ha de portar els marcadors `<!-- FAQ:START -->` /
`<!-- FAQ:END -->` i `<!-- FAQ-LD:START -->` / `<!-- FAQ-LD:END -->`; fora
d'aquí l'script no hi toca res, com fa `generate-seo-snapshot.py` a
`/partits/`. Si no els troba, avisa i no escriu.

Una entrada amb `pendent:` no es publica **enlloc**, ni en català: serveix per
deixar la pregunta escrita mentre s'espera un preu o una data, sense publicar
mitja resposta.

### Les traduccions no s'escriuen a mà

`scripts/faq-tradueix.py` omple les que falten amb **el mateix traductor que
ja fa servir la resta del web** (`scripts/i18n-tradueix.py`): el mateix
glossari, el mateix to per idioma, els mateixos noms propis que no es toquen
mai i la mateixa comprovació que no s'han perdut pel camí.

```bash
python3 scripts/faq-tradueix.py --que-falta   # què falta, sense clau ni cost
python3 scripts/faq-tradueix.py --tot         # amb ANTHROPIC_API_KEY
```

Com la resta del sistema d'i18n, **sense clau no falla**: diu què falta i
marxa. I no publica mai: omple el YAML, i qui escriu a les pàgines continua
sent `generate-faq.py`, un pas a part, perquè entre les dues coses hi hagi
algú mirant-s'ho.

`scripts/i18n-lint.py` també les vigila: una pregunta publicada en català i
sense traduir surt com a `faq-sense-traduccio`, i una que espera una dada, com
a `faq-sense-resposta`. Són el mateix deute que una pàgina sense traduir, i ara
surten a la mateixa llista.

> Per què una font única: el 23/08/2026 hi havia **28 pàgines amb les tres
> versions desquadrades** (la portada anava 15/11/11). Una pregunta viu a sis
> llocs —`<details>` i JSON-LD, per tres idiomes— i sis llocs a mà no
> aguanten.
>
> **Ja no en queda cap.** Totes les preguntes del web han passat per la font
> única i les 98 pàgines amb FAQ tenen el `<details>` visible i el JSON-LD
> quadrats. Cap pàgina amb versió traduïda té un nombre de preguntes diferent
> del català.

Si toques qualsevol de les tres, **afegeix el cas nou a `tests/cerca/prova-motor.mjs`**
i executa'l: és el que impedeix que arreglar una cerca en trenqui tres.

## Detalls que val la pena saber

- **Quan respon i quan no.** La consulta es compara amb les 460 preguntes: les
  interrogatives (`quan`, `on`, `com`, `cuánto`, `when`, `how`…) hi compten,
  perquè són el que distingeix «quan és el campus» de «quant costa el campus»;
  en canvi «club», «Barna» i «bàsquet» **no** compten, perquè surten a gairebé
  totes i farien que qualsevol cosa semblés que encaixa. Cal que hi surti com a
  mínim la meitat del que s'ha escrit, i que la millor passi el llindar. Una
  paraula solta («fotos») és un tema, no una pregunta: no en treu cap.
- **Idioma.** Es mira l'atribut `lang` i el prefix `/es/` o `/en/`. Una pàgina en
  un altre idioma baixa de posició **només si existeix la versió en el teu**; si
  no n'hi ha cap altra (com `/magics/`), no se la penalitza, perquè és l'única
  que respon.
- **Faltes d'ortografia.** Fins a una lletra en paraules de 5 a 7, i dues a
  partir de 8. «Escoleata» troba l'Escoleta.
- **Accents, majúscules, `ç` i `l·l`** són indiferents.
- **L'índex es baixa quan el navegador no té feina** (`requestIdleCallback`), i
  **mai** amb estalvi de dades activat o en xarxes 2G: primer va la pàgina.
- **Les cerques recents** es guarden a `localStorage`, només al dispositiu de qui
  cerca, i es poden esborrar des del mateix cercador.
