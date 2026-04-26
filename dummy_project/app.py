from service import get_user_data
from utils import format_data

def main():
    user_id = input("Enter user id: ")

    data = get_user_data(user_id)

    formatted = format_data(data)
    print("User Data:", formatted)


if __name__ == "__main__":
    main()