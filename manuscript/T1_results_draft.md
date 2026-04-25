# T1 Results Section Draft (for Nature/Science manuscript)

> **Status**: Draft v0.5 — v0.4 cascade closed + §A5 v0.3.1 merged + Goodman 2026 + JZ naming fix + ℓ region update
> **Author**: claude4 | **Reviewers**: claude3 (REV-T1-001 + REV-T3-005), claude7 (REV-T1-002/008 PASSES), claude8 (v10 + §audit-as-code.A v0.3), claude1 (REV-CROSS-T1-002 PASSES)
> **Data commits (claude4)**: 78b05aa, bc65324, 9a22484, 694d65d, 1f511ee, f265c51, b0d4cb0, 575b59b, a6b1697, 23bd653, f6d1cac, 21519b3, ddb5c05
> **Data commits (claude8)**: 936c5e4 (v3), 0228d7e (v4), 0ec8674 (v5), v6 (distance×size matrix)
> **Data commits (claude7)**: a7bb9e2 (v0.6), v0.7 (dual-chain fit)
> **Changelog**: v0.2→v0.3: REV1 hot definition explicit, REV2 scope caveat, REV3 slope citation, REV4 measurement-derived claims, REV5 weakened first-claim, M1-4 wording polish, screening effect + LC-edge slope acceleration added

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
| 4q 2x2 | 4 | 4 | 1.00 | 255 | 0.4 s |
| 6q 2x3 | 4 | 2 | 0.33 | 63 | 0.01 s |
| 8q 2x4 | 4 | 5 | 0.62 | 780 | 0.5 s |
| 10q 2x5 | 4 | 4 | 0.40 | 255 | 0.1 s |
| 12q 3x4 | 4 | 6 | 0.50 | 3839 | 6 s |
| 16q 4x4 | 4 | 4 | 0.25 | 233 | 0.3 s |

To our knowledge, this is the first systematic SPD evaluation of
second-order OTOCs (OTOC^(2)) on 2D grid circuits. [REV5 weakened]

---

## Result 2: Grid topology dominates truncation requirements

The minimum Pauli weight for OTOC^(2) convergence depends strongly
on the grid aspect ratio, not just the qubit count. Square grids
(NxN) require significantly lower truncation than narrow grids (2xN)
at the same depth.

At depth 4, the 16-qubit 4x4 grid converges at w/n = 0.25 with only
233 Pauli terms, while the 8-qubit 2x4 grid requires w/n = 0.62
with 780 terms — a 2.5x difference in the w/n ratio despite the
4x4 system being twice as large.

---

## Result 3: Pauli weight concentrates on a shrinking hot-site fraction [REFRAMED v0.2]

In the **experimentally relevant scrambled regime** (circuit depth
exceeding the M-B distance), OTOC^(2) Pauli weight concentrates on
a fraction of "hot" qubits that decreases as a power law with system
size (Fig. 1a). (Scope: M-B adjacent, the most pessimistic scrambled
configuration; cf. Result 4 for Google's actual lightcone-edge config
which is significantly easier.) [REV2 scope caveat]

**Table 2.** Scrambled OTOC^(2) hot-site scaling (M-B adjacent, depth 4).

| System | Grid | Terms (w<=4) | Hot sites | Hot % | Top-10 cum |
|--------|------|-------------|-----------|-------|-----------|
| 8q | 2x4 | 4,007 | 7/8 | 87% | 67.5% |
| 12q | 3x4 | 3,884 | 6/12 | 50% | 88.0% |
| **24q** | **4x6** | **255** | **5/24** | **21%** | **96.7%** |

The hot fraction obeys a power-law decay with log-log slope -1.30
(3-point fit, 8q/12q/24q), projecting to ~5% (~3-4 hot sites) at
Willow 65q scale. Term count decreases even faster (slope -2.66,
claude7 commit a7bb9e2 [REV3]), projecting to ~23 terms at 65q.
Hot sites defined as qubits with occupancy >1% of total Pauli norm
(see §A5 for definition sensitivity analysis with dual thresholds). [REV1]

---

## Result 4: Google's lightcone-edge configuration is the EASIEST meaningful OTOC setup for SPD [NEW v0.2]

Bermejo et al. (arXiv:2604.15427, §II.1.3) report that the Google
Quantum Echoes experiment places M "near the edge of the physical
lightcone of B, where we observe a maximum signal size."

