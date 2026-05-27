from __future__ import annotations

from typing import Any

from .base import ValidationResult


class StringValidator:
    def validate(
        self,
        value: Any,
    ) -> ValidationResult:

        if not isinstance(value, str):
            return ValidationResult(
                valid=False,
                normalized={},
                errors=("expected string",),
            )

        return ValidationResult(
            valid=True,
            normalized={"value": value.strip()},
            errors=(),
        )


class IntegerRangeValidator:
    def __init__(
        self,
        *,
        minimum: int,
        maximum: int,
    ) -> None:
        self._minimum = minimum
        self._maximum = maximum

    def validate(
        self,
        value: Any,
    ) -> ValidationResult:

        if not isinstance(value, int):
            return ValidationResult(
                valid=False,
                normalized={},
                errors=("expected integer",),
            )

        if value < self._minimum:
            return ValidationResult(
                valid=False,
                normalized={},
                errors=("value below minimum",),
            )

        if value > self._maximum:
            return ValidationResult(
                valid=False,
                normalized={},
                errors=("value above maximum",),
            )

        return ValidationResult(
            valid=True,
            normalized={"value": value},
            errors=(),
        )
