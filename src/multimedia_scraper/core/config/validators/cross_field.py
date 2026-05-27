from __future__ import annotations

from collections.abc import Mapping

from .base import ValidationResult


class CrossFieldValidator:
    def validate(
        self,
        payload: Mapping[str, object],
    ) -> ValidationResult:

        errors: list[str] = []

        cache_enabled = payload.get(
            "cache.enabled",
        )

        cache_dir = payload.get(
            "cache.root_directory",
        )

        if cache_enabled and not cache_dir:
            errors.append(
                "cache.root_directory required when cache.enabled=true",
            )

        if errors:
            return ValidationResult(
                valid=False,
                normalized={},
                errors=tuple(errors),
            )

        return ValidationResult(
            valid=True,
            normalized=dict(payload),
            errors=(),
        )
