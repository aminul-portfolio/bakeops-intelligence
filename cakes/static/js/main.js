document.addEventListener("DOMContentLoaded", () => {
  const slider = document.querySelector(".cake-slider");
  if (!slider) return;

  const container = slider.querySelector(".slides-container");
  const slides = slider.querySelectorAll(".cake-slide");
  const prevBtn = slider.querySelector(".slider-btn.prev");
  const nextBtn = slider.querySelector(".slider-btn.next");

  let current = 0;
  const max = slides.length;

  function goTo(index) {
    current = (index + max) % max; // wrap around
    container.style.transform = `translateX(-${current * 100}%)`;
  }

  function next() {
    goTo(current + 1);
  }

  function prev() {
    goTo(current - 1);
  }

  let timer = setInterval(next, 5000);

  function resetTimer() {
    clearInterval(timer);
    timer = setInterval(next, 5000);
  }

  nextBtn.addEventListener("click", () => {
    next();
    resetTimer();
  });

  prevBtn.addEventListener("click", () => {
    prev();
    resetTimer();
  });
});
