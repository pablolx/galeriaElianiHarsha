const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector("#site-nav");

if (navToggle && siteNav) {
  navToggle.addEventListener("click", () => {
    const expanded = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!expanded));
    navToggle.querySelector(".menu-label").textContent = expanded ? "Abrir menu" : "Fechar menu";
    siteNav.classList.toggle("is-open", !expanded);
  });
}

document.querySelectorAll(".copy-link").forEach((button) => {
  button.addEventListener("click", async () => {
    const feedback = button.closest(".share-block").querySelector(".copy-feedback");
    try {
      if (navigator.share) {
        await navigator.share({ title: document.title, url: button.dataset.shareUrl });
        feedback.textContent = "Link compartilhado.";
      } else {
        await navigator.clipboard.writeText(button.dataset.shareUrl);
        feedback.textContent = "Link copiado.";
      }
    } catch (error) {
      if (error.name !== "AbortError") {
        feedback.textContent = "Não foi possível compartilhar. Copie o endereço da página.";
      }
    }
  });
});
