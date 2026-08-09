#!/usr/bin/env python3
"""CARTELA DE PARTNERS — outro obligatorio de todo reel del CB Grup Barna.
Genera:  outro_partners_dark.png / outro_partners_light.png (1080x1920)
         outro_partners_dark.mp4 / outro_partners_light.mp4 (3 s, 9:16, 30 fps)
Editar la lista PARTNERS / INSTIT y volver a ejecutar cuando entre o salga un partner.
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

S=2                      # supersampling
W,H = 1080*S,1920*S
RED=(253,3,12); BLACK=(10,10,10); WHITE=(255,255,255)
BASE=os.path.dirname(os.path.abspath(__file__))
ANTON=os.path.join(BASE,"assets/Anton.ttf")
INTER=os.path.join(BASE,"assets/Inter.ttf")

PARTNERS=["globasket","herbolari_montserrat","stepback","aquamiga","armand","instax",
"time_chamber","mercat_encants","illa_fantasia","aquarium_bcn","mullor","bac_de_roda",
"westfield_glories","foto_jane","eix_clot","ce_vila_olimpica","ovella_negra","tot_salut",
"melosa","romeo_abogados","zapic"]
INSTIT=["districte_sant_marti","esportcat_generalitat"]
COLS,ROWS=4,6

def fit(im,bw,bh):
    im=im.copy(); im.thumbnail((bw,bh),Image.LANCZOS); return im
def ctr(dr,txt,f,y,fill,c):
    b=dr.textbbox((0,0),txt,font=f); dr.text(((W-(b[2]-b[0]))//2-b[0],y),txt,font=f,fill=fill)

def card(dark=True):
    d_=os.path.join(BASE,"logos_mono" if dark else "logos_black")
    bg,ink = (BLACK,WHITE) if dark else (WHITE,BLACK)
    c=Image.new("RGBA",(W,H),bg+(255,)); dr=ImageDraw.Draw(c)
    escut=Image.open(os.path.join(BASE,"escut_mono.png" if dark else "escut_black.png")).convert("RGBA")
    e=fit(escut,230*S,185*S); c.alpha_composite(e,((W-e.width)//2,155*S))
    ctr(dr,"GRÀCIES",ImageFont.truetype(ANTON,66*S),382*S,RED,c)
    ctr(dr,"ALS QUI FAN POSSIBLE EL CB GRUP BARNA",ImageFont.truetype(INTER,26*S),470*S,ink,c)
    x0,x1,y0,y1 = 70*S,1010*S,545*S,1270*S
    cw=(x1-x0)/COLS; ch=(y1-y0)/ROWS
    bw,bh=int(cw-26*S),int(ch-30*S)
    n=len(PARTNERS)
    for i,name in enumerate(PARTNERS):
        p=os.path.join(d_,name+".png")
        if not os.path.exists(p): print("  ! falta logo:",name); continue
        im=fit(Image.open(p).convert("RGBA"),bw,bh)
        row,col=divmod(i,COLS)
        in_row=min(COLS,n-row*COLS)
        off=(COLS-in_row)*cw/2                      # centra la última fila incompleta
        cx=x0+off+cw*col+cw/2; cy=y0+ch*row+ch/2
        c.alpha_composite(im,(int(cx-im.width/2),int(cy-im.height/2)))
    dr.line([(370*S,1318*S),(710*S,1318*S)],fill=RED,width=3*S)
    ctr(dr,"AMB EL SUPORT DE",ImageFont.truetype(INTER,22*S),1348*S,ink,c)
    for i,name in enumerate([380,700]):
        im=fit(Image.open(os.path.join(d_,INSTIT[i]+".png")).convert("RGBA"),250*S,115*S)
        c.alpha_composite(im,(int(name*S-im.width/2),int(1450*S-im.height/2)))
    ctr(dr,"@cbgrupbarna",ImageFont.truetype(ANTON,34*S),1552*S,RED,c)
    return c.convert("RGB").resize((1080,1920),Image.LANCZOS), c.convert("RGB")

def video(png,out):
    subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-i",png,
        "-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-t","3",
        "-vf","zoompan=z='min(zoom+0.00035,1.04)':d=90:s=1080x1920:fps=30,"
              "fade=t=in:st=0:d=0.35,fade=t=out:st=2.7:d=0.3,format=yuv420p",
        "-c:v","libx264","-preset","slow","-crf","18","-r","30",
        "-c:a","aac","-b:a","128k","-shortest",out],check=True)

if __name__=="__main__":
    for dark in (True,False):
        tag="dark" if dark else "light"
        small,big=card(dark)
        small.save(f"outro_partners_{tag}.png")
        big.save(f"_hi_{tag}.png")
        video(f"_hi_{tag}.png",f"outro_partners_{tag}.mp4")
        print("OK",tag)
