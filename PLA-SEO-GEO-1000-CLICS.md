# Pla SEO/GEO · de ~130-150 clics/mes a 1.000 clics/mes

Encàrrec de l'Ana (29/09/2026). Pla d'actualització centrat a fer créixer els clics
orgànics mensuals de linksbio.cbgrupbarna.info, combinant SEO clàssic (Google Search)
i GEO (que els assistents d'IA —ChatGPT, Gemini, Perplexity, AI Overviews— citin i
recomanin el club).

---

## 0. Abans de res: un fet que canvia tot el pla

**El 14/09/2026 la web es va traslladar de `cbgrupbarna.info` a
`linksbio.cbgrupbarna.info`** (decisió de direcció): `cbgrupbarna.com` (WordPress) es
queda com la web "convencional" del club i aquest repositori passa a viure en un
subdomini. Els 600 fitxers es van reescriure (URLs, sitemap, robots, `llms.txt`), i
els enllaços antics de `cbgrupbarna.info/<pagina>` redirigeixen (via meta-refresh, no
és un 301 de servidor perquè GitHub Pages no ho permet) cap al mateix camí a
`linksbio.cbgrupbarna.info`. `cbgrupbarna.info` (arrel) redirigeix, en canvi, a
`cbgrupbarna.com`.

**Conseqüència directa per aquest pla:** si Search Console segueix mirant la propietat
`cbgrupbarna.info`, **no veurà cap dada de la web d'avui** — que viu a un altre
subdomini. L'última fotografia real que tenim (30/08/2026, abans del trasllat) és:
**2.910 impressions i 49 clics en 11 dies** (18→28/08), CTR 1,7%, posició mitjana 8,4.
Extrapolat a un mes, això és **~130-150 clics/mes**, i és probable que amb el trasllat
del 14/09 aquesta xifra hagi caigut a gairebé zero durant uns dies (Google necessita
temps per re-indexar un domini nou) abans de tornar a pujar.

### 🔴 Acció 0 — cal l'Ana, aquesta setmana, abans de res més

1. **Confirmar si `linksbio.cbgrupbarna.info` és una propietat verificada a Search
   Console.** Si la propietat que hi ha donada d'alta encara és `cbgrupbarna.info`,
   cal afegir-hi `linksbio.cbgrupbarna.info` com a propietat nova (verificació per
   DNS al mateix Cloudflare/Arsys que ja gestiona el domini, o pel fitxer HTML que
   GitHub Pages ja serveix). **Sense això, cap número d'aquest pla es pot mesurar.**
2. **Enviar el sitemap nou** (`https://linksbio.cbgrupbarna.info/sitemap.xml`, 392
   URL) des d'aquesta propietat.
3. **Demanar una inspecció manual de la portada** (`URL Inspection` → `Request
   Indexing`) per accelerar el primer rastreig del subdomini nou.
4. Si es pot, **posar un `301` de servidor de debò** a nivell de DNS/CDN per a
   `cbgrupbarna.info → linksbio.cbgrupbarna.info` (i no cap a `.com`) per a les
   pàgines que ja tenien clics reals (campus, portada, blog) — avui aquest trànsit
   es perd cap al WordPress. És l'única peça d'aquest pas 0 que necessita algú amb
   accés a Cloudflare, no només a Search Console.

**Fins que l'Ana no confirmi el punt 1, tota la resta del pla es pot preparar
(codi, contingut, fitxes) però no es podrà saber si funciona.**

---

## 1. Els números: què cal per arribar a 1.000

