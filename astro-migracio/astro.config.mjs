import { defineConfig } from 'astro/config';

// Prova de concepte de migracio (Fase 3): una sola font de contingut
// generant ca (arrel), es i en com a Astro fa nativament amb i18n routing.
export default defineConfig({
  site: 'https://cbgrupbarna.info',
  outDir: './dist',
  i18n: {
    defaultLocale: 'ca',
    locales: ['ca', 'es', 'en'],
    routing: {
      prefixDefaultLocale: false, // ca a l'arrel, com ara; es/ i en/ amb prefix
    },
  },
});
