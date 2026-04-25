# RETRACTION: T6 XEB Statistical Detectability — both v1 and v2 sample counts wrong

> Agent: claude1 | Branch: claude1 | Date: 2026-04-25 | Status: **FULLY RETRACTED**
> Trigger: User pressure to actually read primary source (arXiv MCP had been "downloading" for 1+ hour with no progress)
> Source verified: Wu et al. PRL 127, 180501 (2021) main text, accessed via direct WebFetch + local PDF read

## Summary

The XEB statistical detectability attack line for T6 — claimed in commits `2f36410` (v1) and `79a7d12` (v2 post-claude7 review) and supported in commit `ac07679` v3.1 attack summary — used **incorrect sample counts** in both versions. After reading the Wu 2021 PRL primary source directly, the actual numbers invalidate the entire attack line.

## What was wrong (v1 + v2)

| Version | N_actual used | Source | Status |
|---------|---------------|--------|--------|
| v1 (commit 2f36410) | 10⁶ per instance (estimated) | my own estimate | wrong |
| v2 (commit 79a7d12) | 5×10⁶ per instance (paper-actual claimed) | claude7 REV-T6-004 | also wrong |
| **Wu 2021 primary source** | **~1.9×10⁷ per instance × 10 instances = 1.9×10⁸ total** | direct PDF read | correct |

## Recomputed SNR with primary-source N

For Porter-Thomas distributed ideal probabilities (Var[2ⁿp − 1] = 1 per sample):
- SNR per single instance: F_XEB × √(1.9×10⁷) = 6.62×10⁻⁴ × 4359 = **2.89**
- SNR for 10-instance combined dataset: F_XEB × √(1.9×10⁸) = 6.62×10⁻⁴ × 13784 = **9.12**

The Wu paper itself reports "F=0 null hypothesis rejected with significance of 9σ" (page 4). My recomputed 9.12σ matches their 9σ exactly.

**The XEB statistical claim that ZCZ 2.0 is marginal NOT detectable is false.** ZCZ 2.0 XEB signal is detected at 9σ with the actual sample count.

## Comparison vs my v2 claim

| System | F_XEB | N_actual (correct) | SNR (correct) | My v2 claim | Reality |
|--------|-------|---------------------|----------------|--------------|---------|
| ZCZ 2.0 (56q × 20c) | 6.62×10⁻⁴ | 1.9×10⁸ (10 inst × 1.9×10⁷) | **9.12** ✓ | "marginal NOT detectable, SNR=1.48" | DETECTABLE at 9σ |

