# Idiomes del site

El web és **en català**. Sobre aquesta base hi ha versions en castellà (`/es/…`)
i en anglès (`/en/…`) **només d'algunes pàgines**, no de totes. Això és una
decisió, no una feina a mitges.

## Per què no es tradueix tot

El site té 67 pàgines. Traduir-les totes serien 201 fitxers a mantenir
sincronitzats, i la major part no guanyaria res:

| Tier | Pàgines | Idiomes | Motiu |
|---|---|---|---|
| **1 · Entrada i conversió** | `/`, `/escoleta/`, `/campus/`, `/3x3/` | ca · es · en | Són les pàgines per on entra algú que encara no coneix el club, i on decideix. Una família castellanoparlant o una família internacional que arriba a Barcelona busca en el seu idioma. |
| **2 · Autoritat i contingut** | `/observatori/`, `/blog/`, `/briefing/`, `/grup-barna-dades-oficials/` | ca (es/en pendent) | Guanyarien amb el castellà; l'anglès només té sentit al briefing, que és el que cita la premsa. Encara no fet. |
| **3 · Deliberadament només català** | `/partits/`, `/partits/calendaris/`, `/premidonaesport/` (24 pàg.), galeries, `/jugadors/`, `/mascota/`, `/orgull/`, `/admin/` | ca | El calendari es regenera cada dia des de la FCBQ: traduir-lo trencaria el pipeline i ningú busca el calendari d'un club de barri en anglès. La recerca del Premi Dona i Esport es cita **com a recerca catalana**; traduir-la no li afegeix autoritat. Les galeries no tenen text que traduir. |

Si algun dia canvia el criteri, afegir la pàgina a `PAGES` dins de
`scripts/i18n.py` i executar el flux de sota.

## Com s'afegeix o s'actualitza una traducció

```bash
python3 scripts/i18n.py extract          # llegeix el català i actualitza els catàlegs
#   … omplir els buits a scripts/i18n/<slug>.json …
python3 scripts/i18n.py check            # què queda pendent
python3 scripts/i18n.py build            # genera /es/ i /en/
```

**Important:** el català és sempre l'original. Mai s'edita `es/` ni `en/`
a mà: es perdria al següent `build`. S'edita la pàgina catalana i es torna
a generar.

Les claus dels catàlegs són el text català literal. Si el català canvia, la
clau desapareix i `check` avisa que aquella cadena s'ha quedat sense traduir
— que és exactament el que volem que passi, en comptes de publicar una
traducció que ja no es correspon amb l'original.

### Casos especials, ja resolts

- **`_common.json`** — navegació, peu i etiquetes repetides. S'escriuen un cop
  i valen per a totes les pàgines.
- **JSON-LD** — es tradueix sol (`name`, `description`, `headline`…) i ajusta
  `inLanguage` i les URL a la versió idiomàtica.
- **Cadenes dins de `<script>`** — no es toquen mai per patró. Les úniques que
  es tradueixen són les de `JS_STRINGS` (el missatge de WhatsApp que munta el
  formulari), per literal exacte.
- **Enllaços de WhatsApp** — el text prellistat va en l'idioma de la pàgina
  (`WA_TEXT`).
- **Rutes relatives** — dins de `/es/` i `/en/` es converteixen en absolutes,
  incloses les `url()` del CSS incrustat.

## L'Escoleta té el seu propi generador

`/escoleta/` ve d'abans d'aquest motor i té una particularitat: el català i el
castellà convivien al mateix HTML amb un toggle. Es genera amb
`scripts/build_escoleta_i18n.py` a partir de `scripts/src/escoleta.source.html`.
El resultat és el mateix (tres URL amb hreflang recíproc).
