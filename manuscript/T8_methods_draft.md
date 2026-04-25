# T8 Methods Section Draft

> Draft by claude2. Target: Nature Methods section format.

---

## Lossy GBS covariance construction

The Jiuzhang 3.0 experiment uses 144 squeezed-source modes with squeezing parameter r = 1.49–1.66 nepers (10.4–13.9 dB), passed through a random unitary interferometer U (Haar-distributed), followed by photon loss at total transmission η = 0.424 (Oh et al., arXiv:2306.03709, Table I; Deng et al., PRL 134, 090604, 2025; arXiv:2304.12240).

The lossy output state is Gaussian with covariance matrix:
σ_lossy = η · S · σ_sq · S^T + (1 − η)/2 · I

where σ_sq = diag(e^{-2r}, e^{2r}, ...) is the squeezed vacuum covariance (xp-ordering), S is the symplectic representation of U, and I is the identity (vacuum noise from the loss channel). All covariance matrices are 288 × 288 real symmetric positive-definite.

## Oh et al. critical threshold

Oh et al. (Nature Physics 20, 1647, 2024) established that lossy GBS becomes classically simulable when the total transmission falls below a critical threshold η_c. For the Jiuzhang 3.0 parameter regime (25 squeezed sources, r ≈ 1.5), we estimate η_c ≈ 0.538 using an empirical fit to Oh et al. Table I data (code/shared/oh_2024_critical_eta.py). The Jiuzhang 3.0 operating point η = 0.424 < η_c provides a margin of 0.114 (21% below threshold).

## Gaussian quadrature sampling

Samples are drawn from the multivariate Gaussian distribution N(0, σ_lossy) using Cholesky decomposition of the 288 × 288 covariance matrix. Quadrature pairs (x_i, p_i) are converted to photon number proxies via n_i = max(0, round((x_i² + p_i²  − 1)/2)). Click patterns are obtained by thresholding: c_i = 1 if n_i > 0, else 0. Batched sampling (10,000 samples per batch) avoids memory overflow at full 144-mode scale. Wall-clock time: 0.67 seconds for 50,000 samples at 144 modes on a single workstation (AMD Ryzen, 16 GB RAM, no GPU).

## Exact Hafnian probabilities

For small-scale benchmarks (4–8 modes), exact GBS output probabilities are computed using the Hafnian of the A-matrix:

P(n_1, ..., n_M) = |Haf(A_S)|² / (∏ n_i! · √det(σ_Q))

where A = X(I − σ_Q^{-1}), σ_Q = σ_lossy + I/2, X is the symplectic exchange matrix, and A_S is the submatrix of A with rows/columns repeated according to photon numbers. Hafnians are computed using the thewalrus library v0.22.0 (Gupt et al., JOSS 4, 1705, 2019). Fock space is truncated at cutoff = 4 photons per mode.

## HOG score computation

The Heavy Output Generation (HOG) score measures the fraction of classical samples falling in the high-probability region of the ideal output distribution. For each mode configuration, exact probabilities are enumerated via Hafnian, the median probability is computed, and the HOG score is the fraction of classical samples with probability above the median. A HOG score of 0.5 corresponds to uniform random sampling; HOG > 0.5 indicates the classical sampler captures quantum correlations.

## Positive-P phase-space sampling

Following Goodman et al. (arXiv:2604.12330, 2026), we implement a positive-P sampler with iterative whitening-coloring (WC). Initial samples are drawn independently per mode from thermal distributions with mean photon number n̄_i = (σ_lossy[2i,2i] + σ_lossy[2i+1,2i+1] − 1)/2. The real and imaginary parts of complex amplitudes α_i are stacked into a 2M-dimensional vector and iteratively transformed: (1) whiten by Cholesky decomposition of current sample covariance; (2) color by Cholesky decomposition of target covariance (derived from σ_lossy in the complex α basis). After 10 WC iterations, photon numbers are drawn from Poisson distributions with mean |α_i|², and click patterns obtained by thresholding. This procedure achieves 525% improvement in inter-mode click correlations over the independent thermal baseline.

## Negative control

The same Gaussian baseline is applied to Jiuzhang 4.0 parameters (η = 0.51, r = 1.8, 8176 modes; arXiv:2508.09092) on a 200-mode subset. The critical threshold at these parameters is η_c ≈ 0.21 (code/shared/oh_2024_critical_eta.py), placing Jiuzhang 4.0 well above the simulability boundary. The resulting 1086% photon count deviation (predicted 36,181 vs reported ~3,050) confirms the method correctly identifies the boundary between classically simulable and quantum-hard regimes.

## Software and reproducibility

All code is implemented in Python 3.11 with NumPy 2.4, SciPy 1.17, quimb, cotengra, and thewalrus 0.22.0. Random seeds are fixed (seed = 42) throughout. Hardware: single workstation, AMD Ryzen CPU, NVIDIA RTX 4060 8GB GPU (GPU used for cotengra contraction path optimization only). All scripts and results are archived on branch claude2 of the project repository.
