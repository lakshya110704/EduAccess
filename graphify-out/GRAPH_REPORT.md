# Graph Report - EduAccess  (2026-10-24)

## Corpus Check
- 25 files · ~291,037 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 2, .example 1, .css 1)

## Summary
- 254 nodes · 392 edges · 25 communities (12 shown, 13 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 34 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `791b41a0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- eduaccess_backend/urls.py
- CustomUser
- Frontend Templates & Flows
- Project Config & Entrypoints
- Appointment
- script.js
- PageTests
- MeSerializer
- App Config
- Brand Logo
- tests.py
- Background Image
- BookingTests
- EduAccess
- tests.py
- permissions.py
- api/urls.py
- ProfessorSerializer

## God Nodes (most connected - your core abstractions)
1. `AppointmentAccessTests` - 12 edges
2. `PageTests` - 12 edges
3. `BaseTestCase` - 11 edges
4. `AppointmentViewSet` - 11 edges
5. `api()` - 11 edges
6. `CustomUser` - 11 edges
7. `AppointmentSerializer` - 10 edges
8. `BookingTests` - 10 edges
9. `loadAppointments()` - 10 edges
10. `loadNotifications()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Layout` --references--> `IsAppointmentParticipant`  [INFERRED]
  CLAUDE.md → api/permissions.py
- `Layout` --references--> `role_required()`  [INFERRED]
  CLAUDE.md → api/permissions.py
- `Layout` --references--> `api()`  [INFERRED]
  CLAUDE.md → frontend/static/script.js
- `Teal Login button` --shares_data_with--> `login_view()`  [INFERRED]
  frontend/static/assets/login.png → api/views.py
- `Select Role dropdown` --shares_data_with--> `login_view()`  [INFERRED]
  frontend/static/assets/login.png → api/views.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Student Dashboard Features** — frontend_templates_student_dashboard_availability_section, frontend_templates_student_dashboard_locator_section, frontend_templates_student_dashboard_appointment_section, frontend_templates_student_dashboard_notifications_section [EXTRACTED 1.00]
- **Role-Based UI Templates** — frontend_templates_login, frontend_templates_student_dashboard, frontend_templates_professor_dashboard [INFERRED 0.85]

## Communities (25 total, 13 thin omitted)

### Community 0 - "eduaccess_backend/urls.py"
Cohesion: 0.18
Nodes (5): role_required(), decorator(), logout_view(), professor_dashboard(), student_dashboard()

### Community 1 - "CustomUser"
Cohesion: 0.13
Nodes (4): Command, Migration, Migration, Migration

### Community 2 - "Frontend Templates & Flows"
Cohesion: 0.11
Nodes (22): Login Page, Login Form (username, password, role), Professor Dashboard Page, Manage Appointments Table, Update Availability Section, Student Dashboard Page, Book Appointment Section, Professor Availability Table (+14 more)

### Community 4 - "Appointment"
Cohesion: 0.12
Nodes (6): AppointmentSerializer, Meta, AppointmentStatusSerializer, Meta, AppointmentViewSet, _name()

### Community 5 - "script.js"
Cohesion: 0.20
Nodes (22): Student Dashboard screenshot (Welcome, Student) with frosted-glass cards over blurred campus building background, Book Appointment form (professor select, time slot datetime, Submit), Cabin Locator section (professor name input + Find Cabin button), Notifications section (empty), Professor Availability table (Professor Ashish: Free), actionButton(), api(), el() (+14 more)

### Community 6 - "PageTests"
Cohesion: 0.13
Nodes (9): make_user(), PageTests, login_view(), Username and Password fields with icons, EduAccess logo and title branding, Frosted-glass login card over blurred campus background, Teal Login button, EduAccess Login Page Screenshot (+1 more)

### Community 7 - "MeSerializer"
Cohesion: 0.25
Nodes (3): MeSerializer, Meta, MeView

### Community 10 - "tests.py"
Cohesion: 0.12
Nodes (5): AppointmentAccessTests, BaseTestCase, MeTests, NotificationTests, ProfessorDirectoryTests

### Community 16 - "EduAccess"
Cohesion: 0.33
Nodes (5): API, Commits, EduAccess, graphify, Running locally

### Community 20 - "tests.py"
Cohesion: 0.14
Nodes (8): CustomUserAdmin, Appointment, CustomUser, Notification, Layout, Professor Dashboard screenshot (EduAccess), Update Availability radio group (Free/Busy/Unavailable), Manage Appointments table (Student, Time, Action columns; empty)

### Community 23 - "api/urls.py"
Cohesion: 0.29
Nodes (3): NotificationSerializer, Meta, NotificationViewSet

### Community 24 - "ProfessorSerializer"
Cohesion: 0.29
Nodes (3): ProfessorSerializer, Meta, ProfessorViewSet

## Knowledge Gaps
- **10 isolated node(s):** `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Django`, `gunicorn + whitenoise (deployment)`, `psycopg2 (PostgreSQL driver)` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 103 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `tests.py` to `EduAccess`, `eduaccess_backend/urls.py`, `script.js`, `permissions.py`?**
  _High betweenness centrality (0.312) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `AppointmentViewSet` (e.g. with `IsAppointmentParticipant` and `AppointmentSerializer`) actually correct?**
  _`AppointmentViewSet` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Django` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CustomUser` be split into smaller, more focused modules?**
  _Cohesion score 0.1323529411764706 - nodes in this community are weakly interconnected._
- **Why does `api()` connect `script.js` to `tests.py`?**
  _High betweenness centrality (0.270) - this node is a cross-community bridge._
- **Should `Frontend Templates & Flows` be split into smaller, more focused modules?**
  _Cohesion score 0.11333333333333333 - nodes in this community are weakly interconnected._
- **Why does `CustomUser` connect `tests.py` to `CustomUser`, `views.py`?**
  _High betweenness centrality (0.157) - this node is a cross-community bridge._