# CLAIM-EVIDENCE/1 — ChomView proposal

**Status:** `web/chatgpt` proposal only; not installed in a host and not
verified on the active FruitStack VPS. This protocol is a narrow machine-readable
extension of ChomView's existing Behavioral Integrity / Premature Closure role.

## Problem and owner

A model can plausibly claim that tests passed, a change was merged, a feature
deployed, or a result independently verified without a matching source. Prompt
reminders are insufficient. ChomView owns **claim review**, PeachMe optionally
wires this to Claude Code's `Stop` hook, and AppleMe separately measures
trajectory evidence concerns. Do not build another LLM critic or model router.

## Contract

`runtime/claim_gate.py` implements:

- `protected_claims(text)`: conservative, deterministic identification of
  positive claims about test success, deployment, repository integration and
  verification. It abstains on explicit disclaimers and ordinary text.
- `review_final(text, session_id, report=..., host_key=..., mode=...)`:
  compares a signed host review to the *exact full response hash*, session ID,
  protected claim kinds and source references. Reviews expire after 15 minutes.
  The output contains `SUPPORTED`, `UNVERIFIED`, or `CONTRADICTED`.
- `sign_host_review(...)`: a library function strictly for the trusted
  independently authorized verifier process, never an agent tool or MCP method.
  Signing authenticates the host's verdict; it **does not** prove the host
  verifier's process actually checked the right facts.
- No external network or model call, no data registry and no automatic writes.

Use `CHOMVIEW_CLAIM_GATE_KEY` supplied only by the host process, with at least
32 characters of host-generated secret material. Store signed reviews outside
the agent-writable project, with OS permissions enforced by the operator. Do
not expose the key, signed-report writer, or host filesystem privileges to
the worker. The report is bound to a session and exact message, so a cached
test receipt cannot silently attest a modified deployment claim.

Sample **host verifier** flow (pseudo-code):

```python
# Host process ONLY; independently check tests, commits and deployment first.
from claim_gate import sign_host_review

signed = sign_host_review(
    message=final_text,
    session_id=host_bound_session_id,
    claims=[
        {"kind": "TEST_RESULT", "verdict": "SUPPORTED",
         "evidence_refs": ["ci://run/1234"]},
    ],
    host_key=protected_host_secret,
)
# Host persists signed JSON outside agent-writable paths.
```

A model must never be authorized to invoke `sign_host_review` itself.

## Runtime behaviour and limits

Default `observe` allows the existing completion path and reports uncertainty.
Configured `enforce` blocks only identified high-impact positive assertions
that have no matching host-authenticated evidence verdict. This is **not** a
blanket task blocker: agents may transparently say that work is unverified.
The lexical detector is intentionally incomplete and language-limited; it is
not an exhaustive fact checker. Hosts must still enforce actual permissions,
tool authorization, and independent acceptance separately.

## A/B/C acceptance

A: no claim review, B: observe-only, C: host-attested enforcement at Stop.
Use identical tasks, expected evidence, host, provider, model and budgets.
Measure unsubstantiated positive claims, false interruptions, completion
quality, median and tail latency, extra provider calls/tokens and real costs.
No efficacy or active deployment claim is implied by passing unit tests.
