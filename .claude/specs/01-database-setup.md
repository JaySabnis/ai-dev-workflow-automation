# Database Setup Specification — User Data Service

## 1. Objective
Define and manage a **MySQL-backed database layer** with:
- Structured schema (users, user_scores)
- Reliable connection management
- Version-controlled schema evolution
- Clean integration with application layer

---

## 2. Database Technology
- Database: MySQL 8+
- ORM: SQLAlchemy
- Migration Tool: Alembic
- Driver: pymysql

---

## 3. Database Creation

### Create Database
```sql
CREATE DATABASE user_db;
```

### Connection URL Format
```
mysql+pymysql://<username>:<password>@localhost:3306/user_db
```

---

## 4. Schema Design

### users
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL
);
```

### user_scores
```sql
CREATE TABLE user_scores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    score INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## 5. ORM Models (SQLAlchemy)

### User Model
```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
```

### UserScore Model
```python
class UserScore(Base):
    __tablename__ = "user_scores"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)
```

---

## 6. Database Connection Layer
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/user_db"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
```

---

## 7. Session Management
- One session per request
- Always close session after use
- Use dependency injection in API layer

---

## 8. Schema Management (Migrations)

### Initialize
```bash
alembic init migrations
```

### Configure
Set DB URL in `alembic.ini`

### Generate Migration
```bash
alembic revision --autogenerate -m "init schema"
```

### Apply Migration
```bash
alembic upgrade head
```

### Rollback
```bash
alembic downgrade -1
```

---

## 9. Migration Rules
- Never modify tables manually in production
- All schema changes must go through Alembic
- Each change = new migration file
- Keep migrations small and atomic

---

## 10. Constraints & Integrity
- `user_id` must reference existing user
- Use `ON DELETE CASCADE`
- Fields required unless explicitly nullable

---

## 11. Indexing (Recommended)
```sql
CREATE INDEX idx_user_id ON user_scores(user_id);
```

---

## 12. Environment Configuration
```
DB_USER=root
DB_PASSWORD=***
DB_HOST=localhost
DB_PORT=3306
DB_NAME=user_db
```

---

## 13. Development vs Production

| Environment | Strategy |
|------------|--------|
| Local dev | Optional create_all() |
| Staging/Prod | Alembic only |

---

## 14. Dependencies
```
sqlalchemy
alembic
pymysql
```

---

## 15. Key Rules
- Do NOT rely on create_all() in production
- Use migrations for every schema change
- Keep DB logic separate from business logic
- Ensure referential integrity
