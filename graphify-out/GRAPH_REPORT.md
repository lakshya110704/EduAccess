# Graph Report - EduAccess  (2026-10-25)

## Corpus Check
- 33 files · ~294,439 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 6, .example 2, .in 2)

## Summary
- 338 nodes · 512 edges · 24 communities (11 shown, 13 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 54 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `be970fae`
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
- CustomUserAdmin

## God Nodes (most connected - your core abstractions)
1. `CustomUser` - 24 edges
2. `SignupTests` - 14 edges
3. `Appointment` - 13 edges
4. `Notification` - 13 edges
5. `BaseTestCase` - 13 edges
6. `AppointmentAccessTests` - 13 edges
7. `SignupForm` - 12 edges
8. `BookingTests` - 12 edges
9. `PageTests` - 12 edges
10. `EduAccess` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Manage Appointments table (Student, Time, Action columns; empty)` --shares_data_with--> `Appointment`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Layout` --references--> `Appointment`  [INFERRED]
  CLAUDE.md → api/models.py
- `Layout` --references--> `CustomUser`  [INFERRED]
  CLAUDE.md → api/models.py
- `Layout` --references--> `api()`  [INFERRED]
  CLAUDE.md → frontend/static/script.js
- `Update Availability radio group (Free/Busy/Unavailable)` --shares_data_with--> `CustomUser`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Student Dashboard Features** — frontend_templates_student_dashboard_availability_section, frontend_templates_student_dashboard_locator_section, frontend_templates_student_dashboard_appointment_section, frontend_templates_student_dashboard_notifications_section [EXTRACTED 1.00]
- **Role-Based UI Templates** — frontend_templates_login, frontend_templates_student_dashboard, frontend_templates_professor_dashboard [INFERRED 0.85]

## Communities (24 total, 13 thin omitted)

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
Cohesion: 0.13
Nodes (9): make_user(), PageTests, login_view(), Username and Password fields with icons, EduAccess logo and title branding, Frosted-glass login card over blurred campus background, Teal Login button, EduAccess Login Page Screenshot (+1 more)

### Community 7 - "CustomUser"
Cohesion: 0.06
Nodes (12): Command, Migration, Migration, Migration, Migration, Migration, CustomUser, Meta (+4 more)

### Community 10 - "tests.py"
Cohesion: 0.08
Nodes (7): AdminUserCreationTests, AppointmentAccessTests, BaseTestCase, BookingTests, MeTests, NotificationTests, ProfessorDirectoryTests

### Community 15 - "signup.js"
Cohesion: 0.33
Nodes (4): collegeId, email, form, role

### Community 17 - "package.json"
Cohesion: 0.20
Nodes (9): description, devDependencies, @biomejs/biome, name, private, scripts, format, lint (+1 more)

### Community 20 - "Appointment"
Cohesion: 0.07
Nodes (11): Appointment, AppointmentSerializer, Meta, AppointmentStatusSerializer, Meta, MeSerializer, Meta, ProfessorSerializer (+3 more)

## Knowledge Gaps
- **11 isolated node(s):** `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Django`, `gunicorn + whitenoise (deployment)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 148 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `views.py` to `Project Config & Entrypoints`, `Appointment`, `script.js`, `CustomUser`?**
  _High betweenness centrality (0.278) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `CustomUser` (e.g. with `CustomUserAdmin` and `SignupForm`) actually correct?**
  _`CustomUser` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `views.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05075187969924812 - nodes in this community are weakly interconnected._
- **Why does `CustomUser` connect `CustomUser` to `views.py`, `SignupTests`, `PageTests`, `tests.py`, `Appointment`, `CustomUserAdmin`?**
  _High betweenness centrality (0.209) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Appointment` (e.g. with `AppointmentSerializer` and `AppointmentStatusSerializer`) actually correct?**
  _`Appointment` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Should `biome.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._