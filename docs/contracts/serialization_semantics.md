# DTO / Serialization Semantics Contract

Status: Frozen Contract  
Criticality: HIGH  
Depends On:
- runtime_invariants.md
- di_semantics.md
- failure_semantics.md
- plugin_semantics.md
- event_semantics.md
- concurrency_semantics.md

Applies To:
- API boundaries
- plugin interfaces
- event systems
- workers
- IPC
- persistence layers
- cache systems
- stream metadata
- orchestration messages
- external adapters
- queue payloads
- browser automation messages

This document defines the canonical DTO and serialization semantics for the multimedia_scraper architecture.

Violation of this contract is considered:
- boundary corruption
- compatibility corruption
- runtime integrity violation
- plugin isolation violation
- persistence corruption

---

# 1. Purpose

This contract freezes:
- DTO design rules
- serialization boundaries
- transport semantics
- compatibility guarantees
- schema evolution rules
- validation semantics
- immutability requirements

The DTO system exists to guarantee:
- stable boundaries
- deterministic serialization
- runtime isolation
- transport safety
- plugin compatibility
- persistence safety
- cache correctness
- replayability
- observability consistency

If another contract conflicts with this document:
THIS DOCUMENT WINS.

---

# 2. Ownership

Primary Owner:
- contracts/
- core/runtime

Secondary Owners:
- API maintainers
- plugin maintainers
- event system maintainers

Consumers:
- all boundary-crossing systems

Business/domain entities MUST NOT define transport semantics directly.

---

# 3. Architectural Model

The system uses:
- explicit DTOs
- immutable transport models
- schema-versioned serialization
- validation-first deserialization
- transport-safe primitives
- deterministic encoding

The system does NOT use:
- implicit ORM object transport
- arbitrary object pickling
- hidden runtime object serialization
- mutable transport objects
- reflection-dependent schemas

---

# 4. Core Definitions

---

# 4.1 DTO

A DTO (Data Transfer Object) is:
- immutable
- transport-safe
- serialization-safe
- validation-defined
- boundary-oriented

DTOs exist ONLY for:
- boundary crossing
- persistence
- IPC
- events
- external APIs
- plugin communication

DTOs are NOT domain entities.

---

# 4.2 Serialization

Serialization is the transformation of DTOs into:
- JSON
- msgpack
- protobuf-like binary formats
- transport-safe primitives

Serialization MUST be:
- deterministic
- version-aware
- schema-validatable

---

# 4.3 Boundary

A boundary is any transition between:
- processes
- plugins
- threads
- runtimes
- persistence systems
- external APIs
- event systems
- cache systems

All boundaries MUST use DTO semantics.

---

# 5. Core DTO Invariants

These invariants MUST ALWAYS hold.

---

# 5.1 DTOs Must Be Immutable

DTOs MUST be immutable after creation.

Forbidden:
- mutable DTO state
- in-place mutation
- transport-side mutation

Allowed:
- creation of new DTO instances

---

# 5.2 DTOs Must Be Pure Data

DTOs MUST contain only:
- transport-safe primitives
- nested DTOs
- enums
- validated collections

Forbidden:
- open sockets
- runtime services
- locks
- file handles
- subprocesses
- callbacks
- coroutine objects
- event loops
- executors

---

# 5.3 DTOs Must Not Contain Behavior

DTOs MUST NOT contain:
- business logic
- runtime logic
- side effects
- lifecycle management

Allowed:
- validation helpers
- serialization helpers
- schema metadata

---

# 5.4 Serialization Must Be Deterministic

Equivalent DTOs MUST serialize identically.

Serialization MUST NOT depend on:
- memory layout
- hash randomization
- object identity
- import order

---

# 5.5 DTO Schemas Must Be Explicit

All DTOs MUST define:
- schema structure
- field types
- optionality
- defaults
- version semantics

Implicit schema inference is forbidden.

---

# 5.6 Boundary Crossing Requires Serialization

Cross-boundary object sharing is forbidden.

Objects MUST NOT cross boundaries via:
- shared references
- runtime pointers
- mutable shared objects

All boundaries MUST use:
DTO → serialization → transport → deserialization

---

# 5.7 DTO Validation Is Mandatory

Incoming DTOs MUST validate before use.

