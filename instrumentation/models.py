"""Canonical records for the M02 evidence chain."""

from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any
from .provenance import immutable_id, sha256_json

@dataclass(frozen=True)
class Experiment:
    configuration: str
    hypothesis: str
    task_definition: str
    component_versions: dict[str, str]
    model_versions: dict[str, str]
    available_tools: list[str]
    input_information_hash: str
    context_hash: str
    resource_budget: dict[str, Any]
    human_intervention: dict[str, Any]
    task_decomposition: dict[str, Any]
    experiment_id: str = field(default_factory=lambda: immutable_id("exp"))
    timestamp: str = ""
    reproducibility_group: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class Execution:
    experiment_id: str
    execution_id: str = field(default_factory=lambda: immutable_id("run"))
    execution_trace: list[dict[str, Any]] = field(default_factory=list)
    outputs: list[Any] = field(default_factory=list)
    errors: list[dict[str, Any]] = field(default_factory=list)
    latency_ms: float | None = None
    cost: float | None = None
    resource_usage: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class Artifact:
    experiment_id: str
    execution_id: str
    kind: str
    content: Any
    artifact_id: str = field(default_factory=lambda: immutable_id("art"))
    parent_hash: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["content_hash"] = sha256_json(self.content)
        return d

@dataclass(frozen=True)
class Measurement:
    experiment_id: str
    execution_id: str
    metric: str
    value: float
    method: str
    artifact_refs: list[str]
    measurement_id: str = field(default_factory=lambda: immutable_id("meas"))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class Evidence:
    experiment_id: str
    evidence_refs: list[str]
    claim: str
    status: str
    provenance_hash: str
    evidence_id: str = field(default_factory=lambda: immutable_id("ev"))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
