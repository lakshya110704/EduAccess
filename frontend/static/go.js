// Directions page "Back": return to the previous EduAccess page when there is one (e.g. the dashboard);
// otherwise (opened from a WhatsApp link) the link's own href takes the visitor to the EduAccess home page.

const back = document.querySelector("[data-go-back]");
const cameFromEduAccess = document.referrer && new URL(document.referrer).origin === window.location.origin;

if (back && cameFromEduAccess && window.history.length > 1) {
  back.addEventListener("click", (event) => {
    event.preventDefault();
    window.history.back();
  });
}
