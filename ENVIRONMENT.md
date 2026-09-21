# CHOMVIEW-EMPIRICAL-EVALUATION-001 Environment Lock

**Date:** 2026-09-20  
**Evaluator:** Claude Haiku 4.5  
**Contract Version:** 1.0

## Claude Code Environment

```
CLAUDE_CODE_VERSION: 2.1.278
OPERATING_SYSTEM: Linux 5.15.0-186-generic
PLATFORM: linux
SHELL: bash
USER: root
```

## ChomView Source

```
REPOSITORY: https://github.com/tonnestate/ChomView
REVISION: 663bdd4521c8ce60457e4798ec980efa7533ebc4
TAG: v0.1.0
CLONE_DATE: 2026-09-20
CLONE_PATH: /tmp/chomview-source
```

## Model Lock

```
MODEL: Claude Haiku 4.5
MODEL_ID: claude-haiku-4-5-20251001
```

All four arms (A, B, C, D) will use the same model and Claude Code version.

## Evaluation Workspace

```
ROOT: /root/chomview-eval/
├── corpus/          — task definitions and expected outcomes
├── hidden/          — hidden answer keys (inaccessible to actor sessions)
├── runs/            — execution artifacts per task per arm
├── results/         — scored results and metrics
└── manifests/       — randomization, contamination checks, etc.
```

## Preflight Checks

- [x] Claude Code 2.1.278 available
- [x] ChomView repository cloned and verified at pinned revision
- [x] Evaluation directory structure created
- [x] Environment locked

**Status: READY FOR EXECUTION**
