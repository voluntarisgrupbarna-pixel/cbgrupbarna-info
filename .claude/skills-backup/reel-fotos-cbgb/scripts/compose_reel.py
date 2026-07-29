#!/usr/bin/env python3
"""
compose_reel.py — compositor de plans d'un reel CB Grup Barna (fotos + Anton + escut).
Ús:   LANG=ca python3 compose_reel.py         (o LANG=es)
Entrada: fotos a ./src/  |  Sortida: PNGs 1080x1920 a ./scenes/
Edita el diccionari SCENES per canviar guió, fotos i trams.
Tokens de marca: sistema-visual-cbgb (#0E1116 / #E63329 / Anton / Inter / marge 80).
"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os

W, H = 1080, 1920
DARK = (14, 17, 22)       # #0E1116
RED = (230, 51, 41)       # #E63329
WHITE = (245, 245, 247)
MARGIN = 80
LANG = os.environ.get("LANG_REEL", os.environ.get("LANG", "ca"))[:2]
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
ANTON = os.path.join(ASSETS, "Anton.ttf")
INTER = os.path.join(ASSETS, "Inter.ttf")
CRESTP = os.path.join(ASSETS, "escut_transp.png")
SRC, OUT = "src", "scenes"
os.makedirs(OUT, exist_ok=True)
CREST = Image.open(CRESTP).convert("RGBA")

# ---------- GUIÓ (edita això) ----------
# tipus: hook | burst | line | drop | cta   |   t(ca), t(es) = text per idioma
def T(ca, es): return {"ca": ca, "es": es}[LANG if LANG in ("ca","es") else "ca"]

SCENES = [
 dict(id="h1", type="hook", img="cover8.jpg", vbias=0.08, ypos=0.66, dark=0.5,
      line=lambda: T("AIXÒ NO ES VEN","ESTO NO SE VENDE"), color="white"),
 dict(id="h2", type="hook", img="hookA.jpg", vbias=0.40, dark=0.60,
      line=lambda: T("AMB UN LOGO","CON UN LOGO"), color="red"),
 dict(id="b1", type="burst", img="b1_families.jpg", vbias=0.35, big="+450",
      small=lambda: T("FAMÍLIES","FAMILIAS")),
 dict(id="b2", type="burst", img="team36.jpg", vbias=0.20, big="36",
      small=lambda: T("EQUIPS","EQUIPOS")),
 dict(id="b3", type="burst", img="b3_escoleta.jpg", vbias=0.30, big="",
      small=lambda: T("ESCOLETA","ESCUELA")),
 dict(id="b4", type="burst", img="b4_campus.jpg", vbias=0.30, big="",
      small=lambda: "CAMPUS"),
 dict(id="b5", type="burst", img="b5_3x3.jpg", vbias=0.35, big="3x3",
      small=lambda: "GLÒRIES"),
 dict(id="b6", type="burst", img="b6_magics.jpg", vbias=0.25, big="",
      small=lambda: "MÀGICS"),
 dict(id="b7", type="burst", img="girl33.jpg", vbias=0.12, big="",
      small=lambda: T("PARITAT REAL","PARIDAD REAL")),
 dict(id="b8", type="burst", img="b8_barri.jpg", vbias=0.25, big="1",
      small=lambda: T("BARRI","BARRIO")),
 dict(id="emo", type="line", img="emo.jpg", vbias=0.32, dark=0.46, size=104,
      lines=lambda: T(["Cada dissabte,","el Clot es troba aquí"],
                      ["Cada sábado,","el Clot se encuentra aquí"])),
 dict(id="build", type="line", img="build.jpg", vbias=0.30, dark=0.50, size=104,
      red_first=True,
      lines=lambda: T(["Una comunitat real.","No un impacte buit."],
                      ["Una comunidad real.","No un impacto vacío."])),
 dict(id="drop", type="drop",
      lines=lambda: T(["LA TEVA MARCA,","DINS DEL BARNA"],
                      ["TU MARCA,","DENTRO DEL BARNA"]),
      sub=lambda: "TEMPORADA 26 / 27"),
 dict(id="cta", type="cta",
      lines=lambda: T(["VOLS SER","PARTNER?"],["¿QUIERES SER","PARTNER?"]),
      button=lambda: T("ESCRIU-NOS «PARTNER»","ESCRÍBENOS «PARTNER»"),
      handle="@cbgrupbarna"),
]

# ---------- helpers ----------
def font(p, s): return ImageFont.truetype(p, s)
def col(name): return RED if name == "red" else WHITE

def fit_font(path, size, text, tr, maxw=W-2*MARGIN):
    while size > 40:
        f = ImageFont.truetype(path, size)
        d = ImageDraw.Draw(Image.new("RGB",(4,4)))
        w = sum(d.textlength(c,font=f)+tr for c in text)-tr
        if w <= maxw: return f
        size -= 6
    return ImageFont.truetype(path, size)

def fill_crop(path, vbias=0.5, zoom=1.0):
    im = Image.open(path).convert("RGB"); iw, ih = im.size
    s = max(W/iw, H/ih)*zoom; nw, nh = int(iw*s), int(ih*s)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw-W)//2; y = int((nh-H)*vbias)
    x = max(0, min(x, nw-W)); y = max(0, min(y, nh-H))
    return im.crop((x, y, x+W, y+H))

def brand(im, dark=0.44, desat=0.72, bottom=0.9, top=0.4):
    im = ImageEnhance.Color(im).enhance(desat)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    base = Image.blend(im.convert("RGB"), Image.new("RGB",(W,H),DARK), dark*0.55)
    base = Image.blend(base, Image.new("RGB",(W,H),(60,0,0)), 0.05)
    g = Image.new("L",(1,H),0)
    for yy in range(H):
        t=yy/H; b=max(0,(t-0.45)/0.55)**1.4*(bottom*255); tp=max(0,(0.30-t)/0.30)**1.4*(top*255)
        g.putpixel((0,yy),int(min(255,b+tp)))
    g=g.resize((W,H))
    return Image.composite(Image.new("RGB",(W,H),(6,7,10)), base, g).convert("RGB")

def spaced(d, xy, text, fnt, fill, tr=0, cx=None):
    ws=[d.textlength(c,font=fnt)+tr for c in text]; tot=sum(ws)-(tr if text else 0)
    x,y=xy
    if cx is not None: x=cx-tot/2
    for c,w in zip(text,ws): d.text((x,y),c,font=fnt,fill=fill); x+=w
    return tot

def lh(f): a,dd=f.getmetrics(); return a+dd

def watermark(im, size=132):
    c=CREST.copy(); r=size/c.height; c=c.resize((int(c.width*r),size),Image.LANCZOS)
    pad=22; cw,ch=c.size; chip=Image.new("RGBA",(cw+pad*2,ch+pad*2),(0,0,0,0))
    ImageDraw.Draw(chip).rounded_rectangle([0,0,cw+pad*2,ch+pad*2],radius=26,fill=(10,12,16,150))
    chip.alpha_composite(c,(pad,pad))
    b=im.convert("RGBA"); b.alpha_composite(chip,(MARGIN-10,MARGIN-10)); return b.convert("RGB")

# ---------- renderers ----------
def r_hook(s):
    bg=brand(fill_crop(f"{SRC}/{s['img']}",s['vbias'],1.05),dark=s.get('dark',0.6),desat=0.6,bottom=0.85,top=0.5)
    bg=watermark(bg); d=ImageDraw.Draw(bg); line=s['line']()
    fnt=fit_font(ANTON,176,line,5); y=int(H*s['ypos']) if s.get('ypos') else (H-lh(fnt))//2-20
    spaced(d,(0,y),line,fnt,col(s['color']),tr=5,cx=W//2)
    d.rectangle([W//2-70,y+lh(fnt)+16,W//2+70,y+lh(fnt)+28],fill=RED); bg.save(f"{OUT}/{s['id']}.png")

def r_burst(s):
    bg=brand(fill_crop(f"{SRC}/{s['img']}",s['vbias'],1.02),dark=0.40,bottom=1.0); bg=watermark(bg,112)
    d=ImageDraw.Draw(bg); big=s['big']; small=s['small']()
    if big:
        bf=font(ANTON,300 if len(big)<=4 else 210); spaced(d,(0,H//2-300),big.upper(),bf,WHITE,tr=4,cx=W//2)
    if small:
        sf=font(ANTON,92); sw=spaced(ImageDraw.Draw(Image.new("RGB",(4,4))),(0,0),small.upper(),sf,WHITE,tr=8)
        yb=H//2+70; d.rectangle([W//2-sw/2-36,yb-6,W//2+sw/2+36,yb+lh(sf)+2],fill=RED)
        spaced(d,(0,yb),small.upper(),sf,WHITE,tr=8,cx=W//2)
    bg.save(f"{OUT}/{s['id']}.png")

def r_line(s):
    bg=brand(fill_crop(f"{SRC}/{s['img']}",s['vbias']),dark=s.get('dark',0.46)); bg=watermark(bg)
    d=ImageDraw.Draw(bg); lines=s['lines']()
    fnt=min((fit_font(ANTON,s.get('size',104),l.upper(),2) for l in lines),key=lambda f:f.size)
    size=fnt.size; lhh=int(size*1.02); blk=lhh*len(lines); y0=H-190-blk
    d.rectangle([MARGIN+10,y0-34,MARGIN+130,y0-22],fill=RED); y=y0
    for i,l in enumerate(lines):
        c=RED if (s.get('red_first') and i==0) else WHITE
        spaced(d,(0,y),l.upper(),fnt,c,tr=2,cx=W//2); y+=lhh
    bg.save(f"{OUT}/{s['id']}.png")

def r_drop(s):
    bg=Image.new("RGB",(W,H),DARK); d=ImageDraw.Draw(bg)
    c=CREST.copy(); ch=560; r=ch/c.height; c=c.resize((int(c.width*r),ch),Image.LANCZOS)
    bg.paste(c,(W//2-c.width//2,300),c); d.rectangle([W//2-300,300+ch+50,W//2+300,300+ch+62],fill=RED)
    lines=s['lines'](); mf=font(ANTON,92)
    spaced(d,(0,300+ch+95),lines[0],mf,WHITE,tr=4,cx=W//2)
    spaced(d,(0,300+ch+95+int(92*1.05)),lines[1],mf,RED,tr=4,cx=W//2)
    spaced(d,(0,300+ch+95+int(92*1.05)*2+30),s['sub'](),font(INTER,50),WHITE,tr=10,cx=W//2)
    bg.save(f"{OUT}/{s['id']}.png")

def r_cta(s):
    bg=Image.new("RGB",(W,H),RED); d=ImageDraw.Draw(bg)
    c=CREST.copy(); ch=300; r=ch/c.height; c=c.resize((int(c.width*r),ch),Image.LANCZOS)
    bg.paste(c,(W//2-c.width//2,250),c); lines=s['lines'](); f=font(ANTON,128)
    spaced(d,(0,H//2-120),lines[0],f,WHITE,tr=6,cx=W//2)
    spaced(d,(0,H//2-120+int(128*1.02)),lines[1],f,DARK,tr=6,cx=W//2)
    pf=fit_font(ANTON,88,s['button'](),4,maxw=W-160); label=s['button']()
    pw=spaced(ImageDraw.Draw(Image.new("RGB",(4,4))),(0,0),label,pf,WHITE,tr=4); yb=H//2+170
    d.rounded_rectangle([W//2-pw/2-50,yb-20,W//2+pw/2+50,yb+lh(pf)+6],radius=22,fill=DARK)
    spaced(d,(0,yb),label,pf,WHITE,tr=4,cx=W//2)
    spaced(d,(0,yb+210),s['handle'],font(INTER,58),WHITE,tr=4,cx=W//2); bg.save(f"{OUT}/{s['id']}.png")

R={"hook":r_hook,"burst":r_burst,"line":r_line,"drop":r_drop,"cta":r_cta}
if __name__=="__main__":
    for s in SCENES: R[s["type"]](s)
    print(f"[{LANG}] plans generats a {OUT}/:", ", ".join(s["id"] for s in SCENES))
