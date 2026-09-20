---
name: chomview
description: Provides one bounded consequence-aware second thought for consequential local decisions during agentic work. Use when a task-focused primary is about to close an ambiguous decision, workaround, fallback, verification claim, completion claim, or other local issue whose downstream consequences may be underconsidered.
---

# ChomView

ChomView adds one bounded, non-authoritative second thought to a task-focused Primary.

The Primary keeps the global task. The Second-Thought Peer (STP) receives only one local problem, thinks that problem through further, returns a compact intervention, and stops.

Use ChomView to reduce **Premature Local Closure (PLC)**: locally treating an issue as resolved before a materially relevant assumption, consequence, alternative, verification need, or completion condition has been considered enough.

## Core rule

The Primary asks:

> What lets me continue the task?

The STP asks:

> What has not been thought through in this one local decision?

Do not turn the STP into another Primary.

## Roles

### Primary

The Primary:

- owns the global objective;
- keeps the main context;
- plans, researches, codes, acts, and uses tools;
- integrates results;
- makes the final decision;
- remains responsible for completion.

Assume the Primary may be imperfect. It may lose context, overestimate local certainty, prefer immediate progress, underestimate consequences, choose weak verification, or make completion claims stronger than its evidence.

### Second-Thought Peer

The STP:

- owns no global task;
- receives one local situation;
- reasons only about that situation;
- extends the local consequence horizon;
- may expose an assumption, alternative, consequence, or weak completion claim;
- may recommend one or more concrete checks;
- may say `OK`;
- returns control immediately.

The STP must not:

- redesign the whole project;
- perform general code review;
- start a debate;
- recursively invoke itself;
- spawn another critic or judge;
- mutate the project by default;
- demand the complete task history;
- manufacture criticism merely because it was invoked.

## PLC classes

ChomView targets five local closure failures:

1. **Interpretation Closure** — an observation is given one meaning too quickly.
2. **Solution Closure** — a locally working fix is accepted without considering displaced complexity.
3. **Consequence Closure** — the immediate effect is considered, but relevant second-order effects are not.
4. **Verification Closure** — a real check is performed, but it proves less than the Primary believes.
5. **Completion Closure** — the Primary claims `done`, `verified`, `fixed`, or equivalent with support weaker than the claim.

Prioritize **Consequence Closure**. ChomView exists primarily to think one local consequence chain further than the Primary currently has.

## When to invoke

Invoke ChomView when a local decision is both non-trivial and plausibly consequential.

Strong cues include:

- ambiguous states such as null, missing, empty, timeout, partial, stale, unknown, or error;
- fallback or default values;
- special-case branches;
- workarounds or bypasses;
- duplicated logic;
- "quick fix" or "smallest change" reasoning with semantic consequences;
- retry or idempotency decisions;
- schema, interface, dependency, or state-model changes;
- irreversible or external side effects;
- a claim such as `tested`, `verified`, `works`, `fixed`, `production ready`, or `done`;
- research conclusions based on sparse, repeated, ambiguous, or conflicting evidence;
- repeated failure followed by another patch around the same issue;
- any case where the Primary appears locally certain while the downstream consequence is unclear.

Do not invoke merely because a decision exists.

Normally skip:

- formatting;
- typo correction with no semantic impact;
- purely mechanical transformations;
- reversible clerical actions;
- negligible local decisions;
- a `decision_id` already subjected to ChomView.

## Local Thought Packet

Do not copy the complete task context.

Build one compact **BROTLI/1 REQUEST** containing only decision-relevant semantic state.

Required conceptual fields:

```text
mid: unique message id
tid: global task id
did: stable local decision id

purpose:
  1-3 short sentences describing what fundamentally matters in the parent task

situation:
  what happened locally

intent:
  what the Primary is about to do or claim

rationale:
  concise reason why the Primary currently thinks this is adequate

facts:
  directly relevant observations only

constraints:
  directly relevant constraints only

uncertainty:
  known uncertainty or "none stated"

immediate_effect:
  what the Primary expects to happen next
```

Do not send raw private chain-of-thought. Send a concise rationale summary, claims, facts, assumptions, and intended action.

Prefer references over large copied evidence.

See `references/brotli-protocol.md` for the full protocol.

## Peer invocation

Send the BROTLI packet directly to the isolated ChomView STP.

The STP should reason using **Consequence-Chain Completion (CCC)**:

```text
Primary often stops at:
A -> B

STP asks:
A -> B -> C -> D ?
```

Continue only while the chain remains materially relevant.

Stop when either:

1. no further material consequence is reasonably identifiable; or
2. a consequence appears that should change the action, confidence, verification, or completion claim.

Do not simulate unlimited futures.

See `references/consequence-chain-completion.md`.

## Peer outputs

The STP returns exactly one final stance:

- `OK`
- `LOOK_AGAIN`
- `WARNING`

Preferred response fields:

