// static/js/cart.js

document.addEventListener("DOMContentLoaded", () => {
  // -----------------------------
  // CART HELPERS
  // -----------------------------

  const STORAGE_KEY = "cakeCart";

  // In-memory fallback if localStorage is not available
  let memoryCart = {
    items: [],
    totalQty: 0,
    totalAmount: 0
  };

  function safeParse(json, fallback) {
    try {
      return JSON.parse(json);
    } catch (e) {
      console.warn("Failed to parse cart JSON, resetting cart.", e);
      return fallback;
    }
  }

  function getEmptyCart() {
    return {
      items: [],
      totalQty: 0,
      totalAmount: 0
    };
  }

  function getCart() {
    // Try localStorage first
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) return memoryCart || getEmptyCart();

      const parsed = safeParse(raw, getEmptyCart());

      // Ensure required fields exist
      if (typeof parsed.totalQty !== "number") parsed.totalQty = 0;
      if (typeof parsed.totalAmount !== "number") parsed.totalAmount = 0;
      if (!Array.isArray(parsed.items)) parsed.items = [];

      memoryCart = parsed;
      return parsed;
    } catch (e) {
      console.error("Error reading cart from localStorage, using memoryCart.", e);
      return memoryCart || getEmptyCart();
    }
  }

  function saveCart(cart) {
    memoryCart = cart;
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
    } catch (e) {
      // If storage fails (Safari private mode, quota, etc.), we just keep memoryCart
      console.warn("Could not save cart to localStorage, keeping in memory.", e);
    }

    // Let other scripts listen for cart updates
    document.dispatchEvent(
      new CustomEvent("cart:updated", { detail: { cart } })
    );
  }

  function recalcTotals(cart) {
    let totalQty = 0;
    let totalAmount = 0;

    cart.items.forEach((item) => {
      totalQty += item.qty;
      totalAmount += item.qty * (item.price || 0);
    });

    cart.totalQty = totalQty;
    cart.totalAmount = Number(totalAmount.toFixed(2));
  }

  function updateCartBadge() {
    const cart = getCart();
    const badge = document.getElementById("cart-total");
    if (!badge) return;

    const qty = cart.totalQty || 0;
    badge.textContent = qty;

    // Optional: hide badge if 0
    badge.style.display = qty > 0 ? "inline-block" : "none";
  }

  function addToCart({ id, name, price }) {
    const cart = getCart();

    // Prefer an ID if given, fallback to name
    const key = id || name || "Cake";

    const existing = cart.items.find((it) => it.key === key);

    if (existing) {
      existing.qty += 1;
    } else {
      cart.items.push({
        key: key,
        id: id || null,
        name: name || "Cake",
        price: price || 0,
        qty: 1
      });
    }

    recalcTotals(cart);
    saveCart(cart);
    updateCartBadge();
  }

  // -----------------------------
  // BUTTON HANDLERS
  // -----------------------------

  const buttons = document.querySelectorAll("[data-add-to-cart='true']");

  buttons.forEach((btn) => {
    btn.addEventListener("click", (event) => {
      event.preventDefault();

      if (btn.disabled) return; // prevent spam clicking during feedback state

      const nameAttr  = btn.getAttribute("data-product-name");
      const priceAttr = btn.getAttribute("data-product-price");
      const idAttr    = btn.getAttribute("data-product-id");

      const name  = nameAttr && nameAttr.trim() ? nameAttr.trim() : "Cake";
      const price = priceAttr ? parseFloat(priceAttr) : 0;
      const id    = idAttr && idAttr.trim() ? idAttr.trim() : null;

      addToCart({ id, name, price });

      // ---- Visual feedback ----
      const originalText = btn.getAttribute("data-original-text") || btn.textContent;
      btn.setAttribute("data-original-text", originalText);

      const addedLabel =
        btn.getAttribute("data-added-label") || "Added!";

      btn.disabled = true;
      btn.classList.add("btn-success");
      btn.classList.remove("btn-outline-success");
      btn.textContent = addedLabel;

      setTimeout(() => {
        btn.disabled = false;
        btn.textContent = originalText;
        btn.classList.remove("btn-success");
        btn.classList.add("btn-outline-success");
      }, 1200);
    });
  });

  // -----------------------------
  // INIT ON PAGE LOAD
  // -----------------------------

  updateCartBadge();

  // In case some other script modifies cart directly and saves, keep badge synced
  document.addEventListener("cart:updated", () => {
    updateCartBadge();
  });
});
