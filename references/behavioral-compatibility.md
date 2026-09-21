# Behavioral Compatibility — Heterogeneous Agent Contract

ChomView v0.4 adds a behavioral compatibility layer for heterogeneous agents.

The governing principle is:

```text
wild cognition != wild authority
```

An agent may have different heuristics, priorities, communication styles, model training, cultural priors, or internal reasoning strategies. ChomView does not normalize those differences. It governs only what the agent is authorized to do in the host system.

## Non-normalization rule

ChomView must not classify an action as wrong merely because the agent is unusual, disagreeable, culturally unfamiliar, highly autonomous, conservative, aggressive, creative, or otherwise different from the host's preferred style.

Behavioral compatibility is about explicit system contracts:

```text
personality != permission
capability != permission
availability != authorization
preference != spending authority
new evidence != authorization for a new objective
```

## Authority decisions

A deterministic behavioral-contract rule may return one of four decisions:

- `ALLOW` — the action is within the declared authority boundary.
- `LOOK_AGAIN` — the action remains permitted, but a concrete contract concern should be reconsidered.
- `REQUIRE_CONSENT` — the action affects a protected stakeholder/resource or exceeds autonomous authority and requires explicit consent.
- `BLOCK` — the action violates an explicit execution boundary and must not execute.

These decisions are independent from the v0.3 recurrence levels `NOTICE -> WARNING -> STRIKE -> FREEZE -> ESCALATE`. The contract governs current authority; Behavioral Continuity governs repeated acknowledged violations.

## Stakeholders and resources

A contract rule may name affected stakeholders and resources. Examples include:

```text
stakeholders: owner, user, customer, production operator
resources: money, tokens, compute, production state, credentials, external messages
```

A preference may explain why an agent wants an action. It does not create authority over another stakeholder's resources.

## Project-local contract

Claude Code installations keep the contract at:

```text
.claude/chomview/behavioral-contract.json
```

The source template lives at `config/behavioral-contract.default.json`.

Rules use deterministic matchers over actor id, tool name, and serialized tool input. Semantic rules remain context-only unless the host or peer can bind them safely to a deterministic action boundary.

Example rule:

```json
{
  "rule_id": "owner-budget-expensive-provider",
  "enabled": true,
  "priority": 100,
  "decision": "REQUIRE_CONSENT",
  "authority": "REQUIRES_OWNER_CONSENT",
  "stakeholders": ["owner"],
  "resources": ["money", "tokens"],
  "rationale": "A quality preference does not grant authority to spend protected owner resources.",
  "matchers": [
    {
      "actor_regex": ".*",
      "tool": "ProviderCall",
      "input_regex": "premium|expensive"
    }
  ]
}
```

The example is illustrative; ChomView does not invent provider names, budgets, ownership, or permissions on behalf of a project.

## Precedence

For one proposed tool action, enforcement is conservative and deterministic:

1. an existing `FREEZE`/`ESCALATE` state blocks unrelated mutation;
2. a matching `BLOCK` contract rule blocks execution;
3. a recurrence at `STRIKE` or above blocks execution;
4. a matching `REQUIRE_CONSENT` rule or recurrence `WARNING` requires permission;
5. `LOOK_AGAIN`/`NOTICE` inject context without fabricating authority.

Read-only diagnosis remains available during a v0.3 freeze.

## OmniRoute / foreign-agent use

A routed or foreign agent does not inherit authority merely because it is capable of invoking a tool. The host should bind the agent to a project-local behavioral contract and, where useful, expose an actor id through `CHOMVIEW_ACTOR_ID` or the hook payload.

This permits heterogeneous agents to keep their own cognition while sharing the same execution boundaries.

## Scope boundary

ChomView v0.4 is an implementation release, not evidence that behavioral contracts improve benchmark performance. It also does not claim to solve general value alignment, cultural alignment, human morality, or arbitrary semantic policy interpretation.
