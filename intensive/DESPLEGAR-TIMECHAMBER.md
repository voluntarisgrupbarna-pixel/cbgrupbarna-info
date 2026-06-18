# Alojar el programa Intensive bajo dominio "Time Chamber" (gratis)

Hay dos formas. La **A** es la recomendada (mejor SEO, URL real "Time Chamber").

---

## Opción A · URL gratuita `timechamber.netlify.app` (recomendada)

1. Entra en https://app.netlify.com y crea cuenta gratis (botón "Sign up", puedes usar Google/GitHub). Sin tarjeta.
2. "Add new site" → "Import an existing project" → conecta GitHub → elige el repo `cbgrupbarna-info`.
3. Deja todo por defecto y pulsa "Deploy". El repo ya incluye `netlify.toml`, así que la home servirá el programa Intensive automáticamente.
4. "Site configuration" → "Change site name" → escribe **timechamber**.
   Resultado: **https://timechamber.netlify.app** mostrando el programa.

> Igual de fácil en Vercel (https://vercel.com): importa el repo; ya incluye `vercel.json`. Te dará `timechamber.vercel.app`.

### Si tienes un dominio propio (p. ej. timechamberacademy.com)
En Netlify: "Domain management" → "Add a domain" → sigue los pasos DNS.
La URL será tu dominio Time Chamber, con el programa servido directamente.

---

## Opción B · Enmascarar un dominio que ya tengas (iframe)

Si ya tienes un dominio Time Chamber y solo quieres que muestre el programa
**sin cambiar la barra de direcciones**, sube el archivo `/tc/index.html`
de este repo a la raíz de ese dominio/host. Envuelve la página real a
pantalla completa y la barra mantiene tu dominio Time Chamber.

> Nota: el enmascarado por iframe es peor para SEO que la Opción A, porque el
> contenido real sigue viviendo en cbgrupbarna.info. Para posicionar por
> "tecnificación basket", usa la Opción A.
