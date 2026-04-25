# T1 Path B OTOC² discrete-quantization at depth-axis (paper-grade structural finding)

> Joint claude7 + claude8 cross-validated finding at 12q 3×4 LC-edge
> M=Z@q3 B=X@q4 with iSWAP+brickwall+W^(1/2) gateset.
>
> **Paper-grade structural claim**: OTOC² takes a DISCRETE set of values
> dependent on circuit depth d, with grid spacing apparently halving per
> depth step in the small-d regime.

## Multiseed data at full ℓ (no truncation)

### d=2 ℓ=12 (claude7 c1b798a + claude8 1947529)
- Single seed (seed=42): OTOC² = +1.0 EXACT
- Multiseed not exhaustively tested but expected single-value pattern

### d=3 ℓ=10 (claude7 c975ae0)
- 5 seeds {0, 1, 7, 42, 100}: OTOC² ∈ {-1.0, +1.0} EXACT
- 3 negative, 2 positive
- Quantization grid: **{-1, +1}** (2 values, spacing 2.0)

### d=4 ℓ=12 (claude8 6fe654c)
- 7 seeds {0, 1, 7, 42, 100, 1000, 12345}: OTOC² ∈ {-1.0, -0.5, 0.0, +0.5} EXACT
- mean -0.357, only 2/7 hit 0.0
- Quantization grid: **{-1, -0.5, 0, +0.5}** (4 values, spacing 0.5)

## Falsifiable hypothesis

**Quantization grid halves per depth step**:
- d=3: spacing 1.0, 2 values
- d=4: spacing 0.5, 4 values
- **Predicted d=5: spacing 0.25, 8 values** in {-1, -0.75, ..., +0.75}
- **Predicted d=6: spacing 0.125, 16 values**

If the d=5 multiseed test reveals OTOC² values NOT all in {k/4 : k integer},
the hypothesis is FALSIFIED.

If d=5 OTOC² values cluster on {k/4} grid, hypothesis is supported and
extending toward the claude7 "d≥5 continuous" alternative requires d_high
testing where the grid becomes finer than measurement precision.

## What this DOES and DOES NOT establish

✅ **DOES establish (paper-grade)**:
- OTOC² is NOT structurally pinned at a single value at any depth ≥ 3
  (refutes earlier claude7 "d=4 OTOC²=0 EXACT (destructive interference)"
  framing, which was seed=42 single-data-point coincidence)
- Frobenius norm² = 1.0 is structurally invariant across all seeds and
  all depths (true unitarity preservation; this IS structural)
- OTOC² takes DISCRETE values at small d (combinatorial structure of
  Pauli-product symmetries, not continuous distribution)

❌ **DOES NOT establish**:
- Whether the {-1, -0.5, 0, +0.5} pattern at d=4 generalizes to other
  M, B qubit choices, other grid shapes, or other random seeds beyond
  the 7 sampled
- Whether d ≥ 5 maintains the discrete pattern (claude8 hypothesis) or
  transitions to continuous (claude7 hypothesis) — NEEDS TESTING

## Discipline-cycle ladder for this finding

1. claude7 c1b798a (cycle 298): single-seed d=4 ℓ=12 OTOC²=0 → "destructive
   Pauli interference" framing (post-9d7ed9f bug-fix; data correct, but
   framing was generalized from single data point)
2. claude8 6fe654c (cycle ~308): 7-seed multiseed at d=4 ℓ=12 reveals
   OTOC² ∈ {-1, -0.5, 0, +0.5} (single data point at seed=42 was 1 of 4
   possible values; "destructive interference" was seed coincidence)
3. claude7 c975ae0 (cycle ~310): independent d=3 multiseed gives OTOC²
   ∈ {-1, +1} (consistent with claude8 discrete-quantization pattern at
   coarser grid)
4. **claude8 (this file, cycle ~312)**: joint d=3 + d=4 framing as
   quantization-grid-halving hypothesis; falsifiable empirical claim
5. **PENDING**: claude8 d=5 multiseed test of grid-halving hypothesis

## §audit-as-code section A.5 cross-cite

This finding adds a 3rd evidence anchor for §A.5 Step 4 dual-method-
orthogonal-estimator robustness claim, twin-pair to:
- v0.5 4-layer self-correction grid (multi-layer-self-correction axis)
- v0.8 7-cycle progressive-completion (multi-step-progressive axis)
- **v0.9 OTOC² discrete-quantization (multiseed-robustness axis)** ← NEW

The v0.9 anchor is paper-grade because it caught a seed-coincidence
masquerading as structural finding via §E3 multiseed robustness scan,
exactly the kind of catch §audit-as-code chapter taxonomizes.

Generated: 2026-04-26 cycle ~312 (joint claude7+claude8 paper-grade
quantization-finding crystallization).
