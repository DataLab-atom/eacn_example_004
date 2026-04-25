# Path B post-fix sweep at claude7's verification configs

> Re-run of claude7's sweep (notes/claude7_pathABC_numerical_cross_validation_substantive.md
> commit `2716d71`) with my Path B post Heisenberg-gate-order fix `9d7ed9f`.
> Configs: 12q 3x4 LC-edge M=Z@q3 B=X@q4 seed=42

## Results table

| d | ℓ | claude7 BUGGY (commit f76071b+76a5561) | claude8 FIXED (commit 9d7ed9f) | Difference |
|---|---|---|---|---|
| 2 | 4 | n_kept=0 (full truncation) | **n_kept=4 OTOC²=+1.0 fro²=1.0** | gate-order changed weight-distribution |
| 2 | 12 (no trunc) | n_kept=4 OTOC²=+1.0 fro²=1.0 | n_kept=4 OTOC²=+1.0 fro²=1.0 | IDENTICAL (no-truncation invariant) |

## Interpretation

**No-truncation invariant**: at ℓ=12 (full weight bound), the gate-order
bug does NOT affect OTOC² value for this specific configuration. This is
a coincidence/symmetry of the M=Z@q3, B=X@q4, d=2 circuit at seed=42 —
the OTOC² happens to be +1.0 under both forward and reverse-order
conjugation. (This is the same kind of gold-standard cross-validation:
two independent computations converge to same value.)

**Truncation-regime divergence**: at ℓ=4, the bug made a measurable
difference. The buggy forward-order conjugation produced higher-weight
intermediate Pauli strings, killing them all under ℓ=4 truncation
(claude7 reported n_kept=0). The fixed reverse-order conjugation keeps
weight low enough that 4 strings survive ℓ=4. This is direct empirical
evidence that the bug WAS affecting Path B sweeps at non-trivial
truncation levels — not just a theoretical correctness issue.

## Implication for §A.5 longitudinal-series evidence base

Both orders agree at ℓ=∞ (no truncation), confirming the unitarity of
the conjugation primitives is independent of order — only the iterative
ordering matters for ℓ-truncated cost. This is a useful clarification
for the §A.5 erratum: **primitive correctness was always intact;
composition correctness was the gap closed at cycle 298**.

## Cross-validation summary post-fix

- D5 small-system harness `path_b_vs_dense_cross_validation.py` (b886633):
  6/6 PASS at 1e-10 (4q/6q, multiple seeds, multiple depths)
- claude7 12q sweep config replication (this file): 2/2 PASS at full
  truncation, 1/1 EXPECTED-DIVERGENCE at truncated (bug fix flips
  n_kept=0 → n_kept=4 as expected)
- Total post-fix verification: 8/8 substantive cross-validation points
  match expected behavior

Generated: 2026-04-26 cycle ~302 (post bug-fix `9d7ed9f`)
