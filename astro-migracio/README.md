# Prova de concepte Astro (Fase 3)

**Això NO és el lloc en producció.** cbgrupbarna.info es continua servint des de
l'arrel del repositori tal com sempre. Aquest directori és un projecte Astro
aïllat, provant si soluciona el problema real: `/femeni/` i les seves
traduccions ja s'han desincronitzat perquè cada versió és un HTML clonat a mà.

## Què demostra

**Cas 1 — `/instal-lacions/`** ca/es/en des d'**una sola font**:

- `src/data/instalacions.json` — dades que no canvien per idioma (nom, adreça, mapa)
- `src/i18n/instalacions.ts` — textos traduïts (títol, descripcions, etiquetes)
- `src/components/InstalacionsPage.astro` — l'ÚNICA plantilla
- `src/pages/instal-lacions/`, `src/pages/es/instal-lacions/`,
  `src/pages/en/instal-lacions/` — tres fitxers de 3 línies cada un, que
  només diuen "renderitza la plantilla en aquest idioma"

**Cas 2 — `/femeni/`**, el cas real més difícil (529 línies, estadístiques,
3 pilars i FAQ): `src/i18n/femeni.ts` + `src/components/FemeniPage.astro`.
La part que importa: **el JSON-LD `FAQPage` es genera automàticament des del
mateix array `faq`** de cada idioma — no s'escriu a mà. Verificat amb
`npm run build`: les 5 preguntes i respostes surten correctes i diferents a
`dist/femeni/`, `dist/es/femeni/` i `dist/en/femeni/`. Avui, al lloc real,
aquest JSON-LD es manté a mà en cada idioma i és exactament el tipus de cosa
que es desincronitza en silenci.

Canviar un text es fa **un cop**, al fitxer `.ts` corresponent, i surt
actualitzat als tres idiomes (contingut visible i schema) en el següent
build. Avui, al lloc real, calen tres edicions manuals — i per això
`/femeni/`, `/es/baloncesto-femenino/` i `/en/womens-basketball/` ja han
divergit (veure `PENDENTS-WEB.md`).

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
