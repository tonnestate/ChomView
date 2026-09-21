# ChomView: A Bounded Second-Thought Peer Against Premature Local Closure in Task-Focused LLM Agents

## Consequence-Aware Local Intervention for Low-Cost Agentic Systems

### Pre-Empirical Position Paper and Registered Evaluation Protocol

## Abstract

Long-horizon LLM agents must simultaneously maintain a global objective, use tools, interpret evidence, choose implementations, manage context, control cost, verify progress, and decide when local problems are sufficiently resolved. This creates a structural asymmetry of attention: the Primary is responsible for moving the whole task forward while individual local decisions compete for limited reasoning effort.

We study a proposed failure mode called **Premature Local Closure (PLC)**: a local issue is treated as sufficiently resolved while a materially relevant assumption, consequence, alternative, verification requirement, or completion condition remains underconsidered. PLC is not equivalent to error. A prematurely closed decision may ultimately prove correct. Of particular interest is **Consequence Closure**, where the agent understands the immediate effect of its action but fails to project a materially relevant downstream consequence.

We propose **ChomView**, an interaction architecture with a task-owning Primary and one bounded non-authoritative **Second-Thought Peer (STP)**. The STP receives one local problem through a compact BROTLI thought packet, thinks that problem through further than the Primary currently has, performs bounded consequence-chain completion, and returns `OK`, `LOOK_AGAIN`, or `WARNING` plus concise advice and optional verification guidance. It does not take over the parent task or start an iterative debate.

The central hypothesis is not that a stronger model should supervise a weaker one. ChomView tests whether **role separation itself can improve local decision quality when both reasoners are individually limited**. The proposed contribution is therefore not second opinions, subgoaling, or verification planning individually, but a particular low-cost composition: one local problem, one consequence-aware peer thought, one non-binding intervention, then return control.

## 1. Problem Statement

The task-focused Primary has a legitimate operational objective: keep the global task moving. A local blocker therefore exerts pressure toward a decision that is sufficient to continue. That is often rational. It becomes problematic when `sufficient to continue` is mistaken for `sufficiently thought through`.

Example:

```text
NULL causes the exception.
The caller expects a number.
Map NULL to 0.
Exception disappears.
Continue.
```

The local fix may work while leaving unexamined whether NULL means absence, timeout, malformed response, or provider failure; whether zero has valid domain meaning; whether the transformation destroys information; and what downstream systems infer from zero.

The motivating architecture hypothesis is that the Primary may be capable of considering these issues but does not allocate enough local attention because it is carrying the global task.

## 2. ChomView Primary Archetype

A ChomView Primary is a behavioral archetype, not a psychological diagnosis or model family. It is a task-focused agent that may combine:

- strong progression pressure;
- context loss or constraint drift;
- rapid acceptance of locally plausible interpretations;
- overconfidence in locally coherent solutions;
- incomplete downstream consequence projection;
- weak revalidation;
- verification selected from within the Primary's own framing;
- completion claims stronger than available support.

A ChomView Primary may still be useful precisely because it moves quickly.

## 3. PLC

For a task with local decision points `d_i`, let the Primary observe local information `E_i`, form interpretation `I_i`, and consider action or claim `A_i`.

PLC occurs when the Primary treats `A_i` as sufficiently resolved while at least one reasonably accessible consideration that could materially change the action, confidence, consequence estimate, verification need, or completion claim remains inadequately considered.

PLC is neither necessary nor sufficient for eventual error.

### PLC subtypes

1. Interpretation Closure
2. Solution Closure
3. Consequence Closure
4. Verification Closure
5. Completion Closure

The ChomView proposal is centered particularly on Consequence Closure.

## 4. Consequence Projection

A task-focused Primary may reason only far enough to restore progress:

```text
A -> B
```

The STP extends only the materially relevant local chain:

```text
A -> B -> C -> D
```

This process is **Consequence-Chain Completion (CCC)**.

CCC stops when no additional material consequence is reasonably identifiable or once a consequence is found that should change the local decision, confidence, verification, or completion claim.

It does not attempt exhaustive future simulation.

## 5. Core Hypothesis

The Primary and STP have different immediate objectives:

```text
Primary: GlobalProgress(T)
STP:     LocalDeliberation(d_i)
```

The main hypothesis is that one locally focused peer may expose relevant considerations missed by the task-focused Primary even if both use the same limited model class.

A practically important version is:

```text
limited task-focused Primary + limited local STP
>
limited task-focused Primary alone
```

for consequential local decisions, after cost accounting.

## 6. Architecture

The Primary retains:

- global task ownership;
- main context;
- tools;
- execution;
- integration;
- final decision authority.

The STP receives:

