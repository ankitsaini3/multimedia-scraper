# Observability API Reference

## Concrete Implementation Surfaces

### Bootstrap & Lifecycle Coordination
| Surface | Type | Responsibility | Architectural Guarantees |
|---------|------|----------------|--------------------------|
| `BootstrapObservabilityController` | Class | Central runtime coordinator for observability activation, degraded fallback, early-event replay, and deterministic shutdown. | Single authority for activation/degraded transitions. Async-safe `initialize()`, `emit()`, `shutdown()`. Tracks `_dropped_events` and `degraded` state. |
| `EarlyBootstrapLogger` | Class | Emergency telemetry emitter used before full sink/pipeline activation. | Avoids background scheduling, worker startup, and runtime dependencies. Appends directly to `EarlyBootstrapBuffer`. |
| `DegradedObservabilityLogger` | Class | Fallback logger invoked when sinks fail or pipelines collapse. | Routes degraded events exclusively to `ConsoleTelemetrySink`. Guarantees runtime survival and emergency visibility. |
| `EarlyBootstrapBuffer` | Class | Bounded pre-runtime telemetry queue (`deque[LogEventDTO]`). | Fixed capacity (default `256`). Deterministic replay ordering. Zero detached execution. |
| `StartupDiagnosticsRegistry` | Class | Append-only registry for bootstrap phase tracking. | Immutable snapshots, deterministic phase ordering, explicit `phase_started`/`completed`/`failed` state transitions. |

### Sinks, Queues & Routing
| Surface | Type | Responsibility | Architectural Guarantees |
|---------|------|----------------|--------------------------|
| `BoundedTelemetryQueue` | Class | Async-safe bounded queue with explicit overflow policies. | Cancellation-safe, observable state (`statistics()`, `wait_until_empty()`). Supports `DROP_OLDEST`, `DROP_NEWEST`, `BLOCK`, `REJECT`. |
| `BaseTelemetrySink` | Class | Abstract base for async telemetry sinks. | Encapsulates worker loop (`_run_worker`), bounded buffering, health tracking, and deterministic shutdown. Isolates infrastructure failures. |
| `CompositeTelemetrySink` | Class | Fanout coordinator for multiple sinks. | Strict sink isolation. Sets `degraded=True` if any downstream sink fails. Never raises from fanout execution. |
| `ConsoleTelemetrySink` | Class | Human-readable stdout sink. | Non-blocking emits via `asyncio.to_thread`. Uses `ConsoleTelemetryFormatter`. |
| `FileTelemetrySink` | Class | Append-only JSON file sink. | Auto-creates parent dirs on `start()`. Blocks IO in thread pool. Strict append semantics. |
| `JsonTelemetrySink` | Class | Machine-readable stdout sink. | Uses `JsonTelemetryFormatter`. Isolated blocking writes. |

### Security, Redaction & Sanitization
| Surface | Type | Responsibility | Architectural Guarantees |
|---------|------|----------------|--------------------------|
| `create_secure_log_event()` | Factory | Canonical immutable `LogEventDTO` builder with auto-redaction. | Sanitizes messages, fields, and exception strings. Guarantees transport/serialization safety. |
| `create_plugin_safe_event()` | Factory | Plugin-isolated telemetry event creator. | Applies `PluginTelemetryPolicy`, strips `PLUGIN_RESTRICTED_FIELDS`, optionally sanitizes exception messages. |
| `automatically_redact_fields()` | Pipeline | Recursive field sanitization combining structural redaction + secret filtering. | Transport-safe output. Deterministic replacement semantics. |
| `filter_secrets()` | Utility | Regex-based secret stripping from raw strings. | Stable `REDACTION_TOKEN` replacement. Covers bearer tokens, API keys, passwords, secrets, authorization headers. |
| `redact_fields()` | Utility | Key-based field masking/dropping against `SENSITIVE_FIELD_NAMES`. | Supports `RedactionPolicy.MASK` (→ `"****"`) or `RedactionPolicy.DROP`. |
| `format_exception()` | Utility | Produces `ExceptionSnapshot` from `BaseException`. | Traverses `__cause__`/`__context__` chain. Applies `filter_secrets` to message. Captures depth & qualified name. |
| `iter_exception_chain()` | Generator | Deterministic exception chain traversal. | Prioritizes `__cause__`, falls back to `__context__`. Yields full causal lineage. |

