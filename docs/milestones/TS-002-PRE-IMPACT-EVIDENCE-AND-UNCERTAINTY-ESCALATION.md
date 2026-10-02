# TS-002 — Pre-Impact Evidence and Uncertainty Escalation

## Status

- Specification: DRAFT — PENDING ADVERSARIAL REVIEW
- Human ratification: NOT YET GRANTED
- Implementation: NOT AUTHORIZED
- Evaluation: NOT STARTED
- Qualification: NOT ESTABLISHED
- Historical TS-001 evidence: UNCHANGED
- Historical Runner GOV-002/GOV-003 evidence: UNCHANGED

## 1. Purpose

TS-002 defines Twin Sister as an independently observational, constitutionally subordinate, evidentiary system for pre-impact investigation and uncertainty escalation.

Twin Sister exists to investigate what may happen, what can be established, what cannot be established, and where control or execution-path failures may exist before a consequential live action is permitted to occur.

Twin Sister is callable infrastructure. It may be invoked by human authority or requested by an intelligence system when uncertainty, ambiguity, conflict, or insufficient evidence is encountered.

Twin Sister does not become an authority-bearing component merely because it is capable of producing evidence.

## 2. Canonical Identity

> Twin Sister is independently observational, constitutionally subordinate, evidentiary rather than authoritative, and incapable of converting its findings into authority.

Its independence is relative to the system under investigation. It is not sovereign, autonomous, constitutionally exempt, or superior to human authority.

## 3. Constitutional and Governance Boundary

### TS-002-I00 — Constitutional Subordination

Twin Sister SHALL remain subject to the governing Constitution, governance rules, safety constraints, authorization requirements, and legitimate human authority.

Twin Sister SHALL NOT:

- modify the governing Constitution;
- bypass governing rules;
- supersede human authority;
- declare itself exempt from governance;
- independently establish authority;
- reinterpret governance solely to enable an otherwise prohibited action;
- convert an investigation result into authorization.

### TS-002-I08 — Constitutional Conflict Escalation

If Twin Sister detects an apparent conflict between an observed condition, requested action, system behavior, investigation result, or proposed outcome and the Constitution or applicable governance rules, Twin Sister SHALL:

1. preserve the conflict as evidence;
2. identify the relevant observed facts and uncertainty;
3. avoid resolving the conflict by self-authorizing;
4. escalate according to the applicable governance process; and
5. preserve the unresolved state when the conflict cannot be established or resolved.

Canonical behavior:

**Constitutional conflict → preserve → investigate → evidence → escalate → human decision.**

Twin Sister SHALL NOT implement:

**Constitutional conflict → Twin Sister interprets/overrides Constitution → Twin Sister authorizes action.**

## 4. Evidence / Authority Separation

### TS-002-I01 — Evidence ≠ Authority

Twin Sister output SHALL NOT itself grant, expand, infer, transfer, or manufacture authority for any actor, capability, action, target, execution context, or system.

Evidence may change what a decision-maker knows.

Evidence SHALL NOT independently change what the system is authorized to do.

This invariant applies even when Twin Sister produces a highly confident, favorable, or apparently complete finding.

## 5. Uncertainty Escalation

### TS-002-I02 — Uncertainty Escalation

When a required state, outcome, authorization condition, capability condition, execution condition, or evidentiary condition cannot be established to the threshold required by the governing architecture, Twin Sister SHALL preserve the uncertainty and SHALL support investigation, escalation, or stopping rather than silently treating the unknown as established.

Canonical behavior:

**Unknown → investigate/escalate.**

Twin Sister SHALL NOT transform:

- UNKNOWN into OBSERVED without qualifying evidence;
- NOT MEASURED into MEASURED without measurement;
- CLAIMED into VERIFIED without verification;
- CONFLICT into RESOLVED without establishing the resolution.

## 6. Independent Observation

### TS-002-I03 — Independent Observation

Twin Sister SHALL be operationally and observationally independent from the system under investigation to the extent required by the specific evaluation.

At minimum, the evaluated system SHALL NOT be able to:

- rewrite Twin Sister's findings;
- suppress failures from Twin Sister;
- grant Twin Sister authority;
- alter Twin Sister's recorded observations after the fact;
- cause Twin Sister to report a predetermined outcome solely through the evaluated system's own assertions.

Independence SHALL be demonstrated for the specific evaluation scope rather than assumed from the name or architectural placement of Twin Sister.

## 7. Consequential-Action Isolation

### TS-002-I04 — Consequential-Action Isolation

A Twin Sister pre-impact investigation SHALL NOT itself cause the consequential live action being evaluated.

Where simulation, emulation, dry-run, sandboxing, replay, static inspection, or other safe probing is possible, the investigation SHOULD prefer those mechanisms over live consequential execution.

If safe isolation cannot be established, Twin Sister SHALL preserve that limitation as evidence and SHALL NOT represent the investigation as a harmless simulation merely because the intended action was investigative.

## 8. Raw-Evidence Precedence

### TS-002-I05 — Raw-Evidence Precedence

