// SweetCakes storefront navbar interactions

document.addEventListener("DOMContentLoaded", () => {

  const header = document.querySelector(".sc-site-header");

  const navCollapse = document.getElementById("mainNavbar");

  const body = document.body;



  function handleScroll() {

    if (!header) return;

    header.classList.toggle("is-scrolled", window.scrollY > 8);

  }



  window.addEventListener("scroll", handleScroll, { passive: true });

  handleScroll();



  if (navCollapse) {

    navCollapse.addEventListener("shown.bs.collapse", () => {

      body.classList.add("nav-open");

    });

    navCollapse.addEventListener("hidden.bs.collapse", () => {

      body.classList.remove("nav-open");

    });



    navCollapse.querySelectorAll(".sc-nav__link, .sc-btn--nav, .sc-btn--nav-secondary").forEach((link) => {

      link.addEventListener("click", () => {

        if (window.innerWidth < 992 && navCollapse.classList.contains("show")) {

          const toggle = document.querySelector(".sc-navbar__toggle");

          if (toggle && window.bootstrap?.Collapse) {

            window.bootstrap.Collapse.getOrCreateInstance(navCollapse).hide();

          } else if (toggle) {

            toggle.click();

          }

        }

      });

    });

  }

});


