# El cercador de cbgrupbarna.info

Cerca a tot el web **sense servidor i sense servei de tercers**. La consulta no
surt del navegador de qui cerca: no s'envia a Google, no cal consentiment de
galetes i no queda registrada enlloc.

## Les peces

| Fitxer | Què fa |
|---|---|
| `.github/scripts/generate-search-index.py` | Llegeix tots els `.html` i escriu `/cerca-index.json` (uns 490 KB, ~130 KB per la xarxa). Salta `noindex`, redireccions, `/admin/`, `/galeria/` i els residus de `/patrocinis/`. |
| `/cerca-index.json` | L'índex. **No s'edita a mà**: es regenera. |
| `js/cerca.js` | El motor i la interfície. |
| `css/cerca.css` | L'estil, amb els tokens del sistema visual. |
| `/cerca/`, `/es/cerca/`, `/en/search/` | La versió a pàgina sencera, amb `?q=`. `noindex, follow`, i per això no entren al `sitemap.xml`. |
| `scripts/afegeix-cerca.py` | Posa les dues línies del cercador a totes les pàgines amb capçalera del club. |
| `tests/cerca/prova-motor.mjs` | 27 casos de prova del motor contra l'índex real, sense navegador. |

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
- **`RESPOSTES`** — les preguntes que mereixen una resposta i no una llista
  d'enllaços (contacte, com apuntar-s'hi, on entrenem, quotes…). Surten a dalt
  de tot, amb el text ja escrit en els tres idiomes.

Si toques qualsevol de les tres, **afegeix el cas nou a `tests/cerca/prova-motor.mjs`**
i executa'l: és el que impedeix que arreglar una cerca en trenqui tres.

## Detalls que val la pena saber

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
