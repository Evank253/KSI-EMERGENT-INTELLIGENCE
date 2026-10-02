from dataclasses import dataclass
from typing import Callable

from .objective import Objective
from .planner import Planner
from .execution_loop import ExecutionLoop
from ..capability.awareness import CapabilityAwareness
from ..governance.capability_context import CapabilityContext
from ..governance.execution_boundary import GovernedExecutionBoundary


@dataclass
class RunnerState:
    objective_id: str
    status: str
    capability_snapshot: dict


class KSIRunner:
    """Governed cognitive execution kernel.

    The underlying tool executor and explicit capability context are injected
    into GovernedExecutionBoundary. ExecutionLoop owns neither.
    """

    def __init__(
        self,
        tool_executor: Callable[[str, str], object],
        capability_context: CapabilityContext | None = None,
    ):
        self.capabilities = CapabilityAwareness()
        self.planner = Planner()
        self.capability_context = capability_context or CapabilityContext("KSI_RUNNER")
        self.boundary = GovernedExecutionBoundary(tool_executor, self.capability_context)
        self.execution = ExecutionLoop(self.boundary)

    def run(self, objective: Objective, authorization=None):
        steps = self.planner.plan(objective)
        results = [
            self.execution.execute(step, authorization=authorization)
            for step in steps
        ]
        return {
            "objective": objective,
            "plan": steps,
            "results": results,
            "capability_awareness": self.capabilities.snapshot(),
            "qualification": "NOT_QUALIFIED",
            "authority_granted": False,
        }
