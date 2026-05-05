# Plan: Add Audit Columns to Database Tables

## Context

The `users` and `user_scores` tables had no timestamps. Adding `created_at` and `updated_at` audit columns gives visibility into when records were created and last modified — useful for debugging, data audits, and future features like change history. These are standard audit fields that every production table should carry.

---

## Scope

Touched only the minimum layers needed (bottom-up):

```
Migration (DB schema) → ORM models → Repositories (dict output) → Pydantic schemas
```

Services and routes layers were **not touched** — they pass dicts through without inspecting keys, so audit fields flow through automatically.

---

## Files Modified

| # | File | Change |
|---|------|--------|
| 1 | `dummy_project/app/core/models.py` | Added `TimestampMixin`; applied to `User` and `UserScore` |
| 2 | `dummy_project/migrations/versions/a1b2c3d4e5f6_add_audit_columns.py` | New Alembic migration chained from `4d41c850d44c` |
| 3 | `dummy_project/app/repositories/users.py` | All dict-returning functions include `created_at` and `updated_at` |
| 4 | `dummy_project/app/schemas/user.py` | `CreatedUserResponse`, `UserResponse`, `ScoreResponse` expose both audit fields |

---

## Step 1 — `dummy_project/app/core/models.py`

Added `TimestampMixin` using `server_default=func.now()` (MySQL `CURRENT_TIMESTAMP`) and `onupdate=func.now()`. Applied to both `User` and `UserScore`.

```python
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func

from app.core.db import Base


class TimestampMixin:
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)


class UserScore(TimestampMixin, Base):
    __tablename__ = "user_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)
```

---

## Step 2 — `dummy_project/migrations/versions/a1b2c3d4e5f6_add_audit_columns.py`

New migration chained from `4d41c850d44c` (init schema). Uses `sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')` for `updated_at` — the correct MySQL-native syntax for server-side auto-update. `nullable=False` is safe because MySQL populates existing rows using the server default when adding a column.

```python
revision: str = 'a1b2c3d4e5f6'
down_revision = '4d41c850d44c'

def upgrade() -> None:
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')))
    op.add_column('user_scores', sa.Column('created_at', sa.DateTime(), nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')))
    op.add_column('user_scores', sa.Column('updated_at', sa.DateTime(), nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')))

def downgrade() -> None:
    op.drop_column('user_scores', 'updated_at')
    op.drop_column('user_scores', 'created_at')
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
```

---

## Step 3 — `dummy_project/app/repositories/users.py`

After `session.refresh()`, all server-generated columns are populated. For `get_user_from_db`, `session.get()` already fetches all columns from the DB row.

Updated 4 functions to include audit fields in returned dicts:

- `get_user_from_db` → `"created_at": user.created_at, "updated_at": user.updated_at`
- `create_user_in_db` → `"created_at": user.created_at, "updated_at": user.updated_at`
- `add_score_to_db` → `"created_at": entry.created_at, "updated_at": entry.updated_at`
- `update_score_in_db` → `"created_at": entry.created_at, "updated_at": entry.updated_at`

`get_scores_for_user` returns `list[int]` — unchanged.

`services/users.py` line 34 does `{**user, "scores": scores, "average_score": avg}` — audit fields from `get_user_from_db` automatically propagate into `UserResponse` with no service changes needed.

---

## Step 4 — `dummy_project/app/schemas/user.py`

Added `from datetime import datetime`. Extended three response models:

- `CreatedUserResponse` → `created_at: datetime`, `updated_at: datetime`
- `UserResponse` → `created_at: datetime`, `updated_at: datetime`
- `ScoreResponse` → `created_at: datetime`, `updated_at: datetime`

Request models left unchanged — clients never send audit fields.

---

## Applying the Migration

```bash
cd dummy_project
alembic upgrade head
# Confirmed: a1b2c3d4e5f6 (head)
```

MySQL column structure confirmed:

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| `created_at` | datetime | NO | CURRENT_TIMESTAMP |
| `updated_at` | datetime | NO | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

---

## Verification

```bash
# Migration state
alembic current  # → a1b2c3d4e5f6 (head)

# API — create user, response must include created_at and updated_at
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "age": 25}'

# API — add score, ScoreResponse must include created_at and updated_at
curl -X POST http://localhost:8000/api/v1/users/1/scores \
  -H "Content-Type: application/json" \
  -d '{"score": 90}'
```

```sql
-- Rollback (if needed)
-- alembic downgrade 4d41c850d44c
```