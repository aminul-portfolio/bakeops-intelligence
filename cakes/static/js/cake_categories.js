document.addEventListener("DOMContentLoaded", function () {
  const categoryCards = Array.from(
    document.querySelectorAll(".cake-type-card[data-category]")
  );
  const cakeGrid = document.querySelector(".cake-grid");
  const cakeCards = cakeGrid
    ? Array.from(
        cakeGrid.querySelectorAll(".portfolio-card, .cake-card")
      )
    : [];

  if (!categoryCards.length || !cakeCards.length) return;

  let emptyStateEl = null;

  // --- Helpers --------------------------------------------------

  function createEmptyState() {
    if (emptyStateEl || !cakeGrid) return;
    emptyStateEl = document.createElement("div");
    emptyStateEl.className = "cake-empty-state text-muted small mt-2";
    emptyStateEl.style.fontStyle = "italic";
    emptyStateEl.textContent =
      "No cakes in this category yet. Try another style above.";
    cakeGrid.parentNode.insertBefore(emptyStateEl, cakeGrid.nextSibling);
  }

  function showEmptyState() {
    if (!emptyStateEl) createEmptyState();
    if (emptyStateEl) emptyStateEl.style.display = "block";
  }

  function hideEmptyState() {
    if (emptyStateEl) emptyStateEl.style.display = "none";
  }

  function filterCakes(category) {
    let visibleCount = 0;

    cakeCards.forEach((cake) => {
      const cakeCategory = cake.dataset.category;
      const matches =
        !category || category === "all" || cakeCategory === category;

      cake.style.display = matches ? "" : "none";
      if (matches) visibleCount++;
    });

    if (visibleCount === 0) {
      showEmptyState();
    } else {
      hideEmptyState();
    }
  }

  function handleCategorySelection(card) {
    const clickedCategory = card.dataset.category || "all";
    const isAlreadyActive = card.classList.contains("is-active");

    // Clear all active states
    categoryCards.forEach((c) => c.classList.remove("is-active"));

    // If it was already active, reset to ALL
    const newCategory = isAlreadyActive ? "all" : clickedCategory;

    // Only mark as active if we're actually filtering to that category
    if (!isAlreadyActive && newCategory !== "all") {
      card.classList.add("is-active");
    }

    filterCakes(newCategory);
  }

  // --- Set up cards ---------------------------------------------

  categoryCards.forEach((card) => {
    // Make them accessible as buttons
    card.setAttribute("role", "button");
    card.setAttribute("tabindex", "0");

    card.addEventListener("click", () => {
      handleCategorySelection(card);
    });

    card.addEventListener("keydown", (evt) => {
      if (evt.key === "Enter" || evt.key === " ") {
        evt.preventDefault();
        handleCategorySelection(card);
      }
    });
  });

  // --- Initial state: show ALL cakes ----------------------------

  filterCakes("all");
  hideEmptyState();
});
