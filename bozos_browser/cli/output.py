from bozos_browser.domain.models import SearchResult


def format_result(result: SearchResult) -> str:
    offer = result.offer
    price = offer.price or "dohodou"
    return (
        f"[{result.score:3}] {offer.title} | {price} | "
        f"{offer.url} | {result.vehicle}"
    )

