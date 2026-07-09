# Instrucciones del proyecto

## Skills — activación conjunta y proactiva

Usa siempre la skill `todas-las-skills` como punto de entrada. Evalúa el contexto y aplica **todas las skills relevantes combinadas**, no solo una.

### Reglas rápidas de combinación

| Tarea | Skills a combinar |
|---|---|
| Cambio de código | `verify` + `code-review` + `simplify` (si aplica) |
| PR de GitHub | `review` + `security-review` |
| Código con API Claude/Anthropic | `claude-api` + `verify` |
| Gráficos / datos | `dataviz` + `artifact-design` |
| Diseño visual | `artifact-design` + `create_visual_design_express_skill` |
| Investigación + presentación | `deep-research` + `dataviz` + `artifact-design` |
| Configuración inicial repo | `session-start-hook` + `init` |
| Arrancar app | `run` + `verify` |
| Tarea recurrente | `loop` |
| Configurar settings/hooks | `update-config` |

No esperes a que el usuario invoque `/skill-name`. Actívalas proactivamente y en combinación.
