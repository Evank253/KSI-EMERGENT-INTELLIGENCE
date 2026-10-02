"""Explicit qualification state machine."""

from __future__ import annotations
from enum import Enum

class QualificationState(str, Enum):
    OBSERVED = "OBSERVED"
    CANDIDATE = "CANDIDATE"
    CONTROLLED = "CONTROLLED"
    REPLICATED = "REPLICATED"
    REVIEWED = "REVIEWED"
    QUALIFIED = "QUALIFIED"
    REJECTED = "REJECTED"
    EVIDENCE_INSUFFICIENT = "EVIDENCE_INSUFFICIENT"

_ALLOWED = {
    QualificationState.OBSERVED: {QualificationState.CANDIDATE, QualificationState.REJECTED, QualificationState.EVIDENCE_INSUFFICIENT},
    QualificationState.CANDIDATE: {QualificationState.CONTROLLED, QualificationState.REJECTED, QualificationState.EVIDENCE_INSUFFICIENT},
    QualificationState.CONTROLLED: {QualificationState.REPLICATED, QualificationState.REJECTED, QualificationState.EVIDENCE_INSUFFICIENT},
    QualificationState.REPLICATED: {QualificationState.REVIEWED, QualificationState.REJECTED, QualificationState.EVIDENCE_INSUFFICIENT},
    QualificationState.REVIEWED: {QualificationState.QUALIFIED, QualificationState.REJECTED, QualificationState.EVIDENCE_INSUFFICIENT},
    QualificationState.QUALIFIED: set(),
    QualificationState.REJECTED: set(),
    QualificationState.EVIDENCE_INSUFFICIENT: {QualificationState.OBSERVED},
}

class InvalidTransition(ValueError):
    pass

class QualificationMachine:
    def __init__(self, state: QualificationState = QualificationState.OBSERVED):
        self.state = state

    def transition(self, target: QualificationState) -> QualificationState:
        if target not in _ALLOWED[self.state]:
            raise InvalidTransition(f"{self.state.value} -> {target.value} is not permitted")
        self.state = target
        return self.state
