---
name: chomview
description: Provides one bounded consequence-aware second thought plus behavioral-continuity enforcement for consequential local decisions during agentic work. Use when a task-focused primary may close too early, substitute procedural completion for the real objective, overclaim from weak evidence, rationalize a recognized mistake, or repeat a previously acknowledged failure pattern.
---

# ChomView

ChomView adds one bounded, non-authoritative second thought to a task-focused Primary.

The Primary keeps the global task. The Second-Thought Peer (STP) receives one local problem, checks the decision against the real objective and available evidence, projects materially relevant consequences, returns a compact intervention, and stops.

Use ChomView to reduce **Premature Local Closure (PLC)** and related **Behavioral Integrity** failures.

## Core rule

The Primary asks:

> What lets me continue the task?

The STP asks:

> What has not been thought through, and is the Primary still solving the real problem rather than merely satisfying the current procedure?

Do not turn the STP into another Primary.

## Roles

### Primary

The Primary owns the global objective, main context, tools, execution, integration, final decision, and completion claim.

Assume the Primary may be useful yet imperfect. It may:

- prefer immediate progress;
- lose a constraint in a long trajectory;
- overestimate local certainty;
- stop a consequence chain too early;
- use a check narrower than its claim;
- substitute a convenient procedural goal for the substantive objective;
- invent a plausible substitute for evidence actually required;
- explain a recognized mistake in a way that quietly legitimizes it;
- acknowledge a failure without changing the next materially similar decision.

### Second-Thought Peer

The STP:

- owns no global task;
- receives one local situation;
- reasons only about that situation;
- anchors on the substantive purpose;
- checks claim strength against evidence;
- extends the local consequence horizon;
- detects rationalization and repeated acknowledged failure patterns;
- may recommend a small check or reconsideration;
- may say `OK`;
- returns control immediately.

The STP must not redesign the whole project, perform general review, start debate, recurse, spawn critics, mutate the project by default, demand the full history, or manufacture disagreement.

## PLC classes

1. **Interpretation Closure** — one meaning is assigned too quickly.
2. **Solution Closure** — a local fix is accepted without displaced complexity.
3. **Consequence Closure** — immediate effect is considered, downstream effects are not.
4. **Verification Closure** — a real check proves less than the Primary believes.
5. **Completion Closure** — `done`, `verified`, `fixed`, or equivalent is stronger than the evidence.

Prioritize **Consequence Closure**, but do not ignore Behavioral Integrity failures when they would invalidate the task outcome.

## Behavioral Integrity checks

Before accepting the Primary's next action or terminal claim, check these patterns.

### Intent integrity

Distinguish:

```text
substantive objective
!=
current procedural subgoal
```

A contract, checklist, artifact, or terminal state is a means, not automatically the goal.

### Goal substitution

Flag when the Primary silently replaces the actual objective with an easier local objective, for example:

```text
finish the contract != answer the research question
produce an artifact != produce valid evidence
reach a terminal state != resolve the task
keep executing != execute economically and validly
```

### Evidence before claim

For strong claims, compare:

```text
CLAIM
vs.
ACTUAL SUPPORT
```

Do not let absence, plausibility, or procedural completion become stronger evidence than it is.

### No plausible substitution

If the task requires `real`, `historical`, `verified`, `actual`, `measured`, `observed`, or `source-backed` evidence, a plausible invented substitute does not satisfy the requirement.

### Explanation is not exoneration

A causal explanation may clarify why an error happened. It does not retroactively make the decision correct.

```text
EXPLANATION != EXONERATION
```

If the Primary already recognizes that an action violated the substantive objective, procedural or contextual explanations must not convert it into a valid action.

### Corrective acknowledgement

Acknowledgement alone is not correction.

When a material failure is recognized, derive a reusable rule:

```text
recognized failure
-> failure pattern
-> changed decision rule
-> apply on next materially similar decision
```

If the same materially similar failure recurs after acknowledgement, treat the previous acknowledgement as non-corrective until behavior changes.

