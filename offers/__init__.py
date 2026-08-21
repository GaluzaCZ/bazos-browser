"""Source-independent offer contracts used by providers and applications."""

from .criteria import SearchCriteria
from .models import Offer
from .provider import MarketplaceProvider
from .repository import OfferRepository

__all__ = ["MarketplaceProvider", "Offer", "OfferRepository", "SearchCriteria"]
