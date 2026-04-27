def format_data(data: dict) -> str:
    return "".join(f"{key}:{value}\n" for key, value in data.items())


def calculate_average(numbers: list[int]) -> int:
    if not numbers:
        raise ValueError("Cannot calculate average of an empty list")
    return sum(numbers) // len(numbers)