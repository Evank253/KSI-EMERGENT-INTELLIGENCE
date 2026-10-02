# RUNNER-GOV-003 — Implementation Record

## Status

**IMPLEMENTED — INDEPENDENT VERIFICATION PENDING**

This record documents the implementation performed after human authorization commit:

- Authorization: `1d59b0d3103ddf13fdbbbdcf73b083204f0400e3`
- Prior implementation baseline: `d59a9ca1415b786dc9639037f227b773e71f4340`
- Current implementation head: `87e9a445f5dc19ef8107b8276735ca5ba70c6195`

The implementation remains scoped to the ratified GOV-003 specification. No bridge deployment or B-001 integration is authorized by this record.

## Implemented control

Execution now follows:

```
ActionRequest
    ↓
Distinct Capability Gate
    ↓
Governance Authorization
    ↓
Executor
```

The capability gate is a dedicated enforcement component and does not consult CapabilityAwareness status, evidence, confidence, or governance scope.

Missing, empty, whitespace-only, or invalid capability identity fails closed.

Explicit capability grants live only in the injected `CapabilityContext`. They are evaluated independently from governance authorization.

## Files changed

1. `runner/governance/capability_gate.py`
   - Added the named distinct `authorize_capability(required_capability, context)` decision point.
2. `runner/governance/capability_context.py`
   - Added explicit execution context with actor, capability grants, and optional run ID.
3. `runner/governance/gateway.py`
   - Added `required_capability` to `ActionRequest`.
   - Capability grants are not stored in `Authorization`; they remain in the separate capability context.
4. `runner/governance/execution_boundary.py`
   - Invokes the distinct capability gate before governance authorization.
   - Executor invocation requires both gates to ALLOW.
   - ExecutionDecision records capability disposition separately.
5. `runner/kernel/planner.py`
   - Carries the required capability on the existing plan step.
6. `runner/kernel/runner.py`
   - Injects the explicit capability context alongside the executor.
7. `runner/tests/test_capability_gate.py`
   - Covers fail-closed inputs, explicit grants, awareness non-authority, executor blocking, and distinct gate invocation.
8. `runner/tests/test_execution_matrix.py`
   - Covers the GOV-003 matrix, including the AC-09 discriminating pairs.
9. `runner/tests/test_kernel.py`
   - Supplies an explicit capability context for the authorized kernel path.
10. `runner/capability/gate.py`
   - Removed as the superseded combined gate/context implementation.

## Implementation commits

Sequential commits after the earlier GOV-003 implementation record:

- `b5e5a3f63b7dff1936873177ac446b9948c7053e` — add explicit capability execution context
- `c8dd81ab891829dc3f6e16780af64f67b7f4a99c` — add distinct capability authorization gate
- `6bc3346b20a99c8152c97eb3aea804e64e1d8a04` — use distinct capability context and gate
- `fa8897c18b3770106405caff22225213d1bb98bd` — inject explicit capability context
- `45701bdcd28196923b7e539458e9930bfd3029e3` — align capability gate tests with split governance modules
- `5ab63dc328f13717a63020e458b7f6f852995fe6` — add AC-09 discriminating execution matrix
- `74c47269015b43ab4ac4b5731c8ab6a2585b2131` — provide explicit capability context in kernel tests
- `dd40a4da09cca25839f6ae3894a784091f025f2f` — remove superseded capability gate module
- `d35297b3891f1234f0996ec83c7a1518441d90d7` — cover execute_step capability-gate path
- `c56c21ca7ef95dfb9d3915e3ac6150182d8a5631` — use separate capability context in gate tests
- `995e12f8652f2e5fe8fe31a9cfed0127fa00aa1f` — keep matrix capability grants in context
- `87e9a445f5dc19ef8107b8276735ca5ba70c6195` — keep kernel governance authorization separate from capability context

## Evidence status

### Static implementation evidence

The requested distinct gate/context separation is present in the live branch. The existing `runner/governance/execution_boundary.py` remains the single designed executor boundary; no duplicate `runner/kernel/execution_boundary.py` was created.

### Runtime evidence

**NOT YET ESTABLISHED BY AN INDEPENDENT EVALUATOR.**

No 33/33 regression result, executor call count, or adversarial disposition is asserted here.

### Local test execution

A local attempt to reconstruct and execute the suite remains blocked because this environment cannot resolve `raw.githubusercontent.com`. Therefore this record does not claim local test execution.

## Required next evidence

Independent evaluation should specifically inspect:

- distinct gate invocation on every designed execution path
- missing/empty/invalid capability
- missing/unauthorized capability
- governance ALLOW + capability DENY
- capability ALLOW + governance REJECT/ESCALATE
- CLAIMED/MEASURED/VERIFIED without explicit grant
- AC-09 full matrix
- AC-10 regression suite and exact pass/fail count
- instrumented executor invocation counts
- static call graph
- residual/private-reference limitations

## Explicit non-claims

This implementation does not claim:

- hardening of the `_tool_executor` private residual identified by Eval 003
- capability gating on planner-only paths beyond the execution boundary
- Kronos/M02 integration
- Observe→Verify→Evidence runtime loop
- qualification or production security
- bridge deployment or B-001 authorization

## Disposition boundary

Until independent verification produces evidence and a human disposition:

- GOV-003 qualification: **NOT ESTABLISHED**
- GOV-003 ratification: specification remains ratified
- Implementation: **present**
- B-001 bridge: **NOT AUTHORIZED**
- Bridge deployment: **NOT AUTHORIZED**
