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

## 1.3.2 — 2026-08-26

**Auditoria de rendiment, SEO, GEO i contingut** sobre les 408 pàgines, i els
arreglos que en surten. Rendiment: `js/galetes.js` passa a `defer` a les 382
pàgines i als tres generadors (deixa de bloquejar el primer dibuix; el
consentiment i l'RGPD queden igual, verificat amb navegador real); els heros i
targetes del blog passen de JPG a WebP (−34% de pes) i el hero d'article deixa
el `loading="lazy"` per `fetchpriority="high"` perquè és l'LCP; 604 imatges
reben `width`/`height` per no moure la pàgina mentre carreguen. SEO: es
completen les **84 meta descriptions que acabaven tallades amb «…»** (ara
frases senceres de ≤165 caràcters, també als JSON de `i18n/feina/` perquè cap
`munta` les reverteixi); vuit `og:image` de /es/ i /en/ apuntaven a fitxers
inexistents i ara apunten a l'actiu real; la portada deixa de tenir dos `h1`
(el del masthead passa a `p`, mateixa classe); i s'escurcen els títols i
descripcions més llargs (campus, empreses, 3x3, briefing i blog, als tres
idiomes). Les fitxes de fotos del 3x3 en castellà i anglès recuperen el
JSON-LD que només tenia la catalana. Sitemap, enllaços interns, hreflang i
paritat i18n: comprovats, cap error.

## 1.3.1 — 2026-08-25

**Prova d'UX** sobre 16 pàgines × 2 amples amb navegador real, i els arreglos
que en surten: el botó ≡ passa a flotant tot sol quan una capçalera ja anava
plena i el feia vessar (/partits/ i /portes-obertes/ a 1280); cap foto es
mostra més gran que el fitxer (marc limitat a /escoleta/ als tres idiomes,
`srcset` amb el @2x a la foto de /femeni/, i `sizes` corregits al hero de
/patrocinadors/ —servia el fitxer de 800 en un marc de 1120— i a la franja de
la portada).

## 1.3.0 — 2026-08-25

**L'estètica definitiva, completa.** Les tres peces que quedaven del document
del 25 d'agost: el **botó ≡** amb el mapa de navegació complet a totes les
capçaleres (377 pàgines més; component autocontingut `js/mapa.js` generat des
de `i18n/routes.yml`); els **panells de la portada** —«Entrenaments» amb els
horaris reals de l'Escoleta i «Descarrega el full (PDF)» amb el flyer nou per
la porta de descàrrega existent, amb casella de butlletí—; i els **sèniors**
pugen a dalt de la portada, per sobre del formulari, amb l'eyebrow a la
temporada 26·27.

## 1.2.1 — 2026-08-25

La tanda de decisions de l'Ana del mateix dia, executades: l'edat de
l'Escoleta unificada a **4-8 anys** a les 484 pàgines (dues el contradeien
amb 4-7); `/premsa/moments/` traduïda —neixen `/es/premsa/momentos/` i
`/en/premsa/highlights/`, 38 entrades per idioma—; el **briefing** refet per
a la temporada 2026-27 amb les xifres quadrades amb `data.json` (fora les
«~2M d'impressions» injustificables, dins les 439.000 visualitzacions del
panell verificat); i el **flyer nou de l'Escoleta** (A5 a 300 ppp, PNG i
PDF a `escoleta/flyer/`), amb foto real de la galeria i l'estètica
definitiva.

## 1.2.0 — 2026-08-25

**L'estètica definitiva.** S'aplica el document tancat del 25 d'agost a tot
el lloc: **desapareix la crema** `#F4F1EC` —totes les superfícies clares
passen a blanc pur, el del logo— i entra el **groc** `#EEFF00` amb regla
escrita: sempre a la lletra, mai al fons, i només als dos punts d'entrada a
la campanya d'Escoleta (el ticker, ara enllaç, i el seu CTA). 179 fitxers
passats per `aplica-estetica.py`, que des d'ara tradueix qualsevol crema a
blanc. De retruc, el vermell de l'escut passa de 4,36:1 a 4,92:1 de
contrast sobre les superfícies clares i entra a l'AA sense ajudes.

## 1.1.3 — 2026-08-25

`PENDENTS-WEB.md` posat al dia: registrat el fet i el pendent de la icona a
l'enllaç d'accessibilitat del peu (1.1.2), amb la resposta a per què no hi
ha logo oficial de «web accessible».

## 1.1.2 — 2026-08-25

L'enllaç «Accessibilitat» del peu (i el seu equivalent en castellà i
anglès) ara porta una icona i el nivell de conformitat visible:
«♿ Accessibilitat — WCAG 2.2 AA». No hi ha cap logo oficial de web
accessible que certificar-se pugui; el que fa falta és que la declaració
enllaçada es vegi sense haver de clicar-hi, i ara es veu.

## 1.1.1 — 2026-08-24

Primera tanda de codi del «Camí cap al 10» (auditoria d'estètica i de la
resta d'apartats): els preus del campus (195/160/150 €) ja no es publiquen
enlloc —a totes les pàgines en ca/es/en, el generador `build-campus-fitxa.py`
i totes les dades estructurades—, la política de privacitat declara
Formspree com a encarregat del tractament, i `/jugadors/` porta `noindex`
mentre no tingui plantilla. `PENDENTS-WEB.md` actualitzat marcant les tres
accions com a fetes.

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
