# Implementation Plan: FastAPI Integration — User Data Service

## Context

The `dummy_project/` currently exposes its business logic only via a CLI (`app.py`). This plan adds a FastAPI REST API layer on top of the existing service and database layers, following the spec at `.claude/specs/02-fastapi-setup.md`. The goal is to expose 4 endpoints (fetch user, create user, add score, update score) without duplicating logic or violating layer boundaries.

---

## Files to Modify

### 1. `dummy_project/requirements.txt`
Add FastAPI ecosystem dependencies:
```
fastapi
uvicorn
pydantic
```

### 2. `dummy_project/utils.py`
Fix `calculate_average` per spec §14:
- Change integer division `//` → float division `/`
- Return `None` on empty list instead of raising `ValueError`

```python
def calculate_average(numbers: list[int]) -> float | None:
    if not numbers:
        return None
    return sum(numbers) / len(numbers)
```

> **Note:** `service.py::get_user_data` already catches `ValueError`/`ZeroDivisionError` and sets `avg = None` — after this fix, that except branch becomes dead code but is harmless. No change needed to service.py for this.

### 3. `dummy_project/database.py`
Add 3 new DB functions (no calculations, pure data access):

```python
def create_user_in_db(session: Session, name: str, age: int) -> dict:
    user = User(name=name, age=age)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "name": user.name, "age": user.age}

def add_score_to_db(session: Session, user_id: int, score: int) -> dict:
    entry = UserScore(user_id=user_id, score=score)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return {"id": entry.id, "user_id": entry.user_id, "score": entry.score}

def update_score_in_db(session: Session, score_id: int, new_score: int) -> dict:
    entry = session.get(UserScore, score_id)
    if entry is None:
        raise KeyError(f"Score {score_id} not found")
    entry.score = new_score
    session.commit()
    session.refresh(entry)
    return {"id": entry.id, "user_id": entry.user_id, "score": entry.score}
```

### 4. `dummy_project/service.py`
Add 3 new service functions (business validation only, no HTTP concepts):

```python
def create_user(name: str, age: int, session: Session) -> dict:
    # business rule: age must be positive
    return create_user_in_db(session, name, age)

def add_score_for_user(user_id: int, score: int, session: Session) -> dict:
    # validate user exists first
    get_user_from_db(session, user_id)   # raises KeyError if not found
    return add_score_to_db(session, user_id, score)

def update_score_for_user(user_id: int, score_id: int, new_score: int, session: Session) -> dict:
    # validate user exists
    get_user_from_db(session, user_id)
    # update_score_in_db raises KeyError if score_id not found
    return update_score_in_db(session, score_id, new_score)
```

---

## New Files to Create

### 5. `dummy_project/app/__init__.py`
Empty file (marks directory as package).

### 6. `dummy_project/app/dependencies.py`
FastAPI dependency for session-per-request injection:

```python
from db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 7. `dummy_project/app/schemas/__init__.py`
Empty file.

### 8. `dummy_project/app/schemas/user.py`
Pydantic request/response models:

```python
from pydantic import BaseModel
from typing import Optional

# Requests
class CreateUserRequest(BaseModel):
    name: str
    age: int

class AddScoreRequest(BaseModel):
    score: int

class UpdateScoreRequest(BaseModel):
    score: int

# Responses
class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    scores: list[int]
    average_score: Optional[float]

class ScoreResponse(BaseModel):
    id: int
    user_id: int
    score: int

class CreatedUserResponse(BaseModel):
    id: int
    name: str
    age: int
```

### 9. `dummy_project/app/routes/__init__.py`
Empty file.

### 10. `dummy_project/app/routes/users.py`
All 4 endpoint handlers — routing + validation + session injection only, no business logic:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.user import (
    CreateUserRequest, AddScoreRequest, UpdateScoreRequest,
    UserResponse, ScoreResponse, CreatedUserResponse
)
import service

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
def fetch_user(user_id: int, db: Session = Depends(get_db)):
    try:
        data = service.get_user_data(str(user_id), db)
        return {**data, "id": user_id, "scores": data.get("scores", [])}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")


@router.post("", response_model=CreatedUserResponse, status_code=201)
def create_user(body: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        return service.create_user(body.name, body.age, db)
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")


@router.post("/{user_id}/scores", response_model=ScoreResponse, status_code=201)
def add_score(user_id: int, body: AddScoreRequest, db: Session = Depends(get_db)):
    try:
        return service.add_score_for_user(user_id, body.score, db)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")


@router.put("/{user_id}/scores/{score_id}", response_model=ScoreResponse)
def update_score(user_id: int, score_id: int, body: UpdateScoreRequest, db: Session = Depends(get_db)):
    try:
        return service.update_score_for_user(user_id, score_id, body.score, db)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")
```

### 11. `dummy_project/app/main.py`
FastAPI app entry point:

```python
from fastapi import FastAPI
from app.routes.users import router as users_router

app = FastAPI(title="User Data Service", version="1.0.0")
app.include_router(users_router)
```

---

## Running the Server

```bash
source venv/bin/activate
cd dummy_project
uvicorn app.main:app --reload --port 8000
```

API docs available at: `http://localhost:8000/docs`

---

## Verification Plan

### Step 1: Dependency install
```bash
pip install fastapi uvicorn pydantic
```

### Step 2: Server starts cleanly
```bash
uvicorn app.main:app --reload --port 8000
# Expect: no import errors, Uvicorn running
```

### Step 3: Endpoint tests (via curl)

**Create user:**
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name": "TestUser", "age": 25}'
# Expect: 201 with {id, name, age}
```

**Add score:**
```bash
curl -X POST http://localhost:8000/api/v1/users/1/scores \
  -H "Content-Type: application/json" \
  -d '{"score": 95}'
# Expect: 201 with {id, user_id, score}
```

**Fetch user:**
```bash
curl http://localhost:8000/api/v1/users/1
# Expect: 200 with {id, name, age, scores, average_score}
```

**Update score:**
```bash
curl -X PUT http://localhost:8000/api/v1/users/1/scores/1 \
  -H "Content-Type: application/json" \
  -d '{"score": 99}'
# Expect: 200 with updated score
```

**404 case:**
```bash
curl http://localhost:8000/api/v1/users/9999
# Expect: 404
```

### Step 4: Swagger UI
- Open `http://localhost:8000/docs` — all 4 endpoints listed

---

## Critical Files Summary

| File | Action | Purpose |
|------|--------|---------|
| `dummy_project/requirements.txt` | Modify | Add fastapi, uvicorn, pydantic |
| `dummy_project/utils.py` | Modify | Fix calculate_average (float, None on empty) |
| `dummy_project/database.py` | Modify | Add create/add/update DB functions |
| `dummy_project/service.py` | Modify | Add create/add/update service functions |
| `dummy_project/app/__init__.py` | Create | Package marker |
| `dummy_project/app/main.py` | Create | FastAPI app entry point |
| `dummy_project/app/dependencies.py` | Create | DB session dependency |
| `dummy_project/app/schemas/__init__.py` | Create | Package marker |
| `dummy_project/app/schemas/user.py` | Create | Pydantic request/response models |
| `dummy_project/app/routes/__init__.py` | Create | Package marker |
| `dummy_project/app/routes/users.py` | Create | All 4 endpoint handlers |

---

## Layer Constraints (from spec §13)

- `routes/users.py` — routing, validation, session injection ONLY; no business logic, no direct DB calls
- `service.py` — business rules ONLY; no HTTPException, no status codes
- `database.py` — queries ONLY; no average calculation, no validation
- `format_data` from utils.py is NOT used anywhere in the API flow
