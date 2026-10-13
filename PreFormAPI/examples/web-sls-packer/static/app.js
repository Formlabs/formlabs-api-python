// Drop (or pick) files, post them as multipart, and let htmx swap the returned rows into the table.
const zone = document.getElementById("dropzone");
if (zone) {
  const status = document.getElementById("drop-status");
  const upload = (files) => {
    const stls = [...files].filter((f) => /\.(stl|obj|3mf)$/i.test(f.name));
    if (!stls.length) return;
    status.textContent = `Uploading ${stls.length} file(s)…`;
    status.hidden = false;
    const body = new FormData();
    stls.forEach((f) => body.append("files", f, f.name));
    // htmx.ajax cannot carry a FormData body, so post with fetch and hand the fragment to htmx.
    fetch(zone.dataset.url, { method: "POST", body })
      .then((r) => r.text())
      .then((html) => { htmx.swap("#parts", html, { swapStyle: "beforeend" }); status.textContent = `${stls.length} part(s) added.`; })
      .catch((e) => { status.textContent = `Upload failed: ${e}`; });
  };
  ["dragenter", "dragover"].forEach((ev) => zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.add("over"); }));
  ["dragleave", "drop"].forEach((ev) => zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.remove("over"); }));
  zone.addEventListener("drop", (e) => upload(e.dataTransfer.files));
  document.getElementById("picker").addEventListener("change", (e) => upload(e.target.files));
}

// Part viewer: the Three.js module is fetched the first time a thumbnail is clicked, and each part's STL
// only when its dialog opens.
const dialog = document.getElementById("viewer");
if (dialog) {
  let viewer;
  document.addEventListener("click", async (e) => {
    const thumb = e.target.closest(".thumb[data-stl]");
    if (!thumb) return;
    viewer ??= await import("/static/viewer.js");
    viewer.show(dialog, thumb);
  });
  dialog.addEventListener("close", () => viewer && viewer.hide());
  dialog.querySelector(".viewer-close").addEventListener("click", () => dialog.close());
}
