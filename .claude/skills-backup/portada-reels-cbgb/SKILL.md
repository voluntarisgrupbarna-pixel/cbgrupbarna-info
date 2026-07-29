---
name: portada-reels-cbgb
description: "Portada (caratula) VERTICAL 9:16 dels reels del CBGB: la miniatura que decideix si un no-seguidor et segueix. Resol el coll d'ampolla de conversio (molt abast, pocs seguidors nous = problema d'aparador). Carregar sempre que es dissenyi la portada d'un reel, es planifiqui la graella, o es pregunti \"per que no converteixo tot i l'abast\". Usa sistema-visual-cbgb, es produeix amb produccio-cartells/disseny-cartells-cbgb, combina amb reels-cbgb."
---

# portada-reels-cbgb — La portada dels reels (la caràtula que converteix)

Font de criteri per a **la portada** del reel. No diu què gravar (`reels-cbgb`),
ni fixa els valors de marca (`sistema-visual-cbgb`), ni com editar
(`capcut-reels-cbgb` / `video-club-cbgb`). Diu **com ha de veure's la caràtula**
perquè converteixi abast en seguidors.

## La portada és VERTICAL (i per què importa)

- Es dissenya a **9:16, 1080×1920 — llenç sencer, vertical.** Mai quadrada.
- La graella del perfil pot **mostrar una retallada** (3:4 a la graella nova,
  1:1 a l'antiga), però això NO vol dir dissenyar quadrat: vol dir **dissenyar
  vertical i protegir el centre**. Si dissenyes quadrat, perds el 9:16 de la
  pestanya Reels i del feed.
- **Regla d'or: una portada vertical, amb el centre protegit** → serveix a totes
  les superfícies alhora.

## Per què la portada és LA palanca

El club té abast fort però converteix poc a seguidor: el coll d'ampolla és
**l'aparador** (el perfil i la graella que veu un no-seguidor quan l'abast l'hi
porta). La portada és **la miniatura que decideix si algú toca → mira → segueix**.
Una portada custom d'alta qualitat puja el click-through des d'Explora i de la
graella → més views → més senyal a l'algoritme. Aquest és el remei gràfic al
diagnòstic de conversió de `benchmark-clubs-barri-cbgb`.

## La idea que no es pot oblidar

1. **Aparador, no fotograma.** Mai el primer frame ni un a l'atzar (surt borrós,
   a mig moviment, no comunica). És una miniatura DISSENYADA que: (a) es llegeix
   a ~300px, (b) respecta la zona segura central, (c) sembla de la mateixa mà que
   les caselles del voltant.
2. **La graella és la primera impressió** d'un no-seguidor. El que converteix és
   la **coherència** (mateix sistema, mateixa estètica). Una portada preciosa en
   una graella caòtica no converteix ningú.

## Les 3 retallades (per què el centre mana)

Una sola portada, tres retallades:

- **Pestanya Reels:** 9:16 sencer (1080×1920).
- **Feed:** retallat a 4:5 → es perden ~285px dalt i ~285px baix.
- **Graella:** 3:4 (nova) o 1:1 (antiga) → torna a tallar dalt i baix.

L'única zona garantida a TOTES és el **CENTRE**: títol, cara, logo i CTA sempre
**al centre vertical**. Píxels exactes i mapa de zones → `references/especificacions-portada.md`.

## La portada bona — recepta

- **Llenç:** 1080×1920 (9:16), vertical. Dissenya al llenç sencer, **protegeix el
  centre**.
- **Zona segura:** títol/cara/logo dins del centre **~1080×1350**; per anar sobre
  segur amb comptes de graella 1:1, dins del centre **1080×1080**. Res crític al
  top ~285px ni al bottom ~285px.
- **Text: 3-5 paraules MÀXIM, una idea.** Display condensada gegant en majúscules
  (Anton / Bebas Neue / Oswald, segons `sistema-visual-cbgb`). **Legible a 300px:**
  si a mida de miniatura no es llegeix, menys paraules i més grans.
- **Contrast fort:** fons de color pla de marca + retall net del protagonista a
  alt contrast (efecte pòster NBA de `sistema-visual-cbgb`). Res de degradats
  tous ni fons enfeinat darrere de text petit.
