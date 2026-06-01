(function () {
  "use strict";

  const LABELS = [
    "Water Supply",
    "Electricity",
    "Public Works",
    "Sanitation",
    "General",
  ];
  const DATA = [45, 32, 28, 15, 20];

  function initChart() {
    const canvas = document.getElementById("dept-chart");
    if (!canvas || typeof Chart === "undefined") return;

    const ctx = canvas.getContext("2d");

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: LABELS,
        datasets: [
          {
            label: "Complaints",
            data: DATA,
            backgroundColor: [
              "rgba(255, 149, 0, 0.85)",
              "rgba(10, 132, 255, 0.85)",
              "rgba(255, 149, 0, 0.55)",
              "rgba(10, 132, 255, 0.55)",
              "rgba(134, 134, 139, 0.7)",
            ],
            borderColor: [
              "#FF9500",
              "#0A84FF",
              "#FF9500",
              "#0A84FF",
              "#86868B",
            ],
            borderWidth: 1,
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        animation: {
          duration: 1500,
          easing: "easeOutQuart",
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: "#1C1C1E",
            titleColor: "#F5F5F7",
            bodyColor: "#86868B",
            borderColor: "rgba(255, 149, 0, 0.3)",
            borderWidth: 1,
          },
        },
        scales: {
          x: {
            grid: { color: "rgba(255, 255, 255, 0.05)" },
            ticks: { color: "#86868B", font: { family: "system-ui, sans-serif" } },
          },
          y: {
            beginAtZero: true,
            grid: { color: "rgba(255, 255, 255, 0.05)" },
            ticks: {
              color: "#86868B",
              stepSize: 10,
              font: { family: "system-ui, sans-serif" },
            },
          },
        },
      },
    });
  }

  function observeChart() {
    const section = document.getElementById("analytics");
    if (!section) {
      initChart();
      return;
    }

    let started = false;
    const observer = new IntersectionObserver(
      (entries) => {
        if (started) return;
        if (entries.some((e) => e.isIntersecting)) {
          started = true;
          initChart();
          observer.disconnect();
        }
      },
      { threshold: 0.2 }
    );
    observer.observe(section);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", observeChart);
  } else {
    observeChart();
  }
})();
