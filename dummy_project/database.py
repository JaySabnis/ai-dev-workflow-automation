def get_user_from_db(user_id):
    users = {
        1: {"name": "Jay", "age": 25},
        2: {"name": "Alice", "age": 30},
        3: {"name": "Bob", "age": 35}
    }

    return users[user_id]  # KeyError risk