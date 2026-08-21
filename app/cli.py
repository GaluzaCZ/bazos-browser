import argparse
from collections.abc import Iterable, Sequence

from offers import SearchCriteria

from .models import SearchResult


def parse_request(
    argv: Sequence[str] | None = None,
) -> tuple[SearchCriteria, int]:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=_positive_integer, default=20)
    arguments = parser.parse_args(argv)
    return SearchCriteria(query=arguments.query), arguments.limit


def print_results(results: Iterable[SearchResult]) -> None:
    for result in results:
        print(format_result(result))


def format_result(result: SearchResult) -> str:
    offer = result.offer
    price = offer.price or "dohodou"
    return (
        f"[{result.score:3}] {offer.title} | {price} | "
        f"{offer.url} | {result.vehicle}"
    )


def _positive_integer(value: str) -> int:
    parsed_value = int(value)
    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed_value
