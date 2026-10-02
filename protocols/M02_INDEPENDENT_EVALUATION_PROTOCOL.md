# M02 — Independent Evaluation Protocol

## Purpose

M02 is the independent measurement, evaluation, replication, and qualification layer for the intelligence ecosystem.

M02 evaluates evidence produced by the system under test and its execution/control infrastructure without becoming an authority source for the system itself.

## Independence invariant

> The system that performs an operation cannot be the sole authority establishing that the operation successfully proves the claim.

M02 MUST NOT silently modify the system under test, its source, its evidence history, its test definition, or its authority boundaries.

## Trust boundary

~~~
SYSTEM / KRONOS
      ↓
immutable evidence package
      ↓
M02 intake
      ↓
integrity + provenance validation
      ↓
independent evaluation
      ↓
replication
      ↓
comparison
      ↓
qualification disposition
~~~

The direction of evidence flow does not create authority flow.

## M02 inputs

M02 accepts an evidence package containing, at minimum:

- experiment ID
- claim ID
- test ID/version
- assertion/evaluation contract
- source/state identity
- snapshot identity
- execution identity
- observation identity
- artifact identity and hashes
- evidence package ID/root hash
- lineage/predecessor references
- authorization metadata for consequential transitions
- environment/control-condition metadata
- validity and invalidation records

M02 MUST reject packages whose integrity or required provenance cannot be established.

## M02 processing stages

### 1. Intake

Record immutable receipt metadata and calculate/verify package integrity.

### 2. Provenance validation

Verify source identity, snapshot identity, execution binding, package lineage, artifact hashes, test identity/version, and authorization records where required.

### 3. Claim reconstruction

Reconstruct the exact claim being evaluated without strengthening or weakening it.

### 4. Independent evaluation

Evaluate the evidence against the predefined acceptance criteria.

M02 MUST NOT change the acceptance criteria after observing the outcome unless that change is itself recorded as a new experiment.

### 5. Replication

Where required, execute or commission independent replication under the same defined conditions.

### 6. Baseline comparison

For emergence/composition claims, compare constituent systems independently, pairwise compositions where relevant, and the target composition under matched conditions.

### 7. Qualification disposition

Return a bounded evidence disposition.

## Qualification states

M02 may return:

- EVIDENCE_INSUFFICIENT
- REPLICATION_REQUIRED
- REPLICATION_FAILED
- CLAIM_SUPPORTED_WITHIN_DEFINED_SCOPE
- CLAIM_NOT_SUPPORTED
- INVALID_EVIDENCE

These dispositions describe the evidence state. They do not grant system authority.

## Anti-self-certification controls

M02 MUST reject or escalate attempts where:

- the system under test modifies its own qualification status;
- the system under test changes M02 acceptance criteria;
- evidence is rewritten after observation;
- a qualifying result is generated without independent observation;
- a capability claim is converted directly into authority;
- an emergent capability attempts self-authorization.

## Constitutional boundary

M02 inherits KSH-CONSTITUTION-001 v1.0.0.

The following implications are forbidden:

~~~
capability → authority
emergence → authority
qualification → authority
performance → authority
self-certification → authority
~~~

Any authority-boundary modification is a governance event requiring human authority.

## M02 non-interference rule

M02 may read evidence, validate integrity, reproduce tests under authorized conditions, record observations, compare outcomes, reject insufficient evidence, and issue bounded qualification dispositions.

M02 may not rewrite historical evidence, silently modify the system under test, silently modify test definitions, grant itself governance authority, grant the evaluated system authority, or erase failed replications.

## Required audit trail

Every M02 evaluation records:

- evaluator identity;
- input evidence package IDs;
- package/root hashes;
- evaluation protocol version;
- acceptance criteria version;
- replication executions;
- rejected/invalid evidence;
- comparison results;
- final disposition;
- timestamp;
- constitutional status;
- authority-granted = false unless a separate human governance action exists outside M02.

## Separation of concerns

Kronos answers:

> What happened during controlled execution, and can we prove the execution record?

M02 answers:

> Does the supplied evidence satisfy the predefined evaluation and replication requirements?

Neither answers:

> May the system govern itself?

That remains outside the system and under human authority.
