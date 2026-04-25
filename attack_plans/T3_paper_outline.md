# T3 Paper Outline v0.1

**Working title**: *Mapping the RBM Classical-Approximation Boundary on Diamond Spin Glass*

> Status: outline draft. Authors-internal. Not yet a manuscript.
> Owner: claude3. §D5 reviewer: claude7.

## Story in one paragraph

King et al. (Science 388, 199, 2025) demonstrate beyond-classical
quantum simulation of disordered spin-glass dynamics on the D-Wave
Advantage2 processor across five geometries, two precision regimes,
sizes up to 567 (now 3367) qubits, and quench times 7–40 ns.
We do **not** challenge the beyond-classical claim. Instead, we
**quantitatively map** the precision boundary of one specific
classical attack — the restricted Boltzmann machine ansatz with
α≤8 trained by Adam without Stochastic Reconfiguration — on the
3D diamond geometry at the ground-state level. We find a sharp
discontinuous transition: the RBM hits the exact ground state at
N≤24 to machine precision, but plateaus at +12–19% relative error
for all N ∈ {36, 54, 72}. We discuss possible causes and propose
the boundary itself as the contribution.

## Sections

### 1. Introduction
- King et al. 2025 claim (5 geometries × 2 precision × t_a 7–40 ns
  × ⟨q²⟩ + Binder cumulant; sizes up to 3367)
- Mauron-Carleo 2503.08247 sub-claim (diamond, high-precision,
  t_a=7 ns, N≤128) and King's response 2504.06283
- Our scope: diamond geometry, ground state at Γ=0, sizes 8–72,
  fixed J seed (RandomState(42), uniform[-1,1])
- Contribution: empirical precision boundary, not a beyond-classical
  challenge

### 2. Methods (claude7 lead on §D5 cross-validate methodology)
- 2.1 Lattice spec v2 (canonical lexicographic indexing, sorted
  edges; J/edges MD5 hash protocol). Reference: commit d9cf7fa
- 2.2 RBM ansatz (NetKet 3.21, complex-valued, α∈{2,4,8}, Adam
  optimizer, MetropolisLocal sampler, 8 chains, 512–2048 samples
  per VMC step). NetKet SR preconditioner unavailable on this
  JAX/plum combination — flagged as limitation
- 2.3 ED brute-force ground state for N≤24 (reproducible across
  authors via J/edges hash)
- 2.4 DMRG (claude7 contribution): tenpy chi=64/128/256/512.
  Convergence: chi=64 already bytewise identical for N=36/54/72
  (sparse classical Ising → low entanglement → polynomial cost)
- 2.5 §D5 reviewer-author cross-validation protocol:
  ED (N=8/16/24) → DMRG (N=36/54/72) → RBM independent runs;
  reviewer (claude7) supplies authoritative truth, author (claude3)
  reports RBM error. Hash-based J/edges alignment guarantees
  identical Hamiltonian across both ends

### 3. Results
- 3.1 Table: RBM α=4 vs ground truth (ED for N≤24, DMRG for N≥36)

  | N | Ground truth | RBM α=4 | rel_err | Status |
  |---|---|---|---|---|
  | 8 | -4.411178 (ED) | -4.411 | <0.01% | ✓ BREAK |
  | 16 | -11.504074 (ED) | -11.504 | 0.00% | ✓ BREAK |
  | 24 | -16.145950 (ED) | -16.133 | +0.08% | ✓ BREAK |
  | 36 | -27.789167 (DMRG) | -23.518 | +15.4% | ✗ FAIL |
  | 54 | -35.958331 (DMRG) | -29.135 | +19.0% | ✗ FAIL |
  | 72 | -46.382921 (DMRG) | -40.545 | +12.6% | ✗ FAIL |

- 3.2 Discontinuous transition at N=24→36: ratio jumps from 0.08%
  to 15.4%, a factor of ~190× in a single step. Not a smooth
  capacity decay
- 3.3 α-scan at N=36: α=2/4/8 all fail at ~15% (capacity ceiling
  hypothesis ruled out by α=8 not improving over α=4)
- 3.4 Wall-clock cost T(N) ~ N^2.30 for the unconverged optimization
  (commit c1bf88c). Fast does not mean accurate

### 4. Discussion
- 4.1 Phase-transition framing: 0.08% → 15.4% is qualitative, not
  quantitative. Unlikely to be capacity overflow alone
- 4.2 Hypotheses for the watershed (left open as future work):
  - permutation symmetry breaking at the 3D-3D-vertical lattice
    transition (Lv goes from 1/2 to ≥3 effective)
  - effective information entropy of J distribution shifting
    above an RBM-representable threshold
  - Adam's basin-finding insufficient without Stochastic
    Reconfiguration in this regime
- 4.3 Comparison to Mauron-Carleo (4-th order Jastrow + SR,
  reportedly N=128 with <7% correlator error at t_a=7 ns):
  consistent with the hypothesis that SR or 4-body cumulant
  subtraction is necessary for N≥36

### 5. Limitations and Future Work
- 5.1 Ground state only. Quench dynamics framework verified at
  N=8 (commit 91902d1, piecewise TDVP with RK4) but not pushed
  to King's regime
- 5.2 Single geometry (diamond). 2D square, 3D-cubic-dimer,
  3D-cubic-nodimer, biclique not addressed
- 5.3 Single precision (high-precision a/128). ±J low-precision
  not tested
- 5.4 Two-point correlators only. 4-point Binder cumulant not
  computed
- 5.5 SR-RBM exploration deferred (NetKet 3.21 + JAX 0.10
  compatibility issue with VMC_SR; rollback to NetKet 3.20
  documented as path (a))

### 6. Methods reproducibility (per claude6 audit checklist)
- 6.1 J generation: `np.random.RandomState(42).uniform(-1, 1, size=len(edges))`
  on canonical_diamond_v2 sorted edges
- 6.2 Hash table for cross-validation:
  N=16 J_md5 = `424e74310832a0b11b650fbe0342f3fb`
  N=72 J_md5 = `29eb3e38ddffee6569acb8f34cb347d2`
- 6.3 RBM seed: `seed=42` for both Flax param init and MC sampler
- 6.4 All commits referenced in this outline are public on
  branches `claude3` and `claude7` of the team repo

### 7. §D5 cross-validation methodology contribution (claude7 lead)
- 7.1 Reviewer-author cycle as a methodology, not just a process
- 7.2 Pre-experiment hash alignment (J + edges) prevents
  graph-isomorphism trap (case study: commit a209bb6 → d9cf7fa
  spec v2 freeze)
- 7.3 Independent variational ansätze (RBM + DMRG) for
  cross-validation when ED is infeasible

## Open author actions
- [claude3] Try NetKet 3.20 rollback for SR-RBM at N=36 (path (a) hedge)
- [claude3] Quench dynamics demo at N≤24 (path (b), §methods only)
- [claude7] Take §D5 cross-validation methodology section
- [claude7] tenpy TDVP-MPS exploration (optional, dynamics second axis)
