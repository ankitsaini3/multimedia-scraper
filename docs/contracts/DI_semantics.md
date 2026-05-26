# Dependency Injection Semantics Contract

Status: Frozen Contract  
Scope: Core Runtime Architecture  
Applies To:
- app/
- services/
- workers/
- plugins/
- playback/
- extraction/
- orchestration/runtime layers

Non-Goals:
- Concrete framework selection
- IoC container implementation details
- Web-framework-specific dependency injection

---

# 1. Purpose

This document defines the canonical Dependency Injection (DI) semantics for the multimedia_scraper system.

The DI system exists to:

- Eliminate hidden global state
- Enable deterministic runtime construction
- Support testability and isolation
- Enforce architectural boundaries
- Enable plugin isolation
- Allow runtime composition without import coupling
- Support lifecycle-aware resource ownership

This contract freezes:
- service registration semantics
- dependency resolution semantics
- ownership rules
- visibility rules
- lifecycle binding
- concurrency guarantees
- failure boundaries

All runtime components MUST comply with this contract.

---

# 2. Ownership

Primary Owner:
- core/runtime

Secondary Owners:
- platform maintainers
- plugin API maintainers

Consumers:
- all services
- orchestrators
- plugins
- workers
- pipelines
- adapters

Only runtime composition layers may construct dependency graphs.

Business logic MUST NEVER manually wire global runtime state.

---

# 3. Architectural Model

The system uses:

- explicit constructor injection
- immutable dependency graphs after startup
- scoped dependency ownership
- interface-oriented resolution
- runtime-managed lifecycle binding

The DI system is NOT:
- a service locator
- a global registry
- mutable shared state
- reflection-heavy magic wiring

---

# 4. Core Concepts

## 4.1 Service

A service is a runtime-managed object with:

- explicit interface contract
- declared lifecycle
- deterministic ownership
- typed dependency set

Examples:
- HTTP client
- FFmpeg manager
- cache backend
- plugin registry
- event bus
- task scheduler

---

## 4.2 Interface

Dependencies MUST resolve through abstract contracts.

Allowed:
- Protocols
- ABCs
- typed interfaces

Forbidden:
- concrete implementation coupling
- runtime monkey patching
- implicit attribute contracts

---

## 4.3 Provider

A provider constructs service instances.

Providers MAY:
- lazily create instances
- eagerly initialize instances
- bind resources to scopes

Providers MUST:
- be deterministic
- be side-effect controlled
- declare dependency requirements

---

## 4.4 Scope

A scope defines service ownership lifetime.

Mandatory scopes:

| Scope | Meaning |
|---|---|
| application | entire runtime lifespan |
| session | temporary orchestration session |
| task | per operation/request/job |
| plugin | isolated plugin-owned scope |

No additional scopes may exist without architecture approval.

---

# 5. Interface Definitions

## 5.1 Service Registration

All services MUST define:

- interface type
- implementation/provider
- scope
- lifecycle policy

Example model:

```python
ServiceDefinition(
    interface=CacheBackend,
    provider=RedisCacheProvider,
    scope="application",
)
````

---

## 5.2 Resolution

Resolution MUST be:

* explicit
* typed
* deterministic

Resolution MUST NOT:

* depend on import order
* depend on runtime mutation
* depend on hidden globals

---

## 5.3 Constructor Injection

Dependencies MUST be provided through constructors or explicit factory methods.

Allowed:

```python
class SearchService:
    def __init__(self, cache: CacheBackend):
        ...