- **Protagonista al centre:** una cara/gest amb qui projectar-se o admirar (com
  "l'estrella ÉS el contingut" de `reels-cbgb`).
- **Marca exacta:** colors i tipografies de tokens.conf. Logo en posició constant
  i **al centre vertical, mai a una cantonada** (les cantonades les menja la
  graella).
- **Sempre custom:** puja SEMPRE portada pròpia, mai el frame automàtic.
- **Cross-plataforma:** la mateixa portada vertical val per a TikTok i Shorts.

## La graella com a aparador (aquí es guanya la conversió)

- **Dissenya la GRAELLA, no només portades soltes:** pensa les properes 9
  caselles com un conjunt abans de publicar.
- **Un "look" dominant per a ≥80% de les portades.** La varietat mata el
  reconeixement. Coherència de sistema, tipografia i posició de logo; opcional un
  **ritme de color** (alternar negre de marca / vermell / foto) perquè es llegeixi
  intencional.
- **Pots actualitzar portades antigues** per refrescar la graella SENSE tornar a
  publicar el reel → eina per arreglar l'aparador de manera retroactiva.

## Catàleg de portades del club

Cada contingut habitual, resolt com a portada amb el mateix sistema:

- **Fitxatge / renovació:** retall del jugador/a sobre color pla, nom gegant,
  etiqueta "FITXATGE" / "SEGUEIX". (Ritual: `luxury-logic-cbgb`, `codis-lux-cbgb`.)
- **Prèvia de partit:** rival + data, "VS" gegant, escut.
- **Resultat:** marcador com a targeta de dada, èmfasi al guanyador.
- **MVP / jugada:** cara + "MVP" + número.
- **Campus / esdeveniment (3x3):** nom gegant, data, lockup de logo.
- **Sèrie de contingut** ("Tip de…", "Reaction…"): plantilla constant perquè la
  sèrie es reconegui d'un cop d'ull a la graella.

Totes: mateix sistema, text al centre, ≤5 paraules, legibles a 300px.
(Producció de plantilles: `produccio-cartells`; criteri gràfic: `disseny-cartells-cbgb`.)

## Filtre de qualitat — abans de publicar

1. **Legible a 300px?** Comprova-ho a mida de miniatura (zoom ~25% o mirant la
   graella). Si no es llegeix → menys paraules, més grans.
2. **Zona segura?** Títol/cara/logo dins del centre; res crític dalt/baix on la
   graella retalla.
3. **≤5 paraules, una idea?**
4. **Marca exacta?** Colors i tipografies de tokens.conf; **es reconeix com a
   Barna sense veure el logo?**
5. **Encaixa a la graella?** Al costat de les 8 caselles veïnes, sembla la mateixa
   mà?
6. **Portada custom vertical (no fotograma, no quadrada)?**

Si falla **2 o més**, refer abans de publicar. La inconsistència és el que més
rebaixa el nivell percebut (mateix esperit que `sistema-visual-cbgb`).

## Com fer-la servir (flux)

- **Abans de muntar un reel:** decideix PRIMER la portada (és l'aparador) i
  després grava/edita per servir-la.
- **Abans d'una tanda:** planifica les 9 caselles juntes, un sol look.
- **Valors exactes:** `sistema-visual-cbgb` (tokens.conf).
- **Produir la portada:** `produccio-cartells` (plantilla Canva/Figma o per codi)
  aplicant `disseny-cartells-cbgb`; després pujar-la com a **portada custom** del
  reel.
- **Grafisme dins del reel** (rètols, subtítols, targetes): `reels-cbgb` /
  `capcut-reels-cbgb`.
- **Angle nou/avançat:** `ana-innovacio-barna`.

## Advertència sobre les dades tècniques

El comportament de retallada i les zones segures d'Instagram **canvien** (la
graella ha passat a 3:4/4:5 i es va ajustant). Els píxels exactes viuen a
`references/especificacions-portada.md`; abans d'un rollout gran, comprova la
retallada actual dins de l'app. Dades recollides el juliol de 2026.
