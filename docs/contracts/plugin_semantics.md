# Plugin Semantics

Status:

```text id="plg7m2"
STABLE CONTRACT DRAFT
```

Scope:

```text id="plg1x9"
Phase 1 — Runtime Foundations
Phase 2 — Plugin Infrastructure
```

This specification defines:

* plugin contracts
* capability semantics
* plugin lifecycle
* plugin isolation guarantees
* dependency constraints
* runtime ownership boundaries
* plugin activation rules
* plugin failure semantics
* plugin observability semantics
* compatibility guarantees

This document is:

```text id="plg4k0"
architecturally authoritative
```

All plugin implementations must conform to these semantics.

---

# 1. Plugin Philosophy

Plugins exist to provide:

* extensibility
* provider isolation
* capability composition
* runtime-safe integration
* replaceable external integrations

Plugins are:

```text id="plg0w5"
capability providers
```

NOT runtime owners.

---

# 2. Foundational Plugin Rule

Plugins operate:

```text id="plg9r1"
inside runtime boundaries
```

Plugins MUST NOT:

* own runtime lifecycle
* mutate runtime coordination state
* bypass supervision
* control global runtime behavior

The runtime remains authoritative.

---

# 3. Plugin Scope

Plugins are responsible for:

* provider integrations
* provider-specific metadata
* capability exposure
* provider-specific workflows
* provider-specific event handling

Plugins are NOT responsible for:

* runtime startup
* runtime shutdown
* supervision ownership
* event system ownership
* dependency container ownership

---

# 4. Plugin Ownership Model

# Runtime Owns

* plugin lifecycle
* plugin activation ordering
* plugin shutdown ordering
* plugin isolation
* plugin registration

---

# PluginRegistry Owns

* registration
* capability indexing
* compatibility validation
* lifecycle coordination

---

# Plugins Own

* plugin-local state
* plugin-local resources
* provider-specific infrastructure
* capability implementation

---

# Plugins Do NOT Own

* runtime lifecycle
* global cancellation root
* supervision root
* runtime state machine

---

# 5. Plugin Contract

Canonical plugin contract:

```python id="plg_evt1"
from typing import Protocol
from collections.abc import Sequence

class Plugin(Protocol):

    metadata: "PluginMetadata"

    async def initialize(
        self,
        context: "RuntimeContext",
    ) -> None:
        ...

    async def activate(self) -> None:
        ...

    async def deactivate(self) -> None:
        ...

    async def shutdown(self) -> None:
        ...

    def capabilities(self) -> Sequence["Capability"]:
        ...
```

This contract is considered:

```text id="plg_g0w5"
stable public architecture
```

---

# 6. PluginMetadata Semantics

Canonical metadata contract:

```python id="plg_evt2"
from dataclasses import dataclass

@dataclass(frozen=True)
class PluginMetadata:

    name: str
    version: str
    api_version: str
    description: str
```

Metadata MUST be immutable.

---

# 7. Plugin Identity Rules

Plugin identity MUST be:

```text id="plg_m9r1"
globally unique within runtime
```

Duplicate plugin names are forbidden.

---

# 8. Capability Semantics

Capabilities define:

```text id="plg_d7k8"
what functionality a plugin provides
```

Capabilities are runtime contracts.

---

# Capability Contract

Canonical capability contract:

```python id="plg_evt3"
from dataclasses import dataclass

@dataclass(frozen=True)
class Capability:

    name: str
    version: str
```

Capabilities MUST remain immutable.

---

# 9. Capability Rules

Capabilities MUST:

* be declarative
* remain runtime-safe
* remain implementation-agnostic
* expose stable interfaces

Capabilities MUST NOT:

* expose infrastructure internals
* expose mutable runtime state
* expose runtime ownership APIs

---

# 10. Plugin Lifecycle State Machine

Canonical plugin lifecycle:

