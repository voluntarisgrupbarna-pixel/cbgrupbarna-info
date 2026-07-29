---
name: captacio-pack-cbgb
description: "Genera el PACK de captacion de partners/sponsors/colaboraciones de CB Grup Barna de una temporada: Plan estrategico (Word), Dossier de venta (deck PPTX sin precios) y Hoja de targets/CRM (Excel con pipeline ponderado). Trae ya el calendario por olas, los niveles Oro/Plata/Bronce con rangos de precio placeholder y el foco en colaboraciones en especie. Cargar cuando Ana diga: genera o monta el plan de captacion, hazme el pack de sponsors, prepara el dossier y la hoja de targets, plan de partners de la temporada, el plan de sponsors, o los materiales para captar empresas. Es la capa de PRODUCCION; la estrategia y los scripts viven en patrocinis-club. Usa los valores de sistema-visual-cbgb y ejecuta con las skills docx, pptx y xlsx."
---

# Pack de captacion de partners - CB Grup Barna

Esta skill produce los MATERIALES; la skill patrocinis-club aporta el CRITERIO
(que vendemos, con que palabras, scripts, objeciones, contrato). Leerla siempre
antes de generar, para no perder la logica madre: no vendemos espacio
publicitario, vendemos pertenencia a un barrio. Primero DESEO, despues DATO.

## Que genera (los 3 entregables)

Un encargo de "plan de captacion" son estos tres archivos, nombrados
CBGB_*_<temporada>:

1. Plan estrategico .docx (skill docx). Documento interno de trabajo.
2. Dossier de partners .pptx (skill pptx). Pieza de venta. SIN precios abiertos.
3. Hoja de targets .xlsx (skill xlsx). CRM vivo con pipeline.

Antes de arrancar, confirmar con Ana 3 cosas (si no las dice, usar estos
defaults): formato (default: los 3), foco del ciclo (default: temporada completa
mas especie), e incluir rangos de precio (default: si, placeholder, solo interno).

## Reglas de oro del pack

- Precios solo internos. Rangos placeholder en el Plan y la Hoja; en el Dossier,
  "els preus, a la reunio". Validar con Junta antes de usar.
- Datos del club marcados. Cifras de comunidad (p. ej. "~600 jugadors") van como
  placeholder a confirmar con datos reales de la temporada.
- Marca exacta (sistema-visual-cbgb): navy 1B2A4A, rojo E63329, tinta 0E1116,
  display condensada (Anton o Arial bold en mayusculas), Arial para cuerpo. Nada
  de degradados ni barras/rayas decorativas en el deck.
- Cerrar con angulo novedoso (ana-innovacio-barna): del logo a la activacion con
  metricas mas informe de retorno automatico post-evento.

## Estructura del Plan (Word)

Idea madre y objetivo, los 3 activos que vendemos, niveles (tabla), colaboraciones
en especie, targets por sector, proceso comercial y scripts (email frio, guion de
reunion, objeciones), calendario de la temporada, contrato tipo (minimos),
mantenimiento y renovacion, angulo novedoso, proximos pasos. Contenido detallado
de scripts y contrato: skill patrocinis-club.

## Estructura del Dossier (deck, 8 slides)

