# -*- coding: utf-8 -*-
"""Font unica del mapa de paraules clau del CB Grup Barna.
Genera mapa-paraules-clau.csv (definicio) i full-captura.csv (per omplir).
Executar: python3 seo/_fonts.py
Columnes: id, keyword, idioma, familia, intencio, plataformes, url_objectiu,
prioritat, rival_previst.
Plataformes: G=Google, IG=Instagram, TT=TikTok, IA=assistents d'IA."""

K = [
# --- CLUB / BASE -------------------------------------------------------------
("club de basquet a Barcelona","ca","CLUB","descobriment","G+IA","/",1,"clubs grans + directoris FCBQ"),
("club de basquet base Barcelona","ca","CLUB","descobriment","G+IA","/",1,"clubs de barri + basquetcatala"),
("basquet base Barcelona","ca","CLUB","descobriment","G+IG+TT+IA","/",1,"clubs de barri + comptes de highlights"),
("clubs de basquet de Barcelona","ca","CLUB","comparacio","G+IA","/posicionament/",2,"directoris + llistes de clubs"),
("on jugar a basquet a Barcelona","ca","CLUB","descobriment","G+IA","/",2,"Ajuntament + directoris"),
("club de baloncesto en Barcelona","es","CLUB","descobriment","G+IA","/",1,"clubs grans + directoris"),
("baloncesto base Barcelona","es","CLUB","descobriment","G+IG+TT+IA","/",1,"clubs de barri"),
("clubes de baloncesto Barcelona","es","CLUB","comparacio","G+IA","/posicionament/",2,"directoris + llistes"),
("donde jugar baloncesto en Barcelona","es","CLUB","descobriment","G+IA","/",2,"Ajuntament + directoris"),
("baloncesto cerca de mi","es","CLUB","descobriment","G","/",2,"Maps: qualsevol club del radi"),
("basketball club Barcelona","en","CLUB","descobriment","G+IA","/",3,"clubs internacionals + expats"),
# --- GEO / BARRI -------------------------------------------------------------
("basquet al Clot","ca","GEO","descobriment","G+IG+TT+IA","/",1,"cap rival clar: territori nostre"),
("club de basquet El Clot","ca","GEO","descobriment","G+IA","/",1,"entitats del barri"),
("basquet Sant Marti","ca","GEO","descobriment","G+IA","/blog/basquet-base-sant-marti-clot/",1,"clubs del districte"),
("baloncesto Sant Marti Barcelona","es","GEO","descobriment","G+IA","/blog/basquet-base-sant-marti-clot/",1,"clubs del districte"),
("baloncesto El Clot","es","GEO","descobriment","G+IA","/",1,"entitats del barri"),
("basquet Poblenou","ca","GEO","descobriment","G","/",2,"clubs veins"),
("basquet Glories","ca","GEO","descobriment","G+IG","/3x3/",2,"Westfield + esdeveniments"),
("clubs esportius Sant Marti","ca","GEO","descobriment","G+IA","/club/",2,"altres esports del districte"),
("esport per a nens al Clot","ca","GEO","descobriment","G+IA","/escoleta/",2,"altres entitats del barri"),
# --- ESCOLA / INICIACIO ------------------------------------------------------
("escola de basquet Barcelona","ca","ESCOLA","descobriment","G+IA","/escoleta/",1,"escoles privades + Barca Escola"),
("escoleta de basquet Barcelona","ca","ESCOLA","descobriment","G+IA","/escoleta/",1,"clubs amb escoleta"),
("basquet per a nens 4 anys Barcelona","ca","ESCOLA","transaccional","G+IA","/escoleta/",1,"escoles esportives + casals"),
("basquet per a nenes 5 anys Barcelona","ca","ESCOLA","transaccional","G+IA","/escoleta/",1,"escoles esportives"),
("iniciacio al basquet Barcelona","ca","ESCOLA","descobriment","G+IA","/escoleta/",2,"escoles esportives"),
("escuela de baloncesto Barcelona","es","ESCOLA","descobriment","G+IA","/escoleta/",1,"escoles privades + Barca"),
("escuela de baloncesto para ninos Barcelona","es","ESCOLA","transaccional","G+IA","/escoleta/",1,"escoles esportives"),
("baloncesto para ninos de 4 anos Barcelona","es","ESCOLA","transaccional","G+IA","/escoleta/",1,"escoles esportives + casals"),
("baloncesto infantil Barcelona","es","ESCOLA","descobriment","G+IG+IA","/escoleta/",1,"clubs + academies"),
("apuntar a mi hijo a baloncesto Barcelona","es","ESCOLA","transaccional","G+IA","/escoleta/",1,"clubs amb inscripcio oberta"),
("apuntar a mi hija a baloncesto Barcelona","es","ESCOLA","transaccional","G+IA","/basquet-femeni/",1,"clubs amb seccio femenina"),
("basketball school Barcelona kids","en","ESCOLA","descobriment","G+IA","/escoleta/",3,"escoles internacionals"),
# --- ACADEMIA / TECNIFICACIO -------------------------------------------------
("academia de basquet Barcelona","ca","ACADEMIA","descobriment","G+IA","/",1,"academies privades + Pau Gasol Academy"),
("academia de baloncesto Barcelona","es","ACADEMIA","descobriment","G+IA","/",1,"academies privades + Pau Gasol Academy"),
("academia de baloncesto en Barcelona precio","es","ACADEMIA","transaccional","G+IA","/campus/",2,"academies de pagament"),
("tecnificacio basquet Barcelona","ca","ACADEMIA","descobriment","G+IA","/campus/",2,"academies + campus"),
("tecnificacion baloncesto Barcelona","es","ACADEMIA","descobriment","G+IA","/campus/",2,"academies + campus"),
("escola club o academia de basquet","ca","ACADEMIA","informacional","G+IA","/blog/com-triar-escola-basquet-barcelona/",1,"blogs esportius"),
# --- CAMPUS ------------------------------------------------------------------
("campus de basquet Barcelona","ca","CAMPUS","transaccional","G+IG+TT+IA","/campus/",1,"campus nacionals + Barca Campus"),
("campus de baloncesto Barcelona","es","CAMPUS","transaccional","G+IG+TT+IA","/campus/",1,"campus nacionals + Pau Gasol"),
("campus basquet estiu Barcelona","ca","CAMPUS","transaccional","G+IA","/campus/",1,"campus d'estiu + casals"),
("campus baloncesto verano Barcelona","es","CAMPUS","transaccional","G+IA","/campus/",1,"campus d'estiu + casals"),
("campus baloncesto ninos Barcelona","es","CAMPUS","transaccional","G+IA","/campus/",1,"campus + casals esportius"),
("casal esportiu estiu Barcelona basquet","ca","CAMPUS","transaccional","G+IA","/campus/",2,"casals municipals"),
("campus baloncesto Barcelona precio","es","CAMPUS","transaccional","G+IA","/campus/",2,"campus de pagament"),
("com triar un campus de basquet","ca","CAMPUS","informacional","G+IA","/blog/campus-basquet-barcelona-guia/",2,"blogs + comparadors"),
# --- FEMENI ------------------------------------------------------------------
("basquet femeni Barcelona","ca","FEMENI","descobriment","G+IG+TT+IA","/basquet-femeni/",1,"clubs amb seccio femenina + mitjans"),
("baloncesto femenino Barcelona","es","FEMENI","descobriment","G+IG+TT+IA","/es/baloncesto-femenino/",1,"clubs + mitjans esportius"),
("club de basquet femeni Barcelona","ca","FEMENI","descobriment","G+IA","/basquet-femeni/",1,"clubs amb seccio femenina"),
("basquet per a nenes Barcelona","ca","FEMENI","transaccional","G+IA","/basquet-femeni/",1,"clubs + escoles"),
("baloncesto para ninas Barcelona","es","FEMENI","transaccional","G+IA","/es/baloncesto-femenino/",1,"clubs + escoles"),
("equip femeni de basquet Barcelona","ca","FEMENI","descobriment","G+IA","/basquet-femeni/",2,"clubs de LF2 i Copa Catalunya"),
("clubs amb seccio femenina Barcelona","ca","FEMENI","comparacio","G+IA","/basquet-femeni/",2,"clubs + federacio"),
("paritat en clubs esportius","ca","FEMENI","informacional","G+IA","/premidonaesport/",2,"institucions + mitjans"),
("womens basketball Barcelona","en","FEMENI","descobriment","G+IA","/en/womens-basketball/",3,"clubs + expats"),
("el metode Barna","ca","FEMENI","marca","G+IA","/basquet-femeni/el-metode-barna/",2,"cap: terme propi"),
# --- INCLUSIU ----------------------------------------------------------------
("basquet inclusiu Barcelona","ca","INCLUSIU","descobriment","G+IA","/magics/",1,"entitats d'esport adaptat"),
("baloncesto inclusivo Barcelona","es","INCLUSIU","descobriment","G+IA","/magics/",1,"entitats d'esport adaptat"),
("basquet per a persones amb discapacitat intel-lectual","ca","INCLUSIU","descobriment","G+IA","/magics/",1,"Special Olympics + fundacions"),
("baloncesto adaptado Barcelona","es","INCLUSIU","descobriment","G+IA","/magics/",2,"esport adaptat"),
("Barna Magics","ca","INCLUSIU","marca","G+IG+IA","/magics/",1,"cap: terme propi"),
("esport inclusiu Sant Marti","ca","INCLUSIU","descobriment","G+IA","/magics/",2,"entitats del districte"),
# --- 3X3 ---------------------------------------------------------------------
("3x3 Barcelona","ca","3X3","descobriment","G+IG+TT+IA","/3x3/",1,"FEB 3x3 + torneigs urbans"),
("torneig 3x3 basquet Barcelona","ca","3X3","transaccional","G+IA","/3x3/",1,"torneigs urbans"),
("torneo 3x3 baloncesto Barcelona","es","3X3","transaccional","G+IA","/3x3/",1,"torneigs urbans"),
("basquet 3x3 Glories","ca","3X3","transaccional","G+IG","/3x3/",1,"Westfield + Time Chamber"),
("que es el basquet 3x3","ca","3X3","informacional","G+IA","/blog/que-es-basquet-3x3/",2,"FEB + mitjans"),
("reglas baloncesto 3x3","es","3X3","informacional","G+IA","/blog/que-es-basquet-3x3/",2,"FEB + Wikipedia"),
# --- MARCA -------------------------------------------------------------------
("CB Grup Barna","ca","MARCA","marca","G+IG+TT+IA","/",1,"basquetcatala + FCBQ + cbgrupbarna.com"),
("Grup Barna basquet","ca","MARCA","marca","G+IA","/",1,"web historica + federacio"),
("Club Basquet Grup Barna","ca","MARCA","marca","G+IA","/",1,"enciclopedia.cat + federacio"),
("CB Grup Barna opiniones","es","MARCA","verificacio","G+IA","/opina/",1,"Google Maps + directoris"),
("CB Grup Barna ressenyes","ca","MARCA","verificacio","G+IA","/opina/",1,"Google Maps"),
("CB Grup Barna equips","ca","MARCA","navegacio","G+IA","/partits/equips/",2,"basquetcatala"),
("CB Grup Barna campus","ca","MARCA","navegacio","G+IA","/campus/",2,"cap"),
("CB Grup Barna escoleta","ca","MARCA","navegacio","G+IA","/escoleta/",2,"cap"),
("CB Grup Barna partits","ca","MARCA","navegacio","G+IA","/partits/",2,"basquetcatala"),
("cbgrupbarna","ca","MARCA","navegacio","G+IG+TT","/",2,"comptes propis"),
("es bo el CB Grup Barna","ca","MARCA","verificacio","IA","/opina/",1,"ressenyes + mitjans"),
("que tal es el CB Grup Barna","es","MARCA","verificacio","IA","/opina/",1,"ressenyes + mitjans"),
# --- INFORMACIONAL (blog) ----------------------------------------------------
("a quina edat comencar a jugar a basquet","ca","INFO","informacional","G+IA","/blog/a-quina-edat-comencar-basquet/",1,"blogs de salut i esport"),
("a que edad empezar baloncesto","es","INFO","informacional","G+IA","/blog/a-quina-edat-comencar-basquet/",1,"blogs + mitjans"),
("com triar un club de basquet per al meu fill","ca","INFO","informacional","G+IA","/blog/com-triar-escola-basquet-barcelona/",1,"blogs de families"),
("como elegir club de baloncesto para mi hijo","es","INFO","informacional","G+IA","/blog/com-triar-escola-basquet-barcelona/",1,"blogs de families"),
("per que les noies deixen el basquet","ca","INFO","informacional","G+IA","/blog/per-que-les-noies-deixen-el-basquet/",1,"mitjans + estudis"),
("por que las ninas dejan el deporte","es","INFO","informacional","G+IA","/blog/per-que-les-noies-deixen-el-basquet/",1,"mitjans + estudis"),
("equipacio femenina de basquet","ca","INFO","informacional","G+IA","/blog/equipacio-femenina-basquet/",2,"marques esportives"),
("entrenadores de basquet a Barcelona","ca","INFO","informacional","G+IA","/blog/entrenadores-basquet-barcelona/",2,"federacio + mitjans"),
("club de basquet segur per a menors","ca","INFO","verificacio","G+IA","/blog/club-basquet-segur-igualtat-families/",1,"institucions"),
("proteccio del menor en un club esportiu","ca","INFO","verificacio","G+IA","/proteccio-menor/",1,"institucions + federacions"),
("LOPIVI club esportiu","ca","INFO","verificacio","G+IA","/proteccio-menor/",2,"institucions + assessories"),
("delegat de proteccio del menor","ca","INFO","verificacio","G+IA","/proteccio-menor/",2,"institucions"),
("basquet base al Clot i Sant Marti","ca","INFO","informacional","G+IA","/blog/basquet-base-sant-marti-clot/",2,"cap rival clar"),
("basquet femeni a Barcelona dades","ca","INFO","informacional","G+IA","/blog/basquet-femeni-barcelona-0-75-per-cent/",2,"mitjans + federacio"),
# --- COMPETICIO --------------------------------------------------------------
("calendari partits basquet base Barcelona","ca","COMPETICIO","navegacio","G+IA","/partits/",2,"basquetcatala + FCBQ"),
("resultats basquet base Catalunya","ca","COMPETICIO","navegacio","G+IA","/partits/",2,"basquetcatala + FEB"),
("Supercopa Catalunya basquet","ca","COMPETICIO","informacional","G+IA","/posicionament/",2,"FCBQ + mitjans"),
("partits de basquet base en directe","ca","COMPETICIO","navegacio","G+IA","/partits/",3,"MyPlay + federacio"),
("calendari equip cadet femeni Barcelona","ca","COMPETICIO","navegacio","G","/partits/equips/",3,"basquetcatala"),
# --- PATROCINI ---------------------------------------------------------------
("patrocinar un club esportiu a Barcelona","ca","PATROCINI","transaccional","G+IA","/patrocinadors/",1,"agencies + altres clubs"),
("patrocinio deportivo Barcelona","es","PATROCINI","transaccional","G+IA","/patrocinadors/",1,"agencies + clubs grans"),
("com patrocinar un club de basquet","ca","PATROCINI","informacional","G+IA","/patrocinadors/",2,"agencies"),
("publicitat en clubs esportius de barri","ca","PATROCINI","transaccional","G+IA","/patrocinadors/",2,"agencies locals"),
("col-laborar amb un club esportiu Sant Marti","ca","PATROCINI","transaccional","G+IA","/patrocinadors/",2,"entitats del districte"),
# --- INSTITUCIONAL -----------------------------------------------------------
("Premi Dona i Esport","ca","INSTITUCIONAL","informacional","G+IA","/premidonaesport/",2,"FCBQ + institucions"),
("clubs de basquet amb paritat real","ca","INSTITUCIONAL","comparacio","G+IA","/premidonaesport/",2,"mitjans + institucions"),
("historia del basquet al Clot","ca","INSTITUCIONAL","informacional","G+IA","/historia/",3,"enciclopedia.cat + premsa"),
("entitats esportives del districte de Sant Marti","ca","INSTITUCIONAL","descobriment","G+IA","/club/",3,"Ajuntament"),
("60 anys club de basquet Barcelona","ca","INSTITUCIONAL","informacional","G+IA","/historia/",3,"premsa local"),
# --- INSTAGRAM (cerques dins l'app) -----------------------------------------
("basquet barcelona","ca","IG-APP","descobriment","IG","perfil @cbgrupbarna",1,"clubs + comptes de highlights"),
("baloncesto barcelona","es","IG-APP","descobriment","IG","perfil @cbgrupbarna",1,"clubs + academies"),
("basquet clot","ca","IG-APP","descobriment","IG","perfil @cbgrupbarna",1,"entitats del barri"),
("basquet base","ca","IG-APP","descobriment","IG","perfil @cbgrupbarna",1,"clubs de tot el pais"),
("basquet femeni","ca","IG-APP","descobriment","IG","perfil @cbgrupbarna",1,"clubs + jugadores"),
("baloncesto femenino","es","IG-APP","descobriment","IG","perfil @cbgrupbarna",1,"clubs + LF Endesa"),
("campus basquet","ca","IG-APP","transaccional","IG","posts de campus",1,"campus nacionals"),
("escola basquet nens","ca","IG-APP","transaccional","IG","posts d'escoleta",2,"escoles + academies"),
("basquet inclusiu","ca","IG-APP","descobriment","IG","posts de Magics",2,"entitats adaptades"),
("3x3 barcelona","ca","IG-APP","descobriment","IG","posts de 3x3",1,"torneigs + FEB"),
("somclot","ca","IG-APP","marca","IG","perfil @cbgrupbarna",1,"qui mes fa servir el hashtag"),
("cb grup barna","ca","IG-APP","marca","IG","perfil @cbgrupbarna",1,"comptes d'equips i jugadors"),
("club basquet barcelona","ca","IG-APP","descobriment","IG","perfil @cbgrupbarna",2,"clubs grans"),
("basquet sant marti","ca","IG-APP","descobriment","IG","perfil @cbgrupbarna",2,"clubs del districte"),
# --- TIKTOK (cerques dins l'app) --------------------------------------------
("basquet barcelona","ca","TT-APP","descobriment","TT","perfil @cbgrupbarna",1,"comptes de highlights + clubs"),
("baloncesto barcelona","es","TT-APP","descobriment","TT","perfil @cbgrupbarna",1,"creadors + academies"),
("baloncesto base","es","TT-APP","descobriment","TT","perfil @cbgrupbarna",1,"creadors + clubs"),
("campus de baloncesto","es","TT-APP","transaccional","TT","videos de campus",1,"campus nacionals + Pau Gasol"),
("baloncesto femenino","es","TT-APP","descobriment","TT","videos femeni",1,"jugadores + lligues"),
("entrenamiento baloncesto ninos","es","TT-APP","informacional","TT","videos d'entreno",1,"entrenadors creadors"),
("jugadas baloncesto ninos","es","TT-APP","descobriment","TT","videos de partit",2,"comptes de highlights"),
("club de baloncesto barcelona","es","TT-APP","descobriment","TT","perfil @cbgrupbarna",2,"clubs grans"),
("baloncesto inclusivo","es","TT-APP","descobriment","TT","videos de Magics",2,"entitats adaptades"),
("3x3 baloncesto","es","TT-APP","descobriment","TT","videos de 3x3",2,"FEB + torneigs"),
("cb grup barna","ca","TT-APP","marca","TT","perfil @cbgrupbarna",1,"comptes d'equips"),
("basquet clot","ca","TT-APP","descobriment","TT","perfil @cbgrupbarna",2,"entitats del barri"),
# --- IA (preguntes reals, no keywords) --------------------------------------
("a quin club de basquet apunto la meva filla a Barcelona","ca","IA-PROMPT","descobriment","IA","/basquet-femeni/",1,"clubs que les IA citin"),
("mejor club de baloncesto base en Barcelona","es","IA-PROMPT","comparacio","IA","/",1,"clubs que les IA citin"),
("clubs de basquet a Barcelona amb equip femeni fort","ca","IA-PROMPT","comparacio","IA","/basquet-femeni/",1,"clubs de LF2 i Copa Catalunya"),
("donde apuntar a un nino de 5 anos a baloncesto en Barcelona","es","IA-PROMPT","transaccional","IA","/escoleta/",1,"escoles + clubs"),
("campus de baloncesto en Barcelona para el verano","es","IA-PROMPT","transaccional","IA","/campus/",1,"campus nacionals"),
("clubs de basquet inclusius a Barcelona","ca","IA-PROMPT","descobriment","IA","/magics/",1,"entitats adaptades"),
("es fiable el CB Grup Barna","ca","IA-PROMPT","verificacio","IA","/opina/",1,"ressenyes + premsa"),
("que clubs de basquet de Barcelona tenen paritat","ca","IA-PROMPT","comparacio","IA","/premidonaesport/",1,"clubs + institucions"),
("club de basquet al districte de Sant Marti","ca","IA-PROMPT","descobriment","IA","/",1,"clubs del districte"),
("quiero patrocinar un club de baloncesto en Barcelona","es","IA-PROMPT","transaccional","IA","/patrocinadors/",2,"agencies + clubs"),
]

import csv, io, unicodedata

with io.open('seo/mapa-paraules-clau.csv','w',encoding='utf-8',newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['id','keyword','idioma','familia','intencio','plataformes','url_objectiu','prioritat','rival_previst'])
    for i,(kw,idi,fam,intent,plat,url,prio,riv) in enumerate(K,1):
        w.writerow(['K%03d'%i,kw,idi,fam,intent,plat,url,prio,riv])

with io.open('seo/full-captura.csv','w',encoding='utf-8',newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['id','keyword','idioma','plataforma','data','sortim_si_no','posicio_barna',
                'url_o_perfil_nostre','rival_1','rival_2','rival_3','captura','notes'])
    for i,(kw,idi,fam,intent,plat,url,prio,riv) in enumerate(K,1):
        for p in plat.split('+'):
            w.writerow(['K%03d'%i,kw,idi,p,'','','','','','','','',''])

print('files:', len(K), 'keywords')
