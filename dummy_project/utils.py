def format_data(data: dict) -> str:
    return "".join(f"{key}:{value}\n" for key, value in data.items())


def calculate_average(numbers: list[int]) -> float | None:
    if not numbers:
        return None
    return sum(numbers) / len(numbers)