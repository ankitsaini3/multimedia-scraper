from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any


@dataclass(frozen=True, slots=True)
class ValidationResult:
    valid: bool
    normalized: Mapping[str, Any]
    errors: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "normalized",
            MappingProxyType(
                dict(self.normalized),
            ),
        )
