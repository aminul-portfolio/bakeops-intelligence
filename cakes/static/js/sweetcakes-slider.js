document.addEventListener("DOMContentLoaded", () => {
  const slider = document.getElementById("scHeroSlider");
  if (!slider) return;

  const track = slider.querySelector(".sc-hero-slider__track");
  const slides = slider.querySelectorAll(".sc-hero-slider__slide");
  const prevBtn = slider.querySelector(".sc-hero-slider__control--prev");
  const nextBtn = slider.querySelector(".sc-hero-slider__control--next");
  const dots = slider.querySelectorAll(".sc-hero-slider__dot");

  if (!track || slides.length === 0 || !prevBtn || !nextBtn) return;

  let currentIndex = 0;
  let isAnimating = false;
  let autoplayTimer = null;
  const AUTOPLAY_DELAY = 6500;

  function setActiveDot(index) {
    dots.forEach((dot, dotIndex) => {
      const isActive = dotIndex === index;
      dot.classList.toggle("is-active", isActive);
      dot.setAttribute("aria-current", isActive ? "true" : "false");
    });
  }

  function goTo(index) {
    if (isAnimating) return;

    const total = slides.length;
    const newIndex = (index + total) % total;
    if (newIndex === currentIndex) return;

    isAnimating = true;
    currentIndex = newIndex;
    track.style.transform = `translateX(-${currentIndex * 100}%)`;
    setActiveDot(currentIndex);

    window.setTimeout(() => {
      isAnimating = false;
    }, 500);
  }

  function goNext() {
    goTo(currentIndex + 1);
  }

  function goPrev() {
    goTo(currentIndex - 1);
  }

  function startAutoplay() {
    if (autoplayTimer !== null) return;
    autoplayTimer = window.setInterval(goNext, AUTOPLAY_DELAY);
  }

  function stopAutoplay() {
    if (autoplayTimer === null) return;
    window.clearInterval(autoplayTimer);
    autoplayTimer = null;
  }

  nextBtn.addEventListener("click", (event) => {
    event.preventDefault();
    stopAutoplay();
    goNext();
    startAutoplay();
  });

  prevBtn.addEventListener("click", (event) => {
    event.preventDefault();
    stopAutoplay();
    goPrev();
    startAutoplay();
  });

  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      stopAutoplay();
      goTo(index);
      startAutoplay();
    });
  });

  slider.addEventListener("mouseenter", stopAutoplay);
  slider.addEventListener("mouseleave", startAutoplay);
  slider.addEventListener("focusin", stopAutoplay);
  slider.addEventListener("focusout", startAutoplay);

  slider.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight") {
      event.preventDefault();
      stopAutoplay();
      goNext();
      startAutoplay();
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      stopAutoplay();
      goPrev();
      startAutoplay();
    }
  });

  let touchStartX = 0;
  let touchEndX = 0;

  slider.addEventListener(
    "touchstart",
    (event) => {
      if (!event.touches.length) return;
      touchStartX = event.touches[0].clientX;
      touchEndX = touchStartX;
      stopAutoplay();
    },
    { passive: true }
  );

  slider.addEventListener(
    "touchmove",
    (event) => {
      if (!event.touches.length) return;
      touchEndX = event.touches[0].clientX;
    },
    { passive: true }
  );

  slider.addEventListener("touchend", () => {
    const deltaX = touchEndX - touchStartX;
    if (Math.abs(deltaX) > 40) {
      if (deltaX < 0) {
        goNext();
      } else {
        goPrev();
      }
    }
    startAutoplay();
  });

  track.style.transition = "transform 0.5s ease";
  goTo(0);
  startAutoplay();
});
