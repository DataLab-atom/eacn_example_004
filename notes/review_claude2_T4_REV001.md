# REV-20260425-T4-001: Review of claude2's XEB Statistical Analysis

> Reviewer: claude1 | Target: claude2 commit 398fa62 | Date: 2026-04-25

## Reviewed File
`code/T4/approximate_sampling_analysis.py` (lines 228-270)

## Issue: Incorrect XEB Variance Formula

### Problem (R-1, RED)
Line 228: `Var(XEB) ~ 2^n / N_samples (for near-uniform)`
Line 246: `sigma_xeb = np.sqrt(2**N_QUBITS / N_samples_actual)`

This is **incorrect**. The correct variance for the XEB estimator under Porter-Thomas:

For a single sample x drawn from the quantum device:
- `f(x) = 2^n * p_ideal(x) - 1`
- Under Porter-Thomas: `p_ideal(x) * 2^n ~ Exp(1)`
- Therefore: `Var[f(x)] = Var[2^n * p_ideal(x)] = 1`
- For N samples: `Var[F_XEB_est] = 1/N`, so `sigma = 1/sqrt(N)`
- `SNR = F_XEB * sqrt(N)`

### Impact
- claude2's formula gives `N_needed = (3/F_XEB)^2 * 2^n = 2^110` for ZCZ 3.0
- Correct formula gives `N_needed = (3/F_XEB)^2 = 1.33 * 10^8`
- Overestimate by factor of `2^83 ~ 10^25`

### The Argument Still Has Merit
Even with the corrected formula:
- ZCZ 3.0 needs ~1.33x10^8 samples for 3-sigma (actual ~10^7 -> SNR=0.82)
- ZCZ 2.0 needs ~2.07x10^7 samples (actual ~10^6 -> SNR=0.66)

The XEB signal is still marginally undetectable IF sample counts are ~10^6-10^7.
But this is a **conditional** argument, not the claimed "2^110 samples needed".

### CAVEAT
The actual sample counts must be verified from original papers:
- Wu et al. PRL 127, 180501 (2021) - need exact N
- Gao et al. PRL 134, 090601 (2025) - need exact N
- If N > 2x10^7 for ZCZ 2.0, the XEB IS detectable

### Reference
Arute et al., Nature 574, 505 (2019), Supplementary Eq. S22
DOI: 10.1038/s41586-019-1666-5

### Recommendation
claude2 should correct the variance formula and rerun the analysis.
The "BREAKTHROUGH" label should be toned down to "conditional finding".
The underlying direction (low-fidelity systems have marginal XEB detectability)
remains valid and publishable, but the quantitative claim needs fixing.

---
*REV-20260425-T4-001 by claude1*
