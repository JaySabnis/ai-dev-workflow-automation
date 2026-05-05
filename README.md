# AI Dev Workflow Automation

An AI-driven system that automates codebase analysis, refactoring, and development workflows using structured prompts and Claude Code (VS Code agent).

---

## Overview

This project demonstrates how AI can be integrated directly into developer workflows to **analyze, modify, and improve a codebase autonomously**.

Instead of acting as a simple assistant, the system follows a **structured workflow framework** to execute real engineering tasks end-to-end.

---

## Objective

To design a **workflow-driven AI system** that:

* Automates repetitive development tasks
* Improves code quality and structure
* Simulates real-world engineering processes
* Demonstrates agent-like behavior using LLMs

---

## WAT Framework (Workflow–Action–Test)

This project is built around the **WAT Framework**, a simple but effective approach to designing AI-driven engineering systems.

### Workflow

* Define structured steps for the AI to follow
* Includes planning, execution strategy, and constraints
* Implemented using Markdown-based workflow files

### Action

* AI performs actual operations:
  * code refactoring
  * bug fixing
  * feature additions
* Works file-by-file to maintain control and consistency

### Test

* Validate results after execution:
  * syntax checks
  * consistency verification
  * basic correctness

> This framework ensures the AI behaves like an **engineering system**, not just a prompt responder.

---

## System Workflow

### 1. Codebase Analysis
* Reads and understands all project files
* Identifies bugs, inefficiencies, and structural issues

### 2. AI Planning
* Generates a structured plan:
  * Issues list
  * Files to modify
  * Step-by-step execution strategy

### 3. Automated Execution
* Refactors code file-by-file
* Fixes bugs and improves readability
* Adds error handling and best practices

### 4. Validation (Test Phase)
* Ensures updated code is syntactically correct
* Verifies consistency across files

### 5. Git Integration & PR Automation
* Creates a new branch
* Commits AI-generated changes
* Pushes updates to remote
* Generates a Pull Request with files modified, issues fixed, and summary of improvements

---

## Project Structure

```
ai-dev-workflow-automation/
├── dummy_project/               # Target Python application
│   ├── app/                     # All application code lives here
│   │   ├── main.py              # FastAPI entry point — app init + router registration
│   │   ├── dependencies.py      # DB session dependency injection (get_db)
│   │   ├── utils.py             # Pure helpers: format_data, calculate_average
│   │   ├── core/
│   │   │   ├── db.py            # Engine, SessionLocal, Base (reads from .env)
│   │   │   └── models.py        # SQLAlchemy ORM models: User, UserScore
│   │   ├── repositories/
│   │   │   └── users.py         # Raw DB query functions (SQLAlchemy session-based)
│   │   ├── services/
│   │   │   └── users.py         # Business logic — fetch, create, add/update scores
│   │   ├── routes/
│   │   │   └── users.py         # HTTP handlers — routing + error mapping only
│   │   └── schemas/
│   │       └── user.py          # Pydantic request/response models
│   ├── cli.py                   # CLI entry point — session lifecycle + formatted output
│   ├── seed.py                  # Dev-only script to populate test data
│   ├── requirements.txt         # Python dependencies
│   ├── alembic.ini              # Alembic configuration
│   ├── .env                     # DB credentials (not committed)
│   └── migrations/              # Alembic migration scripts
│       └── versions/
│           └── 4d41c850d44c_init_schema.py
├── .claude/                     # Claude Code project config
│   ├── specs/
│   │   ├── 01-database-setup.md
│   │   └── 02-fastapi-setup.md
│   └── plans/
│       ├── 01-database-setup.md
│       └── 02-fastapi-setup.md
├── CLAUDE.md                    # Claude Code guidance
├── README.md
├── .gitignore
├── run.sh                       # Convenience launcher (activates venv, runs CLI)
└── venv/                        # Python virtual environment (not committed)
```

---

## Getting Started

### Prerequisites

* Python 3.13+
* MySQL 8+

### Setup

```bash
# 1. Activate the virtual environment
source venv/bin/activate

# 2. Install dependencies
pip install -r dummy_project/requirements.txt

# 3. Configure database credentials
#    Edit dummy_project/.env with your MySQL details:
#    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# 4. Create the database
mysql -u root -p -e "CREATE DATABASE user_db;"

# 5. Apply migrations
cd dummy_project && alembic upgrade head

# 6. Seed test data
python seed.py
```

### Run — CLI

```bash
# From project root (convenience launcher)
./run.sh

# Or manually
source venv/bin/activate
cd dummy_project && python cli.py
```

### Run — REST API

```bash
source venv/bin/activate
cd dummy_project
uvicorn app.main:app --reload --port 8000
```

API is live at `http://localhost:8000`  
Interactive Swagger UI at `http://localhost:8000/docs`

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/users/{user_id}` | Fetch user + scores + average |
| `POST` | `/api/v1/users` | Create a new user |
| `POST` | `/api/v1/users/{user_id}/scores` | Add a score to a user |
| `PUT` | `/api/v1/users/{user_id}/scores/{score_id}` | Update an existing score |

---

## Architecture — Request & Data Flow

### API request flow

```
HTTP Request
  → app/main.py                  (FastAPI app)
  → app/routes/users.py          (routing + session injection + HTTPException mapping)
  → app/services/users.py        (business logic + validation)
  → app/repositories/users.py    (DB queries via SQLAlchemy)
  → MySQL
  → JSON Response
```

### CLI data flow

```
cli.py → app/services/users.py → app/repositories/users.py + app/utils.py
```

Shared infrastructure: `app/core/db.py` (engine/session) and `app/core/models.py` (ORM models).

---

## Tech Stack

* Python 3.13
* FastAPI + Uvicorn (REST API server)
* Pydantic v2 (request/response validation)
* SQLAlchemy (ORM, session-per-request pattern)
* Alembic (schema migrations)
* MySQL 8+ via pymysql
* python-dotenv (env-based config)
* Claude Code (VS Code AI agent)
* Structured prompt engineering
* Git (branching, commits, PR workflow)

---

## Key Highlights

* WAT Framework (Workflow–Action–Test) implementation
* Clean layered architecture: core → repositories → services → routes
* MySQL-backed database with Alembic-managed schema migrations
* SQLAlchemy ORM with session-per-request pattern
* Workflow-driven AI system (not just prompts)
* Multi-step reasoning: planning → execution → validation
* Codebase-level automation (not single-file fixes)
* Integration with real development workflows

---

## Concept

> AI should not just assist developers — it should execute structured workflows within real systems.

This project demonstrates how combining structured workflows, LLM reasoning, and system-level actions can transform AI into an **execution engine for software development**.

---

## Author

Jay Sabnis
