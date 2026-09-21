# ChomView clean rebase package

Purpose: clean, non-discoverable handoff after evaluation/content drift.

## Canonical source

The repository files at the package root are an exact reconstruction of GitHub commit:

- repository: `tonnestate/ChomView`
- commit: `73c4d30238b919e0d0421e340ffdcc3ef5b02ba8`
- commit date: 2026-09-20
- verification: all 40 blob files matched the GitHub tree SHA values exactly before packaging

No v0.3 behavior, trigger, new evaluation design, or research claim was added.

## Recovered later evaluation evidence

The supplied `EVAL-00_NEXT.zip` contained:

- EVAL-006L
- EVAL-006R
- EVAL-006X
- EVAL-006X-REPAIR
- EVAL-008

These are preserved in `HISTORICAL_EVALS_006L_008_SANITIZED.zip` and are deliberately NOT merged into the canonical repository tree.

Every historical `.claude` directory inside those evaluations was preserved byte-for-byte in a local `HISTORICAL_CLAUDE_RUNTIME.zip` and then removed as a discoverable directory. This prevents Claude Code from loading an old embedded ChomView skill merely because the evidence was extracted near a runtime workspace.

Python `__pycache__`, `.pyc`, and `.pyo` residue was removed.

## Not reconstructed

No standalone EVAL-005 or plain EVAL-006 artifact was present in the supplied ZIP. Searches of the accessible uploaded/chat files did not recover a standalone source artifact for those names, so none was fabricated.

## Source checksums

Original supplied `EVAL-00_NEXT.zip` SHA-256:

`49ad0c36733221a7aede93e33763d21bd44609898a7248ff0baedac3ee1b58ad`

Sanitized historical-evals archive SHA-256:

`96244b9a393b96fef3f90a1ed1fee067293558e69c10f19123c0f9598338ffe8`
