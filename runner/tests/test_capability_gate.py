import unittest
from unittest.mock import patch

from runner.capability.awareness import CapabilityAwareness, CapabilityStatus
from runner.governance.capability_context import CapabilityContext
from runner.governance.capability_gate import (
    CapabilityDisposition,
    authorize_capability,
)
from runner.governance.execution_boundary import GovernedExecutionBoundary
from runner.governance.gateway import ActionRequest, Authorization, Disposition


class TestCapabilityGate(unittest.TestCase):
    def _context(self, grants=frozenset({"ANALYZE_OBJECTIVE"})):
        return CapabilityContext("HUMAN_OPERATOR", grants, "TEST-RUN")

    def _request(self):
        return ActionRequest(
            "analyze", "analysis", True, "COGNITIVE_OPERATION", "KSI_RUNNER", "ANALYZE_OBJECTIVE"
        )

    def _boundary(self, grants=frozenset({"ANALYZE_OBJECTIVE"})):
        executed = []
        boundary = GovernedExecutionBoundary(
            lambda action, target: executed.append((action, target)) or "EXECUTED",
            self._context(grants),
        )
        return boundary, executed

    def test_missing_capability_fails_closed(self):
        self.assertEqual(authorize_capability("", self._context()), CapabilityDisposition.DENY)

    def test_whitespace_capability_fails_closed(self):
        self.assertEqual(authorize_capability("   ", self._context()), CapabilityDisposition.DENY)

    def test_invalid_capability_type_fails_closed(self):
        self.assertEqual(authorize_capability(123, self._context()), CapabilityDisposition.DENY)

    def test_explicit_grant_allows_exact_capability(self):
        self.assertEqual(authorize_capability("ANALYZE_OBJECTIVE", self._context()), CapabilityDisposition.ALLOW)

    def test_unauthorized_capability_denied(self):
        self.assertEqual(authorize_capability("OTHER_CAPABILITY", self._context()), CapabilityDisposition.DENY)

    def test_awareness_status_never_grants_authority(self):
        awareness = CapabilityAwareness()
        awareness.register_claim("ANALYZE_OBJECTIVE")
        measured = awareness.record_measurement("ANALYZE_OBJECTIVE", ["EVIDENCE-1"])
        measured.status = CapabilityStatus.VERIFIED
        self.assertEqual(authorize_capability("ANALYZE_OBJECTIVE", self._context(frozenset())), CapabilityDisposition.DENY)

    def test_capability_allow_alone_never_executes(self):
        boundary, executed = self._boundary()
        request = self._request()
        decision, output = boundary.execute(request, None)
        self.assertEqual(decision.capability_disposition, CapabilityDisposition.ALLOW)
        self.assertEqual(decision.disposition, Disposition.ESCALATE)
        self.assertIsNone(output)
        self.assertEqual(executed, [])

    def test_capability_denial_prevents_executor(self):
        boundary, executed = self._boundary(frozenset({"OTHER_CAPABILITY"}))
        decision, output = boundary.execute(self._request(), Authorization("HUMAN_OPERATOR", "COGNITIVE_OPERATION"))
        self.assertEqual(decision.capability_disposition, CapabilityDisposition.DENY)
        self.assertEqual(decision.disposition, Disposition.REJECT)
        self.assertIsNone(output)
        self.assertEqual(executed, [])

    def test_distinct_gate_invoked_on_boundary_path(self):
        boundary, executed = self._boundary()
        with patch("runner.governance.execution_boundary.authorize_capability", wraps=authorize_capability) as gate:
            boundary.execute(self._request(), Authorization("HUMAN_OPERATOR", "COGNITIVE_OPERATION", True, True))
        gate.assert_called_once()
        self.assertEqual(executed, [])

    def test_distinct_gate_invoked_on_execute_step_path(self):
        boundary, executed = self._boundary()
        step = type("Step", (), {
            "action": "analyze",
            "target": "analysis",
            "consequential": True,
            "required_scope": "COGNITIVE_OPERATION",
            "required_capability": "ANALYZE_OBJECTIVE",
        })()
        with patch("runner.governance.execution_boundary.authorize_capability", wraps=authorize_capability) as gate:
            boundary.execute_step(step, Authorization("HUMAN_OPERATOR", "COGNITIVE_OPERATION", True, True, frozenset()))
        gate.assert_called_once()
        self.assertEqual(executed, [])


if __name__ == "__main__":
    unittest.main()
