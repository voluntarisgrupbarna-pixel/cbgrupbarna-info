# Versions · cbgrupbarna.info

Aquest repositori no tenia cap manera de dir «això és el que hi havia
publicat en tal data» més enllà del missatge de cada commit. A partir
d'aquí sí: cada versió és un punt fix del codi, amb el número escrit al
fitxer `VERSION` i explicat aquí.

**Com es numera.** `MAJOR.MENOR.PEDAÇ`, a l'estil habitual:

- **PEDAÇ** (1.0.**1**) — un arreglo o un contingut nou que no canvia com
  funciona res: una resposta del cercador, una traducció, una foto.
- **MENOR** (1.**1**.0) — una funcionalitat nova que s'afegeix sense
  trencar la que ja hi havia: el formulari de «no ho sabem», una secció
  nova.
- **MAJOR** (**2**.0.0) — un canvi que altera com es fa servir la web o
  com es treballa amb el repositori.

**Com es fa una versió nova.** S'actualitza `VERSION`, s'hi afegeix
l'entrada a dalt de tot d'aquest fitxer amb la data i el resum, i es
puja a `main` en el mateix commit. La versió és el commit; el número
només l'hi posa nom.

---

## 1.1.2 — 2026-08-25

El robot diari de la FCBQ portava **dos dies mort** (runs #123-135, tots en
vermell des del 23/08 a les 15:16) i la fallada, de retruc, protegia una
regressió: en arreglar-lo sense mirar més, l'endemà hauria esborrat millores
de 45 pàgines publicades.

- **Causa de la fallada:** `generate-team-pages.py` carrega
  `scripts/i18n_chrome.py`, que fa `import yaml`, i el workflow només
  instal·lava `pillow`. Afegit `pyyaml` a `update-partits.yml`.
- **La regressió que hauria vingut després:** el generador de fitxes d'equip
  anava per darrere de les pàgines publicades — no emetia els `hreflang`,
  ni el selector d'idioma, ni `css/a11y.css`. Actualitzat el generador
  perquè ho emeti tot; ara la seva sortida coincideix amb el publicat i
  hi afegeix el que faltava a `/es/` i `/en/`.
- **El peu de les fitxes**, via `i18n/diccionari.yml`: Newsletter, Bústia de
  suggeriments i Preguntes freqüents a la columna Contacte dels tres
  idiomes (abans només al català, i a `/es/partits/` sortien en català).
- **El traductor de `/partits/`** apren «Accessibilitat» i «Bústia de
  suggeriments»: les versions castellana i anglesa ja no ensenyen aquests
  dos rètols en català.
- Regenerades les 48 pàgines d'equip, `/es/partits/` i `/en/partits/` (que
  arrosegaven les FAQ amb restes de català del fix #86 mai aplicat pel
  robot mort) i l'índex del cercador.

Comprovat: axe 0 violacions a les fitxes dels tres idiomes a 390 px,
`a11y-revisa` 458/458, lint i18n 0, motor 74/74.

## 1.1.1 — 2026-08-25

El cercador, net d'ARIA inventada i amb el panell que ja no es desborda.

- **El patró combobox/listbox era invàlid** (axe: `aria-required-children`,
  crític, en tots els estats): el panell barreja resposta, resultats,
  formulari i suggeriments, i cap listbox pot descriure això sense mentir.
  Ara les fletxes mouen el **focus real** entre els resultats (avall entra i
  baixa amb volta, amunt torna cap al camp), el lector de pantalla llegeix
  cada enllaç pel que és, i el panell és una regió amb nom. La suite de UX
  codifica el patró nou (57 proves).
- **Els resultats de la capa es pintaven damunt del vel.** `.cerca-motor` no
  tenia CSS: el panell (max-height 86vh) no repartia l'alçada i el
  contingut es desbordava per sota, gris sobre fosc a 1,37:1. Amb
  `min-height: 0` al motor i al cos, el panell recorta i el cos fa scroll.
- Resultat: **0 violacions axe** (WCAG 2.x A/AA) a `/cerca/`, `/es/busqueda/`,
  `/en/search/`, `/404.html` i a la capa, en els tres estats. Motor 74/74 ·
  contingut 95/95 · ux 57/57.

També: `/accessibilitat/` donada d'alta a `i18n/routes.yml` (no hi era) i
corregit un fals positiu de l'auditoria del 25/08 a `PENDENTS-WEB.md`.

## 1.1.0 — 2026-08-24

Accessibilitat: `css/a11y.css`, capa compartida a les 458 pàgines (focus
visible, salt al contingut, moviment reduït, alt contrast del sistema).
Nova secció **`/accessibilitat/`** (+ `/es/accesibilidad/`,
`/en/accessibility/`), enllaçada des del peu de tot el lloc, amb l'estat
real de conformitat WCAG 2.2 AA. Contrast corregit a l'engròs allà on
l'auditoria d'UX (#78) no havia arribat; menús amb `aria-expanded`; PDF amb
`/Title` i `/Lang`; vídeo d'`/opina/` amb subtítols obligatoris abans de
poder-se activar mai.

Resultat mesurat amb axe-core: 0 violacions WCAG 2.0/2.1/2.2 A i AA a les
458 pàgines servides.

---

## 1.0.2 — 2026-08-24

Confirmat i documentat a `PENDENTS-WEB.md`: a partir d'ara cada feina
tancada puja la seva subversió sense que calgui demanar-ho cada cop. Cap
canvi de codi.

## 1.0.1 — 2026-08-24

Documentat a `PENDENTS-WEB.md` que aquest sistema de versions existeix i per
què és un fitxer i no un tag de git. Cap canvi de codi.

## 1.0.0 — 2026-08-24

Primera versió fixada. Marca l'estat del repositori just després de
publicar el cercador intel·ligent del web: FAQ trilingüe des d'una font
única (`i18n/faq.yml`), motor de cerca amb tolerància a faltes i
sinònims, i un formulari de contacte quan no hi ha resposta escrita.

Commit: `205f0861`

Comprovacions en aquell moment: motor 74/74 · contingut 95/95 · ux
56/56 · i18n-lint 0 errors · paritat de tres idiomes correcta.
