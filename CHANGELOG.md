# Changelog

All notable changes to ChomView will be documented here.

## [0.4.0] - 2026-09-21

### Added
- Behavioral Compatibility layer for heterogeneous/routed agents.
- `wild cognition != wild authority` as the core authority invariant.
- Project-local `behavioral-contract.json` with deterministic actor/tool/input matching.
- Authority outcomes: `ALLOW`, `LOOK_AGAIN`, `REQUIRE_CONSENT`, `BLOCK`.
- Stakeholder and protected-resource metadata.
- `references/behavioral-compatibility.md` and `schemas/behavioral-contract.schema.json`.
- BROTLI/1 optional authority/stakeholder/resource fields.
- Runtime tests for consent, block, actor scope, and non-normalization.

### Changed
- Claude Code installers now seed a default behavioral contract but never overwrite an existing owner-edited contract.
- Repository validation rejects Python build residue and the known flattened-file packaging failure mode.
- v0.3 Behavioral Continuity remains intact and composes with the v0.4 authority contract.

### Claims boundary
- v0.4 is an implementation release. No confirmatory efficacy, cultural-normalization, general alignment, or peer-uplift claim is added.

## [0.3.0] - 2026-09-21

### Added
- Behavioral Continuity Guard with persistent correction rules outside conversational memory.
- Bounded recurrence states: `NOTICE -> WARNING -> STRIKE -> FREEZE -> ESCALATE`.
- Project-local Claude Code hooks for `SessionStart`, `UserPromptSubmit`, and `PreToolUse`.
- Core scope-integrity invariant: new evidence/context does not authorize a new objective or scope expansion.
- `runtime/chomview_guard.py` and deterministic correction-rule matcher enforcement.
- `references/bounded-enforcement.md` and `schemas/correction-rule.schema.json`.
- Treatment manifest with SHA-256 provenance for active behavioral files.
- Duplicate-skill/content-drift validation gate.

### Changed
- Material corrective acknowledgement now persists a reusable rule instead of relying on conversational recall alone.
- Installers configure the Behavioral Continuity Guard while preserving unrelated Claude Code hook settings.
- Second-Thought Peer can identify continuity actions (`REMEMBER`, `RECORD_RECURRENCE`, `RESOLVE_AFTER_EVIDENCE`).

### Safety / boundedness
- No `Stop` hook is installed; v0.3 avoids recursive completion-loop enforcement.
- Deterministic blocking is limited to explicit persisted matchers and freeze state. Semantic-only rules are injected as context and are not mechanically overgeneralized.
- v0.3 is an implementation release, not a claim of confirmatory performance validation.

## [0.2.0] - 2026-09-20

### Added
- Behavioral Integrity checks for intent preservation, evidence-before-claim, plausible substitution, explanation-vs-exoneration, and corrective acknowledgement.
- Repeated acknowledged failure detection and `pattern_rule` / changed-decision-rule guidance.
- `references/behavioral-integrity.md`.
- Evaluation history under `tests/evals/`, including preserved EVAL-001 original reports and subsequent audit reclassification.
- EVAL-004 historical-fork behavioral-policy signal and explicit peer-uplift limitation.

### Changed
- Second-Thought Peer now checks substantive intent and post-hoc rationalization in addition to consequence chains.
- Evaluation protocol separates generic self-reconsideration (B0), ChomView-policy self-reconsideration (B1), generic peer (C), and ChomView peer (D).
- Behavioral cases expanded for goal substitution, synthetic evidence substitution, premature termination, rationalization, and repeated acknowledged failures.

## 0.1.0 — 2026-09-20

### Added

- Initial ChomView Agent Skill.
- Premature Local Closure taxonomy.
- Bounded Second-Thought Peer contract.
- BROTLI/1 local reasoning-state protocol.
- Consequence-Chain Completion.
- Primary acknowledgement protocol.
- Read-only Claude Code peer agent definition.
- JSON schemas for BROTLI request, response, and acknowledgement.
- Scientific concept paper, prior-art boundary, and evaluation protocol.
- GitHub repository packaging, behavioral cases, repository validator, visible peer source, and Claude Code installers.

