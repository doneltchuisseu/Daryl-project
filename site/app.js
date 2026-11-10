"use strict";
/* Timaini Les Courses · boutique (site statique, sans serveur).
   Les produits viennent de data/produits.js, généré par outils/generer-site.py. */

/* ===== Réglages boutique ===== */
const WHATSAPP = "";          // numéro de la boutique au format international, ex. "2376XXXXXXXX". Vide = mode démo.
const LIVRAISON_OFFERTE = 10000;
const FRAIS_LIVRAISON = 500;
const FUSEAU = "Africa/Douala";

const PRODUITS = window.PRODUITS || [];
const FAMILLES = window.FAMILLES || [];
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const fcfa = n => n.toLocaleString("fr-FR").replace(/ | /g, " ") + " FCFA";
const slug = s => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const norm = s => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const parId = id => PRODUITS.find(p => p.id === id);
const famDe = s => FAMILLES.find(f => slug(f) === s);

/* ===== Heure de livraison estimée (heure de Yaoundé) ===== */
function eta() {
  const d = new Date(Date.now() + 60 * 60 * 1000);
  d.setMinutes(Math.ceil(d.getMinutes() / 5) * 5);
  const [h, m] = new Intl.DateTimeFormat("fr-FR", { timeZone: FUSEAU, hour: "2-digit", minute: "2-digit", hour12: false })
    .format(d).split(":");
  return `${+h} h ${m}`;
}
function majEta() { $$("[data-eta]").forEach(e => (e.textContent = eta())); }

/* ===== Textes ===== */
const DESCRIPTIONS = {
  "Eaux": "Une eau de qualité pour toute la famille, livrée bien emballée à votre porte.",
  "Sodas": "Le soda qu’on ne présente plus, à servir bien frais pour les repas, les matchs et les fêtes.",
  "Jus et nectars": "Plein de fruits pour le petit-déjeuner ou le goûter des enfants.",
  "Thés glacés": "Un thé glacé désaltérant, parfait quand il fait chaud à Yaoundé.",
  "Sirops": "À allonger d’eau bien fraîche : une bouteille donne des dizaines de verres pour toute la famille.",
  "Boissons maltées": "La boisson maltée sans alcool préférée du Cameroun, pleine d’énergie.",
  "Petit-déjeuner": "Pour bien commencer la journée : boisson chocolatée, céréales et pâte à tartiner que toute la famille réclame.",
  "Confitures et douceurs": "Confitures, compotée et galettes pur beurre Bonne Maman pour les tartines, le goûter et les desserts.",
  "Sauces": "Ketchup et mayonnaise Heinz pour les frites, les sandwichs et les grillades.",
  "Nouilles": "Les nouilles instantanées Indomie, prêtes en 3 minutes : en sachet ou en gobelet.",
  "Riz": "Du riz basmati Taj Mahal en sachet de 1 kg ou en grand sac pour toute la famille.",
  "Pâtes": "Spaghetti, tagliatelle, rotini et autres pâtes Barilla pour les repas de dernière minute.",
  "Laits": "Le lait longue conservation Candia, nature, vitaminé, sans lactose ou parfumé, prêt à boire.",
  "Thés et infusions": "Le Lipton du quotidien, les thés anglais Twinings et des infusions, à boire chaud ou glacé.",
  "Bébé et enfants": "Laits de croissance pour les 1 à 3 ans. Demandez conseil à votre pédiatre pour choisir le lait adapté à votre enfant.",
  "Cafés": "Café soluble prêt en quelques secondes, ou café en grains Lavazza pour les amateurs d’espresso.",
};
const titreFamille = f => ({ "Eaux": "Les eaux", "Sodas": "Les sodas", "Jus et nectars": "Les jus", "Thés glacés": "Les thés glacés", "Sirops": "Les sirops", "Boissons maltées": "Les boissons maltées", "Cafés": "Les cafés", "Petit-déjeuner": "Le petit-déjeuner", "Bébé et enfants": "Bébé et enfants", "Thés et infusions": "Thés et infusions", "Laits": "Les laits", "Confitures et douceurs": "Confitures et douceurs", "Pâtes": "Les pâtes", "Riz": "Le riz", "Nouilles": "Les nouilles", "Sauces": "Les sauces" }[f] || f);
const BIENTOT = ["Épicerie", "Hygiène et beauté", "Entretien", "Délestage", "Anti-moustiques"];

