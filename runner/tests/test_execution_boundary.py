import unittest

from runner.governance.execution_boundary import (
    GovernanceBoundaryError,
    GovernedExecutionBoundary,
    require_governed_execution,
)
from runner.governance.gateway import ActionRequest, Authorization, Disposition


class TestExecutionBoundary(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.boundary = GovernedExecutionBoundary(
            lambda action, target: self.calls.append((action, target)) or {"ok": True}
        )

    def test_authorized_execution_crosses_boundary(self):
        request = ActionRequest(
            action="compute",
            target="deterministic_fixture",
            consequential=True,
            required_scope="COGNITIVE_OPERATION",
            requested_by="KSI_RUNNER",
        )
        auth = Authorization("HUMAN_OPERATOR", "COGNITIVE_OPERATION", True, True)
        decision, output = self.boundary.execute(request, auth)
        self.assertEqual(decision.disposition, Disposition.ALLOW)
        self.assertEqual(output, {"ok": True})
        self.assertEqual(len(self.calls), 1)

    def test_missing_authorization_never_reaches_tool(self):
        request = ActionRequest(
            action="compute",
            target="deterministic_fixture",
            consequential=True,
            required_scope="COGNITIVE_OPERATION",
            requested_by="KSI_RUNNER",
        )
        decision, output = self.boundary.execute(request, None)
        self.assertEqual(decision.disposition, Disposition.ESCALATE)
        self.assertIsNone(output)
        self.assertEqual(self.calls, [])

    def test_wrong_scope_never_reaches_tool(self):
        request = ActionRequest(
            action="compute",
            target="deterministic_fixture",
            consequential=True,
            required_scope="COGNITIVE_OPERATION",
            requested_by="KSI_RUNNER",
        )
        auth = Authorization("HUMAN_OPERATOR", "ENGINEERING_OPERATION", True, True)
        decision, output = self.boundary.execute(request, auth)
        self.assertEqual(decision.disposition, Disposition.REJECT)
        self.assertIsNone(output)
        self.assertEqual(self.calls, [])

    def test_protected_target_always_stops_at_boundary(self):
        request = ActionRequest(
            action="modify_constitution",
            target="constitution",
            consequential=True,
            required_scope="GOVERNANCE_CHANGE",
            requested_by="KSI_RUNNER",
        )
        auth = Authorization("HUMAN_OPERATOR", "GOVERNANCE_CHANGE", True, True)
        decision, output = self.boundary.execute(request, auth)
        self.assertEqual(decision.disposition, Disposition.ESCALATE)
        self.assertIsNone(output)
        self.assertEqual(self.calls, [])

    def test_execution_decision_is_required_before_tool_result(self):
        request = ActionRequest(
            action="compute",
            target="deterministic_fixture",
            consequential=True,
            required_scope="COGNITIVE_OPERATION",
            requested_by="KSI_RUNNER",
        )
        auth = Authorization("HUMAN_OPERATOR", "COGNITIVE_OPERATION", True, True)
        decision, _ = self.boundary.execute(request, auth)
        require_governed_execution(decision)

        with self.assertRaises(GovernanceBoundaryError):
            require_governed_execution(
                type(decision)(
                    disposition=Disposition.REJECT,
                    request=request,
                )
            )


if __name__ == "__main__":
    unittest.main()
