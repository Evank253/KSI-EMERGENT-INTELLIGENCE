import unittest

from runner.capability.awareness import CapabilityAwareness, CapabilityStatus
from runner.capability.gate import (
    CapabilityContext,
    CapabilityDisposition,
    authorize_capability,
)
from runner.governance.execution_boundary import GovernedExecutionBoundary
from runner.governance.gateway import ActionRequest, Authorization, Disposition


class TestCapabilityGate(unittest.TestCase):
    def test_missing_capability_fails_closed(self):
        context = CapabilityContext("HUMAN_OPERATOR", frozenset({"ANALYZE_OBJECTIVE"}))
        self.assertEqual(
            authorize_capability("", context),
            CapabilityDisposition.DENY,
        )

    def test_whitespace_capability_fails_closed(self):
        context = CapabilityContext("HUMAN_OPERATOR", frozenset({"ANALYZE_OBJECTIVE"}))
        self.assertEqual(
            authorize_capability("   ", context),
            CapabilityDisposition.DENY,
        )

    def test_explicit_grant_allows_exact_capability(self):
        context = CapabilityContext("HUMAN_OPERATOR", frozenset({"ANALYZE_OBJECTIVE"}))
        self.assertEqual(
            authorize_capability("ANALYZE_OBJECTIVE", context),
            CapabilityDisposition.ALLOW,
        )

    def test_unauthorized_capability_denied(self):
        context = CapabilityContext("HUMAN_OPERATOR", frozenset({"OTHER_CAPABILITY"}))
        self.assertEqual(
            authorize_capability("ANALYZE_OBJECTIVE", context),
            CapabilityDisposition.DENY,
        )

    def test_awareness_status_never_grants_authority(self):
        awareness = CapabilityAwareness()
        awareness.register_claim("ANALYZE_OBJECTIVE")
        measured = awareness.record_measurement("ANALYZE_OBJECTIVE", ["EVIDENCE-1"])
        measured.status = CapabilityStatus.VERIFIED
        context = CapabilityContext("HUMAN_OPERATOR", frozenset())
        self.assertEqual(
            authorize_capability("ANALYZE_OBJECTIVE", context),
            CapabilityDisposition.DENY,
        )

    def test_capability_denial_prevents_executor(self):
        executed = []
        boundary = GovernedExecutionBoundary(
            lambda action, target: executed.append((action, target))
        )
        request = ActionRequest(
            "analyze",
            "analysis",
            True,
            "COGNITIVE_OPERATION",
            "KSI_RUNNER",
            "ANALYZE_OBJECTIVE",
        )
        authorization = Authorization(
            "HUMAN_OPERATOR",
            "COGNITIVE_OPERATION",
            True,
            True,
            frozenset({"OTHER_CAPABILITY"}),
        )
        decision, output = boundary.execute(request, authorization)
        self.assertEqual(decision.capability_disposition, CapabilityDisposition.DENY)
        self.assertEqual(decision.disposition, Disposition.REJECT)
        self.assertIsNone(output)
        self.assertEqual(executed, [])

    def test_capability_allow_governance_reject_prevents_executor(self):
        executed = []
        boundary = GovernedExecutionBoundary(
            lambda action, target: executed.append((action, target))
        )
        request = ActionRequest(
            "analyze",
            "analysis",
            True,
            "COGNITIVE_OPERATION",
            "KSI_RUNNER",
            "ANALYZE_OBJECTIVE",
        )
        authorization = Authorization(
            "HUMAN_OPERATOR",
            "ENGINEERING_OPERATION",
            True,
            True,
            frozenset({"ANALYZE_OBJECTIVE"}),
        )
        decision, output = boundary.execute(request, authorization)
        self.assertEqual(decision.capability_disposition, CapabilityDisposition.ALLOW)
        self.assertEqual(decision.disposition, Disposition.REJECT)
        self.assertIsNone(output)
        self.assertEqual(executed, [])

    def test_both_gates_allow_before_executor(self):
        executed = []
        boundary = GovernedExecutionBoundary(
            lambda action, target: executed.append((action, target)) or "EXECUTED"
        )
        request = ActionRequest(
            "analyze",
            "analysis",
            True,
            "COGNITIVE_OPERATION",
            "KSI_RUNNER",
            "ANALYZE_OBJECTIVE",
        )
        authorization = Authorization(
            "HUMAN_OPERATOR",
            "COGNITIVE_OPERATION",
            True,
            True,
            frozenset({"ANALYZE_OBJECTIVE"}),
        )
        decision, output = boundary.execute(request, authorization)
        self.assertEqual(decision.capability_disposition, CapabilityDisposition.ALLOW)
        self.assertEqual(decision.disposition, Disposition.ALLOW)
        self.assertEqual(output, "EXECUTED")
        self.assertEqual(executed, [("analyze", "analysis")])


if __name__ == "__main__":
    unittest.main()
