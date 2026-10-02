# Cycle 4 — Implementation Test Matrix

| ID | Scenario | Expected |
|---|---|---|
| C4-IMP-001 | Clean Cycle 3 + 3 valid PASS repetitions | REPRODUCED |
| C4-IMP-002 | Clean Cycle 3 + PASS, PASS, FAIL | REPRODUCIBILITY_NOT_ESTABLISHED |
| C4-IMP-003 | Test ID mismatch | INVALID_EXPERIMENT |
| C4-IMP-004 | Test version mismatch | INVALID_EXPERIMENT |
| C4-IMP-005 | Assertion contract mismatch | INVALID_EXPERIMENT |
| C4-IMP-006 | State identity changes | INVALID_EXPERIMENT |
| C4-IMP-007 | Source/state SHA changes | INVALID_EXPERIMENT |
| C4-IMP-008 | Invalid repetition evidence | INVALID_EXPERIMENT |
| C4-IMP-009 | Missing repetition evidence | INVALID_EXPERIMENT |
| C4-IMP-010 | Failed repetition omitted from aggregate | INVALID_EXPERIMENT |
| C4-IMP-011 | Retry-until-PASS behavior | INVALID_EXPERIMENT |
| C4-IMP-012 | Fourth run after clean 3-run reproduction | ALLOWED_AS_ADDITIONAL_OBSERVATION |
| C4-IMP-013 | Cycle 3 lineage incomplete | NOT_READY |
| C4-IMP-014 | Package B generic/non-Cycle-3 package | NOT_READY |
| C4-IMP-015 | Aggregate authority flag true | REJECT |
| C4-IMP-016 | Aggregate qualification state not NOT_QUALIFIED | REJECT |
| C4-IMP-017 | Repetition execution IDs duplicated | INVALID_EXPERIMENT |
| C4-IMP-018 | Repetition snapshots duplicated | INVALID_EXPERIMENT |
| C4-IMP-019 | Required fixture/input identity changes | INVALID_EXPERIMENT |
| C4-IMP-020 | Failed required run preserved in evidence | REPRODUCIBILITY_NOT_ESTABLISHED |

## Core invariant

The implementation must evaluate the configured repetitions as a fixed experiment. It cannot redefine success after observing results.
