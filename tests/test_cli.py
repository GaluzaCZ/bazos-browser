from offers import SearchCriteria

from app.cli import parse_request


def test_cli_builds_search_criteria_and_keeps_default_limit() -> None:
    criteria, limit = parse_request(["--query", "bmw"])

    assert criteria == SearchCriteria(query="bmw")
    assert limit == 20
