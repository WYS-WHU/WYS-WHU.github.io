// Official image: geography and page-view totals. Previews never send events.
(() => {
  const section = document.querySelector("#visitors");
  if (!section) return;
  const frame = section.querySelector("#visitor-map");
  const status = frame.querySelector(".visitor-status");
  if (location.protocol !== "https:" || location.hostname !== section.dataset.hostname) {
    status.textContent = "Visitor statistics are available on the live website.";
    return;
  }
  const link = document.createElement("a");
  link.href = section.dataset.statsUrl;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.setAttribute("aria-label", "View visitor locations and page-view statistics on Flag Counter");
  const image = new Image();
  image.alt = "World map showing visitor countries and the total website page views, provided by Flag Counter";
  image.decoding = "async";
  image.onload = () => {
    status.hidden = true;
    frame.classList.add("is-loaded");
  };
  image.onerror = () => {
    image.hidden = true;
    status.textContent = "Visitor statistics are temporarily unavailable.";
  };
  link.append(image);
  frame.append(link);
  // Count the page load even when the visitor does not scroll to the footer.
  image.src = section.dataset.imageUrl;
})();
