import unittest

from runner.capability.awareness import CapabilityAwareness, CapabilityStatus


class TestCapabilityAwareness(unittest.TestCase):
    def test_claim_is_not_measurement(self):
        capabilities = CapabilityAwareness()
        capabilities.register_claim("software_engineering")
        self.assertEqual(
            capabilities.get("software_engineering").status,
            CapabilityStatus.CLAIMED,
        )

    def test_measurement_requires_evidence_reference(self):
        capabilities = CapabilityAwareness()
        record = capabilities.record_measurement(
            "software_engineering",
            ["M02-PACKAGE-001"],
            confidence=0.87,
        )
        self.assertEqual(record.status, CapabilityStatus.MEASURED)
        self.assertEqual(record.evidence_refs, ["M02-PACKAGE-001"])


if __name__ == "__main__":
    unittest.main()
