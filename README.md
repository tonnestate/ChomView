# ChomView

<p align="center">
  <strong>One agent keeps moving. One peer briefly looks at what it is about to overlook.</strong><br>
  A bounded second-thought skill for task-focused AI agents.
</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/license-Apache--2.0-blue">
  <img alt="Status" src="https://img.shields.io/badge/status-experimental-orange">
  <img alt="Version" src="https://img.shields.io/badge/version-0.4.0-green">
  <img alt="Agent Skill" src="https://img.shields.io/badge/agent-skill-purple">
  <img alt="Protocol" src="https://img.shields.io/badge/protocol-BROTLI%2F1-6f42c1">
</p>

---

## Why ChomView exists

Long-running AI agents have a structural problem: the same agent is expected to keep the **whole task** moving while also making dozens of small local decisions correctly.

That often produces a familiar pattern:

```text
"This fixes the immediate problem. Continue."
```

The local decision may be plausible, but the agent may not have thought far enough about:

- what assumption it just made;
- what the action changes downstream;
- whether the smallest local fix merely moves complexity elsewhere;
- whether the check it ran proves what it claims;
- whether `done`, `fixed`, or `verified` is actually supported.

ChomView calls this family of failures **Premature Local Closure (PLC)**.

ChomView does not solve this with a supervisor, jury, recursive reviewer, or full-context second project manager.

It adds one bounded peer thought:

> **What has the Primary not thought through in this one local decision?**

---

## The idea

```text
                     GLOBAL TASK
                         │
                         ▼
                 CHOMVIEW PRIMARY
                         │
              works / decides / moves
                         │
                 local decision
                         │
                         ▼
                 BROTLI/1 packet
                         │
                         ▼
              SECOND-THOUGHT PEER
                         │
              one bounded local thought
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
       OK           LOOK_AGAIN         WARNING
        │                │                │
        └────────────────┴────────────────┘
                         │
                         ▼
                  PRIMARY ACK
               ADOPT / ADAPT / DECLINE
                         │
                         ▼
                 PRIMARY CONTINUES
```

The Primary keeps ownership of the task.

The peer gets one local problem, thinks its consequence chain further, returns concise non-authoritative advice, and stops.

---

## ChomView Primary

The **ChomView Primary** is a behavioral archetype: a useful, task-focused agent that may still be locally chaotic.

It can:

- lose context during long runs;
- forget a constraint;
- prefer the easiest path that restores progress;
- become too confident in a locally coherent explanation;
- underestimate second-order consequences;
- choose a check that is narrower than its claim;
- say `done` before the evidence really supports `done`.

The design assumption is intentionally pessimistic:

> **Do not rely on the Primary to notice every time its own local reasoning is too shallow.**

ChomView does not remove the Primary's autonomy. It gives the Primary one additional perspective before a consequential local decision disappears into the rest of the trajectory.

---

## The informal origin story: "Chaotic Girlfriend Behavior"

ChomView started from an intentionally exaggerated human metaphor.

Imagine a capable but chaotic person focused on getting through the day and completing the immediate mission. They are convinced the current decision is fine, but they do not always think the consequence chain through. A trusted friend does **not** take over their life, forbid the decision, or solve the whole problem. The friend reacts only to the concrete local situation:

> "You can do that — but if you do, have you thought about what happens next?"

Or:

> "If you skip this check, the thing you actually want may fail later. Think this part through once more."

That metaphor became the core ChomView interaction pattern: **a non-authoritative second thought focused on one local consequence chain**.

It is only a design metaphor. ChomView makes no claim that LLM behavior is equivalent to human relationships, personality, or mental-health phenomena.

> **The Digital Cane is for agents, not humans.**  
> Physical punishment is not a governance mechanism. Behavioral enforcement in software, however, is fair game.

In ChomView, the "Digital Cane" means bounded, auditable software enforcement such as `NOTICE`, `REQUIRE_CONSENT`, `BLOCK`, or `FREEZE` — never physical punishment.

---

## What makes ChomView different

ChomView is not a claim that second opinions, critics, subagents, metareasoning, verification planning, or multi-agent systems are new.

The candidate contribution is the composition:

