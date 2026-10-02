# Cycle 4 — Reproducible Repair Protocol

## Purpose

Cycle 4 tests whether the repaired state demonstrated by Cycle 3 produces the same defined PASS outcome repeatedly under controlled, matched evaluation conditions.

Cycle 4 does not establish general software correctness, intelligence, emergence, qualification, or authority.

## Governing question

> Does the repaired state reproduce the same PASS result independently across repeated executions of the same test identity, version, assertion, and evaluation conditions?

## Preconditions

Cycle 4 may begin only when Cycle 3 provides:

- sealed baseline evidence package A;
- authorized repair transition;
- distinct state B;
- sealed repair-effect retest package B;
- identical test identity/version before and after;
- observed FAIL → PASS transition;
- complete predecessor and repair lineage;
- immutable evidence package identifiers and hashes.

If any precondition is absent, Cycle 4 status is NOT_READY.

## Experimental design

~~~
PACKAGE A
  ↓
AUTHORIZED REPAIR
  ↓
STATE B
  ↓
TEST-X v1.0 → PASS #1
  ↓
TEST-X v1.0 → PASS #2
  ↓
TEST-X v1.0 → PASS #3
  ↓
REPRODUCIBILITY COMPARISON
~~~

The repaired state must be fixed for the repeated evaluations. Repeated runs must not silently create materially different repaired states.

## Test identity invariants

Every repetition MUST preserve:

- test_id
- test_version
- assertion identity
- evaluation contract
- expected PASS condition
- relevant fixture/input identity
- evaluation environment contract
- state B identity

A changed test is a different experiment, not a reproduction.

## Required observations

Each repetition records:

- execution ID
- snapshot ID
- state ID
- source/state identity
- test ID/version
- execution status
- observed result
- observation ID
- artifact IDs/hashes
- timing/resource observations where available
- network policy
- secret-access result
- evidence package ID/root hash
- predecessor/reference lineage
- validity status

## Reproducibility rule

A Cycle 4 result is REPRODUCED only when the configured replication threshold is met and every accepted repetition:

1. evaluates the same test identity/version;
2. evaluates the same assertion contract;
3. executes against the same repaired-state identity;
4. produces PASS;
5. produces independently recorded observations;
6. produces valid, immutable evidence;
7. contains no invalidated execution;
8. contains no unexplained material condition change.

Default controlled-fixture threshold: 3 independent PASS executions.

The threshold is an experimental parameter, not a universal scientific law. Any change to it must be recorded in the experiment definition.

## Negative outcomes

- Any FAIL during a required repetition → REPRODUCIBILITY_NOT_ESTABLISHED.
- Invalid execution → repetition rejected; do not count it as PASS or FAIL evidence.
- Changed test identity/version → TEST_IDENTITY_MISMATCH.
- Changed state identity → STATE_IDENTITY_MISMATCH.
- Missing evidence → EVIDENCE_INSUFFICIENT.
- Evidence mutation → EVIDENCE_INTEGRITY_FAILURE.
- Unexplained environment change → CONTROL_CONDITION_MISMATCH.

A negative result remains evidence. The system MUST NOT retry indefinitely until PASS and then discard failures.

## Disposition

Cycle 4 may produce:

- NOT_READY
- REPRODUCIBILITY_NOT_ESTABLISHED
- REPRODUCED
- INVALID_EXPERIMENT

REPRODUCED means the defined experimental claim was reproduced. It does not mean the underlying implementation is universally correct.

## Qualification boundary

Cycle 4 alone cannot transition to QUALIFIED_CAPABILITY, EMERGENT_CAPABILITY, AUTHORIZED, or any expanded authority state.

Qualification remains an M02/external-evaluation concern under the constitutional boundary.

## Authority boundary

Capability → evidence → reproducibility does not imply authority.

Human authority remains external and superior to the experimental system.
