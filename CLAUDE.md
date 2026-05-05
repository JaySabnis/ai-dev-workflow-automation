# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repo demonstrates the **WAT Framework** (Workflow–Action–Test): a structured approach to AI-driven development where Claude acts as an execution engine rather than a simple assistant. The `dummy_project/` is a sample Python codebase backed by MySQL, used as the target for automated analysis, refactoring, and improvement workflows.

## Running the project

```bash
# 1. Activate the virtual environment (Python 3.13)
source venv/bin/activate

# 2. Install dependencies
pip install -r dummy_project/requirements.txt

# 3. Configure database credentials in dummy_project/.env:
#    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# 4. Create the database
mysql -u root -p -e "CREATE DATABASE user_db;"

# 5. Apply migrations
cd dummy_project && alembic upgrade head

# 6. Seed test data
python seed.py

# 7a. Run the CLI app (prompts for a user ID)
python cli.py

# Or use the convenience launcher from project root:
./run.sh

# 7b. Run the REST API server
uvicorn app.main:app --reload --port 8000
# Swagger UI: http://localhost:8000/docs
```

## Architecture

The `dummy_project/` is a layered Python app with a MySQL backend, exposed via both a CLI and a REST API. All application code lives inside `app/`; only `cli.py`, `seed.py`, `alembic.ini`, and `migrations/` sit at the root.

### Project layout

```
dummy_project/
├── cli.py               — CLI entry point
├── seed.py              — dev script to populate test data
├── alembic.ini
├── migrations/
└── app/
    ├── main.py          — FastAPI app init; registers routers
    ├── dependencies.py  — get_db() session dependency
    ├── utils.py         — format_data() and calculate_average()
    ├── core/
    │   ├── db.py        — engine, SessionLocal, Base (reads .env)
    │   └── models.py    — SQLAlchemy ORM models: User, UserScore
    ├── repositories/
    │   └── users.py     — raw DB query functions (SQLAlchemy)
    ├── services/
    │   └── users.py     — business logic; no HTTP concepts
    ├── routes/
    │   └── users.py     — HTTP handlers; routing + error mapping only
    └── schemas/
        └── user.py      — Pydantic request/response models
```

### Layer responsibilities

- `cli.py` — Opens a DB session, calls `services.users.get_user_data()`, prints via `utils.format_data()`, closes session.
- `app/core/db.py` — Engine, `SessionLocal`, and `Base` setup. Reads credentials from `dummy_project/.env` via `python-dotenv`.
- `app/core/models.py` — SQLAlchemy ORM models: `User` (`users` table) and `UserScore` (`user_scores` table with FK cascade).
- `app/repositories/users.py` — DB query functions using SQLAlchemy sessions. Raises `KeyError` on missing records.
- `app/services/users.py` — Business logic: `get_user_data`, `create_user`, `add_score_for_user`, `update_score_for_user`.
- `app/utils.py` — `format_data(dict) -> str` and `calculate_average(list[int]) -> float | None`.
- `app/routes/users.py` — The 4 endpoint handlers. No business logic.
- `app/schemas/user.py` — Pydantic models: `CreateUserRequest`, `AddScoreRequest`, `UpdateScoreRequest`, `UserResponse`, `ScoreResponse`, `CreatedUserResponse`.

### Request flow (API)

```
HTTP Request
  → app/main.py              (FastAPI app)
  → app/routes/users.py      (routing + session injection + error → HTTPException)
  → app/services/users.py    (business logic + validation)
  → app/repositories/users.py (DB queries)
  → MySQL
  → JSON Response
```

### Data flow (CLI)

```
cli.py → app/services/users.py → app/repositories/users.py + app/utils.py
```

Shared infrastructure: `app/core/db.py` (engine/session) and `app/core/models.py` (ORM models).

## Tech stack

- Python 3.13
- FastAPI + Uvicorn (REST API server)
- Pydantic v2 (request/response validation)
- SQLAlchemy (ORM, session-per-request pattern)
- Alembic (schema migrations)
- MySQL 8+ via pymysql
- python-dotenv (env-based config)

## Verified endpoints

All 4 REST endpoints have been tested and confirmed working:

| Method | Path | Status |
|--------|------|--------|
| `POST` | `/api/v1/users` | 201 — returns `{id, name, age}` |
| `GET` | `/api/v1/users/{user_id}` | 200 — returns user + scores + average_score |
| `POST` | `/api/v1/users/{user_id}/scores` | 201 — returns `{id, user_id, score}` |
| `PUT` | `/api/v1/users/{user_id}/scores/{score_id}` | 200 — returns updated score |

Error cases: 404 with `{"detail": "..."}` on missing user or score; 500 on unexpected DB errors.

## WAT Framework workflow

When executing a workflow (refactor, bug-fix, feature-add), follow this sequence:

1. **Workflow** — Read the relevant `.ai/workflows/*.md` file to understand execution steps, then `.ai/rules.md` for constraints, and `.ai/context.md` for project context.
2. **Action** — Modify files in `dummy_project/` one at a time.
3. **Test** — Verify syntax correctness and cross-file consistency after each change.
4. **Git** — Commit on branch `ai-refactor`, push, and open a PR summarizing files modified, issues fixed, and improvements made.

Example prompt to trigger a workflow:
```
Follow .ai/workflows/full-refactor.md
Use rules from .ai/rules.md
Use context from .ai/context.md
Start with analysis and proceed step-by-step.
```
