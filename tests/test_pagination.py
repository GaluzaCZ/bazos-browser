from bazos.search import search_offers
from core.models import SearchCriteria


class FakeHttpClient:
    def __init__(self, pages: dict[str, str]):
        self.pages = pages
        self.requested_urls: list[str] = []

    def get_text(self, url: str) -> str:
        self.requested_urls.append(url)
        return self.pages[url]


def listing_page(ids: list[int], next_href: str | None = None) -> str:
    cards = "".join(
        f"""
        <div class="inzeraty">
          <div class="inzeratynadpis">
            <h2 class="nadpis"><a href="/inzerat/{offer_id}/offer.php">Offer {offer_id}</a></h2>
          </div>
          <div class="inzeratycena">{offer_id} 000 Kč</div>
        </div>
        """
        for offer_id in ids
    )
    pagination = (
        f'<div class="strankovani"><a href="{next_href}"><b>Další</b></a></div>'
        if next_href is not None
        else ""
    )
    return cards + pagination


def paged_client() -> tuple[FakeHttpClient, str]:
    first_url = "https://auto.bazos.cz/inzeraty/osobni/?hledat=BMW"
    return (
        FakeHttpClient(
            {
                first_url: listing_page([1, 2], "/20/?hledat=BMW"),
                "https://auto.bazos.cz/20/?hledat=BMW": listing_page(
                    [2, 3], "/40/?hledat=BMW"
                ),
                "https://auto.bazos.cz/40/?hledat=BMW": listing_page([4]),
            }
        ),
        first_url,
    )


def test_search_pages_to_end_and_deduplicates_offer_urls():
    client, first_url = paged_client()

    offers = search_offers(SearchCriteria(url=first_url), limit=10, client=client)

    assert [offer.id for offer in offers] == ["1", "2", "3", "4"]
    assert client.requested_urls == [
        first_url,
        "https://auto.bazos.cz/20/?hledat=BMW",
        "https://auto.bazos.cz/40/?hledat=BMW",
    ]


def test_search_stops_exactly_at_limit():
    client, first_url = paged_client()

    offers = search_offers(SearchCriteria(url=first_url), limit=3, client=client)

    assert [offer.id for offer in offers] == ["1", "2", "3"]
    assert client.requested_urls == [first_url, "https://auto.bazos.cz/20/?hledat=BMW"]


def test_search_limit_smaller_than_first_page_does_not_fetch_next_page():
    client, first_url = paged_client()

    offers = search_offers(SearchCriteria(url=first_url), limit=1, client=client)

    assert [offer.id for offer in offers] == ["1"]
    assert client.requested_urls == [first_url]


def test_search_stops_after_empty_page():
    url = "https://auto.bazos.cz/inzeraty/osobni/"
    client = FakeHttpClient({url: listing_page([], "/20/")})

    assert search_offers(SearchCriteria(url=url), limit=10, client=client) == []
    assert client.requested_urls == [url]


def test_search_does_not_request_a_page_twice_when_pagination_cycles():
    url = "https://auto.bazos.cz/inzeraty/osobni/"
    client = FakeHttpClient({url: listing_page([1], url)})

    offers = search_offers(SearchCriteria(url=url), limit=10, client=client)

    assert [offer.id for offer in offers] == ["1"]
    assert client.requested_urls == [url]


def test_search_ignores_invalid_or_external_next_url():
    url = "https://auto.bazos.cz/inzeraty/osobni/"
    for next_href in ("javascript:void(0)", "https://example.com/next"):
        client = FakeHttpClient({url: listing_page([1], next_href)})

        offers = search_offers(SearchCriteria(url=url), limit=10, client=client)

        assert [offer.id for offer in offers] == ["1"]
        assert client.requested_urls == [url]