/* ===== Composants ===== */
function carte(p, i = 0) {
  const tag = p.etiquette ? `<span class="tag ${esc(p.etiquette.split(" ")[0])}">${esc(p.etiquette)}</span>` : "";
  return `<article class="card">
    <div class="card__img">${tag}<img src="${p.image}" alt="" loading="${i < 4 ? "eager" : "lazy"}" width="300" height="300"></div>
    <div class="card__meta">
      <div><a class="card__link" href="#/produit/${p.id}"><b>${esc(p.nom)}</b></a><small>${esc(p.marque)} · ${esc(p.format)}</small><span class="price">${fcfa(p.prix)}</span></div>
      <button class="plus" data-add="${p.id}" aria-label="Ajouter ${esc(p.nom)} au panier">+</button>
    </div>
    <span class="explore" aria-hidden="true"><i></i>Voir</span>
  </article>`;
}
const grille = (liste, cls = "") => `<div class="grid ${cls}">${liste.map(carte).join("")}</div>`;
function section(titre, sousTitre, liste, lien, libelle, cls = "") {
  if (!liste.length) return "";
  return `<section class="sec"><div class="wrap">
    <div class="sec-head"><div><h2 class="h2">${titre}</h2><p>${sousTitre}</p></div>${lien ? `<a class="pill" href="${lien}">${libelle}</a>` : ""}</div>
    ${grille(liste, cls)}
  </div></section>`;
}

/* ===== Pages ===== */
function pageAccueil() {
  const img = id => parId(id)?.image || "";
  const favOrdre = ["malta-canette", "tangui-1-5l", "supermont-10l", "nutella-pot"];
  const favoris = favOrdre.map(parId).filter(Boolean);
  const promos = PRODUITS.filter(p => p.etiquette === "Promo");
  const nouveautes = PRODUITS.filter(p => ["Nouveau", "Édition limitée"].includes(p.etiquette));
  const fams = FAMILLES.map(f => {
    const liste = PRODUITS.filter(p => p.famille === f);
    const vitrine = liste.find(p => !p.pack) || liste[0];
    return `<a class="fam" href="#/produits/${slug(f)}"><span class="ico"><img src="${vitrine.image}" alt=""></span><b>${esc(f)}</b><span>${liste.length} produit${liste.length > 1 ? "s" : ""}</span></a>`;
  }).join("");

  return `
  <section class="hero">
    <span class="kernel" style="left:12%;top:110px;width:58px;height:58px;background:var(--orange)"></span>
    <span class="kernel" style="right:13%;top:96px;width:42px;height:42px;background:var(--bleu)"></span>
    <h1><span class="scrib l"></span>Vos courses<br>livrées <u>en 1 h</u><span class="scrib r"></span></h1>
    <p>Boissons fraîches et produits du quotidien, livrés partout à Yaoundé.</p>
    <div class="ctas"><a class="pill dark" href="#/produits">Faire mes courses</a><a class="pill" href="#/produits/promos">Voir les promos</a></div>
    <div class="stage" aria-hidden="true">
      <span class="disc d1"></span><span class="disc d3"></span><span class="disc d2"></span>
      <img class="bottle b1" src="${img("sirop-pomme")}" alt="">
      <img class="bottle b3" src="${img("sirop-peche")}" alt="">
      <img class="bottle b2" src="${img("sirop-fraise")}" alt="">
    </div>
  </section>

  ${section("Les favoris d’ici", "Les incontournables du Cameroun, toujours en stock.", favoris, "#/produits", "Tous les produits")}

  <section class="sec"><div class="wrap">
    <div class="sec-head"><div><h2 class="h2">Nos rayons</h2><p>Boissons, café, petit-déjeuner… et le reste de la supérette arrive bientôt.</p></div><a class="pill" href="#/produits">Tout voir</a></div>
    <div class="fams">${fams}</div>
    <div class="soon"><b>Bientôt&nbsp;:</b>${BIENTOT.map(b => `<span>${b}</span>`).join("")}</div>
  </div></section>

  ${section("Les promos", "Les packs et plateaux au meilleur prix.", promos.slice(0, 8), "#/produits/promos", "Toutes les promos")}

  <section class="banner"><div class="wrap">
    <div>
      <div class="eyebrow">Livré frais</div>
      <h2><span class="scrib" style="position:relative;display:inline-block;filter:invert(1)"></span> Soif&nbsp;?<br>On arrive.</h2>
      <p>Eau, sodas, jus et Malta livrés en moins d’une heure. Pour la maison, le bureau ou la fête de ce soir.</p>
      <a class="pill red" href="#/produits">Commander maintenant</a>
    </div>
    <div class="pics" aria-hidden="true"><img src="${img("malta-verre")}" alt=""><img src="${img("tangui-1-5l")}" alt=""><img src="${img("the-glace-tropical")}" alt=""></div>
  </div></section>

  ${section("Les nouveautés", "Les derniers arrivés dans nos rayons.", nouveautes.slice(0, 4), "#/produits", "Tous les produits")}

  <section class="steps" id="etapes">
    <div class="step"><span class="n">1</span><h3>Je remplis mon panier</h3><p>Sur le site, à toute heure.</p></div>
    <div class="step"><span class="n">2</span><h3>On prépare</h3><p>Votre commande est emballée en 15 minutes dans notre supérette.</p></div>
    <div class="step"><span class="n">3</span><h3>Livré en 1 h</h3><p>Un livreur à moto vous l’apporte. Vous payez à la livraison ou par mobile money.</p></div>
  </section>
  <section class="values">
    <div><b>Livré en 1 h</b><span>Partout à Yaoundé, 7 j/7</span></div>
    <div><b>Paiement facile</b><span>Orange Money, MTN MoMo, espèces</span></div>
    <div><b>Prix justes</b><span>Les prix de votre quartier</span></div>
    <div><b>Un souci&nbsp;?</b><span>On répond sur WhatsApp</span></div>
  </section>`;
}