Portada "Forma part d'un barri"; Qui som (3 valores mas panel "lo que una marca no
puede comprar"); El barri en numeros (stat cards); Que fem junts (3x3, campus,
temporada); Nivells (3 tarjetas, sin precio); Especie (grid mas "valoritzem la
teva aportacio"); Ja confien (prueba social, con placeholders "[el teu logo
aqui]"); Cierre "Places limitades. Parlem." mas contacto. Portada y cierre en
navy, contenido claro (sandwich).

## Estructura de la Hoja de targets (Excel, 4 pestanas)

1. Pipeline targets: empresa, sector, nivel objetivo, vinculo-familia, contacto,
   estado (desplegable), import objetivo, probabilidad, import ponderado
   (= import x prob), proxima accion mas fecha. Fila TOTAL con suma ponderada.
   Priorizar radio 1 km y familias del club.
2. Nivells i preus: rangos placeholder mas 3 escenarios de ingresos
   (conservador/objetivo/ambicioso) por formula.
3. Calendari captacio: olas por periodo (ver mas abajo).
4. Col.laboracions especie: necesidad del club, tipo empresa, valor equivalente,
   contraprestacion.

## Datos base de temporada (ajustar al ano del encargo)

Niveles y rangos (placeholder, uso interno):
- ORO Partner principal: 8.000-15.000 EUR/ano, 1 solo (exclusiva de sector).
  Naming/logo en el pecho de la camiseta, co-branding de un evento, video de marca
  anual, presencia toda la temporada, reunion de balance con Junta.
- PLATA Partner: 3.000-5.000 EUR/ano, 3-4 plazas. Logo en equipacion o
  calentamiento, 1 reel dedicado/ano, activacion en 3x3 o campus, pack de fotos y
  video, mas todo lo de Bronze.
- BRONZE Colaborador: 1.000-2.500 EUR/ano, 6-8 plazas. Logo en web y mur de
  partners, bienvenida en redes, presencia en lonas y carteleria, invitacion a un
  evento/ano.
- ESPECIE / a medida: valorizar el equivalente. Contraprestacion equivalente al
  valor aportado, mismo trato de relacion.

Escenarios de ingresos (formulas Excel):
- Conservador: =8000 + 3*3000 + 6*1000
- Objetivo: =12000 + 4*4000 + 7*1800
- Ambicioso: =15000 + 4*5000 + 8*2500

Calendario por olas (base; desplazar al ano):
- Julio (pretemporada): preparacion. Dossier mas reel listos, 25 targets, precios
  con Junta.
- Agosto: Oro (ancla). 2-3 reuniones Oro, naming camiseta, gran ancla del barrio.
- Septiembre: Plata mas Oro. Ronda Plata, vinculos de familias, equipaciones antes
  de liga.
- Octubre: Bronze mas especie. Email/visita a comercios, cerrar especie.
- Nov-Dic: completar mas activar. Llenar plazas, activaciones, onboarding.
- Ene-Mar: mantenimiento. Informe trimestral, activaciones, captacion 3x3.
- Abr-Jun: renovacion. Informe de retorno, renovacion con mejora, referidos.

Sectores objetivo (radio 1 km mas familias del club):
- Salud/bienestar: dental, fisio, farmacia, optica, nutricion (Plata/Especie).
- Restauracion: restaurantes, cafeterias, forns, gelateries (Bronze, sampling).
- Servicios prof.: gestorias, inmobiliarias, seguros, banca proximidad (Plata/Oro).
- Retail: deporte, ropa, tecnologia, supermercados (Bronze/Plata).
- Construccion/automocion: reformas, constructoras, concesionarios (Plata/Oro).
- Grandes anclas: Westfield Glories y equivalentes (Oro, naming de evento).

Necesidades en especie (cada una es una puerta a una empresa):
- Material deportivo (botiga d'esport, ~2.500 EUR): Plata, logo calentamiento mas reel.
- Fisioterapia equipos (clinica fisio, ~4.000 EUR): Plata mas presencia pavellon.
- Transporte (empresa transporte, ~3.000 EUR): logo autocares mas mencion redes.
- Catering eventos (restauracion/forn, ~1.500 EUR): Bronze mas sampling estand.
- Impresion carteleria (impremta, ~1.500 EUR): Bronze mas credito "produccion por".
- Foto/video puntual (estudio AV, ~2.000 EUR): credito mas pack de contenidos.

Angulo novedoso por defecto (ana-innovacio-barna):
1. Del logo a la activacion con metricas (premio del 3x3, beca de campus, reto).
2. Informe de retorno automatico post-3x3/campus (version sponsor del recap).
3. Micro-sponsors de barrio (tier comunitario para comercios pequenos).

## Flujo de trabajo

1. Leer patrocinis-club (criterio) mas este SKILL.md.
2. Confirmar o asumir los 3 defaults (formato, foco, precios).
3. Generar Excel, luego Word, luego PPTX (en ese orden; el Excel fija cifras que
   citan los otros).
4. QA: recalcular formulas del Excel (0 errores), validar el Word, y revisar el
   deck con un subagente de ojos frescos (overflow, solapes, contraste).
5. Guardar como CBGB_*_<temporada> en la carpeta de Ana y entregarlos con
   present_files. Cerrar con el bloque "Angulo novedoso" y ofrecer el reel de
   captacion y/o version ES del deck.

## Filtro de calidad (antes de entregar)

- El Dossier NO ensena precios; el Plan y la Hoja los marcan como internos.
- Cifras del club marcadas como placeholder a confirmar.
- Marca exacta (colores y tipografia de sistema-visual-cbgb).
- Excel con 0 errores de formula y desplegables funcionando.
- Deck sin overflow ni solapes (verificado con subagente).
- Cierra con angulo novedoso y proximo paso con fecha.

## Errores a evitar

- Poner precios en el dossier que ve la empresa.
- Inventar cifras de comunidad en vez de marcarlas para confirmar.
- Generar el pack sin leer patrocinis-club (se pierde la logica de pertenencia).
- Entregar el deck sin QA visual con subagente.
- Vender "visibilidad" en vez de relacion y pertenencia.
