# Recapitulación detallada — últimos 6 meses de trabajo en Claude

**Ventana actual:** ~febrero 2026 → julio 2026
**Última actualización:** 2026-07-22
**Cómo mantener este archivo:** ver "Protocolo de mantenimiento" en `../SKILL.md`.

---

## 1. Ecosistema de skills del club (construido a lo largo del periodo)

Unas **35 skills** organizadas en capas, orquestadas por la mestra `/cbgb`. Es el activo más importante del periodo: convierte a Claude en un departamento de marketing con criterio propio del club.

| Capa | Skills | Qué aportan |
|---|---|---|
| Núcleo / método | `cbgb` (mestra), `mi-rol-coordinadora`, `ana-innovacio-barna`, `arranque-eficiente` | Enrutado de tareas, rol y formato de Ana, ángulo innovador obligatorio, disciplina de arranque y ahorro de tokens |
| Sistema visual y carteles | `sistema-visual-cbgb`, `disseny-cartells-cbgb`, `produccio-cartells`, `portada-reels-cbgb` | Tokens de marca exactos, criterio de cartel élite, producción (Canva/código), portadas 9:16 de reels |
| Reels y vídeo | `reels-cbgb`, `ganxos-cbgb`, `arrencada-reels-cbgb`, `reel-fotos-cbgb`, `reel-illustrat-cbgb`, `video-club-cbgb`, `video-estrella-cbgb`, `cinema-estrelles-cbgb`, `efecto-brutalismo-cbgb`, `capcut-pro-cbgb`, `capcut-reels-cbgb` | Qué grabar, cómo enganchar (hook 2 seg), control de calidad, montaje por código (Python/ffmpeg) y en CapCut, piezas premium estilo Nike |
| Crecimiento IG | `crecimiento-ig-cbgb`, `aparador-ig-cbgb`, `aparador-perfil-cbgb` | Doctrina con datos reales Q2 2026; el aparador del perfil (bio, pins, primeros 9) como palanca de conversión |
| Benchmarks | `benchmark-barca-basket-cbgb`, `benchmark-clubs-barri-cbgb`, `benchmark-clubs-femenins-cbgb`, `benchmark-pau-gasol-academy-cbgb` | Cómo lo hacen Barça Basket, rivales de barrio (SESE, Horta, Roser), Liga Femenina y Pau Gasol Academy, traducido a jugadas CBGB |
| Códigos de lujo | `codis-lux-cbgb` (fusión de Dior, Vogue, Elie Saab, Bvlgari, Jordan Roth), `luxury-logic-cbgb` | Lógica de deseo y pertenencia de marca de lujo aplicada a escala de barrio |
| Sponsors | `patrocinis-club`, `captacio-pack-cbgb` | Estrategia Oro/Plata/Bronce, dossier, targets, scripts; pack de producción (Word + PPTX + Excel con pipeline) |

Decisión de arquitectura del periodo: las 5 skills de códigos de lujo individuales se **fusionaron en `codis-lux-cbgb`** para reducir carga de contexto.

## 2. Doctrinas y decisiones establecidas (no contradecir sin nueva evidencia)

- **Crecimiento IG (Q2 2026, datos propios):** ~439K visualizaciones/mes con solo **0,03 % de conversión** a seguidores → el cuello de botella es la CONVERSIÓN, no el alcance. Palanca grande: el aparador del perfil (bio canónica, 3 pins, primeros 9), no producir más.
- **El motor es el REEL**, no el carrusel. Métricas que mandan: guardados, compartidos, % alcance a no-seguidores. Métricas que engañan: likes, vistas totales.
- **El ganxo (hook) de los 2 primeros segundos** es palanca de coste cero (`ganxos-cbgb`).
- **Posicionamiento vs rivales de barrio:** de "club" a **medio/tribu de barrio** (tesis de `benchmark-clubs-barri-cbgb`); CBGB se comporta como el medio oficial de su propio mundo (modelo Vogue).
- **Sponsors:** no se vende espacio publicitario, se vende **pertenencia al barrio**; niveles Oro/Plata/Bronce, foco en colaboraciones en especie.
- **Identidad:** club de baloncesto más grande de Barcelona, +450 familias, paridad real masculina/femenina (sección LF2). Toda propuesta debe estar a esa altura.
- **Método de trabajo:** leer la skill que toca ANTES de producir; mínimo de tokens; entregable > explicación (`arranque-eficiente`). Todo output pasa el filtro de 5 puntos de `/cbgb` (funnel, pilar, activo, revenue, defendible en Junta).

