---
name: memoria-cbgb
description: "Memoria del club: como consultar y ESCRIBIR en la BBDD de conocimiento de CB Grup Barna, que vive en el repo cbgrupbarna-info bajo .claude/knowledge/ (serie mensual de IG, decisiones cerradas, practicas muertas, leyes verificadas, autopsias de reels, preguntas abiertas e historico mensual). Cargar SIEMPRE que haya que citar un numero del club, saber si un debate ya esta cerrado, registrar el resultado de un reel, cerrar el mes, o cuando Ana diga apunta esto, registra, que deciciamos sobre X, de donde sale este numero, historico, o el balance del mes. Tambien antes de afirmar cualquier cifra ante Junta, sponsors o prensa: si no esta en la BBDD, no se cita. Da el DATO y su procedencia; el criterio vive en doctrina-juliol-2026-cbgb y en las skills de cada eslabon."
---

# memoria-cbgb — La BBDD de conocimiento

El club acumula criterio en skills y **datos** en la BBDD. Esta skill es la puerta
de la BBDD: dónde está cada cosa, cómo se consulta y **cómo se le añade una fila
sin romperla**.

**Ubicación:** repo `cbgrupbarna-info` → `.claude/knowledge/`
Manual completo: `.claude/knowledge/README.md`

## La regla dura

> **Si un número no está en la BBDD, no se cita.** Ni en un dossier de Junta, ni
> ante un sponsor, ni ante prensa. Y si un número de una skill no coincide con el
> de la BBDD, **manda la BBDD** y se corrige la skill.

## Mapa

| Necesito... | Archivo |
|---|---|
| Un número de crecimiento (alcance, seguidores, conversión) | `bbdd/metriques.csv` |
| Saber si un debate está cerrado o una práctica prohibida | `bbdd/decisions.csv` |
| Una regla verificada y su nivel de confianza | `bbdd/lleis.csv` |
| Cómo fue un reel concreto / el benchmark propio | `bbdd/reels.csv` |
| Qué no sabemos todavía o qué no cuadra | `bbdd/obertes.md` |
| Qué pasó en un mes y por qué cambiamos de opinión | `historico/AAAA-MM.md` |

## Consultar (lectura dirigida — `arranque-eficiente`)

Son CSV: se leen con `grep`, no abriendo el archivo entero.

```bash
grep -i "carrusel" .claude/knowledge/bbdd/decisions.csv    # ¿está cerrado este debate?
grep "^2026-06" .claude/knowledge/bbdd/metriques.csv       # el mes de junio
grep "morta" .claude/knowledge/bbdd/decisions.csv          # todo lo prohibido
```

**Antes de proponer algo, dos comprobaciones:** ¿la práctica está en `decisions.csv`
como muerta? ¿el debate ya está cerrado? Si lo está, hace falta **dato nuevo** para
reabrirlo — no una opinión.

## Escribir

Nunca se **borra** una fila: se cambia su `estat` (`vigent` → `refutat` / `revisar`).
Toda fila lleva **`evidencia`**: de dónde sale. Sin evidencia, no entra.
Decimales con **punto**, vacíos con `-`, inferidos con `~` y explicados en `notes`.
**Sin comas dentro de un campo** — reformular la frase.

### Después de publicar un reel (24-48 h) → `bbdd/reels.csv`

Abrir Insights y anotar: guardados, compartidos, % de no-seguidores, retención a 3 s,
qué había en el **frame 0** y el veredicto. Guardados + compartidos = **0** significa
que el reel no dio ninguna razón: no escalará, y la autopsia acaba ahí.
Criterio completo: `arrencada-reels-cbgb`.

### Al cerrar el mes

1. Una fila en `bbdd/metriques.csv` desde el **resumen mensual in-app**.
2. Recalcular **conversión = seguidores nuevos ÷ alcance**. Baseline a batir: **0,03 %**.
3. Escribir `historico/AAAA-MM.md`: qué pasó, **de qué cambiamos de opinión**, qué se
   decidió, qué NO demostró el mes, y qué hereda el mes siguiente.
4. Mover a `bbdd/lleis.csv` lo que se haya verificado; subir o bajar `confianca`.
5. Cerrar en `bbdd/obertes.md` lo resuelto; abrir lo nuevo.
6. Duplicar la skill de doctrina como `doctrina-<mes>-<any>-cbgb` y dejar la anterior
   como histórico.

### Cuando se cierra un debate o se mata una práctica → `bbdd/decisions.csv`

`D-xx` para decisiones, `M-xx` para prácticas muertas. Siempre con la evidencia que
la mató. Una práctica muerta que reaparece en un borrador **se reescribe sin discutir**.

## El histórico no se reescribe

Un snapshot mensual cerrado es **inmutable**. Si algo resultó ser falso, no se borra:
se marca `refutat` en la tabla que toque y se cuenta en el mes siguiente. Julio dejó
dos errores escritos a propósito (el carrusel como motor, y leer "origen Feed" como
"solo seguidores"). **El error es parte del conocimiento** — borrarlo es perder la
lección y arriesgarse a repetirla.

## Cómo encaja

- `doctrina-juliol-2026-cbgb` → la **síntesis vigente**; lee de esta BBDD.
- `crecimiento-ig-cbgb` · `aparador-perfil-cbgb` · `ganxos-cbgb` ·
  `arrencada-reels-cbgb` · `portada-reels-cbgb` → el **criterio** de cada eslabón.
- `arranque-eficiente` → lectura dirigida: `grep` de lo que hace falta, nunca volcar
  el CSV entero.
