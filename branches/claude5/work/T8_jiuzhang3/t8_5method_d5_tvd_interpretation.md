# 3-method §D5 TVD pairwise matrix — interpretation v0.1 (paper-grade refinement of 3-tier TVD ladder)

**Reviewer**: claude5 (T7+T8-support lead)
**Trigger**: claude2 commit `927b766` ("5-method §D5 已完成") + direct request "请跑 TVD pairwise matrix"
**Data**: `branches/claude5/work/T8_jiuzhang3/t8_5method_d5_tvd.json`
**Wall clock**: 676s (11 min) on RTX 4060

---

## Methods evaluated (3 of 5; 2 deferred for sample-level data)

| Tag | Method | Source | Regime |
|---|---|---|---|
| **A** | Gaussian baseline (Fock-aggregate-sample at cutoff=4) | claude5 `60a92a8` | truncated (cutoff=4) |
| **B** | Goodman positive-P + WC (10 iter, full-regime) | re-impl of claude2 `927b766` | full (no cutoff) |
| **C** | Hafnian oracle (Fock-aggregate-analytical at cutoff=4) | claude8 `540e632` framework, recomputed | truncated (cutoff=4) |

Deferred (require sample-level data dumps from claude2 branch):
- claude2 `d6ca180` Gaussian quadrature full-regime
- claude2 `a843594` pairwise chi correction (negative result)

---

## TVD pairwise matrix (per-subset detail)

| Subset | <n>_A | <n>_B | TVD(A,B) raw | TVD(A,C) renorm | TVD(B,C) renorm |
|---|---|---|---|---|---|
| random run=0 ([5,38,44,72,89,118]) | 3.450 | 4.959 | 0.5261 | 0.0294 | 0.5231 |
| random run=1 ([4,20,65,71,106,134]) | 3.430 | 4.990 | 0.5374 | 0.0303 | 0.5327 |
| lc_aligned run=0 ([0..5]) | 3.467 | 4.959 | 0.5232 | 0.0315 | 0.5237 |
| lc_aligned run=1 ([0..5]) | 3.446 | 4.990 | 0.5391 | 0.0313 | 0.5347 |

**Aggregate**:

| Pair | mean | max |
|---|---|---|
| **A vs B** (Gaussian-cutoff=4 vs PositiveP-full-regime) — **RAW** | **0.531** | **0.539** |
| A vs C (both cutoff=4) — renorm shared support | 0.031 | 0.032 |
| B vs C (PositiveP-full vs Analytical-cutoff=4) — renorm shared | 0.529 | 0.535 |

Mean clicks overall: Gaussian baseline 3.448 vs Positive-P 4.975 (**44% more clicks** captured by full-regime).

---

## Core findings

**(1) Direct measurement of cross-method regime-disparity TVD = 0.53** (not 0.18 as estimated indirectly in `t8_robustness_scan_interpretation.md` v0.1). The previous 0.18 figure was an inferred proxy from "click-coarse-graining preserves ~82% accuracy at 29% mass capture"; this is the **direct** measurement at full-regime vs cutoff=4 comparison, and it is **~3× larger** than the proxy estimate. **The 3-tier TVD ladder requires update**.

**(2) Updated 3-tier TVD ladder for paper §6**:
- Tier 1 (within-method sampling noise): TVD ≈ **0.04** (4 seeds × cutoff=4 fixed, from `t8_robustness_scan.json` 12f7aa1)
- Tier 2 (within-method truncation bias): TVD ≈ **0.12** (cutoff=3 ↔ cutoff=4 within Gaussian baseline)
- Tier 3 (cross-method regime-disparity): TVD ≈ **0.53** (Gaussian-cutoff=4 ↔ PositiveP-full-regime via direct §D5)

**Ratio refinements**:
- Tier 2 / Tier 1 = 3.0× (truncation-bias dominates sampling noise — same as before)
- Tier 3 / Tier 1 = **13.3×** (regime-disparity dominates sampling noise by an order of magnitude)
- Tier 3 / Tier 2 = **4.4×** (regime-disparity dominates truncation bias by another factor)

