import argparse
from collections.abc import Sequence

from bozos_browser.application.search_offers import SearchRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=_positive_integer, default=20)
    return parser


def parse_options(argv: Sequence[str] | None = None) -> SearchRequest:
    parser = build_parser()
    arguments = parser.parse_args(argv)
    return SearchRequest(query=arguments.query, limit=arguments.limit)


def _positive_integer(value: str) -> int:
    parsed_value = int(value)
    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed_value

