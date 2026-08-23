# Proves del cercador

Tres suites, i cadascuna respon una pregunta diferent.

```bash
python3 -m http.server 8899 &        # cal per a la d'ús
node tests/cerca/prova-motor.mjs     # 50 casos · no s'ha de trencar mai
node tests/cerca/prova-contingut.mjs # 85 consultes reals · on no arribem
node tests/cerca/prova-ux.mjs        # 39 comprovacions · es pot fer servir?
```

| Suite | Pregunta que respon | Quan falla vol dir |
|---|---|---|
| `prova-motor.mjs` | Els casos que sabem que han de sortir bé, ¿surten bé? | S'ha trencat alguna cosa. **Arreglar-ho.** |
| `prova-contingut.mjs` | Com escriu la gent de debò i què hi troba | Sol ser un **forat de contingut**: falta una pregunta a `i18n/faq.yml`. Rarament és el motor. |
| `prova-ux.mjs` | Es pot fer servir amb teclat, amb el dit i amb lector de pantalla? | Un problema d'accessibilitat o de navegació. |

Les dues primeres no necessiten navegador: carreguen `js/cerca.js` en un
`vm` de Node amb l'índex real. La tercera obre Chromium.

## Què ha sortit d'aquí

- **El focus s'escapava del diàleg.** Catorze tabulacions i eres a la pàgina
  de sota, sense veure-la. Va sortir de `prova-ux.mjs`; ara hi ha trampa de
  focus.
- **Respostes que no tocaven.** `prova-contingut.mjs` va ensenyar que
  «qui és el president» responia *«Qui hi pot jugar?»* i «com em faig
  entrenador», *«Com em faig patrocinador?»*. La causa era comptar totes les
  paraules igual: casava «qui» o «faig» i es donava per satisfeta. Ara cada
  paraula pesa segons com de rara sigui al corpus de preguntes, i **la més
  distintiva de la consulta ha de sortir per força**.
- **El llindar no es podia pujar.** Semblava que amb un número més alt
  n'hi hauria prou. No: mesurat sobre les 85 consultes, les puntuacions de
  les bones i les dolentes se solapen —«where do they train» és bona i fa
  8,6; «quant val la temporada» és dolenta i fa 9,5—. Qui separa les dues
  famílies és l'estructura de la consulta, no una xifra.

## Com llegir `prova-contingut.mjs`

Cada cas diu què ha de passar: `'resposta'` (ha de sortir la resposta escrita
a dalt), una ruta (ha de ser entre les 3 primeres), `'res'` (no ha de tornar
res) o `null` (només informe, per veure què fa avui).

El resum del final és el que val la pena mirar de tant en tant: **quantes
consultes es responen i quantes només enllacen**. Cada una que només enllaça
és una candidata a pregunta nova.
