from offers import MarketplaceProvider, OfferRepository, SearchCriteria

from .analysis import normalize_title, score_offer
from .models import SearchResult


class SearchApplication:
    def __init__(
        self,
        provider: MarketplaceProvider,
        repository: OfferRepository,
    ) -> None:
        self._provider = provider
        self._repository = repository

    def execute(
        self,
        criteria: SearchCriteria,
        limit: int | None = None,
    ) -> list[SearchResult]:
        offers = self._provider.search(criteria, limit)
        results: list[SearchResult] = []

        for offer in offers:
            self._repository.save(offer)
            results.append(
                SearchResult(
                    offer=offer,
                    vehicle=normalize_title(offer.title),
                    score=score_offer(offer),
                )
            )
        return results