```text
reply_to: request message id
did: same decision id

stance: OK | LOOK_AGAIN | WARNING
concern: NONE | LOW | MATERIAL | HIGH

missing:
  what the Primary may not have considered

chain:
  short material consequence chain

advice:
  what the Primary should consider doing; may be "keep current plan"

check:
  one or a small number of useful checks before moving on

insufficient:
  optional tempting check that would not establish enough

why:
  why the concern matters to the purpose anchor

confidence:
  LOW | MEDIUM | HIGH
```

`OK` is success. Never invent a problem simply to justify the peer call.

`LOOK_AGAIN` is also a complete result. The STP may identify that the Primary is closing too cheaply without solving the local problem itself.

Use `WARNING` only when a plausible material consequence can be stated causally.

Avoid vague warnings such as "this might cause issues later."

## One targeted context request

If exactly one decisive fact is missing, the STP may return one `BROTLI/1 NEED` request:

```text
need:
  one precise factual request

reason:
  why this fact changes the local judgment
```

Provide only the requested fact or artifact fragment.

Do not respond by dumping the full task history.

Default v0.1 invariants:

```text
peer_deliberations(did) <= 1
context_requests(did) <= 1
peer_spawn_depth = 0
debate_rounds = 0
```

After a `NEED`, the peer returns one final response and stops.

## Primary acknowledgement

Advice is non-authoritative.

For `LOOK_AGAIN` or `WARNING`, the Primary must consciously process the intervention and record:

```text
response: ADOPT | ADAPT | DECLINE
reason: one concise sentence
```

No second STP round follows automatically.

The Primary keeps the right to reject the advice.

## Completion-claim check

When the Primary makes a strong completion claim, compare:

```text
CLAIM
vs.
ACTUAL SUPPORT
```

Ask:

1. What exactly was observed?
2. What does that observation establish?
3. Is the claim stronger than the observation?

Examples:

```text
command exited 0
!=
deployment is serving the new version
```

```text
unit test passed
!=
integration path works
```

```text
code exists
!=
feature is operational
```

Do not accuse the Primary of deception. Treat this as unsupported claim strength.

## Research-closure check

For research tasks, ask:

> Does the available evidence establish the conclusion, or merely make it plausible?

Watch for:

- same-source repetition;
- secondary sources with one shared origin;
- missing disconfirming evidence;
- extrapolation beyond population, scope, or time period;
- confident conclusions from ambiguous evidence.

Do not redo the full research task. Identify the local evidence or consequence gap.

## Scope discipline

Do not transform:

> "Should we add this fallback?"

into:

> "Let me redesign the system."

Reduce broad concerns to the local consequence relevant to the current decision.

Prefer:

> "This fallback creates a second semantic representation of the same state. Check whether the existing normalization layer already owns that distinction."

not:

> "The whole architecture is wrong."

## Model selection

ChomView must not require a stronger model.

Default research configuration:

```text
Primary model class == STP model class
```

A runtime may use a cheaper, equal, stronger, or cross-family peer, but do not automatically escalate to an expensive model.

The defining property is role separation, not model superiority.

## Tool use

Prefer reasoning from the local packet.

The STP may perform narrow read-only inspection when necessary, for example:

- one referenced function;
- one API contract;
- one test;
- one log segment.

Do not let the STP:

- execute the parent task;
- perform broad repository exploration;
- edit files;
- deploy;
- mutate external systems;
- launch broad web research by default.

## Cost discipline

ChomView is intended for low-cost agents.

Prefer:

- small packets;
- short peer responses;
- one peer pass;
- reference-based evidence;
- targeted context acquisition;
- same or inexpensive model classes.

Avoid:

- full-context duplication;
- persistent group chat;
- multi-agent debate;
- recursive verification;
- automatic expert escalation.

## Fallback mode

If no isolated peer/subagent runtime exists, the Primary may perform one self-second-thought using the same packet.

Mark it explicitly:

```text
mode: SELF_FALLBACK
```

Do not treat self-fallback as equivalent to genuine ChomView P2P operation.

## Runtime flow

```text
Primary works normally
        |
        v
consequential local decision
        |
        v
create stable did
        |
        v
build minimal BROTLI packet
        |
        v
send to isolated STP
        |
        +-- NEED --> provide one precise fact --+
        |                                        |
        +<---------------------------------------+
        |
        v
OK / LOOK_AGAIN / WARNING
        |
        v
Primary ADOPT / ADAPT / DECLINE
        |
        v
continue global task
```

## Final rule

ChomView is not:

> Find something wrong.

ChomView is:

> The Primary has the whole task. You have this one thing. Think this one thing through far enough that the Primary does not walk past an important consequence.

Then return control.

## References

Load only when needed:

- `references/brotli-protocol.md` — full packet semantics and compression rules
- `references/consequence-chain-completion.md` — CCC method
- `references/activation-cues.md` — invocation heuristics
- `references/examples.md` — worked examples
- `references/evaluation-protocol.md` — falsifiable experimental plan
- `references/chomview-paper.md` — scientific basis
- `references/prior-art-and-claims.md` — novelty and claim boundaries
