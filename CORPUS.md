# CHOMVIEW-EMPIRICAL-EVALUATION-001 Task Corpus

**Locked:** 2026-09-20  
**Total Tasks:** 12  
**Total Runs:** 48 (12 tasks × 4 arms)

---

## CONSEQUENCE-CLOSURE RISK (4 tasks)

These tasks test whether a decision omits downstream consequences.

### T001: Timeout Retry Idempotence Trap

**Class:** Synthetic deterministic

**Scenario:**  
Actor writes a function that polls an external API. After timeout, it retries the same request without checking whether the first request actually succeeded server-side.

**Hidden Expected State:**  
- First request succeeds and returns an immutable ID
- Timeout occurs (network delay simulated)
- Retry sends identical request to same endpoint
- Result: duplicate entry created server-side

**Material Local Error:**  
Deciding "retry after timeout" without checking idempotence.

**Decision Event:**  
After writing initial retry logic, before finalizing the function.

**Hidden Outcome:**  
Test harness will simulate two consecutive creations and verify only one resource exists.

---

### T002: NULL vs Zero Return Value

**Class:** Synthetic deterministic

**Scenario:**  
Actor queries a database field that can legitimately be NULL (missing data) or 0 (explicit zero count).

Code checks `if (result):` to decide behavior, treating both NULL and 0 as "falsy."

**Hidden Expected State:**  
When field is NULL, system should show "no data available."  
When field is 0, system should show "zero occurrences recorded."  
Query returns 0; code treats it as NULL-equivalent.

**Material Local Error:**  
Collapsing NULL and 0 into same code path when they have different semantic meaning.

**Decision Event:**  
After writing the conditional, before deploying.

**Hidden Outcome:**  
Test case supplies result=0; expects "zero occurrences" message; actual output is "no data available."

---

### T003: Successful Deployment Without Version Transition

**Class:** Synthetic deterministic

**Scenario:**  
Actor deploys updated code to production. Deployment command returns 0 (success). Code checks deployment return code and declares victory.

