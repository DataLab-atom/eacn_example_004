# Pauli weight tail analysis — Phase 0b cross-check

**Source**: claude4 JSON exports on `origin/claude4` (commits `0775fa7` 16q,
`575b59b` 8q pair). Loaded via `git show origin/claude4:<path>` — NOT copied
into the claude8 branch (branch-fence compliant).

**Caveat**: all inputs are NOISELESS SPD outputs. 8q cases have n_eff ≈ n
trivially. 16q is unscrambled distant M-B only — 16q scrambled OOM'd on
8 GB. Conclusions are DIAGNOSTIC, not predictive of 65q Willow scale.

## Summary table

| Case | terms | top-1 |c|^2 | top-10 |c|^2 | top-100 |c|^2 | hot sites (p50) | hot share | tail fit (R^2 exp / R^2 pow) |
|---|---:|---:|---:|---:|---|---:|---|
| 16q_4x4_unscrambled_d=4_distant_M-B | 233 | 24.91% | 93.52% | 100.00% | 5/16 | 100.00% | exp R²=0.353 / pow R²=0.174 |
| 8q_2x4_unscrambled_d=4_distant(q0,q7) | 1023 | 21.54% | 82.19% | 99.69% | 6/8 | 100.00% | exp R²=0.512 / pow R²=0.242 |
| 8q_2x4_scrambled_d=4_adjacent(q0,q1) | 4007 | 18.86% | 67.48% | 99.00% | 7/8 | 100.00% | exp R²=0.754 / pow R²=0.522 |
| 36q_6x6_unscrambled_d=4_distant(q0,q35) | 3839 | 24.35% | 80.08% | 99.63% | 7/36 | 100.00% | exp R²=0.725 / pow R²=0.586 |
| 12q_3x4_scrambled_d=4_adjacent(q0,q1) | 3884 | 25.29% | 88.03% | 99.73% | 7/12 | 100.00% | exp R²=0.707 / pow R²=0.604 |

### 16q_4x4_unscrambled_d=4_distant_M-B
- terms: 233 (expected 233)
- total norm Σ|c|²: 1
- cumulative coverage: top-1 24.91%, top-10 93.52%, top-100 100.00%, top-1% (k=2) 47.27%
- per-qubit support count: [233, 0, 0, 0, 0, 0, 0, 174, 0, 0, 0, 174, 0, 0, 171, 171]
- hot sites (count ≥ 50% of max site count): [0, 7, 11, 14, 15] (5/16) carrying 100.00% of total support count
- tail fit (skip top-5): log|c|² ~ exp slope=-0.884 (R²=0.353); log|c|² ~ pow slope=-116 (R²=0.174) → **tail = EXPONENTIAL**

### 8q_2x4_unscrambled_d=4_distant(q0,q7)
- terms: 1023 (expected 1023)
- total norm Σ|c|²: 1
- cumulative coverage: top-1 21.54%, top-10 82.19%, top-100 99.69%, top-1% (k=10) 82.19%
- per-qubit support count: [1023, 0, 0, 768, 768, 768, 768, 768]
- hot sites (count ≥ 50% of max site count): [0, 3, 4, 5, 6, 7] (6/8) carrying 100.00% of total support count
- tail fit (skip top-5): log|c|² ~ exp slope=-0.29 (R²=0.512); log|c|² ~ pow slope=-147 (R²=0.242) → **tail = EXPONENTIAL**

### 8q_2x4_scrambled_d=4_adjacent(q0,q1)
- terms: 4007 (expected 4007)
- total norm Σ|c|²: 1
- cumulative coverage: top-1 18.86%, top-10 67.48%, top-100 99.00%, top-1% (k=40) 94.88%
- per-qubit support count: [4007, 3036, 3036, 0, 2993, 2993, 3014, 2991]
- hot sites (count ≥ 50% of max site count): [0, 1, 2, 4, 5, 6, 7] (7/8) carrying 100.00% of total support count
- tail fit (skip top-5): log|c|² ~ exp slope=-0.11 (R²=0.754); log|c|² ~ pow slope=-251 (R²=0.522) → **tail = EXPONENTIAL**

### 36q_6x6_unscrambled_d=4_distant(q0,q35)
- terms: 3839 (expected 3839)
- total norm Σ|c|²: 1
- cumulative coverage: top-1 24.35%, top-10 80.08%, top-100 99.63%, top-1% (k=38) 97.74%
- per-qubit support count: [3839, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2880, 2816, 2880, 0, 0, 0, 2880, 2816, 2880]
- hot sites (count ≥ 50% of max site count): [0, 27, 28, 29, 33, 34, 35] (7/36) carrying 100.00% of total support count
- tail fit (skip top-5): log|c|² ~ exp slope=-0.11 (R²=0.725); log|c|² ~ pow slope=-261 (R²=0.586) → **tail = EXPONENTIAL**

### 12q_3x4_scrambled_d=4_adjacent(q0,q1)
- terms: 3884 (expected 3884)
- total norm Σ|c|²: 0.571513
- cumulative coverage: top-1 25.29%, top-10 88.03%, top-100 99.73%, top-1% (k=38) 98.02%
- per-qubit support count: [3203, 2043, 2043, 1976, 2043, 0, 2043, 1976, 0, 0, 0, 0]
- hot sites (count ≥ 50% of max site count): [0, 1, 2, 3, 4, 6, 7] (7/12) carrying 100.00% of total support count
- tail fit (skip top-5): log|c|² ~ exp slope=-0.106 (R²=0.707); log|c|² ~ pow slope=-261 (R²=0.604) → **tail = EXPONENTIAL**

