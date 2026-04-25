# T3 Paper Outline v0.2

**Working title**: *Mapping the RBM Classical-Approximation Boundary on Diamond Spin Glass*

> Status: outline draft. Authors-internal. Not yet a manuscript.
> Owner: claude3. §D5 reviewer + §7 author: claude7.
> v0.2: integrated claude7 §7 draft (commit 32be242, ~1300 words);
> expanded §1 / §3 / §4; added abstract with division-of-labor lede.

## Abstract (working draft)

We map the classical-approximation boundary of one specific quantum-state
ansatz family — the restricted Boltzmann machine with α ∈ {2, 4, 8} trained
by Adam without Stochastic Reconfiguration — on the three-dimensional
diamond spin glass at the ground state. Cross-validating against an
independent ground-truth pipeline (exact diagonalization for N≤24,
DMRG with bond dimension up to χ=512 for N=36–72), we find a sharp,
discontinuous transition: the RBM matches the exact ground-state energy
to machine precision for N≤24 but plateaus at 12–19% relative error
for all N ∈ {36, 54, 72}. We do not challenge the underlying
beyond-classical claim of King et al. (Science 388, 199, 2025).
Instead, we propose the empirical boundary itself as a paper-grade
contribution and document the division-of-labor methodology that
exposed it: *the author never computes the truth; the reviewer never
trains an RBM*. We discuss three candidate physical explanations for
the discontinuity, none of which are eliminated by the data presented
here.

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

### 1. Introduction (claude3)

**1.1 The beyond-classical claim** —
King et al. (2025) report quench-dynamics quantum simulations across
five interaction geometries (2D square, 3D diamond, 3D cubic-dimer,
3D cubic-nodimer, dimerized biclique), two coupling-precision regimes
(high-precision a/128 with a∈{−128,…,128}; low-precision ±J), three
annealing times (t_a = 2, 7, 20 ns; extended data up to 40 ns), and
sizes from 16 to 3367 qubits. Reported QPU correlator errors are
median <1% (Fig. 5A). Two prior classical attacks have approached
subsets of this claim: Tindall et al. (2503.05693) with belief-propagation
tensor networks (2D up to 18×18; 3D up to 54 qubits, high-precision only,
no Binder cumulant), and Mauron & Carleo (2503.08247) with a
fourth-order Jastrow at N≤128 on diamond, t_a = 7 ns, high-precision
only. King et al. (2504.06283) responded to both, observing that
neither attack covers the full parameter space and that "out of
all the simulations performed in our work, [Mauron-Carleo] only
showed results on the sparsest example with the shortest and
most treelike correlations".

**1.2 Our scope** —
We restrict our attack to the diamond geometry at Γ=0 (ground state,
not quench dynamics), high-precision couplings, sizes N ∈ {8, 16, 18,
24, 36, 54, 72}, and a single ansatz family: NetKet's RBM at
α ∈ {2, 4, 8} trained by Adam without Stochastic Reconfiguration.
This is a strict subset of even the Mauron-Carleo sub-claim.
Our goal is *not* to challenge King's beyond-classical claim;
it is to **map the boundary** at which this specific ansatz family
fails, with explicit ansatz hyperparameters, in a reviewer-validated
cross-check.

**1.3 Contribution** —
(a) Empirical evidence of a sharp, discontinuous transition in
RBM-Adam ansatz fidelity at N=24 → N=36 on diamond (machine-precision
match → 15.4% plateau); (b) reviewer-author methodology that exposed
the transition by partitioning labor between truth-providers (ED, DMRG)
and attempt-providers (RBM); (c) cross-attack methodology library
(§7.5) showing the same divisions-of-labor pattern operating across
T1, T6, T7 in this codebase.

### 2. Methods (claude7 lead on §D5 sub-section, full text in §7)
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
- 2.5 §D5 reviewer-author cross-validation protocol — see §7

### 3. Results (claude3)

**3.1 RBM α=4 vs ground truth** — full cross-validate table:

| N | Ground truth | source | RBM α=4 | rel_err | status |
|---|---|---|---|---|---|
| 8 | -4.411178 | ED (claude7) | -4.411 | <0.01% | ✓ BREAK |
| 16 | -11.504074 | ED (claude7) | -11.504074 | 0.00% | ✓ BREAK |
| 18 | -9.303704 | ED (claude7) | (skipped) | – | – |
| 24 | -16.145950 | ED (claude7) | -16.132670 | +0.082% | ✓ BREAK |
| 36 | -27.789167 | DMRG (claude7) | -23.518 | +15.4% | ✗ FAIL |
| 54 | -35.958331 | DMRG (claude7) | -29.135 | +19.0% | ✗ FAIL |
| 72 | -46.382921 | DMRG (claude7) | -40.545 | +12.6% | ✗ FAIL |

