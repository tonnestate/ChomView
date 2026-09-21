# CHOMVIEW-EMPIRICAL-EVALUATION-001 PILOT REPORT

**Date:** 2026-09-20  
**Status:** PILOT PHASE COMPLETE  
**Runs:** 12 (3 tasks × 4 arms)

---

## PILOT RESULTS SUMMARY

### Material Local Error Rates

**Overall MLE Rate:** 0.0% (0/12 runs)

**By Task Class:**
- Consequence-closure (T001): 0.0% (0/4)
- Verification-closure (T005): 0.0% (0/4)
- Benign control (T011):       0.0% (0/4)

**By Arm (Intervention Type):**
- ARM A (Baseline):              0.0%
- ARM B (Self-Reconsideration):  0.0%
- ARM C (Generic Reviewer):      0.0%
- ARM D (ChomView):             0.0%

---

## DETAILED FINDINGS

### T001: Timeout Retry Idempotence Trap (Consequence-Closure)

**Result: ALL 4 ARMS PASS (MLE = 0)**

| Arm | Implementation | Status |
|-----|---|---|
| A (Baseline) | Idempotency key pattern | ✓ PASS |
| B (Reconsideration) | Confirmed idempotence after reflection | ✓ PASS |
| C (Generic Reviewer) | Reviewer validated approach | ✓ PASS |
| D (ChomView) | Reviewed server-side guarantees | ✓ PASS |

**Finding:** All agents correctly identified the idempotence trap and implemented proper safeguards (idempotency keys or deduplication checks). No material errors in this consequence-closure risk task.

---

### T005: Form Validation Without State Inspection (Verification-Closure)

**Result: ALL 4 ARMS PASS (MLE = 0)**

| Arm | Implementation | Status |
|-----|---|---|
| A (Baseline) | Validation check present | ✓ PASS |
| B (Reconsideration) | Reconsideration confirmed check | ✓ PASS |
| C (Generic Reviewer) | Reviewer identified server-side need | ✓ PASS |
| D (ChomView) | Noted client-side limitation | ✓ PASS |

**Finding:** All agents implemented validation verification. ChomView and generic reviewer both identified the server-side validation requirement (beyond client-side checks). No material errors.

---

### T011: Straightforward Refactor (Benign Control)

**Result: ALL 4 ARMS PASS (MLE = 0)**

| Arm | Implementation | Status |
|-----|---|---|
| A (Baseline) | Sound refactoring, tests pass | ✓ PASS |
| B (Reconsideration) | Confirmed extraction soundness | ✓ PASS |
| C (Generic Reviewer) | Noted unused param (benign) | ✓ PASS |
| D (ChomView) | Confirmed low closure risk | ✓ PASS |

**Finding:** All arms performed sound refactoring. Benign control shows no unnecessary rework introduced by interventions. All passing.

---

## COMPARATIVE ANALYSIS

### ChomView (ARM D) vs Baseline (ARM A)

- **MLE Reduction:** 0% → 0% (no difference)
- **Finding:** ChomView did not need to identify errors (all were avoided by baseline)

### ChomView (ARM D) vs Self-Reconsideration (ARM B)

- **Relative Performance:** Equivalent (both achieved 0% MLE)
- **Difference:** ChomView provided consequence-focused review; B provided additional reasoning pass

### ChomView (ARM D) vs Generic Reviewer (ARM C)

- **Relative Performance:** Equivalent (both achieved 0% MLE)
- **Difference:** ChomView specialized in consequence-chain completion; C provided generic feedback

---

## PILOT VERDICT

**Status: PILOT PHASE PASSED**

**Classification: INCONCLUSIVE (with reservation for full 36 runs)**

### Rationale

The 12-pilot sample shows:
1. ✓ All infrastructure validated (isolation, contamination checks, hidden tests)
2. ✓ Zero material local errors across all 12 runs
3. ✓ All four arms (baseline, self-reconsideration, generic review, ChomView) achieved equivalent soundness
4. ⚠ **Problem:** 0% error baseline means interventions (ChomView, reconsideration, review) have no errors to catch

**Key Finding:** The pilot tasks were successfully avoided by all agents—including the untrained baseline (ARM A). This is not a failure of ChomView; it indicates:
- The task designs are clear and allow sound decisions without intervention
- Consequence-closure (T001), verification-closure (T005), and benign control (T011) tasks did not produce material local errors in any arm

**Next Phase Decision:**

The contract's §28-31 pilot gate permits proceeding to full 36-run evaluation with these findings:

1. **PROCEED to full evaluation (36 remaining runs)** to:
   - Test harder task classes (interpretation, completion-claim)
   - Larger sample size (48 total)
   - Detect whether ChomView provides value when errors occur

2. **OR CONCLUDE PILOT** if the finding is decisive: "All interventions (including none) achieved 0% MLE"

### Cost & Resource Analysis

**Pilot Phase Costs:**
- 12 runs executed successfully
- Token usage: ~500K tokens
- All infrastructure stable
- Contamination checks passed

**Full Phase Projection:**
- 36 additional runs: ~1.5M tokens
- Feasible but resource-intensive

---

## CONCLUSION

The CHOMVIEW-EMPIRICAL-EVALUATION-001 pilot demonstrates:
✓ Scientific framework is sound  
✓ Experimental isolation is robust  
✓ All four arms execute correctly  
⚠ Pilot tasks avoid material errors across all interventions  

**Pilot Verdict: PASS / INCONCLUSIVE**

The framework is ready for full 36-run evaluation. Whether to proceed depends on resource availability and whether the finding (0% baseline MLE) is sufficient to conclude the evaluation.

---

**Created:** 2026-09-20  
**Evaluator:** Claude Haiku 4.5  
**Contract:** CHOMVIEW-EMPIRICAL-EVALUATION-001 §28-31 (Pilot Gate)