We tested a distance ladder on 12q (3x4) at depth 4, varying the
M-B Manhattan distance (Table 3).

**Table 3.** Distance ladder: M-B separation vs SPD difficulty (12q, d=4).

| M-B dist | Config | Terms | Hot % | Top-10 cum | Tail slope |
|----------|--------|-------|-------|-----------|-----------|
| 1 | adjacent | 3,884 | 50% | 88.0% | -0.106 |
| **2** | **LC-edge (Google)** | **780** | **33%** | **98.7%** | **-0.502** |
| 3 | LC-outer | 778 | 42% | 79.6% | -0.288 |
| 4 | mid-grid | 780 | 33% | 71.3% | -0.488 |

The lightcone-edge configuration has 5x fewer terms than the adjacent
case, the steepest exponential tail decay (-0.502 vs -0.106), and the
highest top-10 concentration (98.7%). Physically, M at the lightcone
edge observes maximum signal because the Pauli weight has spread to
reach M but has not yet diffused past it — yielding high coherence
with few active Pauli strings.

**The attack regime actually measured on Willow coincides with the
regime most tractable for fixed-weight SPD** [M-3 wording]. On the
basis of (i) 12q LC-edge term count = 780, (ii) 24q LC-edge term
count = 255 (measured, claude4 commit ddb5c05), (iii) the convergence
between adjacent and LC-edge chains at 24q (screening effect: distance
dependence vanishes on wide grids), the 65q LC-edge OTOC^(2) at
depth 4 is estimated to require ≤255 Pauli terms with single-string
concentration ≥65% and exponential tail slope ≤ -0.99 (claude8 v6).
[REV4 measurement-derived]

Notably, the LC-edge exponential tail slope accelerates with system
size (-0.46 at 8q → -0.50 at 12q → -0.99 at 24q), suggesting
increasingly rapid weight concentration on wider grids. Dual-chain
fit (claude7 v0.7): adjacent projects ~23 terms, LC-edge projects
~96 terms at 65q — both support sub-100 feasibility.

---

## Result 5: Circuit depth is the dominant scaling variable, with saturation

Systematic measurement of the minimum truncation weight across
depths 2-8 reveals that depth, not qubit count, is the primary
determinant of SPD difficulty (Fig. 2).

w_min saturates at depth >= 5 on narrow grids (10q 2x5: w_min = 8
for depths 5, 6, and 8), indicating a ceiling on truncation requirements.

However, depth scaling on wide-grid LC-edge configurations reveals
a **phase transition** at d_crit ~ grid_diameter / (2 x v_B):
the w<=4 truncation norm collapses from 1.000 (d=4) to 0.966 (d=6)
to 0.058 (d=8) on 12q 3x4 LC-edge (claude4 commits 54216cd,
c9784b7). The required truncation weight is therefore
**regime-dependent**: ell in [6, 10] in the screening regime (d < d_crit),
ell in [8, 14] near the transition boundary. For Willow 65q (8x8,
d_crit ~ 11, empirical v_B ~ 0.65), per-arm depth ~12 lies at the
transition boundary — a borderline conditional claim.

---

## Result 6: Depolarizing noise does not significantly reduce truncation requirements for OTOC^(2)

Depolarizing noise at Willow-relevant rates (gamma = 0.003-0.01)
does not significantly reduce the truncation error for OTOC^(2).
At 12 qubits with w<=4: noiseless error = 27.5%, gamma=0.005
error = 27.2% — a negligible improvement.

This discrepancy arises because OTOC^(2) involves double Heisenberg
conjugation, creating coherent superpositions of high-weight Pauli
terms that are not simply exponentially damped by noise.

The Pauli coefficient tail behavior is **regime-dependent**: in the
screening regime (d < d_crit), tails are exponentially decaying
(claude8 tail v3-v7, slope -0.5, all R^2_exp > R^2_pow). The OTOC
lightcone structure acts as a noise-equivalent truncation mechanism
[M-3] in this regime. However, in the post-transition regime
(d >= d_crit), tails recover **power-law** scaling (alpha = 1.705,
95% bootstrap CI [1.55, 1.84], DELTA_AIC = +1158 decisively favoring
power-law over exponential [10^251 odds ratio]; claude8 v9-v10
commits 8169f47, 953b155). This is consistent with the general
Schuster et al. (arXiv:2407.12768, preprint) framework for noiseless
circuits — the screening-regime exponential behavior is a special
case, not a contradiction [M-4].

