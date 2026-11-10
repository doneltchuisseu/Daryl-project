"use strict";

/* ===== Données produits (à remplacer par les vôtres) ===== */
const PRODUCTS = [
  {
    id: "sriracha", name: "Sriracha Citron vert", price: 2.99, color: "#e63a37", tag: "Sriracha · Citron vert",
    desc: "Découvrez notre pop-corn Sriracha Citron vert, un mélange délicieux de saveurs pimentées et acidulées qui fera monter votre pause snack d’un cran !",
    nutri: [["Énergie", "66 kcal", 3], ["Matières grasses", "3,0 g", 4], ["Sucres", "0,2 g", 1], ["Sel", "0,01 g", 1]],
  },
  {
    id: "caramel", name: "Caramel Sel", price: 2.99, color: "#f08a24", tag: "Caramel · Sel",
    desc: "Le grand classique, revisité : un caramel fondant relevé d’une pointe de fleur de sel. Sucré, salé, impossible de s’arrêter.",
    nutri: [["Énergie", "78 kcal", 4], ["Matières grasses", "2,6 g", 4], ["Sucres", "4,1 g", 5], ["Sel", "0,12 g", 2]],
  },
  {
    id: "truffe", name: "Truffe Parmesan Citron", price: 2.99, color: "#2540d8", tag: "Truffe · Parmesan",
    desc: "Une recette de chef : parfum de truffe, parmesan affiné et zeste de citron pour un pop-corn aussi chic que gourmand.",
    nutri: [["Énergie", "70 kcal", 3], ["Matières grasses", "3,4 g", 5], ["Sucres", "0,3 g", 1], ["Sel", "0,09 g", 2]],
  },
];
const FREE_SHIPPING = 25;
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const eur = n => n.toFixed(2).replace(".", ",") + " €";
const find = id => PRODUCTS.find(p => p.id === id);

/* ===== Sachet de pop-corn en SVG ===== */
function bagSVG(p) {
  const c = p.color;
  const scallops = Array.from({ length: 9 }, (_, i) =>
    `<circle cx="${28 + i * 18}" cy="262" r="10" fill="#f6ecdc"/>`).join("");
  return `
<svg viewBox="0 0 200 290" role="img" aria-label="Sachet ${p.name}" xmlns="http://www.w3.org/2000/svg">
  <path d="M14 14h172l6 14-4 236a14 14 0 0 1-14 14H26a14 14 0 0 1-14-14L8 28z" fill="${c}"/>
  <path d="M8 28h184v22H8z" fill="#000" opacity=".12"/>
  <path d="M8 28h184" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>
  <g fill="#f6ecdc" font-family="Bowlby One,Arial Black,sans-serif" text-anchor="middle">
    <text x="78" y="108" font-size="46">POP</text>
    <text x="164" y="84" font-size="15">POP</text>
    <text x="100" y="152" font-size="46">POP</text>
  </g>
  <rect x="26" y="168" width="148" height="20" rx="3" fill="#f6ecdc" opacity=".92"/>
  <text x="100" y="182" text-anchor="middle" font-family="Quicksand,sans-serif" font-weight="700" font-size="9" fill="${c}">${p.tag.toUpperCase()}</text>
  <text x="100" y="208" text-anchor="middle" font-family="Quicksand,sans-serif" font-weight="700" font-size="7" fill="#f6ecdc">GOURMET · FABRIQUÉ EN FRANCE</text>
  ${scallops}
  <path d="M12 250h176v30H12z" fill="#f6ecdc" opacity="0"/>
</svg>`;
}

/* ===== Hero : sachets ===== */
$$("[data-bag]").forEach(el => (el.innerHTML = bagSVG(find(el.dataset.bag))));

/* ===== Grille "Rencontrez la bande" ===== */
$("#grid").innerHTML = PRODUCTS.map(p => `
  <a class="card" href="#produit/${p.id}" data-id="${p.id}">
    <div class="card__img">${bagSVG(p)}</div>
    <div class="card__meta"><b>${p.name}</b><span>${eur(p.price)}</span></div>
    <span class="card__cta"><i></i>Voir</span>
  </a>`).join("");

/* ===== Fiche produit (routage par hash) ===== */
const fiche = $("#fiche");
let current = null;

