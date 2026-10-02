# RUNNER-GOV-003 — Capability-Constrained Execution
## Revision 1 — Ratified Specification

**Status:** RATIFIED — SPECIFICATION ONLY  
**Implementation:** NOT AUTHORIZED  
**Repository write:** AUTHORIZED FOR SPECIFICATION RECORD ONLY  
**Qualification:** NOT STARTED  
**Claim status:** NOT ESTABLISHED

**Human ratification:** Revision 1 ratified after adversarial specification review. This ratification approves the milestone definition only. It does not authorize implementation, evaluation, qualification, claim promotion, or alteration of historical artifacts.

**Historical boundaries (immutable):**
- External Evaluation Attempt 002 — FROZEN
- External Evaluation Attempt 003 — FROZEN
- RUNNER-GOV-002 (unauthorized execution prevention under evaluated designed public scope) — FROZEN

---

## 1. Claim

**RUNNER-GOV-003:**

A Runner execution request cannot proceed to the underlying executor unless:

1. the request carries an explicit required capability identity, and
2. that capability is authorized for the execution context by a distinct capability decision, and
3. the existing governance authorization decision also permits execution.

Capability authorization is a mandatory precondition to executor invocation. It does not replace governance authorization.

This claim does not assert that Runner is secure, production-ready, formally verified, or bypass-proof against arbitrary language-level introspection.

---

## 2. Definitions

### 2.1 Capability

A **capability** is a named, discrete unit of executable ability that the Runner may be asked to exercise (e.g. a tool class, operation class, or bounded skill id).

A capability is **not**:

- evidence
- authority
- an epistemic status
- a governance scope (`required_scope`)
- a qualification result

### 2.2 Capability identifier

**Type:** non-empty string (normalized: strip leading/trailing whitespace; empty after normalize is invalid).

**Field name (required on every governed execution request reaching the boundary):** `required_capability: str`

**Where it lives:**

- On the object that enters `GovernedExecutionBoundary.execute` (today’s analogue: extend the request model; do not rely on planner-only metadata).
- Plan/step layers may also carry it for planning, but **presence at the boundary request is mandatory**. Upstream omission is not a substitute for a boundary-level field.

### 2.3 Execution context

The **execution context** is the set of facts against which capability authorization is evaluated. At minimum it must include:

- `actor` (who/what is requesting)
- `capability_grants` (the set of capability identifiers authorized for this actor/run)
- optional: `run_id` / `objective_id` if grants are run-scoped

**Capability authorization** means:

`required_capability` is a member of `capability_grants` for that context after normalization.

Grants are **explicit**. They are not inferred from epistemic status, prior success, measurement confidence, or governance scope.

### 2.4 Relationship to `required_scope`

| Concept | Role |
|---|---|
| `required_scope` | Existing governance authorization dimension (e.g. `COGNITIVE_OPERATION`, `GOVERNANCE_CHANGE`) |
| `required_capability` | Distinct capability identity for capability-gate evaluation |

They are **orthogonal**:

- Satisfying `required_scope` does not authorize a capability.
- Holding a capability grant does not satisfy governance scope or protected-target rules.
- Implementation must not rename `required_scope` to “capability” or implement the capability gate solely inside the existing `authorize()` function without a **distinct** decision point.

### 2.5 Epistemic status (non-equivalence invariant)

If the system tracks capability epistemic states (including but not limited to CLAIMED, MEASURED, VERIFIED, or any analogous labels):

```
CLAIMED   ≠ AUTHORIZED
MEASURED  ≠ AUTHORIZED
VERIFIED  ≠ AUTHORIZED
```

Registration, measurement, verification, confidence scores, or evidence references **do not** constitute a capability grant. Only an explicit grant in the execution context does.

---

## 3. Distinct capability decision point

### 3.1 Requirement

There must be a **named, distinct** capability decision function or object, for example:

- `authorize_capability(required_capability, context) -> CapabilityDisposition`
- `CapabilityGate.evaluate(...)`

