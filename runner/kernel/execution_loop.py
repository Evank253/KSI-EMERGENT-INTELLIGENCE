from dataclasses import dataclass
from ..governance.gateway import ActionRequest, Authorization, Disposition, authorize
from ..governance.escalation import Escalation, escalate


@dataclass(frozen=True)
class ExecutionResult:
    disposition: Disposition
    action: str
    output: object | None = None
    escalation: Escalation | None = None


class ExecutionLoop:
    def __init__(self, tool_executor):
        self.tool_executor = tool_executor

    def execute(self, step, authorization: Authorization | None = None) -> ExecutionResult:
        request = ActionRequest(
            action=step.action,
            target=step.target,
            consequential=step.consequential,
            required_scope=step.required_scope,
            requested_by="KSI_RUNNER",
        )
        disposition = authorize(request, authorization)
        if disposition is Disposition.ALLOW:
            output = self.tool_executor(step.action, step.target)
            return ExecutionResult(disposition=disposition, action=step.action, output=output)
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
