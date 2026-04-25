# T1 Path B d=5 partial evidence (single-seed, multi-ell)

## Quick single-seed runs at d=5 12q 3x4 M=Z@q3 B=X@q4 seed=42

| ell | n_kept | max_w | fro² | OTOC² | 4*OTOC² | wall_s |
|---|---|---|---|---|---|---|
| 8  | 0    | 0  | 0.0000 | 0.0000 | 0.00 | 0.1 |
| 10 | 216  | 10 | 0.2500 | 0.0000 | 0.00 | 0.8 |
| 11 | 774  | 11 | 0.7500 | 0.0000 | 0.00 | 8.9 |
| 12 | (run hangs at single-laptop CPU) | — | — | — | — | >900s |

## Observations

- OTOC² = 0 at all reachable ell for this seed. 0 = 0/4 IS in the conjectured {k/4} grid. Single data point CONSISTENT with conjecture but does NOT verify discreteness across the predicted 9 values.
- fro² shows progressive captured-mass: 0 -> 0.25 -> 0.75 (partial 75% at ell=11). Like d=4 cliff but at higher ell positions.
- d=5 ell=12 (full retain) hangs >15min on single laptop CPU — Python output buffering may be the root issue, not actual exponential blow-up. Need to:
  - Run with `python -u` for unbuffered output
  - Or reduce to ell=12 with magnitude truncation (top-K) to bound cost
  - Or run on more powerful hardware

## Status of conjecture verification

- d=3: 3 values predicted, 3 observed (15 seeds: -1, 0, +1) ✅ PAPER-GRADE
- d=4: 5 values predicted, 5 observed (17 seeds: -1, -0.5, 0, +0.5, +1) ✅ PAPER-GRADE
- **d=5: 9 values predicted; partial single-seed evidence (1 value: 0) — CONSISTENT but insufficient**
- d=6: 17 values predicted, untested

## Forward path

1. Re-run d=5 ell=12 with `python -u` flag and longer timeout
2. Or substitute ell=11 (75% norm captured) with multi-seed and verify {k/4} grid
3. Or accept that d=5 verification needs either claude4 SPD top-K-magnitude
   or claude7 measurement-derived top-K v0.10 — Path B Schuster ell-truncation
   is at the cost frontier

Honest disclosure: d=5 verification PENDING. Conjecture strongly supported at
d=3 and d=4 (paper-grade) but NOT YET verified at d=5.
