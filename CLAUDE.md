# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Arquitectura del repositori

Aquest repositori és un monorepo estàtic per al web del **CB Grup Barna** (club de bàsquet base, Barcelona, 1965). Conté múltiples microsites independents:

| Directori | Tecnologia | URL de producció |
|-----------|-----------|-----------------|
| `/` (arrel) | HTML/CSS/JS estàtic, sense build | https://cbgrupbarna.info/ |
| `galeria/` | Next.js 14 + Supabase + Tailwind | Vercel (deploy independent) |
| `galeria-3x3-glories/` | HTML estàtic | https://cbgrupbarna.info/galeria-3x3-glories/ |
| `premidonaesport/` | HTML estàtic multi-pàgina | https://cbgrupbarna.info/premidonaesport/ |
| `orgull/` | HTML estàtic | https://cbgrupbarna.info/orgull/ |
| `ruleta-3x3/` | HTML estàtic | https://cbgrupbarna.info/ruleta-3x3/ |

## Font de dades canònica

**`data.json`** és el hub central de dades del club. Totes les apps en llegiran. Quan canviï qualsevol dada (places campus, stats, events, contactes), actualitza **únicament** aquest fitxer — no dupliquis dades als HTMLs.

Camps principals: `club`, `temporada`, `campus.weeks[]`, `tres_x_tres`, `events.calendari[]`, `contactesClub`, `patrocinadors`.

Actualitza sempre `lastUpdate` en format ISO `2026-XX-XXTXX:XX:XX+02:00` quan modifiquis el fitxer.

## La portada (`index.html`)

Fitxer monolític de ~1658 línies. Tot el CSS i el JS és inline (no hi ha bundler). Estructura interna:
- **Ticker** (línies ~896–907): barra de novetats superior, duplicada per fer l'efecte de bucle
- **Top-grid**: cards de prioritat alta (Portes Obertes, Campus, 3x3, Escoleta)
- **Social grid**: tiles d'Instagram incrustats, configurats des de `social-grid.json`
- **Feed de contingut**: news, patrocinis, streaming

Els colors principals estan com variables CSS: `--red`, `--green`, `--yellow`, `--blue`.

## Galeria Next.js (`galeria/`)

```bash
cd galeria
npm install
npm run dev      # http://localhost:3000
npm run build
npm run lint
```

Requereix un fitxer `.env.local` amb:
```
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
```

**Rols d'usuari Supabase**: `viewer` / `contributor` / `editor` / `admin`. Per donar permisos admin, canvia el `role` a la taula `profiles` directament via Supabase Table Editor.

**Schema de la BD** a `galeria/supabase/schema.sql`. Taules principals: `profiles`, `seasons`, `events`, `photos`.

**App Router** (Next.js 14): les rutes estan a `galeria/src/app/`. Les rutes de l'admin estan sota `galeria/src/app/admin/`.

## Skills disponibles

| Skill | Quan usar |
|-------|-----------|
| `/update-campus` | Actualitzar places del campus a `data.json` |
| `/update-ticker` | Canviar missatges del ticker a `index.html` |
| `/add-event` | Afegir event nou al calendari a `data.json` |
| `/deploy-web` | Commit + push dels canvis al repositori |

## Idioma i to

- La web és en **català** (principal) i castellà (parcial)
- Tots els textos públics nous han de ser en català
- El ticker va sempre en **MAJÚSCULES**
- CTAs principalment via WhatsApp (+34 698 425 153)

## Deploy

- **Arrel i microsites estàtics**: s'publiquen automàticament via GitHub Pages (CNAME apunta a `cbgrupbarna.info`)
- **Galeria**: deploy independent a Vercel, vinculat al directori `galeria/`
- La branca de desenvolupament activa és `claude/fashion-sales-strategy-tpe252`