Validation MUST occur:
- before runtime integration
- before persistence
- before plugin execution
- before event publication

Unvalidated DTO usage is forbidden.

---

# 5.8 Deserialization Must Be Safe

Deserialization MUST:
- reject malformed payloads
- reject schema violations
- reject unsupported versions
- avoid arbitrary code execution

Unsafe deserialization is forbidden.

---

# 5.9 DTO Versioning Must Be Explicit

Versioned DTOs MUST define:
- schema version
- compatibility guarantees
- migration semantics

Hidden schema evolution is forbidden.

---

# 5.10 DTOs Must Be Transport Stable

DTO serialization MUST remain stable across:
- process boundaries
- runtime restarts
- plugin boundaries
- replay operations
- cache retrieval

---

# 6. DTO Taxonomy

---

# 6.1 Command DTOs

Represent requested actions.

Examples:
- DownloadRequestDTO
- StreamStartCommandDTO

Properties:
- intent-oriented
- validation-heavy
- immutable

---

# 6.2 Event DTOs

Represent facts that occurred.

Examples:
- DownloadCompletedEventDTO
- StreamFailedEventDTO

Properties:
- append-only semantics
- replay-safe
- timestamped

---

# 6.3 State DTOs

Represent snapshots of state.

Examples:
- JobStatusDTO
- CacheEntryDTO

Properties:
- serializable snapshots
- transport-safe
- deterministic

---

# 6.4 Persistence DTOs

Represent storage-safe models.

Properties:
- migration-aware
- versioned
- backward-compatible where required

---

# 6.5 External API DTOs

Represent external transport contracts.

Properties:
- adapter-isolated
- boundary-stable
- compatibility-controlled

---

# 7. Interface Definitions

---

# 7.1 DTO Interface

All DTOs MUST support:

```python id="5n0nd7"
class DTO(Protocol):
    def schema_version(self) -> int: ...
    def serialize(self) -> bytes | dict: ...
````

---

# 7.2 Serialization Interface

Serializers MUST define:

```python id="8ngh95"
class Serializer(Protocol):
    def serialize(self, dto: DTO) -> bytes: ...
    def deserialize(self, payload: bytes) -> DTO: ...
```

---

# 7.3 Validation Interface

Validators MUST define:

```python id="v8k07x"
class Validator(Protocol):
    def validate(self, payload: object) -> ValidationResult: ...
