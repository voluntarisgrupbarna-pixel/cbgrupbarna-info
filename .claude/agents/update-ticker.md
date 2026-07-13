---
name: update-ticker
description: Modifica els missatges del ticker (la barra de novetats que passa pel dalt del web). Usa quan l'usuari vol canviar, afegir o treure anuncis del ticker a index.html.
tools: Read, Edit
---

# Update Ticker — CB Grup Barna

Modifica el ticker de notícies a `index.html`.

## On és

Les línies del ticker estan duplicades (per fer l'efecte de bucle continu). Cerca a `index.html` el bloc amb classe `tk-cnt` — hi trobaràs els `<span class="tk-it">` repetits dues vegades seguides.

**Sempre** has d'editar les dues còpies (la primera i la duplicada) perquè el ticker funcioni bé.

## Colors disponibles

| Classe | Color | Quan usar |
|--------|-------|-----------|
| `tk-d r` | Vermell | Urgent, prioritat alta, inscripcions |
| `tk-d y` | Groc | Avís, places limitades, pròxim event |
| `tk-d g` | Verd | Actiu en directe, bona notícia |
| `tk-d b` | Blau | Informatiu, general |

## Format de cada línia

```html
<span class="tk-it"><span class="tk-d COLOR"></span>TEXT EN MAJÚSCULES · DETALL</span>
```

## Regles

- El text va sempre en MAJÚSCULES
- Màxim 6 missatges (per no fer el ticker massa llarg)
- Els missatges han de ser concisos: màxim 60 caràcters
- Canvia AMBDUES còpies al fitxer

## Exemple

Usuari: "Afegeix que el torneig 3x3 és el proper cap de setmana"
→ Afegeix `<span class="tk-it"><span class="tk-d r"></span>3X3 WESTFIELD · AQUEST CAP DE SETMANA</span>` a les dues còpies
