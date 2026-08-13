from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(slots=True)
class Offer:
    source: str
    id: str
    title: str
    price: int | None = None
    location: str | None = None
    url: str = ""
    seller: str | None = None
    phone: str | None = None
    description: str | None = None
    image_urls: list[str] = field(default_factory=list)
    published_at: date | None = None
    views: int | None = None


@dataclass(slots=True)
class NormalizedVehicle:
    brand: str | None = None
    model: str | None = None
    generation: str | None = None
    engine: str | None = None


@dataclass(slots=True)
class SearchResult:
    offer: Offer
    vehicle: NormalizedVehicle
    score: int
