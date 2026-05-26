# `docs/contracts/state_persistence_semantics.md`

# State & Persistence Semantics

---

# 1. Purpose

This document defines the authoritative state and persistence model of the runtime.

It specifies:

* runtime state ownership
* persistence boundaries
* transactional semantics
* cache semantics
* snapshot semantics
* durable vs ephemeral state
* replay guarantees
* consistency contracts
* recovery behavior
* resumability guarantees
* persistence lifecycle rules

This contract governs all stateful behavior across:

* runtime services
* downloads
* streams
* playback pipelines
* metadata stores
* cache systems
* resumable operations
* event replay systems
* plugins
* providers
* workers

This document is the canonical persistence governance layer.

---

# 2. Architectural Goals

The persistence model exists to guarantee:

```text id="k2x4mb"
1. Deterministic state ownership
2. Recoverable runtime behavior
3. Predictable durability guarantees
4. Replay-safe execution
5. Transactional integrity
6. Explicit lifecycle semantics
7. Cache correctness
8. Crash-safe recovery
9. Consistency across runtime boundaries
10. Long-term maintainability
```

---

# 3. Core Principles

---

## 3.1 Explicit State Ownership

Every mutable state MUST have exactly one authoritative owner.

Shared mutable ownership is forbidden.

---

## 3.2 State Is Never Implicit

State transitions MUST occur through explicit contracts.

Implicit mutation is forbidden.

---

## 3.3 Durability Must Be Declared

Every state category MUST define:

```text id="xaw7e6"
durable
ephemeral
reconstructable
derived
```

Undefined persistence semantics are forbidden.

---

## 3.4 Persistence Is Layer-Bound

Persistence responsibilities MUST remain inside explicitly designated layers.

Persistence leakage across architectural boundaries is forbidden.

---

# 4. State Taxonomy

---

# 4.1 Durable State

Durable state survives:

```text id="q3v8ow"
process restart
runtime crash
machine reboot
worker restart
```

Examples:

```text id="n9ptlz"
download metadata
media metadata
user configuration
persistent cache indexes
resume checkpoints
database records
plugin registry state
```

---

# 4.2 Ephemeral State

Ephemeral state exists only during active execution.

Examples:

```text id="67mnvz"
in-flight streams
active tasks
runtime locks
worker queues
playback buffers
temporary allocations
session-local caches
```

Ephemeral state MUST NOT be relied upon for recovery.

---

# 4.3 Derived State

Derived state is reconstructable from authoritative state.

Examples:

```text id="j0uvro"
computed indexes
thumbnails
search indexes
media manifests
cache projections
analytics summaries
```

Derived state MAY be discarded safely.

---

# 4.4 Snapshot State

Snapshot state represents point-in-time runtime capture.

Examples:

```text id="h6q5an"
download progress snapshots
pipeline checkpoints
replay checkpoints
stream recovery snapshots
```

Snapshots support resumability and recovery.

---

# 5. State Ownership Model

---

# 5.1 Single Authoritative Owner

Each state domain MUST define exactly one authoritative owner.

Examples:

| State Domain    | Owner                 |
| --------------- | --------------------- |
| download state  | download service      |
| playback state  | playback orchestrator |
| metadata state  | metadata repository   |
| cache index     | cache service         |
| plugin registry | plugin manager        |

---

# 5.2 Read vs Write Ownership

Multiple readers are allowed.

Write authority MUST remain singular.

---

# 5.3 Ownership Transfer

Ownership transfer MUST be:

```text id="p9jdrq"
explicit
transactional
observable
recoverable
```

Implicit ownership transfer is forbidden.

---

# 6. Persistence Boundaries

---

# 6.1 Persistence Is Infrastructure Responsibility

Persistence logic belongs to infrastructure layers only.

Business/domain layers MUST NOT directly manage storage engines.

---

# 6.2 Storage Abstraction

All persistence MUST occur through contracts.

Examples:

```text id="f6g0ji"
Repository interfaces
Persistence adapters
Snapshot stores
Cache interfaces
Checkpoint stores
```

---

# 6.3 Persistence Leakage Is Forbidden

Upper layers MUST NOT depend on:

```text id="t0p9hy"
SQLite details
filesystem layout
serialization engines
database drivers
```

---

# 7. Transactional Semantics

---

# 7.1 Atomicity Requirement

Transactional operations MUST be atomic.

Partial persistence is forbidden unless explicitly declared.

---

# 7.2 Transaction Boundaries

Each transactional operation MUST define:

