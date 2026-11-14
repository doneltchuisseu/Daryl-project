"""Génère les 4 créatives de campagne TIMAINI LES COURSES (1080 x 1350, images fixes).

Usage : python3 outils/generer-creatives.py   puis   node outils/rendre-creatives.js

L'offre (validée par le client), identique sur les 4 créatives :
« Vos courses livrées chez vous. Vous payez à la réception. »
Leviers d'Alex Hormozi utilisés :
  1. Résultat rêvé        : « Le frigo plein, sans sortir de chez vous »
  2. Garantie / risque nul : « Pas satisfait ? Vous ne payez pas »
  3. L'offre empilée       : « Vous commandez. On s'occupe du reste » (liste de ce qui est inclus)
  4. Effort et temps gagnés : « Gardez votre samedi. On fait les courses »
Règles : image fixe (pas de bouton ni d'adresse web), pas de promesse de délai,
livraison offerte dès 25 000 FCFA.
"""
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
OUT = RACINE / "livrables/creatives"

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:"Quicksand",system-ui,sans-serif;color:#3A2316;position:relative;
  background:radial-gradient(120% 90% at 75% 45%,#FFD65A 0%,#F7B731 48%,#E9A23B 100%)}
.rays{position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 74% 58%,rgba(255,255,255,.13) 0 6deg,transparent 6deg 18deg)}
.grain{position:absolute;inset:0;background-image:radial-gradient(rgba(58,35,22,.06) 1px,transparent 1px);background-size:4px 4px}
.top{position:absolute;left:72px;top:64px;right:72px;display:flex;justify-content:space-between;align-items:center}
.logo{font-family:"Bowlby One",sans-serif;font-size:36px;line-height:.88;color:#C8232C;text-transform:uppercase}
.logo small{display:block;font-size:.42em;color:#3A2316;letter-spacing:.14em}
.badge{background:#3A2316;color:#FFF6E0;border-radius:999px;padding:12px 26px;font-size:23px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
h1{position:absolute;left:72px;top:150px;font-family:"Bowlby One",sans-serif;line-height:.98;text-transform:uppercase;color:#3A2316;text-shadow:0 6px 0 #FFF6E0}
h1 em{font-style:normal;color:#C8232C}
.sub{position:absolute;left:72px;font-size:33px;line-height:1.35;font-weight:600}
.sub b{font-weight:700;color:#C8232C}
.chip{position:absolute;background:#FFF6E0;border-radius:999px;padding:12px 24px;font-size:24px;font-weight:700;box-shadow:0 6px 0 #3A2316;white-space:nowrap}
.card{position:absolute;background:#FFF6E0;border-radius:28px;box-shadow:0 12px 0 #3A2316;padding:28px 32px}
.card .t{font-size:23px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#C8232C}
.spark{position:absolute;width:28px;height:28px;background:#FFF6E0;clip-path:polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%)}
.disc{position:absolute;border-radius:50%}
.acc{position:relative;display:inline-block}
.acc::after{content:"";position:absolute;left:30%;top:-.02em;width:.34em;height:.11em;background:currentColor;border-radius:.05em;transform:rotate(-24deg);box-shadow:0 .06em 0 #FFF6E0}
.offre{position:absolute;left:72px;right:72px;top:508px;background:#3A2316;border-radius:26px;padding:22px 30px;text-align:center;box-shadow:0 10px 0 #C8232C;font-family:"Bowlby One",sans-serif;font-size:50px;line-height:1;color:#FFD65A;text-transform:uppercase}
/* Bandeau du bas : image fixe, donc pas de bouton ni d'adresse */
.foot{position:absolute;left:0;right:0;bottom:0;height:190px;background:#3A2316;display:flex;align-items:center;justify-content:space-between;padding:0 72px;gap:28px}
.foot .site{font-family:"Bowlby One",sans-serif;color:#FFF6E0;font-size:34px;line-height:1.08;text-transform:uppercase;white-space:nowrap}
.foot .pay{flex:none;background:#C8232C;color:#FFF6E0;border-radius:22px;padding:18px 28px;text-align:center;transform:rotate(-2deg);box-shadow:0 8px 0 #F7B731}
.foot .pay b{display:block;font-family:"Bowlby One",sans-serif;font-weight:400;font-size:31px;line-height:1;text-transform:uppercase}
.foot .pay span{display:block;font-size:21px;font-weight:700;margin-top:6px}
/* Groupe de produits posés (sans sac) */
.groupe{position:absolute}
.groupe img{position:absolute;filter:drop-shadow(0 14px 14px rgba(58,35,22,.32))}
.groupe .ombre{position:absolute;left:6%;right:6%;bottom:-14px;height:40px;border-radius:50%;background:radial-gradient(rgba(58,35,22,.35),transparent 70%)}
/* Sac de courses */
.bag{position:absolute}
.bag .back{position:absolute;left:4%;right:4%;border-radius:10px 10px 0 0;background:linear-gradient(#A8763E,#B9864C)}
.bag .handle{position:absolute;z-index:1}
.bag .item{position:absolute;filter:drop-shadow(0 10px 10px rgba(58,35,22,.3));z-index:2}
.bag .front{position:absolute;left:0;bottom:0;z-index:5;filter:drop-shadow(0 26px 26px rgba(58,35,22,.35))}
"""


def foot():
    return ('<div class="foot"><div class="site">Faites vos courses<br>sur notre site</div>'
            '<div class="pay"><b>Livraison à Yaoundé</b><span>Espèces ou mobile money</span></div></div>')


def offre():
    """L'offre, identique sur les 4 créatives."""
    return ('<h1 style="font-size:96px;line-height:1.2;width:940px">Vos courses<br><em>livr<span class="acc">e</span>es<br>chez vous.</em></h1>'
            '<div class="offre">Vous payez à la réception</div>')


def top(badge):
    return f'<div class="top"><div class="logo">Timaini<small>Les courses</small></div><div class="badge">{badge}</div></div>'


def groupe(left, top_, w, h, items):
    """Produits posés et serrés. items : (fichier, centre x en %, bas en px, hauteur en px, rotation, plan)"""
    imgs = "".join(f'<img src="assets/{f}.webp" style="left:{x}%;bottom:{b}px;height:{hh}px;'
                   f'transform:translateX(-50%) rotate({r}deg);z-index:{z}">' for f, x, b, hh, r, z in items)
    return f'<div class="groupe" style="left:{left}px;top:{top_}px;width:{w}px;height:{h}px"><span class="ombre"></span>{imgs}</div>'


def bag(left, top_, w, items):
    """Sac kraft : anses derrière les produits, produits qui dépassent largement."""
    hf = round(w * 0.62)
    over = round(w * 0.95)
    imgs = "".join(
        f'<img class="item" src="assets/{f}.webp" style="left:{x}%;bottom:{round(hf * d / 100)}px;'
        f'height:{h}px;transform:translateX(-50%) rotate({r}deg);z-index:{2 + i % 2}">'
        for i, (f, x, d, h, r) in enumerate(items))
    front = f"""<svg class="front" width="{w}" height="{hf}" viewBox="0 0 100 62" preserveAspectRatio="none">
<defs><linearGradient id="k" x1="0" x2="1"><stop offset="0" stop-color="#C08A4E"/><stop offset=".55" stop-color="#D3A267"/><stop offset="1" stop-color="#B57F45"/></linearGradient></defs>
<path d="M2 4 L98 4 L100 62 L0 62 Z" fill="url(#k)"/><path d="M2 4 L98 4 L98.3 10 L1.7 10 Z" fill="#E2B67C"/>
<path d="M1.7 10 L98.3 10" stroke="#9C6A35" stroke-width=".5"/>
<path d="M30 62 L33 10 M70 62 L67 10" stroke="#A9773F" stroke-width=".35" opacity=".6"/></svg>
<div style="position:absolute;z-index:6;left:0;right:0;bottom:{round(hf * .22)}px;text-align:center;font-family:'Bowlby One',sans-serif;color:#7A1418;opacity:.82;line-height:.85;text-transform:uppercase">
<div style="font-size:{round(w * .13)}px">Timaini</div><div style="font-size:{round(w * .05)}px;letter-spacing:.2em;color:#3A2316">Les courses</div></div>"""
    handle = (f'<svg class="handle" width="{w}" height="{round(w * .62)}" style="left:0;bottom:{hf - round(w * .02)}px" viewBox="0 0 100 62">'
              '<path d="M18 62 C18 4 46 4 46 62" stroke="#7A4F24" stroke-width="3.4" stroke-linecap="round" fill="none"/>'
              '<path d="M54 62 C54 4 82 4 82 62" stroke="#7A4F24" stroke-width="3.4" stroke-linecap="round" fill="none"/></svg>')
    back = f'<div class="back" style="bottom:0;height:{hf + round(w * .03)}px"></div>'
    return f'<div class="bag" style="left:{left}px;top:{top_}px;width:{w}px;height:{hf + over}px">{back}{handle}{imgs}{front}</div>'


def etapes(lignes):
    return "".join(f'<div style="display:flex;gap:14px;align-items:center;margin-top:{14 if i else 12}px">'
                   f'<span style="flex:none;width:44px;height:44px;border-radius:50%;background:#3A2316;color:#FFF6E0;display:grid;place-items:center;font-family:Bowlby One,sans-serif;font-size:22px">{i + 1}</span>'
                   f'<span style="font-size:28px;font-weight:700;line-height:1.2">{t}</span></div>'
                   for i, t in enumerate(lignes))


def coches(lignes):
    return "".join(f'<div style="display:flex;gap:16px;align-items:flex-start;margin-top:{0 if i == 0 else 30}px">'
                   f'<span style="flex:none;width:46px;height:46px;border-radius:50%;background:#C8232C;color:#FFF6E0;display:grid;place-items:center;font-size:26px;font-weight:700">✓</span>'
                   f'<div><div style="font-size:31px;font-weight:700;line-height:1.15;white-space:nowrap">{t}</div>'
                   f'<div style="font-size:25px;font-weight:600;opacity:.8;margin-top:6px">{d}</div></div></div>'
                   for i, (t, d) in enumerate(lignes))


def page(title, body):
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{title}</title>'
            f'<link rel="stylesheet" href="../../site/fonts/fonts.css"><style>{CSS}</style></head>'
            f'<body><div class="rays"></div><div class="grain"></div>{body}</body></html>')


C = {}

# 1. Les produits du quotidien, apportés à la porte
C["offre-1-produits"] = (
    top("Yaoundé · 7 j/7") + offre()
    + '<p class="sub" style="top:660px;width:450px">Vous choisissez vos produits sur notre site. <b>On vous apporte tout à la porte.</b></p>'
    + '<span class="chip" style="left:72px;top:930px;transform:rotate(-3deg)">🛒 Plus de 100 produits</span>'
    + '<span class="disc" style="left:590px;top:680px;width:420px;height:420px;background:#C8232C"></span>'
    + groupe(560, 640, 470, 500, [
        ("tangui-1-5l", 16, 120, 330, -8, 1), ("azur-huile-1l", 84, 120, 320, 8, 1),
        ("sirop-fraise", 34, 140, 270, -3, 1), ("jus-orange-1l", 66, 140, 270, 4, 1),
        ("nido-boite-2-5kg", 50, 30, 270, 0, 3),
        ("malta-canette", 20, 0, 200, -6, 4), ("heinz-ketchup-907g", 80, 0, 210, 6, 4)])
    + foot())

# 2. Comment ça se passe, en 4 étapes
C["offre-2-etapes"] = (
    top("Comment ça marche") + offre()
    + '<div class="card" style="left:72px;top:660px;width:560px"><div class="t">Comment ça se passe</div>'
    + etapes(["Vous commandez sur notre site", "On fait vos courses pour vous", "On vous livre chez vous",
              "Vous payez à la réception"]) + '</div>'
    + '<span class="disc" style="left:660px;top:700px;width:380px;height:380px;background:#3A2316;opacity:.92"></span>'
    + groupe(645, 660, 400, 460, [
        ("sirop-peche", 25, 110, 280, -7, 1), ("milo-boite-1-5kg", 72, 100, 250, 6, 1),
        ("nutella-pot", 34, 0, 220, -4, 3), ("indomie-oignon-poulet", 74, 0, 190, 5, 3)])
    + foot())

# 3. Ce qui est inclus
C["offre-3-inclus"] = (
    top("L'offre") + offre()
    + '<div class="card" style="left:72px;top:650px;width:640px;padding:32px 34px">'
    + coches([("On fait vos courses", "Plus besoin d’aller au marché"),
              ("On vous livre chez vous", "Livraison offerte dès 25 000 FCFA"),
              ("Vous vérifiez à la livraison", "Puis vous payez, pas avant"),
              ("Espèces ou mobile money", "Vous choisissez à la réception")])
    + '</div>'
    + bag(745, 630, 290, [("jus-orange-1l", 22, 45, 260, -9), ("tangui-1-5l", 80, 45, 270, 8),
                          ("coca-pack6-1-5l", 52, 35, 225, -2)])
    + foot())

# 4. Les produits lourds : on porte, vous restez chez vous
C["offre-4-on-porte"] = (
    top("Gagnez du temps") + offre()
    + '<p class="sub" style="top:660px;width:450px">Pas de marché, pas d’embouteillages, rien à porter. <b>On achète tout et on vous livre.</b></p>'
    + '<span class="chip" style="left:72px;top:930px;transform:rotate(-2deg)">💪 Vous ne portez rien</span>'
    + '<span class="disc" style="left:600px;top:680px;width:420px;height:420px;background:#C8232C"></span>'
    + groupe(560, 620, 480, 520, [
        ("supermont-10l", 22, 120, 340, -7, 1), ("taj-mahal-xxxl-5kg", 78, 120, 320, 7, 1),
        ("azur-huile-5l", 50, 90, 270, 0, 2),
        ("nido-boite-2-5kg", 26, 0, 220, -4, 3), ("milo-boite-1-5kg", 74, 0, 210, 5, 3)])
    + foot())

if __name__ == "__main__":
    for nom, html in C.items():
        (OUT / f"{nom}.html").write_text(page(nom, html), encoding="utf-8")
        print("écrit", nom)
