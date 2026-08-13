import argparse
from collections.abc import Iterable, Sequence

from .models import SearchResult
from .service import SearchRequest


def parse_request(argv: Sequence[str] | None = None) -> SearchRequest:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=_positive_integer, default=20)
    arguments = parser.parse_args(argv)
    return SearchRequest(query=arguments.query, limit=arguments.limit)


def print_results(results: Iterable[SearchResult]) -> None:
    for result in results:
        print(format_result(result))


def format_result(result: SearchResult) -> str:
    listing = result.listing
    price = listing.price or "dohodou"
    return (
        f"[{result.score:3}] {listing.title} | {price} | "
        f"{listing.url} | {result.vehicle}"
    )


def _positive_integer(value: str) -> int:
    parsed_value = int(value)
    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed_value

