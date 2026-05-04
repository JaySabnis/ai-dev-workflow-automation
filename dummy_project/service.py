import logging
from typing import Optional

from sqlalchemy.orm import Session

from database import (
    get_user_from_db, get_scores_for_user,
    create_user_in_db, add_score_to_db, update_score_in_db,
)
from utils import calculate_average

logger = logging.getLogger(__name__)


def get_user_data(user_id: str, session: Session) -> dict:
    try:
        uid = int(user_id)
    except (ValueError, TypeError) as e:
        logger.error("Invalid user_id %r: %s", user_id, e)
        raise ValueError(f"user_id must be a valid integer, got: {user_id!r}") from e

    try:
        user = get_user_from_db(session, uid)
    except KeyError:
        logger.error("User %d not found in database", uid)
        raise ValueError(f"No user found with id: {uid}")
    except Exception:
        logger.exception("Unexpected error fetching user %d from database", uid)
        raise

    scores: list[int] = get_scores_for_user(session, uid)
    avg: Optional[float] = calculate_average(scores)

    result = {**user, "scores": scores, "average_score": avg}
    logger.debug("Fetched data for user %d: %s", uid, result)
    return result


def create_user(name: str, age: int, session: Session) -> dict:
    return create_user_in_db(session, name, age)


def add_score_for_user(user_id: int, score: int, session: Session) -> dict:
    get_user_from_db(session, user_id)
    return add_score_to_db(session, user_id, score)


def update_score_for_user(user_id: int, score_id: int, new_score: int, session: Session) -> dict:
    get_user_from_db(session, user_id)
    return update_score_in_db(session, score_id, new_score)
