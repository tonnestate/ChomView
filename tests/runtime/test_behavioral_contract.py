#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("chomview_guard", ROOT/"runtime/chomview_guard.py")
guard=importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(guard)

class BehavioralContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.store=guard.default_store()
        guard.save_store(self.root,self.store)

    def tearDown(self):
        self.tmp.cleanup()

    def payload(self, tool="ProviderCall", value="premium", actor="wild-agent"):
        return {
            "hook_event_name":"PreToolUse",
            "tool_name":tool,
            "tool_input":{"provider":value},
            "actor_id":actor,
            "cwd":str(self.root),
        }

    def contract(self, decision="REQUIRE_CONSENT", actor_regex="wild-.*"):
        return {
            "schema_version":1,
            "contract_id":"test",
            "contract_version":"0.4.0",
            "default_decision":"ALLOW",
            "principles":["wild cognition != wild authority", "preference != spending authority"],
            "rules":[{
                "rule_id":"budget.premium",
                "enabled":True,
                "priority":100,
                "decision":decision,
                "authority":"REQUIRES_OWNER_CONSENT" if decision=="REQUIRE_CONSENT" else "DENY_EXECUTION",
                "stakeholders":["owner"],
                "resources":["money","tokens"],
                "rationale":"Protected owner resources require declared authority.",
                "matchers":[{"actor_regex":actor_regex,"tool":"ProviderCall","input_regex":"premium"}],
            }],
        }

    def test_default_contract_is_non_normalizing(self):
        ctx=guard.format_context(self.store,guard.default_contract())
        self.assertIn("wild cognition != wild authority",ctx)
        self.assertIn("preference != spending authority",ctx)
        self.assertIn("personality",ctx)

    def test_require_consent(self):
        d=guard.pretool_decision(self.root,self.store,self.payload(),self.contract())
        self.assertEqual("ask",d["hookSpecificOutput"]["permissionDecision"])
        reason=d["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("owner",reason)
        self.assertIn("money",reason)

    def test_block(self):
        d=guard.pretool_decision(self.root,self.store,self.payload(),self.contract("BLOCK"))
        self.assertEqual("deny",d["hookSpecificOutput"]["permissionDecision"])

    def test_actor_scope(self):
        d=guard.pretool_decision(self.root,self.store,self.payload(actor="trusted-agent"),self.contract())
        self.assertIsNone(d)

    def test_look_again_does_not_create_authority(self):
        c=self.contract("LOOK_AGAIN")
        c["rules"][0]["authority"]="CAN_EXECUTE"
        d=guard.pretool_decision(self.root,self.store,self.payload(),c)
        self.assertNotIn("permissionDecision",d["hookSpecificOutput"])
        self.assertIn("LOOK_AGAIN",d["hookSpecificOutput"]["additionalContext"])

if __name__=="__main__":
    unittest.main()
