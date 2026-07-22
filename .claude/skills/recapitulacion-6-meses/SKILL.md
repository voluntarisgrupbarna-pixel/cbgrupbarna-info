---
name: recapitulacion-6-meses
description: Memoria viva de CB Grup Barna — recapitulación RODANTE de los últimos 6 meses de trabajo de Ana con Claude (web cbgrupbarna.info, ecosistema de ~35 skills, doctrinas de crecimiento IG, sponsors, vídeo, eventos). Cargar SIEMPRE al empezar cualquier sesión o tarea del club para arrancar con el contexto de lo ya hecho y no repetir ni contradecir trabajo previo. Cargar también siempre que Ana pregunte "qué hemos hecho", "recuérdame dónde estábamos", "resumen de estos meses", "qué skills tenemos", "cuándo hicimos X", "dónde lo dejamos", o pida un informe de actividad para la Junta. Incluye el protocolo para MANTENER la recapitulación al día — cada trabajo significativo que se cierre se anota aquí, y la ventana avanza (lo que supera 6 meses se archiva).
---

# Recapitulación 6 meses — memoria viva del club

Esta skill es la **memoria de trabajo** del proyecto CB Grup Barna en Claude. Resuelve un problema real: cada sesión de Claude empieza de cero, y Ana no tiene por qué re-explicar seis meses de decisiones, doctrinas y entregables. Con esta skill cargada, cualquier sesión arranca sabiendo **qué se ha construido, qué se decidió y por qué, y dónde se quedó todo**.

No es un log de commits: es la vista de directora de marketing. Lo que importa es el hito, la decisión y el estado — no el detalle técnico.

## Recapitulación ejecutiva (ventana actual: ~febrero → julio 2026)

Lo esencial en 30 segundos:

1. **Ecosistema de skills (~35)** — Se construyó un sistema completo de skills del club orquestado por la mestra `/cbgb`: identidad y rol de Ana, sistema visual, carteles, reels/vídeo (operativo, estrella y cinematográfico), CapCut, crecimiento IG, benchmarks (Barça Basket, clubs de barrio, femenino, Pau Gasol Academy), códigos de lujo (Dior, Vogue, Elie Saab, Bvlgari, Jordan Roth → fusionados en `codis-lux-cbgb`), sponsors (`patrocinis-club`, `captacio-pack-cbgb`) y disciplina de arranque (`arranque-eficiente`).
2. **Diagnóstico de crecimiento IG (Q2 2026)** — Con datos propios: ~439K visualizaciones/mes y solo 0,03 % de conversión a seguidores. Conclusión doctrinal: **el alcance nunca fue el problema; lo es la CONVERSIÓN** (bio, pins, primeros 9). El motor es el REEL, no el carrusel. Vive en `crecimiento-ig-cbgb` y `aparador-perfil-cbgb`.
3. **Web cbgrupbarna.info (mayo 2026 →)** — Portal del club en GitHub Pages: link-in-bio, dashboard "Lo Calent", SEO bilingüe + GA4, hub de datos `data.json` con GitHub Action horaria desde JotForm, ruleta 3x3 Westfield Glòries, landing Mes de l'Orgull, galería de fotos con lead-gate de newsletter, panel de administración para eventos/fotos, página de la mascota con reels CA/ES.
4. **Captación de leads como sistema** — Todo lo público empuja a registro: ruleta con formulario + backend Apps Script, galerías con puerta PIN/newsletter, vCard para difusión WhatsApp.
5. **Primer sponsor visible en web** — Foto Jané (banner + logo SVG en galería, junio 2026).

**El detalle completo (timeline mes a mes, inventario de skills, decisiones y pendientes) está en `references/recap-actual.md`. Leerlo cuando la tarea toque un área concreta o Ana pida detalle.**

## Cómo usar esta skill (3 modos)

**Modo 1 — Arranque de sesión (silencioso).** Al empezar cualquier tarea del club, usar esta recapitulación como contexto de fondo: comprobar si lo que se pide ya existe, se decidió distinto, o encaja con una doctrina establecida (p. ej. no proponer carruseles como motor de crecimiento: contradice `crecimiento-ig-cbgb`). No recitar la recapitulación a Ana; simplemente trabajar informada.

**Modo 2 — Pregunta directa.** Si Ana pregunta qué se ha hecho, cuándo se hizo algo o dónde se quedó un tema: responder desde `references/recap-actual.md`, corto y al grano, con fechas. Si el detalle no está ahí, reconstruirlo (ver fuentes abajo) y **aprovechar para actualizar la recapitulación**.

**Modo 3 — Informe para Junta.** Si pide un resumen de actividad presentable: formato dossier corto (contexto / hitos / impacto / siguiente paso), tono institucional, cero relleno — el formato de `mi-rol-coordinadora`. La recapitulación es la materia prima; el informe se redacta a medida.

## Protocolo de mantenimiento (lo que hace que esté "siempre presente")

Una memoria que no se actualiza caduca en un mes. Por eso el mantenimiento es parte de la skill:

1. **Al cerrar un trabajo significativo** (nueva skill, sección web, campaña, dossier, decisión doctrinal): añadir una entrada de 1-3 líneas en el mes correspondiente de `references/recap-actual.md` — qué se hizo, fecha y dónde vive (skill, URL, carpeta). Los micro-ajustes (typos, una foto subida) no se anotan.
2. **Ventana rodante:** al tocar el archivo, si el mes más antiguo supera los 6 meses, moverlo a la sección "Archivo (fuera de ventana)" al final del archivo — se resume en 2-3 líneas, no se borra: la historia del club también es un activo.
3. **Actualizar la fecha de "última actualización"** en la cabecera del archivo.
4. **Fuentes para reconstruir o verificar** si algo falta:
   - `git log` del repo `cbgrupbarna-info` (la web y sus fechas exactas).
   - El listado de skills instaladas y sus descripciones (el ecosistema y sus doctrinas).
   - Las propias skills satélite: cada una documenta las decisiones de su área.

## Relación con otras skills

- `arranque-eficiente` manda leer primero la skill que toca: esta recapitulación es el **paso cero** de ese protocolo (contexto antes que nada).
- `/cbgb` enruta la tarea a la satélite correcta; esta skill dice **qué ya existe** para que el enrutado no reinvente nada.
- `mi-rol-coordinadora` define el formato de entrega de los informes del Modo 3.