No n'hi ha prou amb "millorar el SEO" en general. Repartit per bloc, a partir de les
dades reals del 30/08 (l'única fotografia que tenim):

| Bloc | On som avui | Potencial realista si s'executa el pla | Horitzó |
|---|---|---|---|
| **Marca** («grup barna basquet», «club barna»...) | Ja hi som: pos. 2, CTR 17,6% | +20-30% per més trànsit d'Instagram cap al web (avui 439.000 visualitzacions/mes a IG i gairebé cap clic surt cap aquí) | 1 mes |
| **Campus** (16 consultes, pos. 12-16 avui) | ~1 clic/11 dies | 150-250 clics/mes si es puja a pos. 4-8 en temporada alta (maig-juliol) | 2-3 mesos, estacional |
| **Local** («escola bàsquet Sant Martí/Clot», «bàsquet nens Barcelona») | Impressions soltes, pos. 3-4 en alguna consulta | 100-200 clics/mes amb fitxa de Google verificada + contingut local ampliat | 2 mesos |
| **Castellà (`/es/`)** | CTR 0,99% (3x pitjor que el català amb volum similar) | Doblar-lo (2-3%) suposaria +70-100 clics/mes només millorant títols i metes | 3-4 setmanes |
| **Blog / contingut nou** (23 articles avui) | Molt volum global inútil (Iran, Tailàndia...) + alguna consulta local bona | 300-500 clics/mes en 4-6 mesos amb 10-15 articles nous ben dirigits a Barcelona | 4-6 mesos |
| **GEO** (assistents d'IA) | `llms.txt` ja actiu, ja hi ha sessions de cerca conversacional detectades | No compta com a "clic" de Search Console de la mateixa manera, però alimenta trànsit directe i marca | Continu |

**Lectura honesta:** 1.000 clics/mes **no és una xifra d'una setmana ni d'un mes**.
Amb tots els blocs executats i la temporada de campus (maig-juliol) ajudant, és una
xifra **realista a 4-6 mesos**, no abans. Prometre-ho abans seria com els «195 €» que
no es publiquen sense poder-los complir: millor una progressió certa que una promesa
buida.

---

## 2. Fase 1 (setmanes 1-2) · Fonaments tècnics — codi, sense esperar l'Ana

**Estat el 29/09/2026, revisat en directe:** quatre dels sis punts ja estaven fets
per sessions posteriors al 30/08 que no ho havien anotat en aquest document —
verificat i registrat a `PENDENTS-WEB.md`. Els que quedaven per fer avui:

1. ~~**Schema `Event` + `Offer` a les pàgines de campus.**~~ **No es pot fer
   encara, i és correcte que no s'hagi fet.** El campus d'estiu 2026 ja és una
   edició tancada (l'`Event` hi tindria dates passades) i el de Nadal encara no
   té dates ni preu confirmats per l'Ana —la pàgina mateixa ho diu: «es
   publiquen durant el mes d'octubre». Hi ha una plantilla llesta a
   `POSICIONAMENT-CAMPUS-SEO.md`. **Pendent real: que l'Ana doni les dates i el
   preu del campus de Nadal** (és literalment ara, octubre), i llavors s'enganxa
   en cinc minuts.
2. ~~**Auditoria de títols i metes en castellà.**~~ **Fet, revisat i ja estava
   bé.** Comparats `campus/`, `campus-basquet-barcelona/`,
   `tecnificacio-basquet-barcelona/`, `escola-basquet-barcelona/` i la portada
   contra la seva parella en castellà: cap és una traducció literal, totes fan
   servir vocabulari propi («baloncesto», «manejo de balón»). El CTR baix
   d'`/es/` del 30/08 no es pot atribuir a còpia feble; caldrà tornar-ho a
   mirar amb dades del domini nou.
3. ~~**Verificar reciprocitat de l'`hreflang`.**~~ **Fet.** Auditades les 471
   pàgines amb `hreflang`: **0 errors reals**. Però ha sortit d'aquí un 🔴
   **bug real i arreglat**: `es/ventajas-familia/` i `en/family-benefits/`
   tenien el `canonical` sense el prefix d'idioma (apuntaven a URL que donen
   404 en directe). Arreglat al generador
   (`scripts/build-avantatges-familia.py`) i a les dues pàgines publicades.
4. ~~**`/campus-nadal-basquet-barcelona/` enllaçada des de `/campus/`.**~~
   **Ja ho estava** (i també des de `campus-basquet-barcelona/` i
   `tecnificacio-basquet-barcelona/`).
5. ~~**Secció pròpia de tecnificació.**~~ **Ja existeix**:
   `/tecnificacio-basquet-barcelona/` als tres idiomes, amb `hreflang` i al
   sitemap.
6. ~~**Consolidar `campus-basquet-barcelona/` i `campus/`.**~~ **Ja estan
   diferenciades**: una és el producte i la inscripció, l'altra la comparativa
   amb l'oferta de la ciutat. No calia tocar-hi res.

---

## 3. Fase 2 (setmanes 2-4) · Local i fitxa de Google — cal l'Ana

Aquest bloc és el que té millor relació esforç/resultat i **ja estava preparat des
del 30/08/2026**, només falta executar-lo:

1. **Verificar la fitxa de Google Business** (`business.google.com/verifications`,
   mètode vídeo a La Nau del Clot). Sense això no es pot respondre cap ressenya ni
   assegurar que els canvis del perfil es vegin. És el pas que desbloqueja tota la
   resta d'aquesta fase.
2. **Publicar les 3 respostes a ressenyes ja redactades** (Cristina Alaminos, la
   ressenya sobre conducta amb menors, Jordi Gili).
3. **Campanya de ressenyes a les famílies** (individual, 10-15 al dia, no al grup
   gran): cada ressenya nova amb «bàsquet Barcelona» o «Clot» al text ajuda al
   posicionament local, a banda de la nota mitjana.
4. **Unificar telèfon i correu a les 4 fonts descuadrades** (fitxa de Google, Guia
   Barcelona/barcelona.cat, cbgrupbarna.com, Badgie): el NAP (nom-adreça-telèfon)
   inconsistent és un dels factors que més penalitza el posicionament local a
   Google.
5. **Pujar fotos reals a la fitxa de Google** (La Nau, entrenaments, equips): les
   fitxes amb fotos pròpies reben més clics al mapa local.

---

## 4. Fase 3 (mes 2) · Autoritat externa i enllaços — cal l'Ana + partners

Ja hi ha material preparat, només falta enviar-lo:

1. **`MISSATGES-PARTNERS-LLESTOS.md`**: missatges ja redactats per demanar als 22
   partners que enllacin la seva fitxa (`/patrocinadors/partners/<nom>/`) des de la
   seva pròpia web. Cada enllaç extern d'un negoci real del barri és domini
   d'autoritat que Google i els assistents d'IA llegeixen com a senyal de
   confiança.
2. **`AUTORITAT-EXTERNA-CAMPUS.md`**: les sis onades de mencions externes pel
   campus (Globasket i Centre Bac de Roda ja renovats; Nova Farmàcia del Clot
   signada; resta de partners, premsa de barri, institucional/federatiu i Wikidata
   encara sense onada iniciada).
3. **Viquipèdia**: el CB Roser en té fitxa i el Barna no — és una de les fonts amb
   més pes per als motors d'IA. Cal algú sense conflicte d'interès que l'escrigui,
   o declarar-lo obertament si ho fa algú del club, amb la *Guia Clot · Camp de
   l'Arpa* com a font secundària real.
4. **Fitxa de Google Business Profile completa**: descripcions, categories, serveis
   i sis preguntes precarregades ja redactades a `CAMPUS-FITXA-GOOGLE-I-AGENDES.md`,
   llestes per copiar — falta enganxar-les.

---

## 5. Fase 4 (mesos 2-4) · Contingut nou dirigit, no volum

**No repetir l'error dels tres articles que xuclen el 40% de les impressions i quasi
cap clic** («a quina edat començar», «què és el 3x3»): són consultes globals que
Google respon sol o amb AI Overview. **Cap article nou s'ha d'escriure per a una
consulta que ja tingui resposta directa a Google.** El filtre per a cada article nou:

- Ha de portar **«Barcelona», «Clot» o «Sant Martí»** al títol o ser inequívocament
  local pel context (una pregunta que només té sentit responguda des d'aquí).
- Ha de respondre una pregunta que **avui no tingui cap secció pròpia** al web (com
  la tecnificació, ara mateix).
- Candidats concrets, per ordre d'impacte esperat:
  1. «Campus de bàsquet a Barcelona: quin triar» — ja existeix
     (`campus-basquet-barcelona-guia`), revisar si cobreix bé «tecnificació» com a
     paraula pròpia.
  2. Un article/secció dedicada a **tecnificació d'alt rendiment a Barcelona**,
     separada de campus, per atacar la posició 57.
  3. **«Escola de bàsquet al Clot / Sant Martí»**, ampliant les impressions soltes
     ja detectades («basketball for kids near me» pos. 3, «escuela de basketball
     para niños» pos. 4) amb una pàgina o secció que reculli explícitament aquesta
     intenció local.
  4. Contingut de temporada per a `campus-nadal-basquet-barcelona/` i
     `campus/setmana-santa/`: dates i preus concrets i indexables («campus nadal
     basquet barcelona» ja té cerques pròpies).

---

## 6. GEO · que els assistents d'IA recomanin el club

Ja hi ha base construïda (`llms.txt`, JSON-LD ric a la majoria de pàgines, i s'han
detectat sessions de cerca conversacional reals als registres de Search Console —
fragments com «busca mas», «cuando empieza»). Per créixer aquí:

1. **Mantenir `llms.txt` sincronitzat** amb qualsevol pàgina nova (ja ho fa el
   robot `chore(seo)` que corre a cada push).
2. **Cada pàgina de decisió** (campus, escoleta, femení, patrocini) ha de tenir
   `FAQPage` complet i honest — els assistents d'IA citen literalment la resposta
   marcada, no el text de la pàgina sencera.
3. **No inventar mai una dada** perquè quedi millor per a un assistent d'IA: és
   exactament la mena d'error que després es cita textualment i és molt difícil de
   desfer (a diferència d'una posició de Google, que es pot recalcular).
4. Mesurar-ho és indirecte: GA4 pot veure trànsit `referral` d'`chatgpt.com`,
   `perplexity.ai`, `gemini.google.com`; val la pena afegir-ho com a segment quan
   es construeixi el dashboard d'analítica pendent.

---

## 7. Calendari resumit

| Setmana | Qui | Què |
|---|---|---|
| 1 | **Ana** | Confirmar/crear propietat de Search Console per a `linksbio.cbgrupbarna.info`, enviar sitemap, demanar indexació de la portada |
| 1-2 | Codi | Schema `Event`+`Offer` al campus, auditoria de títols `/es/`, hreflang, enllaç a campus de Nadal |
| 2 | **Ana** | Verificar fitxa de Google Business, publicar les 3 respostes a ressenyes |
| 2-4 | **Ana** | Campanya de ressenyes a famílies, unificar NAP a les 4 fonts, pujar fotos a la fitxa |
| 2-4 | Codi + **Ana** | Consolidar pàgines de campus, secció de tecnificació |
| Mes 2 | **Ana** | Enviar missatges als 22 partners (ja redactats), continuar onades d'autoritat externa |
| Mes 2-4 | Codi | 3-4 peces de contingut noves, dirigides i locals |
| Cada mes | **Ana** | Repetir la lectura de Search Console i comparar amb aquesta taula |

---

## 8. Com sabrem si funciona

Repetir cada mes la mateixa lectura que es va fer el 30/08/2026 (Search Console →
Rendiment → exportar `Queries.csv` + `Pages.csv`), i comparar-la amb aquesta taula
de blocs. **La primera lectura útil després d'aquest pla és la de mitjans
d'octubre**: prou dies perquè Google hagi re-indexat el subdomini nou i s'hagi vist
l'efecte del pas 0. Fins llavors, qualsevol xifra que es miri és soroll del
trasllat de domini, no del pla.
