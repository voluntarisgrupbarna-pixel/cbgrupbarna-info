# Multiidioma

La web és en català, castellà i anglès. Aquesta carpeta no conté cap pàgina:
conté el que fins ara no vivia enlloc i per això s'anava trencant sol.

El problema mai va ser traduir. Va ser que **res avisava quan una traducció es
quedava enrere**. Tocaves la pàgina catalana, no la castellana, i no passava
res —fins que algú se n'adonava mesos després. Per això la primera peça que
s'ha fet és la que se n'adona, no la que tradueix.

## Què hi ha

| Fitxer | Què és |
|---|---|
| `routes.yml` | Quina pàgina catalana correspon a quina castellana i a quina anglesa. El genera `scripts/i18n-routes.py` i **es pot editar a mà**: les edicions manen. |
| `diccionari.yml` | Els textos de la capçalera i el peu: una clau, tres idiomes. D'aquí els dibuixa `scripts/i18n_chrome.py`, que és el que fa servir el generador. |
| `etiquetes.yml` | El vocabulari tancat dels enllaços: com s'ha de dir cada secció en cada idioma. |
| `excepcions.yml` | Decisions preses, amb el motiu escrit: noms propis que no es tradueixen i paraules iguals en els tres idiomes. |
| `baseline.txt` | Els errors que ja hi havia el dia que es va activar el lint. La CI no s'atura per aquests; sí per qualsevol de nou. |

## Com es fa servir

```bash
python3 scripts/i18n-routes.py           # refresca el mapa quan hi ha pàgines noves
python3 scripts/i18n-lint.py             # informe: què està trencat i què està pendent
python3 scripts/i18n-aplica-etiquetes.py # posa els noms canònics a les pàgines
python3 scripts/i18n_chrome.py           # veure com queden capçalera i peu en cada idioma
```

El lint diu quins enllaços es diuen d'una manera que no toca i l'aplicador els
arregla: tots dos llegeixen `etiquetes.yml`, de manera que el vocabulari
s'escriu una vegada i des d'allà es comprova i s'aplica.

El lint separa dues coses que no s'han de barrejar:

- **Errors** — contradiccions. Un `hreflang` que apunta a una pàgina que no
  existeix, dues pàgines que no s'apunten l'una a l'altra, un `lang` que no
  correspon al directori, un enllaç amb un sinònim que el vocabulari dona per
  prohibit. Aturen la CI.
- **Pendents** — feina. Traduccions que falten, slugs sense traduir,
  traduccions més velles que el seu original. No aturen res: es prioritzen.

Quan s'arregla un error de `baseline.txt`, se n'esborra la línia. El fitxer
només pot minvar.

## D'on ve i cap a on va

La capçalera i el peu ja surten del diccionari: `scripts/build-pages.py` els
demana a `i18n_chrome.py` i el mateix codi en sap fer les tres versions. Els
`hreflang` i el commutador d'idioma encara s'escriuen a mà pàgina per pàgina;
`routes.yml` ja té tot el que necessiten per sortir d'aquí.

Això encara **no** està fet, i té un motiu. `scripts/build-pages.py` no es pot
executar sencer avui sense perdre contingut real (l'apartat de posicionament
de `/patrocinadors/`, la instantània SEO i els botons `.ics` de
`/partits/calendaris/`, paraules clau de `/campus/` i `/premsa/`). Fins que
això no es resolgui, la migració ha d'anar secció a secció mirant el `git
diff` sencer.

I `/blog/` tampoc estava tan al dia com semblava. Regenerar-lo hauria
esborrat tres coses que només eren a les pàgines publicades: el títol llarg de
la guia de campus, els seixanta-un anys del club —algú havia actualitzat la
xifra a la pàgina i no al generador— i un paràgraf amb l'enllaç a la
comparativa de campus de Barcelona. Ara aquestes tres coses són al generador i
`/blog/` es torna a poder regenerar sense perdre-hi res. **Abans de regenerar
qualsevol altra secció, cal fer aquesta mateixa comprovació**: generar,
comparar amb el que hi ha publicat i tornar al generador el que només visqui a
disc.

## Una cosa que no es toca: les URL

La guia del club diu que les **etiquetes** i els **enllaços** no admeten
sinònims: «Dies de partit», mai «Calendari». Els `<title>` i les descripcions
sí que poden portar termes de cerca. I les **URL es queden com estan**:
`/partits/calendaris/` no canvia de nom, perquè trencaria els enllaços
interns, el sitemap i els `.ics` que la gent ja té subscrits al mòbil. Ningú
llegeix una URL; tothom llegeix una etiqueta.
