"""Deterministic IDs, hashing, and parent/child provenance."""

from __future__ import annotations
import hashlib
import json
import uuid
from typing import Any

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))

def immutable_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"

def lineage_hash(parent_hash: str | None, payload: Any) -> str:
    body = {"parent_hash": parent_hash, "payload": payload}
    return sha256_json(body)

def verify_hash(value: Any, expected_hash: str) -> bool:
    return sha256_json(value) == expected_hash
