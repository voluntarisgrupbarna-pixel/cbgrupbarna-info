# Plantilla "Producte del partner" — blog CB Grup Barna

Model: `donacio-flectomin-fardi-basquet-barna` (CA) / `donacion-flectomin-fardi-baloncesto-barna` (ES) / `flectomin-fardi-donation-basketball-barna` (EN).

Fer servir sempre que un patrocinador/col·laborador doni, cedeixi o patrocini un producte concret
(no una donació econòmica genèrica, sinó un producte amb marca i fabricant).

## Estructura obligatòria (3 idiomes: CA arrel `/blog/`, ES `/es/blog/`, EN `/en/blog/`)

1. **Capçalera SEO/GEO**: title, description, keywords, canonical, `hreflang` (ca/es/en/x-default).
2. **JSON-LD**: `BlogPosting` + `FAQPage` (5-8 preguntes) + `BreadcrumbList`, i afegir
   `"about": {"@type":"Product","name":"<producte>","brand":{"@type":"Organization","name":"<fabricant>"}}`
   dins del `BlogPosting`.
3. **Cos de l'article**:
   - Qui és el fabricant/marca (any de fundació, seu, activitat).
   - Què és el producte (composició/característiques, format, ús) — **sempre amb font** (web del
     fabricant, punts de venda, prospecte). Mai inventar dades.
   - La col·laboració amb el club (què s'ha donat/patrocinat i com s'utilitza).
   - **Avís legal si el producte és un medicament, complement alimentari o cosmètic**: aclarir que
     no és consell mèdic, que no substitueix una dieta equilibrada ni un professional sanitari si
     correspon, i mai fer alegacions de salut no acreditades (Reglament CE 1924/2006).
4. **FAQ visibles** (`<details>`) idèntiques a les del JSON-LD.
5. **Bloc de tancament — dades de contacte del partner (SEMPRE presents):**
   correu, web i Instagram (o altres xarxes) del fabricant/col·laborador. Si no es tenen tots,
   demanar-los abans de publicar; mai deixar-los en blanc ni inventar-los.
6. **Bloc de descompte (NOMÉS si el partner ofereix un descompte real):**
   afegir un botó/enllaç a la landing de descomptes (p. ex. el lloc Experience Cloud de
   Salesforce del club) **sempre que hi hagi descompte**. Si no hi ha descompte (cas Flectomin:
   donació pura, sense codi ni rebaixa), **no incloure aquest bloc** — no inventar-ne un.
7. Actualitzar `blog/index.html`: entrada nova al `blogPost` del JSON-LD + targeta nova a
   `.cards` (CA és l'idioma amb índex complet; ES/EN encara no tenen índex propi).
8. Publicar sempre per **branca + Pull Request** (mai directe a `main`), seguint
   `reference_cbgrupbarna_info_workflow` (gh api, no clonar).

## Checklist abans de publicar
- [ ] Dades del producte verificades (fabricant, composició/ús, format) amb font real.
- [ ] Avís legal si aplica (medicament/complement/cosmètic).
- [ ] Contacte del partner complet: mail + web + IG (o xarxa equivalent).
- [ ] Enllaç de descompte afegit **només si** n'hi ha un real, i amb la URL correcta.
- [ ] 3 idiomes amb `hreflang` creuat correcte.
- [ ] Article enllaçat des de `blog/index.html` (CA).
- [ ] Auditoria `seo-geo-aeo-cbgb/scripts/audit.sh` abans/després de publicar.