1. the Primary keeps the global task;
2. one isolated peer receives only one local problem;
3. the peer does not need to be stronger than the Primary;
4. communication is compressed through a BROTLI reasoning-state packet rather than a full-context dump by default;
5. the peer explicitly performs **Consequence-Chain Completion**;
6. it may answer `OK`, `LOOK_AGAIN`, or `WARNING`;
7. advice is non-authoritative;
8. the Primary acknowledges the advice but keeps agency;
9. one decision gets one bounded second thought;
10. no recursive debate follows.

The strongest practical hypothesis is deliberately simple:

```text
limited task-focused Primary
+
limited local Second-Thought Peer
>
limited task-focused Primary alone
```

Not because two weak agents magically become strong, but because the second agent temporarily has only **one thing** to think about.

---

## Premature Local Closure

ChomView targets five local failure classes:

| PLC class | Typical failure |
|---|---|
| Interpretation Closure | An observation is assigned one meaning too quickly |
| Solution Closure | A local fix is accepted without considering displaced complexity |
| Consequence Closure | Immediate effect is considered, downstream effects are not |
| Verification Closure | A real check proves less than the Primary believes |
| Completion Closure | `done` / `verified` / `fixed` is stronger than the supporting evidence |

**Consequence Closure is the primary ChomView target.**

---


## Behavioral Integrity

ChomView v0.2 extends PLC handling with **Behavioral Integrity** checks derived from observed agent failures:

- substantive objective vs procedural completion;
- evidence strength vs claim strength;
- real/source-backed requirements vs plausible substitutes;
- explanation vs exoneration;
- acknowledgement vs actual correction;
- repeated materially similar failures after acknowledgement.

The key operational rule is:

```text
acknowledgement without a changed future decision rule is not correction
```

See [`references/behavioral-integrity.md`](references/behavioral-integrity.md).

---

## Behavioral Compatibility — v0.4

ChomView v0.4 extends Behavioral Continuity to heterogeneous and routed agents. The core rule is:

```text
wild cognition != wild authority
```

Agents may differ in model family, training, style, internal heuristics, initiative, or cultural priors. ChomView does **not** try to make them think alike. It applies the same explicit host-system boundaries to all of them:

```text
personality != permission
capability != permission
availability != authorization
preference != spending authority
```

A project-local behavioral contract can bind concrete tool actions to stakeholders and protected resources and return:

```text
ALLOW | LOOK_AGAIN | REQUIRE_CONSENT | BLOCK
```

This makes it possible to let an unusual agent reason freely while still requiring owner consent before it spends protected money/tokens, crosses an execution boundary, or performs another explicitly governed action.

The contract is deterministic where configured. ChomView does not infer moral, cultural, or personality "normality".

See [`references/behavioral-compatibility.md`](references/behavioral-compatibility.md).

---
## BROTLI/1

ChomView communicates with a compact semantic packet called **BROTLI/1**.

For this project, BROTLI means:

> **Bounded Reasoning-Oriented Transfer for Local Intervention**

It is a reasoning-state protocol, not a requirement to transmit raw chain-of-thought. It sends only decision-relevant state:

```text
purpose
local situation
Primary intent
concise rationale
relevant facts
relevant constraints
known uncertainty
expected immediate effect
```

The peer returns:

```text
OK | LOOK_AGAIN | WARNING
missing consideration
short consequence chain
advice
smallest useful check
optional insufficient check
confidence
```

See [`references/brotli-protocol.md`](references/brotli-protocol.md).

---

## Consequence-Chain Completion

The Primary often reasons far enough to get:

```text
A -> B
```

The Second-Thought Peer asks what materially follows:

```text
A -> B -> C -> D
```

It does **not** simulate an unlimited future.

It stops when either:

- no further material consequence is reasonably identifiable; or
- one consequence is important enough to change the local action, confidence, verification, or completion claim.

See [`references/consequence-chain-completion.md`](references/consequence-chain-completion.md).

---

## Example

Primary:

```text
Provider returned NULL.
I'll persist 0 and continue.
```

Second thought:

```text
stance: WARNING
concern: HIGH

missing:
NULL may encode provider failure while 0 may be valid business data.

chain:
NULL -> 0 -> semantic information loss -> downstream consumer sees factual zero

advice:
Preserve distinct states unless provider semantics prove equivalence.

check:
Confirm NULL semantics and inspect one downstream consumer.

insufficient:
Testing only that the exception disappeared.
```

