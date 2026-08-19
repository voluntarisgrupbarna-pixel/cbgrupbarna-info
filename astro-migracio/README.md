# Prova de concepte Astro (Fase 3)

**Això NO és el lloc en producció.** cbgrupbarna.info es continua servint des de
l'arrel del repositori tal com sempre. Aquest directori és un projecte Astro
aïllat, provant si soluciona el problema real: `/femeni/` i les seves
traduccions ja s'han desincronitzat perquè cada versió és un HTML clonat a mà.

## Què demostra

`/instal-lacions/` ca/es/en generat des d'**una sola font**:

- `src/data/instalacions.json` — dades que no canvien per idioma (nom, adreça, mapa)
- `src/i18n/instalacions.ts` — textos traduïts (títol, descripcions, etiquetes)
- `src/components/InstalacionsPage.astro` — l'ÚNICA plantilla
- `src/pages/instal-lacions/`, `src/pages/es/instal-lacions/`,
  `src/pages/en/instal-lacions/` — tres fitxers de 3 línies cada un, que
  només diuen "renderitza la plantilla en aquest idioma"

Canviar una descripció es fa **un cop**, a `instalacions.ts`, i surt actualitzada
als tres idiomes en el següent build. Avui, al lloc real, calen tres edicions
manuals — i per això `/femeni/` ja ha divergit de les seves traduccions.

## Provar-ho

```bash
cd astro-migracio
npm install
npm run build      # genera dist/instal-lacions/, dist/es/instal-lacions/, dist/en/instal-lacions/
npm run dev        # servidor local per veure-ho abans de fer build
```

## Què falta per a la migració real (no és feina d'aquesta setmana)

1. **Migrar tot el contingut real**, pàgina a pàgina, al patró
   dades+traduccions+plantilla — és la feina gran, setmanes, no dies.
2. **Preservar totes les URL existents** (SEO): cap redirecció trencada.
3. **Portar el CSS de marca real** (`css/barna.css`, Anton + Inter, `#E20613`) —
   aquí hi ha estils mínims només per provar el mecanisme.
4. **JSON-LD i SEO** (hreflang, canonical, sitemap) automatitzats des de la
   mateixa font, no repetits a mà com ara.
5. **Decidir el tall**: build i desplegament via GitHub Actions cap a
   GitHub Pages, substituint els fitxers estàtics actuals — un canvi
   d'infraestructura real, es fa amb temps i es revisa abans de publicar-se.
6. **Migrar els generadors ja existents** (`scripts/build-pages.py`,
   `.github/scripts/generate-team-pages.py`) a aquest sistema, no deixar-los
   coexistint amb Astro.

Fase 3 de la proposta "Web 10" continua sent on passa tot això. El que hi ha
aquí és la prova que l'enfocament funciona, no la migració feta.
