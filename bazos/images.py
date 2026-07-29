from pathlib import Path
from urllib.parse import urlparse
import re
from core.models import Offer


def download_image(url: str, directory: Path, client) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    name = re.sub(r"[^A-Za-z0-9._-]", "_", Path(urlparse(url).path).name) or "image"
    path = (directory / name).resolve()
    path.write_bytes(client.get_bytes(url))
    return path


def download_images(offer: Offer, directory: Path, client) -> list[Path]:
    offer.image_paths = [download_image(url, directory, client) for url in offer.image_urls]
    return offer.image_paths
