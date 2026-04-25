"""
T8 Hafnian-direct oracle for JZ 3.0 small mode subsets.

Per t-modywqdx allocation correction (claude5 ack ts=1777100097230):
  - claude5 lead: (2) MPS chi=100-400 + Oh-2024 SDK sampler 主体
  - claude8 副: (1) Hafnian-direct probability oracle + (3) HOG/TVD benchmark

This wrapper provides exact ground-truth probabilities on small (10-12 mode) subsets
of the JZ 3.0 (144 mode, r=1.5, eta=0.424) interferometer for cross-validating
claude5's chi-truncated Oh-MPS approximation. Different-algorithm cross-check =
stronger §D5 paper signal than two-implementations-of-Oh-MPS.

Backend: thewalrus (Bulmer 2022 phase-space toolchain).

Reference instance: claude5 skeleton JZ30_AUDIT.gaussian_baseline_status (pending,
populated by this wrapper).

Stub status: SKELETON v0.1 (Tick N+1 four-stub push). All compute paths raise
NotImplementedError; smoke test only checks thewalrus import availability.

Implementation roadmap (Tick N+2):
1. thewalrus.hafnian or thewalrus.quantum.probabilities API selection.
2. Mode-subset selection strategy (10-12 modes from 144):
   - random subset (n_runs=10 for variance)
   - lightcone-aligned subset (heralded-mode neighborhood)
3. JZ 3.0 covariance matrix construction (r=1.5 squeezing + eta=0.424 loss).
4. Compute exact Pr(click pattern) for each subset.
5. Output JSON for Tick N+3 hog_tvd_benchmark consumption.

References:
  - Bulmer 2022, Sci. Adv. 8, eabl9236 (arXiv:2108.01622) — thewalrus-implemented
    GBS phase-space sampler, hafnian-based.
  - Quesada et al. PRX Quantum 3, 010306 (2022) — quadratic speedup hafnian.
  - JZ 3.0 paper (Madsen 2022 / Deng 2023 line) — 144 modes, r=1.5, eta=0.424.

Status: PENDING Tick N+2 implementation.
"""
from __future__ import annotations

from typing import Dict, List


JZ30_PARAMS = {
    "n_modes": 144,
    "squeezing_r": 1.5,
    "loss_eta": 0.424,
}


def construct_jz30_covariance_matrix():
    """Build the 2N x 2N Gaussian covariance matrix for JZ 3.0 lossy interferometer."""
    raise NotImplementedError("Tick N+2: thewalrus + (r=1.5, eta=0.424, U_haar) -> Sigma")


def select_mode_subset(strategy: str, n_modes: int = 12, seed: int = 42):
    """Select a subset of modes for exact-hafnian probability computation."""
    raise NotImplementedError("Tick N+2: random / LC-aligned / heralded subset strategies")


def exact_hafnian_probability(subset_modes, click_pattern):
    """Compute Pr(click_pattern | subset) via thewalrus exact hafnian."""
    raise NotImplementedError("Tick N+2: thewalrus.hafnian on reduced covariance")


def emit_oracle_json(out_path: str) -> None:
    """Write {subset, click_patterns, exact_probs} JSON for hog_tvd consumer."""
    raise NotImplementedError("Tick N+2: serialize (subset_id, click_pattern, prob)")


def _smoke():
    try:
        import thewalrus  # noqa: F401
        print("hafnian_oracle.py: thewalrus importable; ready for Tick N+2 implementation")
    except ImportError:
        print("hafnian_oracle.py: thewalrus NOT installed; pip install thewalrus before Tick N+2")


if __name__ == "__main__":
    _smoke()
