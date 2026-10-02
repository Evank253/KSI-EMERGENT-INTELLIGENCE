from enum import Enum

from .capability_context import CapabilityContext


class CapabilityDisposition(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


def _normalize(value: str | None) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip().upper()


def authorize_capability(
    required_capability: str | None,
    context: CapabilityContext | None,
) -> CapabilityDisposition:
    """Authorize only an explicit capability grant in the execution context."""
    capability = _normalize(required_capability)
    if not capability or context is None:
        return CapabilityDisposition.DENY

    grants = {_normalize(grant) for grant in context.capability_grants}
    grants.discard("")
    return (
        CapabilityDisposition.ALLOW
        if capability in grants
        else CapabilityDisposition.DENY
    )
