import unittest

from runner.governance.execution_boundary import GovernedExecutionBoundary
from runner.governance.gateway import ActionRequest, Authorization, Disposition


class TestRunnerValidationMatrix(unittest.TestCase):
    def setUp(self):
        self.executed = []
        self.boundary = GovernedExecutionBoundary(
            lambda action, target: self.executed.append((action, target)) or "EXECUTED"
        )

    def _run(self, request, authorization):
        return self.boundary.execute(request, authorization)

    def test_normal_authorized_operation(self):
        request = ActionRequest("analyze", "analysis", True, "COGNITIVE_OPERATION", "KSI_RUNNER")
        decision, output = self._run(request, Authorization("HUMAN_OPERATOR", "COGNITIVE_OPERATION", True, True))
        self.assertEqual(decision.disposition, Disposition.ALLOW)
        self.assertEqual(output, "EXECUTED")

    def test_missing_authorization(self):
        request = ActionRequest("analyze", "analysis", True, "COGNITIVE_OPERATION", "KSI_RUNNER")
        decision, _ = self._run(request, None)
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_wrong_authorization_scope(self):
        request = ActionRequest("analyze", "analysis", True, "COGNITIVE_OPERATION", "KSI_RUNNER")
        decision, _ = self._run(request, Authorization("HUMAN_OPERATOR", "ENGINEERING_OPERATION", True, True))
        self.assertEqual(decision.disposition, Disposition.REJECT)

    def test_runner_requests_greater_authority(self):
        request = ActionRequest("expand", "authority_model", True, "GOVERNANCE_CHANGE", "KSI_RUNNER")
        decision, _ = self._run(request, Authorization("KSI_RUNNER", "GOVERNANCE_CHANGE", True, True))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_runner_modifies_constitution(self):
        request = ActionRequest("modify", "constitution", True, "GOVERNANCE_CHANGE", "KSI_RUNNER")
        decision, _ = self._run(request, Authorization("HUMAN_OPERATOR", "GOVERNANCE_CHANGE", True, True))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_runner_modifies_authority_model(self):
        request = ActionRequest("modify", "authority_model", True, "GOVERNANCE_CHANGE", "KSI_RUNNER")
        decision, _ = self._run(request, Authorization("HUMAN_OPERATOR", "GOVERNANCE_CHANGE", True, True))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_emergent_capability_claims_authority(self):
        request = ActionRequest("grant", "authority_model", True, "GOVERNANCE_CHANGE", "EMERGENT_CAPABILITY")
        decision, _ = self._run(request, Authorization("EMERGENT_CAPABILITY", "GOVERNANCE_CHANGE", True, True))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_qualification_claims_authority(self):
        request = ActionRequest("grant", "authority_model", True, "GOVERNANCE_CHANGE", "QUALIFIED_CAPABILITY")
        decision, _ = self._run(request, Authorization("QUALIFIED_CAPABILITY", "GOVERNANCE_CHANGE", True, True))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_historical_evidence_modification(self):
        request = ActionRequest("rewrite", "evidence_history", True, "GOVERNANCE_CHANGE", "KSI_RUNNER")
        decision, _ = self._run(request, Authorization("HUMAN_OPERATOR", "GOVERNANCE_CHANGE", True, True))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_agent_bypass(self):
        request = ActionRequest("authorize", "authorization_scopes", True, "GOVERNANCE_CHANGE", "AGENT")
        decision, _ = self._run(request, Authorization("AGENT", "GOVERNANCE_CHANGE", True, True))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_tool_bypass_is_not_available_through_boundary(self):
        request = ActionRequest("execute_direct", "tool_registry", True, "COGNITIVE_OPERATION", "TOOL")
        decision, output = self._run(request, None)
        self.assertEqual(decision.disposition, Disposition.ESCALATE)
        self.assertIsNone(output)
        self.assertEqual(self.executed, [])


if __name__ == "__main__":
    unittest.main()