function pageCatalogue(filtre, recherche = "") {
  let liste = PRODUITS, titre = "Nos produits", sous = "Boissons, cafés, petit-déjeuner… tout le quotidien, livré en 1 h.";
  const fam = filtre && filtre !== "promos" ? famDe(filtre) : null;
  if (filtre === "promos") { liste = liste.filter(p => p.etiquette === "Promo"); titre = "Les promos"; sous = "Les packs et plateaux au meilleur prix."; }
  else if (fam) { liste = liste.filter(p => p.famille === fam); titre = titreFamille(fam); sous = DESCRIPTIONS[fam] || ""; }
  if (recherche) {
    const mots = norm(recherche).split(/\s+/).filter(Boolean);
    liste = PRODUITS.filter(p => { const t = norm(`${p.nom} ${p.marque} ${p.format} ${p.famille}`); return mots.every(m => t.includes(m)); });
    titre = `« ${esc(recherche)} »`; sous = `${liste.length} résultat${liste.length > 1 ? "s" : ""}`;
  }
  const tri = sessionStorage.getItem("tri") || "pertinence";
  const tries = { "prix-asc": (a, b) => a.prix - b.prix, "prix-desc": (a, b) => b.prix - a.prix, "nom": (a, b) => a.nom.localeCompare(b.nom, "fr") };
  if (tries[tri]) liste = [...liste].sort(tries[tri]);

  const chip = (href, label, n, actif) => `<a class="chip" href="${href}" aria-current="${actif}">${label}<small>${n}</small></a>`;
  const chips = recherche ? "" : [
    chip("#/produits", "Tout", PRODUITS.length, !filtre),
    chip("#/produits/promos", "Promos", PRODUITS.filter(p => p.etiquette === "Promo").length, filtre === "promos"),
    ...FAMILLES.map(f => chip(`#/produits/${slug(f)}`, f, PRODUITS.filter(p => p.famille === f).length, fam === f)),
  ].join("");

  return `<div class="wrap page-head">
    <nav class="crumbs"><a href="#/">Accueil</a> › ${recherche ? "Recherche" : fam || filtre === "promos" ? `<a href="#/produits">Nos produits</a> › ${titre}` : "Nos produits"}</nav>
    <h1 class="h2">${titre}</h1><p style="margin-top:8px;opacity:.8">${sous}</p>
    <div class="filters">
      <div class="chips">${chips}</div>
      <label class="sort">Trier&nbsp;:<select id="tri">
        <option value="pertinence">Pertinence</option><option value="prix-asc">Prix croissant</option>
        <option value="prix-desc">Prix décroissant</option><option value="nom">Nom</option></select></label>
    </div>
    ${liste.length ? grille(liste) : `<div class="empty"><b>Aucun produit trouvé</b><p>Essayez un autre mot, ou parcourez tous les produits.</p><a class="pill dark" href="#/produits">Tous les produits</a></div>`}
  </div>`;
}

