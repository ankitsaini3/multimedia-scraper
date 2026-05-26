from __future__ import annotations

from dataclasses import asdict, dataclass
from types import MappingProxyType
from typing import Any, Mapping


@dataclass(frozen=True, slots=True, kw_only=True)
class ConfigDTO:
    """
    Immutable base configuration DTO.

    Architectural guarantees:
    - immutable
    - hashable
    - deterministic
    - serialization-safe
    - transport-safe
    """

    def to_dict(self) -> Mapping[str, Any]:
        """
        Deterministic read-only serialization view.
        """
        return MappingProxyType(asdict(self))