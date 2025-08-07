const API_BASE = "http://127.0.0.1:8000/api";

// Load availability of all professors and populate table + dropdown
async function loadAvailability() {
  try {
    const response = await fetch("/api/users/", {
      credentials: "include"
    });

    const users = await response.json();
    console.log("Fetched users from /api/users/:", users);

    const tbody = document.getElementById('availability-table');
    const profDropdown = document.getElementById('professor-select');
    console.log("Dropdown found:", profDropdown);

    if (tbody) tbody.innerHTML = '';
    if (profDropdown) profDropdown.innerHTML = '';

    users
      .filter(user => user.role && user.role.toLowerCase() === 'professor')
      .forEach(prof => {
        console.log("Adding professor to dropdown:", prof.username);

        // Add to availability table
        if (tbody) {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${prof.username}</td>
            <td class="status-${prof.availability_status?.toLowerCase()}">${prof.availability_status}</td>
          `;
          tbody.appendChild(row);
        }

        // Add to appointment dropdown
        if (profDropdown) {
          const option = document.createElement("option");
          option.value = prof.id;
          option.text = prof.username;
          profDropdown.appendChild(option);
        }
      });

  } catch (error) {
    console.error("Error loading professor availability:", error);
  }
}

// Auto-refresh professor availability every 10 seconds
setInterval(() => {
  console.log("Refreshing availability table...");
  loadAvailability();
}, 10000);

// Book a new appointment
async function submitAppointment() {
  const profSelect = document.querySelector("#professor-select");
  const datetimeInput = document.querySelector("#appointment-datetime");

  if (!profSelect || !datetimeInput) {
    alert("Missing form elements");
    return;
  }

  const profId = profSelect.value;
  const datetime = datetimeInput.value;

  if (!profId || !datetime) {
    alert("Please select a professor and date/time.");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/appointments/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: 'include',
      body: JSON.stringify({
        professor: parseInt(profId),
        appointment_time: datetime
      })
    });

    if (response.ok) {
      alert("✅ Appointment Requested!");
    } else {
      const data = await response.json();
      alert("❌ Failed to book: " + JSON.stringify(data));
    }
  } catch (error) {
    console.error("Error submitting appointment", error);
  }
}

// Load user notifications
async function loadNotifications() {
  try {
    const response = await fetch(`${API_BASE}/notifications/`, { credentials: 'include' });
    const notes = await response.json();
    const ul = document.getElementById("notification-list");

    if (ul) {
      ul.innerHTML = '';
      notes.forEach(n => {
        const li = document.createElement("li");
        li.textContent = `${n.message} (${new Date(n.sent_at).toLocaleString()})`;
        ul.appendChild(li);
      });
    }
  } catch (error) {
    console.error("Failed to load notifications", error);
  }
}

// Initialize event handlers and data on page load
window.addEventListener("load", () => {
  loadAvailability();
  loadNotifications();

  const bookBtn = document.querySelector("#appointment button");
  if (bookBtn) {
    bookBtn.addEventListener("click", submitAppointment);
  }

  document.querySelectorAll('input[name="availability-status"]').forEach(radio => {
    radio.addEventListener("change", async () => {
      const selected = document.querySelector('input[name="availability-status"]:checked');
      if (!selected) return;

      const status = selected.value;

      try {
        const resp = await fetch("/api/users/me/", { credentials: 'include' });
        const user = await resp.json();

        const updateResp = await fetch(`${API_BASE}/users/${user.id}/`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          credentials: 'include',
          body: JSON.stringify({ availability_status: status })
        });

        if (!updateResp.ok) {
          alert("Failed to update availability");
        } else {
          console.log("Availability updated to", status);
          loadAvailability(); // Refresh after update
        }

      } catch (error) {
        console.error("Error updating availability:", error);
      }
    });
  });
});