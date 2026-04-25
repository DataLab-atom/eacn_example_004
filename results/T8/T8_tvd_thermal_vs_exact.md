# T8: TVD Thermal vs Exact — Quantifying the Gap Oh MPS Must Close

## 6-mode exact analysis (r=1.5, eta=0.424, cutoff=3)

| Metric | Value |
|--------|-------|
| TVD(exact, thermal) | 0.5008 |
| HOG thermal (uniform weight) | 0.5007 |
| HOG thermal (probability weight) | 0.7948 |
| HOG Gaussian sampler | 0.5152 |

## Interpretation

- Thermal approximation has TVD=0.50 from exact → 50% accuracy
- But weighted HOG=0.79 shows high-probability patterns are well-matched
- The gap is in low-probability tail (many rare patterns differ)
- Oh et al. MPS chi=400 targets this tail correction
- At JZ 3.0 scale, chi correction should close the 50% TVD gap
  to competitive levels (Oh achieved this for JZ 2.0 with chi=160-600)
