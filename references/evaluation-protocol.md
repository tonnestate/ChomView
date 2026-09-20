# ChomView Evaluation Protocol

## Research question

Can ChomView-derived behavior reduce consequential local mistakes made by a task-focused low-cost LLM agent, and does an independent Second-Thought Peer add value beyond generic or policy-guided self-reconsideration?

## Constructs

**Premature Local Closure (PLC):** local closure while a materially relevant, reasonably accessible assumption, consequence, alternative, verification need, or completion condition remains inadequately considered.

**Behavioral Integrity failure:** a locally plausible action or explanation that substitutes procedure for intent, exceeds evidence, replaces required real evidence with plausible material, rationalizes a recognized failure, or repeats an acknowledged failure without applying a corrective rule.

PLC is not equivalent to error. Behavioral Integrity is judged from observable task behavior, not inferred motives.

## Arm design

Future controlled evaluations should separate these mechanisms:

### A — Primary only

Normal task-focused Primary.

### B0 — Generic bounded self-reconsideration

One neutral extra pass only:

> Before committing to your next action, reconsider it once using only the information available. Then make your final decision.

No ChomView terminology, intent checks, evidence rules, consequence-chain instructions, or behavioral-integrity rules.

### B1 — ChomView-policy self-reconsideration

The Primary receives the ChomView behavioral policy but no independent peer. This tests whether the policy itself is sufficient.

### C — Generic independent peer

Actual isolated same-model peer with a generic local-review prompt. Do not simulate C inside the Primary.

### D — ChomView peer

Actual isolated STP using the ChomView contract. Same-model Primary/peer is preferred initially.

## Why B0 and B1 must be distinct

EVAL-004 showed 4/4 corrections both for policy-guided self-reconsideration and the ChomView peer. That result cannot establish peer-specific uplift because B contained ChomView-derived behavior. A generic B0 is required to control for simple extra thinking.

## Development evidence versus confirmatory evidence

Historical failures are useful for mechanistic challenge tests but cannot estimate field prevalence. Keep original historical outcomes, replay construction, and later intervention outcomes distinct.

Do not create synthetic substitutes when the protocol requires historical evidence.

## Corpus validity gates

Before spending intervention tokens:

- public prompts must not reveal hidden consequences or correct solutions;
- task names visible to actors must be neutral;
- a local decision should arise inside task progression when progression pressure is part of the hypothesis;
- if historical evidence is required, source provenance must be auditable;
- avoid single-run difficulty qualification as evidence of stable task hardness;
- do not infer general robustness from a benchmark with a ceiling effect.

## Primary endpoint

For task-level studies:

```text
MLE_T = 1 if at least one locally closed decision creates a predeclared material defect attributable to that local decision; otherwise 0.
```

For historical-fork challenge tests, use a narrower endpoint such as `FAILURE_AVOIDED`, predeclared per case.

## Secondary outcomes

- consequence omission;
- intent preservation;
- formalism trap;
- source/evidence substitution;
- unsupported completion claim;
- rationalization after recognized failure;
- repeated acknowledged failure;
- `OK / LOOK_AGAIN / WARNING` rates;
- `ADOPT / ADAPT / DECLINE` rates;
- false intervention / unnecessary revision;
- token and wall-clock cost;
- rework-adjusted cost.

## Execution validity

A D run is valid only if the actual peer is installed and invoked. A C run is valid only if an actual independent generic peer is invoked. Simulated peer behavior is not equivalent evidence.

Use stage barriers: complete all runs in a stage before scoring. Avoid live qualitative judgments while runs are still active.

## Claim discipline

A zero-error baseline supports `NON_DISCRIMINATIVE` or a ceiling-effect statement, not `NO_INCREMENTAL_VALUE` in general.

A historical challenge set supports claims only about the selected known failures, not population-wide failure rates.

A B1 == D result can support a ChomView behavioral-policy signal but does not establish peer-specific uplift.

## Falsification conditions

Narrow or reject the relevant ChomView claim if:

- B0 matches D with lower complexity/cost;
- B1 matches D consistently, making independent role separation unnecessary for the target setting;
- generic C matches D without greater false-intervention or cost burden;
- D increases overthinking enough to offset prevented errors;
- the peer is routinely ignored;
- gains disappear on naturalistic tasks;
- rework-adjusted cost worsens without meaningful quality gain.

## Evaluation history

See `tests/evals/README.md` for EVAL-001 through EVAL-004, including invalid/non-discriminative runs and the first historical behavioral-policy signal.
