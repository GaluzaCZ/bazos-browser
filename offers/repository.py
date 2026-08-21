from typing import Protocol

from .models import Offer


class OfferRepository(Protocol):
    def save(self, offer: Offer) -> None: ...
