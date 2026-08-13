from bozos_browser.adapters.http import HttpClientError, RequestsHttpClient
from bozos_browser.domain.models import Offer
from bozos_browser.domain.errors import MarketplaceError

from .detail import enrich_offer_from_html
from .listing import build_search_url, parse_listing


class BazosProvider:
    def __init__(self, client: RequestsHttpClient) -> None:
        self._client = client

    def search(self, query: str, limit: int) -> list[Offer]:
        url = build_search_url(query)
        offers: list[Offer] = []
        seen_offer_urls: set[str] = set()
        visited_pages: set[str] = set()

        while url and url not in visited_pages and len(offers) < limit:
            visited_pages.add(url)
            page_offers, next_url = parse_listing(self._get_text(url), url)
            if not page_offers:
                break
            for offer in page_offers:
                if offer.url in seen_offer_urls:
                    continue
                seen_offer_urls.add(offer.url)
                offers.append(offer)
                if len(offers) == limit:
                    break
            url = next_url

        return offers

    def load_detail(self, offer: Offer) -> Offer:
        return enrich_offer_from_html(offer, self._get_text(offer.url))

    def _get_text(self, url: str) -> str:
        try:
            return self._client.get_text(url)
        except HttpClientError as error:
            raise MarketplaceError(str(error)) from error
