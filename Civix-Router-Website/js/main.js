(function () {
  "use strict";

  const TYPING_TEXT = "உதாரணம்: தெரு விளக்கு எரியவில்லை...";
  const TYPING_SPEED = 80;
  const TYPING_PAUSE = 2500;

  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", (e) => {
        const id = anchor.getAttribute("href");
        if (!id || id === "#") return;
        const target = document.querySelector(id);
        if (!target) return;
        e.preventDefault();
        const header = document.querySelector(".site-header");
        const offset = header ? header.offsetHeight : 0;
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: "smooth" });
        closeMobileNav();
      });
    });
  }

  function initMobileNav() {
    const header = document.querySelector(".site-header");
    const toggle = document.querySelector(".nav-toggle");
    const nav = document.querySelector("#site-nav");
    if (!header || !toggle || !nav) return;

    toggle.addEventListener("click", () => {
      const open = header.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", String(open));
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeMobileNav);
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeMobileNav();
    });
  }

  function closeMobileNav() {
    const header = document.querySelector(".site-header");
    const toggle = document.querySelector(".nav-toggle");
    if (header) header.classList.remove("nav-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
  }

  function animateCounters() {
    const counters = document.querySelectorAll(".stat-value[data-target]");
    if (!counters.length) return;

    const duration = 2000;

    const runCounter = (el) => {
      const target = parseInt(el.getAttribute("data-target"), 10);
      const suffix = el.getAttribute("data-suffix") || "";
      const start = performance.now();

      function tick(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const value = Math.floor(eased * target);
        el.textContent = value + suffix;
        if (progress < 1) requestAnimationFrame(tick);
        else el.textContent = target + suffix;
      }

      requestAnimationFrame(tick);
    };

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          runCounter(entry.target);
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.4 }
    );

    counters.forEach((c) => observer.observe(c));
  }

  function initTypingAnimation() {
    const el = document.getElementById("typing-text");
    if (!el) return;

    let index = 0;
    let deleting = false;

    function type() {
      if (!deleting) {
        el.textContent = TYPING_TEXT.slice(0, index + 1);
        index++;
        if (index >= TYPING_TEXT.length) {
          setTimeout(() => {
            deleting = true;
            type();
          }, TYPING_PAUSE);
          return;
        }
        setTimeout(type, TYPING_SPEED);
      } else {
        el.textContent = TYPING_TEXT.slice(0, index - 1);
        index--;
        if (index <= 0) {
          deleting = false;
          index = 0;
          setTimeout(type, 400);
          return;
        }
        setTimeout(type, TYPING_SPEED / 2);
      }
    }

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      el.textContent = TYPING_TEXT;
      return;
    }

    type();
  }

  function initHeaderScroll() {
    const header = document.querySelector(".site-header");
    if (!header) return;

    window.addEventListener(
      "scroll",
      () => {
        header.style.background =
          window.scrollY > 40
            ? "rgba(13, 13, 13, 0.95)"
            : "rgba(13, 13, 13, 0.85)";
      },
      { passive: true }
    );
  }

  document.addEventListener("DOMContentLoaded", () => {
    initSmoothScroll();
    initMobileNav();
    initTypingAnimation();
    initHeaderScroll();
    animateCounters();
  });
})();