This decision must **not** be solely a branch inside the existing governance `authorize(request, authorization)` with no separable interface.

### 3.2 Capability dispositions (minimum)

| Disposition | Meaning |
|---|---|
| `CAPABILITY_ALLOW` | Capability identity valid and granted in context |
| `CAPABILITY_DENY` | Missing, empty, invalid, or not granted |

No success-shaped return is permitted for deny cases.

### 3.3 Placement

The capability decision must occur on **every designed public path** that can reach the underlying executor, including:

- `GovernedExecutionBoundary.execute` / `execute_step`
- Any kernel path that delegates to that boundary

It is **not sufficient** to check capability only in the planner or only in `ExecutionLoop` if a caller can invoke the boundary directly.

Recommended conjunction (either order is acceptable if both are mandatory and both can deny):

```
Execution request
      ↓
Capability identification (required_capability present and valid)
      ↓
Capability decision (grant check)
      ↓
Governance authorization (existing authorize())
      ↓
GovernedExecutionBoundary executor invocation (only if both ALLOW)
      ↓
Underlying executor
```

Short-circuit on capability DENY is allowed; governance may still be evaluated for evidence if desired, but executor invocation is forbidden.

---

## 4. Scope

**In scope**

- Capability identity on boundary-level requests
- Distinct capability decision
- Integration with existing GovernedExecutionBoundary
- Ordering/conjunction relative to executor invocation
- Authorized / missing / invalid / unauthorized capability behavior
- Independence from governance authorization
- Designed public API routes

**Out of scope (remain NOT ESTABLISHED unless separately claimed)**

- Production security
- Formal verification
- Process isolation
- Absolute protection against private-attribute / introspection bypass (Eval 003 residual)
- Kronos / M02 integration
- Mandatory Observe → Verify → Evidence loop
- Human authority qualification
- General AI safety

---

## 5. Threat model for this milestone

**Failure mode under test:**

A request reaches the underlying executor even though the required capability was absent, invalid, or not granted in the execution context.

**Property under test:**

Capability decision before (or otherwise strictly prior to) executor invocation, conjunctive with governance authorization.

This is **not** a re-test of “does `authorize()` still block unauthorized governance?”

---

## 6. Acceptance criteria

### AC-01 — Explicit capability identity

Every governed execution request that can reach the executor path must carry a normalized non-empty `required_capability`.

**Evidence:** source inspection + runtime tests (missing/empty → no executor call).

### AC-02 — Distinct mandatory capability evaluation

A distinct capability decision point is invoked on every designed public path to the executor, before executor invocation.

**Evidence:** source inspection (named decision site) + instrumentation.

### AC-03 — Missing / empty / invalid capability fails closed

Missing field, empty string, whitespace-only, or otherwise invalid capability identity → executor invocations = 0.

No alternate “safe success” outcome that performs execution.

### AC-04 — Unauthorized capability fails closed

Valid identity not in `capability_grants` for the context → executor invocations = 0.

### AC-05 — Authorized capability may proceed to governance

Valid granted capability does not by itself execute; it only allows the request to be subject to existing governance rules.

When capability ALLOW **and** governance ALLOW (non-protected, correct scope, etc.) → executor invocations = 1.

When capability ALLOW **and** governance REJECT/ESCALATE → executor invocations = 0.

### AC-06 — Designed-path non-bypass

Every designed public execution route encounters the capability decision before executor invocation.

(Private-attribute residual on `_tool_executor` remains a known limitation per Eval 003; out of scope to close here unless separately authorized.)

### AC-07 — Governance remains mandatory

Capability ALLOW does not create unrestricted execution.

Governance authorization remains required.

Controls are conjunctive, not substitutive.

### AC-08 — Epistemic status does not authorize

CLAIMED, MEASURED, VERIFIED (or analogous) without an explicit grant → executor invocations = 0 even if governance would otherwise ALLOW.

### AC-09 — Instrumented control matrix

