import logging
from typing import Optional

from database import get_user_from_db
from utils import calculate_average

logger = logging.getLogger(__name__)


def get_user_data(user_id: str) -> dict:
    try:
        uid = int(user_id)
    except (ValueError, TypeError) as e:
        logger.error("Invalid user_id %r: %s", user_id, e)
        raise ValueError(f"user_id must be a valid integer, got: {user_id!r}") from e

    try:
        user = get_user_from_db(uid)
    except KeyError:
        logger.error("User %d not found in database", uid)
        raise ValueError(f"No user found with id: {uid}")
    except Exception:
        logger.exception("Unexpected error fetching user %d from database", uid)
        raise

    scores: list[int] = [10, 20, 30, 40]
    avg: Optional[float]
    try:
        avg = calculate_average(scores)
    except (ZeroDivisionError, ValueError) as e:
        logger.warning("Could not compute average score for user %d: %s", uid, e)
        avg = None

    result = {**user, "average_score": avg}
    logger.debug("Fetched data for user %d: %s", uid, result)
    return result