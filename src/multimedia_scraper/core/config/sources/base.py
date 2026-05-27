from __future__ import annotations

from abc import ABC, abstractmethod

from .models import ConfigSource


class ConfigSourceProvider(ABC):
    @abstractmethod
    def load(self) -> ConfigSource:
        """
        Load and normalize source payload.
        """
