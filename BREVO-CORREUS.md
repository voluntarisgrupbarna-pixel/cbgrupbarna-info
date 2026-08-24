# Els correus automàtics del club

Dos correus que surten sols des de Brevo. Aquí hi ha **el text llest per
enganxar** i **com muntar-los**. La part de formularis, atributs i llistes és a
[`/js/README-brevo.md`](js/README-brevo.md).

| Correu | Quan surt | A qui |
|---|---|---|
| **1 · Benvinguda** | En confirmar l'alta a la newsletter | Llista Newsletter i llista Galeria |
| **2 · Rebut** | Just després d'enviar un formulari | Portada, `/escriu-nos/`, `/portes-obertes/` i descàrregues |

Cap dels dos substitueix la resposta d'una persona. El de «rebut» diu *ho hem
rebut i això és el que ens has escrit*; qui contesta de veritat és el club, el
mateix dia.

---

## Com es munten (una sola vegada)

**Campanyes → Plantilles → Nova plantilla** per a cada correu. A dins:

- **Emissor**: CB Grup Barna `<hola@cbgrupbarna.info>`.
- **Respondre a**: el correu que llegeix algú de veritat.
- Els buits es posen amb els atributs: `{{ contact.NOM }}`,
  `{{ contact.MISSATGE }}`, `{{ contact.TEMA }}`, `{{ contact.ANY_NAIX }}`.
  Si l'atribut és buit, Brevo no escriu res.
- **Els tres idiomes van al mateix correu**, separats per condicions:

```
{% if contact.IDIOMA == "es" %}
  … text en castellà …
{% elif contact.IDIOMA == "en" %}
  … text en anglès …
{% else %}
  … text en català …
{% endif %}
```

Després, **Automatitzacions → Crea un flux**:

| Correu | Disparador | Acció |
|---|---|---|
| Benvinguda | *Un contacte s'afegeix a una llista* → Newsletter | Envia la plantilla «Benvinguda» |
| Benvinguda | Un altre flux igual amb la llista Galeria | La mateixa plantilla |
| Rebut | *Un contacte s'afegeix a una llista* → Vull informació | Envia la plantilla «Rebut» |
| Rebut | Un flux igual per Portes obertes i per Descàrregues | La mateixa plantilla |

Amb doble opt-in, la benvinguda surt **després** de confirmar, que és el que toca:
si sortís abans, s'enviaria a correus que ningú ha verificat.

---

## 1 · Correu de benvinguda

**Assumpte**
```
Ja hi ets · CB Grup Barna
```
```
Ya estás dentro · CB Grup Barna
```
```
You're in · CB Grup Barna
```

**Text**

> Hola{{ ' ' }}{{ contact.NOM }},
>
> Ja estàs apuntat/ada al butlletí del CB Grup Barna. Escrivim poc i quan hi ha
> alguna cosa que val la pena: portes obertes, campus, dies de partit i el que
> passa al club.
>
> Som el club de bàsquet del Clot des del 1965. Més de 34 equips, 450 jugadores
> i jugadors, escoleta de 4 a 8 anys i secció femenina.
>
> Mentrestant:
> · El calendari: cbgrupbarna.info/partits/
> · L'escoleta: cbgrupbarna.info/escoleta/
> · Instagram: @cbgrupbarna
>
> Si algun dia no el vols, es baixa amb un clic al final de qualsevol correu.
>
> — CB Grup Barna

**Castellà**

> Hola{{ ' ' }}{{ contact.NOM }},
>
> Ya estás apuntado/a al boletín del CB Grup Barna. Escribimos poco y cuando hay
> algo que vale la pena: puertas abiertas, campus, días de partido y lo que pasa
> en el club.
>
> Somos el club de baloncesto del Clot desde 1965. Más de 34 equipos, 450
> jugadoras y jugadores, escoleta de 4 a 8 años y sección femenina.
>
> Mientras tanto:
> · El calendario: cbgrupbarna.info/es/partidos/
> · La escoleta: cbgrupbarna.info/es/escoleta/
> · Instagram: @cbgrupbarna
>
> Si algún día no lo quieres, se da de baja con un clic al final de cualquier correo.
>
> — CB Grup Barna

**Anglès**