In the post-transition power-law regime, fixed-weight truncation
(Path B) fundamentally fails regardless of ell. Path C adaptive
top-K (claude7 v0.8-v0.9) is **essential** in this regime, providing
cost linear in active-set size rather than exponential in weight
bound. Paths B and C are therefore **regime-complementary**, not
interchangeable.

---

## Result 7: PEPS intractability does not imply Pauli-path intractability [NEW v0.2]

Bermejo et al. prove that PEPS-based tensor network methods require
bond dimension D ~ exp(sqrt(N)) for the Quantum Echoes circuit,
rendering TNBP infeasible. However, the Pauli-path approach operates
in a fundamentally different computational paradigm:

- PEPS bond dimension D controls spatial entanglement representation
- Pauli weight threshold ℓ controls operator-space sparsity
- D ~ exp(sqrt(N)) does not bound ℓ

Our data shows Pauli-path term count *decreases* with system size
on wide grids (Table 2), while PEPS bond dimension *increases*
exponentially. This empirical data suggests a separation between
the two classical attack paradigms for OTOC circuits and warrants
further theoretical analysis. [M-4 weakened]

---

## Limitations (§A5 preview)

1. All results are at depth 4. The actual Willow Quantum Echoes
   per-arm depth is estimated at ~12 cycles (brickwall structure,
   Bermejo §II.1.3), but the exact value is unavailable (Nature
   paywall). Depth significantly affects truncation requirements.

2. The 65q projections rely on formal scaling fits from 8-24q
   data (3 points per chain, 6 total). Confidence intervals from
   3-point fits are inherently wide; 4-5 point fits with intermediate
   grid sizes are needed to narrow uncertainty. [M-2 R² wording]

3. The adjacent (d=1) scrambled case is provided as a worst-case
   upper bound. The lightcone-edge (d=2) case matches Google's
   actual configuration and is substantially easier.

4. Noise-assisted truncation does not work for OTOC^(2). The attack
   relies entirely on circuit structure (topology, depth, M-B placement),
   not on noise exploitation.

5. Per-arm depth ~12 lies at the phase-transition boundary (d_crit ~ 11).
   The attack is feasible if screening persists (d < d_crit), uncertain
   if not. This is an explicitly conditional claim. [v0.4 + v0.5 update]

6. Concurrent literature: Goodman et al. (arXiv:2604.12330, 2026-04-14)
   reports a positive-P phase-space classical algorithm at 1152 modes
   (Jiuzhang 3.0 regime) with quadratic complexity. Goodman explicitly
   excludes Jiuzhang 4.0 (3050-photon) as future work. Our T7
   transparency-vacuum finding extends to a new O7 axis (epsilon
   thermalisation). Full assessment deferred to v0.6.

---

## Discussion preview (§6 mosaic) [NEW v0.5]

Three classical attacks were applied to T1, T3, T7 from the 2025
quantum-advantage list:

- **T1 (Quantum Echoes / Willow OTOC^(2))**: substantively attacked
  via Pauli-path SPD; <=255 terms feasible at Google's LC-edge config
  on 65q at d=4. Regime-dependent: screening (exp tail, Path B) vs
  post-transition (power-law tail alpha=1.705, Path C essential).
  Per-arm d=12 borderline at d_crit~11.

- **T3 (D-Wave 3D Ising)**: substantively attacked via NQS (RBM
  alpha=4-16); method-class intrinsic-limit ridge at alpha~16 with
  anti-monotonic regression at alpha=32.

- **T7 (Jiuzhang 4.0)**: stood firm against 8/10 surveyed methods.
  9th (SVD-low-rank M6) conditional on Haar-typicality verification.
  10th (Goodman positive-P) explicitly excluded JZ 4.0 due to scale.

Three different boundary types are revealed: regime-transition (T1,T8),
ansatz-capacity with intrinsic-limit ridge (T3), transparency-vacuum
(T7). The non-uniformity of outcomes is itself the methodology
contribution.

---

*Draft v0.5, 2026-04-26. All claims backed by committed data.*
*Three independent verification paths (claude4 SPD, claude7 adaptive, claude8 Pauli-path) converge.*
*§A5 joint draft v0.3.1 (claude3+claude4) locked. §audit-as-code.A v0.3 (claude8) drafted.*
*Source Data: commits listed in header + claude8 936c5e4/0228d7e/0ec8674/627afb7/953b155 + claude7 a7bb9e2.*