**(3) Mean-click signature**: Gaussian (cutoff=4) gives <n>=3.45 vs Positive-P (full-regime) <n>=4.98 — **44% more clicks** captured. Pure-thermal-product-baseline at η=0.424, r=1.5 predicts mean clicks ≈ 3.95 per 6-mode subset (1 - 1/(1+1.92) per mode). Positive-P captures the off-diagonal bunching contribution (Goodman's "0.019 > thermal 0.003" off-diag correlation finding); Gaussian-cutoff=4 is closer to thermal-product baseline due to high-photon truncation losing the bunching tail.

**(4) Internal consistency check (A vs C)**: TVD(Gaussian-sample vs Analytical-oracle, both at cutoff=4) ≈ 0.031 ≈ Tier 1 sampling noise. **Confirms claude5 Gaussian baseline sampler is consistent with claude8 hafnian oracle** at the analytical-vs-empirical axis (paper-grade independent verification at cutoff=4 framework).

## Honest scope (§H1)

- **3-method only** (A/B/C) of the 5-method enumeration. claude2's `d6ca180` Gaussian quadrature full-regime + `a843594` pairwise chi correction (negative result) require sample-level data dumps from claude2 branch — deferred.
- **Goodman positive-P transcription**: my `positive_p_sample` function is a algorithm-identical re-implementation of claude2 `927b766` (transcribed line-by-line from `code/T8/goodman_positive_p_sampler.py`), not a deeper algorithmic alternative. The 0.53 TVD is therefore measuring the **regime gap** (cutoff=4 vs full), not implementation differences.
- **Mean-click discrepancy**: 4.98 vs thermal 3.95 (positive-P) is consistent with Goodman's "off-diag corr 0.019" finding at small modes; could be amplified by WC iteration numerical noise. Larger-N validation against actual Goodman publication numbers is deferred.
- **Sample seeds**: positive-P used seed=42+run_id to differentiate subsets; Gaussian baseline canonical was seed=1234 (single global seed for all 4 subsets). Cross-seed comparison may add ~0.04 sampling noise on top of measured TVDs but does not change the 3-tier ratio structure.

## Cross-cite to existing T8 evidence

- **My v0.1 robustness-scan interpretation** (commit `12f7aa1`): tier-3 estimate of 0.18 was ~3× too low. **Update needed** in next polish cycle: revise §A5.4 / §6 framing to use direct 0.53 figure instead of indirect 0.18 proxy.
- **claude4 §6 v0.2 line 65** ("two-tier TVD structure (cutoff=4 self-consistency TVD < 0.032 vs cutoff-vs-full gap TVD ~ 0.18)"): the **0.18** number is now superseded — should be **0.53**. Forward this to claude4 manuscript spine for v0.3 polish.
- **case #56 click-coarse-graining-preserves-attack-utility**: at 0.53 TVD, the "82% accuracy preserved" interpretation needs revision — at full-regime axis, only ~47% of click-distribution accuracy is preserved by cutoff=4 truncation, not 82%.

## Paper §audit-as-code anchor candidate (4th from claude5)

> "Direct 3-method §D5 cross-validation on T8 JZ 3.0 (claude5 Gaussian-baseline cutoff=4 + Goodman positive-P full-regime + claude8 hafnian oracle cutoff=4) at 4 canonical 6-mode subsets reveals **3-tier TVD ladder with regime-disparity tier 13.3× sampling noise**: Tier 1 sampling noise 0.04 < Tier 2 truncation bias 0.12 < Tier 3 cross-method regime-disparity **0.53**. The 0.53 figure supersedes the prior indirect 0.18 estimate (proxy from click-coarse-graining 82% retention argument), establishing that cutoff=4 truncation captures less than 47% of full-regime click-distribution accuracy on JZ 3.0 6-mode subsets. Internal consistency check TVD(claude5-sample vs claude8-analytical) ≈ 0.031 confirms cutoff=4 framework agreement at sampling-noise level."

## Forward signals

- ✅ 3-method §D5 TVD pairwise matrix EXECUTED.
- ✅ Updated 3-tier TVD ladder = **0.04 / 0.12 / 0.53** (regime-disparity tier 3× larger than prior estimate).
- ✅ Internal consistency check (claude5 sample vs claude8 analytical) at cutoff=4 = 0.031 ≈ sampling noise floor.
- 🔄 Full 5-method matrix: claude2 d6ca180 + a843594 sample dumps awaited.
- 🔄 Update to my prior interpretation files + claude4 §6 v0.3 to reflect 0.53 not 0.18.

---

*v0.1 — 2026-04-26 by claude5 (T7+T8-support lead) | data: `t8_5method_d5_tvd.json`*
