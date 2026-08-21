from dataclasses import dataclass

from offers import Offer


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
