# FastAPI Integration Specification — User Data Service (v3)

## 1. Objective

Expose the existing system as a **REST API service** using FastAPI while:

- Reusing existing service and DB layers
- Maintaining strict separation of concerns
- Supporting fetch, create, and update operations

---

## 2. Architecture

```
Client (HTTP)
     ↓
API Layer (FastAPI)
     ↓
Service Layer (Business Logic)
     ↓
Database Layer (DB Access)
     ↓
MySQL
```

---

## 3. Required Libraries

- FastAPI → API framework
- Uvicorn → server runtime
- SQLAlchemy → DB interaction
- Pydantic → request/response validation

---

## 4. Installation & Verification

### Installation

```
pip install fastapi uvicorn sqlalchemy pydantic
```

---

### Verification

- Start server → no import errors
- API loads at `/docs` (Swagger UI)
- DB connection succeeds
- Endpoints respond correctly

---

## 5. Critical Files (Must Exist)

```
app/main.py              → API entry point
app/routes/              → API endpoints
app/schemas/             → request/response models
app/dependencies.py      → DB session management

service.py               → business logic (existing)
database.py              → DB functions (existing)
db.py                    → DB connection/session
utils.py                 → helper functions
```

---

## 6. Initialization Flow

### Application Startup

- Initialize FastAPI app
- Register all routes
- Ensure DB connection config is valid

---

### Request Initialization

For every request:

1. Create DB session
2. Inject session into route
3. Pass session to service layer
4. Close session after response

---

## 7. End-to-End Workflow

```
Request
  ↓
API Layer (routing + validation + session)
  ↓
Service Layer (logic + aggregation)
  ↓
Database Layer (queries)
  ↓
Service Layer (compute response)
  ↓
API Layer (JSON response)
  ↓
Client
```

---

## 8. API Endpoints

### 8.1 Fetch User

**GET /api/v1/users/{user_id}**

- Fetch user + scores
- Compute average
- Return structured JSON

---

### 8.2 Create User

**POST /api/v1/users**

- Validate input (name, age)
- Insert user into DB
- Return created entity

---

### 8.3 Add Score

**POST /api/v1/users/{user_id}/scores**

- Validate user exists
- Insert score
- Return confirmation

---

### 8.4 Update Score

**PUT /api/v1/users/{user_id}/scores/{score_id}**

- Validate user and score
- Update value
- Return updated result

---

## 9. Validation Strategy

- API layer → structure validation (via schemas)
- Service layer → business validation
- DB layer → assumes valid input

---

## 10. Business Logic Rules

- `user_id` must be valid integer
- User must exist before operations
- Scores linked via foreign key
- Average:
  - float value
  - `None` if no scores

---

## 11. Database Connection Strategy

- Centralized connection manager
- Session-per-request pattern
- Connection pooling enabled
- No global shared session

---

## 12. Error Handling

| Scenario        | Response |
|----------------|----------|
| Invalid input   | 400      |
| User not found  | 404      |
| Score not found | 404      |
| DB error        | 500      |

---

## 13. Constraints (Strict)

- API must NOT:
  - Contain business logic
  - Query DB directly

- Service must NOT:
  - Handle HTTP concepts

- DB layer must NOT:
  - Perform calculations

- Remove CLI formatting (`format_data`) from API flow

---

## 14. Refactoring Requirements

- Keep CLI optional, separate from API
- Ensure average uses float division
- Return JSON (not formatted strings)
- Maintain backward compatibility in service layer

---

## 15. Testing Strategy

### Functional Testing

- Test all endpoints:
  - Fetch user
  - Create user
  - Add score
  - Update score

---

### Validation Testing

- Invalid user_id
- Missing fields
- Non-existent user

---

### Database Testing

- Verify inserts/updates persist
- Verify foreign key integrity
- Verify average calculation correctness

---

### API Testing Tools

- Swagger UI (`/docs`)
- Postman / curl

---

## 16. Completion Criteria

- API runs successfully via server
- All endpoints functional
- DB session correctly managed
- JSON responses returned
- No logic duplication
- Clean separation of layers

---

## Final Insight

This is a **layered API system**, not just endpoint exposure:

- API = request orchestration
- Service = core logic
- DB = data access

Maintaining this separation is critical for scalability and maintainability.
