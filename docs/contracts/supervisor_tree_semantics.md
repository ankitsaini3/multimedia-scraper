# Supervisor Tree Semantics Contract

Status: Frozen Contract  
Criticality: SYSTEM-CRITICAL  
Depends On:
- runtime_invariants.md
- lifecycle_semantics.md
- concurrency_semantics.md
- failure_semantics.md
- resource_ownership_semantics.md
- event_semantics.md

Applies To:
- async runtime
- orchestration
- worker systems
- task execution
- streaming pipelines
- plugin execution
- subprocess supervision
- browser automation
- background services
- retry systems
- event consumers

This document defines the canonical supervision model for the multimedia_scraper runtime.

The supervisor tree is the core fault-containment and lifecycle-control mechanism of the system.

Violation of this contract is considered:
- runtime corruption
- structured concurrency violation
- lifecycle corruption
- async model corruption
- fault containment failure

---

# 1. Purpose

This contract freezes:
- supervision topology
- task ownership semantics
- failure propagation rules
- restart semantics
- cancellation propagation
- shutdown ordering
- runtime fault isolation

The supervisor system exists to guarantee:
- structured concurrency
- deterministic shutdown
- bounded failure propagation
- task ownership correctness
- cancellation integrity
- runtime observability
- restart safety

If another contract conflicts with this document:
THIS DOCUMENT WINS.

---

# 2. Ownership

Primary Owner:
- core/runtime

Secondary Owners:
- orchestration maintainers
- worker infrastructure maintainers

Consumers:
- all async runtime subsystems

No subsystem may bypass supervision semantics.

---

# 3. Supervisor Model

The runtime uses a strict hierarchical supervision tree.

Properties:
- tree-shaped ownership
- parent-child supervision
- deterministic lifecycle
- bounded failure propagation
- cancellation propagation
- structured concurrency enforcement

The runtime is NOT:
- actor-system-style unbounded supervision
- detached task execution
- peer-owned task graphs
- cyclic ownership

---

# 4. Core Supervision Invariants

These invariants MUST ALWAYS hold.

---

# 4.1 Every Task Has Exactly One Supervisor

Every runtime task MUST:
- belong to exactly one supervisor
- have exactly one lifecycle owner
- have exactly one cancellation chain

Shared supervision is forbidden.

---

# 4.2 Supervision Topology Must Be a Tree

The supervision graph MUST remain acyclic.

Allowed:
- parent → child ownership

Forbidden:
- cycles
- peer ownership
- shared child ownership
- orphan nodes

---

# 4.3 Parent Owns Child Lifecycle

Supervisors own:
- child startup
- child cancellation
- child shutdown
- child restart policy
- child cleanup reconciliation

Children MUST NOT outlive parents.

---

# 4.4 Child Failure Is Observable

All child failures MUST:
- surface to supervisor
- preserve traceback context
- remain observable
- enter supervision reconciliation

Silent child failure is forbidden.

---

# 4.5 Orphan Tasks Are Forbidden

Every active task MUST remain reachable from:
- runtime root
through
- supervision ownership chain

Detached tasks are forbidden.

---

# 4.6 Supervision State Must Be Observable

The runtime MUST expose:
- supervisor hierarchy
- child task state
- restart counts
- cancellation chains
- failed tasks
- unhealthy supervisors

Invisible supervision state is forbidden.

---

# 4.7 Supervisor Shutdown Is Deterministic

Supervisor shutdown MUST:
1. stop accepting new children
2. cancel/drain children
3. reconcile failures
4. cleanup owned resources
5. terminate deterministically

---

# 4.8 Failure Containment Must Hold

Child failure MUST NOT corrupt:
- unrelated branches
- sibling supervisors
- runtime root
- supervision graph integrity

---

# 4.9 Restart Semantics Must Be Explicit

Every supervised child MUST define:
- restartable/non-restartable
- retry budget
- backoff policy
- fatal escalation policy

Implicit restart behavior is forbidden.

---

# 4.10 Cancellation Must Propagate Downward

Cancellation MUST propagate:
parent
→ child
→ descendants

