# Lenguaje cinematográfico del athlete film

Las herramientas concretas del género y cómo aplicarlas.

## Movimiento: slow-motion y speed ramps

- **Slow-mo:** ralentizar el momento (un tiro, un gesto) da peso épico. Necesita
  grabar a 60-120 fps; si no, interpolar (CapCut "smooth slow", DaVinci Optical
  Flow, o ffmpeg `minterpolate`). Sin fps ni interpolación, queda a tirones.
- **Speed ramp (la firma):** transición suave de cámara lenta a tiempo real (o al
  revés) dentro de un mismo plano. Acelera al acercarse al "drop" musical y ralentiza
  en el impacto. En CapCut: curva de velocidad personalizada. Cuadrar el cambio de
  velocidad con el beat.

## Planos (shot language)

- **Plano héroe:** el protagonista a contraluz, ángulo bajo (lo hace grande),
  silueta, o caminando hacia cámara. Poco profundo (sujeto enfocado, fondo difuso).
- **Detalle / insertos:** manos agarrando el balón, zapatillas en el parquet, gota
  de sudor, ojos, la red al entrar el tiro. Son el pegamento emocional.
- **Acción:** la jugada, pero tratada (slow-mo, ángulo).
- **Atmósfera:** pabellón vacío, luces, polvo en el haz de luz. Construye el "mundo".
- Mezclar escalas: abierto → medio → detalle crea ritmo visual.

## Grading (color)

- Un **look consistente** es lo que más sube el nivel percibido. Dos rutas:
  - **Cálido contrastado** (teal & orange suave): épico, comercial, tipo Nike.
  - **Desaturado moody** (alto contraste, sombras profundas): dramático, serio.
- Subir contraste, bajar un punto la saturación global salvo pieles, negros densos.
- **Grano/textura de film** sutil unifica y da sensación de cine (no exagerar).
- Mantener el MISMO grade en toda la pieza y en la serie. Coordinar acento de color
  con `sistema-visual-cbgb`.
- Receta automática base: `scripts/cinematic_grade.sh`.

## Diseño de sonido (el 50% que casi nadie cuida)

- **Música primero:** elige la pista antes de montar; el ritmo dirige los cortes.
  Identifica el "drop" y constrúyelo todo hacia ahí.
- **Capas de efectos:** whoosh en transiciones, impacto grave en el corte fuerte,
  sonidos reales realzados (bote, swish, chirrido de zapatilla, respiración).
- **Voz / quote:** una frase del jugador/a o coach, o voz en off. Da alma.
- **Ducking:** baja la música automáticamente cuando entra la voz, súbela después.
- **Silencio:** un microsilencio antes del drop multiplica el impacto.
- Normalizar a ~ -14 LUFS para IG.

## Tipografía cinética

- Revelado del **nombre** del jugador/a como momento (entra con el drop).
- **Dato/dorsal** como elemento gráfico grande.
- Frase corta y potente, al ritmo. Mínima: el vídeo manda, el texto apoya.
- Tipografía y color de `sistema-visual-cbgb`. Subtítulos si hay voz.

## Transiciones invisibles

- **Whip pan:** barrido rápido que oculta el corte.
- **Match cut:** unir dos planos por una forma/movimiento similar.
- **Speed blur / zoom blur:** desenfoque de movimiento entre cortes.
- **Máscara:** un objeto cruza y "limpia" el plano.
- Evitar SIEMPRE las transiciones preset decorativas (estrellas, giros, glitch
  gratuito): son la marca del montaje amateur.

## Loop

Para reels, pensar el final para que enganche con el principio (loop): aumenta
reproducciones y retención.
