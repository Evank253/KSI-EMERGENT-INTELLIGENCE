# Cycle 3/4 Adversarial Test Matrix

This matrix defines negative controls before implementation. A failed negative control is an engineering failure, not a reason to weaken the acceptance rule.

| ID | Adversarial condition | Required disposition |
|---|---|---|
| ADV-001 | Test ID changed between A and B | REJECT |
| ADV-002 | Test version changed between A and B | REJECT |
| ADV-003 | Assertion contract changed | REJECT |
| ADV-004 | Package B omits predecessor | REJECT |
| ADV-005 | Package A reused as Package B | REJECT |
| ADV-006 | State A reused as State B | REJECT |
| ADV-007 | PASS asserted without execution | REJECT |
| ADV-008 | Evidence mutated after sealing | REJECT |
| ADV-009 | Repair executed without required authorization | REJECT |
| ADV-010 | PASS once, FAIL on required replication | REPRODUCIBILITY_NOT_ESTABLISHED |
| ADV-011 | Replication changes state identity | REJECT |
| ADV-012 | Replication changes evaluation conditions without declaration | CONTROL_CONDITION_MISMATCH |
| ADV-013 | Invalid execution presented as qualifying evidence | REJECT |
| ADV-014 | M02 modifies the system under test | REJECT |
| ADV-015 | M02 rewrites historical evidence | REJECT |
| ADV-016 | M02 acceptance criteria changed after outcome | REJECT / NEW_EXPERIMENT |
| ADV-017 | Qualified capability requests authority | GOVERNANCE_ESCALATION |
| ADV-018 | Emergent capability self-authorizes | REJECT |
| ADV-019 | Qualification status is self-written by evaluated system | REJECT |
| ADV-020 | Failed replication is omitted from final package | REJECT |

## Invariant

No adversarial failure may be converted into PASS by changing the definition after the result is observed.

## Qualification boundary

Passing this matrix establishes robustness of the evidence-control mechanism. It does not itself establish emergence or grant authority.
