from datetime import datetime

from bazos_sniper import BazosProvider
from offers import Offer, SearchCriteria


LIST_PAGE = """
<div class="inzeraty">
  <div class="inzeratynadpis">
    <h2 class="nadpis"><a href="/inzerat/123/test.php">BMW 320d</a></h2>
    <div class="popis">Zachovalé auto</div>
    <span>22.8. 2026</span>
  </div>
  <div class="inzeratycena">150 000 Kč</div>
  <div class="inzeratylok">Praha</div>
</div>
<div class="inzeraty">
  <div class="inzeratynadpis">
    <h2 class="nadpis"><a href="/inzerat/456/test-2.php">BMW 330d</a></h2>
    <div class="popis">Druhé auto</div>
    <span>21.8. 2026</span>
  </div>
  <div class="inzeratycena">200 000 Kč</div>
  <div class="inzeratylok">Brno</div>
</div>
"""

DETAIL_PAGE = """
<h1 class="nadpisdetail">BMW 320d E90</h1>
<div class="popisdetail">Detailní popis</div>
"""


class FakeHttpClient:
    def get_text(self, url: str) -> str:
        return DETAIL_PAGE if "/inzerat/123/" in url else LIST_PAGE


def test_bazos_provider_returns_general_offer() -> None:
    offers = BazosProvider(FakeHttpClient()).search(
        SearchCriteria(query="bmw"),
        limit=1,
    )

    assert len(offers) == 1
    offer = offers[0]
    assert isinstance(offer, Offer)
    assert offer.source == "bazos"
    assert offer.external_id == "123"
    assert offer.title == "BMW 320d E90"
    assert offer.price == 150_000
    assert offer.published_at == datetime(2026, 8, 22)


def test_bazos_provider_accepts_no_limit() -> None:
    offers = BazosProvider(FakeHttpClient()).search(
        SearchCriteria(query="bmw"),
        limit=None,
    )

    assert [offer.external_id for offer in offers] == ["123", "456"]
