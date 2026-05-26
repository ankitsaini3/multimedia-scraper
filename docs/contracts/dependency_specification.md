# Dependency Specification

Status:

```text id="2v4j5f"
STABLE CONTRACT DRAFT
```

Scope:

```text id="ozr4oe"
Phase 1 — Foundations
```

This specification defines:

* dependency direction rules
* ownership boundaries
* allowed imports
* forbidden imports
* runtime isolation constraints
* plugin dependency constraints
* infrastructure dependency policy
* architectural layering guarantees

This document is intended to be:

```text id="a6h0f0"
architecturally enforceable
```

NOT advisory guidance.

---

# 1. Dependency Philosophy

Dependencies define architecture.

This project enforces:

```text id="x4ggo6"
strict directional dependency flow
```

to guarantee:

* runtime stability
* subsystem isolation
* plugin safety
* deterministic startup
* test isolation
* maintainability
* future extensibility

---

# 2. Foundational Dependency Rule

The runtime foundation must remain independent from feature systems.

Therefore:

```text id="q9n22k"
feature systems depend on runtime
runtime NEVER depends on feature systems
```

This rule is absolute.

---

# 3. Architectural Layer Model

Canonical layer model:

```text id="2o56qh"
core runtime
    ↓
plugin infrastructure
    ↓
provider systems
    ↓
application services
    ↓
interfaces / UI / CLI
```

Dependencies may only move downward.

Reverse dependencies are forbidden.

---

# 4. Stable Runtime Boundary

The following namespace defines the stable runtime layer:

```text id="n5im5l"
src/multimedia_scraper/core/
```

Everything inside this boundary is considered:

```text id="1lfr3u"
FOUNDATIONAL INFRASTRUCTURE
```

---

# 5. Core Runtime Dependency Rules

# Allowed Imports

```text id="r9uz8v"
core/*
    MAY import:
        stdlib
        typing
        collections
        asyncio
        dataclasses
        pathlib
        core/*
        contracts/*
```

Allowed third-party runtime dependencies must remain minimal.

---

# Allowed Infrastructure Libraries

Phase 1 approved libraries:

| Category           | Allowed                  |
| ------------------ | ------------------------ |
| Validation         | pydantic                 |
| Structured logging | structlog                |
| Typing support     | typing_extensions        |
| TOML parsing       | tomli (Python 3.10 only) |

No additional infrastructure dependencies allowed without ADR review.

---

# Forbidden Imports

```text id="8ax8g8"
core/*
    MUST NOT import:
        playback/*
        downloads/*
        providers/*
        browser/*
        extraction/*
        search/*
```

Core runtime must remain feature-agnostic.

---

# 6. Core Runtime Internal Dependency Rules

# Allowed Internal Flow

```text id="cqjlwm"
config
    -> logging
    -> runtime
    -> events
    -> supervision
    -> plugins
```

This represents:

```text id="bjlwmr"
startup dependency direction
```

NOT arbitrary import freedom.

---

# Forbidden Internal Cycles

Forbidden:

```text id="iaytut"
events -> runtime -> events
plugins -> supervision -> plugins
logging -> runtime -> logging
```

Circular runtime dependencies are forbidden.

---

# 7. Runtime Contract Isolation

Concrete runtime implementations MUST NOT leak across boundaries.

Example:

Bad:

```python id="jqk6qf"
from core.events.bus import AsyncEventBus
```

Good:

```python id="rjlwmz"
from core.contracts.events import EventBus
```

Runtime consumers depend on:

```text id="jlwm3k"
contracts
```

NOT implementations.

---

# 8. Contract Namespace Rules

Canonical stable contract namespace:

```text id="a9dq2o"
core/contracts/
```

Contracts define:

* interfaces
* protocols
* DTO boundaries
* lifecycle guarantees
* ownership semantics

Contracts MUST remain implementation-agnostic.

---

# Allowed Contract Dependencies

