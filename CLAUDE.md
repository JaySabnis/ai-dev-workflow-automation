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

# 7. Run the app (prompts for a user ID)
python app.py

# Or use the convenience launcher from project root:
./run.sh
```

## Architecture

The `dummy_project/` is a layered Python app with a MySQL backend:

- `app.py` — Entry point. Opens a DB session, calls `service.get_user_data()`, prints formatted result, closes session.
- `service.py` — Orchestration layer. Validates user ID, fetches user and scores from DB, computes average score, returns merged dict. Uses structured logging.
- `database.py` — DB query functions using SQLAlchemy sessions. `get_user_from_db(session, int)` raises `KeyError` on miss; `get_scores_for_user(session, int)` returns a list of ints.
- `models.py` — SQLAlchemy ORM models: `User` (`users` table) and `UserScore` (`user_scores` table with FK cascade).
- `db.py` — Engine, `SessionLocal`, and `Base` setup. Reads credentials from `dummy_project/.env` via `python-dotenv`.
- `utils.py` — Two pure functions: `format_data(dict) -> str` and `calculate_average(list[int]) -> int` (raises `ValueError` on empty list).
- `seed.py` — Dev-only script to populate test data into MySQL.
- `migrations/` — Alembic migration scripts managed via `alembic.ini`.

Data flow: `app.py` → `service.py` → `database.py` + `utils.py`, with `db.py` and `models.py` as shared infrastructure.

## Tech stack

- Python 3.13
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
