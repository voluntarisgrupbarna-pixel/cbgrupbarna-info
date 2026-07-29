# Backup del ecosistema de skills — CB Grup Barna

Copia versionada de las **36 skills del club** que viven en `~/.claude/skills/`.
Ese directorio no tiene control de versiones: un borrado accidental o un cambio
de máquina se lleva años de criterio acumulado. Esto lo arregla — cada push a
GitHub es una copia fuera del ordenador.

**Última sincronización: 2026-07-29.** Cierra la incidencia O-12 de
`.claude/knowledge/bbdd/obertes.md`.

## Qué hay y qué no

- **Sí**: las 36 skills del club (`*-cbgb`, `*-club`, `arranque-eficiente`,
  `ana-innovacio-barna`, `cbgb`), con sus `references/`, `scripts/` y `assets/`
  (tipografías y escudo incluidos, para que restaurar deje todo funcionando).
- **No**: las skills genéricas de Anthropic (`docx`, `pptx`, `pdf`, `xlsx`,
  `skill-creator`, `canvas-design`, `theme-factory`…). Se reinstalan solas y no
  son conocimiento del club.

## Esto es un backup, no la copia viva

Las skills **se editan en `~/.claude/skills/`**. Este directorio es un espejo:
si se edita aquí, el cambio no lo ve nadie hasta que se copie de vuelta.
`skills-backup/` (y no `skills/`) precisamente para que Claude no las cargue
dos veces.

## Restaurar

```bash
# todo el ecosistema
cp -r .claude/skills-backup/*/ ~/.claude/skills/

# una sola skill
cp -r .claude/skills-backup/ganxos-cbgb ~/.claude/skills/
```

## Volver a sincronizar (después de crear o editar skills)

```bash
cd ~/.claude/skills
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
