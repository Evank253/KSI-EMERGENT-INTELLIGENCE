from dataclasses import dataclass, field
from enum import Enum


class CapabilityStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    CLAIMED = "CLAIMED"
    MEASURED = "MEASURED"
    VERIFIED = "VERIFIED"


@dataclass
class CapabilityRecord:
    capability_id: str
    status: CapabilityStatus = CapabilityStatus.UNKNOWN
    evidence_refs: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    confidence: float | None = None


class CapabilityAwareness:
    def __init__(self) -> None:
        self._records: dict[str, CapabilityRecord] = {}

    def register_claim(self, capability_id: str, limitations: list[str] | None = None) -> CapabilityRecord:
        record = CapabilityRecord(
            capability_id=capability_id,
            status=CapabilityStatus.CLAIMED,
            limitations=limitations or [],
        )
        self._records[capability_id] = record
        return record

    def record_measurement(
        self,
        capability_id: str,
        evidence_refs: list[str],
        confidence: float | None = None,
    ) -> CapabilityRecord:
        record = self._records.setdefault(CapabilityRecord(capability_id=capability_id).capability_id,
                                           CapabilityRecord(capability_id=capability_id))
        record.status = CapabilityStatus.MEASURED
        record.evidence_refs = list(evidence_refs)
        record.confidence = confidence
        return record

    def get(self, capability_id: str) -> CapabilityRecord:
        return self._records.get(capability_id, CapabilityRecord(capability_id=capability_id))

    def snapshot(self) -> dict[str, dict]:
        return {
            key: {
                "status": value.status.value,
                "evidence_refs": list(value.evidence_refs),
                "limitations": list(value.limitations),
                "confidence": value.confidence,
            }
            for key, value in self._records.items()
        }
