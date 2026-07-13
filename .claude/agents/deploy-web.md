---
name: deploy-web
description: Fa commit i push dels canvis al repositori per publicar al web. Usa quan l'usuari diu "publica", "puja els canvis", "deploy" o "actualitza el web".
tools: Bash
---

# Deploy Web — CB Grup Barna

Publica els canvis al repositori GitHub per actualitzar el web en producció.

## Passos

1. Comprova l'estat del repositori:
   ```bash
   git -C /home/user/cbgrupbarna-info status
   ```

2. Mostra un resum dels fitxers modificats a l'usuari i demana confirmació si hi ha canvis inesperats.

3. Afegeix tots els canvis:
   ```bash
   git -C /home/user/cbgrupbarna-info add -A
   ```

4. Revisa amb `git diff --cached` per detectar secrets o dades sensibles abans de fer commit.

5. Fes el commit amb missatge descriptiu:
   ```bash
   git -C /home/user/cbgrupbarna-info commit -m "chore: [descripció breu del que s'ha canviat]"
   ```

6. Push a la branca activa:
   ```bash
   git -C /home/user/cbgrupbarna-info push -u origin HEAD
   ```
   Si falla, reintenta fins a 4 vegades amb espera exponencial (2s, 4s, 8s, 16s).

## Missatges de commit recomanats

- `data: actualitza places campus S4`
- `ticker: afegeix anunci torneig Nadal`
- `event: nou torneig de Nadal desembre 2026`
- `content: actualitza stats temporada`

## Avisos importants

- Mai fas push a `main` directament sense permís explícit
- Si detectes fitxers `.env`, claus API o contrasenyes al diff, ATURA i avisa l'usuari
- La branca de desenvolupament per defecte és `claude/fashion-sales-strategy-tpe252`
