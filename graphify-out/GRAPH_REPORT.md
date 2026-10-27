# Graph Report - EduAccess  (2026-10-27)

## Corpus Check
- 34 files · ~295,322 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 6, .example 2, .css 2)

## Summary
- 358 nodes · 521 edges · 31 communities (16 shown, 15 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 39 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dbc128cc`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- eduaccess_backend/urls.py
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
- models.py
- entrypoint.sh
- CustomUser
- AppointmentSerializer
- role-switch.js
- SignupForm
- MeSerializer
- Appointment
- CustomUserAdmin
- AppointmentStatusSerializer
- ProfessorSerializer

## God Nodes (most connected - your core abstractions)
1. `CustomUser` - 18 edges
2. `PageTests` - 15 edges
3. `BaseTestCase` - 14 edges
4. `SignupTests` - 13 edges
5. `EduAccess` - 12 edges
6. `AppointmentAccessTests` - 12 edges
7. `SignupForm` - 12 edges
8. `api()` - 11 edges
9. `BookingTests` - 10 edges
10. `Appointment` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Update Availability radio group (Free/Busy/Unavailable)` --shares_data_with--> `CustomUser`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Layout` --references--> `SignupForm`  [INFERRED]
  CLAUDE.md → api/forms.py
- `Layout` --references--> `CustomUser`  [INFERRED]
  CLAUDE.md → api/models.py
- `Layout` --references--> `Notification`  [INFERRED]
  CLAUDE.md → api/models.py
- `Layout` --references--> `role_required()`  [INFERRED]
  CLAUDE.md → api/permissions.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Student Dashboard Features** — frontend_templates_student_dashboard_availability_section, frontend_templates_student_dashboard_locator_section, frontend_templates_student_dashboard_appointment_section, frontend_templates_student_dashboard_notifications_section [EXTRACTED 1.00]
- **Role-Based UI Templates** — frontend_templates_login, frontend_templates_student_dashboard, frontend_templates_professor_dashboard [INFERRED 0.85]

## Communities (31 total, 15 thin omitted)

### Community 0 - "eduaccess_backend/urls.py"
Cohesion: 0.13
Nodes (6): role_required(), decorator(), logout_view(), professor_dashboard(), signup_done(), student_dashboard()

### Community 1 - "biome.json"
Cohesion: 0.12
Nodes (15): files, includes, formatter, enabled, indentStyle, indentWidth, lineWidth, quoteStyle (+7 more)

### Community 2 - "Frontend Templates & Flows"
Cohesion: 0.11
Nodes (22): Login Page, Login Form (username, password, role), Professor Dashboard Page, Manage Appointments Table, Update Availability Section, Student Dashboard Page, Book Appointment Section, Professor Availability Table (+14 more)

### Community 3 - "Project Config & Entrypoints"
Cohesion: 0.09
Nodes (11): Admin site, API, CI, Commits, Dependencies, Deployment (homelab), EduAccess, graphify (+3 more)

### Community 5 - "script.js"
Cohesion: 0.20
Nodes (22): Student Dashboard screenshot (Welcome, Student) with frosted-glass cards over blurred campus building background, Book Appointment form (professor select, time slot datetime, Submit), Cabin Locator section (professor name input + Find Cabin button), Notifications section (empty), Professor Availability table (Professor Ashish: Free), actionButton(), api(), el() (+14 more)

### Community 6 - "PageTests"
Cohesion: 0.11
Nodes (9): PageTests, login_view(), _wrong_role_message(), Username and Password fields with icons, EduAccess logo and title branding, Frosted-glass login card over blurred campus background, Teal Login button, EduAccess Login Page Screenshot (+1 more)

### Community 7 - "CustomUser"
Cohesion: 0.09
Nodes (6): Command, Migration, Migration, Migration, Migration, Migration

### Community 10 - "tests.py"
Cohesion: 0.06
Nodes (10): AdminSeparationTests, AdminUserCreationTests, AppointmentAccessTests, BaseTestCase, BookingTests, make_user(), MeTests, NotificationTests (+2 more)

### Community 15 - "signup.js"
Cohesion: 0.40
Nodes (3): collegeId, email, form

### Community 17 - "package.json"
Cohesion: 0.20
Nodes (9): description, devDependencies, @biomejs/biome, name, private, scripts, format, lint (+1 more)

### Community 20 - "models.py"
Cohesion: 0.21
Nodes (3): Notification, NotificationSerializer, Meta

### Community 22 - "CustomUser"
Cohesion: 0.25
Nodes (3): CustomUser, Meta, Accounts and sign-up

### Community 23 - "AppointmentSerializer"
Cohesion: 0.08
Nodes (7): AppointmentSerializer, Meta, AppointmentViewSet, MeView, _name(), NotificationViewSet, ProfessorViewSet

### Community 24 - "role-switch.js"
Cohesion: 0.33
Nodes (3): ICONS, radios, serverChoseRole

### Community 25 - "SignupForm"
Cohesion: 0.10
Nodes (4): SignupForm, Meta, dashboard_for(), signup_view()

### Community 27 - "Appointment"
Cohesion: 0.22
Nodes (6): Appointment, IsAppointmentParticipant, Layout, Professor Dashboard screenshot (EduAccess), Update Availability radio group (Free/Busy/Unavailable), Manage Appointments table (Student, Time, Action columns; empty)

## Knowledge Gaps
- **11 isolated node(s):** `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Django`, `gunicorn + whitenoise (deployment)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 163 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `Appointment` to `eduaccess_backend/urls.py`, `Project Config & Entrypoints`, `script.js`, `models.py`, `CustomUser`, `SignupForm`?**
  _High betweenness centrality (0.265) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `CustomUser` (e.g. with `SignupForm` and `Command`) actually correct?**
  _`CustomUser` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `eduaccess_backend/urls.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13157894736842105 - nodes in this community are weakly interconnected._
- **Why does `api()` connect `script.js` to `Appointment`?**
  _High betweenness centrality (0.192) - this node is a cross-community bridge._
- **Should `biome.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Why does `CustomUser` connect `CustomUser` to `eduaccess_backend/urls.py`, `CustomUser`, `tests.py`, `models.py`, `SignupForm`, `MeSerializer`, `Appointment`, `ProfessorSerializer`?**
  _High betweenness centrality (0.168) - this node is a cross-community bridge._