from dataclasses import dataclass

from bazos_sniper import Listing


@dataclass(slots=True)
class NormalizedVehicle:
    brand: str | None = None
    model: str | None = None
    generation: str | None = None
    engine: str | None = None


@dataclass(slots=True)
class SearchResult:
    listing: Listing
    vehicle: NormalizedVehicle
    score: int

