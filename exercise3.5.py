import re
import sys
from collections import defaultdict
from typing import Generator
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
        "datetime": parsed_date,
        "level": m.group(2),
        "text": m.group(3),
    }


def load_logs(file_path: str) -> Generator[str, None, None]:
    with open(file_path, mode='r') as open_file_object:
        for line in open_file_object:
            yield line


def display_log_counts(counts: defaultdict):
    table = PrettyTable()
    table.align = "l"

    table.field_names = ["Рівень логування", "Кількість"]

    for level, count in counts.items():
        table.add_row([level, count])

    print(table)


def main(path: str, levels: list = ()) -> None:
    count_logs_by_level = defaultdict(int)
    filtered_logs = {}

    levels = [x.upper() for x in levels]

    for line in load_logs(path):
        parsed_line = parse_log_line(line)
        current_level = parsed_line["level"]
        count_logs_by_level[current_level] += 1
        if current_level in levels:
            if filtered_logs.get(current_level) is None:
                filtered_logs[current_level] = f"\nДеталі логів для рівня {current_level}"
            filtered_logs[current_level] += f"\n{parsed_line["datetime"]} - {parsed_line['text']}"

    display_log_counts(count_logs_by_level)
    print("\n".join(filtered_logs.values()))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python exercise3.py <path> [<levels>]")

    try:
        main(sys.argv[1], list(sys.argv[2:]))
    except FileNotFoundError as error:
        sys.exit(str(error))
    except ValueError as error:
        sys.exit(str(error))