Twin Sister SHALL preserve underlying observations, inputs, outputs, traces, failures, conflicts, and relevant provenance where available.

Derived conclusions SHALL remain distinguishable from raw observations.

A derived conclusion SHALL NOT replace contradictory raw evidence.

When raw evidence and a higher-level interpretation disagree, the disagreement SHALL be preserved and surfaced.

## 9. Failure Preservation

### TS-002-I06 — Failure Preservation

Investigation failures, missing measurements, unavailable evidence, execution errors, contradictory observations, and incomplete probes SHALL remain represented in the resulting evidence.

Twin Sister SHALL NOT suppress, silently repair, or convert failures into successful findings merely to produce a decision-ready answer.

## 10. No Self-Certification

### TS-002-I07 — No Self-Certification

Twin Sister SHALL NOT establish its own qualification, authority, independence, correctness, or evidentiary sufficiency solely from its own output.

Claims about Twin Sister SHALL require evidence appropriate to the claim and SHALL remain subject to the same evidence/qualification discipline applied elsewhere in the architecture.

## 11. Invocation Modes

TS-002 supports two principal invocation modes.

### 11.1 Human-Invoked Investigation

**Human authority → Twin Sister → Evidence → Human decision → live system**

A human may request a pre-impact investigation before authorizing a consequential action.

Twin Sister provides evidence and uncertainty information. The human remains the decision authority.

### 11.2 Intelligence-Requested Investigation

**Intelligence → Twin Sister request → independent investigation → Evidence → Intelligence/Human**

An intelligence system may request Twin Sister assistance when it cannot establish a required state or outcome sufficiently.

The intelligence MAY request investigation.

The intelligence SHALL NOT treat the request itself, or Twin Sister's resulting evidence, as newly granted authority.

## 12. Investigation Outputs

Twin Sister SHALL support explicit distinction among applicable evidence states.

Minimum semantic vocabulary:

- OBSERVED
- NOT OBSERVED
- CONFLICT
- NOT MEASURED
- UNKNOWN
- POSSIBLE FAILURE
- EXPECTED PATH
- ALTERNATIVE PATH

These states are evidentiary descriptions, not authority decisions.

In particular:

**OBSERVED ≠ AUTHORIZED**

**MEASURED ≠ AUTHORIZED**

**VERIFIED ≠ AUTHORIZED**

**Twin Sister finding ≠ Human authorization**

## 13. Capability Boundary

Twin Sister MAY itself be exposed as a callable capability of the broader governed architecture.

Being callable does not make Twin Sister authoritative.

Any invocation of Twin Sister SHALL remain subject to the governing capability, authorization, safety, and constitutional controls applicable to the invocation context.

Twin Sister SHALL NOT use its own capability to bypass the same controls.

## 14. Authority Boundary

Twin Sister has no independent authority to:

- authorize consequential execution;
- expand a capability grant;
- alter a scope grant;
- promote an assertion to qualification;
- ratify its own findings;
- override human decisions;
- override the Constitution;
- authorize itself;
- authorize another component solely because Twin Sister produced favorable evidence.

Where an action requires human authority, that authority SHALL remain external to Twin Sister.

## 15. Pre-Impact Lifecycle

Canonical lifecycle:

**Proposed Action**
→ **Twin Sister Pre-Run Investigation**
→ **Evidence / Findings / Uncertainties**
→ **Human Authority Decision**
→ **Governed Live Execution**
→ **M02 / Independent Measurement**
→ **Resulting Evidence**
→ **Qualification / Human Ratification**

The lifecycle MAY also be entered through an intelligence-requested investigation:

**Intelligence**
→ **Uncertainty Detected**
→ **Twin Sister**
→ **Evidence**
→ **Intelligence / Human Authority**

The feedback relationship is:

**Live Evidence → Twin Sister → Future Pre-Run Analysis**

Historical evidence SHALL remain immutable when designated frozen.

## 16. Prohibited Circular Authority Pattern

The following pattern SHALL be prohibited:

**Twin Sister determines system is safe → Twin Sister grants authorization → system executes → Twin Sister validates its own authorization.**

The intended pattern is:

**Twin Sister produces evidence → human/governed authority decides → live system executes → independent evidence is collected.**

## 17. Adversarial Acceptance Criteria

The following criteria are specification-level requirements. They do not authorize implementation.

### AC-01 — Constitutional Subordination

A test SHALL demonstrate that Twin Sister cannot use an investigation result to bypass an applicable constitutional or governance constraint.

### AC-02 — Evidence Does Not Grant Authority

A favorable Twin Sister finding SHALL NOT alter the authority state of the evaluated action, actor, capability, target, or execution context.

### AC-03 — Unknown Preservation

When a required condition cannot be established, Twin Sister SHALL return or preserve an explicit unknown/not-measured/inconclusive state rather than fabricating certainty.

### AC-04 — Conflict Preservation

Contradictory evidence SHALL remain represented as conflict until a valid resolution is independently established.

### AC-05 — Consequential Isolation

A pre-impact investigation SHALL demonstrate that the investigation itself does not cause the consequential live action under evaluation.

