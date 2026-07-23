import json
from datetime import date
from pathlib import Path
from .database import connect
from core.models import Offer


class OfferRepository:
    def __init__(self, connection=None): self.connection = connection or connect()
    def offer_exists(self, url: str) -> bool: return self.find_by_url(url) is not None
    def find_by_url(self, url: str) -> Offer | None:
        row = self.connection.execute("SELECT * FROM offers WHERE url=?", (url,)).fetchone()
        return self._offer(row) if row else None
    def save_offer(self, offer: Offer) -> Offer:
        return self._write(offer, "INSERT INTO offers VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)")
    def update_offer(self, offer: Offer) -> Offer:
        self.connection.execute("DELETE FROM offers WHERE url=?", (offer.url,)); return self.save_offer(offer)
    def _write(self, o: Offer, sql: str) -> Offer:
        self.connection.execute(sql, (o.url,o.source,o.id,o.title,o.price,o.location,o.seller,o.phone,o.description,json.dumps(o.image_urls),json.dumps([str(x) for x in o.image_paths]),o.published_at.isoformat() if o.published_at else None,o.views)); self.connection.commit(); return o
    def list_offers(self) -> list[Offer]: return [self._offer(r) for r in self.connection.execute("SELECT * FROM offers")]
    @staticmethod
    def _offer(row) -> Offer:
        return Offer(row[1],row[2],row[3],row[4],row[5],row[0],row[6],row[7],row[8],json.loads(row[9]),[Path(x) for x in json.loads(row[10])],date.fromisoformat(row[11]) if row[11] else None,row[12])
