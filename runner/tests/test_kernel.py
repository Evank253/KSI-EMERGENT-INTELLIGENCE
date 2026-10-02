import unittest

from runner.kernel.objective import Objective
from runner.kernel.runner import KSIRunner
from runner.governance.gateway import Authorization, Disposition


class TestRunnerKernel(unittest.TestCase):
    def test_runner_starts_with_objective_and_plans(self):
        runner = KSIRunner(lambda action, target: {"ok": True})
        result = runner.run(Objective("RUNNER-001", "Analyze a deterministic task", "HUMAN_OPERATOR"))
        self.assertEqual(result["objective"].objective_id, "RUNNER-001")
        self.assertEqual(len(result["plan"]), 1)
        self.assertEqual(result["plan"][0].required_capability, "ANALYZE_OBJECTIVE")
        self.assertEqual(result["qualification"], "NOT_QUALIFIED")
        self.assertFalse(result["authority_granted"])

    def test_runner_can_execute_authorized_non_protected_step(self):
        runner = KSIRunner(lambda action, target: {"ok": True})
        result = runner.run(
            Objective("RUNNER-006", "Run authorized analysis", "HUMAN_OPERATOR"),
            Authorization(
                "HUMAN_OPERATOR",
                "COGNITIVE_OPERATION",
                True,
                True,
                frozenset({"ANALYZE_OBJECTIVE"}),
            ),
        )
        self.assertEqual(result["results"][0].disposition, Disposition.ALLOW)


if __name__ == "__main__":
    unittest.main()
