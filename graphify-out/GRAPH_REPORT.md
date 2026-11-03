# Graph Report - EduAccess  (2026-11-02)

## Corpus Check
- 40 files · ~299,501 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 6, .example 2, .css 2)

## Summary
- 505 nodes · 835 edges · 34 communities (17 shown, 17 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 65 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `430da4da`
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
- OpenTimeViewSet
- entrypoint.sh
- login_view
- Appointment
- role-switch.js
- permissions.py
- .as_user
- ProfessorViewSet
- SignupForm
- go.js
- CustomUser

## God Nodes (most connected - your core abstractions)
1. `CustomUser` - 23 edges
2. `BaseTestCase` - 20 edges
3. `PageTests` - 15 edges
4. `Appointment` - 15 edges
5. `api()` - 14 edges
6. `SignupTests` - 13 edges
7. `loadProfessors()` - 13 edges
8. `AppointmentAccessTests` - 12 edges
9. `OpenTimeTests` - 12 edges
10. `el()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Manage Appointments table (Student, Time, Action columns; empty)` --shares_data_with--> `Appointment`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Layout` --references--> `api()`  [INFERRED]
  CLAUDE.md → frontend/static/script.js
- `Layout` --references--> `Appointment`  [INFERRED]
  CLAUDE.md → api/models.py
- `API` --references--> `OpenTime`  [INFERRED]
  CLAUDE.md → api/models.py
- `Layout` --references--> `SignupForm`  [INFERRED]
  CLAUDE.md → api/forms.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Student Dashboard Features** — frontend_templates_student_dashboard_availability_section, frontend_templates_student_dashboard_locator_section, frontend_templates_student_dashboard_appointment_section, frontend_templates_student_dashboard_notifications_section [EXTRACTED 1.00]
- **Role-Based UI Templates** — frontend_templates_login, frontend_templates_student_dashboard, frontend_templates_professor_dashboard [INFERRED 0.85]

## Communities (34 total, 17 thin omitted)

### Community 0 - "eduaccess_backend/urls.py"
Cohesion: 0.18
Nodes (6): role_required(), decorator(), logout_view(), professor_dashboard(), signup_done(), student_dashboard()

### Community 1 - "biome.json"
Cohesion: 0.12
Nodes (15): files, includes, formatter, enabled, indentStyle, indentWidth, lineWidth, quoteStyle (+7 more)

### Community 2 - "Frontend Templates & Flows"
Cohesion: 0.11
Nodes (22): Login Page, Login Form (username, password, role), Professor Dashboard Page, Manage Appointments Table, Update Availability Section, Student Dashboard Page, Book Appointment Section, Professor Availability Table (+14 more)

### Community 3 - "Project Config & Entrypoints"
Cohesion: 0.07
Nodes (13): MyProfessor, Meta, Admin site, API, CI, Commits, Dependencies, Deployment (homelab) (+5 more)

### Community 5 - "script.js"
Cohesion: 0.15
Nodes (36): Student Dashboard screenshot (Welcome, Student) with frosted-glass cards over blurred campus building background, Book Appointment form (professor select, time slot datetime, Submit), Cabin Locator section (professor name input + Find Cabin button), Notifications section (empty), Professor Availability table (Professor Ashish: Free), actionButton(), addOpenTime(), api() (+28 more)

### Community 6 - "PageTests"
Cohesion: 0.15
Nodes (3): CabinLocationTests, make_user(), PageTests

### Community 7 - "CustomUser"
Cohesion: 0.07
Nodes (11): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+3 more)

### Community 10 - "tests.py"
Cohesion: 0.05
Nodes (9): AdminSeparationTests, AdminUserCreationTests, BaseTestCase, BookingRuleTests, BookingTests, DashboardLayoutTests, DirectionsTests, NotificationTests (+1 more)

### Community 15 - "signup.js"
Cohesion: 0.40
Nodes (3): collegeId, email, form

### Community 17 - "package.json"
Cohesion: 0.20
Nodes (9): description, devDependencies, @biomejs/biome, name, private, scripts, format, lint (+1 more)

### Community 22 - "login_view"
Cohesion: 0.22
Nodes (8): login_view(), _wrong_role_message(), Username and Password fields with icons, EduAccess logo and title branding, Frosted-glass login card over blurred campus background, Teal Login button, EduAccess Login Page Screenshot, Select Role dropdown

### Community 23 - "Appointment"
Cohesion: 0.05
Nodes (20): Appointment, OpenTime, Meta, AppointmentSerializer, Meta, AppointmentStatusSerializer, Meta, _check_quarter_hour() (+12 more)

### Community 24 - "role-switch.js"
Cohesion: 0.33
Nodes (3): ICONS, radios, serverChoseRole

### Community 25 - "permissions.py"
Cohesion: 0.22
Nodes (3): dashboard_for(), IsAppointmentParticipant, Layout

### Community 26 - ".as_user"
Cohesion: 0.09
Nodes (5): AppointmentAccessTests, MeTests, MyProfessorTests, OpenTimeTests, ProfessorDirectoryTests

### Community 30 - "SignupForm"
Cohesion: 0.17
Nodes (3): SignupForm, Meta, signup_view()

### Community 38 - "CustomUser"
Cohesion: 0.05
Nodes (18): AcademicBlockAdmin, CustomUserAdmin, FacultyBlockInline, Command, AcademicBlock, Meta, CustomUser, Meta (+10 more)

## Knowledge Gaps
- **11 isolated node(s):** `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Django`, `gunicorn + whitenoise (deployment)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 210 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `permissions.py` to `eduaccess_backend/urls.py`, `Project Config & Entrypoints`, `script.js`, `CustomUser`, `Appointment`, `SignupForm`?**
  _High betweenness centrality (0.220) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `CustomUser` (e.g. with `CustomUserAdmin` and `SignupForm`) actually correct?**
  _`CustomUser` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `biome.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Why does `api()` connect `script.js` to `permissions.py`?**
  _High betweenness centrality (0.188) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Appointment` (e.g. with `AppointmentSerializer` and `AppointmentStatusSerializer`) actually correct?**
  _`Appointment` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Should `Frontend Templates & Flows` be split into smaller, more focused modules?**
  _Cohesion score 0.11333333333333333 - nodes in this community are weakly interconnected._