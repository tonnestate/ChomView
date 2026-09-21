# Bounded Enforcement — Behavioral Continuity Guard

ChomView v0.3 adds a bounded enforcement layer for a specific failure mode: the Primary recognizes a material mistake, states the right correction, and later repeats the same materially similar decision pattern.

The mechanism is not punishment. It is state continuity for an already-established correction.

## Contract

A correction becomes enforceable only when all of the following are true:

1. a material failure or integrity breach was recognized;
2. the failure pattern is reusable rather than a one-off detail;
3. a concise `changed_rule` exists;
4. the later event is materially similar to that pattern;
5. applying the old behavior again would matter to the substantive objective.

Do not escalate merely because a new situation looks vaguely similar.

## Persistence

The project-local guard stores correction state outside the conversation in:

```text
.claude/chomview/corrections.json
.claude/chomview/events.jsonl
```

`SessionStart` and `UserPromptSubmit` hooks re-inject active rules into Claude's context. This makes a correction survive fresh turns, resumed sessions, uploaded evidence, and ordinary conversational drift.

A core v0.3 invariant is always present:

```text
new evidence/context != authorization for a new objective
```

New evidence may update facts. It does not silently authorize a new eval, repair, implementation, or scope expansion.

## Escalation

For a deterministic matcher attached to a previously acknowledged rule, recurrence escalates monotonically:

```text
NOTICE -> WARNING -> STRIKE -> FREEZE -> ESCALATE
```

- `NOTICE`: inject the prior rule and allow the normal permission flow to continue.
- `WARNING`: force an explicit permission check before the matching tool call.
- `STRIKE`: block the matching action until it is corrected/reconciled.
- `FREEZE`: block mutating tool calls while keeping read-only diagnosis and guard-maintenance available.
- `ESCALATE`: maintain the freeze and require explicit owner-level reconciliation before continuation.

Resolution resets the recurrence counter only when evidence of correction/reconciliation is recorded. It does not delete the rule.

## Semantic-only rules

Not every behavioral rule can be reduced safely to a regex. A rule without deterministic matchers is still persisted and injected as context, but the guard does not pretend to solve semantic similarity mechanically.

When the Primary or Second-Thought Peer detects a semantic recurrence, it records the recurrence explicitly with the guard. The deterministic state machine then owns escalation.

## No stop-loop enforcement

v0.3 deliberately does **not** install a `Stop` hook. Enforcement happens at session/prompt context injection and before mutating tool calls. This avoids turning an ill-specified completion condition into a self-repeating stop loop.

## Claude Code integration

The implementation uses Claude Code's documented hook lifecycle:

- `SessionStart` to restore persistent correction context;
- `UserPromptSubmit` to place active rules next to new evidence/instructions;
- `PreToolUse` to enforce deterministic recurrences before side effects.

Reference: https://code.claude.com/docs/en/hooks
