# -*- coding: utf-8 -*-
"""Construeix SEO-GEO-CB-Grup-Barna.xlsx a partir dels CSV i de les cerques
ja fetes. Executar: python3 seo/_excel.py"""
import csv, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _xlsx
from _xlsx import Sheet

H, ALERT, OK, BOLD, TITLE, GREY = 1, 4, 6, 2, 5, 7
BASE = os.path.dirname(os.path.abspath(__file__))
def p(f): return os.path.join(BASE, f)

# ---------------------------------------------------------------- troballes --
# Resultats reals de les cerques fetes el 22/08/2026 amb el cercador integrat.
RIVALS = [
 (1,"club de basquet base Barcelona","ca","Google","SI","~3r · cbgrupbarna.info",
  "basquetcatala.cat (cercador de clubs)","fcbarcelona.cat","Viquipedia",
  "cbroser.com",
  "Competim contra directoris i enciclopedies, no contra clubs. Sortim, pero per sota de la federacio."),
 (2,"escola de basquet Barcelona nens","ca","Google","SI, pero de rebot","via article de betevé",
  "Barca Escola (fcbarcelona)","betevé (article sobre NOSALTRES)","escoles.basquetcatala.cat",
  "Claror, AFA Escola Barcelona",
  "GREU: qui posiciona per nosaltres es un mitja, no la nostra /escoleta/. El trafic se'l queda betevé."),
 (3,"basquet femeni Barcelona club","ca","Google","NO","-",
  "enciclopedia.cat (CBF Universitari)","Viquipedia","FC Barcelona (5 resultats)",
  "-",
  "Invisibles tot i tenir TRES pagines de femeni. La canibalitzacio /femeni/ vs /basquet-femeni/ es paga aqui."),
 (4,"campus de basquet Barcelona estiu","ca","Google","NO","-",
  "Campus Nacho Solozabal","Fundacio Basquet Catala / FCBQ","Barca Escola Campus",
  "Campus Olimpia (Eixample), ITW Sport, Showtime, Sant Ignasi, Gametime",
  "Invisibles en una paraula 100% transaccional. Aqui hi ha inscripcions reals en joc."),
 (5,"academia de basquet Barcelona tecnificacio","ca","Google","NO","-",
  "Competize (llistat)","ToYouToMe: 10 millors escoles (llistat)","Beast Basketball Academy",
  "Barca Escola, ITW Sport, Coach Lorenzo, Pau Gasol Academy",
  "Manen els LLISTATS. Entrar en aquests articles val mes que qualsevol canvi a la nostra web."),
 (6,"basquet al Clot Sant Marti","ca","Google","SI","guia.barcelona.cat 1r; nosaltres despres",
  "guia.barcelona.cat","ajuntament.barcelona.cat","basquetcatala.cat",
  "cbgrupbarna.com (la NOSTRA web antiga) per sobre de cbgrupbarna.info",
  "Competim contra nosaltres mateixos: el domini .com es menja el .info al nostre propi territori."),
 (7,"baloncesto base Barcelona ninos","es","Google","NO","-",
  "Barca Academy","Competize (llistat)","Mejor Valorados Barcelona (llistat)",
  "ToYouToMe, shbarcelona; citen CB Roser, CB Coll, Cornella, Lluisos de Gracia",
  "En castella no existim. I els clubs que SI que citen als llistats son rivals directes nostres."),
 (8,"apuntar a mi hija a baloncesto Barcelona","es","Google","NO","-",
  "FC Barcelona (4 resultats)","css.cat (lligues femenines)","Wikipedia",
  "-",
  "La cerca d'una mare decidida a inscriure la filla. No hi som."),
 (9,"baloncesto inclusivo Barcelona","es","Google","NO","-",
  "Barca Genuine","Institut Guttmann","Discapnet",
  "GKEF-FGDA, QL Sport, Fenomens",
  "Tenim els Magics i som invisibles. Poca competencia local: es la victoria mes barata del mapa."),
 (10,"CB Grup Barna opiniones","marca","Google","SI","pero no primers",
  "cbgrupbarna.com (4 resultats)","Foursquare","X / Twitter",
  "FEB baloncestoenvivo, cbblanes.cat",
  "La web antiga domina la marca. I NO es troba cap ressenya enlloc: confirma per que cal /opina."),
]

