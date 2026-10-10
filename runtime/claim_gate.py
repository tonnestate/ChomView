"""CLAIM-EVIDENCE/1: evidence-bound terminal-claim review for ChomView.

The model's prose, file names, and self-declared verification do not grant proof.
Only a trusted host can produce a MAC-bound review referencing external evidence.
The lexical detector deliberately covers a narrow set of high-impact claims;
it is not a general-purpose factuality or truth classifier.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import hmac
import json
import re
from typing import Any

SCHEMA = "CLAIM-EVIDENCE/1"
_KINDS = {
    "IMPLEMENTATION": re.compile(
        r"(?i)(?:\\b(?:implementation|implementierung|reparatur|auftrag|work|changes|"
        r"änderungen|fix|patch|code)\\b.{0,45}\\b(?:complete|completed|done|"
        r"finished|fertig|abgeschlossen|erledigt|umgesetzt|implemented|fixed|behoben)\\b"
        r"|\\b(?:alles erledigt|vollständig umgesetzt|reparatur abgeschlossen)\\b)"
    ),
    "TEST_RESULT": re.compile(
        r"(?i)(?:\b(?:tests?|prüfungen?)\b.{0,55}\b(?:pass(?:ed)?|green|grün|bestanden|erfolgreich)\b"
        r"|\b\d+\s+(?:tests?|prüfungen?)\s+(?:passed|bestanden)\b)"
    ),
    "DEPLOYMENT": re.compile(
        r"(?i)\b(?:deployed|deployment complete|production ready|in production|"
        r"produktiv (?:installiert|ausgerollt|bereit)|auf dem vps installiert|live geschaltet)\b"
    ),
    "REPOSITORY": re.compile(
        r"(?i)\b(?:merged|gemergt|zusammengeführt|"
        r"main (?:updated|aktualisiert)|branch (?:synchronisiert|synced))\b"
    ),
    "VERIFICATION": re.compile(
        r"(?i)\b(?:verified|verifiziert|unabhängig geprüft|"
        r"independently verified|abnahme bestanden)\b"
    ),
}
# A nearby explicit downgrade is not a claim of proven success.
_QUALIFIER = re.compile(
    r"(?i)\b(?:not|nicht|never|kein(?:e|en|er)?|unverified|unbestätigt|"
    r"ungeprüft|pending|offen|ohne nachweis|noch nicht)\b"
)
_MAX_MESSAGE = 32_768
_MAX_REPORT = 32_768
_MAX_REFS = 16
_MAX_AGE_SECONDS = 900  # at most 15 minutes; never reuse stale host proof


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def message_digest(message: str) -> str:
    return hashlib.sha256(message.encode("utf-8")).hexdigest()


def protected_claims(message: str) -> list[str]:
    """Select only high-impact *positive* assertions; abstain on uncertainty."""
    kinds: list[str] = []
    if len(message) > _MAX_MESSAGE:
        return ["UNSCANNED"]  # bounded fail-closed in enforcing mode
    for kind, pattern in _KINDS.items():
        found = False
        for match in pattern.finditer(message):
            # A nearby negation is conservative: false negative > false block.
            pre = message[max(0, match.start() - 45):match.start()]
            clause = re.split(r"[.;\n!?]", pre)[-1]
            if _QUALIFIER.search(clause):
                continue
            found = True
            break
        if found:
            kinds.append(kind)
    return kinds


def _verified_report(report: Any, *, session_id: str, digest: str, key: str | None) -> bool:
    if not isinstance(report, dict) or not isinstance(key, str) or len(key) < 32:
        return False
    if len(_canonical(report)) > _MAX_REPORT:
        return False
    if report.get("schema") != SCHEMA or report.get("session_id") != session_id:
        return False
    if report.get("message_sha256") != digest:
        return False
    try:
        issued = dt.datetime.fromisoformat(str(report["issued_at"]).replace("Z", "+00:00"))
        if issued.tzinfo is None:
            return False
        age = (dt.datetime.now(dt.timezone.utc) - issued.astimezone(dt.timezone.utc)).total_seconds()
        if not 0 <= age <= _MAX_AGE_SECONDS:
            return False
    except (KeyError, TypeError, ValueError, OverflowError):
        return False
    claims = report.get("claims")
    if not isinstance(claims, list) or len(claims) > len(_KINDS) or not claims:
        return False
    for claim in claims:
        if not isinstance(claim, dict) or claim.get("kind") not in _KINDS:
            return False
        if claim.get("verdict") not in {"SUPPORTED", "CONTRADICTED", "UNVERIFIED"}:
            return False
        refs = claim.get("evidence_refs")
        if not isinstance(refs, list) or len(refs) > _MAX_REFS:
            return False
        if not all(isinstance(ref, str) and 4 <= len(ref) <= 256 for ref in refs):
            return False
        if claim["verdict"] == "SUPPORTED" and not refs:
            return False
    signature = report.get("signature")
    if not isinstance(signature, str) or len(signature) != 64:
        return False
    unsigned = {k: v for k, v in report.items() if k != "signature"}
    expected = hmac.new(key.encode("utf-8"), _canonical(unsigned), hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


def sign_host_review(
    *, message: str, session_id: str, claims: list[dict], host_key: str,
) -> dict:
    """For an *independent trusted host verifier only*, never an agent tool.

    This authenticates the verifier's decision. It cannot establish whether
    the verifier actually ran a test or read the claimed source.
    """
    if not isinstance(host_key, str) or len(host_key) < 32:
        raise ValueError("trusted host key must be at least 32 characters")
    payload = {
        "schema": SCHEMA,
        "session_id": session_id,
        "message_sha256": message_digest(message),
        "issued_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "claims": claims,
    }
    payload["signature"] = hmac.new(host_key.encode(), _canonical(payload), hashlib.sha256).hexdigest()
    if not _verified_report(payload, session_id=session_id, digest=message_digest(message), key=host_key):
        raise ValueError("invalid host review claims")
    return payload


def review_final(
    message: str, session_id: str, *, report: Any = None,
    host_key: str | None = None, mode: str = "observe",
) -> dict:
    """No mutation. `block` applies only to explicit high-impact success claims.

    A signed SUPPORTED verdict is a statement *by the host reviewer*.
    It is not machine proof of the referenced source's semantics.
    """
    if mode not in {"observe", "enforce"}:
        raise ValueError("mode must be observe or enforce")
    if not isinstance(message, str) or not isinstance(session_id, str) or not session_id:
        raise ValueError("message and session_id are required")
    kinds = protected_claims(message)
    authenticated = _verified_report(
        report, session_id=session_id, digest=message_digest(message), key=host_key
    )
    signed = {
        claim["kind"]: claim
        for claim in report["claims"]
    } if authenticated else {}
    findings = []
    for kind in kinds:
        claim = signed.get(kind)
        status = claim["verdict"] if claim else "UNVERIFIED"
        findings.append({
            "kind": kind,
            "status": status,
            "evidence_refs": claim["evidence_refs"][:_MAX_REFS] if claim else [],
        })
    problematic = [f for f in findings if f["status"] != "SUPPORTED"]
    return {
        "schema": SCHEMA,
        "status": ("NO_PROTECTED_CLAIMS" if not kinds else
                   "SUPPORTED" if not problematic else
                   "CONTRADICTED" if any(f["status"] == "CONTRADICTED" for f in findings) else
                   "UNVERIFIED"),
        "authenticated_host_review": authenticated,
        "mode": mode,
        "findings": findings,
        "decision": "block" if mode == "enforce" and problematic else "allow",
        "reason": (
            "ChomView: protected completion or verification claim lacks a matching "
            "host-authenticated, source-referenced verdict. Inspect the evidence "
            "or explicitly state that this result is not verified."
            if problematic else ""
        ),
        "limitations": "Checks selected claim classes and authenticated review bindings, not arbitrary factual truth.",
    }


def main(argv: list[str] | None = None) -> int:
    """Host-pinned subprocess interface; does not offer any signing command."""
    import argparse
    import os
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(description="ChomView claim-evidence terminal review")
    parser.add_argument("--session", required=True)
    parser.add_argument("--mode", choices=("observe", "enforce"), default="observe")
    parser.add_argument("--report-file", help="trusted-host produced and protected signed review JSON")
    args = parser.parse_args(argv)

    payload = json.loads(sys.stdin.read())
    if not isinstance(payload, dict):
        raise ValueError("expected a JSON hook payload")
    message = payload.get("last_assistant_message")
    if not isinstance(message, str):
        raise ValueError("last_assistant_message missing")
    report = None
    if args.report_file:
        report_path = Path(args.report_file)
        # A trusted host must configure path and permissions outside the agent workspace.
        if report_path.is_file() and report_path.stat().st_size <= _MAX_REPORT:
            report = json.loads(report_path.read_text(encoding="utf-8"))
    result = review_final(message, args.session, report=report,
                          host_key=os.environ.get("CHOMVIEW_CLAIM_GATE_KEY"),
                          mode=args.mode)
    # No confidential source contents or raw message in output.
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
