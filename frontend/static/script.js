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
  // Swap only the colour class so extra classes on the box (e.g. header-toast) survive.
  box.classList.remove("flash-success", "flash-error");
  box.classList.add(`flash-${kind}`);
}

function emptyRow(tbody, colspan, text) {
  tbody.replaceChildren(el("tr", { className: "empty-row" }, [el("td", { text, attrs: { colspan } })]));
}

const formatTime = (iso) => new Date(iso).toLocaleString([], { dateStyle: "medium", timeStyle: "short" });
const formatRange = (startIso, endIso) =>
  `${formatTime(startIso)}–${new Date(endIso).toLocaleTimeString([], { timeStyle: "short" })}`;

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

function reasonCell(a) {
  const cell = el("td", {}, [el("strong", { text: a.topic })]);
  if (a.details) cell.appendChild(el("div", { text: a.details, className: "reason-details" }));
  return cell;
}

async function loadAppointments() {
  const isProfessor = PAGE === "professor";
  const tbody = document.getElementById(isProfessor ? "professor-appointment-table" : "student-appointment-table");
  if (!tbody) return;
  try {
    const appts = rows(await api("/appointments/"));
    if (!appts.length) {
      emptyRow(tbody, 5, "No appointments yet.");
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
          if (!isProfessor && a.status === "Pending") {
            actions.appendChild(actionButton("Edit", "action-edit", async () => editReason(a)));
          }
          actions.appendChild(actionButton("Cancel", "action-cancel", () => setAppointmentStatus(a.id, "Cancelled")));
        }
        return el("tr", {}, [
          el("td", { text: isProfessor ? a.student_name : a.professor_name }),
          el("td", { text: formatRange(a.appointment_time, a.end_time) }),
          reasonCell(a),
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

// A professor picked with "Book" from search who isn't in My Professors; kept in the dropdown.
let bookedFromSearch = null;
let lastSearch = "";

const formatClock = (iso) => new Date(iso).toLocaleTimeString([], { timeStyle: "short" });

function openTimeCell(p) {
  const windows = (p.open_today || []).map((w) => `${formatClock(w.start)}–${formatClock(w.end)}`);
  return el("td", { text: windows.length ? `${windows.join(", ")} (walk-in)` : "—", className: "open-time" });
}

// "📍 Directions" link to the cabin directions page, when the cabin location is complete.
function directionsLink(p) {
  if (!p.directions_url) return null;
  return el("a", {
    text: "📍 Directions",
    className: "action-directions",
    attrs: { href: p.directions_url },
  });
}

// "In class: Room 204 · back 3:30 PM". Busy is back later today (a time); Unavailable is back on a day (a date).
function noteText(status, note) {
  if (!note) return "";
  const parts = [[note.pick, note.text].filter(Boolean).join(": ")];
  if (note.until) {
    const until = new Date(note.until);
    const when =
      status === "Busy"
        ? until.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })
        : until.toLocaleDateString([], { weekday: "short", day: "numeric", month: "short" });
    parts.push(`back ${when}`);
  }
  const text = parts.filter(Boolean).join(" · ");
  return text.charAt(0).toUpperCase() + text.slice(1);
}

function statusCell(p) {
  const note = noteText(p.availability_status, p.status_note);
  return el(
    "td",
    { text: p.availability_status, className: `status-${p.availability_status.toLowerCase()}` },
    [note ? el("div", { text: note, className: "status-note" }) : null].filter(Boolean),
  );
}

async function setMine(professor, add) {
  await api(`/professors/${professor.id}/mine/`, { method: add ? "POST" : "DELETE" });
  await loadProfessors();
  if (lastSearch) await runSearch(lastSearch);
}

function fillProfessorSelect(mine) {
  const select = document.getElementById("professor-select");
  if (!select) return;
  const options = [...mine];
  if (bookedFromSearch && !options.some((p) => p.id === bookedFromSearch.id)) options.push(bookedFromSearch);
  // Rebuild only when the set changes, so polling doesn't reset the student's selection.
  const ids = options.map((p) => String(p.id)).join(",");
  if (select.dataset.ids === ids) return;
  const current = select.value;
  select.replaceChildren(...options.map((p) => el("option", { text: p.display_name, attrs: { value: p.id } })));
  if (options.some((p) => String(p.id) === current)) select.value = current;
  select.dataset.ids = ids;
}

async function loadProfessors() {
  const tbody = document.getElementById("availability-table");
  try {
    const mine = rows(await api("/professors/"));
    if (tbody) {
      if (!mine.length) emptyRow(tbody, 5, "No professors yet. Search below and tap ☆ Add to follow them.");
      else
        tbody.replaceChildren(
          ...mine.map((p) =>
            el("tr", {}, [
              el("td", { text: p.display_name }),
              el("td", { text: p.cabin_label || "—" }),
              statusCell(p),
              openTimeCell(p),
              el(
                "td",
                {},
                [directionsLink(p), actionButton("✕ Remove", "action-cancel", () => setMine(p, false))].filter(Boolean),
              ),
            ]),
          ),
        );
    }
    fillProfessorSelect(mine);
  } catch (error) {
    console.error("Failed to load professors", error);
  }
}

function bookProfessor(professor) {
  bookedFromSearch = professor;
  loadProfessors().then(() => {
    document.getElementById("find-dialog").close();
    openDialog("book-dialog");
    document.getElementById("professor-select").value = String(professor.id);
    document.getElementById("appointment-datetime").focus();
  });
}

async function runSearch(query) {
  const table = document.getElementById("search-results-table");
  const tbody = document.getElementById("search-results");
  const results = rows(await api(`/professors/?search=${encodeURIComponent(query)}`));
  lastSearch = query;
  table.hidden = false;
  if (!results.length) {
    emptyRow(tbody, 4, `No professor matches "${query}".`);
    return;
  }
  tbody.replaceChildren(
    ...results.map((p) => {
      const actions = el("td");
      actions.appendChild(
        p.is_mine
          ? el("button", { text: "✓ Added", className: "action-added", attrs: { type: "button", disabled: "" } })
          : actionButton("☆ Add", "action-add", () => setMine(p, true)),
      );
      actions.appendChild(actionButton("Book", "action-confirm", async () => bookProfessor(p)));
      const directions = directionsLink(p);
      if (directions) actions.appendChild(directions);
      return el("tr", {}, [
        el("td", { text: p.display_name }),
        el("td", { text: p.cabin_label || "—" }),
        statusCell(p),
        actions,
      ]);
    }),
  );
}

async function searchProfessors(event) {
  event.preventDefault();
  const query = document.getElementById("professor-query").value.trim();
  showMessage("search-message", "", "success");
  if (query.length < 2) {
    showMessage("search-message", "Type at least 2 characters to search.", "error");
    return;
  }
  try {
    await runSearch(query);
  } catch (error) {
    showMessage("search-message", error.message, "error");
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
      body: {
        professor: Number(professor),
        appointment_time: new Date(datetime).toISOString(),
        slots: Number(document.getElementById("appointment-slots").value),
        topic: document.getElementById("appointment-topic").value,
        details: document.getElementById("appointment-details").value.trim(),
      },
    });
    showMessage("appointment-message", "Appointment requested. You'll be notified when the professor responds.");
    event.target.reset();
    loadAppointments();
    // Close the panel shortly after success; the request now shows under My Appointments.
    setTimeout(() => {
      document.getElementById("book-dialog").close();
      showMessage("appointment-message", "", "success");
    }, 1500);
  } catch (error) {
    showMessage("appointment-message", error.message, "error");
  } finally {
    if (button) button.disabled = false;
  }
}