TROBALLES = [
 ("1","La web antiga ens fa la competencia","cbgrupbarna.com surt per sobre de cbgrupbarna.info fins i tot a la nostra marca i al nostre barri.","Decidir que fem amb el .com: redireccio, o repartir-nos els temes.","Alt","Ana + Junta"),
 ("2","Invisibles en castella","A cap de les cerques generiques en castella hi som. El volum gran de Barcelona busca en castella.","Reforcar /es/ i crear les pagines castellanes que falten.","Alt","Contingut"),
 ("3","Manen els llistats, no els clubs","Competize, ToYouToMe, MejorValorados i shbarcelona decideixen qui es 'la millor escola de Barcelona'.","Contactar-los per sortir-hi. Es premsa, no SEO.","Alt","Ana"),
 ("4","Un mitja posiciona per nosaltres","A 'escola de basquet Barcelona nens' surt l'article de betevé, no la nostra /escoleta/.","Enfortir /escoleta/ i enllacar-la des de la home i el blog.","Alt","Claude"),
 ("5","Canibalitzacio femenina","/femeni/ i /basquet-femeni/ competeixen entre elles; el resultat es que no surt cap.","Triar-ne una i redirigir l'altra.","Alt","Claude"),
 ("6","Els Magics, invisibles","Cap resultat nostre a basquet inclusiu, amb poca competencia local.","Pagina /magics/ optimitzada + nota de premsa.","Mitja","Claude + Ana"),
 ("7","Cap ressenya a cap plataforma","Ni Google ni Foursquare. Confirma la urgencia de /opina.","Llancar la campanya de ressenyes.","Alt","Ana"),
 ("8","Adreca inconsistent","guia.barcelona.cat diu Placa Canonge Rodo 2 (08026); la nostra web diu Llacuna 172 (08018).","Unificar NAP a tot arreu. Es determinant per a cerca local.","Alt","Ana"),
]

def resum():
    s = Sheet('Resum', [4, 34, 62, 46, 10, 16], freeze=False, autofilter=False)
    s.add([('Bateria SEO + GEO · CB Grup Barna', TITLE)])
    s.add([('Fotografia del 22 d\'agost de 2026 · abans de presentar la web nova', GREY)])
    s.add([])
    s.add([('QUE JA ESTA MESURAT', BOLD)])
    s.add([('', 0), ('10 cerques a Google (ca + es) passades amb el cercador integrat. Resultats al full "Rivals per cerca".', 3)])
    s.add([('', 0), ('AVIS: aquest cercador NO es Google des de Barcelona. No hi ha geolocalitzacio ni resultats locals.', ALERT)])
    s.add([('', 0), ('Serveix per saber CONTRA QUI competim, no per donar posicions exactes.', 3)])
    s.add([])
    s.add([('QUE FALTA I NOMES ES POT FER DES DEL MOBIL', BOLD)])
    for t in ['Instagram: 6 cerques dins l\'app (3 pestanyes: comptes, publicacions, reels).',
              'TikTok: 5 cerques dins l\'app + les suggerencies de la barra de cerca.',
              'Assistents d\'IA: 3 preguntes a ChatGPT, Perplexity i Gemini.',
              'Recompte de seguidors dels 10 clubs (full "Clubs a comptar").']:
        s.add([('', 0), (t, 3)])
    s.add([])
    s.add([('LES 8 TROBALLES, PER IMPACTE', BOLD)])
    s.add([('#', H), ('Troballa', H), ('Que hem vist', H), ('Que cal fer', H), ('Impacte', H), ('Qui', H)])
    for r in TROBALLES:
        st = ALERT if r[4] == 'Alt' else 0
        s.add([(r[0], st), (r[1], st), (r[2], 0), (r[3], 0), (r[4], st), (r[5], 0)])
    return s

