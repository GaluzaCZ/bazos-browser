from __future__ import annotations

import re
from collections.abc import Iterable
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from core.models import Offer

from .search import _date, _integer


def _text(element: Tag | None, separator: str = " ") -> str | None:
    if element is None:
        return None
    value = element.get_text(separator, strip=True)
    return value or None


def _table_value(soup: BeautifulSoup, labels: Iterable[str]) -> Tag | None:
    """Return the value cell from a detail row identified by its Czech label."""
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
        source = image.get("data-flickity-lazyload") or image.get("data-src") or image.get("src")
        if not source:
            continue
        absolute_url = urljoin(page_url, source)
        if absolute_url not in urls:
            urls.append(absolute_url)
    return urls


def enrich_offer(offer: Offer, client) -> Offer:
    """Load a Bazos detail page and enrich an existing offer in place."""
    soup = BeautifulSoup(client.get_text(offer.url), "lxml")

    title = _text(soup.select_one("h1.nadpisdetail"))
    description = _text(soup.select_one("div.popisdetail"), separator="\n")
    seller_cell = _table_value(soup, ("Jméno", "Prodejce"))
    phone_cell = _table_value(soup, ("Telefon",))
    location_cell = _table_value(soup, ("Lokalita", "Místo"))
    price_cell = _table_value(soup, ("Cena",))
    views_cell = _table_value(soup, ("Vidělo", "Zobrazeno"))
    date_element = soup.select_one(".inzeratydetnadpis .velikost10")
    gallery_urls = _gallery_urls(soup, offer.url)

    if title:
        offer.title = title
    if description:
        offer.description = description
    seller = _text(seller_cell.select_one(".paction")) if seller_cell else None
    offer.seller = seller or _text(seller_cell) or offer.seller

    phone = None
    if phone_cell:
        phone = _text(phone_cell.select_one('a[href^="tel:"], .telefoni')) or _text(phone_cell)
    offer.phone = phone or offer.phone

    location = _text(location_cell)
    if location:
        offer.location = location
    if price_cell is not None:
        offer.price = _integer(_text(price_cell) or "")
    if views_cell is not None:
        offer.views = _integer(_text(views_cell) or "")
    if date_element is not None:
        published_at = _date(_text(date_element) or "")
        offer.published_at = published_at or offer.published_at
    if gallery_urls:
        offer.image_urls = gallery_urls
    return offer
