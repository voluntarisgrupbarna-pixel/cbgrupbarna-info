# Catálogo de plantillas de cartel

Cada plantilla es un molde repetible: misma estructura, cambia el contenido. Eso da
consistencia (look de club top) y velocidad. Formato base IG 4:5 (1080×1350) salvo
indicación. Adaptar a 1:1 y 9:16 reencuadrando, no rehaciendo.

## 1. Convocatoria de partido
- **Mensaje:** próximo partido. Cada equipo, cada finde.
- **Elementos:** equipo vs rival, día/hora, lugar, competición, logo.
- **Estilo:** competición → contraste alto, diagonal (Bulls). Dato (hora) grande.
- **Variable automatizable:** sí (datos por partido). Ver `produccio-cartells`.

## 2. Resultado (victoria / derrota)
- **Mensaje:** marcador final. Versión victoria (épica) y derrota (sobria, digna).
- **Elementos:** marcador grande (`TYPE_DADA`), escudos/nombres, competición, logo.
- **Estilo:** marcador como protagonista. Victoria con acento de color; derrota
  neutra y respetuosa (nunca dramática con menores).
- **Variable automatizable:** sí — caso de uso estrella del cartel autogenerado.

## 3. MVP / jugada del día
- **Mensaje:** destacar a un jugador/a. Pilar formativo + comunidad.
- **Elementos:** foto recortada a contraste, nombre en display, dato (puntos,
  rebotes), logo.
- **Estilo:** póster de jugador estilo NBA (ver anatomía). Alterna chicas/chicos.

## 4. Cumpleaños
- **Mensaje:** felicitar a jugador/a o staff.
- **Elementos:** foto, nombre, "Bon aniversari", logo. Cálido pero dentro del sistema.

## 5. Anuncio de evento / campus
- **Mensaje:** convocar (3x3 Westfield, Campus). CTA claro (inscripción, fecha).
- **Elementos:** nombre del evento en display, fecha/lugar, CTA, logos (club +
  Westfield + sponsors con jerarquía), QR opcional.
- **Estilo:** marca/lifestyle → más Nike (impacto, aire). El CTA debe destacar.

## 6. Welcome / fichaje
- **Mensaje:** "Benvingut/da al Grup Barna".
- **Elementos:** foto recortada, nombre, posición, temporada, logo.
- **Estilo:** póster de jugador. Inicio de la serie de presentación de equipo.

## 7. Activación de sponsor
- **Mensaje:** agradecer/activar a un patrocinador con métrica o acción.
- **Elementos:** logo del sponsor con jerarquía correcta, mensaje de la activación,
  logo del club. Coordinar con eje ingresos de `ana-innovacio-barna`.
- **Estilo:** elegante; el club ofrece plataforma, no pide favor.

## 8. Quote / cita
- **Mensaje:** frase de coach/jugador/a sobre foto de acción.
- **Elementos:** cita en display, autor, foto de fondo desaturada, logo.

## Reglas del catálogo

- Si una plantilla se usa más de 2 veces → entra al sistema y se versiona.
- Toda serie comparte tokens (color, fuente, lockup) y un elemento de sistema.
- Diversidad real en fotos: chicas y chicos, edades, equipos, staff.
- Las plantillas con "variable automatizable: sí" son candidatas a generación por
  código (`produccio-cartells/scripts`).
