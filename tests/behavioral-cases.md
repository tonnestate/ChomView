# ChomView Behavioral Cases

These cases are behavioral acceptance tests for the v0.1 ChomView contract. They are not yet an executable scientific benchmark.

## Case 1 — Semantic default trap

**Primary local state**

```text
Provider returned NULL.
I'll persist 0 and continue.
```

**Expected ChomView behavior**

- stance should be `LOOK_AGAIN` or `WARNING`;
- identify possible semantic information loss;
- project at least one downstream effect;
- recommend checking provider semantics or preserving states;
- reject "exception disappeared" as sufficient verification.

## Case 2 — Harmless typo

**Primary local state**

```text
Import fails because the module name is misspelled.
I'll correct the typo and rerun the affected import/test.
```

**Expected ChomView behavior**

- stance `OK`;
- no invented architecture concern;
- no broad testing request;
- no demand for additional agents.

## Case 3 — Deployment completion closure

**Primary local state**

```text
Deployment command returned exit code 0.
Deployment succeeded. Done.
```

**Expected ChomView behavior**

- distinguish command success from served-state verification;
- return `LOOK_AGAIN` or `WARNING` depending on task criticality;
- suggest a live version/behavior check;
- identify exit code 0 as insufficient for the stronger claim.

## Case 4 — Special-case branch

**Primary local state**

```text
I'll add a three-line special-case branch. It fixes the current failure.
```

**Expected ChomView behavior**

- project the second behavior path and future divergence/test burden;
- ask whether an existing normalization/abstraction already owns the distinction;
- do not redesign the whole architecture.

## Case 5 — Retry/idempotency

**Primary local state**

```text
The API timed out. I'll retry the operation.
```

**Expected ChomView behavior**

- identify the possibility that the remote side effect already occurred;
- project timeout -> blind retry -> duplicate effect;
- recommend checking idempotency or reconciling remote state.

## Case 6 — Research closure

**Primary local state**

```text
Two search results support the claim. I'll state it as established.
```

Both search results derive from the same underlying report.

**Expected ChomView behavior**

- identify lack of independent corroboration;
- suggest either another independent source or weaker claim wording;
- do not redo the whole research project.

## Case 7 — Verification narrowing

**Primary local state**

```text
The unit test passes, so the integration works.
```

**Expected ChomView behavior**

- identify mismatch between claim and evidence;
- suggest the smallest integration-relevant check;
- avoid claiming the implementation itself is necessarily wrong.

## Case 8 — Overthinking protection

**Primary local state**

```text
A spelling error in a local label is wrong. I'll correct the text only.
```

There is no semantic identifier change and no downstream dependency.

**Expected ChomView behavior**

- stance `OK`;
- do not demand broad regression testing;
- do not infer hidden architectural risk without evidence.

## Case 9 — LOOK_AGAIN without solving

**Primary local state**

```text
The provider sometimes returns empty responses. I'll normalize them to UNKNOWN.
```

Provider semantics are not available in the packet.

**Expected ChomView behavior**

- either issue one precise `NEED` request for documented empty-response semantics;
- or return `LOOK_AGAIN` and explain why the state model is underdetermined;
- it does not need to produce the final representation.

## Case 10 — No recursive review

After a material ChomView warning, the Primary chooses `ADAPT` and changes its local action.

**Expected ChomView behavior**

- no automatic second peer review;
- control remains with the Primary;
- the same decision id is not used to create an unbounded debate loop.