```

Forbidden:

* hidden singleton lookup
* module-level dependency access
* implicit ambient context

---

## 5.4 Optional Dependencies

Optional dependencies MUST be explicitly marked.

Allowed:

* Optional[T]
* nullable interfaces
* feature capability negotiation

Forbidden:

* try/except import injection hacks
* silent fallback mutation

---

# 6. Guarantees

The DI system guarantees:

1. Deterministic graph construction
2. Explicit ownership
3. Scope isolation
4. No hidden runtime dependencies
5. Reproducible test environments
6. Dependency acyclic validation
7. Lifecycle-aligned cleanup
8. Thread-safe read-only resolution after startup
9. Plugin isolation boundaries
10. Typed resolution guarantees

---

# 7. Invariants

The following invariants MUST always hold.

## 7.1 Immutable Graph After Startup

After runtime initialization completes:

* service registrations MUST NOT mutate
* scope topology MUST NOT mutate
* dependency bindings MUST NOT mutate

Exception:

* plugin hot-load systems explicitly designed for dynamic mutation

---

## 7.2 Explicit Construction

Every runtime-managed dependency MUST have:

* explicit owner
* explicit constructor path
* explicit lifecycle binding

---

## 7.3 No Hidden Singletons

No service may create hidden global state outside runtime ownership.

Forbidden:

* module singletons
* hidden caches
* implicit registries

---

## 7.4 Scope Safety

Longer-lived scopes MUST NEVER depend on shorter-lived scopes.

Forbidden:

* application scope depending on task scope
* singleton holding request/task objects

Allowed:

* task scope depending on application scope

---

## 7.5 Acyclic Dependency Graph

The dependency graph MUST remain acyclic.

Circular dependencies are forbidden.

---

# 8. Failure Semantics

## 8.1 Startup Failure

If critical dependency graph construction fails:

* startup MUST fail fast
* runtime MUST NOT partially initialize
* cleanup MUST execute for initialized services

---

## 8.2 Resolution Failure

Resolution failures MUST produce typed exceptions.

Examples:

* DependencyNotFoundError
* ScopeViolationError
* CircularDependencyError

Generic exceptions are forbidden.

---

## 8.3 Provider Failure

Provider construction failures MUST:

* preserve graph integrity
* prevent invalid instance publication
* trigger cleanup if partial initialization occurred

---

## 8.4 Plugin Failure Isolation

Plugin dependency failures MUST NOT corrupt:

* application scope
* unrelated plugins
* runtime registry state

---

## 8.5 Cleanup Failure

Cleanup failures:

* MUST be logged
* MUST NOT corrupt remaining shutdown sequence

---

# 9. Lifecycle Semantics

## 9.1 Lifecycle Ownership

The runtime owns:

* initialization
* startup ordering
* shutdown ordering
* cleanup execution

Services MUST NOT self-register globally.

---

## 9.2 Startup Ordering

Dependencies MUST initialize before dependents.

Example:

```text
HTTP Client
    ↓
API Client
    ↓
Search Service
```

Reverse ordering is forbidden.

---

## 9.3 Shutdown Ordering

Shutdown MUST occur in reverse dependency order.

Dependents terminate before dependencies.

---

## 9.4 Lazy Initialization

Lazy initialization is allowed only if:

* deterministic
* thread-safe
* lifecycle-bound
* failure-safe

---

## 9.5 Scope Disposal

When a scope terminates:

* all owned services MUST cleanup
* resources MUST release deterministically
* references MUST become invalid

---

# 10. Concurrency Semantics

## 10.1 Read-Only Resolution

After startup:

* dependency graph access MUST be read-only
* concurrent resolution MUST be safe

---

## 10.2 Mutation During Runtime

Runtime graph mutation is forbidden unless:

* explicitly supported
* isolated
* synchronized

Default assumption:

* immutable graph

---

## 10.3 Shared Services

Application-scoped services MUST define concurrency safety.

Each service MUST explicitly document:

* thread-safe
* async-safe
* single-thread confined

---

## 10.4 Task Scope Isolation

Task-scoped dependencies MUST NOT leak across concurrent tasks.

---

## 10.5 Plugin Isolation

Plugins MUST NOT mutate shared runtime dependency state.

---

# 11. Allowed Dependencies

Allowed dependency directions:

| Source         | Allowed Targets              |
| -------------- | ---------------------------- |
| app            | services, runtime, contracts |
| services       | contracts, infrastructure    |
| plugins        | plugin API only              |
| workers        | services, runtime            |
| orchestration  | services, runtime            |
| infrastructure | contracts only               |

---

# 12. Forbidden Behaviors

The following are architecturally forbidden.

## 12.1 Hidden Global State

Forbidden:

* module-level mutable service instances
* hidden registries
* implicit caches

---

## 12.2 Service Locator Pattern

Forbidden:

```python
GlobalContainer.resolve(...)
```

inside arbitrary business logic.

---

## 12.3 Runtime Import Wiring

Forbidden:

* import-time registration
* side-effect dependency graph mutation

---

## 12.4 Circular Dependencies

Forbidden under all scopes.

---

## 12.5 Scope Escapes

Forbidden:

* leaking task-scoped objects globally
* retaining disposed scope references

---

## 12.6 Cross-Plugin Internal Access

Plugins MUST NOT directly access:

* other plugin internals
* runtime private services
* hidden implementation containers

---

## 12.7 Mutable Shared Singletons

Forbidden unless:

* explicitly synchronized
* documented
* lifecycle-managed

---

# 13. Testing Requirements

Tests MUST support:

* dependency overrides
* isolated scope creation
* deterministic graph construction
* fake provider injection

Tests MUST NOT:

* depend on global singleton mutation
* share mutable runtime state across suites

---

# 14. Compliance Requirements

Any new subsystem MUST document:

* provided interfaces
* consumed interfaces
* lifecycle scope
* concurrency guarantees
* cleanup behavior

Architecture review is REQUIRED if introducing:

* new scope types
* dynamic runtime mutation
* global registries
* cross-plugin dependency channels

---

