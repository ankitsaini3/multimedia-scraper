# Configuration API Reference

## Concrete Implementation Surfaces

### `ConfigurationBootstrapCoordinator`
Central orchestrator for the configuration lifecycle. Manages state transitions, delegates to the resolver and validator, and produces an immutable runtime configuration snapshot.
- **Lifecycle Flow**: `PRE_BOOTSTRAP` → `RESOLVING` → `VALIDATING` → `FREEZING` → `ACTIVATING` → `ACTIVE`
- **Failure Handling**: Catches exceptions during bootstrap, transitions to `FAILED`, invokes `ConfigBootstrapRollbackManager`, and re-raises the original exception.
- **Immutability Guarantee**: Returns `FrozenRuntimeConfig` which wraps the final DTO and forbids mutation, replacement, or direct environment access post-activation.

### `ValidationPipeline`
Gatekeeper for raw configuration payloads. Enforces strict schema compliance before DTO instantiation.
- Validates against `ALLOWED_FIELDS` (rejects unknown keys with `ConfigurationValidationError`).
- Delegates cross-field consistency checks to `CrossFieldValidator`.
- Invokes `RuntimeConfigDTOFactory.create()` on successful validation.

### `RuntimeConfigDTOFactory`
Static factory that transforms flat, dot-notation payloads into a nested, type-safe DTO graph (`RuntimeConfigDTO` → `LoggingConfigDTO`, `CacheConfigDTO`, `FFmpegConfigDTO`).

### `ConfigResolver` & `merge_sources`
Source aggregation layer. Sorts `ConfigSource` instances by `precedence` (ascending) then `source_name` (lexicographic). Higher precedence sources overwrite lower precedence keys during the merge.

### `EnvironmentConfigSourceProvider`
Concrete adapter that maps specific `MULTIMEDIA_SCRAPER_*` environment variables to configuration keys. Only loads variables present in `ENV_MAPPINGS`; ignores missing env vars silently.

### `ConfigBootstrapRollbackManager`
Recovery handler invoked on bootstrap failure. Forces the coordinator through `ROLLING_BACK` → `TERMINATED` states to ensure no partial configuration leaks into the application runtime.

---

## Protocols

| Protocol | Type | Surface | Contract / Usage |
|----------|------|---------|------------------|
| `ConfigSourceProvider` | `abc.ABC` | `load() -> ConfigSource` | Abstract contract for any configuration source loader (env, file, CLI, secret, etc.). Must return an immutable `ConfigSource`. |
| `CacheConfigProvider` | `typing.Protocol` | `@property cache -> CacheConfigDTO` | Structural DI contract. Any class exposing a `cache` property returning `CacheConfigDTO` satisfies this protocol. |
| `BootstrapStateController` | `typing.Protocol` | `_state: ConfigBootstrapState` | Internal structural contract for the rollback manager. Requires mutable `_state` attribute to transition coordinator out of failed states. |

---

## Data Transfer Objects (DTOs)

All DTOs enforce `frozen=True`, `slots=True`, and `kw_only=True` (unless otherwise noted). Immutability is further guarded where applicable via `MappingProxyType`.

### Base & Infrastructure DTOs
| DTO | Fields | Guarantees |
|-----|--------|------------|
| `ConfigDTO` | *(Base)* | Hashable, deterministic, serialization/transport-safe. Provides `to_dict() -> MappingProxyType[str, Any]`. |
| `ConfigSource` | `source_type: ConfigSourceType`, `source_name: str`, `precedence: int`, `payload: Mapping[str, Any]` | `payload` is automatically wrapped in `MappingProxyType` via `__post_init__`. |
| `ValidationResult` | `valid: bool`, `normalized: Mapping[str, Any]`, `errors: tuple[str, ...]` | `normalized` is enforced as read-only `MappingProxyType`. |

### Domain DTOs
| DTO | Fields | Inherits |
|-----|--------|----------|
| `RuntimeConfigDTO` | `logging: LoggingConfigDTO`, `cache: CacheConfigDTO`, `ffmpeg: FFmpegConfigDTO` | `ConfigDTO` |
| `LoggingConfigDTO` | `level: str`, `json_logs: bool`, `correlation_ids: bool` | `ConfigDTO` |
| `CacheConfigDTO` | `enabled: bool`, `root_directory: str`, `max_size_mb: int` | `ConfigDTO` |
| `FFmpegConfigDTO` | `executable_path: str`, `hwaccel_enabled: bool`, `max_parallel_jobs: int` | `ConfigDTO` |

