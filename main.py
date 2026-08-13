from __future__ import annotations

import logging
import sqlite3
from collections.abc import Sequence

from app import SearchApplication
from app.cli import parse_request, print_results
from app.database import ListingRepository, connect_database
from bazos_sniper import BazosSniper


def main(argv: Sequence[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO)
    request = parse_request(argv)
    connection: sqlite3.Connection | None = None

    try:
        connection = connect_database()
        application = SearchApplication(
            bazos=BazosSniper(),
            repository=ListingRepository(connection),
        )
        print_results(application.execute(request))
    except Exception as error:
        logging.getLogger(__name__).error("Search failed: %s", error)
        return 1
    finally:
        if connection is not None:
            connection.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
