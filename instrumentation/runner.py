"""Controlled runners. The system under test is injected as a callable."""

from __future__ import annotations
import time
from dataclasses import dataclass
from typing import Any, Callable
from .models import Experiment, Execution

CONFIGURATIONS = ("A", "B", "C", "A+B", "A+C", "B+C", "A+B+C")

@dataclass(frozen=True)
class RunResult:
    experiment: Experiment
    execution: Execution

class ControlledRunner:
    def run(self, experiment: Experiment, system: Callable[[Experiment], Any]) -> RunResult:
        if experiment.configuration not in CONFIGURATIONS:
            raise ValueError(f"Unsupported configuration: {experiment.configuration}")
        started = time.perf_counter()
        errors: list[dict[str, Any]] = []
        outputs: list[Any] = []
        try:
            outputs.append(system(experiment))
        except Exception as exc:
            errors.append({"type": type(exc).__name__, "message": str(exc)})
        latency_ms = (time.perf_counter() - started) * 1000
        execution = Execution(
            experiment_id=experiment.experiment_id,
            execution_trace=[{"event": "start"}, {"event": "finish"}],
            outputs=outputs,
            errors=errors,
            latency_ms=latency_ms,
        )
        return RunResult(experiment, execution)