The error is the per-instance N (1.9×10⁷ vs my v2's 5×10⁶), and forgetting the K=10 multi-instance combined SNR.

## Cause of error

1. **Did not read the primary source.** Both v1 (my own estimate) and v2 (claude7's review numbers) used inferred or quoted sample counts without direct paper verification. Local arXiv MCP was stuck "downloading" for 1+ hour. I should have used WebFetch / WebSearch / direct PDF download immediately rather than waiting.
2. **Did not implement K=10 instance combination.** Wu reports inverse-variance weighting over 10 instances. My SNR formula treated single-instance samples as if they were the whole experiment.
3. **Did not cross-check against the paper's own 9σ statement.** The paper explicitly states "9σ rejection of F=0" — if my analysis predicted SNR=1.48, that contradicts the paper's reported significance and should have been a flag.

## Retraction scope

The following commits/claims are **FULLY RETRACTED** in their XEB-statistical-detectability content:

- commit `2f36410` (v1) — initially claimed marginal SNR for ZCZ 2.0/2.1
- commit `79a7d12` (v2) — claimed SNR=1.48 with N=5×10⁶ per claude7 review
- commit `ac07679` `T6_attack_summary_v3_1.md` — Line B "XEB statistical detectability" section
- commit `448b3b9` v3.1 amortized framing — does not directly cite XEB statistical numbers but mentions Line B; flagged
- commit `42ccb8d` REV-CROSS-T1-001 review of claude8 — did NOT cite the wrong T6 XEB numbers, not affected

Cross-link: claude7 REV-T6-004 v0.2 PASSES verdict (commit `ae94f56`) was reached on the wrong shared sample counts. claude7 should be notified to amend / withdraw that PASSES verdict; the underlying methodology of their review (Porter-Thomas variance, etc.) was correct, only the sample-count input was wrong.

## What remains valid

- **Line A (TN contraction extrapolation)**: untouched. d=16 36q anchor (4236.7s) + 43-day single-CPU + reproducibility caveat (commit fd9e98d) all stand independently. Wu paper's own TN cost estimate (1.10×10²² FLOPS for matching Sycamore's 0.224% fidelity) is consistent with my v3.1 framing.
- **Line C (Morvan)**: already retracted closed-loop (commit 7d53734).
- **Reproducibility caveat methodology**: untouched.
- **Cross-attack peer review channel** (REV-CROSS-T1-001 verdict on claude8): untouched, did not depend on T6 XEB numbers.

## What changes for the T6 paper claim

The two-line attack (TN constructive + XEB statistical) collapses to a one-line attack (TN constructive). The paper § 3 RCS draft must:
1. Drop XEB statistical detectability as an independent attack line.
2. Keep TN extrapolation + reproducibility caveat as the primary T6 evidence.
3. Acknowledge that Wu's 9σ XEB significance is correctly established at the paper-actual sample count. Their statistics are valid; the only question is whether the classical cost is as high as they claim.
4. The ZCZ 3.0 retraction (claude2 cac3bb5) and ZCZ 2.0 retraction (this document) are now symmetric — both XEB-statistical attacks fail when actual sample counts are used.

## Lessons (for project memory + audit playbook)

1. **arXiv MCP "downloading" status > 30 min: switch to WebFetch / WebSearch / direct PDF download immediately.** Do not wait. The user pointed this out explicitly today; I should have switched 1 hour ago.
2. **When the paper itself reports a statistical significance (e.g., "9σ"), my reanalysis must reproduce that number, or my reanalysis is wrong.** The 9σ vs 1.48 inconsistency was a flag I missed for hours.
3. **K-instance combination is standard in RCS literature.** Do not analyze a single instance's SNR as if it were the whole experiment.
4. **The claude7 review used wrong N too.** Reviewer agreement does not validate input data — both reviewer and author should independently verify primary-source numbers, not delegate to each other. Cross-attack peer review is most valuable when both sides independently fetch the source.

This is the second major T6 retraction this day (Morvan + XEB statistical). Both retractions stem from the same root cause: deriving claims from inferred / cited / second-hand parameters without primary-source verification. The lesson is identical and now redundantly burned-in.

## Audit case implications

- audit_index case #15 enforcement family: this is **A2 (author self-catch)** triggered by user pressure to switch tools. New sub-pattern candidate: **A2-bench** = "author self-catch when external observer flags inefficient tool usage (waiting on stuck MCP for >30 min)".
- case #6 in the §7 case library was "single-day double-erratum learning" (Morvan + XEB v0.1→v2). With this, it becomes "single-day **triple**-erratum learning" or "Morvan + XEB-v0→v2 + XEB-v2→retract." The v2 PASSES verdict was based on wrong N, so the "triple-erratum" framing is honest.

## References

- Wu et al. PRL 127, 180501 (2021), arXiv:2106.14734v1 — primary source, page 4 ("about 19 million bitstrings", "ten randomly generated circuit instances", "9σ")
- Reviewer chain: claude7 REV-T6-004 v0.2 PASSES (commit ae94f56) — also relied on wrong N=5×10⁶, will be notified to amend
- claude2 cac3bb5 — ZCZ 3.0 corresponding retraction (parallel pattern, different parameters)

---
*Drafted by claude1, 2026-04-25. Direct PDF source verification triggered by user pressure to switch from stuck arXiv MCP. Paper §3 RCS draft must drop Line B XEB-statistical attack; Line A TN extrapolation remains the only viable T6 attack line.*
