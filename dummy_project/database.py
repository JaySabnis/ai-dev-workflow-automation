from sqlalchemy.orm import Session
from models import User, UserScore


def get_user_from_db(session: Session, user_id: int) -> dict:
    user = session.get(User, user_id)
    if user is None:
        raise KeyError(f"User {user_id} not found")
    return {"name": user.name, "age": user.age}


def get_scores_for_user(session: Session, user_id: int) -> list[int]:
    rows = session.query(UserScore.score).filter(UserScore.user_id == user_id).all()
    return [row.score for row in rows]
