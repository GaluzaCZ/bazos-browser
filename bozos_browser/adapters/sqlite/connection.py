import sqlite3
from bozos_browser.config import DATABASE_PATH

SCHEMA = """CREATE TABLE IF NOT EXISTS offers (
 url TEXT PRIMARY KEY, source TEXT NOT NULL, offer_id TEXT NOT NULL, title TEXT NOT NULL,
 price INTEGER, location TEXT, seller TEXT, phone TEXT, description TEXT,
 image_urls TEXT NOT NULL, image_paths TEXT NOT NULL, published_at TEXT, views INTEGER)"""


def connect_database() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute(SCHEMA)
    return connection
