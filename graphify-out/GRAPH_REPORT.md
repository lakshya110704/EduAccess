# Graph Report - EduAccess  (2026-11-02)

## Corpus Check
- 35 files · ~295,930 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 6, .example 2, .css 2)

## Summary
- 387 nodes · 609 edges · 33 communities (17 shown, 16 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 61 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1e7f40f8`
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
- permissions.py
- .as_user
- ProfessorViewSet
- serializers.py
- login_view
- api/urls.py

## God Nodes (most connected - your core abstractions)
1. `CustomUser` - 24 edges
2. `BaseTestCase` - 16 edges
3. `PageTests` - 15 edges
4. `SignupTests` - 14 edges
5. `Appointment` - 13 edges
6. `Notification` - 13 edges
7. `AppointmentAccessTests` - 13 edges
8. `EduAccess` - 12 edges
9. `BookingTests` - 12 edges
10. `MyProfessorTests` - 12 edges

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

## Communities (33 total, 16 thin omitted)

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
Cohesion: 0.19
Nodes (27): Student Dashboard screenshot (Welcome, Student) with frosted-glass cards over blurred campus building background, Book Appointment form (professor select, time slot datetime, Submit), Cabin Locator section (professor name input + Find Cabin button), Notifications section (empty), Professor Availability table (Professor Ashish: Free), actionButton(), api(), bookProfessor() (+19 more)

### Community 7 - "CustomUser"
Cohesion: 0.12
Nodes (6): Migration, Migration, Migration, Migration, Migration, Migration

### Community 10 - "tests.py"
Cohesion: 0.09
Nodes (7): Appointment, AdminSeparationTests, AdminUserCreationTests, BaseTestCase, BookingTests, NotificationTests, ThemeAndSwitchTests

### Community 15 - "signup.js"
Cohesion: 0.40
Nodes (3): collegeId, email, form

### Community 17 - "package.json"
Cohesion: 0.20
Nodes (9): description, devDependencies, @biomejs/biome, name, private, scripts, format, lint (+1 more)

### Community 22 - "CustomUser"
Cohesion: 0.07
Nodes (12): SignupForm, Meta, Command, CustomUser, Meta, MeSerializer, Meta, signup_view() (+4 more)

### Community 23 - "AppointmentSerializer"
Cohesion: 0.15
Nodes (4): AppointmentSerializer, Meta, AppointmentViewSet, _name()

### Community 24 - "role-switch.js"
Cohesion: 0.33
Nodes (3): ICONS, radios, serverChoseRole

### Community 25 - "permissions.py"
Cohesion: 0.25
Nodes (3): dashboard_for(), IsAppointmentParticipant, Layout

### Community 26 - ".as_user"
Cohesion: 0.11
Nodes (4): AppointmentAccessTests, MeTests, MyProfessorTests, ProfessorDirectoryTests

### Community 28 - "ProfessorViewSet"
Cohesion: 0.15
Nodes (4): CustomUserAdmin, ProfessorSerializer, Meta, ProfessorViewSet

### Community 29 - "serializers.py"
Cohesion: 0.22
Nodes (4): AppointmentStatusSerializer, Meta, NotificationSerializer, Meta

### Community 30 - "login_view"
Cohesion: 0.22
Nodes (8): login_view(), _wrong_role_message(), Username and Password fields with icons, EduAccess logo and title branding, Frosted-glass login card over blurred campus background, Teal Login button, EduAccess Login Page Screenshot, Select Role dropdown

## Knowledge Gaps
- **11 isolated node(s):** `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Django`, `gunicorn + whitenoise (deployment)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 166 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `permissions.py` to `eduaccess_backend/urls.py`, `Project Config & Entrypoints`, `script.js`, `tests.py`, `models.py`, `CustomUser`?**
  _High betweenness centrality (0.258) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `CustomUser` (e.g. with `SignupForm` and `Command`) actually correct?**
  _`CustomUser` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@biomejs/biome`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `biome.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Why does `CustomUser` connect `CustomUser` to `SignupTests`, `PageTests`, `tests.py`, `models.py`, `permissions.py`, `views.py`, `ProfessorViewSet`, `serializers.py`, `login_view`?**
  _High betweenness centrality (0.201) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Appointment` (e.g. with `AppointmentSerializer` and `AppointmentStatusSerializer`) actually correct?**
  _`Appointment` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Should `Frontend Templates & Flows` be split into smaller, more focused modules?**
  _Cohesion score 0.11333333333333333 - nodes in this community are weakly interconnected._