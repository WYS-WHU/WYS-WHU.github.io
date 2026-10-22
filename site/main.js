document.documentElement.classList.add("js");

// The preview proxies public counts; static exports retain their last snapshot.
const metricNodes = [...document.querySelectorAll("[data-metric-id]")];
const localPreview = ["127.0.0.1", "localhost"].includes(location.hostname);
let metricsInFlight = false;
async function updateMetrics() {
  if (!metricNodes.length || metricsInFlight || document.hidden || location.protocol === "file:") return;
  metricsInFlight = true;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(localPreview ? "/api/metrics" : "assets/metrics.json", { cache: "no-store", signal: controller.signal });
    if (!response.ok) throw new Error("Counters unavailable");
    const snapshot = await response.json();
    if (!Array.isArray(snapshot.items)) throw new Error("Invalid counters");
    const values = new Map(snapshot.items.map(item => [item.id, item.value]));
    if (!metricNodes.every(node => Number.isSafeInteger(values.get(node.dataset.metricId)) && values.get(node.dataset.metricId) >= 0)) throw new Error("Incomplete counters");
    metricNodes.forEach(node => { node.textContent = values.get(node.dataset.metricId).toLocaleString("en-US"); });
  } catch {
    // Keep the last validated HTML snapshot on failure or offline.
  } finally {
    clearTimeout(timeout);
    metricsInFlight = false;
  }
}
updateMetrics();
if (localPreview) {
  setInterval(updateMetrics, 60000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) updateMetrics(); });
}

const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".primary-nav");
const closeMenu = () => {
  menuButton.setAttribute("aria-expanded", "false");
  navigation.classList.remove("is-open");
};
menuButton.addEventListener("click", () => {
  const opening = menuButton.getAttribute("aria-expanded") !== "true";
  menuButton.setAttribute("aria-expanded", String(opening));
  navigation.classList.toggle("is-open", opening);
});
navigation.addEventListener("click", event => {
  if (event.target.closest("a")) closeMenu();
});
document.addEventListener("keydown", event => {
  if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
    closeMenu();
    menuButton.focus();
  }
});

const dialog = document.querySelector("#figure-dialog");
const figureCanvas = document.querySelector("#figure-canvas");
let figureImage = null;
const figureTitle = document.querySelector("#figure-title");
const originalLink = document.querySelector("#figure-original");
let figureTrigger = null;
if (typeof dialog.showModal === "function") {
  document.querySelectorAll(".publication-figure").forEach(link => {
    link.addEventListener("click", event => {
      event.preventDefault();
      figureTrigger = link;
      if (!figureImage) {
        figureImage = document.createElement("img");
        figureImage.id = "figure-image";
        figureCanvas.append(figureImage);
      }
      figureImage.src = link.href;
      figureImage.alt = link.querySelector("img").alt;
      figureTitle.textContent = link.dataset.figureTitle;
      originalLink.href = link.href;
      dialog.showModal();
    });
  });
  document.querySelector(".dialog-close").addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", event => {
    if (event.target === dialog) {
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    }
  });
  dialog.addEventListener("close", () => { if (figureTrigger) figureTrigger.focus(); });
}

if ("IntersectionObserver" in window) {
  const links = [...navigation.querySelectorAll("a")];
  const sections = [...document.querySelectorAll("main > section")];
  const updateCurrent = id => {
    links.forEach(link => {
      if (link.getAttribute("href") === `#${id}`) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  };
  const observer = new IntersectionObserver(() => {
    let current = sections[0];
    sections.forEach(section => { if (section.getBoundingClientRect().top <= innerHeight * .33) current = section; });
    updateCurrent(current.id);
  }, { rootMargin: "-10% 0px -65% 0px", threshold: 0 });
  sections.forEach(section => observer.observe(section));
}
