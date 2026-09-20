# Contributing to ChomView

ChomView is an experimental Agent Skill and research protocol. Contributions are welcome when they preserve the project's central scope: one bounded, non-authoritative local second thought for a task-focused Primary.

## Before opening a pull request

Run:

```bash
python scripts/validate_repo.py
```

Keep these invariants intact unless the pull request explicitly proposes and motivates a research-level change:

```text
peer_deliberations <= 1
context_requests <= 1
peer_spawn_depth = 0
debate_rounds = 0
```

Do not turn the Second-Thought Peer into a global planner, supervisor, autonomous reviewer swarm, or mandatory execution gate.

## Skill changes

Changes to `SKILL.md` should be operational and concise. Put detailed research background, extensive examples, protocol detail, and evaluation material under `references/`.

Any change to BROTLI fields should update the corresponding schemas and behavioral cases.

## Research claims

Do not claim that ChomView is proven to improve agent performance unless supported by reproducible evidence.

Clearly distinguish:

- established prior art;
- observed experimental result;
- hypothesis;
- implementation preference.

## Third-party material

Do not paste third-party skill text, prompts, source code, test cases, or documentation into this repository without verifying license and provenance. Update `THIRD_PARTY_NOTICES.md` when actual reuse occurs.

## Pull requests

A good pull request explains:

1. the local problem;
2. why the current ChomView behavior is insufficient;
3. the smallest proposed change;
4. expected effect on token cost / behavior;
5. behavioral cases added or changed.
