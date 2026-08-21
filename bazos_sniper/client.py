import logging

from offers import Offer, SearchCriteria

from .detail import enrich_offer
from .errors import BazosSniperError
from .http import BazosHttpError, HttpClient
from .listing import build_search_url, parse_listing_page

_LOGGER = logging.getLogger(__name__)


class BazosProvider:
    def __init__(self, http_client: HttpClient | None = None) -> None:
        self._http = http_client if http_client is not None else HttpClient()

    def search(
        self,
        criteria: SearchCriteria,
        limit: int | None = None,
    ) -> list[Offer]:
        offers = self._load_listing_pages(criteria.query, limit)
        for offer in offers:
            try:
                enrich_offer(offer, self._get_text(offer.url))
            except BazosSniperError:
                _LOGGER.exception("Could not load detail: %s", offer.url)
        return offers

    def _load_listing_pages(
        self,
        query: str,
        limit: int | None,
    ) -> list[Offer]:
        url = build_search_url(query)
        offers: list[Offer] = []
        seen_offer_urls: set[str] = set()
        visited_pages: set[str] = set()

        while (
            url
            and url not in visited_pages
            and (limit is None or len(offers) < limit)
        ):
            visited_pages.add(url)
            page_offers, next_url = parse_listing_page(self._get_text(url), url)
            if not page_offers:
                break
            for offer in page_offers:
                if offer.url in seen_offer_urls:
                    continue
                seen_offer_urls.add(offer.url)
                offers.append(offer)
                if limit is not None and len(offers) == limit:
                    break
            url = next_url
        return offers

    def _get_text(self, url: str) -> str:
        try:
            return self._http.get_text(url)
        except BazosHttpError as error:
            raise BazosSniperError(str(error)) from error
