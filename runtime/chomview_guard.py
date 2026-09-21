#!/usr/bin/env python3
"""ChomView v0.4 Behavioral Continuity + Compatibility Guard.

The guard does three bounded things:
1. Re-inject active correction rules at SessionStart/UserPromptSubmit.
2. Enforce v0.3 recurrence escalation NOTICE -> WARNING -> STRIKE -> FREEZE -> ESCALATE.
3. Enforce a project-local v0.4 behavioral contract for heterogeneous agents using
   ALLOW -> LOOK_AGAIN -> REQUIRE_CONSENT -> BLOCK authority decisions.

It does not normalize personality, culture, style, or arbitrary semantic values.
Only explicit behavioral-contract rules and previously established correction rules
may constrain execution.
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
GUARD_MAINTENANCE_RE = re.compile(r"chomview_guard\.py\s+(?:resolve|retire|status|list|remember|violation|contract-status)\b")
CONTRACT_DECISIONS = ("ALLOW", "LOOK_AGAIN", "REQUIRE_CONSENT", "BLOCK")
CONTRACT_RANK = {name: i for i, name in enumerate(CONTRACT_DECISIONS)}

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

DEFAULT_CONTRACT = {
    "schema_version": 1,
    "contract_id": "chomview-default-v0.4",
    "contract_version": "0.4.0",
    "default_decision": "ALLOW",
    "principles": [
        "wild cognition != wild authority",
        "personality != permission",
        "capability != permission",
        "availability != authorization",
        "preference != spending authority",
        "new evidence/context != authorization for a new objective",
    ],
    "rules": [],
}



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


def contract_path(root: Path) -> Path:
    return root / ".claude" / "chomview" / "behavioral-contract.json"


def default_contract() -> dict[str, Any]:
    return json.loads(json.dumps(DEFAULT_CONTRACT))


def load_contract(root: Path) -> dict[str, Any]:
    path = contract_path(root)
    if not path.exists():
        return default_contract()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fallback = default_contract()
        fallback["_load_error"] = f"invalid behavioral contract: {exc}"
        return fallback
    if not isinstance(data, dict) or not isinstance(data.get("rules"), list):
        fallback = default_contract()
        fallback["_load_error"] = "invalid behavioral contract structure"
        return fallback
    return data


def actor_id(payload: dict[str, Any]) -> str:
    return str(payload.get("agent_id") or payload.get("actor_id") or os.environ.get("CHOMVIEW_ACTOR_ID") or "primary")


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


def format_context(store: dict[str, Any], contract: dict[str, Any] | None = None) -> str:
    contract = contract or default_contract()
    rules = active_rules(store)
    rows = [
        "ChomView v0.4 behavioral state. Preserve established correction rules and the project behavioral contract unless explicitly changed by the owner.",
    ]
    for rule in rules[:20]:
        rows.append(f"- CONTINUITY [{rule.get('level','NOTICE')}] {rule.get('rule_id')}: {rule.get('changed_rule')}")
    principles = contract.get("principles") or []
    for principle in principles[:12]:
        rows.append(f"- CONTRACT PRINCIPLE: {principle}")
    active_contract = [r for r in contract.get("rules", []) if isinstance(r, dict) and r.get("enabled", True)]
    for rule in sorted(active_contract, key=lambda r: int(r.get("priority", 0)), reverse=True)[:20]:
        rows.append(
            f"- AUTHORITY [{rule.get('decision','ALLOW')}] {rule.get('rule_id')}: {rule.get('rationale','')}"
        )
    if contract.get("_load_error"):
        rows.append(f"- CONTRACT WARNING: {contract['_load_error']}; deterministic contract rules were not loaded.")
    rows.append(
        "Do not infer authority from capability, availability, preference, personality, culture, or a new upload. Protected stakeholder resources require the authority declared by the behavioral contract."
    )
    return "\n".join(rows)


def contract_matcher_hit(rule: dict[str, Any], payload: dict[str, Any]) -> bool:
    tool_name = str(payload.get("tool_name", ""))
    tool_input = payload.get("tool_input", {})
    serialized = json.dumps(tool_input, ensure_ascii=False, sort_keys=True)
    actor = actor_id(payload)
    for matcher in rule.get("matchers") or []:
        if not isinstance(matcher, dict):
            continue
        actor_re = str(matcher.get("actor_regex", ".*"))
        tool_re = str(matcher.get("tool", ".*"))
        input_re = str(matcher.get("input_regex", ".*"))
        try:
            if (re.search(actor_re, actor, flags=re.IGNORECASE) and
                re.search(tool_re, tool_name) and
                re.search(input_re, serialized, flags=re.IGNORECASE | re.DOTALL)):
                return True
        except re.error:
            continue
    return False


def strongest_contract_rule(contract: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any] | None:
    hits = [
        r for r in contract.get("rules", [])
        if isinstance(r, dict) and r.get("enabled", True) and contract_matcher_hit(r, payload)
    ]
    if not hits:
        return None
    return max(
        hits,
        key=lambda r: (CONTRACT_RANK.get(str(r.get("decision", "ALLOW")), 0), int(r.get("priority", 0))),
    )


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


def pretool_decision(
    root: Path,
    store: dict[str, Any],
    payload: dict[str, Any],
    contract: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    contract = contract or default_contract()
    if is_guard_maintenance(payload):
        return None

    tool_name = str(payload.get("tool_name", ""))
    frozen = [r for r in active_rules(store) if r.get("level") in {"FREEZE", "ESCALATE"}]
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
                "additionalContext": format_context(store, contract),
            }
        }

    contract_rule = strongest_contract_rule(contract, payload)
    contract_decision = str(contract_rule.get("decision", "ALLOW")) if contract_rule else str(contract.get("default_decision", "ALLOW"))

    hits = [r for r in active_rules(store) if matcher_hit(r, payload)]
    recurrence_level = None
    recurrence_reason = None
    if hits:
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
        recurrence_level = str(strongest.get("level"))
        recurrence_reason = (
            f"CHOMVIEW_{recurrence_level}: repeated acknowledged pattern matched rule {strongest.get('rule_id')}. "
            f"Changed rule: {strongest.get('changed_rule')}"
        )

    contract_reason = None
    if contract_rule:
        stakeholders = ", ".join(str(x) for x in contract_rule.get("stakeholders", [])) or "none declared"
        resources = ", ".join(str(x) for x in contract_rule.get("resources", [])) or "none declared"
        contract_reason = (
            f"CHOMVIEW_{contract_decision}: behavioral contract rule {contract_rule.get('rule_id')} matched actor {actor_id(payload)}. "
            f"Authority={contract_rule.get('authority')}; stakeholders={stakeholders}; resources={resources}. "
            f"{contract_rule.get('rationale','')}"
        )

    deny = contract_decision == "BLOCK" or recurrence_level in {"STRIKE", "FREEZE", "ESCALATE"}
    ask = contract_decision == "REQUIRE_CONSENT" or recurrence_level == "WARNING"
    advisory = contract_decision == "LOOK_AGAIN" or recurrence_level == "NOTICE"

    reasons = [x for x in (contract_reason, recurrence_reason) if x]
    reason = " ".join(reasons)
    context = format_context(store, contract)

    if deny:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason or "CHOMVIEW_BLOCK: explicit behavioral boundary matched.",
                "additionalContext": context,
            }
        }
    if ask:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": reason or "CHOMVIEW_REQUIRE_CONSENT: explicit consent is required.",
                "additionalContext": context,
            }
        }
    if advisory:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": (reason + " Reconsider before proceeding.").strip(),
            }
        }
    return None


def handle_hook(payload: dict[str, Any]) -> int:
    root = project_dir(payload)
    store = load_store(root)
    contract = load_contract(root)
    # Materialize core state so it survives fresh sessions and compaction.
    save_store(root, store)
    event = str(payload.get("hook_event_name", ""))

    if event in {"SessionStart", "UserPromptSubmit"}:
        context = format_context(store, contract)
        if context:
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": event,
                    "additionalContext": context,
                }
            }, ensure_ascii=False))
        return 0

    if event == "PreToolUse":
        decision = pretool_decision(root, store, payload, contract)
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


def cmd_contract_status(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve() if args.project else project_dir()
    print(json.dumps(load_contract(root), ensure_ascii=False, indent=2))
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="ChomView v0.4 Behavioral Continuity + Compatibility Guard")
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

    c = sub.add_parser("contract-status", help="print the active behavioral compatibility contract")
    c.set_defaults(func=cmd_contract_status)
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
