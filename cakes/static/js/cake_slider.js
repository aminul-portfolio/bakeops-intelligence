// static/js/cake_slider.js
document.addEventListener("DOMContentLoaded", () => {
  const slider  = document.getElementById("cakeSlider");
  if (!slider) return;

  const track   = slider.querySelector(".slider-track");
  const slides  = slider.querySelectorAll(".slider-item");
  const prevBtn = slider.querySelector(".slider-prev");
  const nextBtn = slider.querySelector(".slider-next");

  // If we don't have enough elements, bail out gracefully
  if (!track || slides.length === 0 || !prevBtn || !nextBtn) return;

  let currentIndex   = 0;
  let isAnimating    = false;
  let autoplayTimer  = null;

  const AUTOPLAY_DELAY   = 6000;  // ms
  const SWIPE_THRESHOLD  = 40;    // px

  // --- Core movement -------------------------------------------------

  function goTo(index) {
    if (isAnimating) return;

    const total = slides.length;
    const newIndex = (index + total) % total; // wrap around

    if (newIndex === currentIndex) return;

    isAnimating = true;
    currentIndex = newIndex;

    const offset = -currentIndex * 100;
    track.style.willChange = "transform";
    track.style.transition = "transform 0.5s ease";
    track.style.transform  = `translateX(${offset}%)`;

    // Unlock after animation
    setTimeout(() => {
      isAnimating = false;
    }, 500);
  }

  function goNext() {
    goTo(currentIndex + 1);
  }

  function goPrev() {
    goTo(currentIndex - 1);
  }

  // --- Autoplay ------------------------------------------------------

  function startAutoplay() {
    if (autoplayTimer !== null) return;
    autoplayTimer = setInterval(goNext, AUTOPLAY_DELAY);
  }

  function stopAutoplay() {
    if (autoplayTimer === null) return;
    clearInterval(autoplayTimer);
    autoplayTimer = null;
  }

  // --- Buttons -------------------------------------------------------

  nextBtn.addEventListener("click", (e) => {
    e.preventDefault();
    stopAutoplay();
    goNext();
    startAutoplay();
  });

  prevBtn.addEventListener("click", (e) => {
    e.preventDefault();
    stopAutoplay();
    goPrev();
    startAutoplay();
  });

  // --- Hover & focus pause -------------------------------------------

  slider.addEventListener("mouseenter", stopAutoplay);
  slider.addEventListener("mouseleave", startAutoplay);

  slider.addEventListener("focusin", stopAutoplay);
  slider.addEventListener("focusout", startAutoplay);

  // --- Keyboard navigation -------------------------------------------

  // Make slider focusable if not already
  if (!slider.hasAttribute("tabindex")) {
    slider.setAttribute("tabindex", "0");
  }

  slider.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") {
      e.preventDefault();
      stopAutoplay();
      goNext();
      startAutoplay();
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      stopAutoplay();
      goPrev();
      startAutoplay();
    }
  });

  // --- Touch swipe (mobile) -----------------------------------------

  let touchStartX = 0;
  let touchEndX   = 0;

  slider.addEventListener(
    "touchstart",
    (e) => {
      if (!e.touches.length) return;
      touchStartX = e.touches[0].clientX;
      touchEndX   = touchStartX;
      stopAutoplay();
    },
    { passive: true }
  );

  slider.addEventListener(
    "touchmove",
    (e) => {
      if (!e.touches.length) return;
      touchEndX = e.touches[0].clientX;
    },
    { passive: true }
  );

  slider.addEventListener("touchend", () => {
    const deltaX = touchEndX - touchStartX;

    if (Math.abs(deltaX) > SWIPE_THRESHOLD) {
      if (deltaX < 0) {
        goNext();
      } else {
        goPrev();
      }
    }

    startAutoplay();
  });

  // --- Init ----------------------------------------------------------

  goTo(0);
  startAutoplay();
});
