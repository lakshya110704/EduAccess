# EduAccess

Django 6.1 + DRF backend with server-rendered templates and vanilla JS. Faculty
availability, cabin locator and appointment booking for students and professors.

## Layout

- `eduaccess_backend/settings.py` — single settings module, every environment-specific value comes from env vars / `.env` via python-decouple (see `.env.example`). `DJANGO_DEBUG` defaults to off; with it off, `DJANGO_SECRET_KEY` is required and HTTPS/HSTS/secure cookies are on. WhiteNoise serves static files. `DB_ENGINE=sqlite` is for local runs and tests only.
- `eduaccess_backend/urls.py` — pages (`/`, `/login/`, `/logout/` POST-only, `/student/`, `/professor/`), `/admin/`, `/api/`, `/healthz/`
- `api/models.py` — `CustomUser` (role, availability_status, cabin_number), `Appointment`, `Notification`
- `api/permissions.py` — `role_required` page decorator, `dashboard_for(user)`, `IsAppointmentParticipant`
- `api/views.py` — API viewsets + page views. Login has a role dropdown (Student/Professor): it succeeds only if
  the credentials belong to an account **of that role** (the stored role decides, the dropdown only has to
  match). Correct credentials + wrong role → "This is a {role} account. Is the role selected right?"; wrong
  credentials → one neutral message for any role (no account enumeration). The public login has no link to the
  admin; staff go to `/admin/` directly.
- `api/serializers.py` — validation lives here (future-only times, no double-booking, professor must be a professor, status transitions)
- `api/forms.py` — `SignupForm`: self-registration rules (role whitelist, email domain per role, unique email
  and college ID, password validators); saves accounts **inactive**
- `api/management/commands/seed_demo.py` — demo users for local runs (DEBUG only)
- `frontend/templates/` — `login.html`, `student-dashboard.html`, `professor-dashboard.html` (`<body data-page=...>` selects the JS behaviour)
- Role themes: `styles.css` defines colour variables per `<body data-theme="student|professor">` (student teal,
  professor indigo + amber). Login/sign-up use a shared radio-based switch (`templates/role-switch.html`) that
  drives the theme via CSS `:has()`; `static/role-switch.js` swaps the heading icon, remembers the last role in
  localStorage and emits a `rolechange` event (used by `signup.js`). Dashboards are stamped with their role's theme.
- `frontend/static/script.js` — all dashboard logic: `api()` fetch wrapper (CSRF header, relative `/api`), renders with `textContent` only, polls every 10s while the tab is visible

## Admin site

- Branded via `frontend/templates/admin/base_site.html` (logo, "EduAccess Admin") and `frontend/static/admin-theme.css`
  (Django admin CSS variables → teal/navy); `frontend/templates/admin/login.html` adds "Staff sign-in".
  Titles set on `admin.site` in `api/admin.py`.
- `LOGOUT_REDIRECT_URL = '/admin/login/'` — only Django's own logout (the admin's) uses it; the app's `/logout/`
  still returns to `/login/`.

## Accounts and sign-up

- `CustomUser` adds `role`, `availability_status`, `cabin_number`, `middle_name`, `college_id` (roll number
  for students, employee ID for professors). `get_full_name()` = first + middle + last.
- DB constraints: email unique case-insensitively (when set); `college_id` unique per role (when set).
- `/signup/` (link on the login page): students and professors register themselves. Email must be on the
  role's domain — `SIGNUP_STUDENT_EMAIL_DOMAIN` (default `muj.manipal.edu`), `SIGNUP_PROFESSOR_EMAIL_DOMAIN`
  (default `jaipur.manipal.edu`) in `.env`. New accounts are inactive; logging in shows "awaiting approval".
- Admins approve in `/admin/` → Users (filter Active = No, check role and college ID) → action
  "Activate selected accounts". The admin's Add user page also sets role/IDs/cabin in one step.
- Not yet: email confirmation (no mail setup) and sign-up rate limiting — needed before going public.

## API

All endpoints need a logged-in session; writes need the `X-CSRFToken` header.

- `GET /api/professors/?search=` — read-only directory (name, cabin, availability)
- `GET|PATCH /api/me/` — current user; professors PATCH `availability_status`
- `GET|POST /api/appointments/`, `GET|PATCH /api/appointments/<id>/` — students book; only `status` is patchable after booking: professor → Confirmed/Cancelled, student → Cancelled; Cancelled is final. No PUT/DELETE. Each change notifies the other party
- `GET /api/notifications/` — own notifications, newest first

## Running locally

Needs Python 3.12+ (Django 6.1). The old `eduaccess-env` / `.venv` folders are Python 3.9 and too old; recreate:

```bash
uv venv --python 3.12 .venv && source .venv/bin/activate && uv pip install -r requirements.txt
cp .env.example .env   # set DJANGO_DEBUG=True, DB_ENGINE=sqlite for a quick local run
python manage.py migrate && python manage.py seed_demo && python manage.py runserver
```