```text id="4y3jxu"
contracts/*
    MAY import:
        stdlib
        typing
        dataclasses
        typing_extensions
```

---

# Forbidden Contract Dependencies

```text id="4vjlwm"
contracts/*
    MUST NOT import:
        infrastructure libraries
        runtime implementations
        plugins
        providers
```

Contracts must remain stable and portable.

---

# 9. RuntimeContext Dependency Rules

RuntimeContext is the root runtime contract.

Everything runtime-scoped depends downward from it.

Rules:

```text id="snjlwm"
RuntimeContext
    MAY expose:
        stable contracts only
```

It MUST NOT expose:

* concrete implementations
* infrastructure internals
* provider-specific state

---

# 10. Event System Dependency Rules

The event system exists as:

```text id="vjlwm0"
cross-cutting runtime coordination
```

NOT business orchestration.

---

# Allowed Event Dependencies

Events MAY depend on:

* contracts
* runtime DTOs
* typed metadata

---

# Forbidden Event Dependencies

Events MUST NOT depend on:

* playback internals
* provider implementations
* infrastructure libraries
* browser state

---

# Event Handler Dependency Constraints

Handlers MAY:

* resolve runtime services
* emit additional events
* log structured telemetry

Handlers MUST NOT:

* mutate runtime lifecycle
* block indefinitely
* bypass supervision

---

# 11. Supervision Dependency Rules

The supervisor owns runtime task coordination.

---

# Supervisor MAY Depend On

* asyncio
* runtime contracts
* events
* logging

---

# Supervisor MUST NOT Depend On

* providers
* playback
* downloads
* extraction logic

---

# Supervision Isolation Rules

The supervisor coordinates tasks.

It does NOT:

* implement business logic
* understand media semantics
* own provider workflows

---

# 12. Plugin Dependency Rules

Plugins are capability providers.

They are NOT runtime owners.

---

# Plugin MAY Depend On

```text id="njlwm7"
plugins/*
    MAY import:
        core/contracts/*
        provider DTOs
        plugin-specific infrastructure
```

---

# Plugin MUST NOT Depend On

```text id="fjlwm9"
plugins/*
    MUST NOT import:
        core implementation internals
        supervision internals
        runtime state mutation APIs
```

---

# Plugin Isolation Guarantees

Plugins:

* MUST remain runtime-isolated
* MUST interact through contracts
* MUST NOT coordinate global lifecycle

---

# Plugin Registration Rules

Plugins register:

* capabilities
* metadata
* handlers

Plugins do NOT register:

* runtime lifecycle ownership
* supervision ownership
* global mutable state

---

# 13. Provider Dependency Rules

Provider systems exist BELOW runtime contracts.

---

# Providers MAY Depend On

* plugin contracts
* provider DTOs
* provider-specific infrastructure
* extraction infrastructure

---

# Providers MUST NOT Depend On

* playback internals
* runtime implementation internals
* unrelated providers

---

# Provider Isolation Rules

Providers MUST remain isolated from each other.

Direct provider-to-provider dependencies are forbidden.

---

# 14. Application Service Dependency Rules

Application services orchestrate feature workflows.

They exist ABOVE providers.

---

# Services MAY Depend On

* runtime contracts
* plugins
* providers
* DTOs

---

# Services MUST NOT Depend On

* runtime implementation internals
* supervision internals
* infrastructure-specific implementations

---

# 15. CLI Dependency Rules

CLI exists at the outermost boundary.

---

# CLI MAY Depend On

* application services
* runtime contracts
* DTOs

---

# CLI MUST NOT Depend On

* provider internals
* supervision internals
* event dispatch internals

---

# 16. Infrastructure Dependency Policy

Infrastructure libraries are:

```text id="2jlwm0"
replaceable implementation details
```

NOT architecture.

---

# Infrastructure Isolation Rule

Infrastructure libraries MUST remain isolated behind contracts.

Example:

Bad:

```python id="mjlwm8"
from structlog import get_logger
```

