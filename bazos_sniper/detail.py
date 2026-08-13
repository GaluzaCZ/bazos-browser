from collections.abc import Iterable
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from .models import Listing
from .parsing import parse_date, parse_integer


def enrich_listing(listing: Listing, html: str) -> Listing:
    soup = BeautifulSoup(html, "lxml")
    title = _text(soup.select_one("h1.nadpisdetail"))
    description = _text(soup.select_one("div.popisdetail"), separator="\n")
    seller_cell = _table_value(soup, ("Jméno", "Prodejce"))
    phone_cell = _table_value(soup, ("Telefon",))
    location_cell = _table_value(soup, ("Lokalita", "Místo"))
    price_cell = _table_value(soup, ("Cena",))
    views_cell = _table_value(soup, ("Vidělo", "Zobrazeno"))
    date_element = soup.select_one(".inzeratydetnadpis .velikost10")
    gallery_urls = _gallery_urls(soup, listing.url)

    if title:
        listing.title = title
    if description:
        listing.description = description
    seller = _text(seller_cell.select_one(".paction")) if seller_cell else None
    listing.seller = seller or _text(seller_cell) or listing.seller

    phone = None
    if phone_cell:
        phone = _text(phone_cell.select_one('a[href^="tel:"], .telefoni')) or _text(
            phone_cell
        )
    listing.phone = phone or listing.phone

    location = _text(location_cell)
    if location:
        listing.location = location
    if price_cell is not None:
        listing.price = parse_integer(_text(price_cell) or "")
    if views_cell is not None:
        listing.views = parse_integer(_text(views_cell) or "")
    if date_element is not None:
        published_at = parse_date(_text(date_element) or "")
        listing.published_at = published_at or listing.published_at
    if gallery_urls:
        listing.image_urls = gallery_urls
    return listing


def _text(element: Tag | None, separator: str = " ") -> str | None:
    if element is None:
        return None
    value = element.get_text(separator, strip=True)
    return value or None


def _table_value(soup: BeautifulSoup, labels: Iterable[str]) -> Tag | None:
    normalized_labels = {label.casefold().rstrip(":") for label in labels}
    for row in soup.select("tr"):
        cells = row.select(":scope > th, :scope > td")
        if len(cells) < 2:
            continue
        label = cells[0].get_text(" ", strip=True).casefold().rstrip(":")
        if label in normalized_labels:
            return cells[1]
    return None


def _gallery_urls(soup: BeautifulSoup, page_url: str) -> list[str]:
    urls: list[str] = []
    for image in soup.select(".carousel-cell img"):
        source = (
            image.get("data-flickity-lazyload")
            or image.get("data-src")
            or image.get("src")
        )
        if not source:
            continue
        absolute_url = urljoin(page_url, source)
        if absolute_url not in urls:
            urls.append(absolute_url)
    return urls

