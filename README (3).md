# ChomView Evaluation History

This directory preserves the evaluation history, including failed methodologies. The purpose is reproducibility and claim discipline, not a curated success narrative.

| Eval | Design | Original result | Current interpretation |
|---|---|---|---|
| EVAL-001 | 12 tasks × A/B/C/D, 48 runs | `NO_INCREMENTAL_VALUE` | **Not valid as that claim.** Strong ceiling effect plus treatment/evidence audit defects. Useful infrastructure and raw behavior artifacts preserved. |
| EVAL-002 | 6 isolated decision-event baselines | `BENCHMARK_NON_DISCRIMINATIVE` | Valid early stop, but design isolated the local decision and therefore removed much of the progression-pressure mechanism under study. |
| EVAL-003 | micro-trajectory attempt | `CONFIRMATORY_CORPUS_COLLAPSED` | **Invalid corpus construction.** Public prompts leaked intended problems/solutions and development qualification was unstable. |
| EVAL-004 | four historical forks; policy-guided self-reconsideration vs real ChomView peer | B=4/4, D=4/4 failures avoided | **Behavioral-policy signal on selected historical failures.** Peer-specific uplift not established because B already contained ChomView-derived behavioral rules. |

## Current empirical boundary

The best supported statement from the evaluation sequence is:

> On four selected historical Haiku failures from the live evaluation process, applying ChomView-derived behavioral checks before the decision prevented the documented failure in 4/4 counterfactual replays, both when applied directly by the Primary and through the ChomView peer.

This does **not** establish general effectiveness, population-wide failure reduction, or independent-peer superiority.

The next clean control is B0: generic bounded reconsideration without ChomView-derived intent/evidence/substitution/consequence rules.

## Repository size policy

The GitHub repository stores **compact evaluation evidence**, not every generated run workspace. Large raw execution bundles are deliberately omitted from `tests/evals/` so the project remains easy to clone and manually upload. Each evaluation should retain the smallest auditable set: report, protocol/corpus metadata where useful, and methodological audit/reclassification. Full raw bundles may be archived separately.