> Hi{{ ' ' }}{{ contact.NOM }},
>
> You're now on the CB Grup Barna newsletter. We write rarely, and only when
> there's something worth it: open days, camps, match days and what's going on
> at the club.
>
> We're the basketball club of El Clot, founded in 1965. Over 34 teams, 450
> players, a 4-to-8 school and a women's section.
>
> In the meantime:
> · Fixtures: cbgrupbarna.info/en/fixtures/
> · The school: cbgrupbarna.info/en/basketball-school/
> · Instagram: @cbgrupbarna
>
> You can unsubscribe with one click at the bottom of any email.
>
> — CB Grup Barna

---

## 2 · Correu de rebut, amb la consulta

Que la persona vegi **exactament què ens ha arribat**. És el que evita el «no
sé si s'ha enviat» i el segon enviament del mateix.

**Assumpte**
```
Hem rebut la teva consulta · CB Grup Barna
```
```
Hemos recibido tu consulta · CB Grup Barna
```
```
We've received your message · CB Grup Barna
```

**Text**

> Hola{{ ' ' }}{{ contact.NOM }},
>
> Hem rebut el que ens has escrit i et responem **el mateix dia**. Si tens
> pressa, el WhatsApp del club és el 698 425 153.
>
> **Això és el que ens ha arribat:**
>
> {% if contact.TEMA %}Tema: {{ contact.TEMA }}{% endif %}
> {% if contact.ANY_NAIX %}Any de naixement: {{ contact.ANY_NAIX }}{% endif %}
> {% if contact.INTERES %}Interessa: {{ contact.INTERES }}{% endif %}
> {% if contact.MISSATGE %}
> «{{ contact.MISSATGE }}»
> {% endif %}
>
> Si hi ha res que no quadri, respon aquest correu i ho corregim.
>
> — CB Grup Barna
> Bàsquet al Clot des del 1965 · cbgrupbarna.info

**Castellà**

> Hola{{ ' ' }}{{ contact.NOM }},
>
> Hemos recibido lo que nos has escrito y te respondemos **el mismo día**. Si
> tienes prisa, el WhatsApp del club es el 698 425 153.
>
> **Esto es lo que nos ha llegado:**
>
> {% if contact.TEMA %}Tema: {{ contact.TEMA }}{% endif %}
> {% if contact.ANY_NAIX %}Año de nacimiento: {{ contact.ANY_NAIX }}{% endif %}
> {% if contact.INTERES %}Le interesa: {{ contact.INTERES }}{% endif %}
> {% if contact.MISSATGE %}
> «{{ contact.MISSATGE }}»
> {% endif %}
>
> Si hay algo que no cuadra, responde a este correo y lo corregimos.
>
> — CB Grup Barna
> Baloncesto en el Clot desde 1965 · cbgrupbarna.info

**Anglès**

> Hi{{ ' ' }}{{ contact.NOM }},
>
> We've received your message and we'll reply **the same day**. If you're in a
> hurry, the club's WhatsApp is +34 698 425 153.
>
> **This is what reached us:**
>
> {% if contact.TEMA %}Topic: {{ contact.TEMA }}{% endif %}
> {% if contact.ANY_NAIX %}Year of birth: {{ contact.ANY_NAIX }}{% endif %}
> {% if contact.INTERES %}Interested in: {{ contact.INTERES }}{% endif %}
> {% if contact.MISSATGE %}
> "{{ contact.MISSATGE }}"
> {% endif %}
>
> If anything looks wrong, reply to this email and we'll fix it.
>
> — CB Grup Barna
> Basketball in El Clot since 1965 · cbgrupbarna.info

---

## Coses a vigilar

- **El de «rebut» no és comercial**: no hi posis novetats ni ofertes. Va a gent
  que no ha donat cap permís de màrqueting, i barrejar-ho seria fer-los publicitat
  sense permís.
- **Un rebut per enviament, no per contacte.** Si el flux es configura «només un
  cop per contacte», qui escrigui dues vegades no rebrà el segon acusament i
  pensarà que no ha arribat. Deixa'l que es repeteixi.
- **Prova-ho amb un correu del club abans d'engegar-ho**, i mira que les tres
  condicions d'idioma es vegin bé: `IDIOMA` buit ha de caure al català.
- **La bústia no rep cap d'aquests correus.** És anònima i el seu text no viatja
  a Brevo.
