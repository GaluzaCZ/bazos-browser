from datetime import date
from pathlib import Path

import pytest

from bazos.detail import enrich_offer
from core.models import Offer


FIXTURES = Path(__file__).parent / "fixtures"


class FakeHttpClient:
    def __init__(self, html: str):
        self.html = html
        self.requested_urls: list[str] = []

    def get_text(self, url: str) -> str:
        self.requested_urls.append(url)
        return self.html


def make_offer(**changes) -> Offer:
    values = {
        "source": "bazos",
        "id": "221902833",
        "title": "Zkrácený titulek",
        "url": "https://auto.bazos.cz/inzerat/221902833/bmw.php",
    }
    values.update(changes)
    return Offer(**values)


def test_enrich_offer_reads_complete_detail_and_only_gallery_images():
    html = (FIXTURES / "bazos_detail.html").read_text(encoding="utf-8")
    client = FakeHttpClient(html)

    offer = enrich_offer(make_offer(), client)

    assert client.requested_urls == [offer.url]
    assert offer.title == "BMW F31 320d xDrive"
    assert offer.description == "První řádek plného popisu.\nDruhý řádek popisu."
    assert offer.seller == "Jan Novák"
    assert offer.phone == "+420 777 123 456"
    assert offer.location == "Praha 100 00"
    assert offer.price == 349_000
    assert offer.views == 1_234
    assert offer.published_at == date(2026, 7, 28)
    assert offer.image_urls == [
        "https://auto.bazos.cz/img/1/123/221902833.jpg",
        "https://www.bazos.cz/img/2/123/221902833.jpg",
    ]
    assert "https://www.bazos.cz/obrazky/bazos.svg" not in offer.image_urls
    assert "https://example.com/reklama.jpg" not in offer.image_urls


def test_enrich_offer_keeps_publicly_masked_phone_and_textual_price():
    html = (FIXTURES / "bazos_detail_masked.html").read_text(encoding="utf-8")

    offer = enrich_offer(make_offer(price=100_000), FakeHttpClient(html))

    assert offer.phone == "777 XXX XXX"
    assert offer.price is None
    assert offer.location == "Brno 602 00"
    assert offer.views == 98


@pytest.mark.parametrize("price_text", ["Dohodou", "V textu"])
def test_enrich_offer_maps_textual_prices_to_none(price_text: str):
    html = f"""
    <table><tr><td>Cena:</td><td>{price_text}</td></tr></table>
    """

    offer = enrich_offer(make_offer(price=42), FakeHttpClient(html))

    assert offer.price is None


def test_enrich_offer_tolerates_missing_optional_fields():
    offer = make_offer(
        price=10_000,
        location="Původní lokalita",
        description="Původní popis",
        image_urls=["https://www.bazos.cz/img/thumbnail.jpg"],
        published_at=date(2026, 7, 1),
        views=12,
    )

    enriched = enrich_offer(offer, FakeHttpClient("<html><body></body></html>"))

    assert enriched is offer
    assert offer.phone is None
    assert offer.seller is None
    assert offer.price == 10_000
    assert offer.location == "Původní lokalita"
    assert offer.description == "Původní popis"
    assert offer.image_urls == ["https://www.bazos.cz/img/thumbnail.jpg"]
    assert offer.published_at == date(2026, 7, 1)
    assert offer.views == 12
