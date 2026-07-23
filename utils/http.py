from __future__ import annotations
import requests


class HttpClient:
    def __init__(self, session: requests.Session | None = None, timeout: float = 15):
        self.session, self.timeout = session or requests.Session(), timeout

    def get_text(self, url: str) -> str:
        response = self.session.get(url, timeout=self.timeout, headers={"User-Agent": "bazos-sniper/1.0"})
        response.raise_for_status()
        return response.text

    def get_bytes(self, url: str) -> bytes:
        response = self.session.get(url, timeout=self.timeout, headers={"User-Agent": "bazos-sniper/1.0"})
        response.raise_for_status()
        return response.content
