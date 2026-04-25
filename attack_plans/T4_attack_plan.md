# T4 Attack Plan: USTC Zuchongzhi 3.0

**Attacker**: claude2
**Branch**: claude2
**Status**: REASSESSING — two major attack lines withdrawn
**Last updated**: 2026-04-25 (v4: post-Morvan withdrawal)

---

## Target Summary

| Field | Value |
|---|---|
| **Paper** | Gao et al., PRL 134, 090601 (2025) |
| **Hardware** | Superconducting 105 qubits (experimental: 83 qubits, 32 cycles) |
| **Claim** | Frontier needs 6.4x10^9 years; 6 orders harder than Google SYC-67/70 |
| **Fidelity** | 1Q: 99.90%, 2Q: 99.62%, readout: 99.13% |
| **Circuit** | 2D grid, 83 active qubits, 32 cycles of random 2-qubit gates |
| **XEB** | Not explicitly stated; estimated from fidelity budget |

## Attack Lines

### Line 1: Pauli Path Noise Threshold (PRIMARY)

Schuster, Yin, Gao, Yao (PRX 15, 041018, 2025) proved polynomial-time classical simulation for noisy RCS when per-gate noise exceeds a critical threshold. 

**Key parameters to compute**:
1. Per-cycle effective depolarizing rate from hardware fidelities
2. Total circuit noise budget: N_2q_gates * (1 - F_2q) + N_1q_gates * (1 - F_1q) + N_readout * (1 - F_ro)
3. XEB fidelity estimate: F_XEB ~ prod(F_gate_i) for all gates
4. Critical noise threshold from Morvan phase transition framework
5. Comparison: is ZCZ 3.0 above or below the threshold?

**Expected result**: With 83 qubits, 32 cycles, and ~2600 two-qubit gates at 99.62% fidelity each, the XEB fidelity is approximately:
F_XEB ~ (0.9962)^2600 * (0.9990)^(83*32) * (0.9913)^83 ~ extremely small

This may place ZCZ 3.0 deep in the noisy, classically simulable regime.

### Line 2: Tensor Network Cost Re-estimation

Using cotengra to find optimal contraction ordering for the 83-qubit 2D grid circuit:
1. Build the tensor network for ZCZ 3.0 circuit topology
2. Optimize contraction path
3. Estimate FLOP count and memory requirements
4. Project wallclock time on modern GPU clusters

### Line 3: Morvan Phase Transition

Apply the two-phase-transition framework:
1. Anti-concentration depth for 83-qubit 2D grid
2. Noise-driven transition: correlated vs product phase
3. Determine which phase ZCZ 3.0 operates in

## Results So Far

### Completed analyses (all on branch claude2):
1. `code/T4/noise_budget_analysis.py` — XEB = 0.026%, lambda = 12.4 (1.5x Sycamore)
2. `code/T4/tn_extrapolation.py` — Brute-force TN ~2^234 FLOPS, infeasible
3. `code/T4/approximate_sampling_analysis.py` — SNR@10^7 = 0.82 < 3 (CORRECTED: was 2^110, now 1.3e8)
4. `code/T4/approximate_tn_benchmark.py` — Small-scale: quantum wins easily at low noise
5. `code/T4/tn_cost_estimation.py` — cotengra calibration data for scaling

### Cross-validated by teammates:
- claude1 Morvan analysis: ZCZ 3.0 lambda/lc = 1.55, deep in classical phase (commit 7886de1)
- claude6/7: XEB variance formula corrected (2^n factor removed)
- claude4 review Y-1/Y-2/Y-3: need paper's actual F_XEB, sample count, numerical validation

### Errata:
- XEB variance: Var = 1/N not 2^n/N (fixed in c6b515b)
- Schuster-Yin DOI: hallucinated, removed from canon (fixed in a5a9686)

## Withdrawn attack lines (errata)
- ~~Statistical undetectability (2^110 samples)~~: XEB variance formula wrong → fixed to 1.3e8 → then N_actual=4.1e8 sufficient (SNR=5.26>3). WITHDRAWN commit cac3bb5.
- ~~Morvan phase transition (lambda/lc=1.55)~~: Parameter definition mismatch. Morvan ε_c=0.47 per-cycle; ZCZ 3.0 ε=0.005 is 100x below threshold → quantum advantage phase. WITHDRAWN commit d37ca22.

## Remaining viable attack lines
- XEB = 0.026%: extremely low fidelity bar, but NOT proven classically matchable
- Sycamore precedent: broken with similar per-gate errors, but at smaller scale
- TN scaling: brute-force infeasible, approximate methods unproven at target scale

## Honest assessment
T4 (ZCZ 3.0) is SIGNIFICANTLY harder than initially assessed.
Recommend: shift primary effort to T8 (JZ 3.0) where Oh et al. provides
a direct, validated attack path. T4 may require supercomputer-scale
TN contraction or novel algorithmic breakthroughs.

## Outstanding TODO
- [ ] Team discussion: reassess T4 viability vs resource allocation
- [ ] Consider T4 as secondary target, T8 as primary
- [ ] Explore Pauli path at ZCZ 3.0 scale (theoretical, not numerical)
- [ ] Check if Pan-Zhang method can be directly scaled to 83q/32c
