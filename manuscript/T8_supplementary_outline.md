# T8 Supplementary Information Outline

> Draft by claude2. Lists all SI content needed per AGENTS.md §E1-E7.

---

## Fig. S1 — Oh et al. critical threshold phase diagram
- (r, η) phase diagram with JZ 3.0 and JZ 4.0 operating points marked
- Source: results/T8/T8_corrected_analysis.png (upgrade to vector)

## Fig. S2 — HOG scaling across 4/6/8 modes
- HOG vs N with Gaussian baseline decline
- Source: results/T8/ (need combined figure)

## Fig. S3 — Triple-impl two-tier TVD structure
- 4-subset × 3-method TVD matrix
- Source: claude5 cross-validation data

## Fig. S4 — JZ 4.0 negative control
- Gaussian prediction vs reported photon counts
- Source: results/T8/T8_jz4_negative_control.md

## Fig. S5 — Positive-P WC correlation improvement
- Click correlation: thermal vs positive-P + WC
- Source: results/T8/T8_goodman_positive_p.png (upgrade to vector)

## Fig. S6 — Pairwise chi correction negative result
- TVD and HOG before/after correction showing -8% degradation
- Source: results/T8/T8_chi_correction_negative.md

## Table S1 — Five classical methods comparison
| Method | Regime | HOG | TVD | Wall-clock | Commit |
|--------|--------|-----|-----|-----------|--------|
| Gaussian quadrature | Full | 0.648 (4m) | — | 2.2 min/10M | d6ca180 |
| Fock-aggregate sample | Cutoff=4 | — | 0.030 | — | 60a92a8 |
| Hafnian oracle | Cutoff=4 | 0.637 | 0.031 | 127s | 540e632 |
| Pairwise chi correction | Full | -8% | -8% | — | a843594 |
| Positive-P + WC | Full | — | — | 5.8 μs/sample | f940d7e |

## Table S2 — Jiuzhang series parameter comparison
| Version | Modes | η | r (nepers) | Sq. photons | Status |
|---------|-------|---|-----------|-------------|--------|
| JZ 1.0 | 100 | 0.283 | 1.35-1.84 | — | BROKEN (Bulmer 2022) |
| JZ 2.0 | 144 | 0.476 | 1.34-1.81 | 4.965 | BROKEN (Oh 2024) |
| JZ 3.0 | 144 | 0.424 | 1.49-1.66 | 3.556 | THIS WORK |
| JZ 4.0 | 8176 | 0.510 | ≤1.8 | — | Stands firm |

## §E1 — Full derivations
- Oh critical threshold empirical fit derivation
- Gaussian→click conversion formula
- Positive-P WC coloring transform

## §E2 — Negative controls
- JZ 4.0: 1086% deviation (detailed)
- Pairwise chi correction: -8% (detailed)

## §E3 — Robustness scans
- η sweep: D_required vs η at multiple squeezing levels
- Source: results/T8/T8_eta_sweep.csv

## §E4 — Raw data
- T8_triple_impl_claude2.json (click pattern counts)
- T8_noise_budget_results.csv (T4 cross-reference)
- T8_goodman_positive_p.json

## §E5 — Failed experiments
- MPS 2D chi-insensitive (T4 commit 2e475f5)
- Pairwise chi correction -8% (T8 commit a843594)
- Morvan lambda definition error (T4 commit d37ca22)
- Statistical undetectability withdrawal (T4 commit cac3bb5)
