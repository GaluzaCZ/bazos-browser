from hashlib import sha256
from pathlib import Path


class TextCache:
    def __init__(self, directory: Path = Path("data/cache")):
        self.directory = directory

    def get(self, key: str) -> str | None:
        path = self.directory / sha256(key.encode()).hexdigest()
        return path.read_text("utf-8") if path.exists() else None

    def set(self, key: str, value: str) -> Path:
        self.directory.mkdir(parents=True, exist_ok=True)
        path = self.directory / sha256(key.encode()).hexdigest()
        path.write_text(value, encoding="utf-8")
        return path