```text id="uxv3ja"
begin point
commit point
rollback semantics
failure semantics
recovery semantics
```

---

# 7.3 Multi-Resource Transactions

Distributed transactions SHOULD be avoided.

Preferred approach:

```text id="0xjlwm"
eventual consistency
idempotent recovery
compensating actions
```

---

# 7.4 Transaction Isolation

Concurrent writes MUST preserve consistency.

Allowed strategies:

```text id="9a8oqt"
optimistic concurrency
version checks
serialized mutation
MVCC
```

---

# 7.5 Rollback Guarantees

Failed transactions MUST leave persistence in a valid state.

No corrupted partial state allowed.

---

# 8. Versioning Semantics

---

# 8.1 Persistent State MUST Be Versioned

Durable schemas MUST define explicit versions.

---

# 8.2 Migration Ownership

Only infrastructure migration systems MAY mutate schema versions.

Plugins MUST NEVER directly migrate global state.

---

# 8.3 Forward Compatibility

Persistence formats SHOULD support:

```text id="v7fj8i"
schema evolution
optional fields
safe extension
backward compatibility
```

---

# 9. Cache Semantics

---

# 9.1 Cache Is Non-Authoritative

Caches MUST NEVER become authoritative state.

Authoritative state MUST exist elsewhere.

---

# 9.2 Cache Types

Supported cache categories:

| Type            | Purpose                 |
| --------------- | ----------------------- |
| memory cache    | fast ephemeral access   |
| disk cache      | reusable artifacts      |
| metadata cache  | provider metadata reuse |
| streaming cache | playback buffering      |
| derived cache   | computed artifacts      |

---

# 9.3 Cache Invalidation

Every cache MUST define invalidation rules.

Undefined invalidation semantics are forbidden.

---

# 9.4 Allowed Invalidation Strategies

Examples:

```text id="0l0vmp"
TTL expiration
version invalidation
content hash invalidation
manual invalidation
dependency invalidation
event-driven invalidation
```

---

# 9.5 Cache Consistency

Caches MAY be eventually consistent.

But stale behavior MUST be bounded and documented.

---

# 9.6 Cache Corruption

Cache corruption MUST NEVER corrupt authoritative state.

Cache recovery MUST support safe eviction.

---

# 10. Snapshot Semantics

---

# 10.1 Snapshot Purpose

Snapshots exist to support:

```text id="f4qv3w"
recovery
resumability
replay
crash restoration
checkpointing
```

---

# 10.2 Snapshot Requirements

Snapshots MUST be:

```text id="j0h9yq"
immutable
versioned
recoverable
consistent
```

---

# 10.3 Snapshot Scope

Snapshots MAY include:

```text id="knv8mr"
download offsets
stream positions
pipeline checkpoints
task progress
worker state
```

---

# 10.4 Snapshot Consistency

Snapshots MUST represent internally consistent state.

Half-written snapshots are forbidden.

---

# 10.5 Snapshot Restoration

Restoration MUST validate:

```text id="y9q3fw"
schema version
resource existence
integrity
compatibility
```

Invalid snapshots MUST fail safely.

---

# 11. Resumability Semantics

---

# 11.1 Resumable Operations Must Define Checkpoints

Resumable systems MUST define checkpoint frequency and durability.

Examples:

```text id="0j56nb"
download chunk checkpoints
stream offsets
transcoding progress
playlist iteration progress
```

---

# 11.2 Resume Guarantees

Resume behavior MUST define:

```text id="yy4ptx"
exact resume
best-effort resume
restart-required semantics
```

---

# 11.3 Replay Safety

Recovery operations MUST be idempotent.

Repeated recovery MUST NOT corrupt state.

---

# 12. Stream State Semantics

---

# 12.1 Stream State Is Primarily Ephemeral

Most stream state is non-durable.

Examples:

```text id="nvwr1r"
buffer queues
decoder state
playback synchronization
```

---

# 12.2 Persisted Stream State

Persisted stream state MAY include:

```text id="3zv9ja"
playback position
manifest checkpoints
adaptive bitrate decisions
session recovery metadata
```

---

# 12.3 Stream Recovery

Recovery MUST tolerate:

```text id="m1c0yq"
network interruption
provider disconnects
partial buffer loss
process restart
```

---

# 13. Metadata Persistence Semantics

---

# 13.1 Metadata Ownership

Metadata repositories are authoritative owners of media metadata.

---

# 13.2 Metadata Freshness

Metadata MUST define freshness policies.

Examples:

```text id="l3vm0k"
immutable metadata
TTL refresh
provider revalidation
conditional refresh
```

