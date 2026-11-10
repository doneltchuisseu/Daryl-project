"""Détoure en lot les photos produit sur fond blanc.

Usage :
    python3 outils/detourer.py                      # dossiers par défaut
    python3 outils/detourer.py ENTREE SORTIE [TOL]

Par défaut, lit livrables/src/images/originaux/ et écrit des .webp
transparents dans livrables/src/images/ (même nom de fichier).
Les images déjà traitées et plus récentes que l'original sont ignorées.

Méthode : on « remplit » le fond blanc à partir des bords de l'image,
donc les zones blanches à l'intérieur du produit (logos, verres…) sont gardées.
Ne marche que sur fond blanc uni : une photo sur fond coloré ou en situation
doit être détourée à la main.
"""
import sys
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

RACINE = Path(__file__).resolve().parent.parent
ENTREE = Path(sys.argv[1]) if len(sys.argv) > 1 else RACINE / "livrables/src/images/originaux"
SORTIE = Path(sys.argv[2]) if len(sys.argv) > 2 else RACINE / "livrables/src/images"
TOL = int(sys.argv[3]) if len(sys.argv) > 3 else 22
HAUTEUR_MIN = 1200  # px : hauteur minimale de sortie, pour un rendu homogène
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def detourer(src: Path, dst: Path) -> tuple[int, int]:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    px = im.load()

    def presque_blanc(p):
        return min(p) >= 255 - TOL and max(p) - min(p) <= 14

    fond = bytearray(w * h)
    file = deque([(x, y) for x in range(w) for y in (0, h - 1)] +
                 [(x, y) for y in range(h) for x in (0, w - 1)])
    while file:
        x, y = file.popleft()
        i = y * w + x
        if fond[i] or not presque_blanc(px[x, y]):
            continue
        fond[i] = 1
        if x > 0: file.append((x - 1, y))
        if x < w - 1: file.append((x + 1, y))
        if y > 0: file.append((x, y - 1))
        if y < h - 1: file.append((x, y + 1))

    masque = Image.new("L", (w, h))
    masque.putdata([0 if f else 255 for f in fond])
    masque = masque.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    rgba = im.convert("RGBA")
    rgba.putalpha(masque)
    cadre = masque.point(lambda v: 255 if v > 30 else 0).getbbox()
    if not cadre:
        raise ValueError("image entièrement blanche")
    rgba = rgba.crop(cadre)
    if rgba.height < HAUTEUR_MIN:
        rgba = rgba.resize((round(rgba.width * HAUTEUR_MIN / rgba.height), HAUTEUR_MIN), Image.LANCZOS)
    rgba.save(dst, "WEBP", quality=90)
    return rgba.size


def main():
    SORTIE.mkdir(parents=True, exist_ok=True)
    fichiers = sorted(p for p in ENTREE.iterdir() if p.suffix.lower() in EXTENSIONS)
    if not fichiers:
        print(f"Aucune image dans {ENTREE}")
        return
    for src in fichiers:
        dst = SORTIE / (src.stem + ".webp")
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            print(f"  déjà fait   {src.name}")
            continue
        try:
            taille = detourer(src, dst)
            petit = "  ⚠ image source petite, risque de flou" if min(Image.open(src).size) < 800 else ""
            print(f"  détouré     {src.name} -> {dst.name} {taille}{petit}")
        except Exception as e:  # une image ratée ne bloque pas le lot
            print(f"  ÉCHEC       {src.name} : {e}")


if __name__ == "__main__":
    main()