function editReason(appt) {
  document.getElementById("reason-appointment").value = appt.id;
  document.getElementById("reason-topic").value = appt.topic;
  document.getElementById("reason-details").value = appt.details;
  showMessage("reason-message", "", "success");
  openDialog("reason-dialog");
}

async function saveReason(event) {
  event.preventDefault();
  const button = event.submitter;
  if (button) button.disabled = true;
  try {
    await api(`/appointments/${document.getElementById("reason-appointment").value}/`, {
      method: "PATCH",
      body: {
        topic: document.getElementById("reason-topic").value,
        details: document.getElementById("reason-details").value.trim(),
      },
    });
    document.getElementById("reason-dialog").close();
    loadAppointments();
  } catch (error) {
    showMessage("reason-message", error.message, "error");
  } finally {
    if (button) button.disabled = false;
  }
}

// ---------- professor ----------

let myStatus = null;

// The header button shows the current note, and is hidden when Free (Free has no note).
function showMyNote(me) {
  myStatus = me;
  document.getElementById("status-note-button").hidden = me.availability_status === "Free";
  document.getElementById("status-note-label").textContent =
    noteText(me.availability_status, me.status_note) || "Add note";
}

async function loadMyNote() {
  try {
    showMyNote(await api("/me/"));
  } catch (error) {
    console.error("Failed to load status", error);
  }
}

