# Integration Boundary Semantics Contract

Status: Frozen Contract  
Criticality: SYSTEM-CRITICAL  
Depends On:
- runtime_invariants.md
- di_semantics.md
- supervisor_tree_semantics.md
- dto_serialization_semantics.md
- plugin_semantics.md
- event_semantics.md
- resource_ownership_semantics.md
- failure_semantics.md
- logging_observability_semantics.md

Applies To:
- plugins
- providers
- services
- runtime
- workers
- orchestration
- event systems
- DTO systems
- external adapters
- subprocess integrations
- IPC boundaries
- cache boundaries
- browser automation
- streaming systems

This document defines the canonical interaction contracts between architectural layers and subsystems.

This contract freezes:
- cross-layer interaction rules
- boundary crossing semantics
- ownership transitions
- event integration semantics
- DTO transport semantics
- supervision interaction rules
- plugin integration rules
- runtime/service interaction semantics

Violation of this contract is considered:
- architectural boundary corruption
- runtime integrity violation
- ownership corruption
- async model corruption
- plugin isolation failure

---

# 1. Purpose

This contract exists to formally define HOW layers interact.

The architecture previously defined:
- layers
- services
- DTOs
- supervision
- runtime semantics

This document freezes:
- allowed interactions
- forbidden interactions
- transport rules
- supervision boundaries
- ownership boundaries
- lifecycle crossing rules

This contract defines the integration laws of the architecture.

If another contract conflicts with this document:
THIS DOCUMENT WINS.

---

# 2. Ownership

Primary Owner:
- core/runtime
- architecture maintainers

Secondary Owners:
- plugin maintainers
- orchestration maintainers
- infrastructure maintainers

All subsystem maintainers MUST comply.

---

# 3. Architectural Boundary Model

The architecture is composed of strict boundaries.

Primary boundaries:

| Boundary | Purpose |
|---|---|
| runtime ↔ services | execution orchestration |
| services ↔ providers | infrastructure access |
| plugins ↔ runtime | isolated extension |
| events ↔ supervision | async coordination |
| DTOs ↔ boundaries | transport safety |
| workers ↔ runtime | supervised execution |
| external adapters ↔ core | external isolation |

Boundaries exist to guarantee:
- isolation
- deterministic ownership
- lifecycle safety
- async correctness
- compatibility stability

---

# 4. Core Integration Invariants

These invariants MUST ALWAYS hold.

---

# 4.1 All Cross-Layer Interaction Must Be Explicit

Subsystems MUST interact through:
- interfaces
- DTOs
- events
- explicit contracts

Forbidden:
- hidden imports
- runtime object tunneling
- implicit ownership transfer
- direct internal mutation

---

# 4.2 Boundaries Must Preserve Isolation

Boundary crossing MUST NOT:
- leak runtime internals
- bypass supervision
- bypass ownership semantics
- bypass validation

Isolation weakening is forbidden.

---

# 4.3 Boundaries Must Preserve Lifecycle Semantics

Cross-layer interaction MUST preserve:
- ownership
- cleanup responsibility
- cancellation propagation
- supervision topology

Boundary crossing MUST NOT create:
- detached resources
- orphan tasks
- unmanaged state

---

# 4.4 Boundaries Must Be Observable

All major boundary crossings MUST remain observable.

Mandatory observability:
- event publication
- plugin invocation
- external adapter calls
- retry escalation
- worker delegation
- subprocess delegation

Invisible integration behavior is forbidden.

---

# 4.5 DTOs Are Mandatory Across Isolation Boundaries

All isolation boundaries MUST use DTO semantics.

Forbidden:
- live runtime object sharing
- service object transport
- mutable shared state across boundaries

---

# 4.6 Runtime Ownership Cannot Be Bypassed

The runtime remains the ultimate owner of:
- lifecycle
- supervision
- resource cleanup
- cancellation propagation

Subsystems MUST NOT bypass runtime authority.

---

# 5. Runtime ↔ Service Semantics

---

# 5.1 Services Are Runtime-Owned

Services:
- are constructed by runtime
- are lifecycle-managed by runtime
- operate inside runtime supervision

Services MUST NOT:
- self-register globally
- create unmanaged execution roots
- bypass supervision tree

---

# 5.2 Services Access Runtime Through Explicit Interfaces

Allowed:
- runtime-provided interfaces
- event APIs
- task APIs
- scoped resource APIs

Forbidden:
- hidden runtime mutation
- direct supervisor graph mutation
- internal runtime state access

---

# 5.3 Services Cannot Own Runtime Lifecycle

Services MAY request:
- task execution
- resource acquisition
- event publication

Services MUST NOT:
- terminate runtime
- mutate runtime topology
- create detached execution systems

---

# 5.4 Runtime ↔ Service Interaction Must Be Scoped

