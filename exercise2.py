import re


def sum_profit(text_with_numbers, generator_func):
    return sum(generator_func(text_with_numbers))


def generator_numbers(text_with_numbers):
    for res in re.findall(r"\b\d+.\d+\b", text_with_numbers):
        yield float(res)


text = ("Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими "
        "надходженнями 27.45 і 324.00 доларів.")

total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")
