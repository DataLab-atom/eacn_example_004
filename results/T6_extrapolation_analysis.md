# T6 Extrapolation Analysis: Zuchongzhi 2.0/2.1 Classical Runtime

> Agent: claude1 | Branch: claude1 | Date: 2026-04-25
> **v2**: Corrected after claude7 review REV-20260425-T6-001
> **v3**: Added 36q wall-clock anchor (commit 9cb1a5c)

## 0. v3 update — wall-clock anchor at 36 qubits

After v2, cotengra `hyper+slicing` produced a real wall-clock data point:
**n=36, d=16: 4236.7 seconds** (≈70 min, peak 33.6 MB, 8192 slices).

| Depth | Fit | b | T(56q) | Status |
|-------|-----|---|--------|--------|
| **d=16** | T = 1.504e-3 × exp(0.386 × n) | 0.386 | **~43 days single CPU** | anchored at 36q |
| d=20 | T = 3.100e-2 × exp(0.127 × n) | 0.127 | unstable | no high-n anchor |

The d=16 b coefficient (0.386) is now believable because it's anchored on a real 36q point. The d=20 fit still lacks high-n data (the 20q data point was an outlier per claude7 R-3) and its 39-second extrapolation is meaningless.

**Honest plain reading for ZCZ 2.0 (56q × 20c)**:
- Single CPU lower bound: ~43 days at d=16 (cycles below ZCZ 2.0).
- Single CPU upper bound: TBD pending d=20 runs at 30-40q.
- vs original 48,000-year claim (Frontier): single CPU at d=16 is already ~10⁵× lower. Hardware mismatch noted (R-6).

Removed all references to retracted Morvan analysis (commit 7d53734).

## 0. Errata (v2 corrections)

- **R-1 FIX**: ZCZ 2.0 = **56 qubits x 20 cycles** (was incorrectly 60q x 24c)
- **R-1 FIX**: ZCZ 2.1 = **60 qubits x 24 cycles** (was incorrectly 66q x 24c)
- **R-2 FIX**: Using reported linear-XEB values from original papers instead of estimated F_total
- **R-5 FIX**: Removed premature 🟡→🔴 reclassification claim
- **R-6 FIX**: Speedup comparison notes hardware mismatch explicitly

## 1. Scaling Study Results (6-20 qubits, greedy contraction)

Exponential fit T = a * exp(b*n) from quimb tensor network contraction:

| Depth | a | b | T(56q) | T(56q) in years | Notes |
|-------|---|---|--------|-----------------|-------|
| 8 | 1.21e+02 | -0.99 | ~0 | ~0 | trivial |
| 12 | 1.59e-02 | 0.14 | 40 s | ~0 | trivial |
| 16 | 2.81e-04 | 0.43 | 4.9e6 s | 0.16 yr | feasible |
| **20** | **3.41e-10** | **1.28** | **outlier** | **unstable** | **b non-monotonic, see R-3** |
| 24 | 1.05e-04 | 0.54 | 1.6e9 s | ~51 yr | for 60q ZCZ 2.1 |

**CAVEAT (R-3)**: The b coefficient is non-monotonic across depths (especially d=20 outlier at b=1.28). The 6-20 qubit range provides insufficient data for reliable extrapolation to 56-60 qubits. More data at 24-36 qubits is needed before any quantitative claim. The numbers above are **order-of-magnitude indicators, not rigorous estimates**.

## 2. Noise / Fidelity Analysis (CORRECTED v2)

Using **reported linear-XEB** values from original papers:

| System | Qubits x Cycles | XEB (reported) | Ratio vs Sycamore | Status |
|--------|-----------------|----------------|-------------------|--------|
| Sycamore | 53q x 20c | 2.2e-3 | 1.00 | **Broken** (Pan-Zhang 2022) |
| **ZCZ 2.0** | **56q x 20c** | **6.6e-4** | **0.30** | 🟡 Challenged |
| **ZCZ 2.1** | **60q x 24c** | **3.66e-4** | **0.17** | 🟡 Challenged |

Key observation: Both ZCZ systems have **lower** XEB fidelity than Sycamore (0.30x and 0.17x respectively). Since Sycamore was broken by classical methods, and lower fidelity generally corresponds to easier classical simulation (per Schuster et al. arXiv:2407.12768), this suggests ZCZ should be at least as classically tractable.

**However** (R-5): This is a directional argument, not a proof. The circuit topology, gate set, and specific error structure differ between Sycamore and ZCZ. A definitive claim requires:
1. Actual wall-clock classical simulation at full scale
2. XEB fidelity matching between classical and quantum outputs
3. Independent verification

## 3. Acceleration Factors (ESTIMATED, not yet validated — R-4)

| Factor | Expected speedup | Reference | Validated? |
|--------|-----------------|-----------|------------|
| Pan-Zhang slicing | significant FLOPS reduction | PRL 129, 090502 (2022) | Validated on Sycamore, not on ZCZ |
| cotengra HyperOptimizer | ~10x vs greedy | cotengra benchmarks | Partially (running) |
| GPU acceleration | hardware-dependent | N/A | Not yet |
| Multi-amplitude batching | problem-dependent | PRL 132, 030601 (2024) | Not yet |

**NOTE (R-4)**: These factors cannot be multiplied without verification. Each factor's applicability to ZCZ 2.0/2.1 specifically must be demonstrated.

**NOTE (R-6)**: Any speedup comparison must specify both the classical hardware (e.g., "single CPU core", "single A100 GPU", "512x H100 cluster") and the quantum hardware baseline. Cross-hardware comparisons (e.g., single CPU vs Frontier) are misleading.

## 4. Evidence Trajectory

The evidence gathered so far **suggests a plausible path toward classical simulation** of ZCZ 2.0/2.1:

1. ZCZ fidelity is 3-6x lower than the already-broken Sycamore
2. ZCZ 2.0 uses similar circuit architecture (2D grid + fSim + RCS)
3. Tensor network methods have improved significantly since 2021
4. The original 48,000-year claim used 2021 algorithms

**This does NOT yet constitute a complete classical counterattack.** The following are required:
- [ ] Full-scale TN contraction at 56q x 20c with optimized path (wall-clock)
- [ ] XEB fidelity verification of classical output
- [ ] Comparison on matched hardware
- [ ] Peer review (claude7 R-2/R-3 items pending)

## 5. References

- Wu et al., PRL 127, 180501 (2021) — Zuchongzhi 2.0: 56q, 20 cycles
- Zhu et al., Sci. Bull. 67, 240 (2022) — Zuchongzhi 2.1: 60q, 24 cycles
- Pan & Zhang, PRL 129, 090502 (2022) — Sycamore classical simulation
- Liu et al., PRL 132, 030601 (2024) — Multi-amplitude contraction
- Morvan et al., Nature 634, 328 (2024) — Phase transition framework (cited only as canon; my analysis on this framework was retracted, see T6_morvan_phase_RETRACTED.md)
- Schuster et al., arXiv:2407.12768 (2024) — Noisy circuit polynomial algorithm (preprint, not accepted)

---
*v1: 2026-04-25 claude1 | v2: 2026-04-25 claude1 (post-review REV-20260425-T6-001 by claude7) | v3: 2026-04-25 claude1 (36q wall-clock anchor + Morvan retraction propagated)*
