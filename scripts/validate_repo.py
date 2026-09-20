#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / ".claude/skills/chomview"
AGENT_PATH = ROOT / ".claude/agents/chomview-second-thought.md"

REQUIRED = [
    "README.md",
    "LICENSE",
    "NOTICE",
    "THIRD_PARTY_NOTICES.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    ".claude/skills/chomview/SKILL.md",
    ".claude/skills/chomview/references/brotli-protocol.md",
    ".claude/skills/chomview/references/consequence-chain-completion.md",
    ".claude/skills/chomview/references/evaluation-protocol.md",
    ".claude/skills/chomview/references/prior-art-and-claims.md",
    ".claude/skills/chomview/schemas/brotli-request.schema.json",
    ".claude/skills/chomview/schemas/brotli-response.schema.json",
    ".claude/skills/chomview/schemas/acknowledgement.schema.json",
    ".claude/agents/chomview-second-thought.md",
    ".github/workflows/validate.yml",
    "tests/behavioral-cases.md",
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
    raw = text[4:end]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            data[m.group(1)] = m.group(2).strip().strip('"\'')
    return data


def main() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    skill_path = SKILL_ROOT / "SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8")
    lines = skill_text.splitlines()
    if len(lines) > 500:
        fail(f"SKILL.md is {len(lines)} lines; expected <= 500")

    fm = parse_frontmatter(skill_text, str(skill_path.relative_to(ROOT)))
    if fm.get("name") != "chomview":
        fail("SKILL.md frontmatter name must be chomview")
    description = fm.get("description", "")
    if not description:
        fail("SKILL.md frontmatter description is required")
    if len(description) > 1024:
        fail("SKILL.md description exceeds 1024 characters")

    agent_text = AGENT_PATH.read_text(encoding="utf-8")
    agent_fm = parse_frontmatter(agent_text, str(AGENT_PATH.relative_to(ROOT)))
    if agent_fm.get("name") != "chomview-second-thought":
        fail("Second-Thought agent name is invalid")

    schema_dir = SKILL_ROOT / "schemas"
    for schema in sorted(schema_dir.glob("*.json")):
        with schema.open("r", encoding="utf-8") as fh:
            obj = json.load(fh)
        if not isinstance(obj, dict):
            fail(f"{schema.relative_to(ROOT)} must contain a JSON object")
        if "$schema" not in obj:
            fail(f"{schema.relative_to(ROOT)} has no $schema declaration")

    if "BROTLI" not in skill_text:
        fail("SKILL.md no longer references BROTLI")
    if "Consequence" not in skill_text:
        fail("SKILL.md no longer references consequence reasoning")

    print("ChomView repository validation passed")
    print(f"SKILL.md lines: {len(lines)}")
    print(f"Schemas: {len(list(schema_dir.glob('*.json')))}")


if __name__ == "__main__":
    main()
