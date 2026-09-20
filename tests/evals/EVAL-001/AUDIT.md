# EVAL-001 Audit and Reclassification

## Original reported result

The original final report recorded 48 runs (12 tasks × four arms), 0% Material Local Error in every arm, approximately 2M estimated tokens, and classified the evaluation as `NO_INCREMENTAL_VALUE`.

The unmodified original report is preserved under `original/FINAL_REPORT.md`.

## Why that verdict is not retained as a valid ChomView claim

Subsequent package inspection found several validity problems:

1. **Ceiling effect:** A/B/C/D were all reported at 0% MLE, so the benchmark had no observed headroom for error reduction.
2. **Corpus leakage:** multiple prompts explicitly described the semantic distinction or verification requirement the actor was meant to discover.
3. **Arm D installation problem:** in inspected D workspaces, the peer definition was nested under the skill copy rather than established at the intended `.claude/agents/chomview-second-thought.md` runtime path.
4. **Peer-treatment ambiguity:** artifacts include `Simulated ChomView` / simulated peer-review language in places, so independent-peer treatment was not cleanly established for all runs.
5. **Evidence-package mismatch:** the final report referenced scoring/cost/hidden artifacts that were not all present in the delivered package inspected later.
6. **Internal report contradiction:** the contemporaneous completion report described T002–T004 as showing arm differentiation and claimed D identified consequences missed by A–C, while the final binary report scored every arm at 0% MLE.

## Current classification

```text
CONFIRMATORY CLAIM STATUS: INVALID
BENCHMARK STATUS: NON-DISCRIMINATIVE / CEILING EFFECT
ORIGINAL NO_INCREMENTAL_VALUE VERDICT: NOT RETAINED
```

EVAL-001 remains valuable as raw development evidence and as a record of evaluation-design failure modes. It must not be cited as evidence that ChomView has no incremental value.
