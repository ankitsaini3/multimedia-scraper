from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class ServiceRegistration:
    interface: type[Any]
    implementation: Any
    scope: str


class ServiceCollection:
    def __init__(self) -> None:
        self._registrations: list[ServiceRegistration] = []

        self._frozen = False

    def register_instance(
        self,
        interface: type[Any],
        implementation: Any,
        *,
        scope: str,
    ) -> None:

        if self._frozen:
            raise RuntimeError(
                "service collection frozen",
            )

        self._registrations.append(
            ServiceRegistration(
                interface=interface,
                implementation=implementation,
                scope=scope,
            ),
        )

    def freeze(self) -> None:
        self._frozen = True

    @property
    def registrations(
        self,
    ) -> tuple[ServiceRegistration, ...]:

        return tuple(
            self._registrations,
        )
