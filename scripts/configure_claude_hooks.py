#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

EVENTS = ("SessionStart", "UserPromptSubmit", "PreToolUse")
MARKER = "chomview_guard.py"


def handler(python_cmd: str) -> dict:
    args = []
    command = python_cmd
    if os.name == "nt" and python_cmd.lower().endswith("py"):
        args.append("-3")
    args.append("${CLAUDE_PROJECT_DIR}/.claude/chomview/chomview_guard.py")
    return {"type": "command", "command": command, "args": args}


def clean_existing(groups: list) -> list:
    out = []
    for group in groups:
        if not isinstance(group, dict):
            out.append(group)
            continue
        hooks = []
        for h in group.get("hooks", []):
            blob = json.dumps(h, sort_keys=True)
            if MARKER not in blob:
                hooks.append(h)
        if hooks:
            g = dict(group)
            g["hooks"] = hooks
            out.append(g)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--python", default=("py" if os.name == "nt" else "python3"))
    args = ap.parse_args()

    project = Path(args.project).resolve()
    settings_path = project / ".claude" / "settings.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    if settings_path.exists():
        data = json.loads(settings_path.read_text(encoding="utf-8"))
    else:
        data = {}
    hooks = data.setdefault("hooks", {})

    common = handler(args.python)
    for event in EVENTS:
        groups = clean_existing(hooks.get(event, []))
        group = {"hooks": [dict(common)]}
        if event == "PreToolUse":
            group["matcher"] = "*"
        groups.append(group)
        hooks[event] = groups

    settings_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(settings_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
