// Cabin form: only list the faculty blocks inside the chosen academic block. The server checks the pair anyway.

for (const form of document.querySelectorAll("[data-cabin-form]")) {
  const academic = form.querySelector("[data-cabin-academic]");
  const faculty = form.querySelector("[data-cabin-faculty]");

  const filter = () => {
    for (const option of faculty.querySelectorAll("option[data-academic]")) {
      const inBlock = option.dataset.academic === academic.value;
      option.hidden = !inBlock;
      option.disabled = !inBlock;
    }
    if (faculty.selectedOptions[0]?.disabled) faculty.value = "";
  };

  academic.addEventListener("change", filter);
  filter();
}