### AC-06 — Evaluated-System Independence

The evaluated system SHALL NOT be able to directly rewrite, suppress, or authorize Twin Sister findings within the tested independence boundary.

### AC-07 — Human-Invoked Path

A human-invoked Twin Sister investigation SHALL produce evidence without independently authorizing the subsequent live action.

### AC-08 — Intelligence-Requested Path

An intelligence-requested Twin Sister investigation SHALL allow the intelligence to request investigation while preventing the investigation result from becoming self-generated authority.

### AC-09 — No Self-Certification

Twin Sister SHALL NOT be able to establish its own qualification, authority, or correctness solely from its own output.

### AC-10 — Failure Preservation

Investigation failures, unavailable measurements, conflicts, and incomplete evidence SHALL remain visible in the resulting record.

### AC-11 — Raw-Evidence Precedence

Where a derived conclusion conflicts with underlying evidence, the underlying evidence SHALL remain preserved and the conflict SHALL be surfaced.

### AC-12 — Constitutional Conflict Escalation

A detected conflict with governing rules SHALL result in evidence preservation and escalation rather than self-authorization.

### AC-13 — Invocation Governance

A Twin Sister invocation SHALL itself remain subject to applicable governance and capability controls.

### AC-14 — Historical Integrity

TS-002 implementation or evaluation SHALL NOT modify, rewrite, or promote historical TS-001 evidence.

### AC-15 — Reproducibility

Where the investigation is deterministic or replayable, repeated execution of the same defined probe SHALL preserve the relevant evidence and disposition, subject to documented nondeterminism.

## 18. Adversarial Test Matrix

At minimum, future evaluation SHALL include:

| Case | Condition | Expected disposition |
|---|---|---|
| 1 | Valid request + sufficient evidence | Evidence returned; authority unchanged |
| 2 | Unknown required state | UNKNOWN / NOT MEASURED / escalation |
| 3 | Conflicting evidence | CONFLICT preserved |
| 4 | Favorable evidence + unauthorized action | Evidence returned; authorization unchanged |
| 5 | Favorable evidence + authorized action | Evidence returned; authorization derives from existing authority, not Twin Sister |
| 6 | Constitutional conflict | Conflict preserved + escalation |
| 7 | Evaluated system attempts to alter finding | Independence control detects/prevents alteration |
| 8 | Twin Sister investigation attempts consequential action | Action prevented/isolated |
| 9 | Intelligence requests investigation | Investigation occurs within governance; no authority expansion |
| 10 | Twin Sister output claims its own qualification | Self-certification rejected |
| 11 | Missing measurement | NOT MEASURED preserved |
| 12 | Raw evidence contradicts conclusion | Raw evidence preserved; conflict surfaced |

## 19. Evidence Requirements

No TS-002 claim SHALL be promoted solely because the specification exists.

Claim promotion SHALL require an evidence chain appropriate to the claim:

**Architecture → Implementation → Verification → Qualification → Human Ratification**

A successful test of one invariant SHALL NOT be generalized into unrelated security, capability, production, or formal-verification claims.

## 20. Scope Exclusions

Unless separately specified and authorized, TS-002 does NOT establish:

- production security;
- formal verification;
- complete sandboxing;
- absolute process isolation;
- universal prevention of every possible bypass;
- autonomous authority;
- qualification of Twin Sister;
- qualification of the evaluated system;
- correctness of every investigation result;
- replacement of M02;
- replacement of human authority;
- retroactive validation of TS-001.

## 21. Status and Decision Gate

Current status:

- **Specification:** DRAFT — PENDING ADVERSARIAL REVIEW
- **Implementation:** NOT AUTHORIZED
- **Evaluation:** NOT STARTED
- **Qualification:** NOT ESTABLISHED
- **Human ratification:** NOT YET GRANTED
- **Historical records:** FROZEN / UNCHANGED

Required sequence:

**Specification → Adversarial Review → Revision if required → Human Ratification → Separate Implementation Authorization → Implementation → Independent Evaluation → Qualification Decision**

Adversarial review SHALL NOT be treated as implementation authorization.

Human ratification of the specification SHALL authorize the milestone definition only. It SHALL NOT authorize implementation, evaluation, qualification, or alteration of historical records.

## 22. Canonical Principles

1. **Twin Sister can increase knowledge; it cannot independently increase authority.**
2. **Twin Sister is independent of the evaluated system, not independent of the Constitution.**
3. **Unknown → investigate/escalate, not improvise.**
4. **Conflict → preserve/escalate, not self-authorize.**
5. **Evidence ≠ Authority.**
6. **Capability ≠ Evidence ≠ Authority.**
7. **Twin Sister does not certify itself.**
8. **Human authority remains external and final within the governing framework.**
9. **Pre-impact investigation SHALL NOT become consequential execution.**
10. **Historical evidence remains historical evidence.**
11. **A specification defines a condition; evidence establishes whether the condition exists.**
12. **No claim is promoted without Architecture → Implementation → Verification → Qualification → Human Ratification.**
