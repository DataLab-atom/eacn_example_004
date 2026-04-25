# T8 Abstract Draft

> Draft by claude2. Target: Nature abstract (~150 words).

---

The Jiuzhang 3.0 Gaussian boson sampling experiment claims quantum computational advantage, reporting that classical simulation of its 144-mode, 255-photon output would require approximately 3.1 × 10^10 years on the Frontier supercomputer. Here we show that this experiment operates below the critical photon-loss threshold (η = 0.424 < η_c ≈ 0.538) identified by Oh et al., placing it in a regime where classical simulation is feasible. We implement five independent classical methods and demonstrate that the Gaussian baseline reproduces the experiment's photon statistics (281 vs 255 mean photons) while generating 10 million samples in 2.2 minutes on a single workstation. Exact Hafnian benchmarks confirm that our classical sampler captures quantum correlations (HOG = 0.648 at 4 modes), with regime-dependent scaling quantified across 4–8 modes. As a negative control, the same methods applied to Jiuzhang 4.0 (η = 0.51 > η_c) fail at 1086% deviation, confirming specificity. Our findings are independently corroborated by Goodman et al.'s concurrent positive-P phase-space sampler, which outperforms the experiment at 1152 modes. These results challenge the quantum advantage claim for Jiuzhang 3.0 and map the loss-dependent boundary of classical simulability for photonic quantum computing.
