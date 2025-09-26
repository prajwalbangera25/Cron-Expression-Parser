import sys

def expand_field(field, min_val, max_val):
    """Expand a single cron field into a list of integers."""
    result = []
    if field == "*":
        return list(range(min_val, max_val + 1))
    for part in field.split(","):
        if "/" in part:  # step values
            base, step = part.split("/")
            step = int(step)
            if base == "*":
                start, end = min_val, max_val
            elif "-" in base:
                start, end = map(int, base.split("-"))
            else:
                start = int(base)
                end = max_val
            result.extend(range(start, end + 1, step))
        elif "-" in part:  # range
            start, end = map(int, part.split("-"))
            result.extend(range(start, end + 1))
        else:  # single value
            result.append(int(part))
    return sorted(set(result))


def parse_cron(cron_str):
    fields = cron_str.split()
    if len(fields) < 6:
        raise ValueError("Invalid cron expression. Must have 5 fields + command.")

    minute, hour, day_month, month, day_week = fields[:5]
    command = " ".join(fields[5:])

    expanded = {
        "minute": expand_field(minute, 0, 59),
        "hour": expand_field(hour, 0, 23),
        "day of month": expand_field(day_month, 1, 31),
        "month": expand_field(month, 1, 12),
        "day of week": expand_field(day_week, 0, 6),
        "command": command,
    }
    return expanded


def format_output(expanded):
    for key, val in expanded.items():
        if key == "command":
            print(f"{key:<14}{val}")
        else:
            print(f"{key:<14}{' '.join(map(str, val))}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cron_parser.py \"<cron_expression>\"")
        sys.exit(1)

    cron_expression = sys.argv[1]
    expanded = parse_cron(cron_expression)
    format_output(expanded)
