from __future__ import annotations

import re
from datetime import date, datetime
from urllib.parse import urlencode, urljoin, urlparse

from bs4 import BeautifulSoup

from core.models import Offer, SearchCriteria

BASE_URL = "https://auto.bazos.cz"


def build_search_url(criteria: SearchCriteria) -> str:
    if criteria.url:
        return criteria.url
    params = {
        "hledat": criteria.query,
        "rubriky": criteria.category,
        "hlokalita": criteria.location,
        "humkreis": criteria.radius,
        "cenaod": criteria.price_min,
        "cenado": criteria.price_max,
        "order": criteria.sort,
    }
    query = urlencode({key: value for key, value in params.items() if value is not None})
    return f"{BASE_URL}/inzeraty/osobni/?{query}"


def _integer(value: str) -> int | None:
    digits = re.sub(r"[^0-9]", "", value)
    return int(digits) if digits else None


def _date(value: str) -> date | None:
    match = re.search(r"\b\d{1,2}\.\d{1,2}\.\s*\d{4}\b", value)
    if match:
        value = match.group(0)
    for fmt in ("%d.%m.%Y", "%d.%m. %Y"):
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            pass
    return None


def parse_listing(html: str, page_url: str = BASE_URL) -> tuple[list[Offer], str | None]:
    soup = BeautifulSoup(html, "lxml")
    offers: list[Offer] = []

    cards = soup.select("div.inzeraty")
    for card in cards:
        link = card.select_one('div.inzeratynadpis h2.nadpis > a[href*="/inzerat/"]')
        if link is None:
            continue
        title = link.get_text(" ", strip=True)
        if not title:
            continue
        url = urljoin(page_url, link.get("href", ""))
        match = re.search(r"/inzerat/(\d+)", url)
        if not match or any(item.url == url for item in offers):
            continue
        heading = card.select_one("div.inzeratynadpis")
        price = card.select_one("div.inzeratycena")
        location = card.select_one("div.inzeratylok")
        views = card.select_one("div.inzeratyview")
        description = card.select_one("div.inzeratynadpis div.popis")
        thumbnail = card.select_one("div.inzeratynadpis img.obrazek[src]")

        price_text = price.get_text(" ", strip=True) if price else ""
        image_urls = [urljoin(page_url, thumbnail["src"])] if thumbnail else []
        offers.append(
            Offer(
                source="bazos",
                id=match.group(1),
                title=title,
                price=_integer(price_text),
                location=location.get_text(" ", strip=True) if location else None,
                url=url,
                description=description.get_text("\n", strip=True) if description else None,
                image_urls=image_urls,
                published_at=_date(heading.get_text(" ", strip=True)) if heading else None,
                views=_integer(views.get_text(" ", strip=True)) if views else None,
            )
        )

    next_link = next(
        (
            link
            for link in soup.select("div.strankovani a[href]")
            if link.get_text(" ", strip=True).casefold() == "další"
        ),
        None,
    )
    next_url = urljoin(page_url, next_link["href"]) if next_link and next_link.get("href") else None
    if next_url:
        parsed_next = urlparse(next_url)
        hostname = (parsed_next.hostname or "").casefold()
        if parsed_next.scheme not in {"http", "https"} or not (
            hostname == "bazos.cz" or hostname.endswith(".bazos.cz")
        ):
            next_url = None
    return offers, next_url


def search_offers(criteria: SearchCriteria, limit: int, client) -> list[Offer]:
    url = build_search_url(criteria)
    result: list[Offer] = []
    seen_offers: set[str] = set()
    visited_pages: set[str] = set()
    while url and url not in visited_pages and len(result) < limit:
        visited_pages.add(url)
        offers, next_url = parse_listing(client.get_text(url), url)
        if not offers:
            break
        for offer in offers:
            if offer.url in seen_offers:
                continue
            seen_offers.add(offer.url)
            result.append(offer)
            if len(result) == limit:
                break
        url = next_url
    return result
