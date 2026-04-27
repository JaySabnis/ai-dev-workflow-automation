_USERS: dict[int, dict] = {
    1: {"name": "Jay", "age": 25},
    2: {"name": "Alice", "age": 30},
    3: {"name": "Bob", "age": 35},
}


def get_user_from_db(user_id: int) -> dict:
    if user_id not in _USERS:
        raise KeyError(f"User {user_id} not found")
    return _USERS[user_id]