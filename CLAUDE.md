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
python app.py

# Or use the convenience launcher from project root:
./run.sh

# 7b. Run the REST API server
uvicorn app.main:app --reload --port 8000
# Swagger UI: http://localhost:8000/docs
```

## Architecture

The `dummy_project/` is a layered Python app with a MySQL backend, exposed via both a CLI and a REST API.

### Core layers

- `app.py` — CLI entry point. Opens a DB session, calls `service.get_user_data()`, prints formatted result via `utils.format_data()`, closes session.
- `service.py` — Business logic layer. Functions: `get_user_data`, `create_user`, `add_score_for_user`, `update_score_for_user`. No HTTP concepts here.
- `database.py` — DB query functions using SQLAlchemy sessions. Raises `KeyError` on missing records. Functions: `get_user_from_db`, `get_scores_for_user`, `create_user_in_db`, `add_score_to_db`, `update_score_in_db`.
- `models.py` — SQLAlchemy ORM models: `User` (`users` table) and `UserScore` (`user_scores` table with FK cascade).
- `db.py` — Engine, `SessionLocal`, and `Base` setup. Reads credentials from `dummy_project/.env` via `python-dotenv`.
- `utils.py` — Two pure functions: `format_data(dict) -> str` (CLI only) and `calculate_average(list[int]) -> float | None` (returns `None` on empty).
- `seed.py` — Dev-only script to populate test data into MySQL.
- `migrations/` — Alembic migration scripts managed via `alembic.ini`.

### FastAPI layer (`app/`)

- `app/main.py` — FastAPI app init; registers the users router.
- `app/dependencies.py` — `get_db()` dependency: creates a `SessionLocal`, yields it, closes after response.
- `app/schemas/user.py` — Pydantic models: `CreateUserRequest`, `AddScoreRequest`, `UpdateScoreRequest`, `UserResponse`, `ScoreResponse`, `CreatedUserResponse`.
- `app/routes/users.py` — The 4 endpoint handlers. Handles routing, session injection, and HTTP error mapping only — no business logic.

### Request flow (API)

```
HTTP Request
  → app/main.py          (FastAPI app)
  → app/routes/users.py  (routing + session injection + error → HTTPException)
  → service.py           (business logic + validation)
  → database.py          (DB queries)
  → MySQL
  → JSON Response
```

### Data flow (CLI)

```
app.py → service.py → database.py + utils.py
```

Shared infrastructure: `db.py` (engine/session) and `models.py` (ORM models).

## Tech stack

- Python 3.13
- FastAPI + Uvicorn (REST API server)
- Pydantic v2 (request/response validation)
- SQLAlchemy (ORM, session-per-request pattern)
- Alembic (schema migrations)
- MySQL 8+ via pymysql
- python-dotenv (env-based config)

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
