import re
import sys
from collections import defaultdict
from prettytable import PrettyTable
from datetime import datetime


def parse_log_line(line: str) -> dict:
    m = re.search(r"^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s([A-Z]+)\s(.*)$", line)
    if m is None:
        raise ValueError(f"Invalid log line: {line}")

    parsed_date = m.group(1)

    # Parsing date to make sure it is valid.
    # All the exceptions are handled in the outer scope
    datetime.strptime(parsed_date, "%Y-%m-%d %H:%M:%S")

    return {
        "datetime": m.group(1),
        "level": m.group(2),
        "text": m.group(3),
    }


def load_logs(file_path: str) -> list:
    with open(file_path, mode='r') as open_file_object:
        return open_file_object.readlines()


def filter_logs_by_level(parsed_logs: list, level: str) -> list:
    return filter(lambda parsed_log: (parsed_log["level"] == level), parsed_logs)


def count_logs_by_level(parsed_logs: list) -> dict:
    res = defaultdict(int)

    for parsed_line in parsed_logs:
        current_level = parsed_line["level"]
        res[current_level] += 1

    return res


def display_log_counts(counts: dict):
    table = PrettyTable()
    table.align = "l"

    table.field_names = ["Рівень логування", "Кількість"]

    for level, count in counts.items():
        table.add_row([level, count])

    print(table)


def main(path: str, level: str = "") -> None:
    parsed_logs = []

    for line in load_logs(path):
        parsed_logs.append(parse_log_line(line))

    display_log_counts(count_logs_by_level(parsed_logs))
    filtered_logs = filter_logs_by_level(parsed_logs, level.upper())

    if len(filtered_logs) > 0:
        print(f"\nДеталі логів для рівня {level}")
        print("\n".join([f"{x["datetime"]} - {x["text"]}" for x in filtered_logs]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python exercise3.py <path> [<level>]")

    try:
        main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")
    except FileNotFoundError as error:
        sys.exit(str(error))
    except ValueError as error:
        sys.exit(str(error))
