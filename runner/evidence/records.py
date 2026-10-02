from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    observation: dict
    provenance: dict
    epistemic_state: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def content_hash(self) -> str:
        payload = {
            "evidence_id": self.evidence_id,
            "observation": self.observation,
            "provenance": self.provenance,
            "epistemic_state": self.epistemic_state,
            "created_at": self.created_at,
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
