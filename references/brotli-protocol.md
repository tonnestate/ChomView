# BROTLI/1 Thought Protocol

## Purpose

BROTLI/1 is the compact peer-to-peer semantic state transfer used by ChomView.

For ChomView, BROTLI means **Bounded Reasoning-Oriented Transfer for Local Intervention**.

It is conceptually separate from the Brotli byte-compression algorithm. A transport may additionally use ordinary Brotli compression, but ChomView depends only on semantic compression.

## Design goals

BROTLI/1 should:

- preserve the local decision state;
- preserve relevant uncertainty;
- preserve facts separately from the Primary's intended action;
- avoid full transcript duplication;
- avoid transmission of raw private chain-of-thought;
- give the STP enough local context to extend the consequence chain;
- remain cheap enough to use repeatedly in long agentic work.

## Request

Canonical logical form:

```yaml
protocol: BROTLI/1
type: request
mid: msg-...
tid: task-...
did: decision-...
purpose: short stable purpose anchor
situation: local event
intent: intended local action or claim
rationale: concise reason the Primary thinks this is sufficient
facts:
  - directly observed local fact
constraints:
  - directly relevant constraint
uncertainty: known uncertainty or none stated
immediate_effect: expected immediate result
refs:
  - optional local evidence reference
```

## Semantic compression rules

### Preserve

Preserve:

- causal facts;
- state distinctions;
- contradictions;
- relevant uncertainty;
- externally imposed constraints;
- the strength of the Primary's claim;
- the intended action.

### Compress

Compress:

- narrative history;
- repeated facts;
- verbose logs;
- irrelevant implementation detail;
- already resolved branches.

### Never silently transform

Do not convert:

```text
provider returned NULL after timeout
```

into:

```text
provider has no result
```

unless that interpretation is explicitly marked as the Primary's interpretation rather than an observed fact.

## Purpose anchor

The purpose anchor should normally fit in 1-3 sentences.

It is not the complete project description.

Its purpose is to let the peer decide whether a local consequence matters to the parent task.

Bad:

```text
Full 8,000-word project specification...
```

Good:

```text
Preserve the existing domain semantics while repairing the failing integration. Avoid duplicate external effects and unnecessary new behavior paths.
```

## Facts versus rationale

Separate direct facts from interpretation.

Example:

```yaml
facts:
  - HTTP call timed out after 5 seconds
  - local client received no response body
rationale: Assume timeout means no result and persist zero
```

Do not encode the assumption as a fact.

## References

Large evidence should be referenced rather than copied when the runtime supports targeted read access.

Example:

```yaml
refs:
  - file:src/provider/client.py#L120-L170
  - log:run-482:provider-call-17
```

The STP should inspect a referenced artifact only when necessary.

## Response

Canonical logical form:

```yaml
protocol: BROTLI/1
type: response
reply_to: msg-...
did: decision-...
stance: OK | LOOK_AGAIN | WARNING
concern: NONE | LOW | MATERIAL | HIGH
missing: concise overlooked point or none
chain: concise consequence chain or none
advice: local recommendation
check: smallest useful local check
insufficient: optional weak check
why: connection to parent purpose
confidence: LOW | MEDIUM | HIGH
```

## NEED

A peer may request one precise fact:

```yaml
protocol: BROTLI/1
type: need
reply_to: msg-...
did: decision-...
need: exact factual information required
reason: why it materially changes the judgment
```

Do not use `NEED` for broad curiosity.

## Acknowledgement

The Primary records:

```yaml
protocol: BROTLI/1
type: ack
did: decision-...
response: ADOPT | ADAPT | DECLINE
reason: concise rationale
```

No automatic second debate round follows.

## Invariants

For v0.1:

```text
peer_deliberations(did) <= 1
context_requests(did) <= 1
peer_spawn_depth = 0
debate_rounds = 0
```

## Security and privacy note

BROTLI should transfer only the minimum local task information needed by the peer. Do not use it as a mechanism to expose hidden chain-of-thought or unrelated confidential context.