### Bootstrap & Security DTOs
| DTO | Fields | Purpose |
|-----|--------|---------|
| `FrozenRuntimeConfig` | `config: RuntimeConfigDTO` | Authoritative runtime snapshot. Marks configuration as sealed and activation-complete. |
| `ConfigBootstrapDiagnostics` | `phase: str`, `source_count: int`, `success: bool` | Telemetry/audit record for bootstrap runs. |
| `CacheConfigView` | `config: CacheConfigDTO` | Read-only view adapter for DI exposure. |
| `SecretStr` | `_value: str` | Redacts value on `str()`/`repr()` (`"********"`). Exposes plaintext only via `reveal()`. |

### Enums & Types
- `ConfigBootstrapState`: `PRE_BOOTSTRAP`, `RESOLVING`, `VALIDATING`, `FREEZING`, `ACTIVATING`, `ACTIVE`, `FAILED`, `ROLLING_BACK`, `TERMINATED`
- `ConfigSourceType`: `DEFAULT`, `FILE`, `ENVIRONMENT`, `SECRET`, `CLI`

---

## Signatures & Contracts

### Bootstrap & Orchestration
```python
class ConfigurationBootstrapCoordinator:
    def __init__(
        self,
        *,
        resolver: ConfigResolver,
        validator: ValidationPipeline,
        providers: Sequence[ConfigSourceProvider],
    ) -> None

    @property
    def state(self) -> ConfigBootstrapState

    def bootstrap(self) -> FrozenRuntimeConfig
```
**Contract**: `resolver` and `validator` must not be `None`. Providers are frozen to `tuple` on init. Raises original exception after rollback on failure.

### Resolution & Merging
```python
class ConfigResolver:
    def resolve(self, sources: Iterable[ConfigSource]) -> dict[str, object]

def merge_sources(sources: Iterable[ConfigSource]) -> dict[str, Any]
```
**Contract**: Sorting key: `(source.precedence, source.source_name)`. Later sources in sorted order overwrite earlier ones.

### Validation Pipeline
```python
class ValidationPipeline:
    def validate(self, payload: Mapping[str, Any]) -> RuntimeConfigDTO

    def _validate_unknown_fields(self, payload: Mapping[str, Any]) -> None
    def _validate_cross_fields(self, payload: Mapping[str, Any]) -> None

class CrossFieldValidator:
    def validate(self, payload: Mapping[str, object]) -> ValidationResult

class SafePathValidator:
    def validate(self, value: str) -> ValidationResult

class StringValidator:
    def validate(self, value: Any) -> ValidationResult

class IntegerRangeValidator:
    def __init__(self, *, minimum: int, maximum: int) -> None
    def validate(self, value: Any) -> ValidationResult

class SecretValidator:
    def validate(self, value: object) -> ValidationResult
```
**Contract**: `_validate_unknown_fields` raises `ConfigurationValidationError` if `set(payload) - ALLOWED_FIELDS` is non-empty. `SafePathValidator` rejects paths containing `".."` after resolution. `CrossFieldValidator` enforces `cache.root_directory` when `cache.enabled` is true.

### Factory & Serialization
```python
class RuntimeConfigDTOFactory:
    @staticmethod
    def create(payload: Mapping[str, Any]) -> RuntimeConfigDTO

def serialize_runtime_config(config: RuntimeConfigDTO) -> str
```
**Contract**: `create` expects dot-notation keys (e.g., `"logging.level"`). `serialize_runtime_config` outputs compact JSON with `sort_keys=True`, `separators=(",", ":")`.

### Dependency Injection & Utilities
```python
class ConfigBootstrapRollbackManager:
    def rollback(self, coordinator: BootstrapStateController) -> None

def resolve_secret(value: str) -> SecretStr

def register_configuration(
    services: ServiceCollection,
    config: FrozenRuntimeConfig,
) -> None
```
**Contract**: `register_configuration` binds `FrozenRuntimeConfig` as an application-scoped singleton in the DI container. `rollback` mutates coordinator state via structural typing.

---

## Constants & Policies

| Constant | Type | Value / Description |
|----------|------|---------------------|
| `IMMUTABLE_CONFIG_POLICY` | `frozenset[str]` | `{"runtime", "cache", "ffmpeg", "plugins", "network"}` |
| `ALLOWED_FIELDS` | `frozenset[str]` | Flat dot-notation keys permitted in payloads: `logging.*`, `cache.*`, `ffmpeg.*` |
| `ENV_MAPPINGS` | `dict[str, tuple[str, Callable[[str], Any]]]` | Maps `MULTIMEDIA_SCRAPER_LOG_LEVEL` → `("logging.level", str)`, `MULTIMEDIA_SCRAPER_CACHE_DIR` → `("cache.root_directory", str)` |