### Context, Lineage & Internal Utilities
| Surface | Type | Responsibility | Architectural Guarantees |
|---------|------|----------------|--------------------------|
| `bind_telemetry_context()` | ContextManager | Task-local `ContextVar` binding with deterministic reset. | Async-safe isolation. Guaranteed restoration on exit. |
| `child_telemetry_context()` | ContextManager | Creates immutable child lineage for supervised tasks/retries. | Requires active parent. Preserves `trace_id`, propagates `causation_id`. |
| `create_root_telemetry_context()` | Factory | Initializes root telemetry context. | Generates fresh `trace_id`, `span_id`, `correlation_id`. Sets `supervisor_depth=0`. |
| `create_child_telemetry_context()` | Factory | Extends parent context immutably. | Increments `supervisor_depth`, wires `parent_span_id` → `span_id`, preserves `runtime_scope_id`. |
| `require_telemetry_context()` | Guard | Enforces mandatory correlation at ownership boundaries. | Raises `CorrelationPropagationError` if context is `None`. |
| `utc_now()` / `monotonic_time_ns()` | Clocks | Wall-clock vs monotonic time separation. | Timezone-aware UTC for timestamps. Strict monotonic ordering for durations/timeouts. |
| `task_lineage_path()` / `trace_id()` / `span_id()` / `correlation_id()` / `supervisor_id()` | Extractors | Read-only lineage accessors. | Deterministic path formatting (`root/leaf/depth:N`). |

### Formatters & Serialization
| Surface | Type | Responsibility | Architectural Guarantees |
|---------|------|----------------|--------------------------|
| `ConsoleTelemetryFormatter` | Formatter | Human-readable log rendering. | `[iso] [SEVERITY] [subsystem] [operation] message`. UTF-8 bytes output. |
| `JsonTelemetryFormatter` | Formatter | Deterministic JSON rendering. | Delegates to `serialize_log_event()`. Compact, sorted keys. |
| `serialize_log_event()` | Serializer | Canonical JSON serialization for `LogEventDTO`. | Sorted keys, compact separators, stable enum/datetime encoding. Raises `TelemetrySerializationError` on failure. |
| `validate_structured_value()` | Validator | Recursive transport-safety validation for `StructuredValue`. | Enforces string keys in mappings, primitive/tuple recursion. Raises `TelemetryValidationError`. |

---

## Protocols

| Protocol | Surface | Contract / Usage |
|----------|---------|------------------|
| `TelemetryContextProvider` | `get_context() -> TelemetryContextDTO \| None` | Structural contract for reading task-local context. |
| `TelemetryContextBinder` | `bind(context: TelemetryContextDTO) -> None` | Structural contract for immutable context attachment. |
| `StructuredEventEmitter` | `async emit(event: LogEventDTO) -> None` | Runtime-owned emission. Must remain bounded, async-safe, cancellation-safe, supervision-safe. |
| `StructuredEventPublisher` | `async publish(event: LogEventDTO) -> None` | Infrastructure-independent publication boundary. |
| `RuntimeLogger` | `async emit()`, `async log()`, `async trace/debug/info/warn/error/fatal()` | Rich structured logging contract. NOT a global singleton. Lifecycle/task-aware, bounded, async-safe. |
| `StructuredTelemetryEvent` | `schema_version: int`, `serialize() -> bytes` | Canonical event contract. Deterministic serialization. |
| `ReplayableTelemetryEvent` | Inherits `StructuredTelemetryEvent`, adds `event_id: str`, `occurred_at_unix_ns: int` | Replay-safe lineage guarantees. |
| `StructuredEventFilter` | `should_emit(event: LogEventDTO) -> bool` | Deterministic filtering. No event mutation. Preserves runtime isolation. |
| `StructuredEventFormatter` | `format(event: LogEventDTO) -> bytes` | Deterministic transport formatting. Preserves causality & correlation metadata. |
| `StructuredFieldRedactor` | `redact_fields(fields: Mapping[str, StructuredValue]) -> Mapping[str, StructuredValue]` | Field-level redaction contract. |
| `StructuredEventRedactor` | `redact_event(event: LogEventDTO) -> LogEventDTO` | Immutable event redaction. Avoids partial mutation. |
| `TelemetryRouter` | `async route(event: LogEventDTO) -> None` | Infrastructure-isolated routing. Preserves ordering, bounded, no mutation. |
| `LogEventSerializer` | `serialize(event: LogEventDTO) -> bytes` | Byte-level serialization contract. |
| `TelemetrySink` | `async start/emit/flush/shutdown()`, `is_healthy() -> bool` | Infrastructure isolation boundary. Bounded, failure-isolated, deterministic shutdown. |
| `TelemetryPipeline` | `async enqueue/drain()`, `queue_depth()`, `capacity()` | Bounded processing behavior with explicit overflow/shutdown semantics. |
| `LifecycleManagedTelemetryComponent` | `async initialize/start/drain/flush/shutdown()`, `lifecycle_state() -> ObservabilityLifecycleState` | Bootstrap + shutdown semantics contract. |
| `TelemetryContextBinder` | `bind(context: TelemetryContextDTO) -> None` | Runtime-owned context attachment. |
| `BootstrapStateController` | (Internal Protocol) | Structural typing for state mutation during rollback. |

