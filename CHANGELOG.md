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

## 2.2.0 — 2026-08-29

**Grups privats amb enllaç propi a la galeria.** Fins ara un àlbum marcat com a
privat des de `/fotos/admin.html` només el podia veure qui tingués la clau
mestra de màrqueting, que obre tots els grups alhora: no hi havia manera de
donar un àlbum a un equip o a una família sense donar-los-ho tot. Ara cada grup
privat neix amb la seva clau (`access_key` a `fotos/events.js`) i el seu enllaç
—`/fotos/?clau=<clau>#<grup>`—, que obre aquell grup i cap altre. El panell el
genera en fer privat l'àlbum, el mostra en un quadre amb botó de copiar i en pot
generar un de nou si l'enllaç es filtra. La clau mestra segueix obrint-los tots
i ara s'edita des de la configuració del panell.

Dues coses més que hi anaven de la mà. Les galeries en castellà i anglès
(`/es/fotos/` i `/en/fotos/`) no havien rebut mai el filtre de privacitat: els
grups privats hi sortien al llistat, als comptadors i als filtres de temporada.
Ja no. I desar la configuració des del panell esborrava del `config.js` la clau
de màrqueting i les dues adreces d'R2, que el formulari no editava però tampoc
tornava a escriure; ara les conserva.

**El que això protegeix i el que no.** La web és estàtica i no hi ha cap
servidor que validi res: és un enllaç **no llistat**, no un mur amb
contrasenya. Treu el grup de la galeria per a qui no en tingui l'enllaç, però
els fitxers segueixen vivint en URL públiques i qui ja tingui l'adreça d'una
foto hi arribarà igualment. Ho diu el mateix panell en generar la clau.

---

## 2.1.0 — 2026-08-29

**Els cinc punts «purament tècnics» del tauler de pendents.** Tres pàgines
noves en tres idiomes —`/palmares/`, `/avantatges-familia/`, `/video/`—, un
arreglo del generador de pàgines i del seu diccionari compartit (`css/a11y.css`,
`js/mapa.js` i el giny de WhatsApp que faltaven a `head()`; el peu amb l'enllaç
vell a `/basquet-femeni/` i sense Newsletter ni Bústia), i set arreglos
d'accessibilitat a l'app `galeria/` (botons i enllaços amb icona que només
tenien `title`, o cap atribut). Detall complet a `PENDENTS-WEB.md`,
«29-08-2026 — Els cinc punts "purament tècnics", fets».

---

## 2.0.0 — 2026-08-27

**Decisió de l'Ana: una sola portada, sense commutador.** Fora el
Franges/Extensa: la portada de les tres llengües es queda amb la vista de
franges tal com es publicava per defecte —el hero de dues columnes, les nou
franges i la barra `#SOMCLOT`—, i desapareix del tot la vista extensa amb el
seu botó de commutador. És un canvi MAJOR perquè altera com es fa servir la
web (una sola maquetació de portada, no dues intercanviables).

Es tanca així, per decisió i no per dada, el pendent P2.7 («mesurar l'ús del
commutador amb GA4 abans de decidir res»): els secrets de GA4 no s'han arribat
a donar d'alta, així que mai hi ha hagut cap xifra real d'ús — l'Ana ha
decidit sense esperar-la.

Fora de les tres portades (`index.html`, `es/index.html`, `en/index.html`):

- El `.masthead` fosc («Qui som»), que només sortia a l'extensa i repetia el
  hero de franges.
- El calendari encastat (`#calendari` / `.e-jornada`, únicament a la
  catalana — la castellana i l'anglesa el tenien com a secció normal, sense
  commutador, i es queden igual: no formava part del sistema de vistes).
- Els blocs editorials «Paritat», «Cultura del Progrés», «El Barna per dins»
  i «Observatori Barna».