```text id="plg_x3u6"
DISCOVERED
    -> VALIDATED
    -> REGISTERED
    -> INITIALIZED
    -> ACTIVE
    -> DEACTIVATED
    -> SHUTDOWN
    -> UNLOADED
```

This lifecycle is stable architecture.

---

# 11. DISCOVERED Semantics

Meaning:

```text id="plg_f5l2"
plugin located but not trusted
```

At this stage:

* metadata MAY be inspected
* execution MUST NOT occur

---

# 12. VALIDATED Semantics

Meaning:

```text id="plg_p8j4"
plugin compatibility verified
```

Validation includes:

* API version compatibility
* metadata validation
* capability validation

Invalid plugins MUST NOT activate.

---

# 13. REGISTERED Semantics

Meaning:

```text id="plg_q2n7"
plugin registered in PluginRegistry
```

At this stage:

* plugin visible to runtime
* capabilities indexed
* plugin inactive

---

# 14. INITIALIZED Semantics

Meaning:

```text id="plg_t9k5"
plugin runtime context attached
```

Initialization MAY:

* allocate plugin-local resources
* subscribe to runtime events
* prepare internal state

Initialization MUST NOT:

* start detached runtime tasks
* mutate runtime lifecycle
* bypass supervision

---

# 15. ACTIVE Semantics

Meaning:

```text id="plg_u4x1"
plugin operational
```

During ACTIVE:

* capabilities usable
* event handling active
* supervised work allowed

---

# 16. DEACTIVATED Semantics

Meaning:

```text id="plg_z7y3"
plugin disabled but not fully released
```

At this stage:

* capability execution stops
* subscriptions MAY remain draining

---

# 17. SHUTDOWN Semantics

Meaning:

```text id="plg_e6w9"
plugin cleanup in progress
```

Plugins MUST:

* release resources
* stop plugin-local work
* participate in cancellation

---

# 18. UNLOADED Semantics

Meaning:

```text id="plg_n1r4"
plugin fully removed from runtime
```

At this stage:

* no plugin-owned runtime resources remain
* no plugin tasks remain active

---

# 19. Plugin Activation Semantics

Plugins activate ONLY after:

* runtime RUNNING state reached
* event bus operational
* supervision operational
* dependency container frozen

Activation before runtime stability is forbidden.

---

# 20. Plugin Shutdown Ordering

Plugin shutdown occurs BEFORE:

```text id="plg_s8p6"
runtime resource release
```

This guarantees:

* logging still available
* supervision still available
* event system still available

during plugin cleanup.

---

# 21. Plugin Isolation Semantics

Plugins are:

```text id="plg_v2j8"
runtime-isolated components
```

Plugin failures MUST remain isolated.

---

# Isolation Guarantees

One plugin MUST NOT:

* corrupt unrelated plugins
* mutate global runtime state
* terminate runtime unexpectedly
* bypass supervision boundaries

---

# 22. Plugin Failure Semantics

Plugin failures MUST:

* preserve root causes
* emit structured logs
* remain observable
* remain isolated

---

# Initialization Failure Rules

Plugin initialization failure:

* MUST prevent activation
* MUST preserve runtime stability
* MUST NOT crash unrelated plugins

---

# Activation Failure Rules

Plugin activation failure:

* MUST isolate plugin
* MUST preserve runtime operation
* MUST emit observability signals

---

# 23. Plugin Dependency Rules

Plugins MAY depend on:

* stable runtime contracts
* provider-specific infrastructure
* capability DTOs

Plugins MUST NOT depend on:

* runtime implementation internals
* supervision internals
* mutable runtime state

---

# 24. Plugin RuntimeContext Rules

Plugins receive:

```text id="plg_w6m3"
restricted runtime access
```

through RuntimeContext.

Plugins MUST treat RuntimeContext as:

```text id="plg_x1n7"
read-only coordination interface
```

---

# Plugins MAY

* publish events
* resolve stable services
* spawn supervised tasks
* log structured telemetry

---

# Plugins MUST NOT

* mutate runtime lifecycle
* freeze runtime
* shutdown runtime
* mutate dependency graph

