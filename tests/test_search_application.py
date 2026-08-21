import sqlite3

from offers import Offer, SearchCriteria

from app.database import SCHEMA, SqliteOfferRepository
from app.service import SearchApplication


class FakeProvider:
    def __init__(self) -> None:
        self.received: tuple[SearchCriteria, int | None] | None = None

    def search(
        self,
        criteria: SearchCriteria,
        limit: int | None = None,
    ) -> list[Offer]:
        self.received = criteria, limit
        return [
            Offer(
                source="other-marketplace",
                external_id="abc",
                title="BMW 320d E90",
                url="https://example.test/abc",
            )
        ]


class FakeRepository:
    def __init__(self) -> None:
        self.offers: list[Offer] = []

    def save(self, offer: Offer) -> None:
        self.offers.append(offer)


def test_application_accepts_offer_provider_without_bazos_dependency() -> None:
    repository = FakeRepository()
    provider = FakeProvider()
    application = SearchApplication(provider, repository)
    criteria = SearchCriteria(query="bmw")

    results = application.execute(criteria, limit=1)

    assert provider.received == (criteria, 1)
    assert repository.offers == [results[0].offer]
    assert results[0].offer.source == "other-marketplace"


def test_sqlite_repository_stores_external_offer_id() -> None:
    connection = sqlite3.connect(":memory:")
    connection.execute(SCHEMA)
    repository = SqliteOfferRepository(connection)
    offer = Offer(
        source="other-marketplace",
        external_id="abc",
        title="BMW",
        url="https://example.test/abc",
    )

    repository.save(offer)
    offer.title = "BMW updated"
    repository.save(offer)

    assert connection.execute(
        "SELECT source, offer_id, title FROM offers WHERE url = ?", (offer.url,)
    ).fetchone() == ("other-marketplace", "abc", "BMW updated")
    assert connection.execute("SELECT COUNT(*) FROM offers").fetchone() == (1,)
