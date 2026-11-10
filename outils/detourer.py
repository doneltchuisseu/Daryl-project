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

Emballage blanc sur fond blanc (brique, film plastique) : si le détourage
« mange » le produit, baisser la tolérance de cette image dans
outils/detourage-reglages.txt (ex. « jus-pomme-pack12 8 »).
Pastille ou logo de vendeur détaché du produit : ajouter « principal »
(ex. « sprite-verre-24 principal ») pour ne garder que le produit.
"""
import sys
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

RACINE = Path(__file__).resolve().parent.parent
ENTREE = Path(sys.argv[1]) if len(sys.argv) > 1 else RACINE / "livrables/src/images/originaux"
SORTIE = Path(sys.argv[2]) if len(sys.argv) > 2 else RACINE / "livrables/src/images"
TOL = int(sys.argv[3]) if len(sys.argv) > 3 else 22
PRINCIPAL = False  # True : ne garder que le plus grand objet de l'image
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
    if PRINCIPAL:
        masque = garder_principal(masque)
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


def garder_principal(masque: Image.Image) -> Image.Image:
    """Ne garde que le plus grand objet (enlève pastilles, logos de vendeur…)."""
    w, h = masque.size
    m = masque.load()
    vu = bytearray(w * h)
    meilleur: list[int] = []
    for y0 in range(h):
        for x0 in range(w):
            if vu[y0 * w + x0] or m[x0, y0] < 128:
                continue
            groupe, pile = [], [(x0, y0)]
            vu[y0 * w + x0] = 1
            while pile:
                x, y = pile.pop()
                groupe.append(y * w + x)
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= nx < w and 0 <= ny < h and not vu[ny * w + nx] and m[nx, ny] >= 128:
                        vu[ny * w + nx] = 1
                        pile.append((nx, ny))
            if len(groupe) > len(meilleur):
                meilleur = groupe
    garde = bytearray(w * h)
    for i in meilleur:
        garde[i] = 255
    return Image.frombytes("L", (w, h), bytes(garde))


def reglages() -> dict[str, tuple[int | None, bool]]:
    """Réglages par image, lus dans outils/detourage-reglages.txt :
    « nom [tolérance] [principal] »."""
    f = RACINE / "outils/detourage-reglages.txt"
    if not f.exists():
        return {}
    out = {}
    for ligne in f.read_text(encoding="utf-8").splitlines():
        mots = ligne.split("#")[0].split()
        if not mots:
            continue
        tol = next((int(m) for m in mots[1:] if m.isdigit()), None)
        out[mots[0]] = (tol, "principal" in mots[1:])
    return out


def main():
    global TOL, PRINCIPAL
    SORTIE.mkdir(parents=True, exist_ok=True)
    tol_defaut, par_image = TOL, reglages()
    fichiers = sorted(p for p in ENTREE.iterdir() if p.suffix.lower() in EXTENSIONS)
    if not fichiers:
        print(f"Aucune image dans {ENTREE}")
        return
    for src in fichiers:
        dst = SORTIE / (src.stem + ".webp")
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            print(f"  déjà fait   {src.name}")
            continue
        tol, PRINCIPAL = par_image.get(src.stem, (None, False))
        TOL = tol if tol is not None else tol_defaut
        try:
            taille = detourer(src, dst)
            petit = "  ⚠ image source petite, risque de flou" if min(Image.open(src).size) < 800 else ""
            print(f"  détouré     {src.name} -> {dst.name} {taille}{petit}")
        except Exception as e:  # une image ratée ne bloque pas le lot
            print(f"  ÉCHEC       {src.name} : {e}")


if __name__ == "__main__":
    main()
