# Preguntas abiertas e inconsistencias

Lo que **no** sabemos todavía o no cuadra. Se cierra una entrada moviendo la
conclusión a `lleis.csv` / `decisions.csv` y borrándola de aquí.

## Inconsistencias a resolver

| # | Qué no cuadra | Impacto | Cómo se cierra |
|---|---|---|---|
| **O-01** | El rojo de marca: `benchmark-clubs-barri-cbgb` dice `#CC0000`; el resto del ecosistema usa `#E63329` | Alto — afecta a toda pieza gráfica | Abrir `tokens.conf` (fuente de verdad de `sistema-visual-cbgb`), fijar el valor y corregir la skill desviada |
| **O-02** | `assets/tokens.conf` no está en la carpeta de `sistema-visual-cbgb`: la skill apunta a un archivo que no acompaña | Alto — nadie puede verificar un token | Localizarlo en el knowledge "Barna" y dejarlo junto a la skill |
| **O-03** | `aparador-perfil-cbgb` y `aparador-ig-cbgb` cubren lo mismo en dos idiomas | Medio — carga de contexto duplicada y riesgo de divergencia | Fusionar en una, como se hizo con `codis-lux-cbgb` |
| **O-11** | **9 skills están referenciadas pero NO instaladas**: `cb-grup-barna`, `mi-rol-coordinadora`, `millorar-club-top-bcn`, `disseny-estetic-club`, `psicologia-social-club`, `referent-basquet-espanyol`, `crear-apps-webs-club`, `xarxes-socials-club`, `guions-virals-cbgb` | **Alto** — `/cbgb` enruta a skills que no existen, y `arranque-eficiente` obliga a entrar por ahí | Recuperarlas o quitar la referencia. Ver `bbdd/skills.csv` (estado `FALTA`). Mientras tanto, `/cbgb` las marca con ⚠️ para que se avise en vez de improvisar |
| **O-14** | Las skills viven en `~/.claude/skills/`**`synced/`** y las gestiona una sincronización externa: el 13/08 ese directorio se reorganizó y el enrutado de `/cbgb` que habíamos actualizado volvió a la versión antigua | **Alto** — cualquier edición hecha en `synced/` se pierde sin avisar | La copia canónica de `cbgb/SKILL.md` es la del repo (`.claude/skills-backup/`). Tras cada sync: comparar, **fusionar** (no sobrescribir: el sync también trae mejoras de verdad) y volver a copiar. **Nunca sincronizar backup→repo a ciegas**: mirar `git diff` antes de commitear |
| **O-15** | `doctrina-juliol-2026-cbgb` y `memoria-cbgb` viven fuera de `synced/` sin backup automático: el 29/08, tras un reinicio de contenedor, **habían desaparecido por completo** de `~/.claude/skills/` | **Confirmado** — ya no es hipótesis: el riesgo que anunciaba el README del backup se materializó | Restauradas desde `.claude/skills-backup/` el mismo día. **Comprobar su presencia en cada actualización de conocimiento**, no solo tras un aviso de reorganización — un reinicio de contenedor no avisa |

**Cerradas** — se dejan escritas con su fecha, no se borran:

| # | Qué era | Cómo se cerró |
|---|---|---|
| ~~O-12~~ | El ecosistema vivía en `~/.claude/skills/` sin control de versiones | **2026-07-29**: espejado en `.claude/skills-backup/` del repo (36 skills) y pusheado a GitHub |
| ~~O-13~~ | El índice de `/cbgb` no incluía ninguna skill de julio | **2026-07-29**: tabla de enrutado rehecha + flujo "Publicar un reel (la cadena de conversión)" |

## Datos por confirmar

| # | Dato | Estado | Cómo se cierra |
|---|---|---|---|
| **O-04** | Las ~500 visualizaciones del reel Campus están **inferidas** de la tasa de comentarios (1 ≈ 0,2 %) | Sin confirmar — **no citar en Junta** | Abrir Insights del reel y sustituir el valor en `reels.csv` |
| **O-05** | Junio fue mes de 3x3 + Campus + CAMPEONES: cuánto del salto es formato y cuánto estacionalidad | Confundido | Un mes sin evento grande con el mismo mix de reels. Si aguanta, L-10 pasa a confianza alta |
| **O-06** | Benchmark propio de arrancadas: `reels.csv` tiene **n = 1** | Insuficiente | 10 filas. Una por reel publicado, a 24-48 h |
| **O-07** | Cifras de seguidores de los clubes rivales: fuente no verificada y volátil | **No citar** en dossier ni ante prensa | Captura propia y fechada de cada perfil |

## Hipótesis a testear

| # | Hipótesis | Prueba limpia |
|---|---|---|
| **O-08** | Arreglar el aparador multiplica ×3-×5 la conversión sin producir más | Cerrar agosto con producción **igual o menor** que julio y mirar si la conversión sube desde 0,03 % |
| **O-09** | Las series "El Clot juga" y "Pregunta tàctica" son las que traen no-seguidores | Etiquetar cada reel con su serie en `reels.csv` y cruzar con volumen de externos |
| **O-10** | El reveal invertido de `efecto-brutalismo-cbgb` convierte mejor que un fichaje estático | Un fichaje con cada formato y comparar guardados y compartidos |