function pageProduit(id) {
  const p = parId(id);
  if (!p) return `<div class="wrap empty"><b>Produit introuvable</b><a class="pill dark" href="#/produits">Voir les produits</a></div>`;
  const similaires = PRODUITS.filter(x => x.famille === p.famille && x.id !== p.id).slice(0, 4);
  const nb = (p.format.match(/^(\d+)\s/) || [])[1];
  const unite = p.pack && nb ? `Soit ${fcfa(Math.round(p.prix / +nb))} l’unité` : "";
  const tag = p.etiquette ? `<span class="tag ${esc(p.etiquette.split(" ")[0])}">${esc(p.etiquette)}</span>` : "";
  const faits = [["Marque", p.marque], ["Format", p.format], ["Rayon", p.famille]];
  if (p.verre) faits.push(["Verre", "Consigne en plus"]);

  return `<div class="wrap page-head">
    <nav class="crumbs"><a href="#/">Accueil</a> › <a href="#/produits">Nos produits</a> › <a href="#/produits/${slug(p.famille)}">${esc(p.famille)}</a> › ${esc(p.nom)}</nav>
    <div class="product">
      <div class="product__vis">${tag}<span class="scrib s1"></span><span class="scrib s2"></span><span class="scrib s3"></span><span class="scrib s4"></span>
        <img src="${p.image}" alt="${esc(p.nom)}"></div>
      <div class="product__info">
        <div class="product__brand">${esc(p.marque)}</div>
        <h1>${esc(p.nom)}</h1>
        <div class="product__price">${fcfa(p.prix)}</div>
        <div class="product__unit">${esc(p.format)}${unite ? " · " + unite : ""}</div>
        <p class="product__desc">${DESCRIPTIONS[p.famille] || ""}</p>
        <div class="buy">
          <div class="stepper"><button data-step="-1" aria-label="Moins">−</button><output id="qte">1</output><button data-step="1" aria-label="Plus">+</button></div>
          <button class="pill dark" id="ajouter">Ajouter au panier</button>
        </div>
        <div class="eta"><i></i><span>Commandé maintenant, livré vers <b data-eta></b></span></div>
        <div class="facts"><h2>Infos pratiques</h2><ul>${faits.map(([k, v]) => `<li><span>${k}</span><b>${esc(v)}</b></li>`).join("")}</ul></div>
      </div>
    </div>
  </div>
  ${section("Dans le même rayon", "Vous aimerez aussi.", similaires, `#/produits/${slug(p.famille)}`, "Tout le rayon")}`;
}

