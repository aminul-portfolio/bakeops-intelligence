// static/js/navbar.js
document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector(".site-header");
  const navCollapse = document.getElementById("navbarMain");
  const body = document.body;

  // add / remove shadow when scrolling
  function handleScroll() {
    if (!header) return;
    if (window.scrollY > 8) {
      header.classList.add("is-scrolled");
    } else {
      header.classList.remove("is-scrolled");
    }
  }

  window.addEventListener("scroll", handleScroll, { passive: true });
  handleScroll(); // run once on load

  // when mobile menu opens/closes, toggle dimmed background
  if (navCollapse) {
    navCollapse.addEventListener("shown.bs.collapse", () => {
      body.classList.add("nav-open");
    });
    navCollapse.addEventListener("hidden.bs.collapse", () => {
      body.classList.remove("nav-open");
    });
  }
});