function showProduct(id) {
  const p = find(id);
  if (!p) return hideProduct();
  current = p;
  $("#p-bag").innerHTML = bagSVG(p);
  $("#p-name").textContent = p.name;
  $("#p-price").textContent = eur(p.price);
  $("#p-desc").textContent = p.desc;
  $("#qty").value = 1;
  $("#p-nutri").innerHTML = p.nutri.map(([label, val, pct]) =>
    `<li><div class="l"><small>${label}</small><b>${val}</b></div><div class="r">${pct}%</div></li>`).join("");
  fiche.hidden = false;
  fiche.scrollIntoView({ behavior: "smooth" });
  document.title = `${p.name} – Pop Pop`;
}
function hideProduct() {
  fiche.hidden = true; current = null; document.title = "Pop Pop – Pop-corn gourmet";
}
function route() {
  const m = location.hash.match(/^#produit\/(.+)$/);
  m ? showProduct(m[1]) : hideProduct();
}
addEventListener("hashchange", route);
$("#back").addEventListener("click", () => { history.pushState(null, "", "#produits"); route(); $("#produits").scrollIntoView({ behavior: "smooth" }); });

$("#buy").addEventListener("submit", e => {
  e.preventDefault();
  const qty = Math.max(1, Math.min(20, parseInt($("#qty").value, 10) || 1));
  add(current.id, qty);
  toast(`${qty} × ${current.name} ajouté${qty > 1 ? "s" : ""} au panier`);
  openCart();
});

/* ===== Panier ===== */
let cart = {};
try { cart = JSON.parse(localStorage.getItem("cart") || "{}"); } catch { cart = {}; }
const save = () => { try { localStorage.setItem("cart", JSON.stringify(cart)); } catch {} render(); };
function add(id, n = 1) {
  cart[id] = Math.min(99, (cart[id] || 0) + n);
  if (cart[id] <= 0) delete cart[id];
  save();
}

function render() {
  const entries = Object.entries(cart).filter(([id]) => find(id));
  const count = entries.reduce((s, [, q]) => s + q, 0);
  const total = entries.reduce((s, [id, q]) => s + find(id).price * q, 0);

  $$("[data-cart-count]").forEach(b => { b.textContent = count; b.dataset.zero = count === 0; });
  $("#cart-total").textContent = eur(total);
  $("#checkout").disabled = count === 0;

  const left = FREE_SHIPPING - total;
  $("#ship-msg").textContent = left > 0
    ? `Plus que ${eur(left)} pour la livraison offerte`
    : "🎉 Livraison offerte !";
  $("#ship-bar").style.width = Math.min(100, (total / FREE_SHIPPING) * 100) + "%";

  $("#cart-items").innerHTML = entries.length ? entries.map(([id, q]) => {
    const p = find(id);
    return `<li class="line">
      <div class="line__img">${bagSVG(p)}</div>
      <div><b>${p.name}</b><span>${eur(p.price)}</span>
        <div class="qty"><button data-d="-1" data-id="${id}" aria-label="Moins">−</button><span>${q}</span><button data-d="1" data-id="${id}" aria-label="Plus">+</button></div>
      </div>
      <b>${eur(p.price * q)}</b>
    </li>`;
  }).join("") : `<li class="empty">Votre panier est vide 🍿</li>`;
}
$("#cart-items").addEventListener("click", e => {
  const b = e.target.closest("button[data-d]");
  if (b) add(b.dataset.id, +b.dataset.d);
});

const drawer = $("#drawer"), overlay = $("#overlay");
function openCart() { drawer.classList.add("is-open"); drawer.setAttribute("aria-hidden", "false"); overlay.hidden = false; }
function closeCart() { drawer.classList.remove("is-open"); drawer.setAttribute("aria-hidden", "true"); overlay.hidden = true; }
$$("[data-open-cart]").forEach(b => b.addEventListener("click", openCart));
$("#close-cart").addEventListener("click", closeCart);
overlay.addEventListener("click", closeCart);
addEventListener("keydown", e => e.key === "Escape" && closeCart());
$("#checkout").addEventListener("click", () => toast("Paiement à brancher (Stripe, Shopify, PayPal…)"));

/* ===== Divers ===== */
const nav = $(".nav");
$("#burger").addEventListener("click", e => {
  const open = nav.classList.toggle("is-open");
  e.currentTarget.setAttribute("aria-expanded", open);
});
let t;
function toast(msg) {
  const el = $("#toast"); el.textContent = msg; el.classList.add("show");
  clearTimeout(t); t = setTimeout(() => el.classList.remove("show"), 2400);
}
$("#year").textContent = new Date().getFullYear();

render();
route();