- La secció `#acces` («Tot a mà», llista plana d'enllaços) i `#presentacions`:
  tot el que hi enllaçaven ja és al mapa ≡ o a pàgines pròpies
  (`/presentacions/`, `/briefing/`, `/posicionament/`).
- El botó `.view-toggle` de la capçalera i tot el JS del commutador
  (`sessionStorage`, l'esdeveniment `canvi_vista`, el `data-view` a `<html>`).

Es queden intactes: les nou franges, el hero, la barra `#SOMCLOT`, el
formulari, la FAQ i tot el contingut que ja era comú a les dues vistes.
Verificat amb `i18n-paritat.py`, `i18n-contingut.py`, `i18n-lint.py`,
`a11y-revisa.py` i `pes-pressupost.py` en verd, i Playwright a 1280/390 px
als tres idiomes.

---
## 1.5.3 — 2026-08-28

**El panell `/admin/` ja deixa entrar.** `GOOGLE_CLIENT_ID` posat a
`admin/config.js` amb un client OAuth dedicat («CB Grup Barna Admin»,
orígens `cbgrupbarna.info`/`www.cbgrupbarna.info`) creat expressament —
no s'ha reutilitzat un client existent d'una altra app que hauria fet
fallar el login per origen incorrecte. Treure el duplicat de
`marqueting@cbgrupbarna.info` a `ALLOWED_EMAILS`.

Pendent d'un pas de l'Ana a Cloud Console: donar d'alta els comptes com a
«Test users» a la pantalla de consentiment (l'app hi és en mode Prova),
o el login es bloquejarà igualment. Detall a `PENDENTS-WEB.md`.

## 1.5.2 — 2026-08-28

**Decisió de l'Ana: cap eina externa d'enviament per al butlletí — tot a
Sheets, com la resta de formularis del web.** La newsletter ja no diu que
l'enviament es fa amb Brevo (no s'havia arribat a activar mai: l'`action`
sempre havia estat buit). S'ha tret l'opció sencera del codi en comptes de
deixar-la a mig fer:

- `js/canals.js` i `js/newsletter.js`: fora `brevoAction`/`brevoCamps` i la
  branca que els feia servir. Les altes ja anaven, per defecte, a la full
  de càlcul compartida (`bustiaEndpoint`, `source: 'newsletter-web'`) —
  ara és l'únic camí, no un pedaç mentre s'esperava la URL de Brevo.
- `/newsletter/` (ca/es/en): el paràgraf que citava Brevo per nom ara diu
  la veritat — full de càlcul del club a Google Drive.
- `/politica-de-privacitat/` (ca/es/en): secció «Newsletter» nova, amb la
  mateixa base jurídica i redactat que la resta de formularis. No hi havia
  cap secció pròpia per a aquesta pàgina i calia una, ara que es corregeix
  el que deia la pàgina mateixa.

## 1.5.1 — 2026-08-27

**Reconciliació de dues tandes paral·leles** (aquesta branca ↔ el PR #103
de la maqueta). En fusionar ha manat el que ja era a `main` on les dues
tandes tocaven el mateix amb intencions diferents, i s'hi ha sumat el que
només tenia aquesta branca:

- **Mana la maqueta**: el menú vell de les portades surt del marcatge (la
  decisió de conservar-lo queda revocada pel PR), i la banda #SOMCLOT es
  queda al seu lloc convertida en crida cap al formulari («Vols
  informació? ↓») — la reubicació davant del peu d'aquesta branca es
  descarta perquè resolia el mateix problema.
- **Se suma d'aquesta branca**: la rotació del hero de l'Escoleta, el logo
  de capçalera a mida, l'esdeveniment `canvi_vista`, la neteja COMPLETA
  d'/escoleta/ (la de la maqueta deixava els atributs i el CSS del
  commutador), els alts redactats a mà de la galeria amb tota la seva
  maquinària, i el cas «carregant/error» del cercador que la maqueta no
  cobria.

---

## 1.5.0 — 2026-08-27

**Textos alternatius reals a la galeria** — la fase final de l'apartat:

- **141 fotos amb alt redactat a mà, en els tres idiomes** (423 textos):
  l'àlbum de l'Escola de Bàsquet – Julio Torralba (91) i la visita de
  l'alcalde Collboni (50), mirades una a una. Les 1.900 restants segueixen
  amb l'alt contextual automàtic (àlbum + posició), també trilingüe.
- **El pujador d'admin ja demana la descripció**: camp opcional per foto a
  la cua de pujada; es desa a `ev.alts` i el generador la conserva entre
  execucions. Les fotos noves poden néixer descrites.
- **Cada idioma llegeix el seu alt**: `alts` (ca), `alts_es`, `alts_en`,
  amb el català de reserva.
- **Els enllaços directes a un àlbum ja funcionen en castellà i anglès**:
  les galeries `/es/` i `/en/` no obrien l'àlbum del `#id` de l'adreça
  (la funció només existia en català). Portada a totes dues.

---

## 1.4.1 — 2026-08-26

**Barrido «todo lo que sea código» del tablón de pendientes:**

- **Zapic fora de les tires de partners** de la presentació i el dossier de
  patrocinis (6 pàgines, ca/es/en) i el seu logo fora del repositori: la
  baixa estava decidida des del 14/08 i les pàgines encara l'ensenyaven.
- **P2.6** — la tira #SOMCLOT deixa de fer de fals final de pàgina a la
  vista franges: ara és l'últim bloc abans del peu real, a les tres portades.
- **P2.7** — el commutador Franges/Extensa ja es mesura: esdeveniment
  `canvi_vista` a GA4 a cada canvi, per decidir amb dades.
- **P3 (logo)** — la capçalera de les tres portades servia l'escut de
  226×300 px per a una casella de 32: ara va `img/logo-head.png` (48×64,
  8 KB, també al preload). El `logo.png` gran queda per a les icones.
- **Neteja d'/escoleta/**: fora els 113 elements de castellà ocult
  (`data-lang="es"`), l'atribut `data-lang` i el JS del commutador antic.
  El castellà viu només a /es/escoleta/. Cap text català tocat.
- **P3 (menú vell): decisió, no oblit** — el `nav#menu` ocult de les
  portades NO es treu: el codi ja registrava «queda al marcatge per si es
  recupera» i són ~30 enllaços interns servits que els cercadors llegeixen.

---

## 1.4.0 — 2026-08-26

**El bloc de codi del camí cap al 10** (accessibilitat, rendiment, estètica):

- **Galeria amb alts reals**: cada foto diu l'àlbum i la posició («Escoleta
  amb Julio Torralba — foto 3 de 91») a la casella, al botó i al visor, en
  els tres idiomes; si un àlbum porta descripcions per foto (`ev.alts`),
  manen aquestes. Els `src` buits del visor ja no re-demanen la pàgina.