The peer does not take over implementation. The Primary decides what to do next.

More examples: [`references/examples.md`](references/examples.md).

---

## Hard boundaries

For one local decision:

```text
peer_deliberations <= 1
context_requests <= 1
peer_spawn_depth = 0
debate_rounds = 0
```

The peer is read-oriented and should not mutate the parent project by default.

`OK` is a valid successful result. ChomView is not rewarded for finding objections.

---

## Repository structure

The GitHub repository is intentionally a **visible portable source distribution**. Runtime-specific dot-directories are created only when ChomView is installed into a target Claude Code project. This keeps the repository uploadable even from file pickers that hide dot-directories.

```text
chomview/
├── SKILL.md
├── README.md
├── LICENSE
├── NOTICE
├── THIRD_PARTY_NOTICES.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
│
├── references/
│   ├── activation-cues.md
│   ├── behavioral-integrity.md
│   ├── behavioral-compatibility.md
│   ├── brotli-protocol.md
│   ├── chomview-paper.md
│   ├── consequence-chain-completion.md
│   ├── evaluation-protocol.md
│   ├── examples.md
│   └── prior-art-and-claims.md
│
├── schemas/
│   ├── acknowledgement.schema.json
│   ├── behavioral-contract.schema.json
│   ├── brotli-request.schema.json
│   ├── brotli-response.schema.json
│   └── correction-rule.schema.json
│
├── config/
│   └── behavioral-contract.default.json
│
├── runtime/
│   └── chomview_guard.py
│
├── agents/
│   └── chomview-second-thought.md
│
├── tests/
│   ├── behavioral-cases.md
│   ├── runtime/
│   │   ├── test_chomview_guard.py
│   │   └── test_behavioral_contract.py
│   └── evals/
│       ├── README.md
│       └── EVAL-001 ... EVAL-004/
│
└── scripts/
    ├── build_treatment_manifest.py
    ├── configure_claude_hooks.py
    ├── install-claude-code.ps1
    ├── install-claude-code.sh
    └── validate_repo.py
```

After installation into a Claude Code project, the relevant files are placed at the native Claude Code locations:

```text
TARGET_PROJECT/
└── .claude/
    ├── skills/
    │   └── chomview/
    │       ├── SKILL.md
    │       ├── references/
    │       └── schemas/
    ├── agents/
    │   └── chomview-second-thought.md
    └── chomview/
        ├── chomview_guard.py
        ├── behavioral-contract.json
        ├── corrections.json
        └── events.jsonl
```

---

## Installation

### Portable Agent Skill source

The repository root is the portable ChomView source package: `SKILL.md`, its progressive-disclosure references, its schemas, and the visible peer definition under `agents/`. A runtime may package or register these files using its own Agent Skills mechanism.

### Claude Code project installation

Claude Code discovers project skills under `.claude/skills/<name>/SKILL.md` and project subagents under `.claude/agents/*.md`. The included installer creates those native target paths for you.

PowerShell:

```powershell
./scripts/install-claude-code.ps1 -ProjectPath C:\path\to\project
```

Bash:

```bash
./scripts/install-claude-code.sh /path/to/project
```

The installer copies:

```text
SKILL.md + references + schemas
    -> TARGET_PROJECT/.claude/skills/chomview/

agents/chomview-second-thought.md
    -> TARGET_PROJECT/.claude/agents/chomview-second-thought.md

runtime/chomview_guard.py
    -> TARGET_PROJECT/.claude/chomview/chomview_guard.py

config/behavioral-contract.default.json
    -> TARGET_PROJECT/.claude/chomview/behavioral-contract.json (only if absent)
```

An existing behavioral contract is preserved on reinstall. The installer also configures the SessionStart, UserPromptSubmit, and PreToolUse hooks required by the guard. It does not modify unrelated project files.

### Manual Claude Code installation

If you do not want to run the installer, create the same target directories and copy the files exactly as shown above. The dot-directories are required in the **target Claude Code project**, not in this source repository.

---

## Validation

Run:

```bash
python scripts/validate_repo.py
```

The validator checks:

- required repository files;
- `SKILL.md` frontmatter;
- Skill line count;
- BROTLI JSON schemas;
- Second-Thought agent frontmatter;
- expected research/reference files;
- v0.4 behavioral-contract files and treatment hashes;
- exactly one active source `SKILL.md`;
- absence of `__pycache__` / `.pyc` residue and known flattened duplicate paths.

The same validator can be used from CI if you add a repository workflow later.

---

## Behavioral tests

The repository contains behavior-level acceptance cases for:

- semantic default traps;
- harmless trivial fixes that should return `OK`;
- deployment completion claims;
- special-case branches with downstream complexity;
- retry/idempotency risk;
- research closure;
- insufficient verification;
- overthinking protection.

See [`tests/behavioral-cases.md`](tests/behavioral-cases.md).

---

## Research status

ChomView is **experimental**.

The repository contains a scientific concept paper and evaluation protocol, and v0.4.0 still does not claim an independent peer-performance uplift or confirmatory efficacy for Behavioral Compatibility. Historical-fork EVAL-004 produced a behavioral-policy signal: ChomView-derived checks corrected 4/4 selected historical failures both as policy-guided self-reconsideration and as a peer intervention; peer-specific uplift remains unestablished.

The core falsifiable question is:

> **Can one bounded second thought from another limited reasoner reduce consequential local mistakes made by a task-focused agent at a cost low enough to be worthwhile?**

The strongest negative result would be that ordinary bounded self-reconsideration or conventional independent review produces the same benefit more cheaply.

See:

- [`references/chomview-paper.md`](references/chomview-paper.md)
- [`references/evaluation-protocol.md`](references/evaluation-protocol.md)
- [`references/prior-art-and-claims.md`](references/prior-art-and-claims.md)

---

## Conceptual prior art

ChomView is independently written and does not claim invention of its individual ingredients.

Relevant neighboring ideas include:

- SOAR and impasse-driven subgoaling;
- bounded rationality and value-of-computation / metareasoning;
- Self-Refine;
- Reflexion;
- Devil's Advocate / anticipatory reflection;
- independent review patterns such as Agent Rigor;
- comparison-only runtime advisors such as COTA;
- test-suite reduction and cost-aware verification;
- multi-agent reliability and failure research.

See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) and [`references/prior-art-and-claims.md`](references/prior-art-and-claims.md).

---

## Roadmap

### v0.2 — Behavioral Integrity

- [x] PLC taxonomy and bounded Second-Thought Peer
- [x] BROTLI/1 and Consequence-Chain Completion
- [x] intent/evidence/substitution/rationalization checks

### v0.3 — Behavioral Continuity

- [x] persistent correction rules
- [x] `NOTICE -> WARNING -> STRIKE -> FREEZE -> ESCALATE`
- [x] SessionStart/UserPromptSubmit continuity injection
- [x] deterministic recurrence enforcement before tool use

### v0.4 — Behavioral Compatibility

- [x] `wild cognition != wild authority`
- [x] heterogeneous-agent behavioral contract
- [x] stakeholder and protected-resource metadata
- [x] actor-scoped deterministic matchers
- [x] `ALLOW | LOOK_AGAIN | REQUIRE_CONSENT | BLOCK`
- [x] preserve owner-edited contract across reinstall
- [x] packaging hygiene gate against flattened duplicates/build residue

### Next

- [x] run initial historical local-failure replays (EVAL-004)
- [ ] add B0 generic-reconsideration control against B1 policy and D peer
- [ ] add benign minimal-decision control cases
- [ ] measure Primary-only vs bounded self-reconsideration vs ChomView
- [ ] measure ignored-warning behavior
- [ ] measure rework-adjusted token cost
- [ ] test same-model low-cost Primary + peer first
- [ ] evaluate manual vs rule-based activation
- [ ] test weaker and stronger peer configurations only after core effect is established
- [ ] evaluate P2P runtime integration and compressed transport

---

## What ChomView is not

ChomView is not:

- a global governor;
- a mandatory approval gate;
- a truth oracle;
- a recursive critic loop;
- a multi-agent debate framework;
- a replacement for project context;
- a claim that two agents are always better than one;
- a personality police or cultural-normalization layer;
- a universal moral authority.

It is one bounded local second thought.

---

## License

Apache License 2.0.

See [`LICENSE`](LICENSE).

---

<p align="center">
  <strong>Keep moving. But look once more before you walk past the consequence.</strong>
</p>
