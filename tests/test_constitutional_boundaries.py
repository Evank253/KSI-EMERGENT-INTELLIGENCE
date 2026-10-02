"""Adversarial constitutional tests for the experimental plane."""
from dataclasses import dataclass

CONSTITUTION_ID = "KSH-CONSTITUTION-001"


@dataclass(frozen=True)
class EmergenceDisposition:
    outcome: str
    authority_granted: bool
    governance_required: bool


def qualify_emergence(reproduced: bool, requests_authority: bool) -> EmergenceDisposition:
    if requests_authority:
        return EmergenceDisposition("GOVERNANCE_ESCALATION", False, True)
    if reproduced:
        return EmergenceDisposition("QUALIFIED_CAPABILITY", False, False)
    return EmergenceDisposition("EVIDENCE_INSUFFICIENT", False, False)


def test_constitution_identity():
    assert CONSTITUTION_ID == "KSH-CONSTITUTION-001"


def test_emergence_never_grants_authority():
    d = qualify_emergence(reproduced=True, requests_authority=False)
    assert d.outcome == "QUALIFIED_CAPABILITY"
    assert d.authority_granted is False


def test_emergent_authority_request_escalates():
    d = qualify_emergence(reproduced=True, requests_authority=True)
    assert d.outcome == "GOVERNANCE_ESCALATION"
    assert d.authority_granted is False
    assert d.governance_required is True


def test_unreproduced_emergence_is_not_qualified():
    d = qualify_emergence(reproduced=False, requests_authority=False)
    assert d.outcome == "EVIDENCE_INSUFFICIENT"
    assert d.authority_granted is False
