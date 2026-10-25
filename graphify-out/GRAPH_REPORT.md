# Graph Report - EduAccess  (2026-10-25)

## Corpus Check
- 30 files · ~293,063 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 6, .example 2, .in 2)

## Summary
- 296 nodes · 437 edges · 21 communities (11 shown, 10 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 38 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `58e18fea`
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
- deploy.sh
- package.json
- CustomUser
- entrypoint.sh

## God Nodes (most connected - your core abstractions)
1. `CustomUser` - 14 edges
2. `BaseTestCase` - 12 edges
3. `AppointmentAccessTests` - 12 edges
4. `PageTests` - 12 edges
5. `Appointment` - 11 edges
6. `api()` - 11 edges
7. `BookingTests` - 10 edges
8. `Notification` - 10 edges
9. `AppointmentSerializer` - 10 edges
10. `AppointmentViewSet` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Manage Appointments table (Student, Time, Action columns; empty)` --shares_data_with--> `Appointment`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Update Availability radio group (Free/Busy/Unavailable)` --shares_data_with--> `CustomUser`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Layout` --references--> `role_required()`  [INFERRED]
  CLAUDE.md → api/permissions.py
- `Layout` --references--> `api()`  [INFERRED]
  CLAUDE.md → frontend/static/script.js
- `Teal Login button` --shares_data_with--> `login_view()`  [INFERRED]
  frontend/static/assets/login.png → api/views.py

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

### Community 3 - "Project Config & Entrypoints"
Cohesion: 0.09
Nodes (10): API, CI, Commits, Dependencies, Deployment (homelab), EduAccess, graphify, Linting and formatting (+2 more)

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
Cohesion: 0.08
Nodes (8): AdminUserCreationTests, AppointmentAccessTests, BaseTestCase, BookingTests, make_user(), MeTests, NotificationTests, ProfessorDirectoryTests

### Community 17 - "package.json"
Cohesion: 0.20
Nodes (9): description, devDependencies, @biomejs/biome, name, private, scripts, format, lint (+1 more)

### Community 20 - "CustomUser"
Cohesion: 0.07
Nodes (18): CustomUserAdmin, Command, Appointment, CustomUser, Notification, IsAppointmentParticipant, AppointmentStatusSerializer, Meta (+10 more)

## Knowledge Gaps
- **11 isolated node(s):** `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Django`, `gunicorn + whitenoise (deployment)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 128 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `CustomUser` to `views.py`, `Project Config & Entrypoints`, `script.js`?**
  _High betweenness centrality (0.323) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `CustomUser` (e.g. with `Command` and `MeSerializer`) actually correct?**
  _`CustomUser` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `views.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06341463414634146 - nodes in this community are weakly interconnected._
- **Why does `api()` connect `script.js` to `CustomUser`?**
  _High betweenness centrality (0.224) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Appointment` (e.g. with `AppointmentSerializer` and `AppointmentStatusSerializer`) actually correct?**
  _`Appointment` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `biome.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._