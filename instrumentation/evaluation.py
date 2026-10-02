"""Independent evaluation primitives."""

from __future__ import annotations
from typing import Any, Callable
from .models import Execution, Measurement

class Evaluator:
    def measure(self, execution: Execution, metric: str, scorer: Callable[[Any], float], method: str) -> Measurement:
        if not execution.outputs:
            raise ValueError("Cannot measure an execution with no output")
        value = float(scorer(execution.outputs[0]))
        return Measurement(
            experiment_id=execution.experiment_id,
            execution_id=execution.execution_id,
            metric=metric,
            value=value,
            method=method,
            artifact_refs=[],
        )

def compare(values: dict[str, float]) -> dict[str, float]:
    if not values:
        return {}
    baseline = max(values.values())
    return {name: value - baseline for name, value in values.items()}
