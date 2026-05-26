# Runtime Invariants Contract

Status: Frozen Contract  
Criticality: SYSTEM-CRITICAL  
Scope: Entire Runtime System  
Priority: Highest

Applies To:
- core runtime
- orchestration
- async execution model
- workers
- event systems
- plugins
- streaming
- download pipeline
- browser automation
- cache systems
- task execution
- resource management

This document defines the non-negotiable runtime invariants of the multimedia_scraper architecture.

These invariants exist to guarantee:
- async correctness
- deterministic execution
- fault containment
- cancellation safety
- resource integrity
- concurrency safety
- lifecycle consistency
- observability correctness

Violation of runtime invariants is considered:
- architectural corruption
- undefined behavior
- production-critical failure

---

# 1. Purpose

This contract freezes the core runtime assumptions that all subsystems MUST obey.

The runtime invariants define:
- what is always true
- what can never happen
- what all async components may safely assume

This document is the foundation of:
- async semantics
- lifecycle semantics
- event semantics
- worker semantics
- plugin semantics
- failure semantics

If another contract conflicts with this document:
THIS DOCUMENT WINS.

---

# 2. Ownership

Primary Owner:
- core/runtime

Secondary Owners:
- orchestration maintainers
- async infrastructure maintainers

All subsystem owners are REQUIRED to comply.

No subsystem may weaken these invariants.

---

# 3. Runtime Model

The runtime is defined as:

- async-first
- cancellation-aware
- lifecycle-bound
- structured-concurrency-oriented
- resource-owned
- deterministic
- isolation-oriented

The runtime is NOT:
- thread-per-task
- fire-and-forget
- globally mutable
- implicitly synchronized
- best-effort cleanup

---

# 4. Global Runtime Invariants

These invariants MUST ALWAYS hold.

---

# 4.1 Single Runtime Ownership

There MUST be exactly one active root runtime owner.

The root runtime owns:
- lifecycle
- cancellation propagation
- shutdown sequencing
- resource cleanup
- task supervision

Forbidden:
- multiple competing runtime roots
- detached orphan runtimes
- nested unmanaged event loops

---

# 4.2 Structured Concurrency

All async tasks MUST belong to a parent scope.

Every spawned task MUST:
- have an owner
- have cancellation propagation
- have lifecycle binding
- terminate before parent scope exit

Forbidden:
- orphan tasks
- detached background tasks
- unmanaged create_task usage
- immortal tasks

Allowed:
- supervised task groups
- owned worker pools
- lifecycle-managed background services

---

# 4.3 No Fire-and-Forget Tasks

Fire-and-forget async execution is forbidden.

Every task MUST satisfy ALL:
- observable
- cancellable
- awaited or supervised
- lifecycle-bound

Forbidden:

