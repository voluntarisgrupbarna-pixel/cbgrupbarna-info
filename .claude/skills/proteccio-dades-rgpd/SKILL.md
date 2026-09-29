---
name: proteccio-dades-rgpd
description: Protecció de dades (RGPD/LOPDGDD), drets d'imatge de menors i LOPIVI per al CB Grup Barna. Carrega-la SEMPRE que es parli de consentiments de famílies, drets d'imatge, fotos o vídeos de nens i nenes, baixes, formularis que recullen dades, llistes de jugadors, galeries, newsletter, WhatsApp de grups, esborrat de dades, dret d'accés/supressió, o abans de publicar qualsevol cosa on surti un menor. També quan algú demani "puc publicar aquesta foto?", "com ho dic a la família?", "quina base legal tenim?" o es toqui la política de privacitat. Ús obligatori abans de crear un formulari nou o un flux de dades nou, encara que l'Ana no ho demani explícitament.
---

# Protecció de dades · CB Grup Barna

El club treballa amb **menors**: cada decisió sobre dades o imatge s'ha de poder
defensar davant una família, la Federació o l'Ajuntament. Aquesta skill dona el
criteri i els fluxos; **no substitueix un assessor jurídic** — quan hi hagi
dubte real (denúncia, requeriment, incident greu), s'escala (vegeu «Escalat»).

## Dades reals del club (font: web publicada, no inventar-ne d'altres)

- **Responsable:** Club Bàsquet Grup Barna, NIF G58432584, C/ Llacuna 170-172,
  Parc del Clot, 08018 Barcelona.
- **Contacte de privacitat:** marqueting@cbgrupbarna.info
- **Política vigent:** `politica-de-privacitat/index.html` (act. 2026-08-24).
  Si canvies un flux de dades, la política es canvia **al mateix commit**.
- **Delegada de Protecció al Menor (LOPIVI):** Ana Fernández. Canal confidencial
  protecciomenorcbgrupbarna@gmail.com, resposta < 7 dies. Pàgina `proteccio-menor/`.
- **Encarregats del tractament declarats:** Meta (WhatsApp), Formspree, Google
  (Drive/Sheets/Analytics), GitHub Pages, Flickr. Un servei nou = s'afegeix a la
  política abans de fer-lo servir.
- Analytics només s'activa amb consentiment (banner «Només les necessàries» /
  «Accepta-les»). No trencar aquesta regla en cap peça nova.

## Regles d'or (i per què)

1. **Menor de 14 anys → consent de pare/mare/tutor.** A partir de 14 pot consentir
   ell mateix el tractament de dades, però al club es demana igualment a la família
   per imatge i comunicacions: evita conflictes i és la pràctica prudent.
2. **Un consentiment per finalitat, casella independent.** Imatge ≠ comunicacions ≠
   dades esportives ≠ newsletter. Mai una casella «accepto tot». (Ja és així al
   formulari de descàrregues: la newsletter és una casella a part.)
3. **Sense consentiment d'imatge, no surt en primer pla.** Peça amb un menor
   identificable sense autorització registrada = no es publica. Es pot usar
   d'esquena, de lluny, a partit ple, o il·lustració.
4. **Minimitzar.** Només es demana el que es fa servir. Mai DNI, salut o
   situació familiar en formularis de màrqueting.
5. **Es pot retirar en qualsevol moment**, i retirar és tan fàcil com donar-lo
   (un correu). Es respon en 30 dies com a màxim; al club, en menys de 7.
6. **Noms de menors:** a xarxes, només nom de pila (o dorsal) i categoria, mai
   cognoms + escola + barri junts. Mai adreça, horaris de casa, telèfons.

## Consentiments que ha de tenir el club (registre)

| Finalitat | Base | On es guarda | Caduca |
|---|---|---|---|
| Inscripció i gestió esportiva (fitxa federativa, assegurança) | Contracte / obligació legal | Gestió d'inscripcions | Mentre duri la relació + terminis legals |
| Imatge en web/xarxes/premsa | Consentiment (familia) | Full de consentiments | Temporada; renovar cada setembre |
| Comunicacions (WhatsApp/email de club) | Consentiment / interès legítim | Llista de grup | Fins a baixa |
| Newsletter | Consentiment | Llista newsletter | Fins a baixa |
| Fotos d'esdeveniment (3x3, campus) | Consentiment via cartell + formulari | Cartell d'accés + formulari | Esdeveniment |

Al **3x3 i al campus** hi ha públic: posar cartell visible a l'entrada
(«s'hi fan fotos i vídeos amb finalitat informativa del club») i formulari
d'oposició. Per a un menor **en primer pla** (pòdium, MVP, portada), consentiment
explícit de la família.

## Flux: «puc publicar aquesta foto?»

1. Hi surt un menor identificable? No → OK.
2. Sí → consta autorització d'imatge vigent (aquesta temporada)? No → no es publica
   (o es retalla/desenfoca/canvia la peça) i es demana a la família.
3. Context sensible (lesió, plor, derrota dura, cos poc vestit, vestidor)? →
   no, encara que hi hagi consentiment: protecció > contingut.
4. Etiquetar: no etiquetar menors; si la família ho demana, sí.
5. Guardar què s'ha publicat i on, per poder-ho retirar si arriba una baixa.

## Flux: baixa o retirada de consentiment

1. Confirmar la petició per escrit (correu/WhatsApp de la família).
2. Deixar de tractar: treure de llistes, de grups, de newsletter.
3. Imatges: retirar de la web/xarxes on el club té control; avisar que el que
   ja hagi compartit un tercer no es pot recuperar.
4. Respondre confirmant què s'ha fet (plantilla a `comunicacio-families`).
5. Anotar data i què s'ha eliminat.

## Drets de les persones (ARSULIPO)

Accés, rectificació, supressió, limitació, oposició, portabilitat. Si arriba una
petició: respondre en **1 mes** (ampliable), verificar identitat sense demanar
més dades de les necessàries, i guardar la traça. Reclamació davant l'Autoritat
Catalana de Protecció de Dades (APDCAT) o l'AEPD: la família ha de saber que existeix.

## Errors típics que aquesta skill evita

- Publicar la foto d'un equip sencer perquè «n'hi ha molts» → n'hi ha d'haver **cada** un.
- Reenviar llistes de contactes en WhatsApp obert → es fa amb **còpia oculta** o
  grup d'anunci (només admins escriuen).
- Formulari Google amb dades de menors sense avís de privacitat visible.
- Reutilitzar el consentiment d'una temporada per la següent.
- Enviar dades (llistats, DNI) per un canal insegur.

## Escalat

- **Incident de dades** (fuita, correu enviat a qui no toca, accés no autoritzat):
  avisar la Junta a l'instant; valorar notificació a l'autoritat en **72 h**.
- **Situació de risc del menor:** no és qüestió de dades, és LOPIVI → canal
  confidencial i Delegada de Protecció; no es gestiona per xarxes ni per grup.
- **Requeriment d'autoritat, denúncia o conflicte de custòdia:** no respondre
  sola; Junta + assessor.

## Què falta per completar aquesta skill (demanar a l'Ana)

- Text exacte dels consentiments actuals que signen les famílies.
- On es guarda el registre i qui hi té accés.
- Si hi ha Registre d'Activitats de Tractament fet i qui el manté.
- Si el club ha designat (o li cal) un DPD: normalment una entitat esportiva
  petita no està obligada, però convé confirmar-ho.
