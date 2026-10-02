from dataclasses import dataclass


@dataclass(frozen=True)
class PlanStep:
    step_id: str
    action: str
    target: str
    consequential: bool
    required_scope: str


class Planner:
    def plan(self, objective) -> list[PlanStep]:
        return [
            PlanStep(
                step_id=f"{objective.objective_id}:001",
                action="analyze_objective",
                target="cognition",
                consequential=False,
                required_scope="COGNITIVE_OPERATION",
            )
        ]