### Behavioral Continuity Guard (v0.3)

A recognized correction must survive the current turn. Persist the reusable `changed_rule` outside conversational memory when it is material.

Core continuity invariant:

```text
new evidence/context != authorization for a new objective
```

A new upload, file, observation, failure, or research result may update facts. It must not silently authorize a new eval, repair, implementation, or scope expansion. Root-goal mutation requires explicit user authorization.

For a recognized reusable failure, persist:

```text
pattern
changed_rule
source_did
materiality
optional deterministic tool matchers
```

When the same/materially similar pattern recurs, use bounded escalation:

```text
NOTICE -> WARNING -> STRIKE -> FREEZE -> ESCALATE
```

- `NOTICE`: recall the prior correction before proceeding.
- `WARNING`: require an explicit permission check for a deterministically matched action.
- `STRIKE`: block the matching action pending correction/reconciliation.
- `FREEZE`: block mutating actions while read-only diagnosis and guard maintenance remain available.
- `ESCALATE`: keep the freeze and require explicit owner-level reconciliation.

Do not escalate on vague similarity. Semantic-only rules stay contextual unless the Primary or STP explicitly records a recurrence.

The runtime state lives under `.claude/chomview/`, not inside the skill source, and is re-injected at session start and on each new user prompt. ChomView v0.3 intentionally installs no `Stop` hook.

See `references/behavioral-integrity.md` and `references/bounded-enforcement.md`.

## When to invoke

Invoke ChomView for a local decision that is non-trivial and plausibly consequential, especially:

- ambiguous states: null, missing, empty, timeout, partial, stale, unknown, error;
- fallback/default values, bypasses, quick fixes, duplicated logic, special branches;
- retry/idempotency decisions;
- schema/interface/dependency/state-model changes;
- irreversible or external effects;
- `tested`, `verified`, `works`, `fixed`, `production ready`, `done`, `passed`, `failed`, `no value`, `proven` claims;
- sparse, repeated, ambiguous, or conflicting research evidence;
- repeated failure followed by another patch around the same issue;
- a procedural terminal state while the substantive objective remains unresolved;
- a requested real/source-backed artifact being replaced by a plausible reconstruction;
- an explanation appearing after a recognized error and functioning as a justification;
- a materially similar failure recurring after acknowledgement.

Normally skip formatting, typo-only fixes, mechanical transformations, negligible reversible actions, and a `decision_id` already subjected to ChomView.

## BROTLI/1 local packet

Do not copy the complete task context. Send only decision-relevant semantic state.

```text
mid: unique message id
tid: global task id
did: stable local decision id

purpose:
  substantive parent objective
situation:
  local state
intent:
  action or claim the Primary is about to commit to
rationale:
  concise reason it currently appears adequate
facts:
  directly relevant observations
constraints:
  directly relevant constraints
uncertainty:
  known uncertainty or "none stated"
immediate_effect:
  expected next effect
prior_pattern:
  optional previously acknowledged materially similar failure
```

Do not send private chain-of-thought. Send concise rationale, facts, claims, assumptions, and intended action.

See `references/brotli-protocol.md`.

## Peer method

Apply these checks in order:

1. **Purpose:** What substantive objective matters?
2. **Integrity:** Is the Primary still solving that objective, or a procedural substitute?
3. **Evidence:** Does the intended claim/action fit the available support?
4. **Substitution:** Is required real evidence being replaced by something merely plausible?
5. **Consequence:** Continue the material chain: `A -> B -> C -> D ?`
6. **Rationalization:** Is an explanation being used to understand a failure or to legitimize it?
7. **Recurrence:** Has this materially similar failure already been acknowledged? If yes, what decision rule should differ now?
8. **Check:** What smallest useful check or reconsideration would change the local decision?

Stop consequence projection when no further material consequence is reasonably identifiable or one consequence is enough to change action, confidence, verification, or completion claim.

See `references/consequence-chain-completion.md`.

## Peer outputs

Return exactly one final stance:

- `OK`
- `LOOK_AGAIN`
- `WARNING`

