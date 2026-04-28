# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repo demonstrates the **WAT Framework** (Workflow–Action–Test): a structured approach to AI-driven development where Claude acts as an execution engine rather than a simple assistant. The `dummy_project/` is a sample Python codebase used as the target for automated analysis, refactoring, and improvement workflows.

## Running the project

```bash
# Activate the virtual environment (Python 3.13)
source venv/bin/activate

# Run the app (prompts for a user ID: 1, 2, or 3)
cd dummy_project && python app.py
```

No external dependencies beyond the standard library — the venv currently only contains pip.

## Architecture

The `dummy_project/` is a 4-file layered Python app used as the AI automation target:

- `app.py` — Entry point. Reads user input, calls `service.get_user_data()`, prints formatted result.
- `service.py` — Orchestration layer. Validates input, fetches from DB, computes average score, returns merged dict.
- `database.py` — In-memory store (`_USERS` dict). `get_user_from_db(int)` raises `KeyError` on miss.
- `utils.py` — Two pure functions: `format_data(dict) -> str` and `calculate_average(list[int]) -> int`.

Data flow: `app.py` → `service.py` → `database.py` + `utils.py`

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