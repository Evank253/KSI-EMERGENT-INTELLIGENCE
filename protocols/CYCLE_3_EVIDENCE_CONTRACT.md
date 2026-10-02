# Cycle 3 — Canonical Evidence Contract

## Purpose

This contract defines the minimum evidence structure required for the controlled Cycle 3 repair-effect claim.

Cycle 3 tests a mechanism:

> Can an authorized state transition cause the same defined test to move from FAIL to PASS under matched evaluation conditions?

The contract does not establish that a real repository defect was repaired, that arbitrary code execution is safe, that the system is intelligent, that emergence occurred, or that any authority exists.

## Canonical evidence chain

PACKAGE A → AUTHORIZED REPAIR → STATE B → PACKAGE B → A ↔ B COMPARISON

Runtime observations attach to the experiment but are descriptive measurements, not automatic causal proof.

## Package A — baseline

Package A MUST be sealed as SEALED_REPAIR_EFFECT_BASELINE.

It must contain package ID/root hash, source/state identity, snapshot ID, execution ID, observation ID, test ID/version, state ID/sequence, observed result = FAIL, artifact hashes, and validity status.

Package A becomes immutable after sealing.

## Repair transition

The repair MUST contain repair ID, authorized actor, authorization scope, change reason, parent package ID, parent state ID, new state ID, and new source/state identity.

The transition must create a distinct state identity. No distinct state means no repair-effect experiment.

## Package B — retest

Package B MUST be independently created and sealed as SEALED_REPAIR_EFFECT_RETEST.

Package B MUST explicitly reference Package A, the repair, and State B.

Package B MUST preserve the exact same test ID, test version, and assertion/evaluation contract. Package B must contain observed result = PASS.

A generic constitutional package without Cycle 3 predecessor/repair/state lineage does not satisfy this contract, even if another part of the system reports FAIL → PASS.

## A ↔ B comparison

The comparison MUST contain A/B package IDs, root hashes, source/state identities, source/package/root change indicators, same-test-identity assertion, before = FAIL, after = PASS, repair-effect disposition, qualification state, and authority state.

The comparison is invalid if it is null or if any required identity cannot be reconstructed.

## Runtime observations

Cycle 3 should attach runtime-before and runtime-after observations where the runtime measurement is part of the configured experiment.

These measurements describe observed system state. They do not establish causality merely because values differ.

## Evidence states

OBSERVED means the required experiment fields are present, integrity checks pass, lineage is reconstructable, and the controlled fixture records the defined FAIL → PASS transition.

EVIDENCE_INSUFFICIENT means required evidence is missing or cannot be verified.

TEST_IDENTITY_MISMATCH means the test ID, version, assertion, or evaluation contract differs between A and B.

LINEAGE_INCOMPLETE means Package B, repair, or state lineage cannot be reconstructed.

AUTHORIZATION_FAILURE means the state transition lacks required authorization.

## Qualification boundary

Cycle 3 may establish an observed repair-effect mechanism within its defined scope. It cannot establish qualification. M02 independent evaluation remains required.

## Authority boundary

No Cycle 3 disposition may grant authority. Human authority remains external and superior to the experimental system.
