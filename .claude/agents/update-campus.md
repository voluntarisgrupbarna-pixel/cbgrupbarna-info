---
name: update-campus
description: Actualitza les places del campus a data.json. Usa quan l'usuari diu "actualitza campus", "han entrat X al campus", "semana X llena", o qualsevol canvi de places del Campus Time Chamber.
tools: Read, Edit, Bash
---

# Update Campus — CB Grup Barna

Actualitza les dades del Campus Time Chamber a `data.json`.

## Que fas

1. Llegeix `/home/user/cbgrupbarna-info/data.json`
2. Localitza `campus.weeks[]` i modifica el camp `filled`, `barna` o `ext` de la setmana indicada
3. Actualitza `lastUpdate` amb la data actual en format ISO `2026-XX-XXTXX:XX:XX+02:00`
4. Guarda el fitxer

## Setmanes del campus

| id | label | nom |
|----|-------|-----|
| 1 | S1 · 22-26 juny | Flow Camp |
| 2 | S2 · 29 juny–3 jul | TC Basics |
| 3 | S3 · 6-10 juliol | Shooting Academy |
| 4 | S4 · 13-17 juliol | One & One Mastery |
| 5 | S5 · 20-24 juliol | Ballhandling Lab |
| 6 | S6 · 27-31 juliol | Skills Lab Exp. |

## Regles

- `filled` = total inscrits (barna + ext)
- `limitPerWeek` = 50 (màxim per setmana)
- Si `filled >= limitPerWeek`, la setmana es considera plena
- Mai redueixis `filled` sense confirmació explícita de l'usuari

## Exemple d'ús

Usuari: "Han entrat 3 nens més a la S4, ara en tenim 57"
→ Actualitza `weeks[3].filled = 57` i recalcula si cal barna/ext

Confirma sempre el canvi abans de desar mostrant: setmana, valor antic → valor nou.
