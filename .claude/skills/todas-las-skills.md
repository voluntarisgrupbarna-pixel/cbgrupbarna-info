---
description: Skill maestra que activa todas las skills disponibles de forma conjunta según el contexto de cada tarea. Úsala siempre como punto de entrada antes de responder cualquier solicitud.
---

# Todas las Skills — Activación Conjunta

Antes de responder, evalúa el contexto de la tarea e invoca **todas las skills relevantes** de forma combinada, no una sola.

## Reglas de activación conjunta

### Tareas de código
- Cambio de código → `verify` (al terminar) + `code-review` (revisar el diff) + `simplify` (si hay duplicación)
- PR de GitHub → `review` + `security-review`
- Código con modelos LLM / API Anthropic → `claude-api` + `verify`

### Tareas de diseño y visualización
- Gráficos, dashboards, datos → `dataviz` + `artifact-design`
- Diseño visual (poster, slide, flyer) → `artifact-design` + `create_visual_design_express_skill`

### Tareas de investigación
- Investigación multi-fuente → `deep-research`
- Investigación + presentación de resultados → `deep-research` + `dataviz` + `artifact-design`

### Tareas de configuración
- Hooks, permisos, settings → `update-config`
- Atajos de teclado → `keybindings-help`
- Configuración inicial del repo → `session-start-hook` + `init`
- Reducir prompts repetitivos → `fewer-permission-prompts`

### Tareas de ejecución
- Arrancar / mostrar la app → `run` + `verify`
- Tarea recurrente / polling → `loop`

## Protocolo de uso

1. Lee la solicitud del usuario.
2. Identifica **todos** los contextos que aplican (puede haber más de uno).
3. Invoca cada skill relevante **antes** de empezar a trabajar, en el orden indicado arriba.
4. Si una skill ya fue invocada en este turno, no la repitas — combina sus instrucciones.
5. Nunca esperes a que el usuario escriba `/skill-name`. Actívalas tú proactivamente.
