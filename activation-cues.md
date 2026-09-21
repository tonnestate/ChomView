# Activation Cues

Activation is deliberately separated from the core ChomView hypothesis.

The first question is whether the STP adds value when invoked. Routing sophistication should come later.

## High-value cues

### Ambiguous interpretation

Invoke when the Primary assigns meaning to:

- null;
- empty;
- timeout;
- partial;
- unknown;
- stale;
- missing;
- error-like states.

### Shortcut language

Strong cues:

- "quick fix";
- "smallest change";
- "just default it";
- "ignore for now";
- "temporary workaround";
- "special case";
- "catch and continue".

These phrases are not errors by themselves. They indicate a useful consequence check.

### State or contract change

Invoke around:

- schema changes;
- interface changes;
- dependency changes;
- state-machine changes;
- retry behavior;
- idempotency;
- external writes;
- destructive operations.

### Strong claims

Invoke before material claims such as:

- fixed;
- verified;
- all tests pass;
- production ready;
- deployed;
- complete;
- resolved.

### Research closure

Invoke when:

- only one primary source underlies several citations;
- evidence is mixed;
- a first plausible explanation is becoming a conclusion;
- the Primary dismisses disconfirming information without resolving it.

### Repeated local failure

Invoke when the same local approach has failed or been patched around repeatedly.

## Low-value cues

Skip normally for:

- formatting;
- typo correction;
- non-semantic renames;
- purely mechanical transformations;
- trivial reversible actions;
- already-reviewed `decision_id`s.

## Future router work

Potential future activation strategies:

1. explicit invocation;
2. deterministic event classes;
3. lightweight high-recall classifier;
4. learned cost-sensitive router.

Do not build a learned router before ChomView's local intervention value is demonstrated.
