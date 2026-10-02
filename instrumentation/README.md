# M02 — Independent Measurement & Evaluation Infrastructure

This package implements the frozen Milestone 02 instrumentation contract for KSI Emergent Intelligence.

Core invariant: instrumentation observes and evaluates the system under test; it does not modify the system under test and cannot self-authorize or self-qualify an emergence result.

Pipeline:

EXPERIMENT → EXECUTION → ARTIFACT → MEASUREMENT → EVIDENCE → QUALIFICATION

Qualification never grants authority.

## Scope

- canonical experiment records
- immutable identifiers
- SHA-256 provenance and lineage
- controlled configuration capture
- baseline/composition runner contracts
- independent evaluation
- explicit qualification state machine
- tamper-evident evidence records
- automated acceptance tests

The implementation uses only the Python standard library.