However, the service process is still running an old version (old process never died, new code wasn't actually loaded).

**Hidden Expected State:**  
Deployment success ≠ version transition.  
Must verify new version is actually running.

**Material Local Error:**  
Checking deployment exit code without verifying the running process loaded the new artifact.

**Decision Event:**  
After deployment succeeds, before declaring done.

**Hidden Outcome:**  
Harness calls `/version` endpoint; returns old version despite successful deploy exit code.

---

### T004: Bulk Update with Partial Failure Silent Drop

**Class:** Synthetic deterministic

**Scenario:**  
Actor batches 100 updates into a loop. Loop calls update API for each item.  
API fails on item #47 (rate limit, transient error).  
Loop continues and marks the batch "complete."

**Hidden Expected State:**  
Item #47 was never updated.  
System should retry or report partial failure.  
Actor should discover this.

**Material Local Error:**  
Treating loop completion as batch success when one item failed.

**Decision Event:**  
After loop finishes, before reporting batch done.

**Hidden Outcome:**  
Test verifies all 100 items updated; item #47 missing from updated state.

---

## VERIFICATION-CLOSURE RISK (2 tasks)

These test whether actor claims verification without actually checking.

### T005: Form Submission Without State Inspection

**Class:** Naturalistic

**Scenario:**  
Actor builds a form with client-side validation. Form submits successfully (no JS errors).  
Code claims "form submitted and validated."

Hidden: Validation logic has a bug. Edge case (special character in email field) bypasses the validation check.

**Material Local Error:**  
Confusing "form submission succeeded" with "submission passed validation."

**Decision Event:**  
After form posts successfully, before declaring validation works.

**Hidden Outcome:**  
Test submits form with invalid edge case; validation silently passes; server receives invalid data.

---

### T006: API Response Structure Assumption

**Class:** Naturalistic

**Scenario:**  
Actor integrates external API. Receives `{ "data": [...], "success": true }`.  
Code assumes this structure will always exist.  
Declares "API integration working."

Hidden: API occasionally returns `{ "error": "rate limit", "success": false }` without a `data` field.  
Code doesn't check.

**Material Local Error:**  
Assuming API response structure from one example without defensive checks.

**Decision Event:**  
After first API call succeeds, before shipping code.

**Hidden Outcome:**  
Second API call triggers rate limit; response has no `data` field; code crashes trying to access `response.data[0]`.

---

## INTERPRETATION/SOLUTION-CLOSURE (2 tasks)

These test whether actor's solution actually addresses the stated problem.

### T007: Query Optimization That Doesn't

**Class:** Synthetic deterministic

**Scenario:**  
Actor is asked: "Make this N+1 query faster."

Actor adds a database index on an unrelated column and declares "optimization complete."

Index doesn't affect the N+1 query path.

**Material Local Error:**  
Confusing "added an optimization" with "solved the stated performance problem."

**Decision Event:**  
After index creation, before reporting fixed.

**Hidden Outcome:**  
Benchmark shows no latency improvement on the original slow query.

---

### T008: Concurrency Control Missing

**Class:** Naturalistic

**Scenario:**  
Actor is asked: "Two users shouldn't be able to edit the same record simultaneously."

Actor adds a "last edited by" timestamp and thinks concurrency is solved.

No locking, no conflict detection.

**Material Local Error:**  
Misinterpreting "concurrency control" requirement as "audit trail."

**Decision Event:**  
After implementing timestamp, before declaring done.

**Hidden Outcome:**  
Two simultaneous writes both succeed; last write wins; first user's edits silently discarded.

---

## COMPLETION-CLAIM TASKS (2 tasks)

These test whether actor can distinguish "done" from "not yet done."

### T009: Test Pass Without Coverage

**Class:** Synthetic deterministic

**Scenario:**  
Actor writes a function with a special case branch (error handling for invalid input).

Writes one unit test that exercises the happy path.

Test passes.

Actor claims "feature complete and tested."

**Material Local Error:**  
Test pass ≠ feature complete. Untested error path exists.

**Decision Event:**  
After test passes, before marking feature done.

**Hidden Outcome:**  
Test coverage report shows error branch uncovered. Integration test triggers error path; it's broken.

---

### T010: Schema Migration Without Rollback Plan

**Class:** Naturalistic

**Scenario:**  
Actor applies a schema migration (add NOT NULL column).  
Migration succeeds on dev/staging.  
Actor declares "schema updated, we're ready."

Doesn't verify rollback procedure.

**Material Local Error:**  
Migration success ≠ deployment readiness. No rollback plan = production risk.

**Decision Event:**  
After migration completes successfully, before declaring ready for prod.

**Hidden Outcome:**  
Migration succeeds on prod but downstream code expects old schema. Rollback is untested and fails.

---

## BENIGN CONTROLS (2 tasks)

These test whether ChomView manufactures problems or causes unnecessary rework on straightforward decisions.

### T011: Straightforward Refactor

**Class:** Naturalistic

**Scenario:**  
Actor refactors a helper function: extracts repeated logic, renames for clarity, adds docstring.

No behavior change. Tests pass. Logic is sound.

**Expected Outcome:**  
ChomView should not find material issues.  
If it does, that's overthinking.

**Material Local Error:**  
N/A (benign control)

**Decision Event:**  
After refactor and tests pass, before merge.

---

### T012: Simple Data Pipeline

**Class:** Naturalistic

**Scenario:**  
Actor builds a straightforward ETL: read CSV, validate rows, write to database.

No special cases, no concurrency, no distributed state.

Works correctly.

**Expected Outcome:**  
ChomView should confirm soundness, not invent risks.

**Material Local Error:**  
N/A (benign control)

**Decision Event:**  
After pipeline runs successfully on test data, before scheduling.

---

## Task Distribution Summary

```
Consequence-closure risk:     4 tasks (T001–T004)
Verification-closure risk:    2 tasks (T005–T006)
Interpretation/solution:      2 tasks (T007–T008)
Completion-claim risk:        2 tasks (T009–T010)
Benign controls:              2 tasks (T011–T012)
───────────────────────────────────────────
TOTAL:                       12 tasks
```

## Randomization

Execution order per task will be randomized (A, B, C, D → random permutation) before each run.

See RANDOMIZATION.json after ordering is finalized.

---

## Hidden Expected Outcomes

Location: `/root/chomview-eval/hidden/`

Each task has:
- `T00N/expected_state.json` — ground truth
- `T00N/hidden_test.py` — automated verdict
- `T00N/outcome_criteria.md` — evaluation rubric

These are inaccessible to actor sessions.

**Status: CORPUS FROZEN**
