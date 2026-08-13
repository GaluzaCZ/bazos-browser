import re
from datetime import date

from bazos_sniper import Listing

from .models import NormalizedVehicle


def normalize_title(title: str) -> NormalizedVehicle:
    text = title.lower()
    brand = "BMW" if re.search(r"\bbmw\b", text) else None
    generation_match = re.search(r"\b(e90|e91|f30|f31)\b", text)
    engine_match = re.search(r"\b(320d|330d)\b", text)
    return NormalizedVehicle(
        brand=brand,
        model="3 Series" if brand == "BMW" and generation_match else None,
        generation=generation_match.group(1).upper() if generation_match else None,
        engine=engine_match.group(1) if engine_match else None,
    )


def score_listing(listing: Listing) -> int:
    today = date.today()
    age = (
        0
        if listing.published_at is None
        else max(0, min(30, (today - listing.published_at).days))
    )
    age_score = 0 if listing.published_at is None else 40 * (30 - age) / 30
    description_score = min(30, len(listing.description or "") * 30 / 500)
    photos_score = min(30, len(listing.image_urls) * 3)
    return max(0, min(100, round(age_score + description_score + photos_score)))