Upward cancellation propagation is policy-controlled.

---

# 5. Supervision Taxonomy

---

# 5.1 Runtime Root Supervisor

Top-level runtime authority.

Owns:
- application lifecycle
- global shutdown
- root scopes
- infrastructure supervisors

There MUST be exactly one runtime root supervisor.

---

# 5.2 Infrastructure Supervisors

Manage:
- network services
- worker pools
- cache systems
- telemetry
- browser pools

Typically long-lived.

---

# 5.3 Task Supervisors

Manage:
- downloads
- extraction jobs
- stream pipelines
- orchestration jobs

Usually short-lived.

---

# 5.4 Plugin Supervisors

Own plugin execution domains.

Must isolate:
- failures
- cancellation
- resource ownership
- event consumers

Plugin supervisors MUST NOT corrupt runtime-global supervision state.

---

# 5.5 Resource Supervisors

Own:
- subprocess groups
- FFmpeg processes
- browser instances
- external transports

Must reconcile external-process failures safely.

---

# 6. Interface Definitions

---

# 6.1 Supervisor Interface

Every supervisor MUST define:

```python id="3s41md"
class Supervisor(Protocol):
    async def start(self) -> None: ...
    async def shutdown(self) -> None: ...
    async def spawn(self, task: TaskSpec) -> TaskHandle: ...
    async def cancel_children(self) -> None: ...
    def children(self) -> list[TaskHandle]: ...
    def health_state(self) -> HealthState: ...
````

---

# 6.2 Child Task Interface

Every supervised task MUST define:

```python id="f1lcrz"
class SupervisedTask(Protocol):
    async def run(self) -> None: ...
    async def cleanup(self) -> None: ...
    def restart_policy(self) -> RestartPolicy: ...
```

---

# 6.3 Restart Policy Interface

Restart policies MUST define:

```python id="wlnj26"
class RestartPolicy(Protocol):
    def max_retries(self) -> int: ...
    def backoff_policy(self) -> BackoffPolicy: ...
    def escalation_policy(self) -> EscalationPolicy: ...
