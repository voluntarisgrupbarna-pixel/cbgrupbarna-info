# Backup del ecosistema de skills — CB Grup Barna

Copia versionada de las **40 skills del club** que viven en
`~/.claude/skills/synced/`. Ese directorio no tiene control de versiones y además
lo pisa una sincronización externa: un borrado, un cambio de máquina o un sync
se lleva años de criterio acumulado. Esto lo arregla — cada push a GitHub es una
copia fuera del ordenador.

**Última sincronización: 2026-08-29 15:30 UTC.** `synced/` trajo una sección
ampliada de la norma de partners en `cbgb` (fusionada). Y algo más serio: tras
un reinicio de contenedor, **`doctrina-juliol-2026-cbgb` y `memoria-cbgb`
habían desaparecido** de `~/.claude/skills/` — restauradas desde aquí el mismo
día (incidencia O-15, confirma lo que O-14 solo advertía). Cierra la incidencia
O-12 de `.claude/knowledge/bbdd/obertes.md`.

## Qué hay y qué no

- **Sí**: las 40 skills del club (`*-cbgb`, `*-club`, `arranque-eficiente`,
  `ana-innovacio-barna`, `cbgb`), con sus `references/`, `scripts/` y `assets/`
  (tipografías y escudo incluidos, para que restaurar deje todo funcionando).
- **No**: las skills genéricas de Anthropic (`docx`, `pptx`, `pdf`, `xlsx`,
  `skill-creator`, `canvas-design`, `theme-factory`…). Se reinstalan solas y no
  son conocimiento del club.

## Esto es un backup, no la copia viva

Las skills **se editan en `~/.claude/skills/synced/`**. Este directorio es un
espejo: si se edita aquí, el cambio no lo ve nadie hasta que se copie de vuelta.
Se llama `skills-backup/` (y no `skills/`) precisamente para que Claude no las
cargue dos veces.

## ⚠️ Las skills las gestiona una sincronización externa

**Viven en `~/.claude/skills/synced/`**, no en `~/.claude/skills/`. El 13/08 ese
directorio se reorganizó y el enrutado de `/cbgb` que habíamos actualizado volvió
a su versión antigua. Tres consecuencias:

1. **Editar dentro de `synced/` no dura.** La copia canónica de `cbgb/SKILL.md` es
   la de aquí.
2. **Sincronizar es FUSIONAR, no sobrescribir**, en las dos direcciones: la
   sincronización también trae mejoras de verdad (así llegó la norma de la cartela
   de partners a `sistema-visual` y `video-club`). Compara antes de copiar.
3. **Nunca sincronices backup→repo a ciegas.** Haz `git diff` antes de commitear:
   si el sync revirtió algo, lo estarías guardando como si fuera un cambio bueno.
   Así se detectó (incidencia O-14).

`doctrina-juliol-2026-cbgb` y `memoria-cbgb` viven **fuera** de `synced/` (las
creamos aquí): la sincronización no las toca, pero tampoco las respalda. Su única
copia de seguridad es esta — y el 29/08 hizo falta usarla: un reinicio de
contenedor las borró por completo de `~/.claude/skills/`. **En cada
actualización de conocimiento, comprobar primero que las dos siguen ahí**
(`ls ~/.claude/skills/`) y restaurarlas sin esperar a que se note su falta.

## Restaurar

```bash
# todo el ecosistema
cp -r .claude/skills-backup/*/ ~/.claude/skills/synced/

# una sola skill
cp -r .claude/skills-backup/ganxos-cbgb ~/.claude/skills/synced/
```

## Volver a sincronizar (después de crear o editar skills)

```bash
cd ~/.claude/skills/synced
cp -r $(ls -d *cbgb* *club* arranque-eficiente ana-innovacio-barna | sort -u) \
      <repo>/.claude/skills-backup/
```

Y en el mismo commit, actualizar `.claude/knowledge/bbdd/skills.csv`: una fila por
skill nueva, o cambiar el `estat` de la que se haya fusionado o jubilado.

## Las 9 que faltan

`skills.csv` marca con `FALTA` nueve skills que otras referencian pero que **no
están instaladas** — `cb-grup-barna`, `mi-rol-coordinadora`, `millorar-club-top-bcn`,
`disseny-estetic-club`, `psicologia-social-club`, `referent-basquet-espanyol`,
`crear-apps-webs-club`, `xarxes-socials-club` y `guions-virals-cbgb`. Si aparecen,
van aquí también. Incidencia O-11.