---

# 13.3 Metadata Provenance

Persisted metadata SHOULD track:

```text id="13k4mp"
provider source
fetch timestamp
schema version
validation state
```

---

# 14. Replay System Semantics

---

# 14.1 Replayability Requirements

Replay systems MUST define:

```text id="gmh3t4"
ordering guarantees
deduplication semantics
idempotency guarantees
retention policies
```

---

# 14.2 Event Replay

Replayable events MUST be:

```text id="tql9ns"
immutable
ordered
versioned
timestamped
```

---

# 14.3 Deterministic Recovery

Replay recovery SHOULD produce deterministic state reconstruction.

---

# 15. Consistency Semantics

---

# 15.1 Strong Consistency

Required for:

```text id="zxy7v1"
critical metadata
capability state
transactional ownership
checkpoint commits
```

---

# 15.2 Eventual Consistency

Allowed for:

```text id="dql4xe"
search indexes
thumbnails
derived analytics
non-critical caches
```

---

# 15.3 Consistency Boundaries

Consistency guarantees MUST be explicitly documented per subsystem.

Undefined consistency behavior is forbidden.

---

# 16. Serialization Semantics

---

# 16.1 Stable Serialization

Durable state MUST use stable serialization formats.

Examples:

```text id="7yx4xv"
JSON
msgpack
protobuf
SQLite
```

---

# 16.2 Unsafe Serialization Forbidden

Unsafe runtime-bound serialization formats are forbidden.

Examples:

```text id="f09nkr"
pickle
raw object dumps
runtime memory snapshots
```

Unless isolated and explicitly approved.

---

# 16.3 Schema Evolution

Serialized state SHOULD tolerate:

```text id="l7prtx"
field addition
optional fields
version migration
partial decoding
```

---

# 17. Failure Semantics

---

# 17.1 Persistence Failures Must Be Explicit

Persistence failures MUST produce typed errors.

Examples:

```python id="m3b7to"
PersistenceError
SnapshotCorruptionError
TransactionConflictError
ResumeStateInvalidError
```

---

# 17.2 Crash Consistency

Crash recovery MUST preserve:

```text id="brg5mu"
structural integrity
authoritative ownership
transaction validity
```

---

# 17.3 Partial Recovery

Subsystems MAY partially recover if explicitly documented.

Undefined partial recovery is forbidden.

---

# 18. Durable vs Ephemeral Resource Rules

| Resource                        | Persistence Type |
| ------------------------------- | ---------------- |
| active playback buffer          | ephemeral        |
| media metadata                  | durable          |
| thumbnails                      | derived          |
| download checkpoints            | durable          |
| runtime queues                  | ephemeral        |
| cache entries                   | derived          |
| plugin registry                 | durable          |
| stream synchronization          | ephemeral        |
| replay logs                     | durable          |
| temporary transcoding artifacts | ephemeral        |

---

# 19. Observability & Auditability

---

# 19.1 Persistence Operations SHOULD Emit Events

Examples:

```text id="4ok4o6"
transaction commit
rollback
snapshot creation
cache eviction
recovery start
recovery completion
```

---

# 19.2 Recovery Visibility

Recovery systems MUST expose:

```text id="d9f2js"
recovery source
recovery timestamp
recovery success/failure
reconstructed state scope
```

---

# 20. Future Compatibility Requirements

This persistence model MUST remain compatible with:

```text id="kgj8cn"
distributed runtimes
cloud object storage
multi-process execution
remote workers
event sourcing
containerized execution
WASM environments
multi-tenant persistence
```

---

# 21. Architectural Invariants

---

## Ownership

```text id="7v5u6v"
Every mutable state has exactly one authoritative owner.
```

---

## Durability

```text id="1tqz1u"
Persistence guarantees must be explicit.
```

---

## Transactions

```text id="qz9fpu"
Transactional operations are atomic.
```

---

## Cache

```text id="9o0a6y"
Caches are never authoritative state.
```

---

## Snapshots

```text id="r0dfz2"
Snapshots are immutable and recoverable.
```

---

## Recovery

```text id="9r6wdf"
Recovery operations are idempotent.
```

---

## Isolation

```text id="2dpr4l"
Persistence responsibilities remain infrastructure-bound.
```

---

## Serialization

```text id="hy3fqa"
Durable serialization formats must remain stable and versioned.
```

---

## Replay

```text id="jw5f0f"
Replay systems preserve ordering and immutability.
```

---

## Determinism

```text id="7kk0l8"
Persistence semantics must remain deterministic.
```
