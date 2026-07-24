from core.models import Offer, SearchCriteria
from core.provider import MarketplaceProvider
from utils.http import HttpClient
from .search import search_offers
from .detail import enrich_offer


class BazosProvider(MarketplaceProvider):
    def __init__(self, client: HttpClient | None = None): self.client = client or HttpClient()
    def search(self, criteria: SearchCriteria, limit: int) -> list[Offer]: return search_offers(criteria, limit, self.client)
    def load_detail(self, offer: Offer) -> Offer: return enrich_offer(offer, self.client)
