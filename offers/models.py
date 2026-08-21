from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Offer:
    source: str
    external_id: str
    title: str
    url: str
    price: int | None = None
    description: str | None = None
    location: str | None = None
    seller: str | None = None
    phone: str | None = None
    image_urls: list[str] = field(default_factory=list)
    published_at: datetime | None = None
    views: int | None = None
