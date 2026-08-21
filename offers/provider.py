from typing import Protocol

from .criteria import SearchCriteria
from .models import Offer


class MarketplaceProvider(Protocol):
    def search(
        self,
        criteria: SearchCriteria,
        limit: int | None = None,
    ) -> list[Offer]: ...
