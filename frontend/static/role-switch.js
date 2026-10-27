// Login / sign-up role switch: follow it with the page theme and heading icon, and remember the last
// choice in this browser. Purely cosmetic: the server still checks the role against the account.

const STORAGE_KEY = "eduaccess-role";
const ICONS = { student: "fa-user-graduate", professor: "fa-chalkboard-teacher" };
const radios = document.querySelectorAll('.role-switch input[name="role"]');

function currentRole() {
  return document.querySelector('.role-switch input[name="role"]:checked')?.value || "student";
}

function applyRole(role) {
  document.body.dataset.theme = role;
  for (const icon of document.querySelectorAll("[data-role-icon]")) {
    icon.classList.remove(...Object.values(ICONS));
    icon.classList.add(ICONS[role]);
  }
  try {
    localStorage.setItem(STORAGE_KEY, role);
  } catch {
    // Storage may be blocked (private mode); the switch still works.
  }
  document.dispatchEvent(new CustomEvent("rolechange", { detail: { role } }));
}

// A fresh page (no role sent back by the server after an error) starts from the remembered role.
const serverChoseRole = document.querySelector('.role-switch input[value="professor"]:checked');
if (!serverChoseRole) {
  let remembered = null;
  try {
    remembered = localStorage.getItem(STORAGE_KEY);
  } catch {
    remembered = null;
  }
  const match = remembered && document.querySelector(`.role-switch input[value="${CSS.escape(remembered)}"]`);
  if (match) match.checked = true;
}

for (const radio of radios) {
  radio.addEventListener("change", () => applyRole(currentRole()));
}
applyRole(currentRole());