---

## Data Transfer Objects (DTOs) & Type Aliases

All DTOs enforce `frozen=True`, `slots=True`, and `kw_only=True` unless explicitly noted. Immutability and serialization safety are strict architectural requirements.

### Core Telemetry DTOs
| DTO | Fields | Guarantees |
|-----|--------|------------|
| `LogEventDTO` | `timestamp_utc: datetime`, `monotonic_ns: int`, `severity: LogSeverity`, `event_category: EventCategory`, `subsystem: str`, `operation: str`, `message: str`, `correlation: CorrelationMetadataDTO`, `fields: Mapping[str, StructuredValue]`, `exception_type/exception_message: str \| None`, `schema_version: int = 1` | Canonical immutable telemetry record. Deterministic, replay/transport-safe. |
| `TelemetryContextDTO` | `correlation: CorrelationMetadataDTO`, `subsystem: str`, `operation: str` | Task-local context. Never contains runtime services, mutable state, or live handles. |
| `CorrelationMetadataDTO` | `correlation_id: str`, `causation_id: str \| None`, `runtime_scope_id: str`, `trace: OperationTraceDTO`, `supervision: SupervisionLineageDTO` | Cross-task/retry/plugin lineage propagation. Immutable, serialization/replay-safe. |
| `OperationTraceDTO` | `trace_id: str`, `span_id: str`, `parent_span_id: str \| None`, `operation_id: str`, `operation_name: str`, `operation_version: int = 1`, `started_at_utc: datetime` | Request/retry lineage & trace hierarchy. |
| `SupervisionLineageDTO` | `runtime_id: str`, `root_supervisor_id: str`, `supervisor_id: str`, `parent_supervisor_id: str \| None`, `supervisor_depth: int`, `task_id: str \| None = None` | Supervision ownership ancestry. Runtime-boundary-safe. |

### Infrastructure & Diagnostics DTOs
| DTO | Fields | Purpose |
|-----|--------|---------|
| `BootstrapPhaseDiagnostic` | `phase: str`, `started_at_utc: datetime`, `completed_at_utc: datetime \| None`, `success: bool`, `failure_type/failure_message: str \| None` | Immutable startup phase snapshot. |
| `ObservabilityBootstrapSnapshot` | `state: ObservabilityBootstrapState`, `degraded_mode: bool`, `healthy_sinks: int`, `unhealthy_sinks: int`, `dropped_events: int` | Runtime observability state snapshot. |
| `ExceptionSnapshot` | `exception_type: str`, `message: str`, `module: str`, `qualified_name: str`, `is_retryable: bool`, `causal_chain_depth: int` | Structured, secret-safe exception representation. |
| `FailureCorrelationSnapshot` | `correlation_id/trace_id/span_id/supervisor_id: str`, `task_id/operation/subsystem: str \| None` | Correlated failure lineage for diagnostics. |
| `QueueStatistics` | `capacity: int`, `current_depth: int`, `dropped_events: int`, `rejected_events: int` | Bounded queue telemetry snapshot. |
| `TelemetryHealthSnapshot` | `status: TelemetryHealthStatus`, `queue_depth: int`, `dropped_events: int`, `last_failure_unix_ns: int \| None` | Infrastructure health state. |
| `PluginTelemetryPolicy` | `allow_exception_messages/allow_structured_fields/allow_host_paths/allow_environment_metadata: bool` | Capability-safe plugin isolation policy. |

