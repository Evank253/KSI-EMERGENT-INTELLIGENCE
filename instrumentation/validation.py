"""Schema validation without third-party dependencies."""

from __future__ import annotations
from typing import Any

REQUIRED_EXPERIMENT_FIELDS = {
    "experiment_id", "timestamp", "configuration", "hypothesis", "task_definition",
    "component_versions", "model_versions", "available_tools", "input_information_hash",
    "context_hash", "resource_budget", "human_intervention", "task_decomposition",
    "reproducibility_group",
}

def validate_experiment(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_EXPERIMENT_FIELDS - record.keys())
    errors.extend(f"missing:{field}" for field in missing)
    if record.get("configuration") not in {"A", "B", "C", "A+B", "A+C", "B+C", "A+B+C"}:
        errors.append("invalid:configuration")
    for field in ("component_versions", "model_versions", "resource_budget", "human_intervention", "task_decomposition"):
        if field in record and not isinstance(record[field], dict):
            errors.append(f"invalid:{field}:expected_object")
    for field in ("available_tools",):
        if field in record and not isinstance(record[field], list):
            errors.append(f"invalid:{field}:expected_array")
    return errors

def assert_valid_experiment(record: dict[str, Any]) -> None:
    errors = validate_experiment(record)
    if errors:
        raise ValueError("; ".join(errors))
