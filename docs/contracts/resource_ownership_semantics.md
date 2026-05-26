# Resource Ownership Semantics Contract

Status: Frozen Contract  
Criticality: SYSTEM-CRITICAL  
Depends On:
- runtime_invariants.md
- lifecycle_semantics.md
- concurrency_semantics.md
- di_semantics.md
- failure_semantics.md

Applies To:
- async runtime
- subprocess management
- FFmpeg integration
- browser automation
- streaming
- downloads
- network systems
- caches
- temporary storage
- worker systems
- plugins
- event pipelines

This document defines the canonical ownership semantics for all runtime-managed resources.

Violation of this contract is considered:
- runtime corruption
- lifecycle corruption
- concurrency corruption
- cleanup failure
- production-critical architectural failure

---

# 1. Purpose

This contract freezes the ownership model for all resources inside the multimedia_scraper architecture.

The ownership model exists to guarantee:
- deterministic cleanup
- leak prevention
- cancellation correctness
- lifecycle safety
- fault isolation
- async correctness
- bounded resource usage
- runtime observability

This document defines:
- who owns resources
- who may use resources
- who may transfer resources
- who must cleanup resources
- how ownership interacts with cancellation
- how ownership interacts with async execution

If another subsystem contract conflicts with this document:
THIS DOCUMENT WINS.

---

# 2. Ownership

Primary Owner:
- core/runtime

Secondary Owners:
- infrastructure maintainers
- orchestration maintainers

Consumers:
- all runtime-managed components

Only runtime-managed scopes may own managed resources.

---

# 3. Resource Model

A resource is any entity requiring:
- acquisition
- lifecycle tracking
- cleanup
- supervision
- bounded usage

Resources include but are not limited to:
- sockets
- HTTP sessions
- browser instances
- Playwright contexts
- FFmpeg subprocesses
- pipes
- file handles
- temporary files
- memory buffers
- semaphores
- locks
- queues
- worker threads
- executor pools
- streams
- database connections
- plugin sandboxes

Pure immutable values are NOT resources.

---

# 4. Core Ownership Invariants

These invariants MUST ALWAYS hold.

---

# 4.1 Every Resource Has Exactly One Owner

Every managed resource MUST have:
- exactly one owner scope
- exactly one cleanup authority
- exactly one lifecycle boundary

Shared ownership is forbidden.

Allowed:
- shared access
- borrowed access
- read-only access

Forbidden:
- ambiguous ownership
- multi-owner cleanup responsibility
- hidden ownership transfer

---

# 4.2 Resource Lifetime Is Scope-Bound

Resources MUST NOT outlive their owner scope.

If a scope terminates:
- all owned resources MUST terminate
- all child resources MUST cleanup
- all subordinate handles MUST invalidate

Forbidden:
- leaked subprocesses
- leaked sockets
- leaked temporary files
- leaked worker tasks

---

# 4.3 Ownership Must Be Explicit

Ownership MUST be explicit in:
- constructors
- APIs
- factories
- runtime registries

Forbidden:
- implicit ownership
- undocumented transfer
- hidden global resources

---

# 4.4 Cleanup Responsibility Is Non-Transferable

The owning scope remains responsible for cleanup unless:
- ownership is explicitly transferred
- transfer succeeds atomically

Cleanup responsibility MUST NEVER become ambiguous.

---

# 4.5 Ownership Transfer Must Be Explicit

Ownership transfer MUST define:
- old owner
- new owner
- transfer boundary
- cleanup responsibility
- failure rollback semantics

Implicit transfer is forbidden.

---

# 4.6 Borrowed Access Does Not Transfer Ownership

Borrowed resources:
- MUST NOT cleanup underlying resource
- MUST NOT outlive owner scope
- MUST NOT retain resource indefinitely

Borrowers MAY:
- temporarily use resources
- read resource state
- perform scoped operations

Borrowers MUST NOT:
- assume ownership
- mutate lifecycle state
- suppress cleanup

---

# 4.7 Cleanup Must Be Deterministic

