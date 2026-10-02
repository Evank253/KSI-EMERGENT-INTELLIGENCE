# RUNNER-GOV-003 — Implementation Record

## Status

**IMPLEMENTED — INDEPENDENT VERIFICATION PENDING**

This record documents the implementation performed after human authorization commit:

- Authorization: `1d59b0d3103ddf13fdbbbdcf73b083204f0400e3`
- Implementation head: `d59a9ca1415b786dc9639037f227b773e71f4340`

The implementation is scoped to the ratified GOV-003 specification. No bridge deployment or B-001 integration is authorized by this record.

## Implemented control

Execution now follows:

```
ActionRequest
    ↓
Capability Gate
    ↓
Governance Authorization
    ↓
Executor
```

The capability gate is a dedicated enforcement component and does not consult CapabilityAwareness status, evidence, confidence, or governance scope.

Missing, empty, or whitespace-only capability identity fails closed.

Explicit capability grants are supplied through the execution authorization context and are evaluated independently from governance authorization.

## Files changed

1. `runner/capability/gate.py`
   - Added independent capability gate.
2. `runner/governance/gateway.py`
   - Added explicit capability grants to execution authorization context.
   - Added required capability identity to ActionRequest, with an empty default that the capability gate rejects.
3. `runner/governance/execution_boundary.py`
   - Enforced capability gate before governance authorization.
   - Executor invocation remains behind both gates.
   - ExecutionDecision records capability disposition separately.
4. `runner/kernel/planner.py`
   - Added required capability to PlanStep.
   - Planner assigns `ANALYZE_OBJECTIVE` to the existing analysis step.
5. `runner/tests/test_capability_gate.py`
   - Added capability gate, fail-closed, non-authority, ordering, and executor-blocking tests.
6. `runner/tests/test_execution_matrix.py`
   - Updated matrix for capability enforcement and added substitution/missing-capability cases.
7. `runner/tests/test_kernel.py`
   - Updated kernel regression for explicit capability grant.

## Implementation commits

The GitHub Contents API produced sequential commits:

- `088f412ead0d597bb865d733b260f4730e26c195` — add capability gate
- `ff59bcc51b73c4fa80fc82662e156b8f7ce86731` — add capability grants to Authorization/ActionRequest
- `fcc8b5e519fd80634c39d3040d7bee9ba29c61b7` — enforce capability gate at execution boundary
- `92c8b05ce8599ad2270c4bade822f43a69f94bed` — require capability on planned steps
- `f84ee49123670f44f66c2b076375ee950ee77502` — preserve fail-closed legacy request behavior
- `f35bfb1ad27fc561e723403f7ef03794afed0306` — preserve fail-closed plan-step behavior
- `5a7ee89a5ed93a267f10e09ed10f6885aff4210f` — add GOV-003 capability tests
- `320497342fe60932f73d0788c9890ca8773df9d6` — update execution matrix
- `d59a9ca1415b786dc9639037f227b773e71f4340` — update kernel regression

## Evidence status

### Static implementation evidence

The post-authorization comparison is ahead by 9 commits and reports the expected GOV-003 file changes. The sole underlying executor invocation remains in `GovernedExecutionBoundary.execute`, after both enforcement stages.

### Runtime evidence

**NOT YET ESTABLISHED BY AN INDEPENDENT EVALUATOR.**

No test pass count, instrumented executor count, or adversarial pass/fail disposition is asserted here.

### Local test execution

A local attempt to reconstruct and execute the suite was blocked because this environment cannot resolve `raw.githubusercontent.com`. Therefore this record does not claim local test execution.

## Required next evidence

Independent evaluation should specifically inspect:

- direct boundary invocation
- Runner/kernel path
- ExecutionLoop path
- alternate executor references
- missing/invalid capability
- capability substitution
- governance ALLOW + capability DENY
- capability ALLOW + governance REJECT
- existing GOV-002 regression behavior
- instrumented executor invocation counts
- static call graph
- residual/private-reference limitations

## Disposition boundary

Until independent verification produces evidence and a human disposition:

- GOV-003 qualification: **NOT ESTABLISHED**
- GOV-003 ratification: specification remains ratified
- Implementation: **present**
- B-001 bridge: **NOT AUTHORIZED**
- Bridge deployment: **NOT AUTHORIZED**
