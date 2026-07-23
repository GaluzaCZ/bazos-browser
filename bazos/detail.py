from __future__ import annotations
from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup
from .search import _date, _integer
from core.models import Offer


def enrich_offer(offer: Offer, client) -> Offer:
    soup = BeautifulSoup(client.get_text(offer.url), "lxml")
    text = soup.get_text(" ", strip=True)
    desc = soup.select_one(".popis, #popis, .inzeratpopis")
    offer.description = desc.get_text("\n", strip=True) if desc else offer.description
    seller = soup.select_one(".jmenoinzerenta, .inzerent, [class*=prodejce]")
    offer.seller = seller.get_text(" ", strip=True) if seller else offer.seller
    phone = soup.select_one('a[href^="tel:"], .telefoni')
    offer.phone = phone.get_text(" ", strip=True) if phone else offer.phone
    images = [urljoin(offer.url, img.get("src")) for img in soup.select("img[src]") if img.get("src")]
    offer.image_urls = list(dict.fromkeys(images))
    price = soup.select_one(".inzeratcena, .cena")
    offer.price = _integer(price.get_text(" ", strip=True)) if price else offer.price
    views = re.search(r"(?:zobrazen[ío]|views?)\s*:?\s*([\d ]+)", text, re.I)
    offer.views = _integer(views.group(1)) if views else offer.views
    published = re.search(r"(?:vložen[ío]|datum)\s*:?\s*(\d{1,2}\.\d{1,2}\.\s*\d{4})", text, re.I)
    offer.published_at = _date(published.group(1)) if published else offer.published_at
    return offer