```python
asyncio.create_task(fn())
````

without ownership tracking.

---

# 4.4 Deterministic Shutdown

Shutdown MUST be deterministic.

The runtime MUST guarantee:

1. cancellation propagation
2. ordered shutdown
3. resource cleanup
4. final task reconciliation
5. event draining policies

Shutdown MUST NOT:

* abandon active tasks
* leak resources
* silently suppress fatal failures

---

# 4.5 Cancellation Is Normal Control Flow

Cancellation is NOT exceptional corruption.

All async components MUST:

* propagate cancellation
* remain cleanup-safe
* remain idempotent under cancellation

Forbidden:

* swallowing CancelledError
* retry loops ignoring cancellation
* cancellation suppression without explicit reason

Allowed:

* temporary shielding for critical cleanup sections

---

# 4.6 Resource Ownership Is Explicit

Every resource MUST have exactly one owner.

Resources include:

* sockets
* subprocesses
* ffmpeg processes
* browser instances
* streams
* file handles
* locks
* semaphores
* queues
* temporary files

Ownership MUST define:

* creator
* lifecycle
* cleanup responsibility
* failure boundary

---

# 4.7 No Resource Leaks

The runtime MUST guarantee eventual cleanup for:

* tasks
* subprocesses
* transports
* temporary files
* browser sessions
* network connections

Resources MUST NOT outlive their owning scope.

---

# 4.8 Async Boundaries Must Be Explicit

Async transitions MUST be explicit.

Forbidden:

* hidden blocking I/O
* sync wrappers around async internals
* implicit thread blocking inside event loop

Blocking operations MUST:

* move to worker threads/processes
* declare execution semantics

---

# 4.9 Event Loop Integrity

The event loop MUST NEVER be blocked by:

* CPU-heavy work
* synchronous subprocess waiting
* blocking filesystem calls
* blocking network calls
* busy waits

Long-running CPU work MUST:

* use worker pools
* use subprocess isolation
* use external executors

---

# 4.10 Failure Containment

Failures MUST remain bounded.

A subsystem failure MUST NOT corrupt:

* runtime scheduler
* unrelated scopes
* dependency graph
* event system integrity

Failures MUST propagate through:

* typed boundaries
* supervised ownership chains

---

# 4.11 Immutable Runtime Topology After Startup

After startup:

* runtime ownership graph is immutable
* supervision topology is immutable
* core dependency graph is immutable

Exception:

* explicitly documented hot-reload/plugin systems

---

# 4.12 Scope Integrity

Scopes MUST obey strict ownership rules.

Parent scopes:

* own child scopes
* supervise child scopes
* cancel child scopes

Child scopes MUST NOT:

* outlive parent scope
* mutate parent lifecycle state

---

# 4.13 Cleanup Must Be Idempotent

Cleanup operations MUST be safe to execute:

* multiple times
* after partial failure
* after cancellation

Cleanup MUST NOT:

* resurrect resources
* recreate runtime state
* spawn detached work

---

# 4.14 Runtime State Must Be Observable

Critical runtime state MUST be observable.

The runtime MUST expose:

* task ownership
* task states
* active scopes
* cancellation states
* resource counts
* worker saturation
* queue pressure
* fatal failures

Silent runtime state is forbidden.

---

# 4.15 Backpressure Must Exist

All unbounded production systems MUST define backpressure.

Applies to:

* queues
* streams
* downloads
* event pipelines
* worker pools
* buffering systems

Forbidden:

* unbounded memory growth
* infinite queue accumulation
* unconstrained producer rates

---

# 4.16 Bounded Concurrency Is Mandatory

Concurrency MUST be bounded.

Mandatory controls:

* semaphores
* worker limits
* queue limits
* stream limits
* connection limits

Unbounded parallelism is forbidden.

---

# 4.17 Runtime Clock Semantics

Runtime timing MUST use monotonic clocks for:

* deadlines
* timeouts
* retries
* scheduling intervals

Wall clock time MUST NOT control:

* timeout correctness
* cancellation deadlines

---

# 4.18 Async APIs Must Be Honest

Async APIs MUST accurately represent behavior.

Forbidden:

* fake async wrappers over blocking code
* async functions performing hidden sync waits

Allowed:

* explicitly documented executor offloading

---

# 4.19 Isolation Boundaries Must Hold

Plugins, workers, and pipelines MUST remain isolated.

Isolation failures MUST NOT:

* corrupt unrelated scopes
* mutate global runtime state
* break supervision guarantees

---

# 4.20 No Hidden Global Mutable State

Global mutable runtime state is forbidden unless:

* explicitly synchronized
* runtime-owned
* lifecycle-bound
* observable

Forbidden:

* module mutable registries
* hidden caches
* implicit singleton mutation

---

# 5. Interface Definitions

---

# 5.1 Runtime Root Interface

The runtime root MUST expose:

* startup()
* shutdown()
* health_state()
* active_scopes()
* task_snapshot()
* cancellation_state()

---

# 5.2 Scope Interface

Scopes MUST support:

* enter
* exit
* cancellation
* child tracking
* cleanup registration

---

# 5.3 Task Supervision Interface

Task supervisors MUST support:

* spawn
* cancel
* await completion
* failure observation
* structured ownership

---

# 5.4 Resource Interface

Managed resources MUST define:

* acquire
* release
* cleanup semantics
* cancellation behavior

---

# 6. Guarantees

The runtime guarantees:

1. Structured task ownership
2. Deterministic shutdown
3. Cancellation propagation
4. Resource cleanup
5. Failure containment
6. Bounded concurrency
7. Backpressure enforcement
8. Observable runtime state
9. Scope integrity
10. Event loop responsiveness

---

# 7. Failure Semantics

---

# 7.1 Fatal Runtime Corruption

The following are fatal runtime violations:

* orphan tasks
* leaked subprocesses
* event loop blocking
* scope ownership corruption
* cancellation suppression
* supervision graph corruption

Fatal violations MAY require runtime termination.

---

# 7.2 Partial Failure Handling

Partial subsystem failures MUST:

* remain isolated
* preserve runtime integrity
* preserve cancellation correctness

---

# 7.3 Cleanup Failure Handling

Cleanup failures:

* MUST be logged
* MUST NOT abort remaining cleanup chain

---

# 7.4 Cancellation Failure

Ignoring cancellation is a contract violation.

Repeated cancellation violations are considered runtime corruption.

---

# 8. Lifecycle Semantics

---

# 8.1 Runtime Lifecycle Phases

The runtime phases are:

1. bootstrap
2. dependency construction
3. initialization
4. startup
5. active execution
6. draining
7. cancellation
8. cleanup
9. shutdown complete

No subsystem may invent conflicting lifecycle phases.

---

# 8.2 Scope Lifecycle

Every scope MUST obey:

create
→ active
→ draining
→ cancelling
→ cleanup
→ terminated

Skipping phases is forbidden.

---

# 8.3 Resource Lifecycle

Resources MUST obey:

uninitialized
→ acquired
→ active
→ releasing
→ released

---

# 8.4 Task Lifecycle

Tasks MUST obey:

created
→ scheduled
→ running
→ completed/cancelled/failed

Zombie task states are forbidden.

---

# 9. Concurrency Semantics

---

# 9.1 Shared Mutable State

Shared mutable state MUST:

* be minimized
* be synchronized
* define ownership

Unsynchronized shared mutation is forbidden.

---

# 9.2 Lock Ordering

Lock acquisition ordering MUST be deterministic.

Circular lock dependencies are forbidden.

---

# 9.3 Async Lock Semantics

Async locks MUST:

* remain cancellation-safe
* release on failure
* avoid starvation where possible

---

# 9.4 Thread Interaction

Cross-thread runtime interaction MUST be explicit.

Forbidden:

* unsafe event loop access
* implicit loop hopping

---

# 9.5 Queue Semantics

Queues MUST define:

* capacity
* overflow policy
* cancellation behavior
* shutdown semantics

---

# 9.6 Stream Concurrency

Streams MUST define:

* producer ownership
* consumer ownership
* flow control
* shutdown propagation

---

# 10. Allowed Dependencies

Allowed:

* structured concurrency primitives
* async-safe synchronization
* lifecycle-bound resources
* supervised workers
* bounded queues

Allowed external patterns:

* Trio-style semantics
* AnyIO-compatible semantics
* structured task groups

---

# 11. Forbidden Behaviors

---

# 11.1 Detached Tasks

Forbidden under all circumstances.

---

# 11.2 Blocking Event Loop

Forbidden under all circumstances.

---

# 11.3 Silent Failure Suppression

Forbidden:

* empty except blocks
* hidden task failures
* ignored cancellations

---

# 11.4 Infinite Retries Without Budget

Forbidden.

Retries MUST define:

* budget
* timeout
* cancellation support

---

# 11.5 Unbounded Queues

Forbidden unless explicitly architecture-approved.

---

# 11.6 Hidden Threads

Forbidden:

* implicit thread spawning
* unmanaged executors

---

# 11.7 Runtime Mutation After Startup

Forbidden unless explicitly documented.

---

# 11.8 Scope Escapes

Forbidden:

* task surviving parent scope
* resource surviving owner scope

---

# 11.9 Async Deadlocks

Architecturally forbidden.

Subsystems MUST avoid:

* circular waits
* nested lock inversion
* dependency cycles

---

# 12. Compliance Requirements

Every subsystem MUST document:

* ownership
* cancellation behavior
* cleanup semantics
* concurrency guarantees
* backpressure policy
* retry policy
* timeout semantics

Any subsystem unable to define these is NOT runtime compliant.

---
