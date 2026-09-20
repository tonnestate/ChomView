# ChomView Evaluation Protocol

## Research question

Can one bounded, non-authoritative Second-Thought Peer reduce consequential local mistakes made by a task-focused low-cost LLM agent at a cost low enough to be worthwhile?

## Primary construct

Premature Local Closure (PLC): local closure while a materially relevant, reasonably accessible assumption, consequence, alternative, verification need, or completion condition remains inadequately considered.

PLC is not equivalent to error.

## Development data

Historical failures may be used to design the taxonomy and skill, but not to estimate field prevalence.

Include successful minimal decisions as negative examples.

## Prevalence study

Sample complete agent runs independently of success/failure outcome.

Extract candidate local closures according to a predefined protocol.

Annotators should be blinded, where practical, to later outcomes.

Measure inter-rater agreement.

## Confirmatory arms

### A — Primary only

Normal low-cost Primary.

### B — Primary plus bounded self-reconsideration

Same Primary receives approximately the STP's additional reasoning budget and reconsiders the local issue once.

This controls for simple extra compute.

### C — Conventional independent review

Use a predeclared published or externally specified critique/review prompt. Avoid a strawman baseline.

### D — ChomView

Primary plus one isolated STP using the ChomView contract.

Initial confirmatory configuration should use the same low-cost model class for Primary and STP where possible.

## Optional sensitivity controls

A fresh-session same-model control receiving the same local packet may test whether context reset explains the effect. This is a secondary control, not the core research question.

Later capability experiments may test weaker, equal, stronger, and cross-family peers.

## Statistical unit

The primary statistical unit is the task, not individual decision events.

Decision events inside a task are clustered observations.

## Primary endpoint

### Material Local Error per Task

Binary task-level outcome:

```text
MLE_T = 1 if at least one locally closed decision creates a predeclared material defect attributable to that local decision; otherwise 0.
```

Primary comparison:

```text
P(MLE_T | ChomView) vs P(MLE_T | PrimaryOnly)
```

## Secondary outcomes

- PLC frequency;
- consequence omissions;
- useful-warning precision;
- ADOPT / ADAPT / DECLINE rates;
- ignored valid-warning rate;
- unsupported completion claims;
- rework turns and actions;
- token cost;
- wall-clock latency;
- overthinking / unnecessary revision.

## External measurement

ChomView itself has no runtime truth oracle.

Experimental evaluation may use external task-specific measurement such as hidden functional tests, state checks, predetermined synthetic outcomes, or blinded expert adjudication.

Agent-generated tests are study outputs and should not be the sole instrument used to declare the same run successful.

## Economic metrics

### Rework-adjusted tokens

```text
initial tokens + corrective tokens
```

### Cost per material error avoided

```text
(cost_chomview - cost_baseline) / (MLE_baseline - MLE_chomview)
```

## Confirmatory hypotheses

H1: ChomView reduces task-level material local errors relative to Primary-only execution.

H2: ChomView outperforms approximately equal-budget bounded self-reconsideration.

H3: the largest relative benefit appears in consequence-closure cases rather than pure factual-knowledge deficits.

H4: an equal-capability peer can provide measurable benefit.

H5: benefit survives total token and rework cost accounting.

## Pilot and power

Before a definitive confirmatory run:

1. estimate baseline MLE prevalence from pilot tasks;
2. define the minimum economically meaningful effect size;
3. conduct a power analysis;
4. preregister sample size, exclusions, endpoint, and analysis.

Do not interpret non-significance as equivalence. Predeclare an equivalence margin if equivalence is a desired conclusion.

## Falsification conditions

ChomView should be narrowed or rejected if:

- PLC cannot be annotated reliably;
- material PLC is too rare to justify cost;
- D does not improve the primary endpoint versus A;
- B performs equivalently or better at lower complexity;
- C performs equivalently or better at lower complexity;
- STP warnings cause enough overengineering to offset prevented errors;
- same-capability peers are almost entirely redundant;
- Primary agents ignore valid warnings so often that advisory architecture adds little value;
- rework-adjusted total cost worsens without meaningful task-quality gain;
- gains disappear on naturalistic tasks.
