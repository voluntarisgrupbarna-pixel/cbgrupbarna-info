# /opina — Landing de ressenyes de Google

Pàgina pública: **https://cbgrupbarna.info/opina**

Objectiu: convertir tràfic propi (WhatsApp, Instagram, QR al pavelló, email) en
ressenyes de Google. Explica *per què* importa abans de demanar l'acció, que és
el que fa que converteixi més que enviar l'enllaç de Google pelat.

Tot el que canvia sovint viu a **`opina.json`**. No cal tocar l'HTML.

---

## 1. Enllaç directe al formulari de ressenya (l'únic pas obligatori)

Mentre `placeId` i `reviewUrl` estiguin buits, el botó obre la fitxa del club a
Google i l'usuari ha de prémer "Escriu una ressenya" (un toc extra = menys
conversió). La pàgina ja avisa d'això automàticament.

Per activar l'enllaç directe, omple **una** d'aquestes dues opcions a `opina.json`:

**Opció A — enllaç curt del perfil d'empresa (recomanada)**

1. Inicia sessió amb el compte que gestiona el Perfil d'Empresa del club.
2. Busca "CB Grup Barna" a Google o entra a business.google.com.
3. Al panell del perfil, botó **"Demana ressenyes"** / "Pedir reseñas".
4. Google dona un enllaç curt tipus `https://g.page/r/XXXXXXXXXXXX/review`.
5. Enganxa'l a `"reviewUrl"`.

**Opció B — Place ID**

1. Obre https://developers.google.com/maps/documentation/places/web-service/place-id
2. Busca "CB Grup Barna, Barcelona" al mapa i copia el **Place ID**
   (comença per `ChIJ...`).
3. Enganxa'l a `"placeId"`. La pàgina construeix sola l'enllaç
   `https://search.google.com/local/writereview?placeid=…`.

> Si el club encara no té Perfil d'Empresa de Google verificat, aquest és el
> primer pas de tot: sense fitxa no hi ha ressenyes. Es reclama gratis des de
> business.google.com amb l'adreça de La Nau del Clot.

Comprova sempre l'enllaç des del mòbil abans de difondre'l.

---

## 2. Comptador d'objectiu

```json
"goal": 300,
"current": 183,
"updated": "5 d'agost de 2026"
```

- `current: null` → amaga la barra i mostra només "Objectiu: 300 ressenyes".
  És l'estat inicial: **posa-hi el número real** abans de la primera difusió.
- El número s'actualitza a mà (Google no dona el recompte per API sense clau de
  pagament). Mirar la fitxa del club a Google i actualitzar el fitxer un cop per
  setmana durant la campanya és suficient.
- `updated` és text lliure: es mostra tal qual sota la barra.

---

## 3. Vídeo d'agraïment (opcional)

```json
"video": {
  "enabled": true,
  "src": "video.mp4",
  "poster": "video.jpg",
  "caption": "Julio Torralba · CB Grup Barna"
}
```

Puja el fitxer a aquesta mateixa carpeta (`opina/video.mp4`). Recomanacions:
20-30 segons, vertical o quadrat, amb subtítols cremats (la majoria el veurà
sense so) i tancament amb la cartela de partners si es reaprofita per a xarxes.
Amb `enabled: false` la secció no apareix.

---

## 4. QR

`qr.svg` apunta a `https://cbgrupbarna.info/opina?s=qr` (el paràmetre serveix
per veure a Analytics quantes ressenyes venen del QR imprès).

Per regenerar-lo o fer-ne un altre amb una altra URL:

```bash
python3 scripts/qr.py "https://cbgrupbarna.info/opina?s=cartell" opina/qr-cartell.svg
```

El generador no té dependències externes i passa les seves pròpies validacions
abans d'escriure el fitxer (`python3 scripts/qr.py` sense arguments les executa).

---

## 5. Paràmetres d'URL útils per a la difusió

Serveixen per saber quin canal funciona, a Google Analytics (esdeveniment
`opina_source`):

| Enllaç | Ús |
|---|---|
| `cbgrupbarna.info/opina?s=wa` | grups de WhatsApp dels equips |
| `cbgrupbarna.info/opina?s=ig` | bio i stories d'Instagram |
| `cbgrupbarna.info/opina?s=mail` | enviament per correu a les famílies |
| `cbgrupbarna.info/opina?s=qr` | QR imprès (ja va dins el `qr.svg`) |
| `cbgrupbarna.info/opina?lang=es` | forçar castellà |

La pàgina detecta sola l'idioma del navegador i recorda l'últim triat.

---

## 6. Regla que no es pot saltar

No es reparteixen textos de ressenya escrits pel club perquè les famílies els
copiïn i enganxin. Google detecta les ressenyes calcades, les esborra i pot
penalitzar la fitxa. La pàgina només dona **idees** de què explicar; el text
l'escriu cadascú. Tampoc s'ofereix res a canvi d'una ressenya (descomptes,
sortejos): està prohibit per les polítiques de Google i posa la fitxa en risc.
