# Prior Art and Claims Boundary

ChomView is an experimental integration pattern. Its scientific value must not depend on pretending its ingredients are individually new.

## Established neighboring ideas

Relevant prior work includes:

- SOAR and impasse-driven subgoaling;
- bounded rationality and value of computation / metareasoning;
- Self-Refine;
- Reflexion;
- Devil's Advocate / anticipatory reflection;
- independent review and verification patterns such as Agent Rigor;
- comparison-only runtime advisors such as COTA;
- test-suite reduction and cost-aware verification;
- multi-agent reliability/failure research;
- lifecycle hooks and pre-execution advice in modern agent harnesses.

## Do not claim novelty for

Do not claim ChomView invented:

- second opinions;
- critics;
- subagents;
- subgoaling;
- metareasoning;
- bounded deliberation;
- weak helper models;
- verification planning;
- minimum testing;
- runtime intervention;
- multi-agent collaboration.

## Candidate contribution

The candidate contribution is the specific composition:

1. a task-focused Primary remains owner of the global task;
2. the Primary is assumed to be locally overconfident and consequence-limited at times;
3. one isolated peer receives one local problem;
4. the peer need not be stronger than the Primary;
5. communication uses a compact semantic packet rather than full-task duplication by default;
6. the peer explicitly performs bounded consequence-chain completion;
7. the peer can say OK, LOOK_AGAIN, or WARNING;
8. the peer may advise "think harder" without solving the problem;
9. advice is non-authoritative;
10. the Primary acknowledges but retains agency;
11. no automatic multi-round debate follows;
12. value is judged against additional compute, review baselines, rework, and token cost;
13. material self-corrections can be persisted as reusable behavioral rules outside conversational memory;
14. repeated acknowledged failures can enter a bounded deterministic escalation state when explicit matchers exist;
15. new evidence is separated from authorization to mutate the root objective;
16. heterogeneous agents may retain different priors while execution authority is bound by an explicit local contract;
17. stakeholder/resource metadata separates preference from spending or mutation authority.

This should be described as a **candidate integration-level research gap**, not proven foundational novelty.

## Strongest falsifier

If bounded self-reconsideration or a standard independent review prompt performs equivalently at lower complexity/cost, ChomView's independent architectural value is weak.

## Strongest positive result

The strongest practical result would be evidence that two similarly limited low-cost model instances with separated immediate responsibilities produce fewer consequential local errors at positive net cost than one task-focused instance alone.

## v0.3 implementation boundary

Claude Code lifecycle hooks, persistent state files, permission gating, and escalation state machines are established engineering mechanisms and are not claimed as novel. ChomView's research question concerns the composition and incremental value of the bounded pattern, not ownership of those primitives.

The v0.3 Behavioral Continuity Guard is an implementation hypothesis. Its presence in the package must not be cited as performance validation.

## v0.4 implementation boundary

Access control, policy enforcement, capability security, permission gates, resource ownership, and policy-as-code are established engineering ideas. ChomView does not claim invention of those mechanisms.

The v0.4 hypothesis is narrower: a bounded second-thought / continuity system may become more robust in heterogeneous-agent environments when it distinguishes cognition from authority and composes explicit stakeholder/resource contracts with prior behavioral corrections.

Do not claim that ChomView defines cultural normality, solves general value alignment, or proves that a foreign agent is safe merely because it passes the local behavioral contract.
