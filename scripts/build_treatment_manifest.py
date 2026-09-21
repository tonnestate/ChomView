#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INCLUDE=[
    "SKILL.md",
    "agents/chomview-second-thought.md",
    "references/activation-cues.md",
    "references/behavioral-integrity.md",
    "references/behavioral-compatibility.md",
    "references/bounded-enforcement.md",
    "references/brotli-protocol.md",
    "references/consequence-chain-completion.md",
    "schemas/acknowledgement.schema.json",
    "schemas/behavioral-contract.schema.json",
    "schemas/brotli-request.schema.json",
    "schemas/brotli-response.schema.json",
    "schemas/correction-rule.schema.json",
    "runtime/chomview_guard.py",
    "config/behavioral-contract.default.json",
    "scripts/configure_claude_hooks.py",
    "scripts/install-claude-code.sh",
    "scripts/install-claude-code.ps1"
]

def sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

obj={
    "schema_version":1,
    "name":"ChomView",
    "version":"0.4.0",
    "treatment_id":"chomview-v0.4.0-behavioral-compatibility",
    "base_source_commit":"f1b209e0ae47250e5f71ec4b6ff76685d5544301",
    "files":{p:sha(ROOT/p) for p in INCLUDE}
}
(ROOT/"TREATMENT_MANIFEST.json").write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")
print(ROOT/"TREATMENT_MANIFEST.json")
