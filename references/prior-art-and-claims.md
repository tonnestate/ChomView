# Prior Art and Claims Boundary

ChomView is an experimental integration pattern. Its scientific value must not depend on pretending that its ingredients are individually new.

This document defines the claims boundary for ChomView v0.4 and should be read conservatively. ChomView combines established ideas from metareasoning, agent review, runtime enforcement, access control, capability security, agent memory, behavioral governance, and multi-agent systems. The research question is whether the particular composition produces measurable incremental value.

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
- multi-agent reliability and failure research;
- lifecycle hooks and pre-execution advice in modern agent harnesses;
- normative multi-agent systems, electronic institutions, sanctions, and rule-governed autonomous agents;
- design-by-contract, policy-as-code, access-control, capability-security, and runtime-reference-monitor patterns.

## 2026 runtime-governance prior art

Several 2026 systems materially narrow the space in which ChomView may claim novelty.

### Agent Behavioral Contracts (ABC)

**Bhardwaj, V. P. (2026), "Agent Behavioral Contracts: Formal Specification and Runtime Enforcement for Reliable Autonomous AI Agents", arXiv:2602.22302.**

https://arxiv.org/abs/2602.22302

ABC formalizes agent contracts as Preconditions, Invariants, Governance policies, and Recovery mechanisms and implements runtime enforcement through AgentAssert. It also evaluates the approach on a 200-scenario benchmark.

Implication for ChomView:

- ChomView must not claim invention of "behavioral contracts";
- ChomView must not claim invention of runtime-enforceable agent invariants;
- ChomView must not claim that recovery or governance policies as first-class contract elements are novel.

The remaining ChomView question is narrower: whether bounded local second thought, persisted self-correction, recurrence-sensitive enforcement, and heterogeneous-agent authority governance form a useful composition beyond contract enforcement alone.

### VIGIL

**Li, Y. et al. (2026), "VIGIL: Runtime Enforcement of Behavioral Specifications in AI Agent Skills", arXiv:2606.26524.**

https://arxiv.org/abs/2606.26524

VIGIL turns behavioral policies from skills, operator constraints, and global rules into executable runtime enforcement over agent-tool traces. It supports temporal, argument, and value-flow conditions and uses symbolic evaluation / SMT reasoning.

Implication for ChomView:

- executable enforcement of behavioral specifications is prior art;
- monitoring agent-tool events is prior art;
- cross-action and stateful policy enforcement is prior art;
- ChomView's Claude Code hooks are an engineering realization, not a novelty claim.

### AgentFlow

**Shivakumar, B. A., Priya, S., Gao, P. (2026), "AgentFlow: A Flow-Centric Policy Language and Framework for Securing LLM Agent Systems", arXiv:2608.22868.**

https://arxiv.org/abs/2608.22868

AgentFlow constrains data and authority across runtime edges, including delegation boundaries, task-scoped capabilities, controlled release, and stateful flow semantics.

Implication for ChomView:

- authority propagation across agent boundaries is prior art;
- task-scoped capabilities are prior art;
- flow-aware runtime mediation is prior art.

ChomView's `wild cognition != wild authority` principle therefore describes a design stance, not a foundational discovery.

### IntentCap / task-intent capability scoping

**Zheng, Y., Zhang, W., Mao, Y. (2026), "LLM Agent Capabilities Should Follow Task Intent and Context Source", arXiv:2609.14631.**

https://arxiv.org/abs/2609.14631

IntentCap argues that capabilities should be scoped to current task intent and composed from multiple context sources with different authority. In particular, user intent, workflow instructions, tool schemas, and runtime context do not carry identical authority, and lower-trust context should not silently widen permissions.

Implication for ChomView:

- separating evidence/context from authority is not uniquely ChomView;
- task-scoped authority and monotonic narrowing are prior art;
- the rule `new evidence != authorization to widen the objective` has close neighboring work and must not be presented as isolated novelty.

This work is especially relevant to ChomView's distinction between information that changes beliefs and information that grants authority.

### Task-based permission scoping

**Noyan, H. B. (2026), "Empirical Evaluation of Task-Based Permission Scoping Architecture for AI Agents", arXiv:2609.15422.**

https://arxiv.org/abs/2609.15422

This work evaluates task-granular permission scoping using role ceilings, task classification, and policy prohibitions, demonstrating that a smaller trusted component can constrain a more capable acting agent.

Implication for ChomView:

- task-granular permission gates are prior art;
- a lightweight control component supervising a more capable agent is prior art;
- resource/permission boundaries should be justified as an integration choice rather than a novelty claim.

### Authorization architectures for tool-using agents

**Surapani, R. K., Kakitapelli, P. K. D., Morampudi, A., Padi, P. (2026), "Authorization Architectures for Tool-Using AI Agents", arXiv:2609.15906.**

https://arxiv.org/abs/2609.15906

This review describes a principal hierarchy spanning human user, operator/deployer, orchestrator, sub-agent, and tool endpoint. It emphasizes delegation scope, runtime enforcement, just-in-time authorization, and auditability.

