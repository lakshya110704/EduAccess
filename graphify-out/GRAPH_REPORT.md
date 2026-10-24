# Graph Report - EduAccess  (2026-10-24)

## Corpus Check
- 25 files · ~291,037 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 2, .example 1, .css 1)

## Summary
- 254 nodes · 408 edges · 20 communities (9 shown, 11 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 50 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dbf5a635`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- views.py
- CustomUser
- Frontend Templates & Flows
- Project Config & Entrypoints
- Appointment
- script.js
- PageTests
- MeSerializer
- App Config
- Brand Logo
- tests.py
- Background Image
- BookingTests
- EduAccess

## God Nodes (most connected - your core abstractions)
1. `CustomUser` - 16 edges
2. `Appointment` - 13 edges
3. `Notification` - 13 edges
4. `AppointmentAccessTests` - 13 edges
5. `AppointmentViewSet` - 13 edges
6. `BaseTestCase` - 12 edges
7. `BookingTests` - 12 edges
8. `PageTests` - 12 edges
9. `AppointmentSerializer` - 11 edges
10. `api()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Manage Appointments table (Student, Time, Action columns; empty)` --shares_data_with--> `Appointment`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Layout` --references--> `CustomUser`  [INFERRED]
  CLAUDE.md → api/models.py
- `Update Availability radio group (Free/Busy/Unavailable)` --shares_data_with--> `CustomUser`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py
- `Layout` --references--> `Appointment`  [INFERRED]
  CLAUDE.md → api/models.py
- `Teal Login button` --shares_data_with--> `login_view()`  [INFERRED]
  frontend/static/assets/login.png → api/views.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Student Dashboard Features** — frontend_templates_student_dashboard_availability_section, frontend_templates_student_dashboard_locator_section, frontend_templates_student_dashboard_appointment_section, frontend_templates_student_dashboard_notifications_section [EXTRACTED 1.00]
- **Role-Based UI Templates** — frontend_templates_login, frontend_templates_student_dashboard, frontend_templates_professor_dashboard [INFERRED 0.85]

## Communities (20 total, 11 thin omitted)

### Community 0 - "views.py"
Cohesion: 0.08
Nodes (12): Notification, dashboard_for(), IsAppointmentParticipant, role_required(), decorator(), NotificationSerializer, Meta, logout_view() (+4 more)

### Community 1 - "CustomUser"
Cohesion: 0.09
Nodes (9): CustomUserAdmin, Command, Migration, Migration, Migration, CustomUser, Professor Dashboard screenshot (EduAccess), Update Availability radio group (Free/Busy/Unavailable) (+1 more)

### Community 2 - "Frontend Templates & Flows"
Cohesion: 0.11
Nodes (22): Login Page, Login Form (username, password, role), Professor Dashboard Page, Manage Appointments Table, Update Availability Section, Student Dashboard Page, Book Appointment Section, Professor Availability Table (+14 more)

### Community 4 - "Appointment"
Cohesion: 0.11
Nodes (7): Appointment, AppointmentSerializer, Meta, AppointmentStatusSerializer, Meta, AppointmentViewSet, _name()

### Community 5 - "script.js"
Cohesion: 0.20
Nodes (22): Student Dashboard screenshot (Welcome, Student) with frosted-glass cards over blurred campus building background, Book Appointment form (professor select, time slot datetime, Submit), Cabin Locator section (professor name input + Find Cabin button), Notifications section (empty), Professor Availability table (Professor Ashish: Free), actionButton(), api(), el() (+14 more)

### Community 6 - "PageTests"
Cohesion: 0.13
Nodes (9): make_user(), PageTests, login_view(), Username and Password fields with icons, EduAccess logo and title branding, Frosted-glass login card over blurred campus background, Teal Login button, EduAccess Login Page Screenshot (+1 more)

### Community 7 - "MeSerializer"
Cohesion: 0.11
Nodes (6): MeSerializer, Meta, ProfessorSerializer, Meta, MeView, ProfessorViewSet

### Community 10 - "tests.py"
Cohesion: 0.11
Nodes (5): AppointmentAccessTests, BaseTestCase, MeTests, NotificationTests, ProfessorDirectoryTests

### Community 16 - "EduAccess"
Cohesion: 0.33
Nodes (5): API, Commits, EduAccess, graphify, Running locally

## Knowledge Gaps
- **10 isolated node(s):** `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Cabin Locator section (professor name input + Find Cabin button)`, `Professor Availability table (Professor Ashish: Free)`, `Username and Password fields with icons` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 103 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `views.py` to `EduAccess`, `CustomUser`, `Appointment`, `script.js`?**
  _High betweenness centrality (0.312) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `CustomUser` (e.g. with `CustomUserAdmin` and `Command`) actually correct?**
  _`CustomUser` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)`, `Cabin Locator section (professor name input + Find Cabin button)` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `views.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08377896613190731 - nodes in this community are weakly interconnected._
- **Why does `api()` connect `script.js` to `views.py`?**
  _High betweenness centrality (0.270) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Appointment` (e.g. with `AppointmentSerializer` and `AppointmentStatusSerializer`) actually correct?**
  _`Appointment` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Should `CustomUser` be split into smaller, more focused modules?**
  _Cohesion score 0.08505747126436781 - nodes in this community are weakly interconnected._