### Type Aliases
| Alias | Definition | Usage |
|-------|------------|-------|
| `StructuredPrimitive` | `str \| int \| float \| bool \| None` | Base transport-safe primitives. |
| `StructuredValue` | `StructuredPrimitive \| tuple[StructuredValue, ...] \| Mapping[str, StructuredValue]` | Recursive field schema for `LogEventDTO.fields`. |
| `StructuredFields` | `Mapping[str, StructuredValue]` | Convenience alias for field mappings. |

---

## Signatures & Method Contracts

### Bootstrap & Lifecycle
```python
class BootstrapObservabilityController:
    async def initialize(self) -> None: ...
    async def emit(self, event: LogEventDTO) -> None: ...
    async def shutdown(self) -> None: ...
    async def _replay_early_events(self) -> None: ...
    # Properties: state, degraded_mode
```
**Contract**: `initialize()` transitions to `INITIALIZING` → `ACTIVE` (or `DEGRADED` on failure). `emit()` routes to `_sink` or `_degraded_logger` if degraded. `shutdown()` drains/flusges, transitions to `SHUTDOWN`.

### Queue & Sink Execution
```python
class BoundedTelemetryQueue:
    async def put(self, event: LogEventDTO) -> None: ...
    async def get(self) -> LogEventDTO: ...
    async def close(self) -> None: ...
    async def drain_iter(self) -> AsyncIterator[LogEventDTO]: ...
    async def wait_until_empty(self) -> None: ...
    def depth(self) -> int: ...
    def statistics(self) -> QueueStatistics: ...
```
**Contract**: `put()` enforces `OverflowPolicy` explicitly. `close()` stops ingestion. `drain_iter()` yields until `RuntimeError` (drained/closed). Thread-safe via `asyncio.Condition`.

```python
class BaseTelemetrySink:
    async def start(self) -> None: ...
    async def emit(self, event: LogEventDTO) -> None: ...
    async def flush(self) -> None: ...
    async def shutdown(self) -> None: ...
    def is_healthy(self) -> bool: ...
    async def _run_worker(self) -> None: ...
    async def _write_event(self, event: LogEventDTO) -> None: ...  # Abstract
```
**Contract**: Worker loop consumes `drain_iter()`. `_write_event` must be overridden. Blocking IO delegated to `asyncio.to_thread`. Health degrades on unhandled worker exception.

### Security & Event Construction
```python
def create_secure_log_event(
    *, context: TelemetryContextDTO, severity: LogSeverity, event_category: EventCategory,
    message: str, fields: Mapping[str, StructuredValue] | None = None, exception: BaseException | None = None,
) -> LogEventDTO: ...

def create_plugin_safe_event(
    *, context: TelemetryContextDTO, severity: LogSeverity, event_category: EventCategory,
    message: str, policy: PluginTelemetryPolicy, fields: Mapping[str, StructuredValue] | None = None,
    exception: BaseException | None = None,
) -> LogEventDTO: ...
```
**Contract**: `create_secure_log_event` applies `automatically_redact_fields()` to message & fields, formats exceptions safely. `create_plugin_safe_event` applies `sanitize_plugin_fields()`, optionally replaces exception with `RuntimeError` if `policy.allow_exception_messages=False`.

### Context & Lineage
```python
@contextmanager
def bind_telemetry_context(context: TelemetryContextDTO) -> Iterator[TelemetryContextDTO]: ...
@contextmanager
def child_telemetry_context(
    *, subsystem: str | None = None, operation: str | None = None,
    supervisor_id: str | None = None, task_id: str | None = None,
) -> Iterator[TelemetryContextDTO]: ...
def require_telemetry_context(*, reason: str) -> TelemetryContextDTO: ...
```
**Contract**: `child_telemetry_context` requires active parent context. Raises `CorrelationPropagationError` otherwise. Lineage is strictly immutable.

