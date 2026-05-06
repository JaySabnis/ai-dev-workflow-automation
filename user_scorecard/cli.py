from app.core.db import SessionLocal
from app.services.users import get_user_data
from app.utils import format_data


def main():
    user_id = input("Enter user id: ")
    session = SessionLocal()
    try:
        data = get_user_data(user_id, session)
        formatted = format_data(data)
        print("User Data:", formatted)
    finally:
        session.close()


if __name__ == "__main__":
    main()