Every resource MUST define:
- acquisition semantics
- release semantics
- failure cleanup semantics
- cancellation cleanup semantics

Best-effort cleanup alone is insufficient.

---

# 4.8 Resource Graphs Must Be Hierarchical

Ownership MUST form a tree.

Allowed:
- parent scope owns child resources

Forbidden:
- ownership cycles
- cleanup dependency cycles
- circular shutdown graphs

---

# 4.9 Failed Acquisition Must Cleanup Partials

Partial acquisition MUST rollback cleanly.

Example:

```text id="ivrd7o"
Acquire socket
→ acquire subprocess
→ subprocess fails
→ socket cleaned up
````

Partial initialization leaks are forbidden.

---

# 4.10 Resource State Must Be Observable

The runtime MUST expose:

* active resources
* owner scopes
* resource counts
* leaked resource detection
* cleanup failures

Invisible resources are forbidden.

---

# 5. Resource Taxonomy

---

# 5.1 Scope-Owned Resources

Owned directly by runtime scopes.

Examples:

* task-local HTTP sessions
* plugin browser contexts
* stream buffers

Destroyed when scope exits.

---

# 5.2 Application-Owned Resources

Owned by application runtime.

Examples:

* global cache pools
* shared HTTP connector pools
* telemetry pipelines

Destroyed during runtime shutdown.

---

# 5.3 Ephemeral Resources

Short-lived temporary resources.

Examples:

* temporary files
* stream chunks
* transient subprocess pipes

Must remain bounded and cleanup-safe.

---

# 5.4 External Resources

Resources backed by external systems.

Examples:

* sockets
* browser processes
* FFmpeg processes
* OS handles

Must define:

* disconnect semantics
* timeout semantics
* termination semantics

---

# 6. Interface Definitions

---

# 6.1 Managed Resource Interface

Every managed resource MUST define:

```python id="heamq0"
class ManagedResource(Protocol):
    async def acquire(self) -> None: ...
    async def release(self) -> None: ...
    def owner_scope(self) -> ScopeId: ...
    def resource_state(self) -> ResourceState: ...
```

---

# 6.2 Ownership Transfer Interface

Transfer operations MUST define:

```python id="0w5v0x"
class OwnershipTransfer(Protocol):
    async def transfer(
        self,
        new_owner: ScopeId,
    ) -> None: ...
