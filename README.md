# Health Tracker

A desktop application for tracking personal health metrics over time. Built with Python, Tkinter, SQLite, and Matplotlib. This document is a rollover/handoff summary so the next developer (or AI session) can continue work without re-deriving structure or intent.

---

## What this app is

The app is a **single-user, single-instance** health log. The user records **weight**, **water intake** (ounces), and **distance walked** (miles). Each metric has:

- A **form** to add entries (with basic validation).
- A **graph** view (time series via Matplotlib).
- A **table** view (sortable list with row delete).

The user switches metrics from **View** (Weight / Water / Distance) and toggles **Graph** or **Table**. All data lives in one local SQLite file. There is no server, no auth, and no multi-user support in this codebase. The design assumes one DB file per “instance” (e.g. one copy of the app folder per person when used as a template).

A **user profile** (name, gender, age, height) is stored in the same DB and edited via **File → Settings**. If no profile row exists on startup, the Settings dialog is shown first so the user can create one.

---

## Tech stack

- **Language:** Python 3
- **GUI:** Tkinter (tk, ttk)
- **Charts:** Matplotlib (embedded in Tk)
- **Database:** SQLite 3; one file per instance (path in `config.py`)

---

## Project structure

```
health_tracker/
├── main.py              # Entry point → run_app()
├── config.py            # DB_PATH, SCHEMA_PATH, APP_NAME, APP_VERSION
├── db.py                # All SQLite access; get_connection() uses config.DB_PATH at call time
├── user_profile.py      # UserProfile dataclass
├── requirements.txt
├── docs/
│   ├── db_schema.sql    # CREATE TABLE IF NOT EXISTS for all tables
│   └── SCHEMA_UPDATES.md
├── gui/
│   ├── main_window.py   # Menu, forms, graph/table per metric, File → Settings
│   ├── user_profile_form.py
│   ├── <metric>_form.py
│   ├── <metric>_graph_display.py
│   └── <metric>_table_display.py   # weight, water, distance
├── tests/
│   ├── conftest.py      # db_path fixture (temp DB); adds project root to path
│   └── test_db.py       # Schema + weight/water/distance/profile tests
└── scripts/
    └── restore_backup.py  # Restore health_tracker.db from health_tracker_backup.db
```

---

## Layout and conventions

- **Entry point:** `main.py` → `run_app()` in `gui/main_window.py`. The main window is built there; `ensure_db()` runs before the window so the schema exists before any widget reads the DB.
- **Config:** `config.py` holds `DB_PATH`, `SCHEMA_PATH`, `APP_NAME`, `APP_VERSION`. No secrets.
- **Schema:** `docs/db_schema.sql` defines all tables. Every table uses `CREATE TABLE IF NOT EXISTS` and indexes use `CREATE INDEX IF NOT EXISTS`, so applying the schema again is safe and additive.
- **Database layer:** `db.py` owns all SQL. It exposes `get_connection()`, `ensure_db()`, and per-metric functions: `add_*`, `get_*_history()`, `get_*_entries()`, `delete_*`. User profile: `get_user_profile()`, `save_user_profile()`. No ORM.
- **User model:** `user_profile.py` defines the `UserProfile` dataclass (first_name, last_name, gender, age, height_inches). The DB stores one row (id=1) for the profile.
- **GUI structure:** One main window. Under File: **Settings…** (user profile dialog), **Close**. Under View: metric choice (Weight / Water / Distance), then **Graph** / **Table**. Per metric there are three modules:
  - `gui/<metric>_form.py` – input form and validation.
  - `gui/<metric>_graph_display.py` – Matplotlib graph, `refresh()` loads from DB.
  - `gui/<metric>_table_display.py` – Treeview table, `refresh()` and `delete_selected_row()`, with an `on_row_deleted` callback to refresh the graph.
- **Naming:** Tables: `tbl_weight`, `tbl_water`, `tbl_distance`, `tbl_user_profile`. Modules and classes mirror that (e.g. `WeightForm`, `WaterGraphDisplay`, `DistanceTableDisplay`, `UserProfileForm`).

---

## How to run

From the project root, with the project’s venv activated:

```bash
python main.py
```

On first run (or if the DB has no user profile row), the user profile dialog appears; after that, the main window shows. Use **View** to switch metrics and **View → Graph** or **View → Table** to switch views. **Delete** in table view removes the selected row for the current metric.

---

## Schema and data safety

Applying the schema (via the app’s `ensure_db()` or by running `sqlite3 <db_file> < docs/db_schema.sql`) only **adds** missing tables and indexes. It does not drop or alter existing tables. See `docs/SCHEMA_UPDATES.md` for step-by-step instructions when adding new tables or moving DBs.

### Backup and restore

- **Backup:** Copy `health_tracker.db` to `health_tracker_backup.db` (or any name) in the project root.
- **Restore:** Close the app, put your backup in the project root as `health_tracker_backup.db`, then run:
  ```bash
  python scripts/restore_backup.py
  ```
  The script overwrites `health_tracker.db` with the backup and renames the current DB to `health_tracker.db.bak` so you can recover it if needed.

---

## Testing

