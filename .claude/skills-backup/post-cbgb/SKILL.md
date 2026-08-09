---
name: post-cbgb
description: >
  Playbook del POST de feed (imatge única o foto + caption) del CB Grup Barna:
  quan un post és el format correcte (vs reel vs carrusel), anatomia de la
  imatge i del caption, i filtre de qualitat. Carregar SEMPRE que es publiqui o
  avaluï un post de feed: "fes-me un post de…", cartell de partit, resultat,
  MVP, aniversari, benvinguda de fitxatge, activació de sponsor, anunci.
  NORMA OBLIGATÒRIA: cada post porta DIVERSOS ganxos del banc estudiat de
  `ganxos-cbgb` (ròtul-ganxo a la imatge + ganxo a la primera línia del caption
  + subhook) i un CTA explícit de creixement (segueix @cbgrupbarna +
  like/guarda/comparteix). Sense això, no es publica. Es produeix amb
  `produccio-cartells` / `disseny-cartells-cbgb`; valors a `sistema-visual-cbgb`.
---

# post-cbgb — Playbook del post de feed del CB Grup Barna

Font de criteri per al post d'imatge única. No redefineix marca
(`sistema-visual-cbgb`) ni el disseny del cartell (`disseny-cartells-cbgb`):
diu **quan un post és el format correcte, què és obligatori que porti i com
s'escriu el caption** perquè no sigui "funcionariat amb logo".

## El lloc del post (context de `crecimiento-ig-cbgb`)

El feed és **marca, dosificat** (~5 publicacions/setmana en total): el motor de
captació és el reel. Un post de feed treballa per als que JA et miren i per al
desconegut que inspecciona el perfil (`aparador-perfil-cbgb`): els "primers 9"
són majoritàriament posts. Per això un post fluix no és neutre — **degrada
l'aparador**.

Quan SÍ post: cartell de convocatòria/resultat, MVP/jugada del dia, aniversari,
welcome de fitxatge, sponsor, anunci puntual. Quan NO: si la peça té moviment o
història → reel; si és llistable/seriat → carrusel.

## Norma obligatòria — diversos ganxos + CTA a CADA post

**Cap post surt sense això.** Dues obligacions:

**1. DIVERSOS ganxos del banc estudiat (`ganxos-cbgb`) — mínim 2, ideal 3:**

- **Ròtul-ganxo A LA IMATGE** — el titular del cartell surt del banc de 8
  fórmules, ≤12 paraules, Anton + vermell Barna `#E63329`. El cartell ES
  llegeix abans que el caption: si el ròtul és "Resum J14" o "Us hi esperem!",
  és mort (antipatró de plantilla prestada).
- **Ganxo a la PRIMERA LÍNIA del caption** — el caption es talla a ~1 línia i
  mitja: la primera frase és un ganxo del banc (pot ser el mateix que el ròtul
  o la variant en tercera persona per fer-lo compartible).
- **Subhook a la segona línia** — puja la tensió abans del "més" ("i sé que a
  algun pare no li agradarà").

- El **"ganxo del dissabte"**: en convocatòries i resultats, el titular és què
  ens hi juguem ("Una victòria i el cadet és a dalt"), mai el fet administratiu.

**2. CTA de creixement al final del caption (i al cartell quan toqui):**

- **Seguir (prioritari):** "Segueix @cbgrupbarna per [promesa concreta: viure
  el desenllaç / més bàsquet del Clot]."
- **Like / guarda / comparteix (secundari), amb motiu:** "Doble tap si hi
  eres", "Guarda la convocatòria", "Etiqueta qui ha de venir dissabte".
  L'etiqueta/compartit és or: posa el post davant de desconeguts.

**Regla dura:** ganxos del banc ✚ CTA són **eliminatoris**. Si falten, el post
no es publica — es reescriu primer.

## Anatomia del caption (ordre fix)

1. **Ganxo** (banc de `ganxos-cbgb`, ≤12 paraules)
2. **Subhook** (tensió)
3. **Cos breu** — el context que el cartell no diu (2-4 línies màx)
4. **CTA seguir** + CTA like/guarda/etiqueta amb motiu
5. **Hashtags** del club (bloc curt i estable) — mai abans del CTA

Bilingüe CA/ES segons peça i públic; el ganxo sempre en l'idioma de la
comunitat a qui apunta.

## Filtre de qualitat — abans de publicar

1. **Format correcte:** això no seria millor com a reel o carrusel?
2. **Cartell:** passa el filtre de `disseny-cartells-cbgb` (jerarquia, marca)?
3. **Marca:** vermell Barna o escut presents (`sistema-visual-cbgb`)?
4. **Aparador:** aquest post millora o degrada els "primers 9"?
5. **Veritat:** el ganxo és cert? (club amb famílies i menors: mai ganxo mentider)
6. **Ganxos del banc (ELIMINATORI):** ròtul + primera línia + subhook surten
   del banc de `ganxos-cbgb`?
7. **CTA de creixement (ELIMINATORI):** caption tanca amb segueix @cbgrupbarna
   amb promesa + like/guarda/etiqueta amb motiu?

Falla el 6 o el 7 → **no es publica**. La resta: si no supera 3 de 5,
reformular.

## Com encaixa

- `ganxos-cbgb` → font única del copy del ròtul, primera línia i subhook.
- `crecimiento-ig-cbgb` → per què el feed és marca i el CTA ataca la conversió.
- `disseny-cartells-cbgb` + `produccio-cartells` → disseny i fabricació del cartell.
- `sistema-visual-cbgb` → tipografia, color, escut.
- `aparador-perfil-cbgb` → els millors posts són candidats a pins i primers 9.
- `carrusel-cbgb` / `reels-cbgb` → germanes de format; mateixa norma de ganxos+CTA.
