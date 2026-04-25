# §A5 — Limitations and method-class capacity boundaries (T1 + T3 joint draft v0.3)

> Co-authored: claude3 (T3 owner) + claude4 (T1 owner).
> Status: draft v0.3, T1+T3 co-authored merged + alpha=32 anti-monotonic update.
> Tracks claude7 §audit-as-code chapter (v0.4-v0.6) cross-T# 4-class taxonomy:
> scale-parameter regime-transition (T1, T8) / ansatz-engineering capacity-bound
> (T3, with method-class intrinsic-limit ridge sub-pattern) / hardware-capacity
> bounded (T6) / transparency-vacuum (T7). This §A5 jointly frames the T1 + T3
> mitigation axis; T6/T7/T8 cross-referenced via the §A5.2 4-class table.

---

## A5.1  Common negative pattern: naive ansatz / naive noise treatment is insufficient

In both T1 (Quantum Echoes / OTOC^(2) on Willow) and T3 (D-Wave
diamond Ising ground state), the obvious first attempt to approximate
the experiment classically *fails by a margin large enough to be
paper-grade*:

- **T3 (claude3)**: A vanilla restricted Boltzmann machine with
  α=4 hidden units (~200 parameters) trained by Adam (no
  Stochastic Reconfiguration) **fails** to recover the ground-state
  energy on every diamond size we test in the King-relevant range.
  Across N ∈ {32, 36, 40, 54, 72} the relative error exceeds the
  Mauron-Carleo +7% threshold uniformly, with peak +28.27% at
  N=40 (commit `5747eb6` + `a9b4195`). The wall is sharp: graph
  diameter 5 → 6 (between N=24 and N=32 at L_perp=2) is the
  dividing line.

- **T1 (claude4)**: Sparse Pauli Dynamics with the assumption
  that the noise channel can substitute for explicit truncation
  is **insufficient** in the scrambled / high-depth regime. The
  Willow OTOC^(2) data exhibits a *regime transition* (claude4
  v0.3 / v0.4) at depth d ≥ d_crit, where the sparse-truncation
  + noise-assisted approach fails to track the experimental
  signal. Specifically: on 12-qubit LC-edge circuits (3x4 grid, M at
  lightcone edge per Bermejo et al. 2026 §II.1.3), the w<=4 truncation
  norm collapses from 1.000 (d=4) to 0.966 (d=6) to **0.058 (d=8)**
  — a 94% loss of operator norm at depth 8. The phase transition occurs
  at d_crit ~ grid_diameter / (2 x v_B) ~ 11 for Willow 65q (8x8 grid,
  empirical v_B ~ 0.65 from 12q d=4/6/8 chain). Post-transition, the
  Pauli coefficient tail transitions from exponential (screening regime,
  slope -0.5) to power-law (alpha=1.705, DELTA_AIC=+1158 decisively
  favoring power-law; claude8 v9-v10 commits 8169f47, 953b155).
  (Source Data: claude4 commits 54216cd, c9784b7; claude8 936c5e4)

**Common pattern**: in both attacks, the *first ansatz family
sized and tuned by literature defaults* fails to clear the
fidelity threshold the experiment sets. Reading these as failures
of the literature ansatz family, rather than as universal
classical limits, is the paper-grade interpretation.

## A5.2  Distinct mitigation paths: capacity vs regime

The two attacks then diverge in *how* the failure resolves.

- **T3 — method-class intrinsic-limit ridge (paper-grade resolution
  within scope)**. Increasing the RBM hidden-units multiplier from
  alpha=4 to alpha=16 partially closes the gap at N=48 (5/5 break)
  and N=54 (4/5 break), but at N=72 only 1/5 break, and **further
  increase to alpha=32 anti-monotonically regresses to 0/5 break
  with all 5 seeds getting worse**. This places the boundary as the
  **method-class intrinsic limit at alpha~16** for this lattice scale
  at the tested sample budget (n_samples=2048), not a parametric
  capacity wall. Three candidate mechanisms remain to be
  disambiguated: (i) Adam-without-SR optimizer fundamentally limits
  at alpha>=16 (P6 tests via SR-equivalent gradient SNR with 4x
  n_samples); (ii) n_samples=2048 insufficient SR-equivalent gradient
  signal-to-noise (P6 dual-tests, overlap with mechanism (i));
  (iii) RBM ansatz class intrinsic at this scale (P2 inductive-bias
  test orthogonal to optimizer).
  (commits: f1d09c9 P1 SUPPORTED + 58a2022 P2 N=54 4/5 + 4509c39
  P3 N=72 1/5 + 9087c9b P-ext alpha=32 0/5 anti-monotonic)

- **T1 — regime-transition (paper-grade resolution within scope)**.
  Rather than scaling the ansatz capacity, the resolution is to
  *recognize and stay within* the SPD-tractable regime (depth
  d below d_crit), and to phrase the attack scope explicitly in
  these terms. In the screening regime (d < d_crit ~ 11), SPD with
  fixed weight ell in [6, 10] captures >96% of operator norm on
  LC-edge configurations, and the attack is feasible (65q projection:
  <=255 terms at d=4). In the post-transition regime (d >= d_crit),
  the tail becomes power-law and fixed-weight truncation fails at
  any ell; Path C adaptive top-K (claude7 v0.8-v0.9) is essential,
  providing cost linear in active-set size rather than exponential
  in weight bound. The combined Path B (screening) + Path C
  (post-transition) constitutes the paper-grade defensible scope.
  (Source Data: claude4 f265c51, ce81491, c9784b7; claude7 c5b7565,
  21b878a; claude8 0ec8674, 953b155). The classical-method boundary on
  Quantum Echoes at this depth scale is set by a regime parameter
  (d_arm x v_B vs grid_diameter), not by ansatz capacity.

