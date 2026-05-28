from __future__ import annotations


def test_multiple_runtime_contexts_are_isolated(
    runtime_context,
):
    runtime_a = runtime_context

    runtime_b = runtime_context.__class__(
        runtime_id=runtime_context.runtime_id,
        config=runtime_context.config,
        observability=runtime_context.observability,
        diagnostics=runtime_context.diagnostics,
        metadata=runtime_context.metadata,
        cancellation_scope=runtime_context.cancellation_scope.create_child(
            name="runtime-b",
        ),
        supervisor=runtime_context.supervisor,
        event_bus=runtime_context.event_bus,
        registry=runtime_context.registry.__class__(),
    )

    runtime_a.registry.register(str, "runtime-a")

    assert runtime_b.registry.try_resolve(str) is None
