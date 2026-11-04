# Graph Report - EduAccess  (2026-11-03)

## Corpus Check
- 42 files · ~300,815 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 6, .example 2, .css 2)

## Summary
- 533 nodes · 915 edges · 54 communities (22 shown, 32 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 98 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2f69b655`
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
- BookingRuleTests
- Background Image
- signup.js
- deploy.sh
- package.json
- CabinGateTests
- entrypoint.sh
- SignupForm
- serializers.py
- role-switch.js
- Layout
- .as_user
- tests.py
- ProfessorViewSet
- permissions.py
- 0009_structured_cabin.py
- go.js
- AcademicBlock
- OpenTimeViewSet
- FacultyBlock
- AppointmentViewSet
- CustomUserAdmin
- SignupForm
- CustomUser
- AppointmentAccessTests
- seed_demo.py
- OpenTimeTests
- CustomUser
- .setUp
- DirectionsTests
- eduaccess_backend/urls.py
- ProfessorDirectoryTests
- DashboardLayoutTests
- .overlapping
- MeSerializer
- Appointment
- AppointmentStatusSerializer

## God Nodes (most connected - your core abstractions)
1. `CustomUser` - 29 edges
2. `BaseTestCase` - 22 edges
3. `Appointment` - 18 edges
4. `FacultyBlock` - 16 edges
5. `Notification` - 16 edges
6. `CabinGateTests` - 16 edges
7. `PageTests` - 15 edges
8. `AppointmentViewSet` - 15 edges
9. `AcademicBlock` - 14 edges
10. `SignupTests` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Update Availability radio group (Free/Busy/Unavailable)` --shares_data_with--> `CustomUser`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Layout` --references--> `SignupForm`  [INFERRED]
  CLAUDE.md → api/forms.py
- `Accounts and sign-up` --references--> `CabinForm`  [INFERRED]
  CLAUDE.md → api/forms.py
- `Accounts and sign-up` --references--> `parse_cabin()`  [INFERRED]
  CLAUDE.md → api/models.py
- `Accounts and sign-up` --references--> `format_cabin()`  [INFERRED]
  CLAUDE.md → api/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Student Dashboard Features** — frontend_templates_student_dashboard_availability_section, frontend_templates_student_dashboard_locator_section, frontend_templates_student_dashboard_appointment_section, frontend_templates_student_dashboard_notifications_section [EXTRACTED 1.00]
- **Role-Based UI Templates** — frontend_templates_login, frontend_templates_student_dashboard, frontend_templates_professor_dashboard [INFERRED 0.85]

## Communities (54 total, 32 thin omitted)

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

### Community 7 - "CustomUser"
Cohesion: 0.08
Nodes (10): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+2 more)

### Community 15 - "signup.js"
Cohesion: 0.40
Nodes (3): collegeId, email, form

### Community 17 - "package.json"
Cohesion: 0.20
Nodes (9): description, devDependencies, @biomejs/biome, name, private, scripts, format, lint (+1 more)

### Community 22 - "SignupForm"
Cohesion: 0.22
Nodes (8): login_view(), _wrong_role_message(), Username and Password fields with icons, EduAccess logo and title branding, Frosted-glass login card over blurred campus background, Teal Login button, EduAccess Login Page Screenshot, Select Role dropdown

### Community 23 - "serializers.py"
Cohesion: 0.19
Nodes (5): OpenTime, Meta, _check_quarter_hour(), OpenTimeSerializer, Meta

### Community 24 - "role-switch.js"
Cohesion: 0.33
Nodes (3): ICONS, radios, serverChoseRole

### Community 27 - "tests.py"
Cohesion: 0.11
Nodes (5): AdminSeparationTests, BaseTestCase, CabinLocationTests, NotificationTests, ThemeAndSwitchTests

### Community 28 - "ProfessorViewSet"
Cohesion: 0.15
Nodes (4): ProfessorSerializer, Meta, professor_search(), ProfessorViewSet

### Community 32 - "AcademicBlock"
Cohesion: 0.17
Nodes (3): CabinForm, AcademicBlock, Meta

### Community 33 - "OpenTimeViewSet"
Cohesion: 0.18
Nodes (5): Notification, NotificationSerializer, Meta, NotificationViewSet, OpenTimeViewSet

### Community 34 - "FacultyBlock"
Cohesion: 0.25
Nodes (3): FacultyBlockInline, FacultyBlock, Meta

### Community 35 - "AppointmentViewSet"
Cohesion: 0.20
Nodes (3): AppointmentSerializer, Meta, AppointmentViewSet

### Community 37 - "SignupForm"
Cohesion: 0.22
Nodes (3): SignupForm, Meta, signup_view()

### Community 38 - "CustomUser"
Cohesion: 0.22
Nodes (3): format_cabin(), parse_cabin(), go_view()

### Community 42 - "CustomUser"
Cohesion: 0.31
Nodes (3): CustomUser, Meta, Accounts and sign-up

### Community 46 - "eduaccess_backend/urls.py"
Cohesion: 0.19
Nodes (7): role_required(), decorator(), _cabin_form(), professor_cabin(), professor_dashboard(), signup_done(), student_dashboard()

### Community 50 - "MeSerializer"
Cohesion: 0.25
Nodes (3): MeSerializer, Meta, MeView

### Community 51 - "Appointment"
Cohesion: 0.33
Nodes (4): Appointment, Professor Dashboard screenshot (EduAccess), Update Availability radio group (Free/Busy/Unavailable), Manage Appointments table (Student, Time, Action columns; empty)

## Knowledge Gaps
- **11 isolated node(s):** `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Django`, `gunicorn + whitenoise (deployment)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 223 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `Layout` to `OpenTimeViewSet`, `Project Config & Entrypoints`, `SignupForm`, `script.js`, `CustomUser`, `eduaccess_backend/urls.py`, `Appointment`?**
  _High betweenness centrality (0.216) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `CustomUser` (e.g. with `CustomUserAdmin` and `SignupForm`) actually correct?**
  _`CustomUser` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `biome.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Why does `api()` connect `script.js` to `Layout`?**
  _High betweenness centrality (0.181) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Appointment` (e.g. with `AppointmentSerializer` and `AppointmentStatusSerializer`) actually correct?**
  _`Appointment` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `Frontend Templates & Flows` be split into smaller, more focused modules?**
  _Cohesion score 0.11333333333333333 - nodes in this community are weakly interconnected._