- a small purpose anchor;
- one local situation;
- Primary intent;
- concise Primary rationale;
- directly relevant facts;
- directly relevant constraints.

It does not receive the full task trajectory by default.

Its intervention is non-authoritative.

The Primary records `ADOPT`, `ADAPT`, or `DECLINE` after material advice.

## 7. BROTLI

BROTLI/1 is a semantic compression protocol for local intervention. It transmits decision-relevant state rather than raw private chain-of-thought or the full transcript.

The protocol distinguishes facts from the Primary's rationale so that local assumptions are not silently promoted into observations.

## 8. Boundedness

The v0.1 architecture uses:

```text
peer_deliberations(did) <= 1
context_requests(did) <= 1
peer_spawn_depth = 0
debate_rounds = 0
```

Residual STP error is accepted rather than recursively creating a reviewer of the reviewer.

## 9. Related Work Boundary

ChomView does not claim novelty for subgoaling, metareasoning, self-reflection, critics, advisors, or verification planning.

SOAR established impasse-driven subgoaling. Value-of-computation research formalized the cost/benefit of additional reasoning. Self-Refine and Reflexion demonstrate structured additional inference. Devil's Advocate performs anticipatory reflection. Agent Rigor provides independent review/verification patterns. COTA demonstrates useful non-binding runtime advice from a small auxiliary model. Multi-agent failure research shows that adding agents is not automatically beneficial.

The candidate gap is the specific composition: local non-authoritative peer intervention for a progression-focused Primary, explicit bounded consequence-chain completion, a peer that need not be stronger, compact local semantic transfer rather than full-task ownership, and one intervention followed by immediate return of control.

This is a candidate integration-level research gap, not established foundational novelty.

## 10. Evaluation

Historical failures are useful for development but cannot estimate field prevalence.

Natural prevalence should be studied from randomly sampled complete agent runs, extracting candidate local closures independent of eventual outcome.

The confirmatory unit is the task, not each decision event.

Core arms:

- A: Primary only
- B: Primary plus bounded self-reconsideration with similar additional budget
- C: conventional independent review using a predeclared baseline
- D: ChomView STP

Initial confirmatory experiments should use the same low-cost model class for Primary and STP where practical.

A fresh-context same-model control can be included as a sensitivity analysis without redefining the central research question.

## 11. Primary Outcome

The proposed primary endpoint is **Material Local Error per Task (MLE)**: whether at least one locally closed decision creates a predeclared material defect attributable to that local decision.

Secondary outcomes include PLC frequency, consequence omissions, useful-warning precision, advice adoption, ignored valid warnings, unsupported completion claims, rework, tokens, latency, and overthinking.

## 12. Economic Criterion

ChomView is designed for low-cost models. Initial token cost alone is insufficient; rework must also be counted.

Useful measures include:

```text
ReworkAdjustedTokens = InitialTokens + CorrectiveTokens
```

and cost per material local error avoided.

## 13. Falsification

ChomView should be narrowed or rejected if:

- PLC cannot be annotated reliably;
- material PLC is too rare to justify peer cost;
- the STP does not reduce material local errors;
- bounded self-reconsideration performs equivalently or better at lower complexity;
- conventional review performs equivalently or better at lower complexity;
- STP warnings create enough overengineering to offset benefit;
- equal-capability peers are largely redundant;
- Primary agents ignore useful advice so often that the advisory architecture adds little value;
- rework-adjusted cost worsens without meaningful quality gain;
- benefits disappear on naturalistic tasks.

## 14. Skill Roadmap

### v0.1

- manual/high-recall activation;
- isolated STP;
- BROTLI/1 request/response;
- CCC;
- `OK / LOOK_AGAIN / WARNING`;
- one context request maximum;
- `ADOPT / ADAPT / DECLINE` acknowledgement.

### v0.2

- stabilized purpose anchor;
- stronger packet validation;
- structured runtime metrics.

### v0.3

- persist material `changed_rule` corrections outside conversational memory;
- re-inject active correction state across sessions and new user input;
- add bounded recurrence enforcement: NOTICE -> WARNING -> STRIKE -> FREEZE -> ESCALATE;
- prevent silent goal mutation from treating new evidence as new authorization;
- add treatment identity and duplicate-skill release gates.

### Later

- weaker/equal/stronger/cross-family peers;
- optional persistent P2P runtime;
- cost-sensitive routing;
- trajectory-derived experience motifs if they demonstrate incremental benefit.

## 15. Claims Boundary

The current defensible claim is that ChomView defines and implements a plausible, falsifiable integration pattern for bounded consequence-aware second thought and behavioral continuity in task-focused agents.

v0.3 implementation is not confirmatory evidence that the new enforcement layer improves outcomes. Historical evaluation evidence and implementation claims must remain separate.
