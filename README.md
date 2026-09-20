# ChomView

<p align="center">
  <strong>One agent keeps moving. One peer briefly looks at what it is about to overlook.</strong><br>
  A bounded second-thought skill for task-focused AI agents.
</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/license-Apache--2.0-blue">
  <img alt="Status" src="https://img.shields.io/badge/status-experimental-orange">
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-green">
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
│   ├── brotli-protocol.md
│   ├── chomview-paper.md
│   ├── consequence-chain-completion.md
│   ├── evaluation-protocol.md
│   ├── examples.md
│   └── prior-art-and-claims.md
│
├── schemas/
│   ├── acknowledgement.schema.json
│   ├── brotli-request.schema.json
│   └── brotli-response.schema.json
│
├── tests/
│   └── behavioral-cases.md
│
├── scripts/
│   ├── install-claude-code.ps1
│   ├── install-claude-code.sh
│   └── validate_repo.py
│
├── .claude/
│   └── agents/
│       └── chomview-second-thought.md
│
└── .github/
    ├── workflows/
    │   └── validate.yml
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.yml
    │   └── research_finding.yml
    └── PULL_REQUEST_TEMPLATE.md
```

---

## Installation

### Agent Skills-compatible runtime

The repository root is an Agent Skill package because `SKILL.md` lives at the root. Install or register the repository directory according to your runtime's Agent Skills mechanism.

### Claude Code project installation

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
    -> .claude/skills/chomview/

.claude/agents/chomview-second-thought.md
    -> .claude/agents/chomview-second-thought.md
```

It does not modify unrelated project files.

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
- expected research/reference files.

The same validation runs automatically in GitHub Actions.

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

The repository contains a scientific concept paper and evaluation protocol, but v0.1.0 does not claim that ChomView has already demonstrated an independent performance uplift.

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

### v0.1.x — Behavioral contract

- [x] PLC taxonomy
- [x] Second-Thought Peer role
- [x] BROTLI/1 request/response protocol
- [x] Consequence-Chain Completion
- [x] non-authoritative acknowledgement
- [x] hard single-pass boundaries
- [x] read-only Claude Code peer agent
- [x] behavioral cases
- [x] repository validation

### Next

- [ ] run historical local-failure replays
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
- a claim that two agents are always better than one.

It is one bounded local second thought.

---

## License

Apache License 2.0.

See [`LICENSE`](LICENSE).

---

<p align="center">
  <strong>Keep moving. But look once more before you walk past the consequence.</strong>
</p>
