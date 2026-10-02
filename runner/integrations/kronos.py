class KronosInterface:
    """Interface boundary; actual execution remains owned by Kronos/M03."""

    def execute(self, execution_request: dict) -> dict:
        raise NotImplementedError("Kronos integration is not connected in Runner v0.1")
