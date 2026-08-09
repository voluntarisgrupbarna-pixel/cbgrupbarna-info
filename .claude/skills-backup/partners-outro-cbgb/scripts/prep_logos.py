import os, numpy as np
from PIL import Image
from scipy import ndimage
SRC=os.path.expanduser("~/Desktop/reel despres partit/LOGOS PARTNERS")  # carpeta de logos del club

def strip_bg(im, tol=28, glob=False):
    a=np.array(im.convert("RGBA")).astype(int); h,w,_=a.shape
    bg=np.median(np.array([a[0,0,:3],a[0,w-1,:3],a[h-1,0,:3],a[h-1,w-1,:3]]),axis=0)
    d=np.abs(a[:,:,:3]-bg).max(axis=2); sim=(d<=tol)
    lab,_=ndimage.label(sim)
    border=set(np.unique(np.concatenate([lab[0,:],lab[-1,:],lab[:,0],lab[:,-1]]))); border.discard(0)
    mask = sim if glob else np.isin(lab,list(border))
    a[:,:,3]=np.where(mask,0,a[:,:,3])
    o=Image.fromarray(a.astype(np.uint8),"RGBA"); bb=o.getbbox()
    return o.crop(bb) if bb else o

COLOR=255
def to_mono(im, polarity=None, gamma=0.75, cut=0.10):
    a=np.array(im).astype(float); al=a[:,:,3]/255.0
    lum=0.2126*a[:,:,0]+0.7152*a[:,:,1]+0.0722*a[:,:,2]
    m=(lum*al).sum()/max(al.sum(),1)
    p = polarity or ("light_on_dark" if m>140 else "dark_on_light")
    new = (lum/255.0) if p=="light_on_dark" else (1-lum/255.0)
    new = new*al
    hi=np.percentile(new[new>0.02],99.0) if (new>0.02).any() else 1.0
    new=np.clip(new/max(hi,0.15),0,1)
    new=np.clip((new-cut)/max(1-cut-0.10,0.05),0,1)**gamma          # limpia antialias, sube blancos
    out=np.zeros_like(a); out[:,:,0:3]=COLOR; out[:,:,3]=new*255
    o=Image.fromarray(out.astype(np.uint8),"RGBA"); bb=o.getbbox()
    return o.crop(bb) if bb else o

M=[("158429743_925773448169577_4767881054911754348_n.jpg","globasket"),
("2429_Logo.1742686758.jpg","herbolari_montserrat"),
("472134134_950981203667438_2630081767870011661_n.jpg","stepback"),
("AGUAMIGA.webp","aquamiga"),("ARMAND.jpg","armand"),
("Captura de pantalla 2025-12-21 a las 16.48.40.png","instax"),
("Captura de pantalla 2026-01-08 a las 15.55.35.png","time_chamber"),
("Captura de pantalla 2026-01-17 a las 16.51.28.png","mercat_encants"),
("Captura de pantalla 2026-01-17 a las 16.52.54.png","illa_fantasia"),
("Captura de pantalla 2026-01-17 a las 16.53.47.png","aquarium_bcn"),
("Captura de pantalla 2026-01-30 a las 17.40.13.png","mullor"),
("Captura de pantalla 2026-01-30 a las 17.45.40.png","bac_de_roda"),
("Captura de pantalla 2026-02-16 a las 15.53.19.png","westfield_glories"),
("Captura de pantalla 2026-04-13 a las 18.46.36.png","foto_jane"),
("Captura de pantalla 2026-04-13 a las 18.59.54.png","eix_clot"),
("LOGO_CE_VILA_OLIMPICA.png","ce_vila_olimpica"),
("OVELLA.png","ovella_negra"),("TOT SALUT.jpg","tot_salut"),
("logo-melosa.png","melosa"),("romeo_abogados.gif","romeo_abogados"),
("zapic_name_logo.png","zapic"),
("logoajuntamentsantmartinegre.png","districte_sant_marti"),
("harm_esportcat_RGB_vertical.png","esportcat_generalitat")]
CROP={"districte_sant_marti":0.38}
GLOB=set()
CUT={"armand":0.30}
TOL={"armand":78,"aquarium_bcn":60,"time_chamber":60,"zapic":60,"foto_jane":80,"mullor":60}
GAM={"armand":2.0,"romeo_abogados":0.45,"bac_de_roda":0.45,"tot_salut":0.55,"aquamiga":0.55,"stepback":0.6,"herbolari_montserrat":0.6}
POL={"tot_salut":"dark_on_light","armand":"light_on_dark","time_chamber":"light_on_dark",
     "aquarium_bcn":"light_on_dark","districte_sant_marti":"light_on_dark"}
os.makedirs("logos_color",exist_ok=True); os.makedirs("logos_mono",exist_ok=True); os.makedirs("logos_black",exist_ok=True)
for f,n in M:
    im=Image.open(os.path.join(SRC,f)).convert("RGBA")
    if n in CROP: im=im.crop((0,int(im.height*CROP[n]),im.width,im.height))
    c=strip_bg(im,TOL.get(n,28),n in GLOB); c.save(f"logos_color/{n}.png")
    to_mono(c,POL.get(n),GAM.get(n,0.75),CUT.get(n,0.10)).save(f"logos_mono/{n}.png")
    globals()['COLOR']=10
    to_mono(c,POL.get(n),GAM.get(n,0.75),CUT.get(n,0.10)).save(f"logos_black/{n}.png")
    globals()['COLOR']=255
e=strip_bg(Image.open(os.path.join(SRC,"LOGO_BARNA_HD.png")))
e.save("escut_color.png"); to_mono(e,"dark_on_light").save("escut_mono.png")
globals()['COLOR']=10; to_mono(e,"dark_on_light").save("escut_black.png"); globals()['COLOR']=255
print("ok")
