# Graph Report - EduAccess  (2026-11-05)

## Corpus Check
- 44 files · ~302,698 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: (none) 7, .example 2, .css 2)

## Summary
- 581 nodes · 1029 edges · 39 communities (23 shown, 16 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 107 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8be6939a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- views.py
- biome.json
- Frontend Templates & Flows
- Project Config & Entrypoints
- CustomUser
- script.js
- PageTests
- django_db
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
- StatusNoteTests
- .as_user
- AppointmentSerializer
- ProfessorViewSet
- permissions.py
- AppointmentUpdateSerializer
- go.js
- FacultyBlock
- models.py
- OpenTimeViewSet
- CustomUserAdmin
- AppointmentViewSet

## God Nodes (most connected - your core abstractions)
1. `CustomUser` - 32 edges
2. `BaseTestCase` - 24 edges
3. `Appointment` - 19 edges
4. `StatusNoteTests` - 18 edges
5. `Notification` - 17 edges
6. `api()` - 17 edges
7. `FacultyBlock` - 16 edges
8. `CabinGateTests` - 16 edges
9. `PageTests` - 15 edges
10. `AcademicBlock` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Manage Appointments table (Student, Time, Action columns; empty)` --shares_data_with--> `Appointment`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Layout` --references--> `SignupForm`  [INFERRED]
  CLAUDE.md → api/forms.py
- `Layout` --references--> `Appointment`  [INFERRED]
  CLAUDE.md → api/models.py
- `Layout` --references--> `CustomUser`  [INFERRED]
  CLAUDE.md → api/models.py
- `Layout` --references--> `Notification`  [INFERRED]
  CLAUDE.md → api/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Student Dashboard Features** — frontend_templates_student_dashboard_availability_section, frontend_templates_student_dashboard_locator_section, frontend_templates_student_dashboard_appointment_section, frontend_templates_student_dashboard_notifications_section [EXTRACTED 1.00]
- **Role-Based UI Templates** — frontend_templates_login, frontend_templates_student_dashboard, frontend_templates_professor_dashboard [INFERRED 0.85]

## Communities (39 total, 16 thin omitted)

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

### Community 4 - "CustomUser"
Cohesion: 0.10
Nodes (7): Command, CustomUser, Meta, SignupTests, Professor Dashboard screenshot (EduAccess), Update Availability radio group (Free/Busy/Unavailable), Manage Appointments table (Student, Time, Action columns; empty)

### Community 5 - "script.js"
Cohesion: 0.13
Nodes (45): Student Dashboard screenshot (Welcome, Student) with frosted-glass cards over blurred campus building background, Book Appointment form (professor select, time slot datetime, Submit), Cabin Locator section (professor name input + Find Cabin button), Notifications section (empty), Professor Availability table (Professor Ashish: Free), actionButton(), addOpenTime(), api() (+37 more)

### Community 6 - "PageTests"
Cohesion: 0.09
Nodes (12): CabinLocationTests, make_user(), PageTests, login_view(), fail(), _wrong_role_message(), Username and Password fields with icons, EduAccess logo and title branding (+4 more)

### Community 7 - "django_db"
Cohesion: 0.06
Nodes (14): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+6 more)

### Community 10 - "BaseTestCase"
Cohesion: 0.06
Nodes (8): AdminSeparationTests, AppointmentReasonTests, BaseTestCase, BookingRuleTests, BookingTests, DashboardLayoutTests, NotificationTests, ThemeAndSwitchTests

### Community 15 - "signup.js"
Cohesion: 0.40
Nodes (3): collegeId, email, form

### Community 17 - "package.json"
Cohesion: 0.20
Nodes (9): description, devDependencies, @biomejs/biome, name, private, scripts, format, lint (+1 more)

### Community 20 - "CabinGateTests"
Cohesion: 0.07
Nodes (3): AdminUserCreationTests, CabinGateTests, DirectionsTests

### Community 22 - "SignupForm"
Cohesion: 0.22
Nodes (3): SignupForm, Meta, signup_view()

### Community 23 - "OpenTime"
Cohesion: 0.16
Nodes (5): OpenTime, Meta, _check_quarter_hour(), OpenTimeSerializer, Meta

### Community 24 - "role-switch.js"
Cohesion: 0.33
Nodes (3): ICONS, radios, serverChoseRole

### Community 25 - "StatusNoteTests"
Cohesion: 0.15
Nodes (4): MyProfessor, Meta, StatusNoteTests, API

### Community 26 - ".as_user"
Cohesion: 0.09
Nodes (5): AppointmentAccessTests, MeTests, MyProfessorTests, OpenTimeTests, ProfessorDirectoryTests

### Community 28 - "ProfessorViewSet"
Cohesion: 0.09
Nodes (7): MeSerializer, Meta, ProfessorSerializer, Meta, status_note_data(), professor_search(), ProfessorViewSet

### Community 29 - "permissions.py"
Cohesion: 0.17
Nodes (4): dashboard_for(), IsAppointmentParticipant, ProfessorHasCabin, Layout

### Community 32 - "FacultyBlock"
Cohesion: 0.10
Nodes (9): CabinForm, AcademicBlock, Meta, FacultyBlock, Meta, format_cabin(), parse_cabin(), go_view() (+1 more)

### Community 33 - "models.py"
Cohesion: 0.17
Nodes (6): FacultyBlockInline, Appointment, Notification, NotificationSerializer, Meta, NotificationViewSet

### Community 36 - "CustomUserAdmin"
Cohesion: 0.20
Nodes (3): AcademicBlockAdmin, AppointmentAdmin, CustomUserAdmin

### Community 49 - "AppointmentViewSet"
Cohesion: 0.29
Nodes (4): AppointmentViewSet, _name(), _reason(), _when()

## Knowledge Gaps
- **11 isolated node(s):** `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Django`, `gunicorn + whitenoise (deployment)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 228 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `permissions.py` to `views.py`, `models.py`, `Project Config & Entrypoints`, `CustomUser`, `script.js`, `SignupForm`?**
  _High betweenness centrality (0.221) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `CustomUser` (e.g. with `CustomUserAdmin` and `SignupForm`) actually correct?**
  _`CustomUser` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `views.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1076923076923077 - nodes in this community are weakly interconnected._
- **Why does `CustomUser` connect `CustomUser` to `FacultyBlock`, `models.py`, `views.py`, `CustomUserAdmin`, `PageTests`, `BaseTestCase`, `CabinGateTests`, `SignupForm`, `StatusNoteTests`, `ProfessorViewSet`, `permissions.py`?**
  _High betweenness centrality (0.191) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `Appointment` (e.g. with `AppointmentSerializer` and `AppointmentUpdateSerializer`) actually correct?**
  _`Appointment` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Should `biome.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._