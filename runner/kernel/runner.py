from dataclasses import dataclass
from .objective import Objective
from .planner import Planner
from .execution_loop import ExecutionLoop
from ..capability.awareness import CapabilityAwareness


@dataclass
class RunnerState:
    objective_id: str
    status: str
    capability_snapshot: dict


class KSIRunner:
    def __init__(self, tool_executor):
        self.capabilities = CapabilityAwareness()
        self.planner = Planner()
        self.execution = ExecutionLoop(tool_executor)

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
