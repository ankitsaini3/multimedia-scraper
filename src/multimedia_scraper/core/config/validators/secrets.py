from __future__ import annotations

from multimedia_scraper.core.config.dto.secrets import (
    SecretStr,
)

from .base import ValidationResult


class SecretValidator:
    def validate(
        self,
        value: object,
    ) -> ValidationResult:

        if not isinstance(value, SecretStr):
            return ValidationResult(
                valid=False,
                normalized={},
                errors=("invalid secret type",),
            )

        if not value.reveal():
            return ValidationResult(
                valid=False,
                normalized={},
                errors=("empty secret",),
            )

        return ValidationResult(
            valid=True,
            normalized={
                "value": value,
            },
            errors=(),
        )
