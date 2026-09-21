#!/usr/bin/env python3
"""ChomView v0.3 Behavioral Continuity Guard.

The guard does two bounded things:
1. Re-inject active correction rules at SessionStart/UserPromptSubmit so a
   correction survives context changes and fresh evidence.
2. Enforce explicit deterministic matchers on PreToolUse with the bounded
   escalation NOTICE -> WARNING -> STRIKE -> FREEZE -> ESCALATE.

It does not decide arbitrary semantic similarity on its own. Rules without
matchers are context-only and remain advisory until the Primary/peer records a
recurrence explicitly.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
LEVELS = ("NOTICE", "WARNING", "STRIKE", "FREEZE", "ESCALATE")
READ_ONLY_TOOLS = {
    "Read", "Grep", "Glob", "WebSearch", "WebFetch", "LS", "NotebookRead",
}
GUARD_MAINTENANCE_RE = re.compile(r"chomview_guard\.py\s+(?:resolve|retire|status|list|remember|violation)\b")

CORE_RULES = [
    {
        "rule_id": "core.evidence-is-not-authorization",
        "pattern": "New evidence or an uploaded artifact silently becomes authorization for a new objective, implementation, eval, repair, or scope expansion.",
        "changed_rule": "New evidence updates the facts of the current root goal. It does not authorize a new objective or scope expansion unless the user explicitly requests that change.",
        "source_did": "CHOMVIEW-V0.3-CORE",
        "materiality": "HIGH",
        "active": True,
        "immutable": True,
        "violation_count": 0,
        "level": "NOTICE",
        "matchers": [],
    }
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def project_dir(payload: dict[str, Any] | None = None) -> Path:
    if os.environ.get("CLAUDE_PROJECT_DIR"):
        return Path(os.environ["CLAUDE_PROJECT_DIR"]).resolve()
    if payload and payload.get("cwd"):
        return Path(str(payload["cwd"])).resolve()
    return Path.cwd().resolve()


def state_paths(root: Path) -> tuple[Path, Path]:
    state_dir = root / ".claude" / "chomview"
    return state_dir / "corrections.json", state_dir / "events.jsonl"


def default_store() -> dict[str, Any]:
    return {"schema_version": SCHEMA_VERSION, "rules": [dict(r) for r in CORE_RULES]}


def load_store(root: Path) -> dict[str, Any]:
    path, _ = state_paths(root)
    if not path.exists():
        return default_store()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default_store()
    if not isinstance(data, dict) or not isinstance(data.get("rules"), list):
        return default_store()
    known = {str(r.get("rule_id")) for r in data["rules"] if isinstance(r, dict)}
    for core in CORE_RULES:
        if core["rule_id"] not in known:
            data["rules"].insert(0, dict(core))
    data["schema_version"] = SCHEMA_VERSION
    return data


def save_store(root: Path, store: dict[str, Any]) -> None:
    path, _ = state_paths(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(store, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def log_event(root: Path, event: dict[str, Any]) -> None:
    _, path = state_paths(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {"at": utc_now(), **event}
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def level_for_count(count: int) -> str:
    if count <= 1:
        return "NOTICE"
    if count == 2:
        return "WARNING"
    if count == 3:
        return "STRIKE"
    if count == 4:
        return "FREEZE"
    return "ESCALATE"


def active_rules(store: dict[str, Any]) -> list[dict[str, Any]]:
    return [r for r in store.get("rules", []) if isinstance(r, dict) and r.get("active", True)]


def format_context(store: dict[str, Any]) -> str:
    rules = active_rules(store)
    if not rules:
        return ""
    rows = [
        "ChomView v0.3 behavioral-continuity state. These are previously established correction rules; preserve them unless explicitly retired by the owner:",
    ]
    for rule in rules[:20]:
        rows.append(
            f"- [{rule.get('level','NOTICE')}] {rule.get('rule_id')}: {rule.get('changed_rule')}"
        )
    rows.append(
        "A new upload, file, observation, or failure is evidence/context for the current root goal; it is not by itself authorization to invent a new goal, eval, repair, implementation, or scope expansion."
    )
    return "\n".join(rows)


def matcher_hit(rule: dict[str, Any], payload: dict[str, Any]) -> bool:
    tool_name = str(payload.get("tool_name", ""))
    tool_input = payload.get("tool_input", {})
    serialized = json.dumps(tool_input, ensure_ascii=False, sort_keys=True)
    for matcher in rule.get("matchers") or []:
        if not isinstance(matcher, dict):
            continue
        tool_re = str(matcher.get("tool", ".*"))
        input_re = str(matcher.get("input_regex", ".*"))
        try:
            if re.search(tool_re, tool_name) and re.search(input_re, serialized, flags=re.IGNORECASE | re.DOTALL):
                return True
        except re.error:
            continue
    return False


def is_guard_maintenance(payload: dict[str, Any]) -> bool:
    if str(payload.get("tool_name", "")) not in {"Bash", "PowerShell"}:
        return False
    command = str((payload.get("tool_input") or {}).get("command", ""))
    return bool(GUARD_MAINTENANCE_RE.search(command))


def pretool_decision(root: Path, store: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any] | None:
    if is_guard_maintenance(payload):
        return None

    # A frozen/escalated rule prevents unrelated mutation until reconciled, but
    # keeps read-only inspection and guard-maintenance available.
    frozen = [r for r in active_rules(store) if r.get("level") in {"FREEZE", "ESCALATE"}]
    tool_name = str(payload.get("tool_name", ""))
    if frozen and tool_name not in READ_ONLY_TOOLS:
        ids = ", ".join(str(r.get("rule_id")) for r in frozen)
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    f"CHOMVIEW_{frozen[0].get('level')}: behavioral continuity is frozen by rule(s) {ids}. "
                    "Reconcile the recognized failure and explicitly resolve or retire the rule before continuing mutation."
                ),
                "additionalContext": format_context(store),
            }
        }

    hits = [r for r in active_rules(store) if matcher_hit(r, payload)]
    if not hits:
        return None

    # One tool call can hit multiple rules. Advance every matching rule once,
    # then enforce the strongest resulting level.
    for rule in hits:
        rule["violation_count"] = int(rule.get("violation_count", 0)) + 1
        rule["level"] = level_for_count(rule["violation_count"])
        rule["last_violation_at"] = utc_now()
        log_event(root, {
            "event": "rule_recurrence",
            "rule_id": rule.get("rule_id"),
            "level": rule["level"],
            "tool_name": tool_name,
        })
    save_store(root, store)

    strongest = max(hits, key=lambda r: LEVELS.index(str(r.get("level", "NOTICE"))))
    level = str(strongest.get("level"))
    rule_id = str(strongest.get("rule_id"))
    rule_text = str(strongest.get("changed_rule"))
    reason = f"CHOMVIEW_{level}: repeated acknowledged pattern matched rule {rule_id}. Changed rule: {rule_text}"

    if level == "NOTICE":
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": reason + " Reconsider before proceeding.",
            }
        }
    if level == "WARNING":
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": reason,
                "additionalContext": format_context(store),
            }
        }
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason + " Current action is blocked pending correction/reconciliation.",
            "additionalContext": format_context(store),
        }
    }


def handle_hook(payload: dict[str, Any]) -> int:
    root = project_dir(payload)
    store = load_store(root)
    # Materialize core state so it survives fresh sessions and compaction.
    save_store(root, store)
    event = str(payload.get("hook_event_name", ""))

    if event in {"SessionStart", "UserPromptSubmit"}:
        context = format_context(store)
        if context:
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": event,
                    "additionalContext": context,
                }
            }, ensure_ascii=False))
        return 0

    if event == "PreToolUse":
        decision = pretool_decision(root, store, payload)
        if decision:
            print(json.dumps(decision, ensure_ascii=False))
        return 0

    return 0


def cmd_remember(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve() if args.project else project_dir()
    store = load_store(root)
    rid = args.rule_id or "rule." + hashlib.sha256((args.pattern + "\n" + args.changed_rule).encode()).hexdigest()[:12]
    existing = next((r for r in store["rules"] if r.get("rule_id") == rid), None)
    rule = existing or {"rule_id": rid, "violation_count": 0, "level": "NOTICE"}
    rule.update({
        "pattern": args.pattern,
        "changed_rule": args.changed_rule,
        "source_did": args.source_did,
        "materiality": args.materiality,
        "active": True,
        "immutable": bool(rule.get("immutable", False)),
        "updated_at": utc_now(),
        "matchers": [],
    })
    for spec in args.matcher or []:
        if "::" not in spec:
            raise SystemExit("--matcher must be TOOL_REGEX::INPUT_REGEX")
        tool_re, input_re = spec.split("::", 1)
        # Compile now so invalid matchers never enter persistent state.
        re.compile(tool_re)
        re.compile(input_re)
        rule["matchers"].append({"tool": tool_re, "input_regex": input_re})
    if not existing:
        store["rules"].append(rule)
    save_store(root, store)
    log_event(root, {"event": "rule_remembered", "rule_id": rid})
    print(rid)
    return 0


def find_rule(store: dict[str, Any], rid: str) -> dict[str, Any]:
    for rule in store.get("rules", []):
        if rule.get("rule_id") == rid:
            return rule
    raise SystemExit(f"unknown rule_id: {rid}")


def cmd_violation(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve() if args.project else project_dir()
    store = load_store(root)
    rule = find_rule(store, args.rule_id)
    rule["violation_count"] = int(rule.get("violation_count", 0)) + 1
    rule["level"] = level_for_count(rule["violation_count"])
    rule["last_violation_at"] = utc_now()
    save_store(root, store)
    log_event(root, {"event": "semantic_recurrence", "rule_id": args.rule_id, "level": rule["level"]})
    print(rule["level"])
    return 0


def cmd_resolve(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve() if args.project else project_dir()
    store = load_store(root)
    rule = find_rule(store, args.rule_id)
    rule["violation_count"] = 0
    rule["level"] = "NOTICE"
    rule["last_resolved_at"] = utc_now()
    save_store(root, store)
    log_event(root, {"event": "rule_resolved", "rule_id": args.rule_id, "evidence": args.evidence})
    print("RESOLVED")
    return 0


def cmd_retire(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve() if args.project else project_dir()
    store = load_store(root)
    rule = find_rule(store, args.rule_id)
    if rule.get("immutable"):
        raise SystemExit("immutable core rule cannot be retired")
    rule["active"] = False
    rule["retired_at"] = utc_now()
    save_store(root, store)
    log_event(root, {"event": "rule_retired", "rule_id": args.rule_id})
    print("RETIRED")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve() if args.project else project_dir()
    store = load_store(root)
    print(json.dumps(store, ensure_ascii=False, indent=2))
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="ChomView v0.3 Behavioral Continuity Guard")
    p.add_argument("--project", help="project root; defaults to CLAUDE_PROJECT_DIR/cwd")
    sub = p.add_subparsers(dest="cmd")

    r = sub.add_parser("remember", help="persist a recognized correction rule")
    r.add_argument("--rule-id")
    r.add_argument("--pattern", required=True)
    r.add_argument("--changed-rule", required=True)
    r.add_argument("--source-did", default="manual")
    r.add_argument("--materiality", choices=["LOW", "MEDIUM", "HIGH"], default="HIGH")
    r.add_argument("--matcher", action="append", help="TOOL_REGEX::INPUT_REGEX; repeatable")
    r.set_defaults(func=cmd_remember)

    v = sub.add_parser("violation", help="record a semantic recurrence detected by Primary/peer")
    v.add_argument("--rule-id", required=True)
    v.set_defaults(func=cmd_violation)

    q = sub.add_parser("resolve", help="reset escalation after evidence-backed correction/reconciliation")
    q.add_argument("--rule-id", required=True)
    q.add_argument("--evidence", required=True)
    q.set_defaults(func=cmd_resolve)

    x = sub.add_parser("retire", help="retire a non-core rule")
    x.add_argument("--rule-id", required=True)
    x.set_defaults(func=cmd_retire)

    s = sub.add_parser("status", aliases=["list"], help="print current correction state")
    s.set_defaults(func=cmd_status)
    return p


def main() -> int:
    # No command means hook mode: stdin is a Claude Code hook payload.
    if len(sys.argv) == 1:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0
        try:
            payload = json.loads(raw)
        except Exception:
            return 0  # fail open on malformed hook input
        return handle_hook(payload)

    p = parser()
    args = p.parse_args()
    if not getattr(args, "func", None):
        p.print_help()
        return 2
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
