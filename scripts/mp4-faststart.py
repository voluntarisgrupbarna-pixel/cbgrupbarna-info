#!/usr/bin/env python3
"""Mou l'index d'un MP4 al davant perque el video pugui comencar a veure's.

Un MP4 porta les dades (`mdat`) i l'index que diu on es cada fotograma
(`moov`). Si l'index queda al final, el navegador no pot ensenyar res —ni saber
quant dura— fins que s'ha baixat el fitxer sencer. Amb un reel de 30 MB, en un
mobil, aixo son molts segons de pantalla quieta: sembla que no hi hagi video.

Aixo es el que fa `qt-faststart` de tota la vida, escrit aqui perque el
repositori no depengui de tenir ffmpeg instal.lat. No re-codifica res: mou
l'atom `moov` davant de `mdat` i suma el desplacament a les taules de posicions
(`stco` de 32 bits i `co64` de 64), que son les que diuen a quin byte comenca
cada tros de video. Els bytes de video no es toquen.

    python3 scripts/mp4-faststart.py mascota/mascota-reel.mp4
    python3 scripts/mp4-faststart.py --comprova mascota/mascota-reel.mp4
"""
import shutil
import struct
import sys
from pathlib import Path


def llegeix_atoms(dades, inici=0, final=None):
    """Llista (tipus, posicio, mida, mida_capcalera) del nivell superior."""
    final = len(dades) if final is None else final
    out, i = [], inici
    while i + 8 <= final:
        mida = struct.unpack(">I", dades[i:i + 4])[0]
        tipus = dades[i + 4:i + 8].decode("latin1", "replace")
        cap = 8
        if mida == 1:
            mida = struct.unpack(">Q", dades[i + 8:i + 16])[0]
            cap = 16
        elif mida == 0:
            mida = final - i
        if mida < cap:
            break
        out.append((tipus, i, mida, cap))
        i += mida
    return out


def desplaça_taules(moov, delta):
    """Suma `delta` a tots els stco/co64 de dins del moov. Torna les posicions
    velles i noves, per poder-ho comprovar despres."""
    dades = bytearray(moov)
    canvis = []

    def recorre(inici, final):
        for tipus, pos, mida, cap in llegeix_atoms(dades, inici, final):
            if tipus in ("moov", "trak", "mdia", "minf", "stbl", "edts", "udta"):
                recorre(pos + cap, pos + mida)
            elif tipus in ("stco", "co64"):
                amplada = 4 if tipus == "stco" else 8
                p = pos + cap + 4                      # versio + banderes
                n = struct.unpack(">I", dades[p:p + 4])[0]
                p += 4
                for _ in range(n):
                    if amplada == 4:
                        v = struct.unpack(">I", dades[p:p + 4])[0]
                        nou = v + delta
                        if nou >= 2 ** 32:
                            sys.exit("El desplacament no cap en un stco de 32 bits.")
                        dades[p:p + 4] = struct.pack(">I", nou)
                    else:
                        v = struct.unpack(">Q", dades[p:p + 8])[0]
                        nou = v + delta
                        dades[p:p + 8] = struct.pack(">Q", nou)
                    canvis.append((v, nou))
                    p += amplada

    recorre(0, len(dades))
    return bytes(dades), canvis


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    nomes_comprova = "--comprova" in sys.argv
    if not args:
        sys.exit(__doc__)
    cami = Path(args[0])
    original = cami.read_bytes()
    atoms = llegeix_atoms(original)
    tipus = [t for t, *_ in atoms]
    if "moov" not in tipus or "mdat" not in tipus:
        sys.exit(f"{cami}: no hi trobo moov o mdat.")
    if tipus.index("moov") < tipus.index("mdat"):
        print(f"{cami}: l'index ja es al davant, no cal tocar res.")
        return
    if nomes_comprova:
        print(f"{cami}: l'index es al final — el video no pot comencar fins "
              f"que s'ha baixat sencer ({len(original) // 1024 // 1024} MB).")
        return

    moov = next(a for a in atoms if a[0] == "moov")
    mdat = next(a for a in atoms if a[0] == "mdat")
    moov_bytes = original[moov[1]:moov[1] + moov[2]]

    # L'ordre nou: tot el que ja hi havia abans del mdat, despres el moov, i
    # despres el mdat i la resta. El moov queda davant de les dades, que es
    # tot el que cal perque el navegador pugui comencar.
    abans = [a for a in atoms if a[0] != "moov" and a[1] < mdat[1]]
    despres = [a for a in atoms if a[0] != "moov" and a[1] >= mdat[1]]
    davant = b"".join(original[p:p + m] for _, p, m, _ in abans)
    darrere = b"".join(original[p:p + m] for _, p, m, _ in despres)

    # Tot el que hi ha des del mdat cap avall s'endarrereix exactament la mida
    # del moov, que es el que s'hi ha ficat pel mig.
    delta = len(moov_bytes)
    moov_nou, canvis = desplaça_taules(moov_bytes, delta)
    nou = davant + moov_nou + darrere

    if len(nou) != len(original):
        sys.exit("La mida no quadra; no escric res.")

    # Comprovacio de veritat, i de totes les posicions, no d'una mostra: cada
    # entrada de la taula ha d'apuntar exactament als mateixos bytes que abans.
    # Sense un descodificador a ma per mirar-ho, aixo es el que dona la
    # seguretat que el video segueix sent el mateix.
    for vell, nouv in canvis:
        if original[vell:vell + 32] != nou[nouv:nouv + 32]:
            sys.exit(f"La posicio {vell} ja no apunta als mateixos bytes. No escric res.")

    copia = cami.with_suffix(cami.suffix + ".original")
    if not copia.exists():
        shutil.copy2(cami, copia)
    cami.write_bytes(nou)
    print(f"{cami}: index mogut al davant. {len(canvis)} posicions desplaçades "
          f"{delta} bytes, totes comprovades. Copia a {copia.name}.")


if __name__ == "__main__":
    main()
