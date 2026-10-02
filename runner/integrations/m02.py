class M02Interface:
    """Interface boundary; qualification remains external and independent."""

    def submit_evidence(self, evidence_package: dict) -> dict:
        raise NotImplementedError("M02 integration is not connected in Runner v0.1")
