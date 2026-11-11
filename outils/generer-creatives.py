"""Génère les 4 créatives de campagne TIMAINI LES COURSES (1080 x 1350).

Usage : python3 outils/generer-creatives.py   puis   node outils/rendre-creatives.js

Chaque créative suit un levier de l'équation de valeur d'Alex Hormozi :
  1. Résultat rêvé       -> « Le frigo plein, sans sortir de chez vous »
  2. Probabilité / risque -> « Vous payez seulement à la réception »
  3. La stack d'offre    -> « Vos courses, et tout ça inclus »
  4. Effort supprimé     -> « Les packs lourds ? C'est nous qui les portons »
Aucune promesse de délai de livraison (demande du client).
"""
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
OUT = RACINE / "livrables/creatives"
SITE_URL = "sitejaune.vercel.app"   # adresse du site retenu : à remplacer par le nom de domaine définitif

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:"Quicksand",system-ui,sans-serif;color:#3A2316;position:relative;
  background:radial-gradient(120% 90% at 75% 45%,#FFD65A 0%,#F7B731 48%,#E9A23B 100%)}
.rays{position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 74% 55%,rgba(255,255,255,.13) 0 6deg,transparent 6deg 18deg)}
.grain{position:absolute;inset:0;background-image:radial-gradient(rgba(58,35,22,.06) 1px,transparent 1px);background-size:4px 4px}
.top{position:absolute;left:72px;top:64px;right:72px;display:flex;justify-content:space-between;align-items:center}
.logo{font-family:"Bowlby One",sans-serif;font-size:36px;line-height:.88;color:#C8232C;text-transform:uppercase}
.logo small{display:block;font-size:.42em;color:#3A2316;letter-spacing:.14em}
.badge{background:#3A2316;color:#FFF6E0;border-radius:999px;padding:12px 26px;font-size:23px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
h1{position:absolute;left:72px;top:170px;font-family:"Bowlby One",sans-serif;line-height:.98;text-transform:uppercase;color:#3A2316;text-shadow:0 6px 0 #FFF6E0}
h1 em{font-style:normal;color:#C8232C}
.sub{position:absolute;left:72px;font-size:34px;line-height:1.35;font-weight:600}
.sub b{font-weight:700;color:#C8232C}
.chip{position:absolute;background:#FFF6E0;border-radius:999px;padding:12px 24px;font-size:24px;font-weight:700;box-shadow:0 6px 0 #3A2316;white-space:nowrap}
.card{position:absolute;background:#FFF6E0;border-radius:28px;box-shadow:0 12px 0 #3A2316;padding:30px 34px}
.spark{position:absolute;width:28px;height:28px;background:#FFF6E0;clip-path:polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%)}
.disc{position:absolute;border-radius:50%}
/* Appel à l'action : l'image n'est pas cliquable, on donne l'adresse exacte du site */
.cta{position:absolute;left:72px;right:72px;bottom:64px}
.cta .lbl{font-family:"Bowlby One",sans-serif;font-size:30px;text-transform:uppercase;margin-bottom:12px;letter-spacing:.01em}
.cta .bar{display:flex;align-items:center;gap:16px;background:#FFF6E0;border:4px solid #3A2316;border-radius:999px;padding:12px 12px 12px 30px;box-shadow:0 10px 0 #3A2316}
.cta .bar svg{flex:none}
.cta .url{flex:1;font-size:38px;font-weight:700;letter-spacing:.01em}
.cta .go{background:#C8232C;color:#FFF6E0;border-radius:999px;padding:16px 30px;font-family:"Bowlby One",sans-serif;font-size:24px;text-transform:uppercase;white-space:nowrap}
.cta .pay{margin-top:18px;font-size:24px;font-weight:700}
/* Sac de courses */
.bag{position:absolute}
.bag .back{position:absolute;left:4%;right:4%;border-radius:10px 10px 0 0;background:linear-gradient(#A8763E,#B9864C)}
.bag .handle{position:absolute;z-index:4;pointer-events:none}
.bag .item{position:absolute;filter:drop-shadow(0 10px 10px rgba(58,35,22,.3));z-index:2}
.bag .front{position:absolute;left:0;bottom:0;z-index:3;filter:drop-shadow(0 26px 26px rgba(58,35,22,.35))}
"""

LOCK = ('<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#3A2316" stroke-width="2.4">'
        '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>')


def cta(label="Faites vos courses sur notre site"):
    return f"""<div class="cta"><div class="lbl">{label}</div>
<div class="bar">{LOCK}<span class="url">{SITE_URL}</span><span class="go">Commander</span></div>
<div class="pay">✓ Paiement à la livraison &nbsp; ✓ Espèces ou mobile money</div></div>"""


def top(badge):
    return f'<div class="top"><div class="logo">Timaini<small>Les courses</small></div><div class="badge">{badge}</div></div>'


def bag(left, top_, w, items):
    """Sac kraft avec des produits qui dépassent.
    items : (fichier, x en % de la largeur, profondeur en % de la hauteur du sac, hauteur en px, rotation)"""
    hf = round(w * 0.62)            # hauteur de la face avant
    over = round(w * 0.95)          # place au-dessus du sac pour les produits
    H = hf + over
    imgs = "".join(
        f'<img class="item" src="assets/{f}.webp" style="left:{x}%;bottom:{round(hf * d / 100)}px;'
        f'height:{h}px;transform:translateX(-50%) rotate({r}deg);z-index:{2 + i % 2}">'
        for i, (f, x, d, h, r) in enumerate(items))
    front = f"""<svg class="front" width="{w}" height="{hf}" viewBox="0 0 100 62" preserveAspectRatio="none">
<defs><linearGradient id="k" x1="0" x2="1"><stop offset="0" stop-color="#C08A4E"/><stop offset=".55" stop-color="#D3A267"/><stop offset="1" stop-color="#B57F45"/></linearGradient></defs>
<path d="M2 4 L98 4 L100 62 L0 62 Z" fill="url(#k)"/>
<path d="M2 4 L98 4 L98.3 10 L1.7 10 Z" fill="#E2B67C"/>
<path d="M1.7 10 L98.3 10" stroke="#9C6A35" stroke-width=".5"/>
<path d="M30 62 L33 10 M70 62 L67 10" stroke="#A9773F" stroke-width=".35" opacity=".6"/></svg>
<div style="position:absolute;z-index:4;left:0;right:0;bottom:{round(hf * .22)}px;text-align:center;font-family:'Bowlby One',sans-serif;color:#7A1418;opacity:.82;line-height:.85;text-transform:uppercase">
<div style="font-size:{round(w * .13)}px">Timaini</div><div style="font-size:{round(w * .05)}px;letter-spacing:.2em;color:#3A2316">Les courses</div></div>"""
    handle = (f'<svg class="handle" width="{w}" height="{round(w * .5)}" style="left:0;bottom:{hf - round(w * .02)}px" viewBox="0 0 100 50">'
              '<path d="M22 50 C22 8 46 8 46 50" stroke="#7A4F24" stroke-width="3.4" stroke-linecap="round" fill="none"/>'
              '<path d="M54 50 C54 8 78 8 78 50" stroke="#7A4F24" stroke-width="3.4" stroke-linecap="round" fill="none"/></svg>')
    back = f'<div class="back" style="bottom:0;height:{hf + round(w * .03)}px"></div>'
    return f'<div class="bag" style="left:{left}px;top:{top_}px;width:{w}px;height:{H}px">{back}{handle}{imgs}{front}</div>'


def page(title, body):
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{title}</title>'
            f'<link rel="stylesheet" href="../../site/fonts/fonts.css"><style>{CSS}</style></head>'
            f'<body><div class="rays"></div><div class="grain"></div>{body}</body></html>')


C = {}

# 1. RÉSULTAT RÊVÉ : ce que le client veut vraiment (le frigo plein), pas « une livraison »
C["1-le-frigo-plein"] = (
    top("Yaoundé · 7 j/7")
    + '<h1 style="font-size:104px;width:940px">Le frigo plein,<br><em>sans sortir<br>de chez vous.</em></h1>'
    + '<p class="sub" style="top:560px;width:430px">Vous choisissez vos produits sur le site. <b>On vous apporte tout à la porte.</b></p>'
    + '<span class="chip" style="left:72px;top:800px;transform:rotate(-3deg)">🛒 Plus de 100 produits</span>'
    + '<span class="disc" style="left:560px;top:560px;width:460px;height:460px;background:#C8232C"></span>'
    + bag(560, 380, 450, [("tangui-1-5l", 18, 45, 390, -9), ("azur-huile-1l", 83, 45, 380, 8),
                          ("nido-boite-2-5kg", 52, 55, 320, 0), ("malta-canette", 30, 30, 260, -5),
                          ("heinz-ketchup-907g", 72, 30, 260, 6)])
    + '<span class="spark" style="left:520px;top:520px"></span><span class="spark" style="left:1000px;top:600px;width:18px;height:18px"></span>'
    + cta())

# 2. PROBABILITÉ PERÇUE / INVERSION DU RISQUE : le client ne prend aucun risque
C["2-payez-a-la-reception"] = (
    top("Zéro risque")
    + '<h1 style="font-size:100px;width:940px">Vous payez<br><em>seulement à<br>la réception.</em></h1>'
    + '<div class="card" style="left:72px;top:540px;width:520px;padding:26px 30px">'
      '<div style="font-size:23px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#C8232C">Comment ça se passe</div>'
      '<div style="font-size:28px;font-weight:700;line-height:1.5;margin-top:10px">'
      '1. Vous commandez sur le site<br>2. Le livreur sonne chez vous<br>3. Vous vérifiez chaque article<br>4. Vous payez. Pas avant.</div></div>'
    + '<p class="sub" style="top:915px;width:500px;font-size:28px">Rien à payer en avance.<br>Ni carte, ni virement.</p>'
    + '<span class="disc" style="left:600px;top:560px;width:430px;height:430px;background:#3A2316;opacity:.92"></span>'
    + bag(610, 410, 410, [("milo-boite-1-5kg", 22, 40, 290, -7), ("sirop-fraise", 52, 45, 380, 2),
                          ("nutella-pot", 82, 38, 250, 7), ("indomie-oignon-poulet", 40, 28, 220, -4)])
    + cta())

# 3. LA STACK D'OFFRE : tout ce qui est inclus, au prix affiché (aucune remise inventée)
C["3-tout-inclus"] = (
    top("L'offre")
    + '<h1 style="font-size:96px;width:940px">Vos courses,<br><em>tout compris.</em></h1>'
    + '<div class="card" style="left:72px;top:470px;width:600px">'
      + "".join(f'<div style="display:flex;gap:16px;align-items:flex-start;margin:{"0" if i == 0 else "20px"} 0 0">'
                f'<span style="flex:none;width:44px;height:44px;border-radius:50%;background:#C8232C;color:#FFF6E0;display:grid;place-items:center;font-size:26px;font-weight:700">✓</span>'
                f'<div><div style="font-size:30px;font-weight:700;line-height:1.15">{t}</div><div style="font-size:23px;font-weight:600;opacity:.8;margin-top:4px">{d}</div></div></div>'
                for i, (t, d) in enumerate([
                    ("Livraison à votre porte", "Offerte dès 10 000 FCFA d'achat"),
                    ("Paiement à la réception", "Aucune avance, aucune carte"),
                    ("Vous vérifiez avant de payer", "Vous ne payez que ce qui est livré"),
                    ("Rien à porter", "Pas de taxi, pas de file, pas de packs sur la tête"),
                ]))
      + '<div style="margin-top:24px;padding-top:18px;border-top:3px dashed #3A2316;font-size:26px;font-weight:700">'
        'Le prix ? <span style="color:#C8232C">Celui affiché sur le site.</span> Rien de plus.</div></div>'
    + bag(700, 560, 330, [("jus-orange-1l", 22, 45, 290, -9), ("tangui-1-5l", 80, 45, 300, 8),
                          ("coca-pack6-1-5l", 52, 35, 250, -2)])
    + cta())

# 4. EFFORT SUPPRIMÉ : la douleur concrète (porter l'eau, le riz, l'huile)
C["4-on-porte-pour-vous"] = (
    top("Pour la maison")
    + '<h1 style="font-size:96px;width:960px">Les packs<br>lourds ?<br><em>On les porte<br>pour vous.</em></h1>'
    + '<p class="sub" style="top:690px;width:470px">Eau 10 L, riz 5 kg, huile, lait : commandez depuis votre téléphone, <b>on pose tout devant votre porte.</b></p>'
    + '<span class="chip" style="left:72px;top:960px;transform:rotate(-2deg)">💪 Vous ne portez rien</span>'
    + '<span class="disc" style="left:580px;top:560px;width:450px;height:450px;background:#C8232C"></span>'
    + bag(580, 390, 440, [("supermont-10l", 28, 42, 400, -7), ("taj-mahal-xxxl-5kg", 74, 40, 350, 7),
                          ("azur-huile-5l", 52, 30, 290, -2)])
    + cta())

if __name__ == "__main__":
    for nom, html in C.items():
        (OUT / f"{nom}.html").write_text(page(nom, html), encoding="utf-8")
        print("écrit", nom)
