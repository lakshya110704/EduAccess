# Graph Report - EduAccess  (2026-10-25)

## Corpus Check
- 33 files · ~294,755 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 6, .example 2, .in 2)

## Summary
- 343 nodes · 506 edges · 24 communities (12 shown, 12 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 41 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `992b5755`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- views.py
- biome.json
- Frontend Templates & Flows
- Project Config & Entrypoints
- SignupTests
- script.js
- PageTests
- CustomUser
- App Config
- Brand Logo
- tests.py
- Background Image
- signup.js
- deploy.sh
- package.json
- Appointment
- entrypoint.sh
- AppointmentSerializer

## God Nodes (most connected - your core abstractions)
1. `CustomUser` - 19 edges
2. `PageTests` - 15 edges
3. `SignupTests` - 13 edges
4. `BaseTestCase` - 12 edges
5. `AppointmentAccessTests` - 12 edges
6. `SignupForm` - 12 edges
7. `EduAccess` - 11 edges
8. `api()` - 11 edges
9. `BookingTests` - 10 edges
10. `Appointment` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Layout` --references--> `Appointment`  [INFERRED]
  CLAUDE.md → api/models.py
- `Layout` --references--> `CustomUser`  [INFERRED]
  CLAUDE.md → api/models.py
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

## Communities (24 total, 12 thin omitted)

### Community 0 - "views.py"
Cohesion: 0.05
Nodes (18): SignupForm, Meta, Notification, dashboard_for(), IsAppointmentParticipant, role_required(), decorator(), NotificationSerializer (+10 more)

### Community 1 - "biome.json"
Cohesion: 0.12
Nodes (15): files, includes, formatter, enabled, indentStyle, indentWidth, lineWidth, quoteStyle (+7 more)

### Community 2 - "Frontend Templates & Flows"
Cohesion: 0.11
Nodes (22): Login Page, Login Form (username, password, role), Professor Dashboard Page, Manage Appointments Table, Update Availability Section, Student Dashboard Page, Book Appointment Section, Professor Availability Table (+14 more)

### Community 3 - "Project Config & Entrypoints"
Cohesion: 0.09
Nodes (10): API, CI, Commits, Dependencies, Deployment (homelab), EduAccess, graphify, Linting and formatting (+2 more)

### Community 5 - "script.js"
Cohesion: 0.20
Nodes (22): Student Dashboard screenshot (Welcome, Student) with frosted-glass cards over blurred campus building background, Book Appointment form (professor select, time slot datetime, Submit), Cabin Locator section (professor name input + Find Cabin button), Notifications section (empty), Professor Availability table (Professor Ashish: Free), actionButton(), api(), el() (+14 more)

### Community 6 - "PageTests"
Cohesion: 0.11
Nodes (9): PageTests, login_view(), _wrong_role_message(), Username and Password fields with icons, EduAccess logo and title branding, Frosted-glass login card over blurred campus background, Teal Login button, EduAccess Login Page Screenshot (+1 more)

### Community 7 - "CustomUser"
Cohesion: 0.08
Nodes (6): Command, Migration, Migration, Migration, Migration, Migration

### Community 10 - "tests.py"
Cohesion: 0.08
Nodes (8): AdminUserCreationTests, AppointmentAccessTests, BaseTestCase, BookingTests, make_user(), MeTests, NotificationTests, ProfessorDirectoryTests

### Community 15 - "signup.js"
Cohesion: 0.33
Nodes (4): collegeId, email, form, role

### Community 17 - "package.json"
Cohesion: 0.20
Nodes (9): description, devDependencies, @biomejs/biome, name, private, scripts, format, lint (+1 more)

### Community 20 - "Appointment"
Cohesion: 0.08
Nodes (14): CustomUserAdmin, Appointment, CustomUser, Meta, AppointmentStatusSerializer, Meta, MeSerializer, Meta (+6 more)

### Community 23 - "AppointmentSerializer"
Cohesion: 0.14
Nodes (4): AppointmentSerializer, Meta, AppointmentViewSet, _name()

## Knowledge Gaps
- **11 isolated node(s):** `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Django`, `gunicorn + whitenoise (deployment)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 151 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `views.py` to `Project Config & Entrypoints`, `Appointment`, `script.js`?**
  _High betweenness centrality (0.274) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `CustomUser` (e.g. with `CustomUserAdmin` and `SignupForm`) actually correct?**
  _`CustomUser` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `views.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05012531328320802 - nodes in this community are weakly interconnected._
- **Why does `api()` connect `script.js` to `views.py`?**
  _High betweenness centrality (0.201) - this node is a cross-community bridge._
- **Should `biome.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Why does `CustomUser` connect `Appointment` to `views.py`, `tests.py`, `CustomUser`?**
  _High betweenness centrality (0.182) - this node is a cross-community bridge._