# Graph Report - EduAccess  (2026-10-25)

## Corpus Check
- 28 files · ~292,219 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 4, .in 2, .example 1)

## Summary
- 286 nodes · 432 edges · 21 communities (11 shown, 10 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 44 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0fb5a979`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- views.py
- biome.json
- Frontend Templates & Flows
- Project Config & Entrypoints
- Appointment
- script.js
- PageTests
- django_db
- App Config
- Brand Logo
- tests.py
- Background Image
- BookingTests
- EduAccess
- package.json
- CustomUser

## God Nodes (most connected - your core abstractions)
1. `CustomUser` - 16 edges
2. `Appointment` - 13 edges
3. `Notification` - 13 edges
4. `AppointmentAccessTests` - 13 edges
5. `BaseTestCase` - 12 edges
6. `BookingTests` - 12 edges
7. `PageTests` - 12 edges
8. `api()` - 11 edges
9. `AppointmentViewSet` - 10 edges
10. `loadAppointments()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Update Availability radio group (Free/Busy/Unavailable)` --shares_data_with--> `CustomUser`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Manage Appointments table (Student, Time, Action columns; empty)` --shares_data_with--> `Appointment`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Teal Login button` --shares_data_with--> `login_view()`  [INFERRED]
  frontend/static/assets/login.png → api/views.py
- `Select Role dropdown` --shares_data_with--> `login_view()`  [INFERRED]
  frontend/static/assets/login.png → api/views.py
- `Layout` --references--> `api()`  [INFERRED]
  CLAUDE.md → frontend/static/script.js

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Student Dashboard Features** — frontend_templates_student_dashboard_availability_section, frontend_templates_student_dashboard_locator_section, frontend_templates_student_dashboard_appointment_section, frontend_templates_student_dashboard_notifications_section [EXTRACTED 1.00]
- **Role-Based UI Templates** — frontend_templates_login, frontend_templates_student_dashboard, frontend_templates_professor_dashboard [INFERRED 0.85]

## Communities (21 total, 10 thin omitted)

### Community 0 - "views.py"
Cohesion: 0.06
Nodes (9): dashboard_for(), role_required(), decorator(), logout_view(), MeView, NotificationViewSet, professor_dashboard(), ProfessorViewSet (+1 more)

### Community 1 - "biome.json"
Cohesion: 0.12
Nodes (15): files, includes, formatter, enabled, indentStyle, indentWidth, lineWidth, quoteStyle (+7 more)

### Community 2 - "Frontend Templates & Flows"
Cohesion: 0.11
Nodes (22): Login Page, Login Form (username, password, role), Professor Dashboard Page, Manage Appointments Table, Update Availability Section, Student Dashboard Page, Book Appointment Section, Professor Availability Table (+14 more)

### Community 4 - "Appointment"
Cohesion: 0.14
Nodes (4): AppointmentSerializer, Meta, AppointmentViewSet, _name()

### Community 5 - "script.js"
Cohesion: 0.20
Nodes (22): Student Dashboard screenshot (Welcome, Student) with frosted-glass cards over blurred campus building background, Book Appointment form (professor select, time slot datetime, Submit), Cabin Locator section (professor name input + Find Cabin button), Notifications section (empty), Professor Availability table (Professor Ashish: Free), actionButton(), api(), el() (+14 more)

### Community 6 - "PageTests"
Cohesion: 0.13
Nodes (8): PageTests, login_view(), Username and Password fields with icons, EduAccess logo and title branding, Frosted-glass login card over blurred campus background, Teal Login button, EduAccess Login Page Screenshot, Select Role dropdown

### Community 7 - "django_db"
Cohesion: 0.15
Nodes (4): Migration, Migration, Migration, Migration

### Community 10 - "tests.py"
Cohesion: 0.10
Nodes (6): AppointmentAccessTests, BaseTestCase, make_user(), MeTests, NotificationTests, ProfessorDirectoryTests

### Community 16 - "EduAccess"
Cohesion: 0.22
Nodes (8): API, CI, Commits, Dependencies, EduAccess, graphify, Linting and formatting, Running locally

### Community 17 - "package.json"
Cohesion: 0.20
Nodes (9): description, devDependencies, @biomejs/biome, name, private, scripts, format, lint (+1 more)

### Community 20 - "CustomUser"
Cohesion: 0.07
Nodes (18): CustomUserAdmin, Command, Appointment, CustomUser, Notification, IsAppointmentParticipant, AppointmentStatusSerializer, Meta (+10 more)

## Knowledge Gaps
- **11 isolated node(s):** `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Django`, `gunicorn + whitenoise (deployment)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 124 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `CustomUser` to `EduAccess`, `views.py`, `script.js`?**
  _High betweenness centrality (0.267) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `CustomUser` (e.g. with `CustomUserAdmin` and `Command`) actually correct?**
  _`CustomUser` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `views.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06341463414634146 - nodes in this community are weakly interconnected._
- **Why does `api()` connect `script.js` to `CustomUser`?**
  _High betweenness centrality (0.220) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Appointment` (e.g. with `AppointmentSerializer` and `AppointmentStatusSerializer`) actually correct?**
  _`Appointment` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Should `biome.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._