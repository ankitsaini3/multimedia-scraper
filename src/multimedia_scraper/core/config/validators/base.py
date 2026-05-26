from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


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