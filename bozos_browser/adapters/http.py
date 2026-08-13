from __future__ import annotations

import requests

from bozos_browser.config import HTTP_TIMEOUT, USER_AGENT


class HttpClientError(RuntimeError):
    def __init__(self, url: str, message: str) -> None:
        super().__init__(f"{message}: {url}")


class RequestsHttpClient:
    def __init__(self) -> None:
        self._session = requests.Session()

    def get_text(self, url: str) -> str:
        return self._get(url).text

    def _get(self, url: str) -> requests.Response:
        try:
            response = self._session.get(
                url,
                timeout=HTTP_TIMEOUT,
                headers={"User-Agent": USER_AGENT},
            )
            response.raise_for_status()
        except requests.RequestException as error:
            raise HttpClientError(url, "HTTP request failed") from error
        return response
