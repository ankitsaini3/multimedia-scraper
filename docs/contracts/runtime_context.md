# Runtime Contracts — Foundations

Status:

```text
STABLE CONTRACT DRAFT
```

Scope:

```text
Phase 1 — Core Runtime ONLY
```

This document defines:

* stable runtime contracts
* ownership boundaries
* lifecycle guarantees
* dependency rules
* concurrency semantics
* failure semantics

These contracts are intended to stabilize BEFORE implementation.

---

# 1. Runtime Philosophy

The runtime layer is:

```text
the operating system of the application
```

It owns:

* lifecycle
* configuration
* logging
* supervision
* event routing
* dependency wiring
* runtime state
* plugin coordination

It does NOT own:

* playback
* downloads
* browser automation
* provider-specific logic

---

# 2. Runtime Design Constraints

The runtime MUST be:

* async-first
* deterministic
* observable
* testable
* cancellation-safe
* plugin-safe
* dependency-injected
* explicitly owned

The runtime MUST NOT:

* rely on hidden globals
* mutate shared state unpredictably
* depend on feature systems
* leak infrastructure implementation details

---

# 3. Runtime Layer Structure

Stable runtime namespace:

```text id="d8s6m5"
core/
├── config/
├── contracts/
├── dependency_injection/
├── events/
├── exceptions/
├── lifecycle/
├── logging/
├── plugins/
├── runtime/
└── supervision/
```

Everything here is considered:

```text id="jlwm5m"
FOUNDATIONAL INFRASTRUCTURE
```

Breaking changes require ADR review.

---

# 4. Runtime Ownership Model

# Runtime Owns

* startup
* shutdown
* dependency graph
* configuration lifecycle
* service registration
* event propagation
* supervision trees
* cancellation propagation
* runtime-scoped resources

---

# Runtime Does NOT Own

* media operations
* provider-specific extraction
* playback state
* browser automation state
* domain business logic

---

# 5. Stable Runtime Contracts

The following contracts are considered public stable contracts:

| Contract         | Stability |
| ---------------- | --------- |
| RuntimeContext   | Stable    |
| EventBus         | Stable    |
| Supervisor       | Stable    |
| PluginRegistry   | Stable    |
| RuntimeLogger    | Stable    |
| ConfigProvider   | Stable    |
| ServiceContainer | Stable    |

These interfaces must remain backward compatible.

---

# 6. RuntimeContext Contract

Purpose:

```text id="8f6zgo"
authoritative runtime coordination object
```

The runtime context is the root runtime object.

All runtime-scoped services are accessed through it.

---

# Contract Definition

```python id="a1i7jv"
from typing import Protocol

class RuntimeContext(Protocol):

    config: "AppConfig"
    logger: "RuntimeLogger"
    event_bus: "EventBus"
    supervisor: "Supervisor"
    container: "ServiceContainer"
    plugins: "PluginRegistry"

    async def startup(self) -> None:
        ...

    async def shutdown(self) -> None:
        ...

    @property
    def is_started(self) -> bool:
        ...

    @property
    def is_shutdown(self) -> bool:
        ...
```

---

# RuntimeContext Guarantees

## Guaranteed After startup()

After successful startup:

* config is immutable
* logger is operational
* event bus is operational
* supervisor is operational
* dependency container is frozen
* plugin registry is initialized

---

## Shutdown Guarantees

shutdown():

* is idempotent
* propagates cancellation globally
* drains supervised tasks
* flushes logging
* shuts down plugins
* releases runtime resources

---

# RuntimeContext Concurrency Semantics

Rules:

* startup() MUST NOT run concurrently
* shutdown() MUST NOT run concurrently
* shutdown() cancels remaining runtime tasks
* runtime state transitions are atomic

---

# RuntimeContext Failure Semantics

startup() failure:

```text id="jfd1ln"
runtime considered unusable
```

Partial startup must trigger rollback cleanup.

shutdown() failures:

* MUST be logged
* MUST preserve root causes
* MUST continue best-effort cleanup

---

# 7. ConfigProvider Contract

