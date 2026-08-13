import logging

from .detail import enrich_listing
from .errors import BazosSniperError
from .http import BazosHttpError, HttpClient
from .listing import build_search_url, parse_listing_page
from .models import Listing

_LOGGER = logging.getLogger(__name__)


class BazosSniper:
    def __init__(self, http_client: HttpClient | None = None) -> None:
        self._http = http_client if http_client is not None else HttpClient()

    def search(self, query: str, limit: int = 20) -> list[Listing]:
        listings = self._load_listing_pages(query, limit)
        for listing in listings:
            try:
                enrich_listing(listing, self._get_text(listing.url))
            except BazosSniperError:
                _LOGGER.exception("Could not load detail: %s", listing.url)
        return listings

    def _load_listing_pages(self, query: str, limit: int) -> list[Listing]:
        url = build_search_url(query)
        listings: list[Listing] = []
        seen_listing_urls: set[str] = set()
        visited_pages: set[str] = set()

        while url and url not in visited_pages and len(listings) < limit:
            visited_pages.add(url)
            page_listings, next_url = parse_listing_page(self._get_text(url), url)
            if not page_listings:
                break
            for listing in page_listings:
                if listing.url in seen_listing_urls:
                    continue
                seen_listing_urls.add(listing.url)
                listings.append(listing)
                if len(listings) == limit:
                    break
            url = next_url
        return listings

    def _get_text(self, url: str) -> str:
        try:
            return self._http.get_text(url)
        except BazosHttpError as error:
            raise BazosSniperError(str(error)) from error

