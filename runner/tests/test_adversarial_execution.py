import unittest

from runner.governance.execution_boundary import GovernedExecutionBoundary
from runner.governance.gateway import ActionRequest, Authorization, Disposition
from runner.capability.awareness import CapabilityAwareness, CapabilityStatus
from runner.evidence.epistemic import EpistemicState, can_advance


class TestAdversarialExecution(unittest.TestCase):
    def test_runner_requesting_greater_authority_escalates(self):
        boundary = GovernedExecutionBoundary(lambda *_: {"unexpected": True})
        request = ActionRequest(
            "expand_authority",
            "authority_model",
            True,
            "GOVERNANCE_CHANGE",
            "KSI_RUNNER",
        )
        decision, output = boundary.execute(request, Authorization(
            "KSI_RUNNER", "GOVERNANCE_CHANGE", True, True
        ))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)
        self.assertIsNone(output)

    def test_emergent_capability_cannot_become_authority(self):
        boundary = GovernedExecutionBoundary(lambda *_: {"unexpected": True})
        request = ActionRequest(
            "grant_self_authority",
            "authority_model",
            True,
            "GOVERNANCE_CHANGE",
            "KSI_RUNNER",
        )
        decision, _ = boundary.execute(request, Authorization(
            "HUMAN_OPERATOR", "GOVERNANCE_CHANGE", True, True
        ))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_qualification_cannot_grant_authority(self):
        boundary = GovernedExecutionBoundary(lambda *_: {"unexpected": True})
        request = ActionRequest(
            "grant_authority_from_qualification",
            "authority_model",
            True,
            "GOVERNANCE_CHANGE",
            "M02",
        )
        decision, _ = boundary.execute(request, Authorization(
            "M02", "GOVERNANCE_CHANGE", True, False
        ))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)

    def test_claim_without_evidence_remains_claimed(self):
        awareness = CapabilityAwareness()
        record = awareness.register_claim("DETERMINISTIC_COMPUTATION")
        self.assertEqual(record.status, CapabilityStatus.CLAIMED)
        self.assertEqual(record.evidence_refs, [])

    def test_failed_measurement_does_not_advance_epistemic_state(self):
        self.assertFalse(
            can_advance(EpistemicState.OBSERVED, EpistemicState.UNKNOWN)
        )

    def test_historical_evidence_modification_is_protected(self):
        boundary = GovernedExecutionBoundary(lambda *_: {"unexpected": True})
        request = ActionRequest(
            "rewrite_history",
            "evidence_history",
            True,
            "GOVERNANCE_CHANGE",
            "KSI_RUNNER",
        )
        decision, output = boundary.execute(request, Authorization(
            "HUMAN_OPERATOR", "GOVERNANCE_CHANGE", True, True
        ))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)
        self.assertIsNone(output)

    def test_agent_authorization_bypass_is_rejected(self):
        boundary = GovernedExecutionBoundary(lambda *_: {"unexpected": True})
        request = ActionRequest(
            "self_authorize",
            "authorization_scopes",
            True,
            "GOVERNANCE_CHANGE",
            "AGENT",
        )
        decision, output = boundary.execute(request, Authorization(
            "AGENT", "GOVERNANCE_CHANGE", True, True
        ))
        self.assertEqual(decision.disposition, Disposition.ESCALATE)
        self.assertIsNone(output)


if __name__ == "__main__":
    unittest.main()
