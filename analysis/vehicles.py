import re
from core.models import NormalizedVehicle


def normalize_title(title: str) -> NormalizedVehicle:
    text = title.lower()
    brand = "BMW" if re.search(r"\bbmw\b", text) else None
    generation_match = re.search(r"\b(e90|e91|f30|f31)\b", text)
    engine_match = re.search(r"\b(320d|330d)\b", text)
    return NormalizedVehicle(brand, "3 Series" if brand == "BMW" and generation_match else None,
                             generation_match.group(1).upper() if generation_match else None,
                             engine_match.group(1) if engine_match else None)
