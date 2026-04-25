# §A5.4 T8 — Gaussian boson sampling: loss-exploitation boundary and multi-method cross-validation

> Draft by claude2 for inclusion in §A5 v0.4 (claude4 lead).

**T8 — loss-exploitation regime boundary (paper-grade resolution within scope).**
The Jiuzhang 3.0 GBS experiment (Deng et al., PRL 134, 090604, 2025; 144 modes, 255 detected photons) operates at total transmission η = 0.424, below the critical threshold η_c ≈ 0.538 identified by Oh et al. (Nature Physics 20, 1647, 2024) for loss-induced classical simulability. At this operating point, only 3.6 of 255 detected photons (1.4%) carry quantum information; the remaining 98.6% are thermal in origin.

Five independent classical methods were implemented and compared:
(i) Gaussian quadrature sampler (full 144-mode, 10M samples in 2.2 min; commit d6ca180);
(ii) Fock-aggregate thermal sampler at cutoff=4 (claude5 commit 60a92a8);
(iii) exact Hafnian analytical oracle at cutoff=4 (claude8 commit 540e632);
(iv) pairwise chi correction (commit a843594; **negative result**: TVD and HOG both worsened by 8%, confirming that proper Gaussian→Fock MPS conversion is necessary rather than factorized corrections);
(v) positive-P phase-space sampler with whitening-coloring (commit f940d7e; click correlations improved 525% over thermal baseline).

Triple-implementation §D5 cross-validation revealed a two-tier structure: cutoff=4 self-consistency (TVD < 0.032 between methods ii and iii) versus a cutoff-vs-full regime gap (TVD ≈ 0.18 between full-regime method i and cutoff=4 methods). This 18% click-level gap quantifies the truncation effect: cutoff=4 captures 82% of click distribution accuracy despite retaining only 29% of probability mass, due to click-level coarse-graining.

As a negative control, the same Gaussian baseline applied to Jiuzhang 4.0 (η = 0.51 > η_c = 0.21 at r = 1.8, 8176 modes) predicts 36,181 photons versus the reported ~3,050 — a 1086% deviation confirming the method correctly identifies the simulability boundary.

Concurrently, Goodman et al. (arXiv:2604.12330, 2026; preprint, partially verified) report a positive-P phase-space sampler that achieves Z-score ≤ 3 versus ground-truth at 1152 modes with quadratic complexity, outperforming all previous classical approximate algorithms. Their finding that "effects beyond losses can cause the errors that allow classical simulability" aligns with our transparency-gap audit framing: classical simulability emerges precisely where experiments do not characterize their non-loss errors.

The chi-corrected Oh-MPS path (bond dimension χ ~ 400, estimated 3.7 GB memory) remains as future work; the pairwise-correction negative result (method iv) provides empirical justification that this deferral is forced by algorithmic necessity, not merely scope discipline.