Runtime interactions MUST remain:
- scope-aware
- cancellation-aware
- lifecycle-bound

---

# 6. Service ↔ Provider Semantics

---

# 6.1 Providers Are Infrastructure Boundaries

Providers encapsulate:
- HTTP systems
- storage systems
- browser automation
- FFmpeg integration
- external APIs

Services MUST interact through provider contracts only.

---

# 6.2 Providers Must Not Leak Infrastructure Internals

Providers MUST NOT expose:
- raw sockets
- unmanaged subprocess handles
- internal transport state
- hidden executors

Providers MUST expose:
- stable interfaces
- DTO-safe outputs
- lifecycle-safe handles

---

# 6.3 Services Must Not Bypass Providers

Forbidden:
- direct infrastructure imports
- direct FFmpeg invocation
- direct Playwright process mutation
- direct transport mutation

Infrastructure access MUST pass through providers.

---

# 6.4 Providers Must Remain Runtime-Compliant

Providers MUST obey:
- supervision semantics
- resource ownership semantics
- cancellation semantics
- observability semantics

---

# 7. Plugin ↔ Runtime Semantics

---

# 7.1 Plugins Execute Inside Isolated Runtime Scopes

Plugins:
- execute under plugin supervisors
- receive scoped runtime interfaces
- operate inside runtime ownership

Plugins MUST NOT:
- mutate runtime topology
- access hidden runtime state
- bypass supervision

---

# 7.2 Plugin APIs Must Be Explicit

Plugins MAY access ONLY:
- documented plugin contracts
- capability interfaces
- DTO contracts
- event APIs

Hidden runtime APIs are forbidden.

---

# 7.3 Plugin Failures Must Remain Isolated

Plugin failure MUST NOT:
- corrupt runtime state
- corrupt unrelated plugins
- corrupt supervision topology

---

# 7.4 Plugins Cannot Share Mutable Runtime State

Plugins MUST communicate through:
- DTOs
- events
- explicit APIs

Shared mutable globals are forbidden.

---

# 7.5 Plugin Resource Ownership Must Be Scoped

Plugin-created resources MUST:
- belong to plugin scope
- cleanup during plugin shutdown
- remain observable

---

# 8. Event ↔ Supervision Semantics

---

# 8.1 Event Processing Must Be Supervised

All event consumers MUST:
- execute inside supervision tree
- belong to runtime scopes
- support cancellation

Detached event consumers are forbidden.

---

# 8.2 Event Publication Does Not Transfer Ownership

Publishing an event:
- transfers data
- DOES NOT transfer runtime ownership

Ownership remains with originating scope unless explicitly transferred.

---

# 8.3 Event Failures Must Remain Observable

Event pipeline failures MUST:
- surface through supervision
- preserve correlation metadata
- remain observable

---

# 8.4 Event Handlers Must Be Cancellation-Compliant

Event consumers MUST:
- propagate cancellation
- cleanup safely
- avoid detached retries

---

# 8.5 Event Systems Cannot Bypass Supervision

Forbidden:
- hidden background event loops
- detached consumer pools
- unmanaged retry threads

---

# 9. DTO Boundary Semantics

---

# 9.1 DTOs Are Required At Isolation Boundaries

Mandatory DTO boundaries:
- plugin communication
- worker communication
- IPC
- event transport
- persistence
- external API transport

---

# 9.2 Runtime Objects Cannot Cross DTO Boundaries

Forbidden across boundaries:
- service instances
- supervisors
- tasks
- sockets
- browser handles
- subprocess handles

---

# 9.3 DTO Validation Must Occur At Boundary Entry

Validation MUST occur:
- before plugin execution
- before event publication
- before persistence
- before worker dispatch

Unvalidated boundary ingress is forbidden.

---

# 9.4 DTOs Must Preserve Correlation Metadata

Boundary DTOs MUST support:
- correlation IDs
- tracing context
- causality metadata

---

# 10. Worker ↔ Runtime Semantics

---

# 10.1 Workers Are Runtime-Supervised

Workers MUST:
- belong to supervisor tree
- support cancellation
- expose health state
- obey bounded concurrency

---

# 10.2 Worker Inputs Must Be DTO-Based

Workers MUST receive:
- validated DTOs
- explicit commands
- transport-safe payloads

Shared mutable runtime state is forbidden.

---

# 10.3 Workers Cannot Escape Supervision

Forbidden:
- detached worker threads
- unmanaged executors
- hidden event loops

---

# 11. External Adapter ↔ Core Semantics

---

# 11.1 External Systems Must Be Adapter-Isolated

External systems include:
- YouTube APIs
- browser automation
- FFmpeg
- filesystem
- network transports

External integration MUST remain isolated behind adapters/providers.

---

# 11.2 Core Domain Must Remain Infrastructure-Agnostic

Core systems MUST NOT depend directly on:
- Playwright internals
- FFmpeg CLI details
- raw HTTP client implementations