/* ===== Routeur ===== */
function route() {
  const [, page = "", arg = ""] = location.hash.split("/");
  const app = $("#app");
  let html, titre = "Timaini Les Courses · Vos courses livrées en 1 h à Yaoundé";
  if (page === "produit") { html = pageProduit(arg); const p = parId(arg); if (p) titre = `${p.nom} · Timaini Les Courses`; }
  else if (page === "produits" || page === "boissons") { html = pageCatalogue(arg); titre = "Nos produits · Timaini Les Courses"; }
  else if (page === "recherche") { const q = decodeURIComponent(arg); html = pageCatalogue("", q); $("#q").value = q; titre = `Recherche « ${q} » · Timaini Les Courses`; }
  else html = pageAccueil();
  app.innerHTML = html + `<div style="height:80px"></div>`;
  document.title = titre;
  majEta();

  const tri = $("#tri");
  if (tri) { tri.value = sessionStorage.getItem("tri") || "pertinence"; tri.onchange = () => { sessionStorage.setItem("tri", tri.value); route(); }; }
  const qte = $("#qte");
  if (qte) {
    $$("[data-step]").forEach(b => (b.onclick = () => { qte.value = qte.textContent = Math.min(20, Math.max(1, +qte.textContent + +b.dataset.step)); }));
    $("#ajouter").onclick = () => { ajouter(arg, +qte.textContent); };
  }
  if (!sessionStorage.getItem("scroll-to")) window.scrollTo({ top: 0, behavior: "instant" });
  const cible = sessionStorage.getItem("scroll-to");
  if (cible) { sessionStorage.removeItem("scroll-to"); $("#" + cible)?.scrollIntoView({ behavior: "smooth" }); }
  $(".nav").classList.remove("open");
}
addEventListener("hashchange", route);

/* ===== Panier ===== */
let panier = {};
try { panier = JSON.parse(localStorage.getItem("panier") || "{}"); } catch { panier = {}; }
const enregistrer = () => { try { localStorage.setItem("panier", JSON.stringify(panier)); } catch {} rendrePanier(); };
function ajouter(id, n = 1) {
  const p = parId(id); if (!p) return;
  panier[id] = Math.min(99, (panier[id] || 0) + n);
  if (panier[id] <= 0) delete panier[id];
  enregistrer();
  if (n > 0) toast(`${n} × ${p.nom} ajouté${n > 1 ? "s" : ""} au panier`);
}
function totaux() {
  const lignes = Object.entries(panier).filter(([id]) => parId(id));
  const nb = lignes.reduce((s, [, q]) => s + q, 0);
  const sous = lignes.reduce((s, [id, q]) => s + parId(id).prix * q, 0);
  const frais = sous === 0 || sous >= LIVRAISON_OFFERTE ? 0 : FRAIS_LIVRAISON;
  return { lignes, nb, sous, frais, total: sous + frais };
}
function rendrePanier() {
  const { lignes, nb, sous, frais, total } = totaux();
  $$("[data-count]").forEach(b => { b.textContent = nb; b.dataset.zero = nb === 0; });
  $("#sub-total").textContent = fcfa(sous);
  $("#ship-fee").textContent = sous === 0 ? "—" : frais ? fcfa(frais) : "Offerte";
  $("#total").textContent = fcfa(total);
  $("#checkout").disabled = nb === 0;
  const reste = LIVRAISON_OFFERTE - sous;
  $("#ship-msg").innerHTML = reste > 0 ? `Plus que <b>${fcfa(reste)}</b> pour la livraison gratuite` : "🎉 Livraison offerte !";
  $("#ship-bar").style.width = Math.min(100, (sous / LIVRAISON_OFFERTE) * 100) + "%";
  $("#cart-items").innerHTML = lignes.length ? lignes.map(([id, q]) => {
    const p = parId(id);
    return `<li class="line"><a class="pic" href="#/produit/${id}"><img src="${p.image}" alt=""></a>
      <div><b>${esc(p.nom)}</b><small>${esc(p.format)} · ${fcfa(p.prix)}</small><br>
        <span class="qty"><button data-d="-1" data-id="${id}" aria-label="Retirer un">−</button><span>${q}</span><button data-d="1" data-id="${id}" aria-label="Ajouter un">+</button></span></div>
      <span class="tot">${fcfa(p.prix * q)}</span></li>`;
  }).join("") : `<li class="drawer__empty"><b>Votre panier est vide</b><span>Ajoutez vos produits préférés.</span><a class="pill dark" href="#/produits" data-close>Faire mes courses</a></li>`;
}
$("#cart-items").addEventListener("click", e => {
  const b = e.target.closest("button[data-d]");
  if (b) ajouter(b.dataset.id, +b.dataset.d);
  if (e.target.closest("[data-close], a.pic")) fermerPanier();
});
document.addEventListener("click", e => {
  const b = e.target.closest("[data-add]");
  if (b) { e.preventDefault(); ajouter(b.dataset.add); }
  const s = e.target.closest("[data-scroll]");
  if (s) { e.preventDefault(); const id = s.dataset.scroll; if (!location.hash || location.hash === "#/" || !$("#" + id)) { sessionStorage.setItem("scroll-to", id); if (location.hash && location.hash !== "#/") location.hash = "#/"; else route(); } else $("#" + id).scrollIntoView({ behavior: "smooth" }); }
});

