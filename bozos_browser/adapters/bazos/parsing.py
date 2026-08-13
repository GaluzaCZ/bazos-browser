import re
from datetime import date, datetime


def parse_integer(value: str) -> int | None:
    digits = re.sub(r"[^0-9]", "", value)
    return int(digits) if digits else None


def parse_date(value: str) -> date | None:
    match = re.search(r"\b\d{1,2}\.\d{1,2}\.\s*\d{4}\b", value)
    if match:
        value = match.group(0)
    for date_format in ("%d.%m.%Y", "%d.%m. %Y"):
        try:
            return datetime.strptime(value.strip(), date_format).date()
        except ValueError:
            continue
    return None