Tests: `DB_ENGINE=sqlite DJANGO_DEBUG=True python manage.py test api`

## Dependencies

- `requirements.in` — direct dependencies (ranges), edited by hand.
- `requirements.txt` — generated lock file (pip-tools / `pip-compile`): every package (direct +
  transitive) pinned exactly, with hashes, resolved under Python 3.12. Never edit by hand; CI, Docker and
  production install from it. pip-tools is used (not `uv pip compile`) because Dependabot can only
  regenerate pip-compile lock files correctly.
- `.python-version` (3.12) — tells Dependabot (and uv/pyenv) which Python to resolve with.
- To add or bump a package: edit `requirements.in`, then
  `uvx --python 3.12 --from pip-tools pip-compile --generate-hashes --strip-extras requirements.in`
  (add `--upgrade-package <name>` to bump one package), run the tests, commit both files.
- Updates are deliberate: `.github/dependabot.yml` opens weekly PRs for pip packages (minor/patch grouped),
  npm (Biome) and GitHub Actions; CI tests each, a human merges.

## Linting and formatting

- Python: Ruff (`ruff.toml`) — lint rules E, F, W, I, B, DJ, UP; line length 120; single quotes;
  migrations excluded from linting. Pinned in `requirements-dev.in/.txt` (pip-tools lock, dev only).
- JavaScript: Biome (`biome.json`) on `frontend/static/` — recommended rules, 2-space indent, line
  width 120. Pinned exactly in `package.json` + `package-lock.json` (`node_modules/` is ignored).
- Check locally before pushing:
  `pip install -r requirements-dev.txt && npm ci`, then
  `ruff check . && ruff format --check . && npx biome ci frontend/static`.
  Auto-fix: `ruff check --fix . && ruff format . && npm run format`.
- `.git-blame-ignore-revs` lists the one-off mass-reformat commit; `git blame` skips it
  (GitHub does automatically; locally run `git config blame.ignoreRevsFile .git-blame-ignore-revs`).

## CI

`.github/workflows/ci.yml` (GitHub Actions) runs two parallel jobs on every push:
- `lint` — `ruff check`, `ruff format --check`, `biome ci frontend/static`; any finding fails CI.
- `test` — Python 3.12, a PostgreSQL 16 service container (so tests run on the same database engine as
  production), `makemigrations --check` to catch missing migrations, then `manage.py test api`.

## Deployment (homelab)

- `Dockerfile` (Python 3.12-slim, hash-checked install, static files collected at build, non-root user,
  gunicorn on :8000), `docker/entrypoint.sh` (runs `migrate` on every start), `docker-compose.yml`
  (`db` = postgres:16 with `pgdata` volume, `web` published on **127.0.0.1:8000 only**).
- Runs on the homelab in `~/eduaccess` (a clone of this repo, left on a detached HEAD at the deployed
  commit). Its `.env` (from `.env.production.example`) lives only on the homelab.
- **Automatic deploys:** the `deploy` job in `ci.yml` runs on pushes to `main` after `lint` and `test` pass.
  It joins the tailnet as an ephemeral `tag:ci` node (Tailscale OAuth client; secrets `TS_OAUTH_CLIENT_ID`,
  `TS_OAUTH_SECRET`) and SSHes to `homelab@homelab.tail2734e7.ts.net` with a deploy-only key
  (`DEPLOY_SSH_KEY`, host key pinned in `DEPLOY_KNOWN_HOSTS`). On the homelab that key is
  `restrict,command="…/deploy/deploy.sh"` in `authorized_keys`, so it can only run `deploy/deploy.sh <sha>`:
  the sha must be on `origin/main`; it checks out, `docker compose up -d --build`, and waits for `/healthz/`.
- Tailscale policy: `tag:ci` may reach only `homelab:22` (policy `tests` enforce this); people's devices use
  `autogroup:member`, never `*`, so tagged nodes stay restricted.
- Manual deploy of a commit: `ssh homelab '~/eduaccess/deploy/deploy.sh <full-sha>'`.
- Access is via Tailscale HTTPS on `homelab.tail2734e7.ts.net` (tailnet devices only), so production's
  HTTPS-only cookies work. Nothing is exposed to the LAN or internet.

## Commits

Never add `Co-Authored-By` or other AI attribution lines to commits or PRs.

## graphify

A knowledge graph of this codebase lives in `graphify-out/` (`graph.json`, `GRAPH_REPORT.md`, `graph.html`).

- Before answering questions about the codebase or reading many files to orient yourself, query the
  graph first: `graphify query "<question>"` (or `/graphify query "<question>"`). Read
  `graphify-out/GRAPH_REPORT.md` for the overall map. Open source files only for the specific code you
  need to change.
- Git hooks (post-commit/checkout/merge/rewrite) rebuild the code graph automatically. After
  changing docs or images, run `/graphify --update`.
- The graph files are tracked in Git. The hook rebuilds them *after* each commit, so they always show
  as modified afterwards: include the changed `graphify-out/` files in the next commit (the copy on
  GitHub is therefore one commit behind).
