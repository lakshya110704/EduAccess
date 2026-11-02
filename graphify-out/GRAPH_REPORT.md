# Graph Report - EduAccess  (2026-11-02)

## Corpus Check
- 38 files · ~298,386 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 6, .example 2, .css 2)

## Summary
- 471 nodes · 798 edges · 42 communities (17 shown, 25 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 78 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3cb9b9c1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Layout
- biome.json
- Frontend Templates & Flows
- Project Config & Entrypoints
- SignupTests
- script.js
- PageTests
- CustomUser
- App Config
- Brand Logo
- BookingRuleTests
- Background Image
- signup.js
- deploy.sh
- package.json
- login_view
- entrypoint.sh
- CustomUser
- Appointment
- role-switch.js
- permissions.py
- .as_user
- views.py
- ProfessorViewSet
- DashboardLayoutTests
- SignupForm
- MeSerializer
- admin.py
- tests.py
- models.py
- 0007_appointment_slots.py
- parse_cabin
- eduaccess_backend/urls.py
- seed_demo.py
- AdminSeparationTests
- Professor Dashboard screenshot (EduAccess)

## God Nodes (most connected - your core abstractions)
1. `CustomUser` - 26 edges
2. `BaseTestCase` - 20 edges
3. `Appointment` - 18 edges
4. `Notification` - 16 edges
5. `PageTests` - 15 edges
6. `SignupTests` - 14 edges
7. `api()` - 14 edges
8. `BookingTests` - 13 edges
9. `AppointmentAccessTests` - 13 edges
10. `BookingRuleTests` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Update Availability radio group (Free/Busy/Unavailable)` --shares_data_with--> `CustomUser`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Manage Appointments table (Student, Time, Action columns; empty)` --shares_data_with--> `Appointment`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Layout` --references--> `SignupForm`  [INFERRED]
  CLAUDE.md → api/forms.py
- `Layout` --references--> `Appointment`  [INFERRED]
  CLAUDE.md → api/models.py
- `Layout` --references--> `CustomUser`  [INFERRED]
  CLAUDE.md → api/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Student Dashboard Features** — frontend_templates_student_dashboard_availability_section, frontend_templates_student_dashboard_locator_section, frontend_templates_student_dashboard_appointment_section, frontend_templates_student_dashboard_notifications_section [EXTRACTED 1.00]
- **Role-Based UI Templates** — frontend_templates_login, frontend_templates_student_dashboard, frontend_templates_professor_dashboard [INFERRED 0.85]

## Communities (42 total, 25 thin omitted)

### Community 0 - "Layout"
Cohesion: 0.22
Nodes (6): IsAppointmentParticipant, role_required(), decorator(), professor_dashboard(), student_dashboard(), Layout

### Community 1 - "biome.json"
Cohesion: 0.12
Nodes (15): files, includes, formatter, enabled, indentStyle, indentWidth, lineWidth, quoteStyle (+7 more)

### Community 2 - "Frontend Templates & Flows"
Cohesion: 0.11
Nodes (22): Login Page, Login Form (username, password, role), Professor Dashboard Page, Manage Appointments Table, Update Availability Section, Student Dashboard Page, Book Appointment Section, Professor Availability Table (+14 more)

### Community 3 - "Project Config & Entrypoints"
Cohesion: 0.09
Nodes (10): Admin site, CI, Commits, Dependencies, Deployment (homelab), EduAccess, graphify, Linting and formatting (+2 more)

### Community 5 - "script.js"
Cohesion: 0.15
Nodes (35): Student Dashboard screenshot (Welcome, Student) with frosted-glass cards over blurred campus building background, Book Appointment form (professor select, time slot datetime, Submit), Cabin Locator section (professor name input + Find Cabin button), Notifications section (empty), Professor Availability table (Professor Ashish: Free), actionButton(), addOpenTime(), api() (+27 more)

### Community 7 - "CustomUser"
Cohesion: 0.09
Nodes (9): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+1 more)

### Community 15 - "signup.js"
Cohesion: 0.40
Nodes (3): collegeId, email, form

### Community 17 - "package.json"
Cohesion: 0.20
Nodes (9): description, devDependencies, @biomejs/biome, name, private, scripts, format, lint (+1 more)

### Community 20 - "login_view"
Cohesion: 0.22
Nodes (8): login_view(), _wrong_role_message(), Username and Password fields with icons, EduAccess logo and title branding, Frosted-glass login card over blurred campus background, Teal Login button, EduAccess Login Page Screenshot, Select Role dropdown

### Community 22 - "CustomUser"
Cohesion: 0.32
Nodes (4): CustomUser, Meta, format_cabin(), Accounts and sign-up

### Community 23 - "Appointment"
Cohesion: 0.06
Nodes (17): Appointment, OpenTime, Meta, AppointmentSerializer, Meta, AppointmentStatusSerializer, Meta, _check_quarter_hour() (+9 more)

### Community 24 - "role-switch.js"
Cohesion: 0.33
Nodes (3): ICONS, radios, serverChoseRole

### Community 26 - ".as_user"
Cohesion: 0.07
Nodes (8): AdminUserCreationTests, AppointmentAccessTests, BaseTestCase, MeTests, MyProfessorTests, NotificationTests, OpenTimeTests, ProfessorDirectoryTests

### Community 27 - "views.py"
Cohesion: 0.15
Nodes (4): Notification, NotificationSerializer, Meta, NotificationViewSet

### Community 30 - "SignupForm"
Cohesion: 0.17
Nodes (3): SignupForm, Meta, signup_view()

### Community 31 - "MeSerializer"
Cohesion: 0.18
Nodes (3): MeSerializer, Meta, MeView

### Community 40 - "Professor Dashboard screenshot (EduAccess)"
Cohesion: 0.50
Nodes (3): Professor Dashboard screenshot (EduAccess), Update Availability radio group (Free/Busy/Unavailable), Manage Appointments table (Student, Time, Action columns; empty)

## Knowledge Gaps
- **11 isolated node(s):** `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Django`, `gunicorn + whitenoise (deployment)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 189 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `Layout` to `Project Config & Entrypoints`, `script.js`, `CustomUser`, `Appointment`, `views.py`, `SignupForm`?**
  _High betweenness centrality (0.244) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `CustomUser` (e.g. with `CustomUserAdmin` and `SignupForm`) actually correct?**
  _`CustomUser` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `biome.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Why does `api()` connect `script.js` to `Layout`?**
  _High betweenness centrality (0.195) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Appointment` (e.g. with `AppointmentSerializer` and `AppointmentStatusSerializer`) actually correct?**
  _`Appointment` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `Frontend Templates & Flows` be split into smaller, more focused modules?**
  _Cohesion score 0.11333333333333333 - nodes in this community are weakly interconnected._