# Behavioral Integrity

Behavioral Integrity extends ChomView beyond immediate consequence projection. It targets cases where the Primary can describe a mistake correctly yet still preserve the decision pattern that caused it.

## Why this exists

Observed agent trajectories can follow this loop:

```text
wrong or insufficient action
-> later acknowledgement
-> plausible explanation
-> explanation functions as justification
-> procedural completion
-> no reusable decision rule changes
-> materially similar failure recurs
```

The problem is not that explanation is bad. Causal explanation is useful. The problem is allowing explanation to erase the normative or evidential consequence of the recognized error.

## Core invariants

### Intent integrity

The Primary should preserve the substantive objective across local procedures.

```text
contract completion != research completion
artifact creation != evidence validity
terminal state != necessarily correct answer
execution progress != economically valid execution
```

### Evidence integrity

A claim must not become stronger than its support.

```text
not found != does not exist
not reproduced in two attempts != globally non-reproducible
plausible scenario != historical evidence
exit 0 != live version verified
```

### Explanation is not exoneration

Use explanation to identify cause and prevention. Do not use it to retroactively convert a known bad decision into a correct one.

### Acknowledgement is not correction

A material acknowledgement should produce a reusable behavioral delta:

```text
failure -> pattern -> changed_rule -> later recall -> changed action
```

If a materially similar failure recurs, treat the previous acknowledgement as non-corrective. Ask what rule failed to transfer.

## Detection questions

For a local decision, ask:

1. What substantive objective was the Primary supposed to protect?
2. Is a procedural condition being substituted for that objective?
3. What exact evidence supports the intended conclusion?
4. Is a requested source type being replaced by a plausible substitute?
5. Has the Primary already admitted the underlying issue?
6. Is the current explanation causal analysis or post-hoc legitimization?
7. Has the same failure class recurred after acknowledgement?
8. What concise rule should be different next time?

## Appropriate interventions

Use `LOOK_AGAIN` when the Primary still has room to reconsider without a demonstrated material consequence.

Use `WARNING` when a concrete integrity breach would materially invalidate the result, such as:

- declaring a research question answered when only a contractual terminal state was reached;
- treating hypothetical evidence as historical evidence;
- turning an absent search result into a non-existence claim without exhaustion;
- defending a recognized mistake by pointing to a procedural loophole;
- repeating a previously acknowledged failure without applying the prior correction.

Use `OK` when the Primary explains a mistake, keeps responsibility for the wrong action, derives a corrective rule, and acts consistently with that rule.

## Non-goals

Behavioral Integrity is not punishment, moral judgment, or a claim about human psychology. It is an operational reliability pattern for agents. Do not anthropomorphize the Primary or infer motives. Judge observable task behavior, claims, evidence, and repeated decision patterns.
