from datetime import date
from pathlib import Path

from bazos.search import build_search_url, parse_listing
from core.models import SearchCriteria


def test_parse_listing_reads_current_bazos_card_fields():
    html = (Path(__file__).parent / "fixtures" / "bazos_listing.html").read_text(encoding="utf-8")

    offers, next_url = parse_listing(html, "https://auto.bazos.cz/inzeraty/osobni/")

    assert [(offer.id, offer.title, offer.price) for offer in offers] == [
        ("221902833", "BMW 840d xDrive Gran Coupe", 1_199_900),
        ("221907051", "ŠKODA ROOMSTER 1,2 TSI", None),
    ]
    assert offers[0].published_at == date(2026, 7, 29)
    assert offers[0].location == "Olomouc 772 00"
    assert offers[0].views == 221
    assert offers[0].description == "Prodám BMW 840d ve výborném stavu ..."
    assert offers[0].image_urls == ["https://www.bazos.cz/img/1t/833/221902833.jpg"]
    assert next_url == "https://auto.bazos.cz/20/"


def test_parse_listing_never_uses_entire_card_text_as_price():
    html = """
    <div class="inzeraty">
      <div class="inzeratynadpis">
        <h2 class="nadpis"><a href="/inzerat/1/a.php">Title</a></h2>
        [29.7. 2026]
      </div>
      <div class="inzeratyview">100 x</div>
    </div>
    """

    offers, _ = parse_listing(html)

    assert offers[0].title == "Title"
    assert offers[0].price is None


def test_build_search_url_uses_names_from_bazos_form():
    criteria = SearchCriteria(
        query="BMW 320d",
        category="auto",
        location="772 00",
        radius=25,
        price_min=100_000,
        price_max=500_000,
        sort="1",
    )

    url = build_search_url(criteria)

    assert url == (
        "https://auto.bazos.cz/inzeraty/osobni/"
        "?hledat=BMW+320d&rubriky=auto&hlokalita=772+00&humkreis=25"
        "&cenaod=100000&cenado=500000&order=1"
    )
