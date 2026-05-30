from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar, cast

from multimedia_scraper.plugins.dto.capability_registration import (
    CapabilityRegistrationDTO,
)
from multimedia_scraper.plugins.dto.manifest import (
    PluginManifestDTO,
)
from multimedia_scraper.plugins.registry.exceptions import (
    DuplicateCapabilityProviderError,
    UnknownCapabilityProviderError,
)
from multimedia_scraper.plugins.types import (
    CapabilityName,
)

T = TypeVar("T")


@dataclass(slots=True, kw_only=True)
class CapabilityRegistry:
    """
    Runtime-owned capability provider registry.

    Responsibilities:
    - capability ownership registration
    - typed provider discovery
    - deterministic provider lookup

    Explicitly excluded:
    - permission enforcement
    - authority delegation
    - sandboxing
    """

    _capabilities: dict[
        CapabilityName,
        list[CapabilityRegistrationDTO],
    ] = field(
        default_factory=dict,
        init=False,
    )

    _providers: dict[
        type[object],
        object,
    ] = field(
        default_factory=dict,
        init=False,
    )

    def register_manifest(
        self,
        manifest: PluginManifestDTO,
        *,
        provider: object,
    ) -> None:
        plugin_id = manifest.metadata.plugin_id

        for capability in manifest.capabilities:
            registration = CapabilityRegistrationDTO(
                capability_name=(capability.capability_name),
                plugin_id=plugin_id,
                provider_type=(capability.provider_type),
                version=capability.version,
                optional=capability.optional,
            )

            registrations = self._capabilities.setdefault(
                capability.capability_name,
                [],
            )

            registrations.append(
                registration,
            )

            provider_type = capability.provider_type

            if provider_type in self._providers:
                raise DuplicateCapabilityProviderError(
                    (f"Capability provider already registered: {provider_type}"),
                )

            self._providers[provider_type] = provider

    def resolve(
        self,
        capability_name: CapabilityName,
    ) -> tuple[CapabilityRegistrationDTO, ...]:
        registrations = self._capabilities.get(
            capability_name,
            [],
        )

        return tuple(registrations)

    def resolve_provider(
        self,
        provider_type: type[T],
    ) -> T:
        provider = self._providers.get(
            provider_type,
        )

        if provider is None:
            raise (
                UnknownCapabilityProviderError(
                    (f"Unknown capability provider: {provider_type}"),
                )
            )

        return cast(T, provider)
