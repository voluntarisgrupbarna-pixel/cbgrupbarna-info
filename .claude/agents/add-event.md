---
name: add-event
description: Afegeix un nou event al calendari del club a data.json. Usa quan l'usuari vol registrar un torneig, jornada, campanya, campus o qualsevol activitat nova al club.
tools: Read, Edit, Bash
---

# Add Event — CB Grup Barna

Afegeix un event nou a `data.json` dins de `events.calendari[]`.

## Camps de cada event

```json
{
  "id": "identificador-unic-sense-espais",
  "nom": "Nom de l'event",
  "inici": "YYYY-MM-DD",
  "final": "YYYY-MM-DD",
  "tipus": "torneig | campus | jornada | campanya | altre"
}
```

## Tipus d'events

| tipus | Quan usar |
|-------|-----------|
| `torneig` | Competicions, 3x3, torneigs interns |
| `campus` | Campus d'estiu, hivern |
| `jornada` | Jornades de portes obertes, Little Basket Day |
| `campanya` | Campanyes temàtiques (Orgull, Nadal, etc.) |
| `altre` | Qualsevol cosa que no encaixi |

## Passos

1. Llegeix `data.json`
2. Demana a l'usuari si no tens: nom, dates d'inici i final, tipus
3. Genera un `id` en camelCase a partir del nom (sense accents, sense espais)
4. Afegeix l'objecte al final de `events.calendari[]`
5. Actualitza `lastUpdate` amb la data actual

## Exemple

Usuari: "Afegeix un torneig de Nadal del 20 al 22 de desembre"
→ Afegeix `{ "id": "torneiNadal", "nom": "Torneig de Nadal", "inici": "2026-12-20", "final": "2026-12-22", "tipus": "torneig" }`
