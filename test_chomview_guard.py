#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("chomview_guard", ROOT/"runtime/chomview_guard.py")
guard=importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(guard)

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.store=guard.default_store()
        self.store["rules"].append({
            "rule_id":"test.repeat",
            "pattern":"repeat bypass",
            "changed_rule":"Do not use --no-verify after acknowledging verification is required.",
            "source_did":"T",
            "materiality":"HIGH",
            "active":True,
            "immutable":False,
            "violation_count":0,
            "level":"NOTICE",
            "matchers":[{"tool":"Bash","input_regex":"--no-verify"}]
        })
        guard.save_store(self.root,self.store)

    def tearDown(self): self.tmp.cleanup()

    def call(self, command):
        store=guard.load_store(self.root)
        payload={"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":command},"cwd":str(self.root)}
        return guard.pretool_decision(self.root,store,payload)

    def test_core_rule_is_present(self):
        ctx=guard.format_context(guard.load_store(self.root))
        self.assertIn("new objective",ctx)
        self.assertIn("core.evidence-is-not-authorization",ctx)

    def test_escalation(self):
        d1=self.call("git commit --no-verify")
        self.assertNotIn("permissionDecision",d1["hookSpecificOutput"])
        d2=self.call("git commit --no-verify")
        self.assertEqual("ask",d2["hookSpecificOutput"]["permissionDecision"])
        d3=self.call("git commit --no-verify")
        self.assertEqual("deny",d3["hookSpecificOutput"]["permissionDecision"])
        d4=self.call("git commit --no-verify")
        self.assertEqual("deny",d4["hookSpecificOutput"]["permissionDecision"])
        store=guard.load_store(self.root)
        r=next(x for x in store["rules"] if x["rule_id"]=="test.repeat")
        self.assertEqual("FREEZE",r["level"])

    def test_freeze_blocks_unrelated_mutation_but_not_read(self):
        for _ in range(4): self.call("git commit --no-verify")
        store=guard.load_store(self.root)
        write={"hook_event_name":"PreToolUse","tool_name":"Write","tool_input":{"file_path":"x","content":"y"},"cwd":str(self.root)}
        read={"hook_event_name":"PreToolUse","tool_name":"Read","tool_input":{"file_path":"x"},"cwd":str(self.root)}
        self.assertEqual("deny",guard.pretool_decision(self.root,store,write)["hookSpecificOutput"]["permissionDecision"])
        self.assertIsNone(guard.pretool_decision(self.root,store,read))

    def test_resolve_resets_but_keeps_rule(self):
        for _ in range(3): self.call("git commit --no-verify")
        class A: project=str(self.root); rule_id="test.repeat"; evidence="corrected and verified"
        guard.cmd_resolve(A())
        store=guard.load_store(self.root)
        r=next(x for x in store["rules"] if x["rule_id"]=="test.repeat")
        self.assertTrue(r["active"])
        self.assertEqual(0,r["violation_count"])
        self.assertEqual("NOTICE",r["level"])

if __name__=="__main__": unittest.main()
