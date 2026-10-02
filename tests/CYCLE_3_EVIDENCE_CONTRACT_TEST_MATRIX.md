# Cycle 3 Evidence Contract — Test Matrix

| ID | Condition | Expected |
|---|---|---|
| C3-CON-001 | Complete Package A + authorized repair + complete Package B + comparison | OBSERVED |
| C3-CON-002 | Package B has null predecessor | LINEAGE_INCOMPLETE |
| C3-CON-003 | Package B has null repair_id | LINEAGE_INCOMPLETE |
| C3-CON-004 | Package B has null state_id | LINEAGE_INCOMPLETE |
| C3-CON-005 | Package B has state_sequence 0 | LINEAGE_INCOMPLETE |
| C3-CON-006 | Test ID differs A vs B | TEST_IDENTITY_MISMATCH |
| C3-CON-007 | Test version differs A vs B | TEST_IDENTITY_MISMATCH |
| C3-CON-008 | Assertion/evaluation contract differs | TEST_IDENTITY_MISMATCH |
| C3-CON-009 | Package B status is generic constitutional package | EVIDENCE_INSUFFICIENT |
| C3-CON-010 | Package B result is not PASS | EVIDENCE_INSUFFICIENT |
| C3-CON-011 | Package A is reused as Package B | EVIDENCE_INSUFFICIENT |
| C3-CON-012 | Repair has no authorization | AUTHORIZATION_FAILURE |
| C3-CON-013 | Package A is modified after sealing | EVIDENCE_INSUFFICIENT |
| C3-CON-014 | Comparison is null | LINEAGE_INCOMPLETE |
| C3-CON-015 | Runtime before/after absent when required | EVIDENCE_INSUFFICIENT |
| C3-CON-016 | FAIL → PASS with complete lineage and identical test | OBSERVED |
| C3-CON-017 | Cycle 3 attempts qualification without M02 | NOT_QUALIFIED |
| C3-CON-018 | Cycle 3 attempts authority grant | AUTHORITY_NOT_GRANTED |

## Core invariant

A FAIL → PASS statement without reconstructable Package A → Repair → State B → Package B lineage is not a cleanly sealed Cycle 3 result.
