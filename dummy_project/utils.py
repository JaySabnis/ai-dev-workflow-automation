def format_data(data):
    result = ""

    for key in data:
        result += key + ":" + str(data[key]) + "\n"

    return result



def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]

    return total / len(numbers)