### Serialization & Validation
```python
def serialize_log_event(event: LogEventDTO) -> bytes: ...
def _json_default(value: Any) -> Any: ...
def validate_structured_value(value: StructuredValue) -> None: ...
def format_exception(exception: BaseException) -> ExceptionSnapshot: ...
def iter_exception_chain(exception: BaseException) -> Iterator[BaseException]: ...
```
**Contract**: `serialize_log_event` uses `json.dumps(sort_keys=True, separators=(",",":"))`. `_json_default` handles `datetime` → `.isoformat()`, `Enum` → `.value`. `validate_structured_value` recursively rejects non-string mapping keys & unsupported types.

---

## Constants, Enums & Policies

### Enums
| Enum | Values | Purpose |
|------|--------|---------|
| `ObservabilityBootstrapState` | `PRE_BOOTSTRAP`, `EARLY_BOOTSTRAP`, `INITIALIZING`, `ACTIVE`, `DEGRADED`, `DRAINING`, `FLUSHING`, `SHUTDOWN` | Bootstrap lifecycle states. |
| `ObservabilityLifecycleState` | `CREATED`, `INITIALIZED`, `ACTIVE`, `DRAINING`, `FLUSHING`, `SHUTDOWN` | Component-level lifecycle states. |
| `EventCategory` | `RUNTIME`, `LIFECYCLE`, `SUPERVISION`, `CANCELLATION`, `RESOURCE`, `NETWORK`, `PLUGIN`, `SECURITY`, `TELEMETRY`, `FAILURE` | Semantic event taxonomy. |
| `LogSeverity` | `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL` | Canonical severity levels (decoupled from stdlib numeric values). |
| `OverflowPolicy` | `DROP_OLDEST`, `DROP_NEWEST`, `BLOCK`, `REJECT` | Bounded queue overflow semantics. |
| `RedactionPolicy` | `MASK`, `DROP` | Field redaction behavior. |
| `DegradedObservabilityReason` | `SINK_FAILURE`, `QUEUE_PRESSURE`, `SERIALIZATION_FAILURE`, `BOOTSTRAP_FAILURE`, `FLUSH_FAILURE` | Degraded mode causation tracking. |
| `TelemetryHealthStatus` | `HEALTHY`, `DEGRADED`, `UNHEALTHY` | Infrastructure health classification. |

### Constants & Rule Sets
| Constant | Type | Value / Description |
|----------|------|---------------------|
| `ROOT_SUPERVISOR_ID` | `str` | `"runtime-root"` |
| `UNKNOWN_SCOPE_ID` / `UNKNOWN_OPERATION` / `UNKNOWN_SUBSYSTEM` | `str` | `"unknown-scope"` / `"unknown-operation"` / `"unknown-subsystem"` |
| `REDACTION_TOKEN` | `str` | `"[REDACTED]"` |
| `SENSITIVE_FIELD_NAMES` | `frozenset[str]` | Authorization tokens, passwords, secrets, API keys, cookies, sessions, credentials. |
| `PLUGIN_RESTRICTED_FIELDS` | `frozenset[str]` | `host_path`, `filesystem_path`, `environment`, `env`, `process`, `subprocess`, `token`, `secret`, `api_key`. |
| `SECRET_PATTERNS` | `tuple[re.Pattern[str], ...]` | Compiled regexes for bearer tokens, `api_key=`, `token=`, `password=`, `secret=`, `authorization=`. |
| `EarlyBootstrapBuffer.DEFAULT_CAPACITY` | `int` | `256` |

---

## Exception & Error Surfaces
| Exception | Raised By | Condition |
|-----------|-----------|-----------|
| `CorrelationPropagationError` | `child_telemetry_context()`, `require_telemetry_context()` | Attempt to create/access context without active parent or when context is missing. |
| `QueueOverflowError` | `BoundedTelemetryQueue._handle_overflow()` | `OverflowPolicy.REJECT` triggered when queue at capacity. |
| `TelemetrySerializationError` | `serialize_log_event()` | Failure during JSON serialization or unsupported type encoding. |
| `TelemetryValidationError` | `validate_structured_value()` | Non-string mapping keys or unsupported `StructuredValue` types detected. |
| `RuntimeError` | `BoundedTelemetryQueue`, `BaseTelemetrySink` | Queue closed, drained, or unsupported overflow policy. |

