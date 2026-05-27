from multimedia_scraper.core.errors import (
    ConfigurationError,
)


class ConfigurationValidationError(
    ConfigurationError,
):
    """Configuration validation failed."""


class ConfigurationFreezeError(
    ConfigurationError,
):
    """Attempted mutation of frozen configuration."""


class SecretResolutionError(
    ConfigurationError,
):
    """Secret resolution failed."""


class ConfigurationSourceError(
    ConfigurationError,
): ...


class EnvironmentResolutionError(
    ConfigurationSourceError,
): ...


class ConfigurationMergeError(
    ConfigurationSourceError,
): ...


class SchemaValidationError(
    ConfigurationValidationError,
): ...


class CrossFieldValidationError(
    ConfigurationValidationError,
): ...


class PathValidationError(
    ConfigurationValidationError,
): ...
