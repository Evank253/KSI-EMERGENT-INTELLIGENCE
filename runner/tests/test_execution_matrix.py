import unittest

from runner.governance.execution_boundary import GovernedExecutionBoundary
from runner.governance.gateway import ActionRequest, Authorization, Disposition


class TestRunnerValidationMatrix(unittest.TestCase):
    def setUp(self):
        self.executed = []
        self.boundary = GovernedExecutionBoundary(
            lambda action, target: self.executed.append((action, target)) or "EXECUTED"
        )

    def _request(self, capability="ANALYZE_OBJECTIVE", target="analysis", scope="COGNITIVE_OPERATION"):
        return ActionRequest(
            "analyze", target, True, scope, "KSI_RUNNER", capability
        )

    def _auth(self, scope="COGNITIVE_OPERATION", grants=frozenset({"ANALYZE_OBJECTIVE"})):
        return Authorization("HUMAN_OPERATOR", scope, True, True, grants)

    def test_normal_authorized_operation(self):
        decision, output = self.boundary.execute(self._request(), self._auth())
        self.assertEqual(decision.disposition, Disposition.ALLOW)
        self.assertEqual(output, "EXECUTED")

    def test_missing_authorization_fails_capability_gate_first(self):
        decision, _ = self.boundary.execute(self._request(), None)
        self.assertEqual(decision.disposition, Disposition.REJECT)

    def test_wrong_authorization_scope_rejected_after_capability_gate(self):
        decision, _ = self.boundary.execute(
            self._request(), self._auth("ENGINEERING_OPERATION")
        )
        self.assertEqual(decision.disposition, Disposition.REJECT)

    def test_runner_requests_greater_authority(self):
        request = self._request("ANALYZE_OBJECTIVE", "authority_model", "GOVERNANCE_CHANGE")
        decision, _ = self.boundary.execute(request, self._auth("GOVERNANCE_CHANGE"))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_runner_modifies_constitution(self):
        request = self._request("ANALYZE_OBJECTIVE", "constitution", "GOVERNANCE_CHANGE")
        decision, _ = self.boundary.execute(request, self._auth("GOVERNANCE_CHANGE"))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_runner_modifies_authority_model(self):
        request = self._request("ANALYZE_OBJECTIVE", "authority_model", "GOVERNANCE_CHANGE")
        decision, _ = self.boundary.execute(request, self._auth("GOVERNANCE_CHANGE"))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_emergent_capability_claims_authority(self):
        request = self._request("ANALYZE_OBJECTIVE", "authority_model", "GOVERNANCE_CHANGE")
        decision, _ = self.boundary.execute(
            request,
            Authorization("EMERGENT_CAPABILITY", "GOVERNANCE_CHANGE", True, True, frozenset({"ANALYZE_OBJECTIVE"})),
        )
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_qualification_claims_authority(self):
        request = self._request("ANALYZE_OBJECTIVE", "authority_model", "GOVERNANCE_CHANGE")
        decision, _ = self.boundary.execute(
            request,
            Authorization("QUALIFIED_CAPABILITY", "GOVERNANCE_CHANGE", True, True, frozenset({"ANALYZE_OBJECTIVE"})),
        )
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_historical_evidence_modification(self):
        request = self._request("ANALYZE_OBJECTIVE", "evidence_history", "GOVERNANCE_CHANGE")
        decision, _ = self.boundary.execute(request, self._auth("GOVERNANCE_CHANGE"))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_agent_bypass(self):
        request = self._request("ANALYZE_OBJECTIVE", "authorization_scopes", "GOVERNANCE_CHANGE")
        decision, _ = self.boundary.execute(
            request,
            Authorization("AGENT", "GOVERNANCE_CHANGE", True, True, frozenset({"ANALYZE_OBJECTIVE"})),
        )
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_tool_bypass_is_not_available_through_boundary(self):
        request = self._request("ANALYZE_OBJECTIVE", "tool_registry")
        decision, output = self.boundary.execute(request, None)
        self.assertEqual(decision.disposition, Disposition.REJECT)
        self.assertIsNone(output)
        self.assertEqual(self.executed, [])

    def test_missing_capability_fails_closed(self):
        request = self._request("")
        decision, output = self.boundary.execute(request, self._auth())
        self.assertEqual(decision.disposition, Disposition.REJECT)
        self.assertIsNone(output)
        self.assertEqual(self.executed, [])

    def test_capability_substitution_denied(self):
        request = self._request("OTHER_CAPABILITY")
        decision, output = self.boundary.execute(request, self._auth())
        self.assertEqual(decision.disposition, Disposition.REJECT)
        self.assertIsNone(output)
        self.assertEqual(self.executed, [])


if __name__ == "__main__":
    unittest.main()
