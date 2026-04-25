# T8: HOG Scaling — Gaussian Baseline vs Mode Count

| N modes | Patterns | Time (s) | HOG | vs Uniform |
|---------|----------|----------|-----|-----------|
| 4 | 256 | 1.2 | 0.648 | BEATS |
| 6 | 729 | 0.9 | 0.515 | BEATS (marginal) |
| 8 | 6561 | 62.3 | 0.441 | loses |

## Interpretation

Gaussian baseline HOG decreases with N: captures correlations at
small scale but insufficient at larger scale. This is EXPECTED —
Oh et al.'s MPS chi correction is designed to close this gap.

The trend confirms the attack architecture:
1. Gaussian baseline: correct photon statistics, partial HOG
2. MPS chi correction: improves probability-level accuracy → HOG
3. At JZ 3.0 scale (144 modes): chi~400 needed for competitive HOG

This is consistent with Oh et al. using chi=160-600 for JZ 2.0.
