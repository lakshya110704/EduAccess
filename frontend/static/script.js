// EduAccess dashboards. The page type comes from <body data-page="student|professor">.

const API_BASE = "/api";
const REFRESH_MS = 10000;
const PAGE = document.body.dataset.page;

function getCookie(name) {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : null;
}

// fetch wrapper: same-origin session auth, CSRF header on writes, JSON in/out.
// Throws an Error carrying the server's message on failure.
async function api(path, { method = "GET", body } = {}) {
  const headers = { Accept: "application/json" };
  if (method !== "GET") {
    headers["Content-Type"] = "application/json";
    headers["X-CSRFToken"] = getCookie("csrftoken");
  }
  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    credentials: "same-origin",
    body: body ? JSON.stringify(body) : undefined,
  });
  // SessionAuthentication answers 403 (not 401) when the session is gone.
  if (response.status === 401 || (response.status === 403 && method === "GET")) {
    window.location.href = "/login/";
    throw new Error("Session expired");
  }
  const data = response.status === 204 ? null : await response.json().catch(() => null);
  if (!response.ok) throw new Error(errorText(data) || `Request failed (${response.status})`);
  return data;
}

// DRF errors come as {detail}, {field: [msgs]} or {non_field_errors: [msgs]}.
function errorText(data) {
  if (!data) return "";
  if (typeof data.detail === "string") return data.detail;
  return Object.values(data).flat().join(" ");
}

// DRF list endpoints may or may not be paginated.
const rows = (data) => (Array.isArray(data) ? data : data.results || []);

function el(tag, { text, className, attrs } = {}, children = []) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  for (const [k, v] of Object.entries(attrs || {})) node.setAttribute(k, v);
  for (const child of children) node.appendChild(child);
  return node;
}

function showMessage(id, text, kind = "success") {
  const box = document.getElementById(id);
  if (!box) return;
  box.textContent = text;
  box.className = `flash form-message flash-${kind}`;
}

function emptyRow(tbody, colspan, text) {
  tbody.replaceChildren(el("tr", { className: "empty-row" }, [el("td", { text, attrs: { colspan } })]));
}

const formatTime = (iso) => new Date(iso).toLocaleString([], { dateStyle: "medium", timeStyle: "short" });

// ---------- shared ----------

async function loadNotifications() {
  const ul = document.getElementById("notification-list");
  if (!ul) return;
  try {
    const notes = rows(await api("/notifications/"));
    if (!notes.length) {
      ul.replaceChildren(el("li", { text: "No notifications yet.", className: "empty-row" }));
      return;
    }
    ul.replaceChildren(...notes.map((n) => el("li", { text: `${n.message} (${formatTime(n.sent_at)})` })));
  } catch (error) {
    console.error("Failed to load notifications", error);
  }
}

async function setAppointmentStatus(id, status) {
  await api(`/appointments/${id}/`, { method: "PATCH", body: { status } });
  await Promise.all([loadAppointments(), loadNotifications()]);
}

function actionButton(label, className, onClick) {
  const button = el("button", { text: label, className, attrs: { type: "button" } });
  button.addEventListener("click", async () => {
    button.disabled = true;
    try {
      await onClick();
    } catch (error) {
      alert(error.message);
      button.disabled = false;
    }
  });
  return button;
}

async function loadAppointments() {
  const isProfessor = PAGE === "professor";
  const tbody = document.getElementById(isProfessor ? "professor-appointment-table" : "student-appointment-table");
  if (!tbody) return;
  try {
    const appts = rows(await api("/appointments/"));
    if (!appts.length) {
      emptyRow(tbody, 4, "No appointments yet.");
      return;
    }
    tbody.replaceChildren(
      ...appts.map((a) => {
        const actions = el("td");
        if (a.status !== "Cancelled") {
          if (isProfessor && a.status === "Pending") {
            actions.appendChild(
              actionButton("Confirm", "action-confirm", () => setAppointmentStatus(a.id, "Confirmed")),
            );
          }
          actions.appendChild(actionButton("Cancel", "action-cancel", () => setAppointmentStatus(a.id, "Cancelled")));
        }
        return el("tr", {}, [
          el("td", { text: isProfessor ? a.student_name : a.professor_name }),
          el("td", { text: formatTime(a.appointment_time) }),
          el("td", { text: a.status, className: `status-${a.status.toLowerCase()}` }),
          actions,
        ]);
      }),
    );
  } catch (error) {
    console.error("Failed to load appointments", error);
  }
}

