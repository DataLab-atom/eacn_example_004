# §6 Discussion Draft (for Nature/Science manuscript)

> **Status**: Draft v0.2 — absorbs claude5 T7-E1/E2/F1 + T8-E1/F1 + claude1 F-3 + claude7 Path C v0.10
> **Author**: claude4 | **Scope**: Full Discussion section

---

## Attack outcomes mosaic

We systematically evaluated leading classical attack frameworks at the
actual experimental parameters of each target. The non-uniformity of
outcomes is itself the methodology contribution — we report what works
and what doesn't, rather than a uniform claim of universal classical
breakdown.

### T1 (Quantum Echoes / Willow OTOC^(2))

Substantively attacked via Pauli-path SPD. At Google's lightcone-edge
configuration on 65 qubits (depth 4): <=255 terms projected, with
single-string concentration >=65% and exponential tail slope <=-0.99
(claude8 v6). The attack is **regime-dependent**: in the screening
regime (d < d_crit ~ 11), fixed-weight truncation (Path B, ell in
[8,14]) captures dominant tail mass with exponential decay; in the
post-transition regime (d >= d_crit), tails recover power-law scaling
(alpha = 1.705, 95% CI [1.55, 1.84], DELTA_AIC = +1158 [10^251 odds]),
and adaptive top-K truncation (Path C) becomes essential.

With estimated Willow per-arm depth ~12 (Bermejo brickwall inference),
the experiment lies at the transition boundary (d_crit ~ 11 +/- 1).
This is an explicitly conditional claim: feasible if screening persists,
uncertain if not.

### T3 (D-Wave 3D diamond Ising)

Substantively attacked via NQS (RBM alpha=4-16). The attack reveals a
**method-class intrinsic-limit ridge**: increasing alpha from 4 to 16
partially closes the gap (N=48 5/5 break, N=54 4/5 break), but further
increase to alpha=32 anti-monotonically regresses to 0/5 break. Three
candidate mechanisms remain to be disambiguated: (i) Adam-without-SR
optimizer limit, (ii) sample budget insufficiency, (iii) RBM ansatz
class intrinsic at this scale.

### T7 (Jiuzhang 4.0)

Stood firm against 8 of 10 surveyed classical methods at actual
experimental parameters (1024 squeezed sources, 8176 output modes,
mean_n=9.5, eta=0.51). The 9th method (SVD-low-rank exploitation, M6)
is conditional on independent verification of the implemented
unitary's Haar-typicality (transparency audit gap O2). The 10th
method (Goodman et al. positive-P, arXiv:2604.12330, 2026) explicitly
excludes JZ 4.0 due to scale, but introduces a new transparency-vacuum
axis O7 (thermalisation epsilon > 1-tanh(r) ~ 0.095 at r=1.5). The
two conditional methods (M6 + Goodman) pivot on orthogonal
transparency-vacuum axes (O2 Haar + O7 thermalisation epsilon), so
closing one does not close the other — the dual-conditional structure
preserves T7 stands-firm verdict regardless of which axis is resolved
first.

### T8 (Jiuzhang 3.0 / 144 modes)

Five independent classical methods implemented (Gaussian quadrature,
Fock-aggregate thermal, exact Hafnian, pairwise chi correction
[negative result], positive-P with whitening-coloring). Triple-impl
cross-validation reveals two-tier TVD structure (cutoff=4
self-consistency TVD < 0.032 vs cutoff-vs-full gap TVD ~ 0.18).
The 0.18 TVD gap quantifies click-coarse-graining at cutoff=4:
~82% click-distribution accuracy preserved despite only 29%
probability mass capture, explaining why cutoff-truncated attacks
remain comparable to full-regime methods despite operating on
truncated Fock space.
Negative control on JZ 4.0 gives 1086% deviation, correctly
identifying the simulability boundary.

## Four boundary types

Four distinct boundary types characterize the classical-quantum
frontier across the attack portfolio:

1. **Scale-parameter regime-transition** (T1, T8): classical attack
   feasibility transitions at a depth/scale threshold determined by
   physical parameters (butterfly velocity, grid diameter, loss rate)

2. **Ansatz-engineering capacity-bound** (T3): classical attack
   feasibility depends on the ansatz expressive class, with a
   method-class intrinsic-limit ridge at optimal capacity

3. **Hardware-capacity bounded** (T6): classical attack feasibility
   limited by physical compute resources (RAM, GPU, bond dimension),
   with monotonic scaling to hardware ceiling

4. **Transparency-vacuum** (T7): classical attack feasibility
   conditional on experimental data availability; transparency gaps
   prevent definitive assessment in either direction

These four classes are complementary, not collapsible. A potential
5th class — physical-mechanism-induced-classicality (Goodman et al.
positive-P algorithm-orthogonal axis) — is documented at the
companion audit-as-code chapter (claude8 §A v0.4, commit c68f3a2)
but not empirically demonstrated in this paper's attack portfolio.

The attack regime actually measured on Willow (lightcone-edge M-B
placement) coincides with the regime most tractable for fixed-weight
SPD — a finding that Google's choice of M-B placement for maximum
quantum signal simultaneously minimizes classical simulation cost.

### Path B + Path C regime-complementary cost comparison

At Willow 65q, the combined Path B (fixed-weight) + Path C (adaptive
top-K) provides regime-dependent cost savings (claude7 v0.10, commit
f008622):

| d_arm | Regime | Path C K | Path B w<=ell | Compression |
|-------|--------|----------|---------------|-------------|
| 4 | screening | 5.6e7 | 5.6e7 | 1x (equivalent) |
| 8 | marginal | 5.6e7 | 5.6e7 | 1x (still feasible) |
| 12 | post-trans border | 5.6e7 | 2.06e9 (w<=5) | **37x** |
| 14 | deep post-trans | 5.6e7 | 2.3e18 (w<=12) | **essential** |

Path C is regime-complementary to Path B: equivalent in screening,
37x compression at the transition boundary, and essential in the
deep post-transition regime where Path B becomes infeasible.

## Concurrent literature

Goodman et al. (arXiv:2604.12330, 2026) reports a positive-P
phase-space classical algorithm achieving quadratic complexity at
1152 modes (Jiuzhang 3.0 regime). Their finding that "effects beyond
losses can cause the errors that allow classical simulability" aligns
with our transparency-gap audit framing. Goodman explicitly excludes
Jiuzhang 4.0 as future work due to scale, strengthening (not
weakening) our T7 transparency-vacuum verdict.

## PEPS vs Pauli-path separation

Bermejo et al. (arXiv:2604.15427) prove PEPS-based tensor network
methods require bond dimension D ~ exp(sqrt(N)) for Quantum Echoes,
rendering TNBP infeasible. Our Pauli-path approach operates in a
fundamentally different paradigm: PEPS bond dimension controls spatial
entanglement, while Pauli weight threshold controls operator-space
sparsity. Our data shows Pauli-path term count *decreases* with system
size on wide grids, while PEPS bond dimension increases exponentially.
This empirical evidence suggests a separation between the two classical
attack paradigms for OTOC circuits, warranting further theoretical
analysis.

## Schuster-Yin reconciliation

The Pauli coefficient tail behavior is regime-dependent rather than
universal. In the screening regime, the OTOC lightcone structure acts
as a noise-equivalent truncation mechanism, producing exponential
tails. In the post-transition regime, tails recover power-law scaling
consistent with Schuster et al. (arXiv:2407.12768). The screening
regime exponential behavior is thus a special case of the general
framework, not a contradiction.

---

*Draft v0.1, 2026-04-26.*
