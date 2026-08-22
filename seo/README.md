# Mapa de paraules clau i bateria de proves · CB Grup Barna

Contra qui competim, amb quines paraules i a quina plataforma. Aquesta carpeta
és la font única: si una paraula no és aquí, no la mesurem.

## Fitxers

| Fitxer | Què és |
|---|---|
| `mapa-paraules-clau.csv` | **145 paraules i frases** amb idioma, família, intenció, plataformes on competim, la URL nostra que hauria de respondre-la, prioritat i rival previst. |
| `full-captura.csv` | **270 files per omplir** (una per paraula i plataforma). És el full de treball de qui passa les cerques. |
| `_fonts.py` | Genera els dos CSV. Si cal afegir o treure paraules, es toca **aquí** i es torna a executar: `python3 seo/_fonts.py`. Mai s'editen els CSV a mà. |

## Com es reparteix

- **Per plataforma:** 107 a Google · 113 a assistents d'IA · 28 a Instagram · 22 a TikTok.
- **Per prioritat:** 84 de prioritat 1 (les que decideixen inscripcions), 53 de suport, 8 de cua llarga.
- **Per idioma:** català i castellà en paral·lel, i quatre en anglès per a les pàgines `/en/`.

## La regla del rival

**No decidim contra qui competim: ho diu la cerca.** La columna `rival_previst`
és només una hipòtesi de partida. El rival real és **qui surti per sobre
nostre** a cada consulta, i s'anota a `rival_1..3` del full de captura. Els que
apareguin i no teníem al radar són el descobriment més valuós de tota la
bateria: a Instagram i TikTok segurament sortiran entrenadors amb perfil propi,
campus nacionals i comptes de jugades que a Google no competeixen amb nosaltres.

## Protocol de captura (perquè les dades valguin)

1. **Des del mòbil**, amb la **sessió tancada** o un perfil net. Si cerques des
   del compte del club, Instagram i TikTok ensenyen el que ja segueixes: el
   resultat surt maquillat.
2. **Una fila per paraula i plataforma.** Si no sortim, s'escriu `no` a
   `sortim_si_no` i igualment s'anoten els tres primers. Saber qui guanya quan
   perdem és la meitat de la feina.
3. **Captura de pantalla sempre**, amb la data. És la prova i permet repetir la
   mesura d'aquí a tres mesos i comparar.
4. **Tres repeticions** a les de prioritat 1: aquests cercadors varien.
5. A Instagram, mirar les **tres pestanyes** (comptes, publicacions, reels): hi
   som a unes i no a altres, i això canvia què cal arreglar.
6. A TikTok, anotar també les **suggerències de la barra de cerca**: són
   recerca de paraules clau gratuïta i real.

## Indicadors

- Cobertura de menció · Taxa de citació amb enllaç · Exactitud factual (0-3) ·
  Posició mitjana en llistats · Quota de veu contra els rivals · Cobertura
  d'intenció (paraules amb una URL nostra sana assignada).

## Problemes ja detectats al mapa

- **Canibalització femenina:** `/femeni/` i `/basquet-femeni/` competeixen per
  "Bàsquet femení a Barcelona", totes dues amb canonical propi. El mapa apunta a
  `/basquet-femeni/`; cal decidir què fem amb l'altra (redirecció o
  diferenciació d'intenció).
- **Canibalització de patrocini:** `/patrocinis/`, `/patrocinadors/` i
  `/dossier-patrocinis/`, dues amb el títol idèntic. El mapa apunta a
  `/patrocinadors/`.
- **Adreça amb tres redaccions** diferents als JSON-LD del web. Per a cerca
  local, la fitxa ha de dir sempre exactament el mateix.
