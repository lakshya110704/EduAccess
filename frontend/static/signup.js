// Sign-up page: relabel the ID and email fields for the selected role.
// Only cosmetic: the server enforces every rule regardless of what this script does.

const form = document.getElementById("signup-form");
const role = document.getElementById("id_role");
const collegeId = document.getElementById("id_college_id");
const email = document.getElementById("id_email");

function relabel() {
  const professor = role.value === "professor";
  const domain = professor ? form.dataset.professorDomain : form.dataset.studentDomain;
  collegeId.placeholder = professor ? "Employee ID" : "Roll number";
  collegeId.setAttribute("aria-label", collegeId.placeholder);
  email.placeholder = `College email (@${domain})`;
  email.setAttribute("aria-label", email.placeholder);
}

role.addEventListener("change", relabel);
relabel();