// ---------- student ----------

async function loadProfessors() {
  const tbody = document.getElementById("availability-table");
  const select = document.getElementById("professor-select");
  try {
    const profs = rows(await api("/professors/"));
    if (tbody) {
      if (!profs.length) emptyRow(tbody, 3, "No professors registered yet.");
      else
        tbody.replaceChildren(
          ...profs.map((p) =>
            el("tr", {}, [
              el("td", { text: p.display_name }),
              el("td", { text: p.cabin_number || "—" }),
              el("td", { text: p.availability_status, className: `status-${p.availability_status.toLowerCase()}` }),
            ]),
          ),
        );
    }
    // Rebuild the dropdown only if the set of professors changed, so polling
    // doesn't reset the student's selection.
    if (select) {
      const ids = profs.map((p) => String(p.id)).join(",");
      if (select.dataset.ids !== ids) {
        const current = select.value;
        select.replaceChildren(...profs.map((p) => el("option", { text: p.display_name, attrs: { value: p.id } })));
        if (profs.some((p) => String(p.id) === current)) select.value = current;
        select.dataset.ids = ids;
      }
    }
  } catch (error) {
    console.error("Failed to load professors", error);
  }
}

async function findCabin(event) {
  event.preventDefault();
  const query = document.getElementById("cabin-query").value.trim();
  const list = document.getElementById("cabin-results");
  if (!query) return;
  try {
    const profs = rows(await api(`/professors/?search=${encodeURIComponent(query)}`));
    if (!profs.length) {
      list.replaceChildren(el("li", { text: `No professor matches "${query}".` }));
      return;
    }
    list.replaceChildren(
      ...profs.map((p) =>
        el("li", {
          text: `${p.display_name}: ${p.cabin_number ? `Cabin ${p.cabin_number}` : "cabin not set"} · ${p.availability_status}`,
        }),
      ),
    );
  } catch (error) {
    list.replaceChildren(el("li", { text: error.message }));
  }
}

async function submitAppointment(event) {
  event.preventDefault();
  const professor = document.getElementById("professor-select").value;
  const datetime = document.getElementById("appointment-datetime").value;
  if (!professor || !datetime) {
    showMessage("appointment-message", "Please select a professor and a date/time.", "error");
    return;
  }
  const button = event.submitter;
  if (button) button.disabled = true;
  try {
    // datetime-local has no zone; send it as the browser's local time in ISO form.
    await api("/appointments/", {
      method: "POST",
      body: { professor: Number(professor), appointment_time: new Date(datetime).toISOString() },
    });
    showMessage("appointment-message", "Appointment requested. You'll be notified when the professor responds.");
    event.target.reset();
    loadAppointments();
  } catch (error) {
    showMessage("appointment-message", error.message, "error");
  } finally {
    if (button) button.disabled = false;
  }
}

// ---------- professor ----------

async function updateAvailability(event) {
  const status = event.target.value;
  try {
    await api("/me/", { method: "PATCH", body: { availability_status: status } });
    showMessage("availability-message", `Status set to ${status}.`);
  } catch (error) {
    showMessage("availability-message", error.message, "error");
  }
}

// ---------- init ----------

function refresh() {
  if (document.hidden) return;
  loadNotifications();
  loadAppointments();
  if (PAGE === "student") loadProfessors();
}

window.addEventListener("DOMContentLoaded", () => {
  if (PAGE === "student") {
    const minTime = new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 16);
    document.getElementById("appointment-datetime").min = minTime;
    document.getElementById("appointment-form").addEventListener("submit", submitAppointment);
    document.getElementById("cabin-form").addEventListener("submit", findCabin);
  }
  if (PAGE === "professor") {
    for (const radio of document.querySelectorAll('input[name="availability-status"]')) {
      radio.addEventListener("change", updateAvailability);
    }
  }
  refresh();
  setInterval(refresh, REFRESH_MS);
  document.addEventListener("visibilitychange", refresh);
});
