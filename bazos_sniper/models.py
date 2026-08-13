from dataclasses import dataclass, field
from datetime import date


@dataclass(slots=True)
class Listing:
    source: str
    id: str
    title: str
    url: str
    price: int | None = None
    location: str | None = None
    seller: str | None = None
    phone: str | None = None
    description: str | None = None
    image_urls: list[str] = field(default_factory=list)
    published_at: date | None = None
    views: int | None = None

