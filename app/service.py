from dataclasses import dataclass

from bazos_sniper import BazosSniper

from .analysis import normalize_title, score_listing
from .database import ListingRepository
from .models import SearchResult


@dataclass(frozen=True, slots=True)
class SearchRequest:
    query: str
    limit: int = 20


class SearchApplication:
    def __init__(
        self,
        bazos: BazosSniper,
        repository: ListingRepository,
    ) -> None:
        self._bazos = bazos
        self._repository = repository

    def execute(self, request: SearchRequest) -> list[SearchResult]:
        listings = self._bazos.search(request.query, request.limit)
        results: list[SearchResult] = []

        for listing in listings:
            self._repository.upsert(listing)
            results.append(
                SearchResult(
                    listing=listing,
                    vehicle=normalize_title(listing.title),
                    score=score_listing(listing),
                )
            )
        return results

