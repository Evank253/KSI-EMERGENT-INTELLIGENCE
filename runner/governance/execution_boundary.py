from dataclasses import dataclass
from typing import Callable

from .gateway import ActionRequest, Authorization, Disposition, authorize


class GovernanceBoundaryError(RuntimeError):
    pass


@dataclass(frozen=True)
class ExecutionDecision:
    disposition: Disposition
    request: ActionRequest


class GovernedExecutionBoundary:
    """Mandatory execution boundary for runner tools.

    Tools receive execution only after the governance gateway authorizes the
    exact ActionRequest. Callers cannot supply a pre-approved boolean or bypass
    the gateway through this interface.
    """

    def __init__(self, tool_executor: Callable[[str, str], object]):
        self._tool_executor = tool_executor

    def execute(
        self,
        request: ActionRequest,
        authorization: Authorization | None = None,
    ) -> tuple[ExecutionDecision, object | None]:
        disposition = authorize(request, authorization)
        decision = ExecutionDecision(disposition=disposition, request=request)

        if disposition is not Disposition.ALLOW:
            return decision, None

        return decision, self._tool_executor(request.action, request.target)

    def execute_step(self, step, authorization: Authorization | None = None):
        request = ActionRequest(
            action=step.action,
            target=step.target,
            consequential=step.consequential,
            required_scope=step.required_scope,
            requested_by="KSI_RUNNER",
        )
        return self.execute(request, authorization)


def require_governed_execution(decision: ExecutionDecision) -> None:
    if decision.disposition is not Disposition.ALLOW:
        raise GovernanceBoundaryError(
            f"Execution denied by governance boundary: {decision.disposition.value}"
        )
