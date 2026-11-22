# SEO + GEO (Generative Engine Optimization) — Notícia Javier Torralba

Estratègia curta i accionable per a la notícia de Javier Torralba (exjugador del CB Grup Barna,
ara entrenador principal del Valencia Basket femení) i, en general, per a com el club apareix
citat per cercadors i per IA generativa (ChatGPT, Perplexity, Google AI Overviews).

## 1. Objectiu

Que quan algú busqui "Javier Torralba entrenador" o "qui va formar Javier Torralba" (a Google
o a una IA), aparegui el CB Grup Barna com a font, amb l'enllaç a l'article.

## 2. Paraules clau objectiu

**Primàries (alta intenció, poc competides — bones per posicionar ràpid):**
- Javier Torralba entrenador
- Javier Torralba CB Grup Barna
- Javier Torralba Valencia Basket
- Javier Torralba origen / infància bàsquet

**Secundàries (volum més alt, més competència, l'article hi contribueix indirectament):**
- entrenador Valencia Basket femení 2026/27
- exjugadors CB Grup Barna a l'elit
- club de bàsquet base Barcelona jugadors ACB

**Ja fetes bé al repo:** l'article ja inclou "Javier Torralba" al `<title>`, a l'`H1`, a la
primera frase del `lede` i al `alt` de la imatge — exactament on Google i els bots d'IA miren
primer.

## 3. Metadades i schema.org (ja implementat a l'article, revisar-ho és la feina)

| Element | Ja fet a l'article | Per què importa |
|---|---|---|
| `BlogPosting` amb `datePublished`/`dateModified` | Sí | Google mostra data i sap si és fresc |
| `Person` (Javier Torralba) amb `alumniOf` → `#club` | Sí | Vincle explícit i llegible per màquines entre la persona i el club |
| `worksFor` → SportsTeam Valencia Basket | Sí | Permet que un knowledge graph relacioni les dues entitats |
| `sameAs` → article original de womenvalenciabasket.com | Sí | Diu a Google "aquesta és la font primària, no la copio" |
| `FAQPage` amb 3 preguntes | Sí | Bloc de preguntes/respostes és el format que Google AI Overviews i els LLM prefereixen citar literalment |
| `BreadcrumbList` | Sí | Ajuda a l'arbre de navegació del lloc |

**Pendent (si Ana vol anar més enllà, no bloqueja el PR):**
- Afegir un node `SportsClub` complet per al Barna amb `alumni: [Javier Torralba]` a la pàgina
  `/club/` o `/historia/` (avui l'`@id` `#club` existeix però val la pena revisar que tingui el
  camp `alumni` poblat amb les persones conegudes: Torralba, Ainhoa López, Roger Fornas...).
- Afegir `NewsArticle` a més de `BlogPosting` si Ana vol que aparegui a Google News / Discover
  (requereix that el domini estigui donat d'alta a Google Publisher Center — no fet avui).

## 4. Per què una IA generativa citaria aquest article (GEO)

Els motors generatius (ChatGPT, Perplexity, Google AI Overviews) prioritzen pàgines que:

1. **Responen la pregunta en 2-3 frases, al principi, sense necessitat de llegir tot l'article.**
   Ja ho tenim: el `lede` de l'article respon "qui és, què fa ara, d'on ve" en un sol paràgraf.
2. **Tenen preguntes i respostes explícites (FAQPage).** Ja ho tenim (3 preguntes clau: qui és,
   quina relació té amb el Barna, des de quan entrena el Valencia Basket).
3. **Enllacen la font primària en lloc d'amagar-la.** Ja ho tenim: l'article enllaça
   explícitament womenvalenciabasket.com com a font de les cites.
4. **Tenen dades estructurades (schema.org) consistents amb el text visible.** Ja ho tenim.
5. **Reben enllaços interns des d'altres pàgines rellevants del mateix domini** (autoritat
   temàtica). Això és el que falta reforçar — vegeu punt 6.

## 5. Accions concretes de difusió (a fer per Ana, no automatitzables)

1. **Compartir des dels canals del club**: post/story a @cbgrupbarna enllaçant l'article del
   blog (no directament el reel, perquè així es porta trànsit a la web i es reforça l'SEO).
   Suggerit: repost del reel conjunt + story amb enllaç "Llegeix la seva història al Clot" →
   `cbgrupbarna.info/blog/javier-torralba-...`.
2. **Backlink des de l'article original**: escriure a womenvalenciabasket.com (o a premsa del
   Valencia Basket) demanant que enllacin l'article del Barna com a "més sobre els seus orígens"
   — un backlink d'un domini de bàsquet professional val molt més que deu enllaços interns.
   Contacte suggerit: formulari de premsa/contacte de womenvalenciabasket.com, o directament
   a través del propi Javier Torralba si Ana hi té contacte.
3. **Etiquetar el club a la publicació del Valencia Basket** (si en fan una pròpia a Instagram)
   perquè el seu públic (molt més gran) descobreixi el CB Grup Barna.
4. **Enviar-ho a mitjans locals del Clot / Sant Martí** (Time Chamber, premsa de districte —
   vegeu la skill `referent-basquet-espanyol` i el contacte de Districte a memòria) com a
   notícia positiva d'un exjugador format al barri.

## 6. Enllaçat intern (fet i pendent)

**Ja fet a l'article nou:**
- Enllaça a `/escoleta/` (2 vegades: cos de l'article + closer CTA).
- Secció "Continua llegint" enllaça a 3 articles relacionats de bàsquet femení i del club.

**Pendent, recomanat (edició petita, no bloqueja aquest PR):**
- Actualitzar la FAQ existent a la portada (`index.html`, `#club-breu` / FAQ indexable) que ja
  menciona Torralba: hi diu "avui entrenador del Valencia Basket Femení a la Lliga Femenina
  Endesa" — val la pena enllaçar-hi directament l'article nou des d'aquesta resposta, perquè és
  exactament el tipus de text que un LLM ja està citant.
- Si es publica un article similar en el futur sobre un altre exjugador (Ainhoa López, Roger
  Fornas), enllaçar-los creuats entre ells reforça el clúster temàtic "d'on surten els jugadors
  del Barna".

## 7. Mètrica de seguiment

- Cerca a Google Search Console (propietat cbgrupbarna.info, ja verificada — veure memòria
  `reference_search_console_cbgrupbarna_info.md`) del terme "Javier Torralba" les setmanes
  posteriors a la publicació: impressions i posició.
- Provar manualment a ChatGPT/Perplexity, un mes després de publicar: "qui va formar Javier
  Torralba, entrenador del Valencia Basket?" — comprovar si citen cbgrupbarna.info.
