import re
from urllib.parse import urlencode, urljoin

from bs4 import BeautifulSoup, Tag
from offers import Offer

from .parsing import parse_date, parse_integer
from .urls import BASE_URL, is_bazos_url


def build_search_url(query: str) -> str:
    encoded_query = urlencode({"hledat": query})
    return f"{BASE_URL}/inzeraty/osobni/?{encoded_query}"


def parse_listing_page(
    html: str,
    page_url: str,
) -> tuple[list[Offer], str | None]:
    soup = BeautifulSoup(html, "lxml")
    offers: list[Offer] = []
    seen_urls: set[str] = set()

    for card in soup.select("div.inzeraty"):
        link = card.select_one(
            'div.inzeratynadpis h2.nadpis > a[href*="/inzerat/"]'
        )
        if link is None:
            continue
        title = link.get_text(" ", strip=True)
        url = urljoin(page_url, link.get("href", ""))
        id_match = re.search(r"/inzerat/(\d+)", url)
        if not title or id_match is None or url in seen_urls:
            continue
        seen_urls.add(url)
        offers.append(
            _parse_card(card, id_match.group(1), title, url, page_url)
        )

    return offers, _find_next_url(soup, page_url)


def _parse_card(
    card: Tag,
    external_id: str,
    title: str,
    url: str,
    page_url: str,
) -> Offer:
    heading = card.select_one("div.inzeratynadpis")
    price = card.select_one("div.inzeratycena")
    location = card.select_one("div.inzeratylok")
    views = card.select_one("div.inzeratyview")
    description = card.select_one("div.inzeratynadpis div.popis")
    thumbnail = card.select_one("div.inzeratynadpis img.obrazek[src]")

    price_text = price.get_text(" ", strip=True) if price else ""
    image_urls = [urljoin(page_url, thumbnail["src"])] if thumbnail else []
    return Offer(
        source="bazos",
        external_id=external_id,
        title=title,
        url=url,
        price=parse_integer(price_text),
        location=location.get_text(" ", strip=True) if location else None,
        description=description.get_text("\n", strip=True) if description else None,
        image_urls=image_urls,
        published_at=parse_date(heading.get_text(" ", strip=True)) if heading else None,
        views=parse_integer(views.get_text(" ", strip=True)) if views else None,
    )


def _find_next_url(soup: BeautifulSoup, page_url: str) -> str | None:
    next_link = next(
        (
            link
            for link in soup.select("div.strankovani a[href]")
            if link.get_text(" ", strip=True).casefold() == "další"
        ),
        None,
    )
    if next_link is None or not next_link.get("href"):
        return None
    next_url = urljoin(page_url, next_link["href"])
    return next_url if is_bazos_url(next_url) else None
