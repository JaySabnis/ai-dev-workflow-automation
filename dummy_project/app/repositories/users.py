from sqlalchemy.orm import Session

from app.core.models import User, UserScore


def get_user_from_db(session: Session, user_id: int) -> dict:
    user = session.get(User, user_id)
    if user is None:
        raise KeyError(f"User {user_id} not found")
    return {"name": user.name, "age": user.age, "created_at": user.created_at, "updated_at": user.updated_at}


def get_scores_for_user(session: Session, user_id: int) -> list[int]:
    rows = session.query(UserScore.score).filter(UserScore.user_id == user_id).all()
    return [row.score for row in rows]


def create_user_in_db(session: Session, name: str, age: int) -> dict:
    user = User(name=name, age=age)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "name": user.name, "age": user.age, "created_at": user.created_at, "updated_at": user.updated_at}


def add_score_to_db(session: Session, user_id: int, score: int) -> dict:
    entry = UserScore(user_id=user_id, score=score)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return {"id": entry.id, "user_id": entry.user_id, "score": entry.score, "created_at": entry.created_at, "updated_at": entry.updated_at}


def update_score_in_db(session: Session, score_id: int, new_score: int) -> dict:
    entry = session.get(UserScore, score_id)
    if entry is None:
        raise KeyError(f"Score {score_id} not found")
    entry.score = new_score
    session.commit()
    session.refresh(entry)
    return {"id": entry.id, "user_id": entry.user_id, "score": entry.score, "created_at": entry.created_at, "updated_at": entry.updated_at}
