# CB Grup Barna — instrucciones del repo

Web estática del club (GitHub Pages, dominio `cbgrupbarna.info`): `index.html`,
galerías de fotos, eventos y despliegue por Actions.

## Antes de producir nada: skills y memoria

Protocolo `arranque-eficiente`, en dos pasos y por este orden:

1. **La skill que toca.** Entrar por `/cbgb` y cargar 1-2 satélites. Leer la skill
   **antes** que el material subido. Para cualquier cosa de contenido, crecimiento
   o conversión en Instagram: `doctrina-juliol-2026-cbgb` da la síntesis vigente.
2. **La memoria.** `.claude/knowledge/` guarda los datos, las decisiones ya
   cerradas y lo que ya corregimos. Skill: `memoria-cbgb`.

Y con el mínimo de tokens: lectura dirigida (`grep`, no volcar archivos enteros),
defaults inteligentes en vez de tandas de preguntas, entregable antes que explicación.

## Las tres reglas duras

1. **Si un número no está en `.claude/knowledge/bbdd/`, no se cita.** Ni en dossier
   de Junta, ni ante sponsors, ni ante prensa.
2. **Si un debate está cerrado en `bbdd/decisions.csv`, no se reabre con una
   opinión** — hace falta dato nuevo. Y lo marcado como `practica_morta` se
   reescribe sin discutir.
3. **El histórico no se reescribe.** `historico/AAAA-MM.md` es inmutable: lo
   refutado se marca en la tabla y se cuenta en el mes siguiente.

## Atajos

```bash
grep -i "<tema>" .claude/knowledge/bbdd/decisions.csv    # ¿ya está decidido?
grep "^2026-06" .claude/knowledge/bbdd/metriques.csv     # cifras de un mes
cat .claude/knowledge/bbdd/obertes.md                    # qué no sabemos aún
```

Manual completo de la memoria: `.claude/knowledge/README.md`.

## Estado actual (julio 2026)

Conversión **0,03 %** — el alcance nunca fue el problema. La palanca es el aparador
del perfil, no producir más. Cadena de conversión: ganxo → razón de reenvío →
portada → aparador → mix.
