# BBDD de conocimiento — CB Grup Barna

Memoria del club: **qué sabemos, desde cuándo, con qué prueba y qué dejó de ser
verdad.** Vive en el repo (versionada en git), no en la cabeza de nadie ni en un
chat perdido.

Dos capas:

| Capa | Qué es | Se toca... |
|---|---|---|
| **`historico/`** | Snapshot narrado de cada mes. **Inmutable** una vez cerrado. | Solo se añade un archivo nuevo al cerrar mes |
| **`bbdd/`** | Tablas acumulativas (CSV) + preguntas abiertas. **Vivas.** | Se les añaden filas continuamente |

La regla: **el histórico no se reescribe.** Si algo resultó ser falso, no se
borra — se marca como refutado en `bbdd/lleis.csv` y se cuenta en el snapshot del
mes siguiente. El error es parte del conocimiento.

## Los archivos

| Archivo | Qué guarda | Cuándo se le añade una fila |
|---|---|---|
| `bbdd/metriques.csv` | Serie mensual de IG (piezas, alcance, % externos, seguidores, conversión) | Al cerrar cada mes, con el resumen in-app |
| `bbdd/decisions.csv` | Decisiones tomadas y prácticas matadas, con su estado | Cada vez que se cierra un debate o se prohíbe una práctica |
| `bbdd/lleis.csv` | Reglas que damos por buenas, con su nivel de confianza | Cuando un patrón se verifica con datos propios |
| `bbdd/reels.csv` | Autopsia de cada reel publicado (frame 0, guardados, retención) | 24-48 h después de publicar cada reel |
| `bbdd/analisis.csv` | Qué hemos analizado (datos propios, benchmarks, referencias) y qué salió de ahí | Al terminar un análisis o benchmark |
| `bbdd/correccions.csv` | Qué creíamos, qué sabemos ahora y con qué prueba | Cada vez que cambiamos de opinión |
| `bbdd/skills.csv` | Inventario del ecosistema de skills, con estado de cada una | Al crear, fusionar o jubilar una skill |
| `bbdd/obertes.md` | Preguntas sin responder e inconsistencias sin resolver | En cuanto aparece una; se borra al cerrarla |
| `historico/AAAA-MM.md` | El mes narrado: qué pasó, qué cambió de opinión, qué se decidió | Al cerrar mes |

## Cómo se usa (3 movimientos)

1. **Antes de afirmar un número** ante Junta, sponsors o prensa → sale de
   `bbdd/metriques.csv`, no de memoria. Si no está ahí, no se cita.
2. **Antes de reabrir un debate** ("¿y si volvemos a los carruseles?") → mirar
   `bbdd/decisions.csv`. Si está cerrado, hace falta **dato nuevo** para reabrirlo.
3. **Después de publicar un reel** → una fila en `bbdd/reels.csv`. Con 10 filas
   hay benchmark propio, que vale más que cualquier consejo genérico de Instagram.

## Convenciones

- **Fechas** `AAAA-MM` o `AAAA-MM-DD`. **Decimales con punto.** Campos vacíos = `-`.
- **Comas dentro de un campo**: no. Reformular la frase.
- **Toda fila lleva `evidencia`**: de dónde sale el dato. Sin evidencia, no entra.
- **Números inferidos o estimados** se marcan con `~` y se explican en `notes`.
- Ninguna fila se **borra**: se cambia su `estat` (`vigent` → `refutat` / `revisar`).

## Cómo encaja con las skills

La BBDD es el **dato**; las skills son el **criterio**. No se duplican:

- `doctrina-juliol-2026-cbgb` → la síntesis vigente. Lee de aquí.
- `memoria-cbgb` → cómo consultar y escribir en esta BBDD.
- `crecimiento-ig-cbgb`, `aparador-perfil-cbgb`, `arrencada-reels-cbgb`,
  `ganxos-cbgb`, `portada-reels-cbgb` → el detalle de cada eslabón.

Si un número de una skill y uno de la BBDD no coinciden, **manda la BBDD** y se
corrige la skill.