---

# 25. Plugin Concurrency Semantics

Plugins operate within runtime concurrency rules.

Plugins MUST:

* use supervised tasks
* support cancellation
* support graceful shutdown

Plugins MUST NOT:

* create detached tasks
* create unmanaged worker pools
* bypass runtime cancellation

---

# 26. Plugin Event Semantics

Plugins MAY:

* publish runtime events
* subscribe to runtime events

Plugins MUST NOT:

* assume event ordering
* depend on synchronous dispatch
* mutate event payloads

---

# 27. Plugin Resource Ownership

Plugins own ONLY:

* plugin-local resources
* plugin-local state
* plugin-local infrastructure

Plugins MUST release owned resources during shutdown.

---

# 28. Plugin Registration Semantics

Registration is:

```text id="plg_y9r4"
runtime-controlled
```

Plugins MUST NOT self-register outside runtime lifecycle.

---

# Duplicate Registration Rules

Duplicate plugin identities are forbidden.

Duplicate capability registration MAY be allowed later depending on capability semantics.

Current contract leaves this implementation-defined.

---

# 29. Plugin Compatibility Semantics

Plugins MUST declare:

```text id="plg_z5t8"
runtime API compatibility
```

Incompatible plugins MUST NOT activate.

---

# Compatibility Guarantees

The runtime guarantees:

* stable plugin contracts
* lifecycle guarantees
* capability semantics

The runtime does NOT guarantee:

* internal implementation stability
* infrastructure library stability

---

# 30. Plugin Discovery Semantics

Discovery identifies candidate plugins.

Discovery does NOT imply:

* trust
* activation
* compatibility
* execution permission

---

# 31. Plugin Observability Semantics

The runtime MUST emit observable signals for:

* plugin discovered
* plugin validated
* plugin initialized
* plugin activated
* plugin deactivated
* plugin shutdown
* plugin failure

Silent plugin failure is forbidden.

---

# 32. Plugin Security Semantics

Plugins are:

```text id="plg_a2m9"
trusted runtime extensions
```

Phase 1 does NOT provide:

* sandboxing
* process isolation
* capability security boundaries

Plugins execute with runtime trust.

---

# 33. Plugin Testing Semantics

Plugin contract tests MUST verify:

* lifecycle compliance
* capability declaration
* cancellation participation
* supervision compliance
* isolation guarantees
* structured observability
* graceful shutdown

---

# 34. Illegal Plugin Behaviors

Forbidden behaviors include:

---

## Detached Runtime Tasks

Forbidden:

```python id="plg_evt4"
asyncio.create_task(...)
```

outside supervision ownership.

---

## Runtime Lifecycle Mutation

Forbidden:

```python id="plg_evt5"
runtime.shutdown()
```

from plugin logic.

---

## Mutable Runtime Contracts

Forbidden:

```python id="plg_evt6"
runtime.config.debug = True
```

---

## Plugin-Owned Global State

Forbidden:

```python id="plg_evt7"
GLOBAL_PLUGIN_STATE = ...
```

---

## Infrastructure Leakage

Forbidden:

```python id="plg_evt8"
raise ProviderInternalException(...)
```

across public capability boundaries.

---

# 35. Plugin Stability Policy

The following are considered:

```text id="plg_b4r7"
FOUNDATIONAL STABLE PLUGIN SEMANTICS
```

* plugin lifecycle
* capability semantics
* plugin isolation guarantees
* activation rules
* runtime ownership boundaries
* plugin concurrency constraints

Breaking changes require:

* ADR review
* compatibility analysis
* migration strategy
* provider ecosystem impact review

---

# 36. Final Plugin Principle

```text id="plg_c6n2"
Plugins provide capabilities.
The runtime owns coordination.
```

Plugins extend the system while remaining fully constrained by:

* runtime lifecycle
* supervision ownership
* event semantics
* dependency boundaries
* cancellation semantics
* observability guarantees.