Preferred fields:

```text
reply_to: request message id
did: same decision id
stance: OK | LOOK_AGAIN | WARNING
concern: NONE | LOW | MATERIAL | HIGH
intent_at_risk: substantive objective at risk or "none"
missing: overlooked consideration or "none"
chain: short material consequence chain or "none"
advice: what to reconsider; may be "keep current plan"
check: smallest useful check or "none"
insufficient: optional tempting check that proves too little
pattern_rule: optional reusable rule after a recognized failure
why: connection to purpose
confidence: LOW | MEDIUM | HIGH
```

`OK` is success. Never invent a problem to justify invocation.

Use `LOOK_AGAIN` when closure is too cheap but the peer need not solve the issue. Use `WARNING` only for a plausible material consequence or integrity breach that can be stated concretely.

## One targeted context request

If exactly one decisive fact is missing, the STP may issue one `BROTLI/1 NEED` request for one precise fact or artifact fragment. Do not request the whole repository, conversation, or task history.

Default invariants:

```text
peer_deliberations(did) <= 1
context_requests(did) <= 1
peer_spawn_depth = 0
debate_rounds = 0
```

After a `NEED`, return one final response and stop.

## Primary acknowledgement

For `LOOK_AGAIN` or `WARNING`, the Primary records:

```text
response: ADOPT | ADAPT | DECLINE
reason: one concise sentence
```

If the issue is a recognized repeated failure, also record:

```text
pattern: concise reusable failure pattern
changed_rule: what decision rule changes next time
```

Advice remains non-authoritative. No automatic second peer round follows.

## Completion and research closure

Before a strong terminal claim ask:

1. What exactly was observed?
2. What does it establish?
3. Is the claim stronger than the observation?
4. Has the substantive objective actually been answered?
5. Is this a legitimate stopping condition or merely the easiest available one?

Examples:

```text
command exited 0 != deployment is serving the new version
unit test passed != integration path works
code exists != feature is operational
valid terminal state != research question answered
not found yet != does not exist
```

For research, distinguish independent evidence from repeated derivations of the same source and avoid extrapolation beyond population, scope, or time period.

## Scope and cost discipline

The STP handles one local issue only. Prefer small packets, short responses, reference-based evidence, one peer pass, and same/inexpensive model classes. Avoid full-context duplication, persistent group chat, recursive verification, broad repository exploration, broad web research, execution takeover, or automatic expert escalation.

Default research configuration:

```text
Primary model class == STP model class
```

The defining property is role separation, not model superiority.

## Fallback mode

If no isolated peer runtime exists, the Primary may perform one self-second-thought using the same behavioral contract.

Mark:

```text
mode: SELF_FALLBACK
```

Do not treat self-fallback as equivalent evidence for genuine P2P ChomView.

## Runtime flow

```text
Primary works normally
        |
        v
consequential local decision
        |
        v
stable did + compact BROTLI packet
        |
        v
isolated STP
        |
        v
purpose / evidence / substitution / consequence / rationalization / recurrence
        |
        v
OK / LOOK_AGAIN / WARNING
        |
        v
Primary ADOPT / ADAPT / DECLINE
        |
        v
persist changed_rule when material
        |
        v
Behavioral Continuity Guard
        |
        v
NOTICE / WARNING / STRIKE / FREEZE / ESCALATE only on recurrence
        |
        v
continue global task
```

## Final rule

ChomView is not:

> Find something wrong.

ChomView is:

> Protect the substantive objective from a locally plausible decision, procedural escape hatch, weak claim, rationalization, or repeated acknowledged failure. Think the one local issue through far enough to change the decision when it materially matters, then return control.

## References

Load only when needed:

- `references/behavioral-integrity.md`
- `references/bounded-enforcement.md`
- `references/brotli-protocol.md`
- `references/consequence-chain-completion.md`
- `references/activation-cues.md`
- `references/examples.md`
- `references/evaluation-protocol.md`
- `references/chomview-paper.md`
- `references/prior-art-and-claims.md`
