from datetime import date
from pathlib import Path

from bazos.search import parse_listing


def test_parse_listing_reads_title_from_heading_and_price_from_card_sibling():
    html = (Path(__file__).parent / "fixtures" / "bazos_listing.html").read_text(encoding="utf-8")

    offers, next_url = parse_listing(html, "https://auto.bazos.cz/inzeraty/osobni/")

    assert [(offer.id, offer.title, offer.price) for offer in offers] == [
        ("208647053", "BMW F31 320d M paket", 349_000),
        ("208647054", "Škoda Octavia", None),
    ]
    assert offers[0].published_at == date(2026, 7, 15)
    assert next_url == "https://auto.bazos.cz/inzeraty/osobni/?strana=2"


def test_parse_listing_never_uses_entire_card_text_as_price():
    html = '<div class="inzeraty"><h2><a href="/inzerat/1/a.php">Title</a></h2> 2026 100</div>'

    offers, _ = parse_listing(html)

    assert offers[0].title == "Title"
    assert offers[0].price is None