Purpose:

```text id="9ol7r0"
deterministic runtime configuration source
```

---

# Contract Definition

```python id="vbb0c8"
from typing import Protocol

class ConfigProvider(Protocol):

    def load(self) -> "AppConfig":
        ...
```

---

# ConfigProvider Guarantees

The provider MUST:

* load deterministically
* validate before returning
* return immutable configuration
* preserve override precedence

---

# Override Order

Frozen behavior:

```text id="u1lzfi"
defaults
    -> config files
    -> environment variables
    -> CLI overrides
```

This order MUST NEVER change.

---

# ConfigProvider Failure Semantics

Invalid configuration MUST:

* fail immediately
* raise typed exceptions
* never partially initialize runtime

---

# 8. RuntimeLogger Contract

Purpose:

```text id="whcc49"
structured runtime observability interface
```

The logger contract abstracts logging implementation details.

Infrastructure logging libraries must remain internal.

---

# Contract Definition

```python id="smpaxn"
from typing import Protocol
from typing import Any

class RuntimeLogger(Protocol):

    def debug(self, message: str, **context: Any) -> None:
        ...

    def info(self, message: str, **context: Any) -> None:
        ...

    def warning(self, message: str, **context: Any) -> None:
        ...

    def error(self, message: str, **context: Any) -> None:
        ...

    def critical(self, message: str, **context: Any) -> None:
        ...
```

---

# RuntimeLogger Guarantees

Logging MUST:

* support structured context
* support correlation IDs
* support runtime-scoped enrichment
* support async-safe logging

Logging MUST NOT:

* expose infrastructure logger internals
* leak secrets
* mutate runtime state

---

# Logging Failure Semantics

Logging failures:

* MUST NOT crash runtime
* MUST degrade gracefully
* MUST preserve operational visibility where possible

---

# 9. EventBus Contract

Purpose:

```text id="0fpj4n"
typed in-process runtime coordination
```

The event bus enables:

* lifecycle notifications
* supervision coordination
* observability hooks
* plugin-safe signaling

It is NOT intended as a distributed messaging system.

---

# Contract Definition

```python id="qmg8jx"
from typing import Protocol
from collections.abc import Awaitable, Callable

EventHandler = Callable[[\"Event\"], Awaitable[None]]

class EventBus(Protocol):

    async def publish(self, event: "Event") -> None:
        ...

    async def subscribe(
        self,
        event_type: type["Event"],
        handler: EventHandler,
    ) -> "Subscription":
        ...

    async def unsubscribe(
        self,
        subscription: "Subscription",
    ) -> None:
        ...
```

---

# EventBus Guarantees

The bus is:

* in-process only
* async-aware
* typed
* runtime-scoped

Delivery semantics:

```text id="z44y7y"
at-most-once delivery
```

No persistence guarantees.

---

# EventBus Isolation Rules

Subscriber failures:

* MUST NOT crash publishers
* MUST be isolated
* MUST be logged

Event handlers:

* MUST NOT block indefinitely
* MUST be cancellation-safe

---

# EventBus Ordering Semantics

Ordering guarantees:

```text id="t6twwm"
NO global ordering guarantee
```

Per-event-type ordering MAY exist later but is NOT guaranteed.

---

# 10. Supervisor Contract

Purpose:

```text id="chp7uy"
runtime task lifecycle ownership
```

The supervisor owns:

* task hierarchy
* fault containment
* cancellation propagation
* graceful shutdown coordination

---

# Contract Definition

```python id="jz0wvg"
from typing import Protocol
from collections.abc import Awaitable

class Supervisor(Protocol):

    async def start(self) -> None:
        ...

    async def shutdown(self) -> None:
        ...

    async def spawn(
        self,
        task: Awaitable[object],
        *,
        name: str,
    ) -> "TaskHandle":
        ...
```

---

# Supervisor Guarantees

The supervisor MUST:

* track runtime-owned tasks
* propagate cancellation
* support graceful shutdown
* isolate task failures

---

# Supervisor Failure Semantics

