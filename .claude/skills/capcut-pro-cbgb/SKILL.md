---
name: capcut-pro-cbgb
description: >
  Guia completa de CapCut Pro per al CB Grup Barna. S'activa automàticament quan
  la conversa implica editar vídeo amb CapCut: muntar highlights, reels, rols,
  clips de campus, vídeos d'equip, exportació, subtítols, efectes, IA, keyframes,
  màscares, tracking, color, àudio. Complementa video-club-cbgb (automatització ffmpeg)
  i reels-cbgb (estratègia) — no els duplica.
triggers:
  - capcut
  - editar vídeo
  - muntar vídeo
  - highlight
  - reel vertical
  - subtítols automàtics
  - keyframe
  - màscara
  - tracking
  - exportació vídeo
  - efecte de so
  - color grading
  - vídeo equip
  - clip campus
---

# Skill: CapCut Pro — CB Grup Barna

## Quan s'activa
Qualsevol feina d'edició de vídeo amb l'app CapCut: muntatge, efectes, subtítols,
àudio, exportació, funcions d'IA, keyframes, màscares, tracking de moviment.

## Ecosistema de skills del club
| Necessitat | Skill |
|---|---|
| Estratègia de contingut i reels | `reels-cbgb` |
| Automatització amb ffmpeg/bash | `video-club-cbgb` |
| **Editar a mà amb CapCut** | **`capcut-pro-cbgb`** ← aquí |
| Estètica visual, colors, disseny | `disseny-estetic-club` |
| Jugadores estrella, destacades | `video-estrella-cbgb` |

---

## Flujo de treball de 9 passos (projecte nou)

1. **Importar material** → Nou projecte › Afegir › seleccionar clips/fotos/àudio
2. **Tallar i ordenar** → arrossegar clips a la línia de temps, tallar amb la tisora, reordenar
3. **Subtítols** → Text › Subtítols automàtics › revisar i corregir cada línia manualment
4. **Àudio** → Afegir música (biblioteca lliure de drets) + ajustar volum + efectes de so
5. **Efectes visuals** → Efectes › aplicar transicions, filtres de color, overlays
6. **Keyframes i animació** → seleccionar clip › Keyframe › definir posició/escala/opacitat en el temps
7. **Màscares i tracking** → Retoc › Màscara o Tracking de moviment per a zones específiques
8. **Color i grading** → Ajustar › Brillantor / Contrast / Saturació / HSL / LUT
9. **Exportar** → icona de compartir › 1080p o 4K › 30fps (reels) o 60fps (acció viva) › H.264

---

## Regles no negociables del club

- **Subtítols**: sempre revisats manualment, mai publicar els automàtics sense correcció
- **Cares**: no aplicar filtres de retoc facial (bellesa, pell) sense consentiment explícit
- **Menors**: no mostrar cares de menors sense autorització escrita dels tutors
- **Música**: només biblioteca CapCut (lliure de drets) o àudio autoritzat pel club; mai música de Spotify/YouTube sense llicència
- **Privacitat**: no publicar vídeos amb dades personals visibles (DNI, telèfon, adreça)
- **Marca**: watermark o logo del club sempre visible en contingut oficial

---

## Atajos de criteri ràpid

| Situació | Decisió |
|---|---|
| Clip llarg de partit → reel 30s | Tallar als 3 millors moments; prioritzar cistella + reacció |
| Exportar per a Instagram Reels | 1080×1920, 30fps, màx 90s, H.264 |
| Exportar per a YouTube | 1920×1080 o 1080×1920, 60fps si acció viva, H.264 |
| Exportar per a WhatsApp club | 720p, 30fps, <50 MB |
| Subtítols no reconeixen el català | Corregir manualment; usar "Idioma: català" a la configuració |
| Keyframe vs transició | Keyframe per a moviment controlat; transició per a tall simple |
| Tracking perd la jugadora | Reduir la zona de tracking; usar màscara manual com a alternativa |

---

## Referència ràpida de funcions

Veure `references/funciones.md` per al catàleg complet per blocs.
Veure `references/flujos-club.md` per a recetes tancades per tipus de peça.
Veure `references/exportacion-checklist.md` per a ajustos d'exportació i checklist final.
Veure `scripts/` per a eines de suport (tallador de partits, presets).
