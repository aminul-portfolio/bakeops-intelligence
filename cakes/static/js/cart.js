// SweetCakes demo cart (localStorage only — no server orders)



document.addEventListener("DOMContentLoaded", () => {

  const STORAGE_KEY = "cakeCart";



  let memoryCart = {

    items: [],

    totalQty: 0,

    totalAmount: 0,

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

      totalAmount: 0,

    };

  }



  function getCart() {

    try {

      const raw = window.localStorage.getItem(STORAGE_KEY);

      if (!raw) return memoryCart || getEmptyCart();



      const parsed = safeParse(raw, getEmptyCart());

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

      console.warn("Could not save cart to localStorage, keeping in memory.", e);

    }



    document.dispatchEvent(new CustomEvent("cart:updated", { detail: { cart } }));

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

    badge.style.display = qty > 0 ? "inline-flex" : "none";

  }



  function showAddedFeedback(btn) {

    const originalText = btn.getAttribute("data-original-text") || btn.textContent;

    btn.setAttribute("data-original-text", originalText);



    const addedLabel = btn.getAttribute("data-added-label") || "Added to demo cart";

    btn.disabled = true;

    btn.classList.add("sc-btn--added");

    btn.textContent = addedLabel;



    window.setTimeout(() => {

      btn.disabled = false;

      btn.textContent = originalText;

      btn.classList.remove("sc-btn--added");

    }, 1200);

  }



  function addToCart({ id, name, price }) {

    const cart = getCart();

    const key = id || name || "Cake";

    const existing = cart.items.find((it) => it.key === key);



    if (existing) {

      existing.qty += 1;

      existing.name = name || existing.name;

      existing.price = price || existing.price;

    } else {

      cart.items.push({

        key,

        id: id || null,

        name: name || "Cake",

        price: price || 0,

        qty: 1,

      });

    }



    recalcTotals(cart);

    saveCart(cart);

    updateCartBadge();

  }



  function bindAddToCartButtons() {

    document.querySelectorAll("[data-add-to-cart='true']").forEach((btn) => {

      btn.addEventListener("click", (event) => {

        event.preventDefault();

        if (btn.disabled) return;



        const name = (btn.getAttribute("data-product-name") || "Cake").trim();

        const price = parseFloat(btn.getAttribute("data-product-price") || "0");

        const id = (btn.getAttribute("data-product-id") || name).trim();



        addToCart({ id, name, price });

        showAddedFeedback(btn);

      });

    });

  }



  const variantSelect = document.getElementById("cake-variant-select");

  const detailBtn = document.getElementById("detail-add-to-cart");



  if (variantSelect && detailBtn) {
    const syncVariant = () => {
      const option = variantSelect.options[variantSelect.selectedIndex];
      const price = option.getAttribute("data-price") || "0";
      const baseName = detailBtn.getAttribute("data-product-base-name") || "Cake";
      const variantLabel = option.textContent.split("—")[0].trim();
      detailBtn.setAttribute("data-product-price", price);
      detailBtn.setAttribute("data-product-name", `${baseName} (${variantLabel})`);
      detailBtn.setAttribute(
        "data-product-id",
        `${detailBtn.getAttribute("data-product-slug")}-${option.value}`
      );
    };

    variantSelect.addEventListener("change", syncVariant);
    syncVariant();
  }

  bindAddToCartButtons();
  updateCartBadge();

  document.addEventListener("cart:updated", () => {
    updateCartBadge();
  });
});
