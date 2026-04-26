from database import get_user_from_db
from utils import calculate_average

def get_user_data(user_id):
    user = get_user_from_db(int(user_id))

    scores = [10, 20, 30, 40]

    avg = calculate_average(scores)

    user["average_score"] = avg

    
    return user