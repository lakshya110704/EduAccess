# Graph Report - EduAccess  (2026-11-04)

## Corpus Check
- 43 files · ~301,496 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: (none) 7, .example 2, .css 2)

## Summary
- 552 nodes · 962 edges · 50 communities (25 shown, 25 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 103 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e4653efe`
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
- django_conf
- App Config
- Brand Logo
- BaseTestCase
- Background Image
- signup.js
- deploy.sh
- package.json
- CabinGateTests
- entrypoint.sh
- SignupForm
- OpenTime
- role-switch.js
- Appointment
- .as_user
- tests.py
- ProfessorViewSet
- permissions.py
- 0009_structured_cabin.py
- go.js
- AcademicBlock
- models.py
- django_db
- OpenTimeViewSet
- CustomUserAdmin
- 0007_appointment_slots.py
- 0001_initial.py
- AcademicBlock
- seed_demo.py
- AdminSeparationTests
- CustomUser
- ThemeAndSwitchTests
- DirectionsTests
- AppointmentViewSet
- MeSerializer
- Appointment

## God Nodes (most connected - your core abstractions)
1. `CustomUser` - 29 edges
2. `BaseTestCase` - 23 edges
3. `Appointment` - 19 edges
4. `Notification` - 17 edges
5. `FacultyBlock` - 16 edges
6. `CabinGateTests` - 16 edges
7. `PageTests` - 15 edges
8. `AppointmentViewSet` - 15 edges
9. `api()` - 15 edges
10. `AcademicBlock` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Update Availability radio group (Free/Busy/Unavailable)` --shares_data_with--> `CustomUser`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Manage Appointments table (Student, Time, Action columns; empty)` --shares_data_with--> `Appointment`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Layout` --references--> `SignupForm`  [INFERRED]
  CLAUDE.md → api/forms.py
- `Accounts and sign-up` --references--> `CabinForm`  [INFERRED]
  CLAUDE.md → api/forms.py
- `Layout` --references--> `CustomUser`  [INFERRED]
  CLAUDE.md → api/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Student Dashboard Features** — frontend_templates_student_dashboard_availability_section, frontend_templates_student_dashboard_locator_section, frontend_templates_student_dashboard_appointment_section, frontend_templates_student_dashboard_notifications_section [EXTRACTED 1.00]
- **Role-Based UI Templates** — frontend_templates_login, frontend_templates_student_dashboard, frontend_templates_professor_dashboard [INFERRED 0.85]

## Communities (50 total, 25 thin omitted)

### Community 0 - "views.py"
Cohesion: 0.11
Nodes (8): role_required(), decorator(), _cabin_form(), logout_view(), professor_cabin(), professor_dashboard(), signup_done(), student_dashboard()

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
Cohesion: 0.14
Nodes (39): Student Dashboard screenshot (Welcome, Student) with frosted-glass cards over blurred campus building background, Book Appointment form (professor select, time slot datetime, Submit), Cabin Locator section (professor name input + Find Cabin button), Notifications section (empty), Professor Availability table (Professor Ashish: Free), actionButton(), addOpenTime(), api() (+31 more)

### Community 6 - "PageTests"
Cohesion: 0.15
Nodes (3): CabinLocationTests, make_user(), PageTests

### Community 7 - "django_conf"
Cohesion: 0.21
Nodes (5): Migration, Migration, Migration, Migration, Migration

### Community 10 - "BaseTestCase"
Cohesion: 0.07
Nodes (6): AdminUserCreationTests, AppointmentReasonTests, BaseTestCase, BookingRuleTests, BookingTests, DashboardLayoutTests

### Community 15 - "signup.js"
Cohesion: 0.40
Nodes (3): collegeId, email, form

### Community 17 - "package.json"
Cohesion: 0.20
Nodes (9): description, devDependencies, @biomejs/biome, name, private, scripts, format, lint (+1 more)

### Community 22 - "SignupForm"
Cohesion: 0.10
Nodes (13): SignupForm, Meta, dashboard_for(), login_view(), fail(), signup_view(), _wrong_role_message(), Username and Password fields with icons (+5 more)

### Community 23 - "OpenTime"
Cohesion: 0.12
Nodes (7): OpenTime, Meta, AppointmentSerializer, Meta, _check_quarter_hour(), OpenTimeSerializer, Meta

### Community 24 - "role-switch.js"
Cohesion: 0.33
Nodes (3): ICONS, radios, serverChoseRole

### Community 25 - "Appointment"
Cohesion: 0.15
Nodes (6): Appointment, MyProfessor, Meta, AppointmentUpdateSerializer, Meta, API

### Community 26 - ".as_user"
Cohesion: 0.09
Nodes (5): AppointmentAccessTests, MeTests, MyProfessorTests, OpenTimeTests, ProfessorDirectoryTests

### Community 28 - "ProfessorViewSet"
Cohesion: 0.15
Nodes (4): ProfessorSerializer, Meta, professor_search(), ProfessorViewSet

### Community 29 - "permissions.py"
Cohesion: 0.20
Nodes (3): IsAppointmentParticipant, ProfessorHasCabin, Layout

### Community 32 - "AcademicBlock"
Cohesion: 0.17
Nodes (3): CabinForm, FacultyBlock, Meta

### Community 33 - "models.py"
Cohesion: 0.27
Nodes (4): Notification, NotificationSerializer, Meta, NotificationViewSet

### Community 34 - "django_db"
Cohesion: 0.18
Nodes (4): Migration, Migration, Migration, Migration

### Community 36 - "CustomUserAdmin"
Cohesion: 0.16
Nodes (4): AcademicBlockAdmin, AppointmentAdmin, CustomUserAdmin, FacultyBlockInline

### Community 42 - "CustomUser"
Cohesion: 0.17
Nodes (6): CustomUser, Meta, format_cabin(), parse_cabin(), go_view(), Accounts and sign-up

### Community 49 - "AppointmentViewSet"
Cohesion: 0.29
Nodes (4): AppointmentViewSet, _name(), _reason(), _when()

### Community 50 - "MeSerializer"
Cohesion: 0.25
Nodes (3): MeSerializer, Meta, MeView

### Community 51 - "Appointment"
Cohesion: 0.50
Nodes (3): Professor Dashboard screenshot (EduAccess), Update Availability radio group (Free/Busy/Unavailable), Manage Appointments table (Student, Time, Action columns; empty)

## Knowledge Gaps
- **11 isolated node(s):** `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Django`, `gunicorn + whitenoise (deployment)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 225 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `permissions.py` to `views.py`, `models.py`, `Project Config & Entrypoints`, `script.js`, `CustomUser`, `SignupForm`, `Appointment`?**
  _High betweenness centrality (0.218) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `CustomUser` (e.g. with `CustomUserAdmin` and `SignupForm`) actually correct?**
  _`CustomUser` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `views.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1076923076923077 - nodes in this community are weakly interconnected._
- **Why does `api()` connect `script.js` to `permissions.py`?**
  _High betweenness centrality (0.184) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `Appointment` (e.g. with `AppointmentSerializer` and `AppointmentUpdateSerializer`) actually correct?**
  _`Appointment` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Should `biome.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._