outside logging implementation layer.

Good:

```python id="hjlwm1"
from core.contracts.logging import RuntimeLogger
```

---

# Approved Infrastructure Boundaries

| Infrastructure | Boundary                    |
| -------------- | --------------------------- |
| structlog      | logging implementation only |
| asyncio        | runtime/supervision only    |
| pydantic       | config/DTO validation only  |
| tomli          | config loader only          |

---

# 17. Dependency Injection Rules

Dependency wiring occurs ONLY through:

```text id="rjlwm7"
ServiceContainer
```

or explicit constructor injection.

---

# Forbidden Runtime Resolution

Forbidden:

```python id="fjlwm4"
from core.runtime.globals import runtime
```

Forbidden:

```python id="qjlwm6"
ServiceLocator.get(...)
```

---

# Allowed Injection

Allowed:

```python id="njlwm6"
class Service:
    def __init__(
        self,
        logger: RuntimeLogger,
    ) -> None:
        ...
```

---

# 18. Runtime State Ownership Rules

Runtime state has a single owner.

---

# Allowed Mutable Runtime State

Mutable state MAY exist only inside:

* supervision
* runtime lifecycle coordination
* event subscription registry
* plugin registry internals

---

# Forbidden Shared Mutable State

Forbidden:

```text id="4jlwm5"
cross-module mutable global state
```

---

# 19. Concurrency Dependency Rules

Concurrency coordination belongs ONLY to:

* supervision
* runtime lifecycle
* event system

---

# Forbidden Concurrency Ownership

Providers MUST NOT:

* manage global task groups
* own runtime cancellation
* bypass supervision

---

# Allowed Task Creation

Long-lived tasks MUST be:

```text id="zjlwm3"
runtime-supervised
```

Detached tasks are forbidden.

---

# 20. Testing Dependency Rules

Tests MUST preserve architecture boundaries.

---

# Tests MUST NOT

* bypass runtime contracts
* mutate hidden globals
* depend on execution order
* depend on external state

---

# Tests SHOULD

* use typed contracts
* use dependency injection
* isolate runtime state
* mock infrastructure boundaries

---

# 21. Import Direction Summary

Canonical dependency flow:

```text id="1jlwm8"
contracts
    ↓
core runtime
    ↓
plugin infrastructure
    ↓
providers
    ↓
application services
    ↓
CLI/UI
```

Reverse imports are forbidden.

---

# 22. Runtime Stability Rules

The following layers are considered:

```text id="yjlwm9"
public stable architecture
```

* contracts
* runtime context
* event bus
* supervision contracts
* plugin contracts
* dependency rules

Breaking changes require:

* ADR review
* migration strategy
* compatibility analysis

---

# 23. Forbidden Architectural Patterns

Forbidden patterns include:

---

## Hidden Global Runtime

Forbidden:

```python id="7jlwm5"
GLOBAL_RUNTIME = RuntimeContext(...)
```

---

## Runtime Singleton Mutation

Forbidden:

```python id="jlwmq2"
runtime.config.debug = True
```

---

## Feature Leakage Into Runtime

Forbidden:

```python id="4jlwm1"
core.runtime imports playback.mpv
```

---

## Infrastructure Leakage

Forbidden:

```python id="3jlwm2"
provider exposes yt_dlp exceptions
```

---

## Circular Runtime Ownership

Forbidden:

```text id="2jlwm7"
plugins own runtime lifecycle
```

---

# 24. Architectural Enforcement

These dependency rules are intended to become:

```text id="wjlwm4"
CI-enforced architecture constraints
```

Future enforcement MAY include:

* import-linter
* static dependency graph validation
* forbidden import checks
* layering validation

---

# 25. Final Dependency Principle

```text id="rjlwm1"
Dependencies define authority.
```

The runtime foundation must remain:

* isolated
* deterministic
* stable
* infrastructure-agnostic
* feature-agnostic

All feature systems are downstream consumers of the runtime foundation.
