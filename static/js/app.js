document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) window.lucide.createIcons();
  const date = document.getElementById("todayDate");
  if (date) date.textContent = new Intl.DateTimeFormat("en-IN",{day:"numeric",month:"short",year:"numeric"}).format(new Date());
  const menu = document.getElementById("menuToggle");
  const sidebar = document.getElementById("sidebar");
  if (menu && sidebar) menu.addEventListener("click", () => sidebar.classList.toggle("open"));
  document.addEventListener("click", e => {
    if (sidebar && sidebar.classList.contains("open") && !sidebar.contains(e.target) && !menu.contains(e.target)) sidebar.classList.remove("open");
  });
  const show = document.getElementById("showPassword");
  const password = document.getElementById("password");
  if (show && password) show.addEventListener("click", () => {
    const isPassword = password.type === "password";
    password.type = isPassword ? "text" : "password";
    show.textContent = isPassword ? "Hide" : "Show";
  });
  document.querySelectorAll("[data-email]").forEach(button => button.addEventListener("click", () => {
    const email = document.getElementById("email");
    const pass = document.getElementById("password");
    if (email && pass) { email.value = button.dataset.email; pass.value = button.dataset.password; pass.focus(); }
  }));
});