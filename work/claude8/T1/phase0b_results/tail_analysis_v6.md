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
| 24q_4x6_scrambled_d=4_adjacent(q0,q1) | 255 | 50.08% | 96.69% | 100.00% | 5/24 | 100.00% | exp R²=0.262 / pow R²=0.124 |
| 12q_3x4_scrambled_d=4_LC-edge(q0,q4,d=2) GOOGLE-CONFIG | 780 | 38.17% | 98.71% | 100.00% | 5/12 | 100.00% | exp R²=0.670 / pow R²=0.371 |
| 12q_3x4_scrambled_d=4_LC-outer(q0,q5,d=3) | 778 | 18.10% | 79.63% | 99.63% | 5/12 | 100.00% | exp R²=0.288 / pow R²=0.125 |
| 12q_3x4_scrambled_d=4_mid(q0,q8,d=4) | 780 | 20.42% | 71.29% | 99.32% | 5/12 | 100.00% | exp R²=0.488 / pow R²=0.232 |
| 8q_2x4_scrambled_d=4_LC-edge(q0,q2,d=2) | 780 | 27.85% | 80.08% | 99.96% | 6/8 | 100.00% | exp R²=0.616 / pow R²=0.321 |
| 24q_4x6_scrambled_d=4_LC-edge(q0,q7,d=2) GOOGLE-CONFIG-ANALOG | 255 | 65.77% | 96.88% | 100.00% | 5/24 | 100.00% | exp R²=0.429 / pow R²=0.216 |

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

### 24q_4x6_scrambled_d=4_adjacent(q0,q1)
- terms: 255 (expected 255)
- total norm Σ|c|²: 1
- cumulative coverage: top-1 50.08%, top-10 96.69%, top-100 100.00%, top-1% (k=2) 74.15%
- per-qubit support count: [255, 192, 192, 0, 0, 0, 192, 192, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
- hot sites (count ≥ 50% of max site count): [0, 1, 2, 6, 7] (5/24) carrying 100.00% of total support count
- tail fit (skip top-5): log|c|² ~ exp slope=-0.59 (R²=0.262); log|c|² ~ pow slope=-82.6 (R²=0.124) → **tail = EXPONENTIAL**

### 12q_3x4_scrambled_d=4_LC-edge(q0,q4,d=2) GOOGLE-CONFIG
- terms: 780 (expected 780)
- total norm Σ|c|²: 0.999938
- cumulative coverage: top-1 38.17%, top-10 98.71%, top-100 100.00%, top-1% (k=7) 96.92%
- per-qubit support count: [605, 0, 0, 0, 525, 525, 0, 0, 525, 525, 0, 0]
- hot sites (count ≥ 50% of max site count): [0, 4, 5, 8, 9] (5/12) carrying 100.00% of total support count
- tail fit (skip top-5): log|c|² ~ exp slope=-0.502 (R²=0.670); log|c|² ~ pow slope=-212 (R²=0.371) → **tail = EXPONENTIAL**

### 12q_3x4_scrambled_d=4_LC-outer(q0,q5,d=3)
- terms: 778 (expected 778)
- total norm Σ|c|²: 0.561615
- cumulative coverage: top-1 18.10%, top-10 79.63%, top-100 99.63%, top-1% (k=7) 75.37%
- per-qubit support count: [604, 0, 0, 0, 524, 525, 0, 0, 524, 525, 0, 0]
- hot sites (count ≥ 50% of max site count): [0, 4, 5, 8, 9] (5/12) carrying 100.00% of total support count
- tail fit (skip top-5): log|c|² ~ exp slope=-0.211 (R²=0.288); log|c|² ~ pow slope=-78.9 (R²=0.125) → **tail = EXPONENTIAL**

### 12q_3x4_scrambled_d=4_mid(q0,q8,d=4)
- terms: 780 (expected 780)
- total norm Σ|c|²: 0.999922
- cumulative coverage: top-1 20.42%, top-10 71.29%, top-100 99.32%, top-1% (k=7) 65.05%
- per-qubit support count: [605, 0, 0, 0, 525, 525, 0, 0, 525, 525, 0, 0]
- hot sites (count ≥ 50% of max site count): [0, 4, 5, 8, 9] (5/12) carrying 100.00% of total support count
- tail fit (skip top-5): log|c|² ~ exp slope=-0.363 (R²=0.488); log|c|² ~ pow slope=-142 (R²=0.232) → **tail = EXPONENTIAL**

### 8q_2x4_scrambled_d=4_LC-edge(q0,q2,d=2)
- terms: 780 (expected 780)
- total norm Σ|c|²: 0.979416
- cumulative coverage: top-1 27.85%, top-10 80.08%, top-100 99.96%, top-1% (k=7) 71.23%
- per-qubit support count: [780, 525, 525, 525, 0, 0, 525, 525]
- hot sites (count ≥ 50% of max site count): [0, 1, 2, 3, 6, 7] (6/8) carrying 100.00% of total support count
- tail fit (skip top-5): log|c|² ~ exp slope=-0.461 (R²=0.616); log|c|² ~ pow slope=-189 (R²=0.321) → **tail = EXPONENTIAL**

### 24q_4x6_scrambled_d=4_LC-edge(q0,q7,d=2) GOOGLE-CONFIG-ANALOG
- terms: 255 (expected 255)
- total norm Σ|c|²: 1
- cumulative coverage: top-1 65.77%, top-10 96.88%, top-100 100.00%, top-1% (k=2) 78.34%
- per-qubit support count: [255, 192, 192, 0, 0, 0, 192, 192, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
- hot sites (count ≥ 50% of max site count): [0, 1, 2, 6, 7] (5/24) carrying 100.00% of total support count
- tail fit (skip top-5): log|c|² ~ exp slope=-0.987 (R²=0.429); log|c|² ~ pow slope=-142 (R²=0.216) → **tail = EXPONENTIAL**

