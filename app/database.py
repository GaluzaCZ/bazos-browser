import json
import sqlite3
from pathlib import Path

from offers import Offer

DATABASE_PATH = Path("cars.db")
SCHEMA = """CREATE TABLE IF NOT EXISTS offers (
 url TEXT PRIMARY KEY, source TEXT NOT NULL, offer_id TEXT NOT NULL, title TEXT NOT NULL,
 price INTEGER, location TEXT, seller TEXT, phone TEXT, description TEXT,
 image_urls TEXT NOT NULL, image_paths TEXT NOT NULL, published_at TEXT, views INTEGER)"""

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
_COLUMN_NAMES = ", ".join(_COLUMNS)
_UPSERT = f"""
    INSERT INTO offers ({_COLUMN_NAMES})
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


def connect_database() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute(SCHEMA)
    return connection


class SqliteOfferRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def save(self, offer: Offer) -> None:
        with self._connection:
            self._connection.execute(
                _UPSERT,
                (
                    offer.url,
                    offer.source,
                    offer.external_id,
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
