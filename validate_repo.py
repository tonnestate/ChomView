#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.3.0"

REQUIRED = [
    "SKILL.md", "README.md", "LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md",
    "CHANGELOG.md", "PACKAGE_MANIFEST.json", "TREATMENT_MANIFEST.json",
    "references/behavioral-integrity.md", "references/bounded-enforcement.md",
    "references/brotli-protocol.md", "references/consequence-chain-completion.md",
    "references/evaluation-protocol.md", "references/prior-art-and-claims.md",
    "schemas/brotli-request.schema.json", "schemas/brotli-response.schema.json",
    "schemas/acknowledgement.schema.json", "schemas/correction-rule.schema.json",
    "tests/behavioral-cases.md", "tests/evals/README.md",
    "tests/runtime/test_chomview_guard.py", "agents/chomview-second-thought.md",
    "runtime/chomview_guard.py", "scripts/configure_claude_hooks.py",
]


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(text: str, path: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail(f"{path} has no opening YAML frontmatter delimiter")
    end = text.find("\n---\n", 4)
    if end < 0:
        fail(f"{path} has no closing YAML frontmatter delimiter")
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            data[m.group(1)] = m.group(2).strip().strip('"\'')
    return data


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_single_active_skill() -> None:
    skill_paths = []
    for p in ROOT.rglob("SKILL.md"):
        rel = p.relative_to(ROOT)
        if "_recovery" in rel.parts:
            continue
        skill_paths.append(rel.as_posix())
    if skill_paths != ["SKILL.md"]:
        fail("expected exactly one active source SKILL.md; found: " + ", ".join(skill_paths))

    forbidden = []
    for p in ROOT.rglob("*"):
        if not p.is_dir():
            continue
        rel = p.relative_to(ROOT)
        parts = rel.parts
        if ".claude-skills" in parts:
            forbidden.append(rel.as_posix())
        if len(parts) >= 3:
            for i in range(len(parts)-2):
                if parts[i:i+3] == (".claude", "skills", "chomview"):
                    forbidden.append(rel.as_posix())
    if forbidden:
        fail("discoverable duplicate ChomView skill path(s): " + ", ".join(sorted(set(forbidden))))


def check_manifest() -> None:
    pkg = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    if pkg.get("version") != VERSION:
        fail(f"PACKAGE_MANIFEST version must be {VERSION}")
    tm = json.loads((ROOT / "TREATMENT_MANIFEST.json").read_text(encoding="utf-8"))
    if tm.get("version") != VERSION:
        fail(f"TREATMENT_MANIFEST version must be {VERSION}")
    files = tm.get("files")
    if not isinstance(files, dict) or not files:
        fail("TREATMENT_MANIFEST files missing")
    for rel, expected in files.items():
        p = ROOT / rel
        if not p.is_file():
            fail(f"treatment file missing: {rel}")
        actual = sha(p)
        if actual != expected:
            fail(f"treatment hash mismatch: {rel}")


def main() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    skill_path = ROOT / "SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8")
    lines = skill_text.splitlines()
    if len(lines) > 500:
        fail(f"SKILL.md is {len(lines)} lines; expected <= 500")

    fm = parse_frontmatter(skill_text, "SKILL.md")
    if fm.get("name") != "chomview":
        fail("SKILL.md frontmatter name must be chomview")
    if not fm.get("description") or len(fm["description"]) > 1024:
        fail("SKILL.md frontmatter description is missing or too long")

    agent_text = (ROOT / "agents/chomview-second-thought.md").read_text(encoding="utf-8")
    agent_fm = parse_frontmatter(agent_text, "agents/chomview-second-thought.md")
    if agent_fm.get("name") != "chomview-second-thought":
        fail("Second-Thought agent name is invalid")

    for schema in sorted((ROOT / "schemas").glob("*.json")):
        obj = json.loads(schema.read_text(encoding="utf-8"))
        if not isinstance(obj, dict) or "$schema" not in obj:
            fail(f"{schema.relative_to(ROOT)} is not a declared JSON schema")

    for marker in ("BROTLI", "Consequence", "Behavioral Continuity Guard", "NOTICE -> WARNING -> STRIKE -> FREEZE -> ESCALATE"):
        if marker not in skill_text:
            fail(f"SKILL.md missing required v0.3 marker: {marker}")

    check_single_active_skill()
    check_manifest()

    print("ChomView repository validation passed")
    print(f"Version: {VERSION}")
    print(f"SKILL.md lines: {len(lines)}")
    print(f"Schemas: {len(list((ROOT / 'schemas').glob('*.json')))}")
    print("Active source SKILL.md copies: 1")
    print("Treatment hashes: verified")


if __name__ == "__main__":
    main()
