from db import SessionLocal
from service import get_user_data
from utils import format_data


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
