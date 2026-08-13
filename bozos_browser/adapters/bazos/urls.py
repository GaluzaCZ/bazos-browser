from urllib.parse import urlparse

BASE_URL = "https://auto.bazos.cz"


def is_bazos_url(url: str) -> bool:
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").casefold()
    return parsed.scheme in {"http", "https"} and (
        hostname == "bazos.cz" or hostname.endswith(".bazos.cz")
    )
