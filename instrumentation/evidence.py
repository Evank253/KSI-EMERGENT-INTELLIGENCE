"""Append-only, tamper-evident evidence records."""

from __future__ import annotations
import copy
from dataclasses import dataclass
from typing import Any
from .provenance import sha256_json, lineage_hash

@dataclass(frozen=True)
class EvidenceRecord:
    sequence: int
    record_type: str
    payload: dict[str, Any]
    parent_hash: str | None
    record_hash: str

class EvidenceStore:
    def __init__(self):
        self._records: list[EvidenceRecord] = []

    def append(self, record_type: str, payload: dict[str, Any]) -> EvidenceRecord:
        if not isinstance(payload, dict):
            raise TypeError("Evidence payload must be a mapping")
        frozen_payload = copy.deepcopy(payload)
        parent = self._records[-1].record_hash if self._records else None
        record_hash = lineage_hash(parent, {"record_type": record_type, "payload": frozen_payload})
        record = EvidenceRecord(len(self._records), record_type, frozen_payload, parent, record_hash)
        self._records.append(record)
        return record

    def records(self) -> tuple[EvidenceRecord, ...]:
        return tuple(self._records)

    def verify(self) -> bool:
        parent = None
        for index, record in enumerate(self._records):
            if record.sequence != index or record.parent_hash != parent:
                return False
            expected = lineage_hash(parent, {"record_type": record.record_type, "payload": record.payload})
            if expected != record.record_hash:
                return False
            parent = record.record_hash
        return True
