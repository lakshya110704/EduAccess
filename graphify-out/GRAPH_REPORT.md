# Graph Report - EduAccess  (2026-10-24)

## Corpus Check
- 25 files · ~291,711 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 3, .example 1, .css 1)

## Summary
- 256 nodes · 410 edges · 19 communities (8 shown, 11 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 50 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5f70db2e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- views.py
- Frontend Templates & Flows
- Project Config & Entrypoints
- Appointment
- script.js
- PageTests
- serializers.py
- App Config
- Brand Logo
- tests.py
- Background Image
- BookingTests
- EduAccess
- tests.py

## God Nodes (most connected - your core abstractions)
1. `CustomUser` - 16 edges
2. `AppointmentAccessTests` - 13 edges
3. `Appointment` - 13 edges
4. `AppointmentViewSet` - 13 edges
5. `Notification` - 13 edges
6. `BaseTestCase` - 12 edges
7. `BookingTests` - 12 edges
8. `PageTests` - 12 edges
9. `AppointmentSerializer` - 11 edges
10. `api()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Layout` --references--> `Appointment`  [INFERRED]
  CLAUDE.md → api/models.py
- `Layout` --references--> `CustomUser`  [INFERRED]
  CLAUDE.md → api/models.py
- `Layout` --references--> `Notification`  [INFERRED]
  CLAUDE.md → api/models.py
- `Layout` --references--> `api()`  [INFERRED]
  CLAUDE.md → frontend/static/script.js
- `Manage Appointments table (Student, Time, Action columns; empty)` --shares_data_with--> `Appointment`  [INFERRED]
  frontend/static/assets/professor.png → api/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Student Dashboard Features** — frontend_templates_student_dashboard_availability_section, frontend_templates_student_dashboard_locator_section, frontend_templates_student_dashboard_appointment_section, frontend_templates_student_dashboard_notifications_section [EXTRACTED 1.00]
- **Role-Based UI Templates** — frontend_templates_login, frontend_templates_student_dashboard, frontend_templates_professor_dashboard [INFERRED 0.85]

## Communities (19 total, 11 thin omitted)

### Community 0 - "views.py"
Cohesion: 0.06
Nodes (15): dashboard_for(), IsAppointmentParticipant, role_required(), decorator(), login_view(), logout_view(), professor_dashboard(), student_dashboard() (+7 more)

### Community 2 - "Frontend Templates & Flows"
Cohesion: 0.11
Nodes (22): Login Page, Login Form (username, password, role), Professor Dashboard Page, Manage Appointments Table, Update Availability Section, Student Dashboard Page, Book Appointment Section, Professor Availability Table (+14 more)

### Community 4 - "Appointment"
Cohesion: 0.15
Nodes (4): AppointmentSerializer, Meta, AppointmentViewSet, _name()

### Community 5 - "script.js"
Cohesion: 0.20
Nodes (22): Student Dashboard screenshot (Welcome, Student) with frosted-glass cards over blurred campus building background, Book Appointment form (professor select, time slot datetime, Submit), Cabin Locator section (professor name input + Find Cabin button), Notifications section (empty), Professor Availability table (Professor Ashish: Free), actionButton(), api(), el() (+14 more)

### Community 7 - "serializers.py"
Cohesion: 0.08
Nodes (12): Notification, AppointmentStatusSerializer, Meta, MeSerializer, Meta, NotificationSerializer, Meta, ProfessorSerializer (+4 more)

### Community 10 - "tests.py"
Cohesion: 0.11
Nodes (5): AppointmentAccessTests, BaseTestCase, MeTests, NotificationTests, ProfessorDirectoryTests

### Community 16 - "EduAccess"
Cohesion: 0.25
Nodes (7): API, CI, Commits, Dependencies, EduAccess, graphify, Running locally

### Community 20 - "tests.py"
Cohesion: 0.08
Nodes (10): CustomUserAdmin, Command, Migration, Migration, Migration, Appointment, CustomUser, Professor Dashboard screenshot (EduAccess) (+2 more)

## Knowledge Gaps
- **10 isolated node(s):** `Username and Password fields with icons`, `EduAccess logo and title branding`, `EduAccess Login Page Screenshot`, `Neoclassical university building with golden dome, palm-lined lawn, blue sky`, `Campus Background Photo (domed administrative building)` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 105 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Layout` connect `views.py` to `EduAccess`, `tests.py`, `script.js`, `serializers.py`?**
  _High betweenness centrality (0.321) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `CustomUser` (e.g. with `CustomUserAdmin` and `Command`) actually correct?**
  _`CustomUser` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Username and Password fields with icons`, `EduAccess logo and title branding`, `EduAccess Login Page Screenshot` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `views.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06463414634146342 - nodes in this community are weakly interconnected._
- **Why does `api()` connect `script.js` to `views.py`?**
  _High betweenness centrality (0.269) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Appointment` (e.g. with `AppointmentSerializer` and `AppointmentStatusSerializer`) actually correct?**
  _`Appointment` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Should `Frontend Templates & Flows` be split into smaller, more focused modules?**
  _Cohesion score 0.11333333333333333 - nodes in this community are weakly interconnected._