```

---

# 7. Guarantees

The runtime guarantees:

1. Structured task ownership
2. Deterministic shutdown
3. Observable failure propagation
4. Cancellation propagation
5. Fault isolation
6. Bounded restart behavior
7. No orphan tasks
8. Lifecycle-bound supervision
9. Deterministic cleanup
10. Supervision graph integrity

---

# 8. Failure Semantics

---

# 8.1 Child Failure

Child failure MUST:

* surface to parent
* enter supervision reconciliation
* preserve failure visibility

Supervisor MAY:

* restart child
* escalate failure
* terminate subtree
* isolate failure

---

# 8.2 Fatal Supervisor Failure

Supervisor corruption is considered fatal if:

* ownership graph breaks
* orphan tasks appear
* cancellation chain corrupts
* restart storm occurs
* cleanup reconciliation fails catastrophically

Fatal supervisor corruption MAY require runtime shutdown.

---

# 8.3 Restart Storm Protection

Supervisors MUST protect against:

* infinite restart loops
* rapid crash cycling
* cascading retries

Mandatory controls:

* retry budgets
* exponential backoff
* escalation thresholds

---

# 8.4 Cleanup Failure

Cleanup failures:

* MUST remain observable
* MUST NOT corrupt sibling cleanup
* MUST NOT detach surviving tasks

---

# 8.5 Cancellation Failure

Tasks ignoring cancellation are considered unhealthy.

Repeated cancellation refusal MAY escalate to:

* forced termination
* subtree teardown
* runtime degradation state

---

# 9. Lifecycle Semantics

---

# 9.1 Supervisor Lifecycle

Every supervisor MUST obey:

created
→ initializing
→ active
→ draining
→ cancelling
→ cleanup
→ terminated

Skipping phases is forbidden.

---

# 9.2 Child Startup Ordering

Children MUST NOT become active before:

* parent initialization completes
* dependencies become healthy

---

# 9.3 Child Shutdown Ordering

Shutdown ordering MUST obey:

children
→ parent cleanup
→ parent termination

Reverse ordering is mandatory.

---

# 9.4 Restart Lifecycle

Restart MUST obey:

failure
→ reconciliation
→ cleanup
→ restart decision
→ backoff
→ reinitialization

Restart without cleanup is forbidden.

---

# 9.5 Supervisor Exit Requirements

A supervisor MUST NOT terminate until:

* children reconcile
* cleanup completes
* owned resources release
* cancellation propagation completes

---

# 10. Concurrency Semantics

---

# 10.1 Supervisor State Mutation Must Be Serialized

Supervisor state mutation MUST be synchronized.

Concurrent mutation of:

* child registry
* restart counters
* lifecycle state
* shutdown state

without synchronization is forbidden.

---

# 10.2 Child Registry Consistency

The child registry MUST remain internally consistent.

Tasks MUST NOT:

* disappear silently
* duplicate entries
* remain after termination

---

# 10.3 Concurrent Shutdown Semantics

Concurrent shutdown attempts MUST:

* remain idempotent
* preserve ordering
* avoid duplicate cleanup

---

# 10.4 Restart Concurrency

Restart operations MUST avoid:

* duplicate restart races
* overlapping cleanup
* simultaneous activation

---

# 10.5 Supervisor Isolation

Supervisors MUST NOT:

* mutate sibling state
* directly manage sibling children
* bypass parent ownership

---

# 11. Restart Policies

---

# 11.1 Permanent Tasks

Critical infrastructure tasks.

Failure MAY:

* escalate immediately
* terminate runtime
* enter degraded mode

Examples:

* telemetry backbone
* core event dispatcher
* runtime scheduler

---

# 11.2 Transient Tasks

Restart only on abnormal failure.

Examples:

* downloads
* extraction jobs
* stream workers

---

# 11.3 Temporary Tasks

Never restarted.

Examples:

* one-shot orchestration jobs
* cleanup tasks

---

# 12. Allowed Dependencies

Allowed:

* structured task groups
* AnyIO-compatible supervision
* lifecycle-bound worker pools
* explicit restart policies
* bounded retry systems

Allowed architectural patterns:

* Erlang-inspired supervision semantics
* Trio nursery semantics
* structured concurrency models

---

# 13. Forbidden Behaviors

---

# 13.1 Detached Tasks

Forbidden under all circumstances.

---

# 13.2 Supervisor Cycles

Forbidden under all circumstances.

---

# 13.3 Infinite Restart Loops

Forbidden.

---

# 13.4 Hidden Failure Suppression

Forbidden:

* swallowed child exceptions
* invisible restart failures
* silent task death

---

# 13.5 Child Escape

Forbidden:

* child surviving supervisor
* resource surviving subtree termination

---

# 13.6 Unbounded Child Creation

Forbidden.

Supervisors MUST define:

* concurrency limits
* queue limits
* spawn limits

---

# 13.7 Cross-Branch Supervision

Forbidden:

* sibling supervisor ownership
* peer cancellation control
* cross-tree mutation

---

# 13.8 Runtime Mutation Without Synchronization

Forbidden:

* unsynchronized child registry mutation
* concurrent restart mutation races

---

# 14. Compliance Requirements

Every subsystem using supervised execution MUST document:

* supervisor ownership
* restart policy
* cancellation behavior
* failure escalation policy
* cleanup semantics
* concurrency limits
* resource ownership model

Subsystems unable to define these are NOT supervision compliant.

---

# 15. Frozen Architecture Rules

The following rules are frozen:

1. Every task has exactly one supervisor
2. Supervision topology is a tree
3. Parent owns child lifecycle
4. Child failures must be observable
5. Orphan tasks are forbidden
6. Cancellation propagates downward
7. Shutdown is deterministic
8. Restart semantics must be explicit
9. Restart storms must be bounded
10. Supervisor state mutation must be synchronized
11. Child tasks cannot outlive parents
12. Cleanup before restart is mandatory
13. Supervision state must be observable
14. Cross-branch supervision is forbidden
15. Detached execution is forbidden

Any violation requires formal architectural revision.

```
