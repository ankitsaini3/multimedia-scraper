from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from .types import ConfigSourceType


@dataclass(frozen=True, slots=True, kw_only=True)
class ConfigSource:
    """
    Immutable normalized config source.
    """

    source_type: ConfigSourceType
    source_name: str
    precedence: int
    payload: Mapping[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "payload",
            MappingProxyType(dict(self.payload)),
        )
