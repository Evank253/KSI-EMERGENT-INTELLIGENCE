# Cycle 4 — Implementation Specification

## Objective

Implement an executable reproducibility experiment against the frozen Cycle 3 Evidence Contract.

Cycle 4 must consume a clean Cycle 3 result. It must not repair an invalid Cycle 3 package while simultaneously claiming reproducibility.

## Preconditions

The implementation MUST verify:

1. Cycle 3 Package A exists and is sealed.
2. Cycle 3 repair authorization exists.
3. State B exists and is distinct from State A.
4. Cycle 3 Package B exists and is sealed as the repair-effect retest.
5. Package B explicitly references Package A, repair ID, and State B.
6. Test ID/version and assertion contract match.
7. Cycle 3 comparison is non-null and valid.
8. Cycle 3 remains within its controlled-fixture scope.

If any precondition fails: Cycle 4 = NOT_READY.

## Execution model

CYCLE 3 CLEAN PACKAGE B
        |
        v
     STATE B
        |
        +-- TEST-X v1.0 --> PASS #1
        |
        +-- TEST-X v1.0 --> PASS #2
        |
        +-- TEST-X v1.0 --> PASS #3
        |
        v
 REPRODUCIBILITY CHECK

The three repetitions must reference the same repaired-state identity.

A repetition is a new execution, not a new repair.

## Required behavior

For each repetition:

1. Create or verify an immutable snapshot bound to State B.
2. Verify source/state identity before execution.
3. Execute the exact same test identity/version.
4. Record observation independently.
5. Capture artifacts and hashes.
6. Seal an evidence package for that repetition.
7. Preserve predecessor/reference lineage.
8. Mark the repetition valid or invalid.
9. Do not alter State B as part of normal repetition.

## Acceptance algorithm

If Cycle 3 is not clean: NOT_READY.

Execute the configured three repetitions.

If any required run has identity mismatch: INVALID_EXPERIMENT.
If any required run is invalid: INVALID_EXPERIMENT.
If any required valid run is FAIL: REPRODUCIBILITY_NOT_ESTABLISHED.
If all required runs are PASS: REPRODUCED.

No hidden retry loop is permitted.

A fourth or later execution may be performed only as an explicitly configured additional observation; it cannot erase a failed required repetition.

## Identity requirements

Every repetition must match:

- test ID
- test version
- assertion contract
- State B identity
- source/state SHA
- relevant fixture/input identity
- control-condition identity

Execution IDs and snapshots MUST differ.

## Evidence requirements

Every accepted repetition requires:

- execution ID
- snapshot ID
- observation ID
- evidence package ID
- root hash
- artifact hashes
- state identity
- test identity
- result
- validity status

The aggregate Cycle 4 result must reference all repetition packages.

## Negative-control behavior

The implementation must explicitly support:

- one PASS + one FAIL -> REPRODUCIBILITY_NOT_ESTABLISHED
- test identity mismatch -> INVALID_EXPERIMENT
- state mutation -> INVALID_EXPERIMENT
- invalid evidence -> INVALID_EXPERIMENT
- missing evidence -> INVALID_EXPERIMENT
- changed assertion -> INVALID_EXPERIMENT
- omitted failed run -> INVALID_EXPERIMENT

## Scope

Cycle 4 establishes reproducibility only for the defined experiment and controlled fixture.

It does not establish general correctness, arbitrary-code safety, emergence, intelligence, M02 qualification, or authority.

## Constitutional boundary

REPRODUCED MUST NOT transition to AUTHORIZED.