## 3. Timeline de la web cbgrupbarna.info (repo `voluntarisgrupbarna-pixel/cbgrupbarna-info`)

### Mayo 2026 — nace el portal
- **2 may:** primer commit — portal cbgrupbarna.info (link-in-bio + dossier Premi Dona i Esport) en GitHub Pages con dominio propio. El mismo día: rediseño con dashboard **"Lo Calent"** (status badges, ticker), hero Portes Obertes, SEO + GA4 + JSON-LD + sitemap, embeds de Instagram, y **GitHub Action horaria** que actualiza `data.json` desde JotForm (límite 50/semana).
- **3 may:** vCard descargable para la lista de difusión de WhatsApp.
- **12 may:** SEO bilingüe CA/ES, Social Proof Wall, sección de sponsors, social grid de Instagram, countdown 3x3, parches de rendimiento.
- **17 may:** `data.json` expandido como **hub de datos compartido del club**.
- **21–26 may:** **ruleta interactiva 3x3 Westfield Glòries 2026** — premios con algoritmo ponderado, códigos por premio, límite de tiradas por email, formulario de registro con backend en Apps Script, normas del sorteo (1500 tiradas/día), paso TikTok, auto-relleno del formulario.

### Junio 2026 — galería, mascota, admin y primer sponsor
- **3 jun:** landing **Mes de l'Orgull 2026** (PR #1).
- **10–11 jun:** nueva portada, sección **Fotos d'Esdeveniments** con galería 3x3 y lead-gate reorientado a **suscripción newsletter** (captura datos completos: club, IG, evento), dashboard del campus con 6 sesiones/overbooking/plazas, protección por código de acceso en `premidonaesport`.
- **12–13 jun:** página de la **mascota** con vídeo animado y reels 1080x1920 en catalán y castellano (voz en off, subtítulos, mejora de audio EQ/reverb; después versiones con voces profesionales sin voz robótica). **Panel de administración** para crear eventos y subir fotos (PR #5), galería estática `/fotos`, sistema de **access gate** (PIN + newsletter) con `config.js`, herramienta de migración desde Flickr y soporte flickr-embed.
- **14–18 jun:** enlace a galería y SEO en portada (primer fold), soporte de subida por **ZIP** en el admin (JSZip), eventos publicados: Cistella Petita 2a Edició, Fotos Equips Temporada 25-26, Senior Femení Sessió Instax. **Primer sponsor visible: Foto Jané** (banner + logo SVG en la galería).

### Julio 2026
- **22 jul:** creada esta skill de recapitulación (`recapitulacion-6-meses`) como memoria viva del proyecto.

## 4. Estado actual y frentes abiertos

- **Web:** operativa en producción (GitHub Pages + dominio propio). Última actividad de contenido: 18 jun (galería/eventos). Ramas abiertas sin fusionar: `fix/mascota-reel-frame0`, `fix/unmute-voice`.
- **IG:** doctrina definida; la ejecución del aparador (bio canónica, pins, primeros 9 de `aparador-perfil-cbgb`) es la palanca pendiente de explotar de forma continua.
- **Sponsors:** sistema completo (estrategia + pack de producción); Foto Jané como primera colaboración visible en web.
- **Verano:** periodo natural de campus y preparación de temporada 26-27 — material de benchmark de campus en `benchmark-pau-gasol-academy-cbgb`.

## Archivo (fuera de ventana)

*(Vacío por ahora. Cuando un mes supere los 6 meses de antigüedad, resumirlo aquí en 2-3 líneas en lugar de borrarlo.)*
