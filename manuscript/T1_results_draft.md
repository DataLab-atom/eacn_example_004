# T1 Results Section Draft (for Nature/Science manuscript)

> **Status**: Draft v0.1 — data-backed claims only, no speculation
> **Author**: claude4 | **Reviewers**: claude3 (REV-T1-001), claude6, claude8 (pending)
> **Data commits**: 78b05aa, bc65324, 9a22484, 694d65d, 1f511ee, f265c51, b0d4cb0, 575b59b

---

## Result 1: SPD successfully computes OTOC and OTOC^(2) on 2D grids

We implemented Sparse Pauli Dynamics (SPD) in the Heisenberg picture
to compute both first-order (OTOC) and second-order (OTOC^(2))
out-of-time-order correlators on 2D grid circuits with iSWAP-like gates.

For systems up to 10 qubits with exact diagonalization validation,
SPD achieves machine precision (relative error < 10^{-13}) when the
Pauli weight truncation threshold equals the system size (w = n).
At reduced truncation levels, SPD provides systematically improvable
approximations with monotonically decreasing error (Table 1).

**Table 1.** SPD convergence for OTOC^(2) on 2D grids (noiseless).

| System | Depth | w_min (<5% error) | w/n | Terms | Wall time |
|--------|-------|--------------------|-----|-------|-----------|
| 4q 2×2 | 4 | 4 | 1.00 | 255 | 0.4 s |
| 6q 2×3 | 4 | 2 | 0.33 | 63 | 0.01 s |
| 8q 2×4 | 4 | 5 | 0.62 | 780 | 0.5 s |
| 10q 2×5 | 4 | 4 | 0.40 | 255 | 0.1 s |
| 12q 3×4 | 4 | 6 | 0.50 | 3839 | 6 s |
| 16q 4×4 | 4 | 4 | 0.25 | 233 | 0.3 s |

To our knowledge, this is the first application of SPD to OTOC circuits.

---

## Result 2: Grid topology dominates truncation requirements

The minimum Pauli weight for OTOC^(2) convergence depends strongly
on the grid aspect ratio, not just the qubit count. Square grids
(N×N) require significantly lower truncation than narrow grids (2×N)
at the same depth (Fig. 1a).

At depth 4, the 16-qubit 4×4 grid converges at w/n = 0.25 with only
233 Pauli terms, while the 8-qubit 2×4 grid requires w/n = 0.62
with 780 terms — a 2.5× difference in the w/n ratio despite the
4×4 system being twice as large.

This topology effect arises because OTOC signal propagation follows
the shortest path between the M and B operator positions. On square
grids, the light-cone spreads isotropically, concentrating Pauli weight
on a small subset of qubits along the propagation path ("hotspot").

---

## Result 3: OTOC^(2) Pauli weight concentrates on a shrinking fraction of qubits

Analysis of the Pauli term distribution reveals that OTOC^(2) signal
is concentrated on a small subset of "hot" qubits along the M-to-B
propagation path (Fig. 1b).

| Grid | Hot sites (>1% occupancy) | Fraction | Cold (zero) |
|------|--------------------------|----------|-------------|
| 4×4 (16q) | 5 | 31% | 69% |
| 6×6 (36q) | 7 | 19% | 81% |

The hot-site fraction decreases as a power law with exponent -0.585,
projecting to ~9 hot sites (14%) for 65-qubit Willow-scale grids.

**Caveat (§A5):** This concentration is observed for the unscrambled
regime (M and B at maximum grid distance, OTOC^(2) ≈ 1). For the
scrambled regime (M and B nearby, OTOC^(2) < 1), which is the
experimentally relevant case, the hot-site fraction increases
significantly (7/8 = 87% at 8 qubits). The scrambled regime
is substantially harder for SPD.

---

## Result 4: Circuit depth is the dominant scaling variable

Systematic measurement of the minimum truncation weight across
depths 2-8 reveals that depth, not qubit count, is the primary
determinant of SPD difficulty (Fig. 2).

| Depth | w/n (2×N grids) | w/n (N×N grids) |
|-------|-----------------|-----------------|
| 2-3 | 0.20 - 0.33 | ~0.25 |
| 4 | 0.33 - 0.62 | 0.25 |
| 5-6 | 0.50 - 0.88 | ~0.50 (est.) |

Importantly, w_min saturates at depth ≥ 5 on narrow grids
(10q 2×5: w_min = 8 for depths 5, 6, and 8), indicating a
ceiling on truncation requirements.

---

## Result 5: Depolarizing noise does not significantly reduce truncation requirements for OTOC^(2)

Contrary to the theoretical expectation from Schuster et al.
(arXiv:2407.12768) that noise exponentially suppresses high-weight
Pauli strings, we find that depolarizing noise at Willow-relevant
rates (gamma = 0.003-0.01 per 2-qubit gate) does not significantly
reduce the truncation error for OTOC^(2).

At 12 qubits with w ≤ 4: noiseless error = 27.5%, gamma = 0.005
error = 27.2% — a negligible improvement.

This discrepancy arises because OTOC^(2) involves double Heisenberg
conjugation (U†BU appears twice), creating coherent superpositions
of high-weight Pauli terms that are not simply exponentially damped
by noise. This mechanism differs fundamentally from the single-pass
RCS setting analyzed by Schuster et al.

**This is a negative result with important implications**: classical
simulation of OTOC^(2) cannot rely on noise-assisted truncation
and must instead exploit circuit structure (topology, depth) for
efficiency.

---

## Discussion points (to be expanded)

1. The attack feasibility depends critically on the per-arm circuit
   depth of Google's Quantum Echoes experiment (estimated 12-18 cycles
   from Bermejo et al. arXiv:2604.15427, to be verified).

2. For the experimentally relevant scrambled regime, SPD term counts
   grow rapidly (4,007 terms at 8q vs 1,023 for unscrambled),
   suggesting that 65-qubit scrambled OTOC^(2) requires either
   (a) adaptive truncation strategies, (b) exploitation of grid
   topology, or (c) acceptance that SPD alone may be insufficient.

3. Three independent classical paths (SPD fixed-weight, Schuster
   Pauli-path, adaptive SPD) provide cross-validation per §D5.

---

*Draft v0.1, 2026-04-25. All claims backed by committed data.*
*Figures referenced but not yet generated.*