def rivals():
    s = Sheet('Rivals per cerca', [4, 34, 7, 9, 9, 26, 30, 28, 24, 40, 60])
    s.add([('#', H), ('Paraula o frase', H), ('Idioma', H), ('Plataforma', H), ('Hi som?', H),
           ('On sortim', H), ('Rival 1', H), ('Rival 2', H), ('Rival 3', H),
           ('Altres que apareixen', H), ('Lectura', H)])
    for r in RIVALS:
        st = OK if r[4].startswith('SI') and 'rebot' not in r[4] else ALERT
        s.add([r[0], r[1], r[2], r[3], (r[4], st), r[5], r[6], r[7], r[8], r[9], r[10]])
    return s

def from_csv(name, fname, widths, note=None):
    s = Sheet(name, widths)
    rows = list(csv.reader(open(p(fname), encoding='utf-8')))
    s.add([(c.replace('_', ' '), H) for c in rows[0]])
    for r in rows[1:]:
        s.add(r)
    return s

def clubs():
    s = Sheet('Clubs a comptar', [6, 30, 22, 22, 14, 16, 12, 40])
    rows = list(csv.reader(open(p('clubs-a-comptar.csv'), encoding='utf-8')))
    s.add([(c.replace('_', ' '), H) for c in rows[0]])
    for r in rows[1:]:
        s.add(r)
    return s

def protocol():
    s = Sheet('Protocol', [4, 100], freeze=False, autofilter=False)
    s.add([('Com passar les cerques perque les dades valguin', TITLE)])
    s.add([])
    for i, t in enumerate([
      'Des del MOBIL i amb la sessio TANCADA (o un perfil net). Des del compte del club, Instagram i TikTok ensenyen el que ja segueixes: el resultat surt maquillat.',
      'Si NO sortim, s\'apunta igual qui surt primer. Saber qui guanya quan perdem es la meitat de la feina.',
      'Captura de pantalla sempre, amb la data. Es la prova i permet repetir la mesura d\'aqui a tres mesos.',
      'Tres repeticions a les de prioritat 1: aquests cercadors varien entre consulta i consulta.',
      'A Instagram, mirar les TRES pestanyes (comptes, publicacions, reels). Hi som a unes i no a altres.',
      'A TikTok, anotar tambe les suggerencies de la barra de cerca: es recerca de paraules clau gratuita i real.',
      'Els perfils que surtin i no coneguem (entrenadors creadors, campus nacionals) son la troballa mes valuosa.'], 1):
        s.add([(str(i), BOLD), (t, 3)])
    s.add([])
    s.add([('Indicadors que seguirem', BOLD)])
    for t in ['Cobertura de mencio: % de respostes d\'IA on sortim.',
              'Taxa de citacio amb enllac: % que a mes enllaca cbgrupbarna.info.',
              'Exactitud factual (0-3) i taxa d\'al-lucinacio.',
              'Posicio mitjana quan la resposta es una llista de clubs.',
              'Quota de veu contra els rivals de barri.',
              'Cobertura d\'intencio: paraules amb una URL nostra sana assignada.']:
        s.add([('', 0), (t, 3)])
    return s

sheets = [
    resum(),
    rivals(),
    from_csv('Tanda 1 (30 cerques)', 'tanda-1.csv', [6, 8, 34, 7, 10, 24, 30, 10, 9, 12, 24, 24, 24, 10, 30]),
    from_csv('Mapa (145 paraules)', 'mapa-paraules-clau.csv', [8, 40, 8, 13, 14, 13, 34, 9, 34]),
    from_csv('Full de captura', 'full-captura.csv', [8, 40, 8, 11, 11, 10, 12, 28, 24, 24, 24, 10, 30]),
    clubs(),
    protocol(),
]
out = p('SEO-GEO-CB-Grup-Barna.xlsx')
_xlsx.write(out, sheets)
print('escrit:', out)
for sh in sheets:
    print('  -', sh.name, len(sh.rows), 'files')
