# Portar cbgrupbarna.com cap a cbgrupbarna.info

La web antiga (`cbgrupbarna.com`, WordPress a Webempresa) **encara respon i
encara s'indexa**. No té cap `canonical` cap a la nova, el seu `robots.txt` ho
permet tot i el seu títol és «Bàsquet al barri del Clot», que persegueix les
mateixes cerques que perseguim nosaltres. Per a Google, doncs, hi ha dos clubs
amb el mateix nom competint entre ells — i el que hi porta deu anys és el que
ja no mantenim.

`redireccions.htaccess` ho resol: es puja a l'arrel del `.com` i cada adreça
antiga passa a la pàgina de la nova que tracta el mateix tema.

## Què hi ha a dins

341 regles, cobrint les **344 adreces** que existeixen de veritat a la web
antiga: 19 pàgines i 325 notícies publicades entre 2016 i 2026, tretes de la
seva pròpia API de WordPress.

| Cap a | Quantes | Què hi va |
|---|---|---|
| `/partits/` | 135 | Cròniques, resultats i calendaris |
| `/premsa/` | 113 | Notícies sense equivalent temàtic |
| `/fotos/` | 29 | Galeries d'imatges |
| `/documents/` | 15 | Assemblees, acords i convocatòries |
| `/campus/` | 10 | Campus, stages i tecnificació |
| `/escoleta/` | 9 | Escola i portes obertes |
| `/partits/equips/` | 7 | Presentacions i plantilles |
| `/3x3/` | 6 | 3x3 i Westfield Glòries |
| `/femeni/` | 1 | La secció femenina |

## Per què no es mana tot a la portada

Seria una regla en comptes de 341. Però Google llegeix un 301 massiu cap a la
portada com un error disfressat — un *soft-404* — i llavors no traspassa
gairebé res de l'autoritat que volíem heretar. Una notícia de fa vuit anys
sobre un partit ha d'anar a la pàgina de partits, no a la portada.

Pel mateix motiu, el que no encaixa amb cap regla **segueix donant 404**. És la
resposta honesta per a una adreça que no ha existit mai.

## L'ordre de les regles no és decoratiu

Totes porten `[L]` i guanya la primera que encaixa. Està pensat perquè una
crònica vagi a `/partits/` encara que parli d'un equip femení: a `/femeni/` hi
va el que tracta de la secció en si, no els resultats. Si hi toques res,
recorda-ho.

## Abans de pujar-lo

- **Baixa't els documents del `.com` que la web nova encara no té.** N'hi ha a
  la biblioteca de mitjans que no estan enllaçats des de cap pàgina i que, un
  cop redirigit tot, no es podrien recuperar per web.
- **No donis de baixa ni el domini ni l'allotjament.** Un 301 només traspassa
  autoritat mentre segueix responent. Això es queda posat.

## Com comprovar que ha anat bé

Un cop pujat, unes quantes adreces a mà:

```
curl -sI https://cbgrupbarna.com/club/historia-del-cb-grup-barna/ | head -3
curl -sI https://cbgrupbarna.com/documents/ | head -3
curl -sI https://cbgrupbarna.com/aixo-no-ha-existit-mai/ | head -3
```

Les dues primeres han de dir `301` i portar a `cbgrupbarna.info`. **La tercera
ha de dir 404**: si retorna un 301, alguna regla és massa àmplia.
