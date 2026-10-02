from dataclasses import dataclass
from typing import Callable

from .capability_context import CapabilityContext
from .capability_gate import CapabilityDisposition, authorize_capability
from .gateway import ActionRequest, Authorization, Disposition, authorize


class GovernanceBoundaryError(RuntimeError):
    pass


@dataclass(frozen=True)
class ExecutionDecision:
    disposition: Disposition
    request: ActionRequest
    capability_disposition: CapabilityDisposition


class GovernedExecutionBoundary:
    """Mandatory capability and governance boundary for runner tools.

    Execution ordering is fixed:
    ActionRequest -> Capability Gate -> Governance Authorization -> Executor.
    The capability gate and governance gateway remain distinct decisions.
    """

    def __init__(
        self,
        tool_executor: Callable[[str, str], object],
        capability_context: CapabilityContext,
    ):
        self._tool_executor = tool_executor
        self.capability_context = capability_context

    def execute(
        self,
        request: ActionRequest,
        authorization: Authorization | None = None,
    ) -> tuple[ExecutionDecision, object | None]:
        capability_disposition = authorize_capability(
            request.required_capability,
            self.capability_context,
        )

        if capability_disposition is not CapabilityDisposition.ALLOW:
            decision = ExecutionDecision(
                disposition=Disposition.REJECT,
                request=request,
                capability_disposition=capability_disposition,
            )
            return decision, None

        disposition = authorize(request, authorization)
        decision = ExecutionDecision(
            disposition=disposition,
            request=request,
            capability_disposition=capability_disposition,
        )

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
            required_capability=step.required_capability,
        )
        return self.execute(request, authorization)


def require_governed_execution(decision: ExecutionDecision) -> None:
    if decision.disposition is not Disposition.ALLOW:
        raise GovernanceBoundaryError(
            f"Execution denied by governance boundary: {decision.disposition.value}"
        )