function openNoteDialog() {
  const status = myStatus.availability_status;
  const note = myStatus.status_note || {};
  const picks = JSON.parse(document.getElementById("status-note-picks-data").textContent)[status];
  document.getElementById("status-note-status").textContent = status.toLowerCase();
  document.getElementById("status-note-picks").replaceChildren(
    ...["", ...picks].flatMap((pick, i) => {
      const id = `status-note-pick-${i}`;
      const radio = el("input", { attrs: { type: "radio", name: "status-note-pick", id, value: pick } });
      radio.checked = pick === (note.pick || "");
      return [radio, el("label", { text: pick || "None", attrs: { for: id } })];
    }),
  );
  document.getElementById("status-note-text").value = note.text || "";
  // Busy: a time today. Unavailable: a day. Prefill in local time.
  const until = note.until ? new Date(note.until) : null;
  const local = until ? new Date(until - until.getTimezoneOffset() * 60000).toISOString() : "";
  document.getElementById("status-note-time-label").hidden = status !== "Busy";
  document.getElementById("status-note-date-label").hidden = status === "Busy";
  document.getElementById("status-note-time").value = status === "Busy" ? local.slice(11, 16) : "";
  document.getElementById("status-note-date").value = status === "Busy" ? "" : local.slice(0, 10);
  const today = new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10);
  document.getElementById("status-note-date").min = today;
  document.getElementById("status-note-message").textContent = "";
  openDialog("status-note-dialog");
}

async function saveNote(note) {
  try {
    showMyNote(await api("/me/", { method: "PATCH", body: note }));
    document.getElementById("status-note-dialog").close();
  } catch (error) {
    showMessage("status-note-message", error.message, "error");
  }
}

function submitNote(event) {
  event.preventDefault();
  const busy = myStatus.availability_status === "Busy";
  const time = document.getElementById("status-note-time").value;
  const date = document.getElementById("status-note-date").value;
  // Local wall-clock time to an instant: today at the time for Busy, start of the day for Unavailable.
  const today = new Date().toLocaleDateString("en-CA");
  let until = null;
  if (busy && time) until = new Date(`${today}T${time}`).toISOString();
  if (!busy && date) until = new Date(`${date}T00:00`).toISOString();
  saveNote({
    status_pick: document.querySelector('input[name="status-note-pick"]:checked')?.value || "",
    status_text: document.getElementById("status-note-text").value,
    status_until: until,
  });
}

async function updateAvailability(event) {
  const status = event.target.value;
  try {
    showMyNote(await api("/me/", { method: "PATCH", body: { availability_status: status } }));
    if (status !== "Free") openNoteDialog();
    showMessage("availability-message", `Status set to ${status}.`);
    // Brief confirmation only; clear it unless a newer message replaced it.
    setTimeout(() => {
      const box = document.getElementById("availability-message");
      if (box.textContent === `Status set to ${status}.`) box.textContent = "";
    }, 3000);
  } catch (error) {
    showMessage("availability-message", error.message, "error");
  }
}

