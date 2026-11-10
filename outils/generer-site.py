"""Génère les données et les images du site à partir du catalogue.

Usage : python3 outils/generer-site.py

Lit   livrables/catalogue-produits.csv   (séparateur « ; »)
      livrables/src/images/<image>.webp  (photos détourées par detourer.py)
Écrit site/data/produits.js               (window.PRODUITS = [...])
      site/images/<image>.webp           (hauteur max 900 px, poids réduit)

Seules les lignes avec publier = « oui » vont sur le site.
À relancer après chaque modification du catalogue ou ajout de photos.
"""
import csv
import json
import shutil
from pathlib import Path

from PIL import Image

RACINE = Path(__file__).resolve().parent.parent
CATALOGUE = RACINE / "livrables/catalogue-produits.csv"
IMAGES_SRC = RACINE / "livrables/src/images"
SITE = RACINE / "site"
HAUTEUR_WEB = 900

# Ordre d'affichage des familles sur le site
ORDRE_FAMILLES = ["Eaux", "Sodas", "Jus et nectars", "Thés glacés", "Sirops", "Boissons maltées", "Petit-déjeuner", "Cafés", "Bébé et enfants"]


def main():
    lignes = list(csv.DictReader(CATALOGUE.open(encoding="utf-8"), delimiter=";"))
    (SITE / "data").mkdir(parents=True, exist_ok=True)
    (SITE / "images").mkdir(parents=True, exist_ok=True)

    produits, manquantes = [], []
    for l in lignes:
        if l.get("publier", "oui").strip().lower() != "oui":
            continue
        src = IMAGES_SRC / f"{l['image']}.webp"
        if not src.exists():
            manquantes.append(l["image"])
            continue
        dst = SITE / "images" / src.name
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            im = Image.open(src)
            if im.height > HAUTEUR_WEB:
                im = im.resize((round(im.width * HAUTEUR_WEB / im.height), HAUTEUR_WEB), Image.LANCZOS)
            im.save(dst, "WEBP", quality=82, method=6)
        produits.append({
            "id": l["image"],
            "nom": l["nom"],
            "marque": l["marque"],
            "format": l["format"],
            "rayon": l["rayon"],
            "famille": l.get("famille") or "Autres",
            "prix": int(l["prix_fcfa"]),
            "etiquette": l["etiquette"],
            "image": f"images/{src.name}",
            "pack": any(m in l["format"].lower() for m in ("bouteilles", "canettes", "pack")),
            "verre": "verre" in (l["format"] + l["nom"]).lower(),
        })

    familles = sorted({p["famille"] for p in produits},
                      key=lambda f: ORDRE_FAMILLES.index(f) if f in ORDRE_FAMILLES else 99)
    js = ("// Fichier généré par outils/generer-site.py — ne pas modifier à la main.\n"
          f"window.PRODUITS = {json.dumps(produits, ensure_ascii=False, indent=1)};\n"
          f"window.FAMILLES = {json.dumps(familles, ensure_ascii=False)};\n")
    (SITE / "data/produits.js").write_text(js, encoding="utf-8")

    # Polices de la charte
    shutil.copytree(RACINE / "livrables/src/fonts", SITE / "fonts", dirs_exist_ok=True)

    print(f"{len(produits)} produits publiés, {len(familles)} familles : {', '.join(familles)}")
    if manquantes:
        print("Photo détourée introuvable pour :", ", ".join(manquantes))


if __name__ == "__main__":
    main()
