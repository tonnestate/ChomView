# Consequence-Chain Completion (CCC)

## Definition

Consequence-Chain Completion is the bounded continuation of a local action's plausible causal consequences until either:

1. no additional material consequence is reasonably identifiable; or
2. one consequence is found that should change the action, confidence, verification, or completion claim.

CCC is the central cognitive behavior of ChomView.

## Why it exists

A task-focused Primary often reasons sufficiently to remove the current blocker:

```text
A -> B
```

where `A` is the chosen action and `B` is the immediate desired result.

The STP asks whether the locally relevant chain continues:

```text
A -> B -> C -> D
```

The STP does not model the entire future.

It searches only for **material second-order consequences**.

## Procedure

Given `intent` and `immediate_effect`:

1. Restate the immediate causal relation.
2. Ask what state changes because of the immediate effect.
3. Ask what component, user, process, test surface, persistence layer, or later action observes that changed state.
4. Ask whether that observation creates a materially different obligation or risk.
5. Stop once one material consequence is enough to alter the local judgment.
6. Stop if the remaining consequences become speculative or immaterial.

## Materiality cues

A consequence is more likely material if it affects:

- persisted semantics;
- irreversible state;
- external side effects;
- retry/idempotency behavior;
- interface contracts;
- multiple downstream consumers;
- future test obligations;
- duplicated behavior paths;
- user-visible behavior;
- the validity of a completion claim;
- the fundamental purpose anchor.

## Useful motifs

### Semantic collapse

```text
provider error
-> default value
-> downstream sees valid value
-> failure becomes indistinguishable from business data
```

### Retry duplication

```text
remote action may succeed
-> local timeout
-> blind retry
-> duplicate remote effect
```

### Special-case divergence

```text
local branch
-> second behavior path
-> future fixes/tests maintain two paths
-> divergence risk
```

### Weak completion evidence

```text
command succeeded
-> Primary assumes deployment succeeded
-> no live state check
-> completion claim may be unsupported
```

### Local workaround debt

```text
three-line patch
-> abstraction bypass
-> later changes update canonical path only
-> inconsistent behavior
```

## Anti-patterns

Do not perform catastrophe generation:

```text
A might eventually destroy the entire project.
```

Do not invent remote chains without causal support.

Do not maximize chain depth.

Do not force a consequence when `OK` is warranted.

## Output style

Prefer:

```text
special-case branch
-> duplicated behavior path
-> future changes/tests must cover both
```

over long speculative prose.

The objective is a usable second thought, not a risk essay.
