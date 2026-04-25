# T3 Attack Scope Analysis — King et al. response to classical attacks

> Source: arXiv:2504.06283 (King et al. 2025-04-10), responding to Tindall et al.
> arXiv:2503.05693 and Mauron & Carleo arXiv:2503.08247.

## Important: King et al. originally claim BEYOND-CLASSICAL across:

### 5 geometries
- 2D square lattices
- 3D diamond lattices ← Mauron-Carleo's only test
- 3D cubic-dimer lattices
- 3D cubic-nodimer lattices
- Dimerized biclique graphs (long-range)

### 2 precision regimes
- "high-precision": couplings J = a/128 with a ∈ {-128, ..., 128}
- "low-precision": ±J model (faster correlation growth, harder)

### Annealing times
- 7 ns to 40 ns (longer = more correlated, harder)

### Physical observables
- Edwards-Anderson order parameter ⟨q²⟩ (2-point)
- **Binder cumulant U (4-point)** — much harder
- Full-state sampling for arbitrary observables

### Sizes
- Up to 567 qubits in original Science paper
- 3367 qubits (L=12) in 2025-04 comment update

## What Mauron-Carleo (my baseline ansatz) did NOT cover

Per King's comment §"We now also address recent results of Mauron and Carleo":
1. Only diamond lattice (NOT 3D-dimer, square, biclique)
2. Only high-precision (NOT ±J)
3. Only t_a = 7 ns (the shortest, most treelike correlations)
4. Only N ≤ 128
5. Only 2-point correlators (NOT Binder cumulant / 4-point)
6. Linear extrapolation of error vs R² has no theoretical justification
7. Only 2D scaling in system size (Lz constant)
8. No Monte Carlo resource cost included

→ "out of all the simulations performed in our work, they only
showed results on the sparsest example with the shortest and
most treelike correlations" — King et al.

## What Tindall et al. (BP tensor networks) did NOT cover

1. Biclique lattices not tractable by their method (no result)
2. Mainly 2D (which King didn't claim was beyond-classical)
3. 3D limited to 54 qubits (3×3×3 dimer)
4. 2-point correlations only, no Binder cumulant
5. Only high-precision problems
6. Up to 20 ns (not 40 ns)

## Implication for my T3 attack

**Current state (commit 50ff9e3)**:
- Built ED + RBM α=4 on diamond lattice, ground state energy match at N=16/24
- This is the EASIEST sub-problem: ground state (Γ=0, no time evolution)

**Gaps to "T3 broken in spirit of King's claim"**:
- ❌ Time evolution (quench dynamics at t_a > 7 ns)
- ❌ 4-point observables (Binder cumulant)
- ❌ Low-precision (±J) regime
- ❌ Other geometries (square, 3D-dimer, biclique)
- ❌ Sizes N > 128
- ❌ Full-state sampling (not just energy/correlator match)

**T3 verdict update**:
- judge1 "energy_fidelity_vs_ED at GS Γ=0": BREAK at N≤24 ✓
- judge_dynamics "fidelity vs King QPU at t_a ∈ [7,40] ns": NOT YET TESTED
- judge_geometry "coverage of 5 King geometries": ONLY 1 of 5 (diamond)
- judge_observables "Binder cumulant 4-point match": NOT TESTED
- judge_precision "low-precision ±J also broken": NOT TESTED
- judge_size "N up to 567 / 3367": NOT TESTED

→ T3 attack is **strictly weaker than even Mauron-Carleo** on its own narrow case.
   It is NOT yet a global "T3 BREAK" — only "T3 PARTIAL: ground state on
   diamond N≤24 matched". Honest scoping required for §5.2 status proposal.

## Recommended next milestones for genuine T3 attack progression

Order by feasibility / impact:
1. **Time-evolved fidelity at t_a = 7 ns on diamond N=16** (matches Mauron-Carleo
   regime). Need t-VMC training schedule with annealing dynamics, not just GS.
2. **Compute ⟨q²⟩ Edwards-Anderson at finite t_a** — need to add disorder average.
3. **Add ±J low-precision** as second J-distribution choice (1-line fix).
4. **Try 3D-dimer geometry** as second lattice.
5. **N=54 then N=128** scaling (if RBM α=4 still hits ED-bounded comparator).
6. **Binder cumulant 4-point** — hardest, requires full-state samples.

## §H3 reminder (AGENTS.md):
"经典方法跑通了 X 不等于量子计算机不擅长 X" — i.e., showing classical
ground-state fidelity is necessary but not sufficient. Need quench dynamics
+ correct critical exponent extraction to challenge the actual King claim.