async function loadOpenTimes() {
  const tbody = document.getElementById("open-time-table");
  if (!tbody) return;
  try {
    const windows = rows(await api("/open-times/"));
    if (!windows.length) {
      emptyRow(tbody, 2, "No open time set for today.");
      return;
    }
    tbody.replaceChildren(
      ...windows.map((w) =>
        el("tr", {}, [
          el("td", { text: `${formatClock(w.start)}–${formatClock(w.end)}` }),
          el("td", {}, [
            actionButton("✕ Remove", "action-cancel", async () => {
              await api(`/open-times/${w.id}/`, { method: "DELETE" });
              await loadOpenTimes();
            }),
          ]),
        ]),
      ),
    );
  } catch (error) {
    console.error("Failed to load open time", error);
  }
}

// "HH:MM" today, in local time, as an ISO timestamp.
function todayAt(hhmm) {
  const [h, m] = hhmm.split(":").map(Number);
  const d = new Date();
  d.setHours(h, m, 0, 0);
  return d.toISOString();
}

async function addOpenTime(event) {
  event.preventDefault();
  const start = document.getElementById("open-start").value;
  const end = document.getElementById("open-end").value;
  try {
    await api("/open-times/", { method: "POST", body: { start: todayAt(start), end: todayAt(end) } });
    showMessage("open-time-message", `Open time ${start}–${end} added. Students can see it now.`);
    event.target.reset();
    await Promise.all([loadOpenTimes(), loadAppointments()]);
  } catch (error) {
    showMessage("open-time-message", error.message, "error");
  }
}

// ---------- pop-up panels ----------

function openDialog(id) {
  const dialog = document.getElementById(id);
  if (!dialog.open) dialog.showModal();
  dialog.querySelector("input:not([type=hidden]), select")?.focus();
}

function wireDialogs() {
  for (const opener of document.querySelectorAll("[data-open-dialog]")) {
    opener.addEventListener("click", () => openDialog(opener.dataset.openDialog));
  }
  for (const dialog of document.querySelectorAll("dialog.panel")) {
    for (const closer of dialog.querySelectorAll("[data-close-dialog]")) {
      closer.addEventListener("click", () => dialog.close());
    }
    // A click on the dimmed backdrop closes it. Backdrop clicks target the <dialog> itself; checking that
    // first matters because pressing Enter in a form fires a synthetic click at (0, 0) on the submit button,
    // which would otherwise look like a click outside the panel.
    dialog.addEventListener("click", (event) => {
      if (event.target !== dialog) return;
      const box = dialog.getBoundingClientRect();
      const inside =
        event.clientX >= box.left &&
        event.clientX <= box.right &&
        event.clientY >= box.top &&
        event.clientY <= box.bottom;
      if (!inside) dialog.close();
    });
  }
}

// ---------- init ----------

function refresh() {
  if (document.hidden) return;
  loadNotifications();
  loadAppointments();
  if (PAGE === "student") loadProfessors();
  if (PAGE === "professor") {
    loadOpenTimes();
    loadMyNote();
  }
}

window.addEventListener("DOMContentLoaded", () => {
  wireDialogs();
  if (PAGE === "student") {
    // Earliest choice: the next quarter hour, in local time (bookings start on :00/:15/:30/:45).
    const quarter = 15 * 60000;
    const next = Math.ceil(Date.now() / quarter) * quarter;
    const minTime = new Date(next - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 16);
    document.getElementById("appointment-datetime").min = minTime;
    document.getElementById("appointment-form").addEventListener("submit", submitAppointment);
    document.getElementById("reason-form").addEventListener("submit", saveReason);
    document.getElementById("search-form").addEventListener("submit", searchProfessors);
  }
  if (PAGE === "professor") {
    document.getElementById("open-time-form").addEventListener("submit", addOpenTime);
    document.getElementById("status-note-button").addEventListener("click", openNoteDialog);
    document.getElementById("status-note-form").addEventListener("submit", submitNote);
    document
      .getElementById("status-note-clear")
      .addEventListener("click", () => saveNote({ status_pick: "", status_text: "", status_until: null }));
    for (const radio of document.querySelectorAll('input[name="availability-status"]')) {
      radio.addEventListener("change", updateAvailability);
    }
  }
  refresh();
  setInterval(refresh, REFRESH_MS);
  document.addEventListener("visibilitychange", refresh);
});
