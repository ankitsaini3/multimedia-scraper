from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypeVar, cast

T = TypeVar("T")


@dataclass(slots=True, kw_only=True)
class RuntimeRegistry:
    """
    Minimal runtime-owned registration registry.

    Responsibilities:

    - explicit registration
    - typed lookup
    - runtime-owned references
    - deterministic ownership

    Explicitly excluded:

    - dependency injection
    - service location
    - auto wiring
    - reflection
    - lifecycle management
    - orchestration
    """

    _registrations: dict[type[Any], object] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    def register(
        self,
        interface: type[T],
        implementation: T,
    ) -> None:
        """
        Explicit runtime registration.
        """

        self._registrations[interface] = implementation

    def resolve(
        self,
        interface: type[T],
    ) -> T:
        """
        Explicit typed runtime lookup.
        """
        value = self._registrations.get(
            interface,
        )

        if value is None:
            raise KeyError(
                (f"Runtime interface not registered: {interface!r}"),
            )

        return cast(T, value)  # pyright: ignore[reportReturnType]

    def try_resolve(
        self,
        interface: type[T],
    ) -> T | None:
        """
        Optional typed lookup.
        """

        value = self._registrations.get(interface)

        if value is None:
            return None

        return cast(T, value)  # pyright: ignore[reportReturnType]

    def is_registered(
        self,
        interface: type[object],
    ) -> bool:
        return interface in self._registrations
