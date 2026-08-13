from __future__ import annotations

import logging
import sqlite3
from collections.abc import Sequence

from bozos_browser.adapters.bazos.provider import BazosProvider
from bozos_browser.adapters.http import RequestsHttpClient
from bozos_browser.adapters.sqlite.connection import connect_database
from bozos_browser.adapters.sqlite.repository import SqliteOfferRepository
from bozos_browser.application.search_offers import SearchOffers
from bozos_browser.cli.arguments import parse_options
from bozos_browser.cli.output import format_result


def main(argv: Sequence[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO)
    request = parse_options(argv)
    connection: sqlite3.Connection | None = None

    try:
        connection = connect_database()
        provider = BazosProvider(RequestsHttpClient())
        repository = SqliteOfferRepository(connection)
        results = SearchOffers(provider, repository).execute(request)
        for result in results:
            print(format_result(result))
    except Exception as error:
        logging.getLogger(__name__).error("Search failed: %s", error)
        return 1
    finally:
        if connection is not None:
            connection.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