const tiroir = $("#drawer"), voile = $("#overlay");
function ouvrirPanier() { tiroir.classList.add("open"); tiroir.setAttribute("aria-hidden", "false"); voile.hidden = false; $("#close-cart").focus(); }
function fermerPanier() { tiroir.classList.remove("open"); tiroir.setAttribute("aria-hidden", "true"); voile.hidden = true; }
$$("[data-open-cart]").forEach(b => (b.onclick = ouvrirPanier));
$("#close-cart").onclick = fermerPanier;
voile.onclick = fermerPanier;
addEventListener("keydown", e => { if (e.key === "Escape") fermerPanier(); });

/* ===== Commande ===== */
const dlg = $("#order");
$("#checkout").onclick = () => { $("#order-total").textContent = fcfa(totaux().total); majEta(); fermerPanier(); dlg.showModal(); };
$("#order-form").addEventListener("submit", e => {
  if (e.submitter?.value !== "ok") return;
  const f = new FormData(e.target);
  const { lignes, sous, frais, total } = totaux();
  const message = [
    "Bonjour Timaini Les Courses, voici ma commande :", "",
    ...lignes.map(([id, q]) => `• ${q} × ${parId(id).nom} (${parId(id).format}) : ${fcfa(parId(id).prix * q)}`), "",
    `Sous-total : ${fcfa(sous)}`, `Livraison : ${frais ? fcfa(frais) : "offerte"}`, `TOTAL : ${fcfa(total)}`, "",
    `Nom : ${f.get("nom")}`, `Téléphone : ${f.get("tel")}`, `Adresse : ${f.get("adresse")} (${$("#quartier").value})`,
    `Livraison : ${f.get("quand")}`, `Paiement : ${f.get("paiement")}`,
  ].join("\n");
  if (WHATSAPP) {
    window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(message)}`, "_blank", "noopener");
    panier = {}; enregistrer();
  } else {
    e.preventDefault();
    e.target.innerHTML = `<div class="done"><b>Commande prête&nbsp;!</b>
      <p>Site de démonstration : le numéro WhatsApp de la boutique n’est pas encore configuré. Voici le message qui sera envoyé :</p>
      <pre>${esc(message)}</pre><button class="pill dark block" value="cancel">Fermer</button></div>`;
  }
});
dlg.addEventListener("close", () => { if (!$("#order-form .modal__body")) location.reload(); });

/* ===== Recherche, menu, divers ===== */
$("#search").addEventListener("submit", e => { e.preventDefault(); const q = $("#q").value.trim(); location.hash = q ? `#/recherche/${encodeURIComponent(q)}` : "#/produits"; });
$("#burger").onclick = e => { const o = $(".nav").classList.toggle("open"); e.currentTarget.setAttribute("aria-expanded", o); };
let minuteur;
function toast(msg) { const t = $("#toast"); t.textContent = msg; t.classList.add("show"); clearTimeout(minuteur); minuteur = setTimeout(() => t.classList.remove("show"), 2400); }
$("#foot-familles").innerHTML = FAMILLES.map(f => `<li><a href="#/produits/${slug(f)}">${esc(f)}</a></li>`).join("");
$("#year").textContent = new Date().getFullYear();
setInterval(majEta, 60000);

rendrePanier();
route();