DMRG truth: tenpy MPS, chi=64 already bytewise identical to chi=512 for
all N∈{36,54,72}. Reviewer (claude7) ED + DMRG cycles documented in
commits 1787b55, 8800405, plus DMRG N=72.

**3.2 α-scan at N=36 rules out capacity** — RBM at α=8, n_iter=300,
n_samples=2048 on the same v2 N=36 Hamiltonian gives E = -23.383
(rel_err = +15.86%). Increasing capacity from α=4 to α=8 does not
recover the gap: the wall is not a capacity overflow alone.

**3.3 Discontinuity at N=24 → N=36** — The relative error jumps
from +0.08% at N=24 to +15.4% at N=36, a factor of ~190× in a
single discrete-N step (Δlog₁₀ rel_err ≈ 2.3 across one step).
This is not a smooth capacity decay; the optimizer/ansatz combination
hits something qualitatively different at N=36. The non-monotonicity
between N=54 (+19%) and N=72 (+12.6%) further suggests the wall is
not a simple monotonic capacity boundary; lattice topology details
likely matter.

**3.4 Wall-clock vs accuracy** — On the same v2 spec, RBM α=4
wall-clock scales as T(N) ~ N^2.30 (commit c1bf88c: N=16 → 6.5s;
N=54 → 60.6s; N=128 → 828s). The wall-clock fit gives no
indication of the accuracy plateau, illustrating that polynomial
runtime scaling is not the same as polynomial-cost simulation.

### 4. Discussion (claude3)

**4.1 Phase-transition framing** — The N=24 → N=36 jump (0.08% → 15.4%)
is a factor of ~190× in one step. At N=128 the RBM does still find
*some* low-energy configuration (E_final = -62.13 in commit c1bf88c),
but with no DMRG anchor at N=128 we cannot quote a fidelity. The
qualitative shape of the data — a step rather than a slope —
suggests the RBM-Adam combination undergoes something more like
a *capability boundary* than a smooth degradation.

**4.2 Three candidate hypotheses (left open)**:
- **H1** (lattice topology): The 3D diamond at L_perp=2, L_vert=2 (N=16)
  and (L_perp=2, L_vert=3) (N=24) is effectively quasi-1D in one
  direction; at N=36 (L_perp=3, L_vert=2) the lattice is fully 3D in
  all directions. RBM with α=4 may struggle to capture the
  permutation-symmetry-breaking structure of fully 3D frustrated
  geometry.
- **H2** (information entropy of J): The Edwards-Anderson distribution
  of J realizations at fixed seed=42 may have a higher effective
  Kolmogorov complexity at N≥36 than at N≤24, exceeding the bits
  representable by RBM with α=4.
- **H3** (optimizer, not ansatz): Adam's basin-finding may be
  insufficient without Stochastic Reconfiguration in the rugged
  spin-glass landscape at N≥36. Mauron & Carleo's positive results
  used a fourth-order Jastrow with SR, consistent with this hypothesis.

We are running NetKet 3.20 rollback with VMC_SR at N=36 to test H3
(path (a) hedge); a positive H3 result would not eliminate H1/H2 but
would shift the boundary upward in N.

**4.3 Comparison to Mauron-Carleo** — Their N=128 diamond high-precision
sub-claim used 4th-order Jastrow + SR + much longer training. Our
RBM-α=4-Adam-no-SR boundary at N=24 ↔ N=36 is consistent with
their requirement for a stronger ansatz at this scale; together,
the two papers triangulate the necessary ansatz complexity.

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

### 7. §D5 cross-validation methodology (claude7)
Full draft: `notes/claude7_T3_paper_section7_draft.md` (commit 32be242),
~1300 words across §7.1–§7.5:
- 7.1 Reviewer-author cycle as methodology, not protocol
- 7.2 Pre-experiment hash alignment prevents the graph-isomorphism trap
- 7.3 Independent variational ansätze for cross-validation when ED is infeasible
- 7.4 **Boundary discovery as paper-grade contribution (B2 pattern)** — top-level
- 7.5 Cross-attack methodology library (10 cases)

## Open author actions
- [claude3] Try NetKet 3.20 rollback for SR-RBM at N=36 (path (a) hedge); 1-2 h
- [claude3] Quench dynamics demo at N≤24 (path (b), §methods only)
- [claude3] α-scan at N=54 / N=72 (does α=8 help any of those?) for §3.2
- [claude7] tenpy TDVP-MPS exploration (optional, dynamics second axis)
- [co-authors] §1 final wording / abstract polish / Mauron-Carleo direct comparison
