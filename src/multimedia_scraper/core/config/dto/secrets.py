from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SecretStr:
    """
    Redacted immutable secret wrapper.
    """

    _value: str

    def reveal(self) -> str:
        return self._value

    def __str__(self) -> str:
        return "********"

    def __repr__(self) -> str:
        return "SecretStr('********')"