- **El cercador sense resultats ja no és un listbox buit** (l'últim avís
  d'axe-core que quedava, a /cerca/ i el 404 dels tres idiomes).
- **Els 4 PDF grans, comprimits** amb Title i Lang conservats: 12,6 MB → 6,2
  MB en total; pesos actualitzats als enllaços. A les pàgines dels 3 PDF
  sense arbre d'etiquetes, nota visible i aria dient que la versió
  accessible és la mateixa pàgina.
- **Hero de l'Escoleta amb 4 fotos reals** de l'àlbum d'estudi (1772×2362,
  retall 3:4 des de dalt, 600/1200 px sense ampliar), en rotació diària a
  les tres portades. Provat amb navegador a 1280 i 390 px.
- **Pressupost de pes a CI** (`scripts/pes-pressupost.py` +
  `pes-pressupost.yml`): cap fitxer servit per sobre del sostre del seu
  tipus; excepcions amb motiu obligatori a `pes-excepcions.txt`.
- **Panell d'analítica** a `/admin/analitica/`: workflow diari que baixa 28
  dies de la GA4 Data API a `dades.json` i panell estàtic darrere la porta
  de l'admin. Sense els dos secrets (pendents de l'Ana) no falla: explica
  què falta.
- **L'app de galeria** (Next.js) passa la mateixa revisió que /fotos/:
  caselles amb teclat i botons d'icona amb nom. Type-check en verd.

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