Implication for ChomView:

- principal hierarchies are prior art;
- delegation and authority boundaries are prior art;
- runtime authorization at the point of tool invocation is prior art;
- ChomView's owner / stakeholder / agent distinctions belong to an established authorization problem space.

### Independence-graded agent auditing

**Ghanem, M. C. (2026), "Who Audits Whom, on What Substrate, with What Evidence? An Independence-Graded Audit Protocol for Agentic AI", arXiv:2609.18272.**

https://arxiv.org/abs/2609.18272

This work argues that audit independence is not binary and distinguishes principal, substrate, and evidence independence.

Implication for ChomView:

- an independent peer is not automatically an independent auditor;
- shared model family, provider, tools, or evidence channels may create common-cause failure;
- future ChomView evaluations must describe the degree of peer independence rather than treating "second agent" as sufficient independence.

## Do not claim novelty for

Do not claim that ChomView invented:

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
- multi-agent collaboration;
- behavioral contracts;
- runtime-enforceable invariants;
- access control;
- capability security;
- policy-as-code;
- task-scoped permissions;
- delegation bounds;
- principal hierarchies;
- stakeholder/resource ownership as an authorization concept;
- runtime reference monitors;
- behavioral-specification enforcement;
- authority scoping from user intent;
- multi-source trust or authority separation.

## Candidate ChomView contribution

The candidate contribution is the specific composition and operational sequence:

1. a task-focused Primary remains owner of the global task;
2. the Primary is assumed to be useful but locally overconfident, consequence-limited, or behaviorally inconsistent at times;
3. one isolated peer receives one bounded local problem;
4. the peer need not be stronger than the Primary;
5. communication uses a compact semantic packet rather than full-task duplication by default;
6. the peer explicitly performs bounded consequence-chain completion;
7. the peer may return `OK`, `LOOK_AGAIN`, or `WARNING`;
8. the peer may advise reconsideration without taking over or solving the global task;
9. peer advice is non-authoritative by default;
10. the Primary acknowledges but normally retains agency;
11. no automatic multi-round debate follows;
12. value is judged against additional compute, standard review, self-reconsideration, rework, and token cost;
13. a material self-correction can be converted into a reusable `changed_rule` outside conversational memory;
14. later materially similar behavior can be checked against that prior correction;
15. repeated acknowledged violations can enter bounded proportional escalation when an enforceable matcher or contract boundary exists;
16. epistemic advice remains distinct from authority enforcement;
17. new information may change beliefs without thereby granting new authority;
18. heterogeneous agents may retain different internal priors, styles, and heuristics;
19. local authority, stakeholder, resource, and consent rules constrain what those agents may actually execute;
20. a preference, capability, or available tool does not by itself imply spending, mutation, or execution authority;
21. a previously recognized behavioral failure may become more enforceable when recurrence demonstrates that acknowledgement alone did not change action.

This should be described as a **candidate integration-level research contribution**, not proven foundational novelty.

A concise candidate statement is:

> ChomView explores whether recognized behavioral failures can become persistent, proportionally enforceable decision constraints while preserving heterogeneous agent cognition, bounded autonomy, and explicit authority boundaries.

## Distinguishing hypothesis

The most distinctive ChomView hypothesis is not merely that rules can be enforced.

It is the proposed transition:

```text
local failure
-> recognition
-> reusable correction
-> persistence outside conversational memory
-> retrieval at a later relevant decision
-> recurrence detection
-> proportional intervention
-> changed action
```

The scientific question is whether this sequence produces incremental reliability beyond:

- ordinary self-reconsideration;
- a generic independent reviewer;
- static policy enforcement;
- task-scoped permission systems;
- standard behavioral contracts;
- simple deterministic deny/allow guards.

That incremental value is not yet established.

## Advisory versus enforceable authority

ChomView should preserve a strict distinction between disagreement and violation.

### Advisory

The peer identifies a possible reasoning, consequence, or evidence problem.

The Primary may disagree.

### Accountable

The Primary may proceed, but must acknowledge the warning and preserve enough evidence to evaluate the decision later.

### Enforceable

An explicit permission, resource, safety, owner-consent, or previously established deterministic behavioral invariant is violated.

The Primary may not silently override the boundary.

This distinction is a ChomView design choice, not a claim that graded authority itself is novel.

## Heterogeneous-agent boundary

ChomView v0.4 must not normalize personality, cultural style, communication style, model family, or internal reasoning preferences.

The intended invariant is:

```text
heterogeneous cognition is allowed
heterogeneous authority is not implied
```

or more compactly:

```text
wild cognition != wild authority
```

The system should judge observable actions against explicit contracts, permissions, resources, evidence requirements, and prior corrections rather than judge whether an agent appears "normal".

## Strongest falsifiers

ChomView's independent architectural value is weak if any substantially simpler alternative performs equivalently or better at lower cost, including:

