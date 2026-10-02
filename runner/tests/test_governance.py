import unittest

from runner.governance.gateway import (
    ActionRequest,
    Authorization,
    Disposition,
    authorize,
)


class TestRunnerGovernance(unittest.TestCase):
    def test_capability_does_not_grant_authority(self):
        request = ActionRequest(
            action="expand_permissions",
            target="authorization_scopes",
            consequential=True,
            required_scope="GOVERNANCE_CHANGE",
            requested_by="KSI_RUNNER",
        )
        authorization = Authorization(
            actor="KSI_RUNNER",
            scope="GOVERNANCE_CHANGE",
            approved=True,
            human_authorized=False,
        )
        self.assertEqual(authorize(request, authorization), Disposition.ESCALATE)

    def test_missing_authorization_escalates(self):
        request = ActionRequest(
            action="deploy",
            target="production",
            consequential=True,
            required_scope="DEPLOYMENT_OPERATION",
            requested_by="KSI_RUNNER",
        )
        self.assertEqual(authorize(request, None), Disposition.ESCALATE)

    def test_wrong_scope_rejected(self):
        request = ActionRequest(
            action="deploy",
            target="production",
            consequential=True,
            required_scope="DEPLOYMENT_OPERATION",
            requested_by="KSI_RUNNER",
        )
        authorization = Authorization(
            actor="HUMAN_OPERATOR",
            scope="ENGINEERING_OPERATION",
            approved=True,
            human_authorized=True,
        )
        self.assertEqual(authorize(request, authorization), Disposition.REJECT)

    def test_governance_change_never_becomes_runner_authority(self):
        request = ActionRequest(
            action="modify_constitution",
            target="constitution",
            consequential=True,
            required_scope="GOVERNANCE_CHANGE",
            requested_by="KSI_RUNNER",
        )
        authorization = Authorization(
            actor="HUMAN_OPERATOR",
            scope="GOVERNANCE_CHANGE",
            approved=True,
            human_authorized=True,
        )
        self.assertEqual(authorize(request, authorization), Disposition.ESCALATE)

    def test_authorized_non_protected_action_executes(self):
        request = ActionRequest(
            action="run_analysis",
            target="analysis",
            consequential=True,
            required_scope="ENGINEERING_OPERATION",
            requested_by="KSI_RUNNER",
        )
        authorization = Authorization(
            actor="HUMAN_OPERATOR",
            scope="ENGINEERING_OPERATION",
            approved=True,
            human_authorized=True,
        )
        self.assertEqual(authorize(request, authorization), Disposition.ALLOW)


if __name__ == "__main__":
    unittest.main()
