"""Minimal end-to-end M02 reference experiment."""

from .evidence import EvidenceStore
from .models import Experiment
from .provenance import sha256_json
from .runner import ControlledRunner
from .state import QualificationMachine, QualificationState

def main():
    experiment = Experiment(
        configuration="A+B+C",
        hypothesis="Composition may expose a capability requiring cross-system interaction.",
        task_definition="Produce a deterministic structured result.",
        component_versions={"A":"reference","B":"reference","C":"reference"},
        model_versions={"reference":"0.1"},
        available_tools=[],
        input_information_hash=sha256_json({"task":"M02-REF-001"}),
        context_hash=sha256_json({"context":"controlled"}),
        resource_budget={"tokens":1000,"tool_calls":0},
        human_intervention={"level":"none"},
        task_decomposition={"steps":["compose","return"]},
        timestamp="2026-10-01T00:00:00Z",
        reproducibility_group="M02-REF-001",
    )
    result=ControlledRunner().run(experiment, lambda _: {"status":"reference-run"})
    store=EvidenceStore()
    store.append("experiment", experiment.to_dict())
    store.append("execution", result.execution.to_dict())
    machine=QualificationMachine()
    machine.transition(QualificationState.CANDIDATE)
    print({"experiment_id": experiment.experiment_id, "execution_id": result.execution.execution_id, "state": machine.state.value, "evidence_integrity": store.verify()})

if __name__ == "__main__":
    main()
