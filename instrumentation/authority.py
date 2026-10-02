"""Authority isolation primitives."""

from __future__ import annotations

def authority_for_qualification(_: str) -> None:
    """Qualification intentionally has no authority-granting side effect."""
    return None

def assert_no_authority_grant(before: dict, after: dict) -> None:
    if before != after:
        raise AssertionError("Qualification changed authority state")
