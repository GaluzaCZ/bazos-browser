from __future__ import annotations

import logging
from dataclasses import dataclass

from bozos_browser.domain.models import Offer, SearchResult
from bozos_browser.domain.errors import MarketplaceError
from bozos_browser.adapters.bazos.provider import BazosProvider
from bozos_browser.adapters.sqlite.repository import SqliteOfferRepository

from .analysis import normalize_title, score_offer

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class SearchRequest:
    query: str
    limit: int = 20


class SearchOffers:
    def __init__(
        self,
        provider: BazosProvider,
        repository: SqliteOfferRepository,
    ) -> None:
        self._provider = provider
        self._repository = repository

    def execute(self, request: SearchRequest) -> list[SearchResult]:
        offers = self._provider.search(request.query, request.limit)
        results: list[SearchResult] = []

        for offer in offers:
            detailed_offer = self._load_detail(offer)
            self._repository.upsert(detailed_offer)
            results.append(
                SearchResult(
                    offer=detailed_offer,
                    vehicle=normalize_title(detailed_offer.title),
                    score=score_offer(detailed_offer),
                )
            )

        return results

    def _load_detail(self, offer: Offer) -> Offer:
        try:
            return self._provider.load_detail(offer)
        except MarketplaceError:
            _LOGGER.exception("Could not load detail: %s", offer.url)
            return offer