Tests use **pytest** and live in **`tests/`**. The `db_path` fixture in `tests/conftest.py` points the app at a temporary SQLite file and runs the schema, so the real DB is never touched.

### Testing instructions

1. From the project root, activate the project’s venv.
2. Install test dependencies (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```
3. Run all tests:
   ```bash
   pytest tests/ -v
   ```
   To run a single file: `pytest tests/test_db.py -v`. To run a single test: `pytest tests/test_db.py::test_add_weight_and_get_weight_history -v`.

### What’s covered (starting point)

- **Schema** – `ensure_db()` creates `tbl_weight`, `tbl_water`, `tbl_distance`, `tbl_user_profile`.
- **Weight** – add, get history, get entries (with id), delete.
- **Water** – add, get history.
- **Distance** – add, get entries.
- **User profile** – get returns `None` when empty; save and get round-trip; save overwrites existing row.

When you add new metrics or DB logic, add tests in `tests/test_db.py` (or a new `test_*.py` module) using the same `db_path` fixture so they run against a fresh temp DB.

**Note for tests:** `db.get_connection()` reads `config.DB_PATH` at call time (not at import). The `db_path` fixture sets `config.DB_PATH` to a temp file before any db calls. Do not change `get_connection()` to use a module-level `DB_PATH` or tests will hit the real DB.

---

## Adding a new metric (for next feature)

When implementing a new tracker (e.g. from the TODO list), follow the existing pattern:

1. **Schema** – In `docs/db_schema.sql`, add `CREATE TABLE IF NOT EXISTS tbl_<name>` (id, created_at, value column) and an index on `created_at`.
2. **DB layer** – In `db.py`, add `add_<name>()`, `get_<name>_history()`, `get_<name>_entries()`, `delete_<name>()` (mirror weight/water/distance).
3. **GUI** – Add `gui/<name>_form.py`, `gui/<name>_graph_display.py`, `gui/<name>_table_display.py` (copy from an existing metric and rename).
4. **Main window** – In `gui/main_window.py`: import the new form/graph/table; add View menu item; add form to form row (pack_forget by default); create graph and table widgets with `on_row_deleted` → graph.refresh; in `_switch_metric()` show/hide the new form; in `_show_content()` show the new graph/table when that metric is selected; in `_on_delete_selected()` call the new table’s `delete_selected_row()` when that metric is active; add `_on_<name>_added()` that calls `add_<name>()` and refreshes the new graph and table.
5. **Tests** – In `tests/test_db.py`, add tests for the new add/get/delete using the `db_path` fixture.

---

## TODO

- [ ] **Dashboard** – A single view that shows all metrics’ graphs (e.g. weight, water, distance) on one screen.
- [ ] **Meds tracker** – A medications table and supporting GUI: form to log meds (e.g. name, dose, time), graph/table views, and delete, following the same pattern as weight/water/distance.
- [ ] **Calorie tracker** – A calories table and supporting GUI: form to log calories (e.g. per meal or day), graph/table views, and delete, following the same pattern as other metrics.

---

### Cloud / web app (plan – under consideration)

*Documented so the next session (or you) can continue without re-deriving. Choices are proposals to think about; nothing is committed yet.*

**Goal:** Same metrics reachable from **mobile browser** (quick updates) and from **local Tkinter GUI**, with one backend. Student budget; containerize first, then host.

**Architecture (proposed):**

- **Backend:** REST API in a **container** (same image runs locally and in cloud).
- **Clients:** (1) Responsive **web app** (phone + desktop browser); (2) existing **Tkinter GUI** with optional "API mode" to use the same backend.
- **Database:** SQLite in container with volume initially; Postgres (e.g. Neon, Supabase) when multi-user or durability is needed.
- **Auth:** Single user at first (API key or password in env). Later: Supabase Auth, Firebase Auth, or Auth0 (all work with Flask).

**Stack (proposed):**

- **API:** Flask (Python). Auth options above unchanged.
- **DB:** Reuse `db.py` and `docs/db_schema.sql`; config via env (`DB_PATH` or `DATABASE_URL`).
- **Web UI:** Server-rendered: Jinja2 templates + minimal JS (e.g. Chart.js). No SPA initially.
- **Container:** Dockerfile for Flask app; docker-compose for local run (API + volume for SQLite).
- **Hosting (when ready):** Same container to Google Cloud Run, Fly.io, Railway, or Render; DB on volume or managed Postgres (Neon/Supabase).

**Suggested project layout (if same repo):**

- Add `web/` with Flask app (`app.py` or factory), `requirements.txt`, `templates/`, `static/`, `Dockerfile`, `.env.example`. Root `docker-compose.yml` for API + SQLite volume.

**Implementation order (when proceeding):**

1. Flask API in `web/` with env-driven config; routes for weight, water, distance, profile calling existing `db` layer.
2. Docker + docker-compose; test locally.
3. Simple auth (e.g. API key in header) for single user.
4. Web UI: Jinja forms + list/chart pages calling the API.
5. Optional: Tkinter API mode (backend URL + key in settings).
6. Deploy to chosen provider; add Postgres when needed.
