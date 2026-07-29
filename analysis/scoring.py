from datetime import date
from core.models import Offer


def score_offer(offer: Offer, reference_date: date | None = None) -> int:
    today = reference_date or date.today()
    age = 0 if offer.published_at is None else max(0, min(30, (today - offer.published_at).days))
    age_score = 0 if offer.published_at is None else 40 * (30 - age) / 30
    description_score = min(30, len(offer.description or "") * 30 / 500)
    photos_score = min(30, len(offer.image_urls) * 3)
    return max(0, min(100, round(age_score + description_score + photos_score)))
