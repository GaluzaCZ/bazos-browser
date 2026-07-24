from __future__ import annotations
from datetime import datetime, date
from urllib.parse import urlencode, urljoin
import re
from bs4 import BeautifulSoup
from core.models import Offer, SearchCriteria

BASE_URL = "https://auto.bazos.cz"


def build_search_url(criteria: SearchCriteria) -> str:
    if criteria.url:
        return criteria.url
    params = {"hledat": criteria.query, "rubrika": criteria.category, "lokalita": criteria.location,
              "hloubsort": criteria.sort, "cenaod": criteria.price_min, "cenado": criteria.price_max,
              "radius": criteria.radius}
    return f"{BASE_URL}/inzeraty/osobni/?{urlencode({k: v for k, v in params.items() if v is not None})}"


def _integer(value: str) -> int | None:
    digits = re.sub(r"[^0-9]", "", value)
    return int(digits) if digits else None


def _date(value: str) -> date | None:
    match = re.search(r"\b\d{1,2}\.\d{1,2}\.\s*\d{4}\b", value)
    if match:
        value = match.group(0)
    for fmt in ("%d.%m.%Y", "%d.%m. %Y"):
        try: return datetime.strptime(value.strip(), fmt).date()
        except ValueError: pass
    return None


def parse_listing(html: str, page_url: str = BASE_URL) -> tuple[list[Offer], str | None]:
    soup = BeautifulSoup(html, "lxml")
    offers: list[Offer] = []
    # A Bazos result is an ``.inzeraty`` card.  Do not use the nearest generic
    # div around a link: it is usually ``.inzeratytext`` and does not contain
    # the sibling ``.inzeratycena`` element.
    cards = soup.select("div.inzeraty")
    if not cards:
        cards = [link.find_parent("div") or link.parent for link in soup.select('a[href*="/inzerat/"]')]

    for card in cards:
        if card is None:
            continue
        link = card.select_one('h2 a[href*="/inzerat/"], a[href*="/inzerat/"]')
        if link is None:
            continue
        title = link.get_text(" ", strip=True)
        if not title:
            continue
        url = urljoin(page_url, link.get("href", ""))
        match = re.search(r"/inzerat/(\d+)", url)
        if not match or any(item.url == url for item in offers):
            continue
        text = card.get_text(" ", strip=True)
        price = card.select_one(".inzeratycena, .inzeratcena")
        price_text = price.get_text(" ", strip=True) if price else ""
        offers.append(Offer("bazos", match.group(1), title, _integer(price_text), url=url,
                            published_at=_date(text)))
    next_link = soup.select_one('a[rel="next"], a.next')
    if next_link is None:
        next_link = next((link for link in soup.select("a[href]")
                          if link.get_text(" ", strip=True).casefold() in {"další", "další >", "další »"}), None)
    return offers, urljoin(page_url, next_link["href"]) if next_link and next_link.get("href") else None


def search_offers(criteria: SearchCriteria, limit: int, client) -> list[Offer]:
    url, result, seen = build_search_url(criteria), [], set()
    while url and len(result) < limit:
        offers, url = parse_listing(client.get_text(url), url)
        for offer in offers:
            if offer.url not in seen:
                seen.add(offer.url); result.append(offer)
                if len(result) == limit: break
    return result
