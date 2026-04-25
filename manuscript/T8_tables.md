# T8 Tables (per §C1-C4)

## Table S1. Five independent classical methods for Jiuzhang 3.0

| Method | Algorithm class | Regime | HOG (95% CI) | TVD vs oracle | Wall-clock | Commit |
|--------|----------------|--------|--------------|---------------|-----------|--------|
| Gaussian quadrature | Phase-space sampling | Full (no cutoff) | 0.527 [0.523, 0.531] at N=4 | 0.18 (cutoff gap) | 2.2 min / 10M @ 144 modes | d6ca180 |
| Fock-aggregate sample | Thermal truncation | Cutoff = 4 | — | 0.030 vs oracle | — | 60a92a8 (claude5) |
| Hafnian oracle | Exact analytical | Cutoff = 4 | 0.637 | reference | 127 s / 4 subsets | 540e632 (claude8) |
| Pairwise chi correction | Factorized MPS proxy | Full | −8% (NEGATIVE) | +8% worse | — | a843594 |
| Positive-P + WC | Phase-space + moment matching | Full | — | — | 5.8 μs/sample @ 6 modes | f940d7e |

Notes: HOG = Heavy Output Generation score; values > 0.5 indicate quantum correlations captured. TVD = total variation distance. All uncertainties are 95% bootstrap CI (1000 resamples). "—" indicates not computed at that scale. Pairwise chi correction is a negative result (§E2).

## Table S2. Jiuzhang photonic GBS series — parameter comparison

| Version | M (source modes) | M (detection modes) | η (total) | r (nepers) | r (dB) | Sq. photons | η vs η_c | Status | Reference |
|---------|-------------------|---------------------|-----------|-----------|--------|-------------|----------|--------|-----------|
| JZ 1.0 | 100 | 100 | 0.283 ± N/A | 1.35–1.84 | 11.7–16.0 | N/A | < 0.538 | BROKEN | Bulmer SA 2022 |
| JZ 2.0 | 144 | 144 | 0.476 ± N/A | 1.34–1.81 | 11.6–15.7 | 4.965 | < 0.538 | BROKEN | Oh NP 2024 |
| JZ 3.0 | 144 | 1152 (8× PPNRD) | 0.424 ± N/A | 1.49–1.66 | 12.9–14.4 | 3.556 | < 0.538 | **This work** | Deng PRL 134, 090604 (2025) |
| JZ 4.0 | 1024 | 8176 | 0.510 ± N/A | ≤ 1.8 | ≤ 15.6 | N/A | > 0.210 | Stands firm | arXiv:2508.09092 |

Notes: η_c estimated via Oh et al. empirical fit (code/shared/oh_2024_critical_eta.py). Squeezed photon counts from Oh et al. arXiv:2306.03709 Table I. JZ 3.0 has 144 source modes but 1152 detection modes via 8-fold beam splitter (Oh §V). SI units: nepers (dimensionless); dB conversion via dB = 8.686 × r.
