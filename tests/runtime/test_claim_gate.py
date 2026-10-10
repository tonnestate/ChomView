"""CLAIM-EVIDENCE/1 contract tests: default uncertainty, signed support, tamper."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("claim_gate", ROOT / "runtime" / "claim_gate.py")
claim_gate = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = claim_gate
spec.loader.exec_module(claim_gate)
SECRET = "this-is-the-trusted-host-only-verification-secret-123"


class ClaimGateTests(unittest.TestCase):
    def test_protected_assertions_and_qualified_downgrades(self):
        self.assertEqual(claim_gate.protected_claims("CI: 93 tests passed. Deployed in production."),
                         ["TEST_RESULT", "DEPLOYMENT"])
        self.assertEqual(claim_gate.protected_claims("Noch nicht verifiziert. Tests sind offen."), [])
        self.assertEqual(claim_gate.protected_claims("I can help explain why tests fail."), [])
        self.assertEqual(claim_gate.protected_claims(""), [])

    def test_completion_claim_is_protected_without_blocking_clear_uncertainty(self):
        self.assertEqual(
            claim_gate.protected_claims("Die Reparatur wurde vollständig umgesetzt."),
            ["IMPLEMENTATION"],
        )
        self.assertEqual(
            claim_gate.review_final(
                "Die Reparatur wurde vollständig umgesetzt.",
                "sid", mode="enforce",
            )["decision"],
            "block",
        )
        self.assertEqual(
            claim_gate.protected_claims("Noch nicht vollständig umgesetzt."),
            [],
        )

    def test_no_evidence_is_review_only_by_default(self):
        v = claim_gate.review_final("93 tests passed.", "sid-1")
        self.assertEqual(v["decision"], "allow")
        self.assertEqual(v["status"], "UNVERIFIED")
        self.assertFalse(v["authenticated_host_review"])
        self.assertEqual(v["findings"][0]["kind"], "TEST_RESULT")

    def test_protected_final_claim_is_blocked_only_in_explicit_enforcement(self):
        v = claim_gate.review_final("Deployment complete; tests passed.",
                                    "sid-1", mode="enforce")
        self.assertEqual(v["status"], "UNVERIFIED")
        self.assertEqual(v["decision"], "block")
        self.assertEqual(claim_gate.review_final(
            "This has not been deployed or verified.", "sid-1", mode="enforce"
        )["decision"], "allow")

    def test_signed_report_must_bind_session_exact_message_refs_and_key(self):
        message = "93 tests passed. Deployed in production."
        claims = [{"kind": kind, "verdict": "SUPPORTED", "evidence_refs": [ref]}
                  for kind, ref in [("TEST_RESULT", "ci://run/15"),
                                    ("DEPLOYMENT", "receipt://deploy/44")]]
        report = claim_gate.sign_host_review(
            message=message, session_id="sid-1", claims=claims, host_key=SECRET
        )
        ok = claim_gate.review_final(message, "sid-1", report=report,
                                     host_key=SECRET, mode="enforce")
        self.assertEqual(ok["decision"], "allow")
        self.assertTrue(ok["authenticated_host_review"])
        for altered in [
            claim_gate.review_final(message+" ", "sid-1", report=report,
                                    host_key=SECRET, mode="enforce"),
            claim_gate.review_final(message, "sid-2", report=report,
                                    host_key=SECRET, mode="enforce"),
            claim_gate.review_final(message, "sid-1", report=report,
                                    host_key="wrong-but-long-enough-password-value", mode="enforce"),
        ]:
            self.assertEqual(altered["decision"], "block")
            self.assertFalse(altered["authenticated_host_review"])

        modified = dict(report)
        modified["claims"] = [{"kind": "TEST_RESULT", "verdict": "SUPPORTED",
                               "evidence_refs": ["fraudulent://self-claim"]}]
        self.assertFalse(claim_gate.review_final(
            message, "sid-1", report=modified, host_key=SECRET, mode="enforce"
        )["authenticated_host_review"])

    def test_contradiction_blocks_and_unsigned_self_report_cannot_grant_proof(self):
        message = "Everything is verified."
        unsigned = {"schema": claim_gate.SCHEMA, "session_id": "x",
                    "message_sha256": claim_gate.message_digest(message),
                    "claims": [{"kind": "VERIFICATION", "verdict": "SUPPORTED",
                                "evidence_refs": ["claim://my-own-text"]}]}
        self.assertEqual(claim_gate.review_final(
            message, "x", report=unsigned, host_key=SECRET, mode="enforce"
        )["decision"], "block")
        signed = claim_gate.sign_host_review(
            message=message, session_id="x",
            claims=[{"kind": "VERIFICATION", "verdict": "CONTRADICTED",
                     "evidence_refs": ["git://real-change/7"]}],
            host_key=SECRET,
        )
        review = claim_gate.review_final(
            message, "x", report=signed, host_key=SECRET, mode="enforce"
        )
        self.assertEqual(review["status"], "CONTRADICTED")
        self.assertEqual(review["decision"], "block")

    def test_long_message_is_not_assumed_safe(self):
        review = claim_gate.review_final("a" * 33_000, "sid", mode="enforce")
        self.assertEqual(review["findings"][0]["kind"], "UNSCANNED")
        self.assertEqual(review["decision"], "block")

    def test_cli_verifies_host_report(self):
        message = "93 tests passed."
        report = claim_gate.sign_host_review(
            message=message, session_id="sid",
            claims=[{"kind": "TEST_RESULT", "verdict": "SUPPORTED",
                     "evidence_refs": ["ci://run/88"]}],
            host_key=SECRET,
        )
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "host-review.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            import os
            env = {**os.environ, "CHOMVIEW_CLAIM_GATE_KEY": SECRET}
            p = subprocess.run(
                [sys.executable, str(ROOT / "runtime" / "claim_gate.py"),
                 "--session", "sid", "--mode", "enforce",
                 "--report-file", str(path)],
                input=json.dumps({"last_assistant_message": message}),
                env=env, capture_output=True, text=True,
            )
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(json.loads(p.stdout)["status"], "SUPPORTED")


if __name__ == "__main__":
    unittest.main()
