from db import SessionLocal
from models import User, UserScore


def seed():
    session = SessionLocal()
    try:
        if session.query(User).count() > 0:
            print("Database already seeded, skipping.")
            return

        users = [
            User(name="Jay", age=25),
            User(name="Alice", age=30),
            User(name="Bob", age=35),
        ]
        session.add_all(users)
        session.flush()

        scores = [10, 20, 30, 40]
        for user in users:
            for score in scores:
                session.add(UserScore(user_id=user.id, score=score))

        session.commit()
        print(f"Seeded {len(users)} users with {len(scores)} scores each.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
