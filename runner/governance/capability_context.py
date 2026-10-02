from dataclasses import dataclass


@dataclass(frozen=True)
class CapabilityContext:
    """Execution context containing only explicit capability grants."""

    actor: str
    capability_grants: frozenset[str] = frozenset()
    run_id: str | None = None
