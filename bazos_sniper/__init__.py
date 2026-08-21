"""Bazos provider for loading source-independent offers."""

from .client import BazosProvider
from .errors import BazosSniperError

__all__ = ["BazosProvider", "BazosSniperError"]
