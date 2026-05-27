from __future__ import annotations

from pathlib import Path

from .base import ValidationResult


class SafePathValidator:
    def validate(
        self,
        value: str,
    ) -> ValidationResult:

        path = Path(value).expanduser().resolve()

        if ".." in path.parts:
            return ValidationResult(
                valid=False,
                normalized={},
                errors=("path traversal detected",),
            )

        return ValidationResult(
            valid=True,
            normalized={
                "value": str(path),
            },
            errors=(),
        )
