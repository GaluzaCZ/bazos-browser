from __future__ import annotations

import json
import sqlite3

from bozos_browser.domain.models import Offer

_COLUMNS = (
    "url",
    "source",
    "offer_id",
    "title",
    "price",
    "location",
    "seller",
    "phone",
    "description",
    "image_urls",
    "image_paths",
    "published_at",
    "views",
)
_SELECT_COLUMNS = ", ".join(_COLUMNS)
_UPSERT = f"""
    INSERT INTO offers ({_SELECT_COLUMNS})
    VALUES ({", ".join("?" for _ in _COLUMNS)})
    ON CONFLICT(url) DO UPDATE SET
        source=excluded.source,
        offer_id=excluded.offer_id,
        title=excluded.title,
        price=excluded.price,
        location=excluded.location,
        seller=excluded.seller,
        phone=excluded.phone,
        description=excluded.description,
        image_urls=excluded.image_urls,
        image_paths=excluded.image_paths,
        published_at=excluded.published_at,
        views=excluded.views
"""


class SqliteOfferRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def upsert(self, offer: Offer) -> None:
        with self._connection:
            self._connection.execute(
                _UPSERT,
                (
                    offer.url,
                    offer.source,
                    offer.id,
                    offer.title,
                    offer.price,
                    offer.location,
                    offer.seller,
                    offer.phone,
                    offer.description,
                    json.dumps(offer.image_urls),
                    "[]",
                    offer.published_at.isoformat() if offer.published_at else None,
                    offer.views,
                ),
            )
