from dataclasses import dataclass


@dataclass(frozen=True)
class Escalation:
    reason: str
    action: str
    required_authority: str = "HUMAN"


def escalate(reason: str, action: str) -> Escalation:
    return Escalation(reason=reason, action=action)