At minimum, instrument the underlying executor for:

| # | Capability condition | Governance condition | Expected calls |
|---|---|---|---:|
| 1 | ALLOW (granted) | ALLOW | 1 |
| 2 | DENY (not granted) | ALLOW | 0 |
| 3 | ALLOW | REJECT | 0 |
| 4 | ALLOW | ESCALATE (e.g. protected target) | 0 |
| 5 | DENY | REJECT | 0 |
| 6 | DENY | ESCALATE | 0 |
| 7 | CLAIMED only (no grant) | ALLOW | 0 |
| 8 | MEASURED but unauthorized | ALLOW | 0 |
| 9 | VERIFIED but unauthorized | ALLOW | 0 |
| 10 | Grant for A, request B | ALLOW | 0 |
| 11 | Missing / empty capability | ALLOW | 0 |

Cases 2 and 3 are the primary discriminators against collapsing into RUNNER-GOV-002.

### AC-10 — Regression preservation

Existing v0.1.1 suite baseline: **33/33 passed**.

Regressions must be recorded, not silently fixed during evaluation.

### AC-11 — Provenance of evaluation

Record:

- repository
- branch
- commit SHA
- date
- environment
- commands
- files inspected
- instrumentation method

---

## 7. Required source inspection

Evaluator must trace:

```
Request → capability id present? → capability decision → governance authorize() → boundary → executor
```

And report:

- All designed paths to the executor
- Whether capability decision is distinct and unavoidable on those paths
- Whether `required_scope` was reused as a stand-in for capability
- Whether epistemic APIs can open an execution path without a grant
- Direct executor references / DI / private attributes (document residual if unchanged)

---

## 8. Required runtime evidence

- Negative cases: observed executor calls = 0
- Positive control (capability ALLOW ∧ governance ALLOW): observed executor calls = 1
- Prefer instrumentation of the real executor callable over return-value-only assertions

---

## 9. Evidence package (when evaluated)

1. This specification (Revision 1 or later frozen text)
2. Implementation commit(s) (if any; none under this document alone)
3. Evaluated commit SHA
4. Test results
5. Instrumentation table (AC-09)
6. Source / path inspection
7. Positive and negative controls
8. Regression results
9. Known limitations
10. Evaluator disposition
11. Cross-review disposition

Eval 002 / 003 artifacts remain frozen and are not rewritten.

---

## 10. Promotion rule

| Disposition | When |
|---|---|
| **ESTABLISHED** | All applicable ACs demonstrated within defined scope |
| **PARTIALLY ESTABLISHED** | Material subset demonstrated; specific gaps named |
| **NOT ESTABLISHED** | Implementation or tests exist but claim not shown |
| **NOT MEASURED** | Required criterion not evaluated |

Passing tests alone do not equal ESTABLISHED.

Passing only governance tests does not equal capability enforcement.

---

## 11. Failure / rollback

If any AC fails:

1. Record failure as evidence
2. Preserve evaluated commit
3. Identify failed AC
4. Classify: implementation / specification / harness
5. Human engineering decision before corrective change
6. Re-evaluate against the frozen failure boundary

Do not silently modify until green.

---

## 12. Independence requirement

The evaluation must answer:

> Did we demonstrate capability enforcement, or only that the existing authorization boundary still works?

Mandatory discriminating evidence includes:

- governance ALLOW ∧ capability DENY → calls = 0
- governance REJECT ∧ capability ALLOW → calls = 0

---

## 13. Decision gate

```
Specification Rev 1 → Adversarial re-review → Human ratification
    → (optional) freeze text into repository as documentation only
    → separate explicit decision: IMPLEMENTATION AUTHORIZED — RUNNER-GOV-003
    → implementation → independent evaluation → cross-review → disposition → freeze
```

**Current position:** Revision 1 has been human-ratified as the specification-only milestone definition.

**This document does not authorize implementation, evaluation, qualification, claim promotion, or alteration of historical artifacts.**
