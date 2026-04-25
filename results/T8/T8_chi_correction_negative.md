# T8: Chi Correction Prototype — Negative Result

## Pairwise correction approach FAILS

| Method | TVD vs exact | HOG (weighted) |
|--------|-------------|----------------|
| Thermal baseline | 0.5008 | 0.7948 |
| Pairwise corrected | 0.5426 | 0.7330 |
| **Change** | **-8.4% (worse)** | **-7.8% (worse)** |

## Why it fails

Pairwise correction (P_corrected = P_thermal × prod R(ni,nj)) introduces
inconsistencies: correction factors from different pairs contradict each
other, leading to a WORSE approximation than pure thermal.

## Correct approach needed

Oh et al.'s MPS method is NOT pairwise correction. It:
1. Converts Gaussian state → Fock-space MPS representation
2. Uses SVD truncation to bond dim chi
3. Samples from the MPS directly

This requires Gaussian→MPS conversion (Hafnian-based matrix decomposition),
which is a non-trivial algorithm beyond simple covariance manipulation.

## Value of this negative result

Eliminates a wrong implementation path. Confirms that proper MPS
representation (not factorized correction) is essential for Oh's method.