These two distinct mitigation paths — **ansatz-engineering** vs
**regime-restriction** — populate two distinct cells of the
cross-target meta-observation matrix maintained in §audit-as-code
(claude7 v0.4 / cycle 21):

| Class | Examples | Mechanism | Sub-pattern |
|-------|----------|-----------|-------------|
| Scale-parameter regime-transition | T1, T8 | natural evolution | d_crit phase transition |
| Ansatz-engineering capacity-bound | T3 (RBM alpha) | designer-choice | **method-class intrinsic-limit ridge** (anti-monotonic regression) |
| Hardware-capacity bounded | T6 (TN bond/slicing) | physical RAM/GPU | monotonic, plateau at hardware ceiling |
| Transparency-vacuum | T7 | data-availability mismatch | M6 conditional |

These four classes are *complementary, not collapsible*:
attempts to compress them into a single "boundary mapping"
narrative would erase the very physics that distinguishes the
attack classes.

## A5.3  Common future-work bound

Both attacks have a hard upper-N at which the present method
cannot generate ground-truth comparison without further work:

- **T3**: For diamond N ≥ 128 we no longer have either ED
  (infeasible at 2^128 basis states) or DMRG bytewise-converged
  truth (open at chi > 512). The present work therefore cannot
  speak to the King reported sizes 567 / 3367 directly. The
  capacity-resolvable interpretation suggests deeper RBM
  (α ≥ 32) or a different ansatz class (NeuralJastrow, transformer,
  PixelCNN) may extend the boundary, but verifying this
  extension requires either (a) a new ground-truth pipeline
  beyond DMRG (e.g., parallel tempering Monte Carlo at very
  high N) or (b) accepting variational-vs-variational comparison
  without an absolute reference.

- **T1**: For circuits at d_arm >= 14 (= grid_diameter for Willow
  65q corner-placement worst case), the SPD truncation cost exceeds
  available compute at any fixed weight bound (Path B fails in
  power-law tail regime; 65^12 ~ 10^22 per sample). Path C adaptive
  top-K remains viable but requires per-circuit empirical calibration
  (K ~ 6800 for 99% retained norm at d=8, claude7 v0.10). The present
  work cannot speak to per-arm depths >= 14 without either (a)
  streaming SPD implementation (claude8 prototype pending) or (b)
  GPU-accelerated computation beyond the 8GB laptop constraint.
  The estimated per-arm depth of 12 (Bermejo brickwall inference,
  UNVERIFIED from Nature paywall) lies at d_crit ~ 11 +/- 1 step,
  making the 65q Willow attack **borderline** — feasible if screening
  persists, infeasible if not. This is an explicitly conditional claim.
  (Source Data: claude4 54216cd, c9784b7, ce81491; claude8 e08334f)

In both cases the boundary is *quantitative and reported with the
specific hyperparameters that produced it* (claude6 audit checklist
discipline). The papers therefore make claims about the
classical-method-attack boundary at the specified hyperparameter
configuration, not about the underlying physics being classically
unattackable in principle.

## A5.4  T8 — GBS loss-exploitation boundary and multi-method cross-validation [NEW v0.4]

> Drafted by claude2 (T8 owner, commit 29ea07c); integrated by claude4.

The Jiuzhang 3.0 GBS experiment (Deng et al., PRL 134, 090604, 2025;
144 modes, 255 detected photons) operates at total transmission
eta = 0.424, below the critical threshold eta_c ~ 0.538 (Oh et al.
Nature Physics 20, 1647, 2024). Five independent classical methods
were implemented: (i) Gaussian quadrature sampler (10M samples/2.2min),
(ii) Fock-aggregate thermal sampler, (iii) exact Hafnian oracle,
(iv) pairwise chi correction (negative result: TVD worsened 8%),
(v) positive-P phase-space sampler (click correlations +525%).

Triple-implementation cross-validation revealed two-tier structure:
cutoff=4 self-consistency (TVD < 0.032) vs cutoff-vs-full regime gap
(TVD ~ 0.18). As negative control, the same baseline on Jiuzhang 4.0
(eta=0.51 > eta_c=0.21, 8176 modes) gives 1086% deviation, correctly
identifying the simulability boundary.

Note: throughout this work, the 144-mode regime corresponds to
Jiuzhang 2.0 (Zhong et al. PRL 127, 180502, 2021); Jiuzhang 3.0
(Deng et al. PRL 131, 150601, 2023; 1152 modes) is the larger system
tested by Goodman et al. (arXiv:2604.12330, 2026).

## Style / cross-references

- §H1 honest scope: each attack's resolution is "POSITIVELY
  RESOLVED IN SCOPE" (claude5 ThresholdJudge convention) — i.e.,
  resolved for the parameter range tested, with the hyperparameter
  set documented, no extrapolation beyond that range claimed.
- §H4 hardware-specific results: numbered ansatz hyperparameters
  appear in §6 reproducibility (T3) and the corresponding §
  in T1 paper.
- §audit-as-code chapter (claude7 v0.4 / claude6 audit_index v0.5)
  hosts the cross-T# taxonomy. This §A5 cross-references that
  chapter rather than reproducing the full taxonomy here.

---

*[End §A5 v0.4 draft. T1+T3+T8 merge complete. alpha=32 anti-monotonic + T8 5-method + JZ naming fix.]*
