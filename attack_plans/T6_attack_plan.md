# T6 Attack Plan: USTC Zuchongzhi 2.0 / 2.1

**Attacker**: claude2
**Branch**: claude2
**Status**: In progress
**Last updated**: 2026-04-25

---

## Target Summary

| Field | Value |
|---|---|
| **Paper** | Wu et al., PRL 127, 180501 (2021) [ZCZ 2.0]; Zhu et al., Sci. Bull. 67, 240 (2022) [ZCZ 2.1] |
| **Hardware** | 60 qubits superconducting, 24 cycles |
| **Claim** | 6 orders harder than Sycamore; classical needs 4.8x10^4 years |
| **XEB fidelity** | ~0.066% (extremely low) |
| **Gate errors** | 1Q: ~0.1%, 2Q: ~0.5%, readout: ~4% |
| **Current status** | Challenged (Morvan et al. 2024 indirectly) |

## Attack Strategy

### Primary Attack: Pauli Path / Noise Threshold Analysis

**Rationale**: Schuster, Yin, Gao & Yao (PRX 15, 041018, 2025) proved a polynomial-time classical algorithm for noisy RCS with uniform depolarizing noise. ZCZ 2.1's extremely low XEB fidelity (~0.066%) suggests it operates deep in the "strong noise" regime where high-weight Pauli paths are exponentially suppressed.

**Key calculation needed**:
1. Determine the per-cycle effective noise rate for ZCZ 2.1's 60-qubit 2D grid
2. Compare against the Morvan phase transition critical threshold
3. If noise exceeds threshold: ZCZ output is a product of uncorrelated subsystems -> efficiently classically simulable
4. Implement Pauli path truncation and show poly-time convergence at ZCZ parameters

### Secondary Attack: Updated Tensor Network Estimation

**Rationale**: Pan-Zhang (PRL 129, 2022) broke Sycamore (53q/20c). ZCZ 2.1 (60q/24c) is ~2000x harder, but hardware has improved. Re-estimate classical runtime with current GPU capabilities and optimized contraction ordering.

**Steps**:
1. Model the ZCZ 2.1 circuit as a tensor network on 2D grid
2. Find optimal contraction ordering via cotengra
3. Estimate wallclock time on modern GPU clusters (A100/H100)
4. Compare against the original 4.8x10^4 year claim

### Tertiary: Morvan Phase Transition Framework

Apply Morvan et al. (Nature 634, 2024) phase transition analysis to ZCZ 2.1:
- Compute the anti-concentration depth for 60-qubit 2D grid
- Determine whether ZCZ's noise rate places it in the "correlated" or "product" phase
- If in product phase: explicit classical spoofing algorithm

## Deliverables

1. `code/T6/pauli_path_analysis.py` - Pauli path noise threshold calculation
2. `code/T6/tn_contraction_estimate.py` - TN contraction cost estimation
3. `code/T6/phase_transition_analysis.py` - Morvan framework applied to ZCZ
4. `results/T6/` - All numerical results with plots
5. Literature canon entries for all cited papers

## Key References

- Pan & Zhang, PRL 129, 090502 (2022) - Broke Sycamore
- Liu et al., PRL 132, 030601 (2024) - Multi-amplitude TN
- Schuster, Yin, Gao, Yao, PRX 15, 041018 (2025) - Poly-time noisy RCS
- Morvan et al., Nature 634, 328 (2024) - RCS phase transitions
- Gonzalez-Garcia, Cirac, Trivedi, Quantum (2025) - Pauli path beyond average case
- Zhao et al., NSR (2025) - Leapfrogging Sycamore with 1432 GPUs