---

# 11.3 External Failures Must Be Translated

External failures MUST:
- become typed runtime failures
- preserve observability
- preserve retry semantics

Raw infrastructure exceptions MUST NOT leak across boundaries.

---

# 12. Failure Boundary Semantics

---

# 12.1 Failures Must Not Skip Layers

Failures MUST propagate through:
- explicit contracts
- typed boundaries
- supervision chains

Hidden failure tunneling is forbidden.

---

# 12.2 Boundary Translation Must Be Explicit

Boundaries MUST define:
- incoming exception model
- outgoing exception model
- retry semantics
- escalation semantics

---

# 12.3 Fatal Boundary Corruption

The following are considered fatal:
- supervision bypass
- detached execution
- ownership corruption
- runtime object leakage
- plugin isolation failure

---

# 13. Lifecycle Boundary Semantics

---

# 13.1 Lifecycle Ownership Cannot Cross Implicitly

Boundary crossing MUST NOT:
- transfer cleanup responsibility implicitly
- create ambiguous ownership
- create detached lifetimes

---

# 13.2 Scope Shutdown Must Cascade Correctly

Scope shutdown MUST cascade through:
runtime
→ supervisors
→ services
→ providers
→ resources

---

# 13.3 Plugin Shutdown Must Reconcile Internal Resources

Plugin unload MUST:
- cancel plugin tasks
- cleanup plugin resources
- drain plugin events
- reconcile plugin failures

---

# 14. Concurrency Boundary Semantics

---

# 14.1 Shared Mutable State Across Layers Is Forbidden

Cross-layer communication MUST use:
- immutable DTOs
- events
- explicit synchronization

---

# 14.2 Boundary Crossing Must Preserve Cancellation

Cancellation MUST propagate across:
- worker boundaries
- plugin boundaries
- provider boundaries
- event pipelines

---

# 14.3 Cross-Layer Concurrency Limits Must Be Explicit

Subsystems MUST define:
- concurrency budgets
- queue semantics
- backpressure semantics

---

# 15. Observability Boundary Semantics

---

# 15.1 Correlation Context Must Cross Boundaries

Boundary transitions MUST preserve:
- correlation IDs
- tracing context
- causality chains

---

# 15.2 Boundary Operations Must Emit Telemetry

Mandatory telemetry:
- plugin invocation
- provider invocation
- worker dispatch
- event publication
- retry escalation
- failure translation

---

# 16. Allowed Dependencies

Allowed:
- interface-based integration
- DTO-based transport
- supervised event systems
- scoped runtime APIs
- capability-oriented plugin APIs
- adapter/provider isolation

Allowed architectural patterns:
- ports-and-adapters
- hexagonal architecture
- structured async boundaries
- supervised worker delegation

---

# 17. Forbidden Behaviors

---

# 17.1 Runtime Object Leakage Across Boundaries

Forbidden under all circumstances.

---

# 17.2 Supervision Bypass

Forbidden:
- detached tasks
- unmanaged worker pools
- hidden event loops

---

# 17.3 Hidden Cross-Layer Mutation

Forbidden:
- internal runtime mutation
- plugin mutation of global state
- provider mutation of runtime topology

---

# 17.4 Cross-Layer Shared Mutable State

Forbidden under all circumstances.

---

# 17.5 Direct Infrastructure Coupling

Forbidden:
- services directly controlling FFmpeg
- services directly mutating browser processes
- plugins directly accessing infrastructure internals

---

# 17.6 Hidden Ownership Transfer

Forbidden.

---

# 17.7 Unvalidated Boundary Inputs

Forbidden under all circumstances.

---

# 17.8 Boundary-Crossing Circular Dependencies

Forbidden:
- plugin ↔ runtime cycles
- service ↔ provider cycles
- worker ↔ runtime ownership inversion

---

# 18. Compliance Requirements

Every subsystem boundary MUST document:
- ownership semantics
- DTO contracts
- supervision semantics
- cancellation semantics
- observability semantics
- retry semantics
- failure translation rules
- concurrency semantics

Subsystems unable to define these are NOT boundary compliant.

---

# 19. Frozen Architecture Rules

The following rules are frozen:

1. All cross-layer interaction must be explicit
2. Isolation boundaries must hold
3. DTOs are mandatory across isolation boundaries
4. Runtime ownership cannot be bypassed
5. Services are runtime-owned
6. Infrastructure access must pass through providers
7. Plugins execute in isolated scopes
8. Event processing must be supervised
9. Runtime objects cannot cross boundaries
10. Worker execution must remain supervised
11. External systems must remain adapter-isolated
12. Failures must propagate through typed boundaries
13. Shared mutable cross-layer state is forbidden
14. Correlation context must cross boundaries
15. Supervision bypass is forbidden

Any violation requires formal architectural revision.
```
