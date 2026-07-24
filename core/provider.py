from abc import ABC, abstractmethod
from .models import Offer, SearchCriteria


class MarketplaceProvider(ABC):
    @abstractmethod
    def search(self, criteria: SearchCriteria, limit: int) -> list[Offer]: ...

    @abstractmethod
    def load_detail(self, offer: Offer) -> Offer: ...
