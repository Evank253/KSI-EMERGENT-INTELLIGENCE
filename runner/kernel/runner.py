from dataclasses import dataclass
from typing import Callable

from .objective import Objective
from .planner import Planner
from .execution_loop import ExecutionLoop
from ..capability.awareness import CapabilityAwareness
from ..governance.execution_boundary import GovernedExecutionBoundary


@dataclass
class RunnerState:
    objective_id: str
    status: str
    capability_snapshot: dict


class KSIRunner:
    """Governed cognitive execution kernel.

    The underlying tool executor is injected only into GovernedExecutionBoundary.
    ExecutionLoop and KSIRunner do not hold a direct callable reference to it.
    """

    def __init__(self, tool_executor: Callable[[str, str], object]):
        self.capabilities = CapabilityAwareness()
        self.planner = Planner()
        self.boundary = GovernedExecutionBoundary(tool_executor)
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
