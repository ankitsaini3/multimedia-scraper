from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from multimedia_scraper.core.config.exceptions import (
    ConfigurationValidationError,
)

from .cross_field import CrossFieldValidator
from .registry import ALLOWED_FIELDS
from .runtime import RuntimeConfigDTOFactory
from multimedia_scraper.core.config.dto.runtime import (
    RuntimeConfigDTO,
)



class ValidationPipeline:

    def validate(
        self,
        payload: Mapping[str, Any],
    ) -> RuntimeConfigDTO:

        self._validate_unknown_fields(payload)

        self._validate_cross_fields(payload)

        return RuntimeConfigDTOFactory.create(
            payload,
        )

    def _validate_unknown_fields(
        self,
        payload: Mapping[str, Any],
    ) -> None:

        unknown = sorted(
            set(payload) - ALLOWED_FIELDS,
        )

        if unknown:
            raise ConfigurationValidationError(
                "unknown configuration fields detected",
            )

    def _validate_cross_fields(
        self,
        payload: Mapping[str, Any],
    ) -> None:

        validator = CrossFieldValidator()

        result = validator.validate(payload)

        if not result.valid:
            raise ConfigurationValidationError(
                "cross-field validation failed",
            )