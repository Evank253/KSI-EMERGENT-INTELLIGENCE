from dataclasses import dataclass

from ..governance.execution_boundary import GovernedExecutionBoundary
from ..governance.gateway import Authorization, Disposition
from ..governance.escalation import Escalation, escalate


@dataclass(frozen=True)
class ExecutionResult:
    disposition: Disposition
    action: str
    output: object | None = None
    escalation: Escalation | None = None


class ExecutionLoop:
    """Plans and sequences steps; does not own or invoke a tool executor.

    Every consequential execution is delegated to GovernedExecutionBoundary,
    which is the sole owner of the underlying executor reference.
    """

    def __init__(self, boundary: GovernedExecutionBoundary):
        self.boundary = boundary

    def execute(self, step, authorization: Authorization | None = None) -> ExecutionResult:
        decision, output = self.boundary.execute_step(step, authorization)
        disposition = decision.disposition

        if disposition is Disposition.ALLOW:
            return ExecutionResult(
                disposition=disposition,
                action=step.action,
                output=output,
            )
        if disposition is Disposition.ESCALATE:
            return ExecutionResult(
                disposition=disposition,
                action=step.action,
                escalation=escalate(
                    reason="Action is outside current authorization boundary.",
                    action=step.action,
                ),
            )
        return ExecutionResult(disposition=disposition, action=step.action)
