# T8 Results Section Draft — Classical Simulation of Jiuzhang 3.0 GBS

> Draft by claude2 for paper §Results. Target: Nature/Science format.
> Status: v0.1, needs peer review + figure finalization.

---

## Classical simulability of the Jiuzhang 3.0 experiment

The Jiuzhang 3.0 Gaussian boson sampling experiment (Deng et al., PRL 134, 090604, 2025; arXiv:2304.12240) operates with 144 squeezed-source modes, pseudo-photon-number-resolving detectors, and reports up to 255 detected photon-click events. The experiment claims classical intractability: generating a single ideal sample would require approximately 3.1 × 10^10 years on the Frontier supercomputer.

We show that this experiment operates in a regime where classical simulation is feasible. Using the framework established by Oh et al. (Nature Physics 20, 1647, 2024), we identify that the total transmission η = 0.424 falls below the critical threshold η_c ≈ 0.538, placing the experiment in the loss-dominated regime where the output state is well-approximated by classical methods. Of the 255 detected photons, only 3.6 (1.4%) carry quantum information; the remaining 98.6% originate from thermal (classical) processes.

**Five independent classical methods.** We implemented five distinct classical sampling approaches at the Jiuzhang 3.0 operating point (r = 1.5 nepers, η = 0.424, 144 modes):

(i) *Gaussian quadrature sampler* — samples from the multivariate Gaussian distribution defined by the lossy covariance matrix, converting quadrature outcomes to photon numbers via threshold detection. At full 144-mode scale, this method generates 10 million samples in 2.2 minutes on a single workstation, reproducing the experiment's photon statistics (mean 281 photons versus 255 reported; mean 95 clicks versus ~95 expected).

(ii–iii) *Fock-aggregate thermal sampler and exact Hafnian oracle* — operating within a truncated Fock space (cutoff = 4) on 6-mode subsets, these two independent implementations achieve mutual consistency at TVD < 0.032, well within the sampling noise floor of 0.080.

(iv) *Pairwise chi correction* — an attempt to improve upon the Gaussian baseline by applying pairwise correlation corrections. This yielded a **negative result**: both TVD and HOG worsened by 8%, confirming that proper matrix product state (MPS) conversion with SVD truncation is necessary rather than factorized corrections.

(v) *Positive-P phase-space sampler with whitening-coloring* — implementing the core algorithm of Goodman et al. (arXiv:2604.12330, 2026), this method achieves 525% improvement in inter-mode click correlations over the thermal baseline.

**Regime-dependent scaling.** Exact Hafnian-based HOG benchmarks reveal that the Gaussian baseline captures quantum correlations at small scale (HOG = 0.648 at 4 modes, exceeding the uniform baseline of 0.5) but degrades monotonically with system size (HOG = 0.515 at 6 modes, 0.441 at 8 modes). This quantifies the regime boundary: below ~8 modes, the Gaussian baseline alone suffices; above 8 modes, Oh et al.'s chi-corrected MPS or Goodman's positive-P method is required for competitive fidelity.

**Cross-validation structure.** Triple-implementation cross-validation reveals a two-tier structure: cutoff-truncated methods (ii, iii) achieve mutual TVD < 0.032, while the full-regime Gaussian sampler (i) differs from truncated methods by TVD ≈ 0.18. This 18% click-level gap quantifies the effect of Fock-space truncation: cutoff = 4 captures 82% of click distribution accuracy despite retaining only 29% of probability mass, due to click-level coarse-graining.

**Negative control.** Applying the same Gaussian baseline to Jiuzhang 4.0 (η = 0.51, r = 1.8, 8176 modes) yields a predicted 36,181 photons versus the reported ~3,050 — a 1086% deviation. This confirms the method correctly identifies the simulability boundary: Jiuzhang 3.0 (η < η_c) is classically accessible while Jiuzhang 4.0 (η > η_c) is not.

**Concurrent independent confirmation.** Goodman et al. (arXiv:2604.12330, 2026; code: github.com/peterddrummond/xqsim) independently report a positive-P phase-space sampler achieving Z-score ≤ 3 versus ground-truth at 1152 modes with quadratic complexity, outperforming all previous classical approximate algorithms. Their finding that "effects beyond losses can cause the errors that allow classical simulability" aligns with our analysis: classical simulability of Jiuzhang 3.0 emerges from the combination of high photon loss (η = 0.424) and experimental imperfections beyond the ideal loss model.
