from dataclasses import dataclass
from .gateway import Authorization


@dataclass(frozen=True)
class AuthorizationRecord:
    authorization: Authorization
    reason: str
    evidence_reference: str | None = None


def require_human_authorization(
    actor: str,
    scope: str,
    reason: str,
    *,
    approved: bool = True,
    evidence_reference: str | None = None,
) -> AuthorizationRecord:
    return AuthorizationRecord(
        authorization=Authorization(
            actor=actor,
            scope=scope,
            approved=approved,
            human_authorized=True,
        ),
        reason=reason,
        evidence_reference=evidence_reference,
    )