```

---

# 6.3 Resource Registry Interface

The runtime MUST support:

* registration
* leak detection
* cleanup tracking
* ownership inspection

---

# 7. Guarantees

The runtime guarantees:

1. Deterministic cleanup
2. Explicit ownership
3. Scope-bound lifetimes
4. Cleanup ordering correctness
5. Cancellation-safe release
6. Leak detection capability
7. Failure rollback semantics
8. Ownership observability
9. Hierarchical ownership integrity
10. Resource isolation

---

# 8. Invariants

---

# 8.1 Released Resources Are Invalid

After release:

* resource use is invalid
* operations MUST fail deterministically

Zombie resource reuse is forbidden.

---

# 8.2 Cleanup Is Idempotent

Calling release multiple times MUST NOT:

* recreate resources
* corrupt runtime state
* double-free resources

---

# 8.3 Ownership Cannot Be Implicitly Shared

Shared mutable resources MUST define:

* synchronization semantics
* ownership authority
* cleanup authority

---

# 8.4 Resource Acquisition Is Atomic From Caller Perspective

Callers MUST observe either:

* successful acquisition
  OR
* deterministic failure cleanup

Partially exposed resources are forbidden.

---

# 8.5 Resource State Transitions Must Be Valid

Resources MUST obey:

uninitialized
→ acquiring
→ active
→ releasing
→ released

Illegal transitions are forbidden.

---

# 9. Failure Semantics

---

# 9.1 Acquisition Failure

If acquisition fails:

* partial resources MUST cleanup
* ownership MUST rollback
* invalid handles MUST NOT escape

---

# 9.2 Cleanup Failure

Cleanup failures:

* MUST be logged
* MUST remain isolated
* MUST NOT stop remaining cleanup chain

---

# 9.3 Owner Scope Failure

If owner scope fails:

* all owned resources MUST cleanup
* subordinate tasks MUST cancel

---

# 9.4 External Process Failure

External subprocess failures MUST:

* propagate through typed boundaries
* cleanup subordinate handles
* preserve runtime integrity

---

# 9.5 Leak Detection Failure

Leak detection MUST:

* surface observability events
* emit diagnostics
* support debugging visibility

Silent leak suppression is forbidden.

---

# 10. Lifecycle Semantics

---

# 10.1 Resource Lifecycle

Every resource MUST obey:

created
→ acquiring
→ active
→ releasing
→ released

No additional hidden lifecycle phases allowed.

---

# 10.2 Scope Shutdown Ordering

Shutdown ordering MUST obey:

child resources
→ dependent resources
→ parent resources

Reverse-order cleanup is mandatory.

---

# 10.3 Cancellation During Acquisition

Cancellation during acquisition MUST:

* rollback partial acquisition
* cleanup intermediate state
* preserve runtime invariants

---

# 10.4 Cancellation During Release

Release MUST remain cancellation-safe.

Critical cleanup MAY temporarily shield cancellation.

---

# 10.5 Runtime Shutdown

Runtime shutdown MUST:

1. stop resource creation
2. cancel active scopes
3. drain resources
4. release resources deterministically
5. reconcile cleanup failures

---

# 11. Concurrency Semantics

---

# 11.1 Ownership Mutation Requires Synchronization

Ownership transfer MUST be synchronized.

Concurrent ownership mutation is forbidden.

---

# 11.2 Resource Access Must Define Concurrency Rules

Every shared resource MUST explicitly define:

* thread-safe
* async-safe
* single-owner-only
* externally synchronized

Undefined concurrency behavior is forbidden.

---

# 11.3 Resource Cleanup Must Be Race-Safe

Concurrent cleanup attempts MUST:

* remain idempotent
* avoid double release
* preserve runtime integrity

---

# 11.4 Resource Pools Must Be Bounded

Pools MUST define:

* maximum size
* acquisition timeout
* exhaustion policy
* shutdown semantics

Unbounded pools are forbidden.

---

# 11.5 Async Resource Acquisition Must Be Cancellation-Safe

Waiting acquisition MUST:

* support cancellation
* release wait state correctly
* avoid leaked reservations

---

# 12. Allowed Dependencies

Allowed:

* async context managers
* lifecycle-bound pools
* structured cleanup stacks
* runtime-owned registries
* bounded connection pools
* explicit ownership transfer systems

---

# 13. Forbidden Behaviors

---

# 13.1 Hidden Global Resources

Forbidden:

* module-level connection pools
* hidden browser instances
* implicit shared subprocesses

---

# 13.2 Detached Resource Lifetimes

Forbidden:

* subprocess surviving owner scope
* socket surviving runtime shutdown
* temporary file without cleanup owner

---

# 13.3 Implicit Ownership Transfer

Forbidden under all circumstances.

---

# 13.4 Cleanup Suppression

Forbidden:

* swallowing cleanup failure
* abandoning cleanup paths
* relying only on GC finalizers

---

# 13.5 Resource Resurrection

Released resources MUST NEVER become active again.

---

# 13.6 Cross-Scope Resource Mutation

Forbidden unless explicitly synchronized and documented.

---

# 13.7 Unbounded Resource Growth

Forbidden:

* unbounded queues
* unbounded subprocess creation
* unbounded browser contexts
* unbounded memory buffering

---

# 13.8 Blocking Cleanup On Event Loop

Forbidden:

* synchronous blocking cleanup
* blocking subprocess waits
* blocking filesystem cleanup

Blocking cleanup MUST use async-safe execution.

---

# 14. Compliance Requirements

Every subsystem using resources MUST document:

* ownership model
* cleanup authority
* transfer semantics
* concurrency guarantees
* cancellation behavior
* pooling policy
* leak prevention strategy

Any subsystem unable to define these is NOT resource compliant.

---
