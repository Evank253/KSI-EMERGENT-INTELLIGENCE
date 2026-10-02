import unittest
from instrumentation.evidence import EvidenceStore
from instrumentation.models import Experiment
from instrumentation.provenance import sha256_json
from instrumentation.runner import ControlledRunner
from instrumentation.state import QualificationMachine, QualificationState, InvalidTransition
from instrumentation.validation import validate_experiment
from instrumentation.authority import assert_no_authority_grant

class TestM02(unittest.TestCase):
    def experiment(self, configuration="A"):
        return Experiment(
            configuration=configuration,
            hypothesis="test composition hypothesis",
            task_definition="return a deterministic capability result",
            component_versions={"A":"1.0"},
            model_versions={"test":"1.0"},
            available_tools=[],
            input_information_hash=sha256_json({"input":"x"}),
            context_hash=sha256_json({"context":"y"}),
            resource_budget={"tokens":100},
            human_intervention={"level":"none"},
            task_decomposition={"steps":1},
            timestamp="2026-10-01T00:00:00Z",
            reproducibility_group="M02-REF-001",
        )

    def test_schema_rejects_missing_fields(self):
        errors = validate_experiment({"configuration":"A"})
        self.assertTrue(errors)

    def test_hash_detects_modification(self):
        payload={"answer":"ok"}
        digest=sha256_json(payload)
        self.assertNotEqual(digest, sha256_json({"answer":"changed"}))

    def test_lineage_is_intact(self):
        store=EvidenceStore()
        store.append("experiment", {"id":"exp"})
        store.append("execution", {"id":"run"})
        self.assertTrue(store.verify())

    def test_invalid_transition_rejected(self):
        machine=QualificationMachine()
        with self.assertRaises(InvalidTransition):
            machine.transition(QualificationState.QUALIFIED)

    def test_runner_records_execution(self):
        result=ControlledRunner().run(self.experiment("A+B"), lambda _: {"capability":"ok"})
        self.assertEqual(result.experiment.configuration, "A+B")
        self.assertEqual(result.execution.outputs[0]["capability"], "ok")

    def test_authority_is_unchanged(self):
        before={"authorized_actions":[]}
        after={"authorized_actions":[]}
        assert_no_authority_grant(before, after)

if __name__ == "__main__":
    unittest.main()