```

---

# 8. Guarantees

The system guarantees:

1. Immutable DTOs
2. Deterministic serialization
3. Safe deserialization
4. Explicit schemas
5. Stable transport semantics
6. Boundary isolation
7. Version-aware compatibility
8. Replay-safe event payloads
9. Validation-first processing
10. Runtime-safe transport

---

# 9. Serialization Semantics

---

# 9.1 Canonical Encoding

Serialization MUST define canonical encoding behavior.

Examples:

* deterministic key ordering
* explicit timezone semantics
* explicit binary encoding

---

# 9.2 Primitive Compatibility

Allowed primitives:

* string
* integer
* float
* boolean
* null
* bytes
* enums
* lists
* maps
* nested DTOs
* timestamps

Forbidden:

* runtime object references
* arbitrary Python objects
* lambdas/functions

---

# 9.3 Time Semantics

Time fields MUST define:

* timezone semantics
* serialization precision
* monotonic vs wall-clock meaning

Implicit local time is forbidden.

---

# 9.4 Binary Payload Semantics

Binary payloads MUST define:

* encoding
* size bounds
* transport compatibility

---

# 9.5 Large Payload Rules

Large payloads SHOULD use:

* chunking
* streaming references
* external storage references

Massive inline payloads are discouraged.

---

# 10. Failure Semantics

---

# 10.1 Validation Failure

Validation failures MUST:

* fail deterministically
* produce typed errors
* prevent runtime integration

---

# 10.2 Unsupported Version Failure

Unsupported versions MUST:

* reject safely
* preserve runtime integrity
* emit compatibility diagnostics

---

# 10.3 Serialization Failure

Serialization failures MUST:

* remain isolated
* preserve source DTO integrity
* avoid partial transport corruption

---

# 10.4 Deserialization Failure

Malformed payloads MUST NOT:

* corrupt runtime state
* partially initialize DTOs
* execute arbitrary code

---

# 10.5 Schema Migration Failure

Migration failures MUST:

* fail safely
* preserve source payload
* avoid silent data mutation

---

# 11. Lifecycle Semantics

---

# 11.1 DTO Lifecycle

DTOs MUST obey:

created
→ validated
→ serialized
→ transported
→ deserialized
→ consumed
→ discarded

DTOs are NOT long-lived runtime entities.

---

# 11.2 Event DTO Lifecycle

Event DTOs MAY additionally support:

* persistence
* replay
* archival

Replay semantics MUST remain deterministic.

---

# 11.3 Persistence DTO Lifecycle

Persistence DTOs MUST define:

* migration path
* retention semantics
* compatibility guarantees

---

# 12. Concurrency Semantics

---

# 12.1 DTOs Are Concurrency-Safe By Immutability

Immutable DTOs MAY be safely shared across:

* async tasks
* threads
* workers

Mutable DTO sharing is forbidden.

---

# 12.2 Serializer Concurrency Rules

Serializers MUST document:

* thread safety
* async safety
* streaming support

---

# 12.3 Concurrent Schema Mutation Is Forbidden

Schemas MUST remain immutable at runtime.

Dynamic schema mutation is forbidden.

---

# 12.4 Transport Ordering

Event transports MUST define:

* ordering guarantees
* deduplication semantics
* replay semantics

Undefined ordering is forbidden.

---

# 13. Compatibility Semantics

---

# 13.1 Backward Compatibility

DTO compatibility rules MUST be explicit.

Allowed:

* additive optional fields

Forbidden without migration:

* field meaning mutation
* destructive schema removal
* incompatible type mutation

---

# 13.2 Forward Compatibility

Unknown fields SHOULD:

* preserve safely
  OR
* reject deterministically

Behavior MUST be explicit.

---

# 13.3 Plugin Compatibility

Plugin DTO contracts MUST remain:

* versioned
* isolated
* transport-stable

Plugins MUST NOT:

* mutate shared schemas
* bypass validation

---

# 14. Allowed Dependencies

Allowed:

* pydantic-like validation
* dataclass-like immutable models
* msgpack/json serializers
* explicit schema systems
* typed transport contracts

Allowed architectural patterns:

* schema-first DTOs
* versioned event contracts
* append-only event evolution

---

# 15. Forbidden Behaviors

---

# 15.1 Arbitrary Object Serialization

Forbidden:

* pickle
* dill
* runtime object graph dumping

---

# 15.2 Mutable DTOs

Forbidden under all circumstances.

---

# 15.3 DTOs With Runtime Handles

Forbidden:

* sockets
* tasks
* subprocess handles
* browser handles
* runtime services

---

# 15.4 Hidden Schema Evolution

Forbidden:

* silent field mutation
* undocumented compatibility breaks

---

# 15.5 Unsafe Deserialization

Forbidden:

* code-executing deserializers
* reflection-based arbitrary construction

---

# 15.6 Shared Mutable Cross-Boundary State

Forbidden under all circumstances.

---

# 15.7 Transporting Domain Entities Directly

Forbidden:

* ORM models across boundaries
* runtime entities across IPC
* live service objects in events

---

# 15.8 Runtime Mutation During Serialization

Serialization MUST NOT mutate DTO state.

---

# 16. Compliance Requirements

Every subsystem using DTOs MUST document:

* schema definitions
* serialization format
* compatibility guarantees
* validation rules
* migration semantics
* replay semantics
* ordering semantics

Subsystems unable to define these are NOT DTO compliant.

---

# 17. Frozen Architecture Rules

The following rules are frozen:

1. DTOs are immutable
2. DTOs are pure data only
3. DTOs cannot contain runtime behavior
4. Serialization must be deterministic
5. Schemas must be explicit
6. Validation is mandatory
7. Deserialization must be safe
8. Boundary crossing requires serialization
9. DTO versioning must be explicit
10. Runtime object transport is forbidden
11. Arbitrary object serialization is forbidden
12. Shared mutable cross-boundary state is forbidden
13. Schema mutation at runtime is forbidden
14. DTO lifecycle is boundary-oriented
15. Transport semantics must remain stable

Any violation requires formal architectural revision.

```

