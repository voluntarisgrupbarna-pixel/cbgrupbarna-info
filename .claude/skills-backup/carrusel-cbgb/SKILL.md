---
name: carrusel-cbgb
description: >
  Playbook de CARRUSELS d'Instagram del CB Grup Barna: quan té sentit un
  carrusel (feed = marca, dosificat — el motor de captació és el reel, segons
  `crecimiento-ig-cbgb`), estructura slide a slide, formats provats del club i
  filtre de qualitat. Carregar SEMPRE que es pensi, dissenyi o avaluï un
  carrusel: "fes-me un carrusel de…", convocatòria/resultats de jornada, top
  fotos del partit, peça formativa "5 coses", història del club, recap de mes.
  NORMA OBLIGATÒRIA: cada carrusel porta DIVERSOS ganxos del banc estudiat de
  `ganxos-cbgb` (portada + re-ganxos entre slides) i un CTA explícit de
  creixement a l'última slide i al caption (segueix @cbgrupbarna +
  like/guarda/comparteix). Sense això, no es publica. Es produeix amb
  `produccio-cartells` i `disseny-cartells-cbgb`; valors de marca a
  `sistema-visual-cbgb`.
---

# carrusel-cbgb — Playbook de carrusels del CB Grup Barna

Font de criteri per als carrusels del feed. No redefineix marca (això és
`sistema-visual-cbgb`) ni com muntar la peça (això és `produccio-cartells`):
diu **quan fer un carrusel, com s'estructura perquè el swipe no mori, i què és
obligatori** perquè converteixi.

## El lloc del carrusel (context de `crecimiento-ig-cbgb`)

Els carrusels inflaven visualitzacions però **no portaven seguidors**: el motor
de captació és el **reel**. El carrusel NO desapareix — fa una altra feina:
**feed = marca i profunditat, dosificat** (~5 publicacions/setmana entre tot el
feed). Un bon carrusel és guardable i re-consultable: la seva mètrica reina és
**guardats**, no likes.

Quan SÍ carrusel: contingut seriat o llistable (5 coses, top fotos, cronologia,
abans/després), profunditat que no cap en un reel, i les peces d'"aparador" que
un desconegut mirarà al perfil (`aparador-perfil-cbgb`).

## Norma obligatòria — diversos ganxos + CTA a CADA carrusel

**Cap carrusel surt sense això.** Dues obligacions:

**1. DIVERSOS ganxos del banc estudiat (`ganxos-cbgb`):**

- **Slide 1 = ganxo verbal del banc de 8 fórmules**, ≤12 paraules, tipografia
  Anton + vermell Barna `#E63329`. La slide 1 és una PORTADA, no una foto amb
  logo: passa el test dels 3 segons (aposta + persona + promesa). Res de
  plantilla prestada ("Resum de la jornada" = mort).
- **Subhook a la slide 2** — puja la tensió i promet què hi ha si segueixes
  lliscant ("i la 7a foto no l'hauria de veure l'àrbitre").
- **Re-ganxo cada 2-3 slides** — una línia que reobre la tensió perquè el
  swipe no mori a mitja peça (mateixa lògica que la retenció d'un reel).
- La **primera línia del caption** repeteix el ganxo de la slide 1.

**2. CTA de creixement a l'ÚLTIMA slide + caption:**

- **Seguir (prioritari):** "Segueix @cbgrupbarna per [promesa concreta]" —
  escrit a l'última slide amb escut i handle, i repetit al caption.
- **Like / guarda / comparteix (secundari), amb motiu:** "Guarda-ho per abans
  del partit", "Doble tap si tu també hi eres", "Envia-ho a qui va fallar
  aquell tir". En carrusel, **guarda** és el CTA natural.

**Regla dura:** ganxos del banc ✚ CTA són **eliminatoris**. Si falten, no es
publica — es reescriu primer.

## Formats de carrusel provats del club

1. **"5 coses" formatiu** — fórmula #4 del banc ("És molt fàcil saber si…:
   només has de comprovar aquestes 5 coses"). El més guardable.
2. **Top fotos de la jornada** — 1 foto èpica per slide, ganxo a la 1a,
   re-ganxo a mitja peça. Variant tercera persona per fer-lo compartible.
3. **Convocatòria / resultats** — sèrie automàtica (`produccio-cartells`), però
   la slide 1 porta el "ganxo del dissabte" (què ens hi juguem), no "Resum J14".
4. **Cronologia / arxiu** — 60è aniversari, "d'on venim": fórmula #7 ("Sabies
   que…?").
5. **Abans/després** — evolució d'un/a jugador/a, del pavelló, del club.

## Filtre de qualitat — abans de dissenyar i abans de publicar

1. **Feina de feed:** és marca/profunditat guardable, o hauria de ser un reel?
2. **Slide 1:** frenaria el scroll d'un DESCONEGUT? (test dels 3 segons)
3. **Arc de swipe:** subhook a la 2 + re-ganxo cada 2-3 slides?
4. **Marca:** cada slide amb vermell Barna o escut (`sistema-visual-cbgb`)?
5. **Bilingüe:** CA/ES on toqui?
6. **Ganxos del banc (ELIMINATORI):** slide 1 + subhook + re-ganxos surten del
   banc de `ganxos-cbgb`?
7. **CTA de creixement (ELIMINATORI):** última slide + caption demanen seguir
   @cbgrupbarna amb promesa + like/guarda amb motiu?

Falla el 6 o el 7 → **no es publica**. La resta: si no supera 3 de 5,
reformular.

## Com encaixa

- `ganxos-cbgb` → el COPY de la slide 1, subhook i re-ganxos. Font única.
- `crecimiento-ig-cbgb` → per què el carrusel és marca i no motor de captació.
- `portada-reels-cbgb` → mateixa lògica de portada aplicada a la slide 1.
- `produccio-cartells` / `disseny-cartells-cbgb` → execució visual de les slides.
- `sistema-visual-cbgb` → tipografia, color, escut. No es redefineix res aquí.
- `aparador-perfil-cbgb` → els carrusels bons són candidats a "primers 9" i pins.
