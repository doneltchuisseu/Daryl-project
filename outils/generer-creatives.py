import pathlib
OUT = pathlib.Path("livrables/creatives")

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:"Quicksand",system-ui,sans-serif;color:#3A2316;position:relative;
  background:radial-gradient(120% 90% at 78% 30%,#FFD65A 0%,#F7B731 45%,#E9A23B 100%)}
.rays{position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 80% 35%,rgba(255,255,255,.14) 0 6deg,transparent 6deg 18deg);pointer-events:none}
.grain{position:absolute;inset:0;background-image:radial-gradient(rgba(58,35,22,.06) 1px,transparent 1px);background-size:4px 4px;pointer-events:none}
.top{position:absolute;left:80px;top:72px;right:80px;display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:26px;letter-spacing:.02em}
.logo{font-family:"Bowlby One",sans-serif;font-size:34px;line-height:.9;color:#C8232C;text-transform:uppercase}
.logo small{display:block;font-size:.42em;color:#3A2316;letter-spacing:.12em}
.badge{background:#3A2316;color:#FFF6E0;border-radius:999px;padding:12px 26px;font-size:24px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
h1{position:absolute;left:80px;top:250px;width:920px;font-family:"Bowlby One",sans-serif;font-size:116px;line-height:.98;text-transform:uppercase;color:#3A2316;text-shadow:0 6px 0 #FFF6E0}
h1 em{font-style:normal;color:#C8232C;display:block}
.sub{position:absolute;left:80px;top:600px;width:480px;font-size:37px;line-height:1.35;font-weight:600;color:#3A2316}
.cta{position:absolute;left:80px;bottom:150px;display:inline-flex;align-items:center;gap:18px;background:#C8232C;color:#FFF6E0;border-radius:999px;padding:26px 46px;font-family:"Bowlby One",sans-serif;font-size:34px;text-transform:uppercase;box-shadow:0 10px 0 #3A2316}
.cta.dark{background:#3A2316;color:#FFF6E0;box-shadow:0 10px 0 #C8232C}
.note{position:absolute;left:80px;bottom:72px;font-size:24px;font-weight:700;opacity:.85}
.prod{position:absolute;filter:drop-shadow(0 22px 22px rgba(58,35,22,.32))}
.disc{position:absolute;border-radius:50%}
.sticker{position:absolute;width:250px;transform:rotate(12deg);filter:drop-shadow(0 10px 14px rgba(58,35,22,.3))}
.spark{position:absolute;width:26px;height:26px;background:#FFF6E0;clip-path:polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%)}
.card{position:absolute;background:#FFF6E0;border-radius:28px;box-shadow:0 14px 0 #3A2316;padding:30px 36px;font-weight:700}
"""

def page(title, body, css=""):
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="../../site/fonts/fonts.css"><style>{BASE_CSS}{css}</style></head>
<body><div class="rays"></div><div class="grain"></div>{body}</body></html>"""

def top(badge="Vos courses"):
    return f"""<div class="top"><div class="logo">Timaini<small>Les courses</small></div><div class="badge">{badge}</div></div>"""

def prod(src, x, y, w, rot=0, z=2):
    return f'<img class="prod" src="assets/{src}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);z-index:{z}">'

creatives = {}

# 1 — Promesse : « vos courses chez vous » (le client garde le sticker)
creatives["1-vos-courses-chez-vous"] = (
    top("Yaoundé · 7 j/7") +
    """<h1>Vos courses,<em>chez vous.</em></h1>
    <p class="sub">Les produits du quotidien, dans un seul panier. On vous les apporte à la porte.</p>
    <div class="disc" style="left:610px;top:620px;width:400px;height:400px;background:#C8232C;opacity:.95"></div>
    <div class="disc" style="left:880px;top:840px;width:220px;height:220px;background:#3A2316;opacity:.9"></div>"""
    + prod("nido-boite-2-5kg.webp", 660, 610, 300, -6, 3)
    + prod("tangui-1-5l.webp", 660, 800, 170, 4, 2)
    + prod("azur-huile-1l.webp", 800, 760, 170, -5, 2)
    + prod("indomie-oignon-poulet.webp", 700, 930, 170, 3, 3)
    + prod("heinz-ketchup-907g.webp", 880, 930, 150, -4, 2)
    + """<span class="spark" style="left:520px;top:520px"></span><span class="spark" style="left:980px;top:560px;width:18px;height:18px"></span>"""
    + """<div class="cta">Faire mes courses →</div><div class="note">Paiement à la livraison · Sur notre site</div>"""
)

# 2 — Réassurance : payer à la livraison (levée du risque)
creatives["2-payez-a-la-livraison"] = (
    top("Sans risque") +
    """<h1>Payez quand<em>vous recevez.</em></h1>
    <p class="sub">Vérifiez vos courses avant de payer le livreur. Espèces ou mobile money.</p>
    <div class="card" style="left:80px;top:745px;width:560px">
      <div style="font-size:26px;letter-spacing:.06em;text-transform:uppercase;color:#C8232C">Comment ça marche</div>
      <div style="font-size:36px;margin-top:12px;line-height:1.3">1. Vous commandez<br>2. On livre chez vous<br>3. Vous payez à la main</div>
    </div>"""
    + prod("evian-pack6-1l.webp", 720, 640, 280, 4, 2)
    + prod("malta-canette.webp", 900, 760, 160, -5, 3)
    + """<div class="disc" style="left:700px;top:880px;width:340px;height:340px;background:#C8232C;opacity:.9;z-index:1"></div>"""
    + """<div class="cta dark">Commander sur notre site →</div><div class="note">Livraison à Yaoundé · Espèces ou mobile money</div>"""
)

# 3 — Valeur : livraison offerte + packs
creatives["3-livraison-offerte-packs"] = (
    top("Bon plan") +
    """<h1>Livraison<em>offerte</em>dès 10 000 F</h1>
    <p class="sub">Packs, eau, jus et sodas : on livre tout.</p>
    <div class="card" style="left:80px;top:800px;width:430px;transform:rotate(-3deg)">
      <div style="font-size:24px;color:#C8232C;text-transform:uppercase">Pack famille</div>
      <div style="font-size:44px;line-height:1.1;margin-top:8px">Sprite, 9 × 1,5 L</div>
      <div style="font-size:52px;color:#C8232C;margin-top:12px">10 000 F</div>
    </div>"""
    + prod("sprite-pack9.webp", 560, 640, 330, 3, 2)
    + prod("jus-orange-pack3.webp", 820, 720, 260, -3, 3)
    + prod("fanta-pack24.webp", 620, 930, 340, -2, 1)
    + """<div class="cta">Remplir mon panier →</div><div class="note">Livraison gratuite dès 10 000 FCFA · Sur notre site</div>"""
)

# 4 — Douleur : fini de porter l'eau et les packs
creatives["4-fini-de-porter"] = (
    top("Pour la maison") +
    """<h1>Fini de porter<em>l’eau.</em></h1>
    <p class="sub">Eau, jus, riz, lait, huile : commandez, on vous pose tout devant la porte.</p>"""
    + prod("supermont-10l.webp", 720, 560, 230, -6, 3)
    + prod("taj-mahal-xxxl-5kg.webp", 860, 700, 200, 5, 2)
    + prod("nido-boite-2-5kg.webp", 760, 900, 210, 3, 2)
    + prod("milo-boite-1-5kg.webp", 900, 930, 170, -3, 3)
    + """<div class="cta">Commander maintenant →</div><div class="note">Paiement à la livraison · Sur notre site</div>"""
)

for name, html in creatives.items():
    (OUT / f"{name}.html").write_text(page(name, html), encoding="utf-8")
    print("écrit", name)
