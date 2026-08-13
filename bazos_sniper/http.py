import requests

HTTP_TIMEOUT = 15.0
USER_AGENT = "bazos-sniper/1.0"


class HttpClient:
    def __init__(self) -> None:
        self._session = requests.Session()

    def get_text(self, url: str) -> str:
        try:
            response = self._session.get(
                url,
                timeout=HTTP_TIMEOUT,
                headers={"User-Agent": USER_AGENT},
            )
            response.raise_for_status()
        except requests.RequestException as error:
            raise BazosHttpError(f"HTTP request failed: {url}") from error
        return response.text


class BazosHttpError(RuntimeError):
    pass