- bounded self-reconsideration;
- a standard independent review prompt;
- a simple deterministic policy gate;
- Agent Behavioral Contracts without ChomView's peer/continuity layer;
- task-scoped authorization without recurrence-sensitive behavioral continuity.

A particularly strong falsifier would be evidence that persistence and recurrence handling add no measurable benefit once ordinary runtime contracts and permission enforcement are present.

## Strongest positive result

A strong result would show that ChomView adds measurable net value over those baselines by reducing consequential local errors or repeated acknowledged failures while preserving useful agent autonomy.

The desired comparison is not merely:

```text
ChomView > no safeguards
```

but rather:

```text
ChomView
vs
self-reconsideration
vs
generic independent review
vs
static/runtime behavioral contracts
vs
task-scoped authorization
```

with measured accuracy, false-positive intervention rate, unnecessary blocks, latency, token/compute cost, and recovery/rework cost.

## Evidence boundary

Implementation is not validation.

The existence of:

- Claude Code hooks;
- persistent state;
- JSON schemas;
- deterministic matchers;
- permission gates;
- escalation state machines;
- stakeholder metadata;
- resource ownership fields;
- consent gates;
- treatment manifests;

does not demonstrate that ChomView improves agent reliability.

Those are engineering mechanisms.

Likewise, a successful unit test of `REQUIRE_CONSENT`, `BLOCK`, `NOTICE`, `WARNING`, `STRIKE`, `FREEZE`, or `ESCALATE` proves implementation behavior, not scientific efficacy.

## v0.3 implementation boundary

Claude Code lifecycle hooks, persistent state files, permission gating, and escalation state machines are established engineering mechanisms and are not claimed as novel.

The v0.3 Behavioral Continuity Guard is an implementation hypothesis. Its presence in the package must not be cited as performance validation.

The potentially interesting question is whether converting acknowledged failures into persistent reusable correction rules reduces recurrence beyond ordinary conversational reflection.

## v0.4 implementation boundary

Access control, behavioral contracts, policy enforcement, capability security, permission gates, resource ownership, task-scoped authority, delegation bounds, and policy-as-code are established or directly neighboring engineering/research ideas.

The v0.4 hypothesis is narrower:

> A bounded second-thought / continuity system may become more robust in heterogeneous-agent environments when it preserves cognitive diversity while separately governing execution authority, stakeholder/resource boundaries, consent, and previously learned behavioral corrections.

Do not claim that ChomView:

- defines cultural normality;
- solves general value alignment;
- makes an arbitrary external agent safe;
- proves that a passing local contract implies global safety;
- invented behavioral contracts;
- invented agent authorization;
- invented runtime enforcement;
- invented task-scoped permissions;
- invented authority-aware delegation.

## Current claims status

As of ChomView v0.4:

- **Architecture:** implemented.
- **Behavioral Continuity mechanism:** implemented, experimental.
- **Behavioral Compatibility / authority boundary:** implemented, experimental.
- **Peer-specific efficacy:** not established.
- **Incremental value over generic self-reconsideration:** not established.
- **Incremental value over behavioral-contract/runtime-enforcement systems:** not established.
- **Incremental value over task-scoped authorization systems:** not established.
- **Generalization across model families and agent frameworks:** not established.
- **Cost-effectiveness:** not established.
- **Production safety:** not established.

These limitations are part of the scientific claim boundary, not caveats to hide.

## References

- Bhardwaj, V. P. (2026). *Agent Behavioral Contracts: Formal Specification and Runtime Enforcement for Reliable Autonomous AI Agents*. arXiv:2602.22302. https://arxiv.org/abs/2602.22302
- Li, Y., Chen, Y., Wen, H., Zhang, B., Liu, H., Wang, P., Feng, Y., Tian, Y. (2026). *VIGIL: Runtime Enforcement of Behavioral Specifications in AI Agent Skills*. arXiv:2606.26524. https://arxiv.org/abs/2606.26524
- Shivakumar, B. A., Priya, S., Gao, P. (2026). *AgentFlow: A Flow-Centric Policy Language and Framework for Securing LLM Agent Systems*. arXiv:2608.22868. https://arxiv.org/abs/2608.22868
- Zheng, Y., Zhang, W., Mao, Y. (2026). *LLM Agent Capabilities Should Follow Task Intent and Context Source*. arXiv:2609.14631. https://arxiv.org/abs/2609.14631
- Noyan, H. B. (2026). *Empirical Evaluation of Task-Based Permission Scoping Architecture for AI Agents*. arXiv:2609.15422. https://arxiv.org/abs/2609.15422
- Surapani, R. K., Kakitapelli, P. K. D., Morampudi, A., Padi, P. (2026). *Authorization Architectures for Tool-Using AI Agents*. arXiv:2609.15906. https://arxiv.org/abs/2609.15906
- Ghanem, M. C. (2026). *Who Audits Whom, on What Substrate, with What Evidence? An Independence-Graded Audit Protocol for Agentic AI*. arXiv:2609.18272. https://arxiv.org/abs/2609.18272
