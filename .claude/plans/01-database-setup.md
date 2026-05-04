# Plan: Database Setup — User Data Service

## Context

The `dummy_project/` currently uses an in-memory Python dict as its database layer. The spec (`01-database-setup.md`) requires replacing it with a production-aligned MySQL-backed layer using SQLAlchemy ORM and Alembic migrations. This plan bridges the two states step by step, keeping the existing `app.py` / `service.py` interface intact while wiring in real DB access.

---

## Gap Analysis

| Area | Current State | Required State |
|------|--------------|----------------|
| Storage | In-memory dict (`_USERS`) | MySQL 8+ (`user_db`) |
| ORM | None | SQLAlchemy models (`User`, `UserScore`) |
| Connection | None | `create_engine` + `SessionLocal` via pymysql |
| Scores | Hardcoded `[10, 20, 30, 40]` | Queried from `user_scores` table |
| Migrations | None | Alembic (`migrations/`) |
| Config | None | `.env` with `DB_*` vars |
| Dependencies | No `requirements.txt` | `sqlalchemy`, `alembic`, `pymysql`, `python-dotenv` |

---

## Implementation Steps

### Step 1 — Add `requirements.txt`
**File:** `dummy_project/requirements.txt` (new)

### Step 2 — Add `.env`
**File:** `dummy_project/.env` (not committed)

### Step 3 — Create `dummy_project/models.py`
Two SQLAlchemy ORM models: `User` and `UserScore` with FK + CASCADE.

### Step 4 — Create `dummy_project/db.py`
Engine, SessionLocal, Base. Reads from `.env`. No `create_all()`.

### Step 5 — Rewrite `dummy_project/database.py`
Replace in-memory dict with `get_user_from_db(session, user_id)` and `get_scores_for_user(session, user_id)`.

### Step 6 — Update `dummy_project/service.py`
Add `session` param; replace hardcoded scores with DB query.

### Step 7 — Update `dummy_project/app.py`
Manage session lifecycle (open/close per request).

### Step 8 — Initialize Alembic
`alembic init migrations` + configure `alembic.ini` and `env.py`.

### Step 9 — Generate Initial Migration
`alembic revision --autogenerate -m "init schema"` + add index if omitted.

### Step 10 — Apply Migration
`CREATE DATABASE user_db;` then `alembic upgrade head`.

### Step 11 — Seed Test Data
`dummy_project/seed.py` — dev-only script to populate Jay/Alice/Bob + scores.

---

## Critical Files

| File | Action |
|------|--------|
| `dummy_project/requirements.txt` | Create |
| `dummy_project/.env` | Create (not committed) |
| `dummy_project/models.py` | Create |
| `dummy_project/db.py` | Create |
| `dummy_project/database.py` | Full rewrite |
| `dummy_project/service.py` | Modify |
| `dummy_project/app.py` | Modify |
| `dummy_project/alembic.ini` | Generated |
| `dummy_project/migrations/` | Generated |
| `dummy_project/seed.py` | Create (dev only) |
| `.gitignore` | Add `.env` entry |

---

## Constraints

- `service.py` error contract preserved: `KeyError` → `ValueError`
- No `create_all()` in production
- All schema changes via Alembic only

---

## Verification

1. `pip install -r requirements.txt`
2. Fill in credentials in `dummy_project/.env`
3. `CREATE DATABASE user_db;`
4. `alembic upgrade head`
5. `python seed.py`
6. `python app.py` → enter `1` → correct output
7. Enter `99` → `ValueError: No user found with id: 99`
8. `alembic downgrade -1` → clean rollback