Unsupervised tasks are forbidden.

Task failures:

* MUST be observable
* MUST preserve root causes
* MUST trigger structured logging
* MUST support future restart policies

---

# Supervisor Concurrency Rules

The supervisor owns runtime task lifetimes.

Rules:

* tasks MUST NOT outlive runtime
* cancellation propagates downward
* orphan tasks are forbidden

---

# 11. ServiceContainer Contract

Purpose:

```text id="jv2e11"
runtime dependency wiring and service ownership
```

The container owns runtime-scoped service registration.

---

# Contract Definition

```python id="h0r1yf"
from typing import Protocol
from typing import TypeVar

T = TypeVar(\"T\")

class ServiceContainer(Protocol):

    def register(
        self,
        interface: type[T],
        implementation: T,
    ) -> None:
        ...

    def resolve(
        self,
        interface: type[T],
    ) -> T:
        ...
```

---

# ServiceContainer Guarantees

The container MUST:

* resolve deterministically
* preserve singleton ownership rules
* prevent duplicate registration
* freeze after runtime startup

---

# ServiceContainer Forbidden Behavior

The container MUST NOT:

* perform hidden imports
* mutate services after freeze
* contain business logic

---

# 12. PluginRegistry Contract

Purpose:

```text id="w9r2e5"
runtime-scoped plugin capability coordination
```

The registry coordinates plugins.

It does NOT execute provider business logic.

---

# Contract Definition

```python id="uqjlwm"
from typing import Protocol
from collections.abc import Sequence

class PluginRegistry(Protocol):

    async def register(
        self,
        plugin: "Plugin",
    ) -> None:
        ...

    def plugins(self) -> Sequence["Plugin"]:
        ...

    def capabilities(self) -> Sequence["Capability"]:
        ...
```

---

# PluginRegistry Guarantees

The registry MUST:

* validate plugin metadata
* preserve capability isolation
* prevent duplicate registrations
* support lifecycle coordination

---

# PluginRegistry Forbidden Behavior

The registry MUST NOT:

* own runtime lifecycle
* supervise arbitrary tasks
* directly mutate runtime context

---

# 13. Dependency Rules

# Allowed Dependencies

```text id="7ltcwx"
core/*
    MAY import:
        stdlib
        core/*
        contracts/*
```

---

# Forbidden Dependencies

```text id="zyjlwm"
core/*
    MUST NOT import:
        playback/*
        downloads/*
        providers/*
        browser/*
```

---

# Plugin Dependency Rules

Plugins MAY depend on:

* core contracts
* runtime interfaces
* provider DTOs

Plugins MUST NOT depend on:

* concrete runtime implementations
* internal supervision implementation details

---

# 14. Runtime Lifecycle Contract

# Startup Sequence

Frozen startup order:

```text id="alaj3w"
configuration
    -> logging
    -> dependency container
    -> event bus
    -> supervisor
    -> plugin registry
    -> runtime activation
```

This order is considered stable architecture.

---

# Shutdown Sequence

Frozen shutdown order:

```text id="zkm68l"
stop accepting work
    -> propagate cancellation
    -> stop supervised tasks
    -> shutdown plugins
    -> flush logging
    -> release resources
```

---

# 15. Runtime State Machine

Stable runtime states:

```text id="f5xjlwm"
INITIALIZED
    -> STARTING
    -> RUNNING
    -> SHUTTING_DOWN
    -> STOPPED
```

Illegal transitions are forbidden.

---

# 16. Exception Boundary Rules

Infrastructure exceptions MUST NOT cross runtime contracts.

Boundary translation is mandatory.

Example:

```python id="3zjlwm"
try:
    ...
except SomeInfrastructureError as exc:
    raise RuntimeSystemError(...) from exc
```

---

# 17. Stability Policy

These contracts are considered:

```text id="6jlwmq"
FOUNDATIONAL PUBLIC ARCHITECTURE
```

Breaking changes require:

* ADR review
* migration analysis
* compatibility evaluation
* lifecycle impact review

These contracts stabilize BEFORE feature implementation begins.
