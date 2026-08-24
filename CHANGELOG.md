# Versions · cbgrupbarna.info

Aquest repositori no tenia cap manera de dir «això és el que hi havia
publicat en tal data» més enllà del missatge de cada commit. A partir
d'aquí sí: cada versió és un punt fix del codi, amb el número escrit al
fitxer `VERSION` i explicat aquí.

**Com es numera.** `MAJOR.MENOR.PEDAÇ`, a l'estil habitual:

- **PEDAÇ** (1.0.**1**) — un arreglo o un contingut nou que no canvia com
  funciona res: una resposta del cercador, una traducció, una foto.
- **MENOR** (1.**1**.0) — una funcionalitat nova que s'afegeix sense
  trencar la que ja hi havia: el formulari de «no ho sabem», una secció
  nova.
- **MAJOR** (**2**.0.0) — un canvi que altera com es fa servir la web o
  com es treballa amb el repositori.

**Com es fa una versió nova.** S'actualitza `VERSION`, s'hi afegeix
l'entrada a dalt de tot d'aquest fitxer amb la data i el resum, i es
puja a `main` en el mateix commit. La versió és el commit; el número
només l'hi posa nom.

---

## 1.0.1 — 2026-08-24

Documentat a `PENDENTS-WEB.md` que aquest sistema de versions existeix i per
què és un fitxer i no un tag de git. Cap canvi de codi.

## 1.0.0 — 2026-08-24

Primera versió fixada. Marca l'estat del repositori just després de
publicar el cercador intel·ligent del web: FAQ trilingüe des d'una font
única (`i18n/faq.yml`), motor de cerca amb tolerància a faltes i
sinònims, i un formulari de contacte quan no hi ha resposta escrita.

Commit: `205f0861`

Comprovacions en aquell moment: motor 74/74 · contingut 95/95 · ux
56/56 · i18n-lint 0 errors · paritat de tres idiomes correcta.
