from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet


class Disposition(str, Enum):
    ALLOW = "ALLOW_WITHIN_SCOPE"
    REJECT = "REJECT"
    ESCALATE = "ESCALATE_GOVERNANCE"


@dataclass(frozen=True)
class Authorization:
    actor: str
    scope: str
    approved: bool = True
    human_authorized: bool = True
    capability_grants: frozenset[str] = frozenset()


@dataclass(frozen=True)
class ActionRequest:
    action: str
    target: str
    consequential: bool
    required_scope: str
    requested_by: str
    required_capability: str


PROTECTED_TARGETS: FrozenSet[str] = frozenset({
    "constitution",
    "authority_model",
    "authorization_scopes",
    "evidence_history",
    "governance",
})


def authorize(request: ActionRequest, authorization: Authorization | None) -> Disposition:
    if request.target in PROTECTED_TARGETS:
        if authorization is None or not authorization.human_authorized:
            return Disposition.ESCALATE
        if authorization.scope != request.required_scope:
            return Disposition.REJECT
        if not authorization.approved:
            return Disposition.REJECT
        return Disposition.ESCALATE

    if request.consequential:
        if authorization is None:
            return Disposition.ESCALATE
        if not authorization.approved:
            return Disposition.REJECT
        if authorization.scope != request.required_scope:
            return Disposition.REJECT

    return Disposition.ALLOW
