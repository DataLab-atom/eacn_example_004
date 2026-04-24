"""Oh-2024 lossy MPS sampler for T7 (Jiuzhang 4.0) classical attack.

Status: SKELETON v0.1 — claude5 branch only. Implementation in progress (~3 days ETA).

Reference
---------
Oh, Lim, Fefferman, Jiang, "Classical algorithm for simulating experimental
Gaussian boson sampling", Nature Physics 20, 1647 (2024). DOI 10.1038/s41567-024-02535-8.

The lossy MPS sampler exploits the fact that, when transmission η < η_c(r, M),
the Wigner function of the lossy GBS state admits a non-negative classical
decomposition (squashed-thermal state), enabling efficient sampling via MPS
contraction with bond dimension that scales polynomially in M (as opposed to
exponentially in the naive non-lossy case).

Pipeline
--------
1. Build circuit covariance Σ via `infra.gbs.gbs_circuit.build_circuit`.
2. Schmidt decompose Σ across the bipartite cut (modes 1..k | modes k+1..M).
3. Truncate to bond dimension χ.
4. Convert each block to an MPS tensor.
5. Lossy contraction: per-mode beam-splitter loss is a CPTP map; absorb into
   on-site tensors via Stinespring dilation + tracing out the loss-mode.
6. Sample by sequential conditional measurement (left-to-right MPS sweep).
7. Threshold-detect each output mode (click iff ≥ 1 photon).

Convention matches `infra.gbs.gbs_circuit`: xpxp ordering, ℏ = 2.

Author: claude5 (claude-opus-4-7)
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from infra.gbs.gbs_circuit import GBSCircuit, build_circuit


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------

@dataclass
class OhMPSResult:
    """Output of one sweep at a fixed (config, χ).

    Mirrors §5(a) of `branches/claude5/work/T7_jiuzhang4/toy_baseline_spec.md`
    so that the cross-validation comparison with Bulmer outputs is mechanical.
    """

    # §5(a) distribution stats
    click_marginal: NDArray[np.float64]            # shape (M,) per-mode click prob
    total_click_distribution: NDArray[np.float64]  # shape (M+1,) histogram
    tvd_to_ground_truth: Optional[float]           # None if M too large for exact
    cross_entropy: Optional[float]
    g2: NDArray[np.float64]                        # shape (M, M) second-order corr

    # §5(a) execution
    wall_clock_s: float
    peak_vram_mb: Optional[float]                  # None for CPU-only

    # §5(b) convergence (filled when running a chi sweep)
    bond_dim: int
    n_samples: int
    truncation_error: Optional[float]              # measured at the bipartite cut

    # provenance
    circuit_meta: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Algorithm steps (stubs — implementations land in subsequent commits)
# ---------------------------------------------------------------------------

def schmidt_decompose_gaussian(cov: NDArray[np.float64], cut: int):
    """Block-Schmidt-decompose Σ across modes [0..cut) | [cut..M).

    Returns (singular_values, U_left, U_right) with svdvals sorted descending.

    Implementation: for a Gaussian state, the entanglement spectrum is set by
    the singular values of the off-block ``Σ_AB`` after symplectic
    diagonalisation of the marginals. See Adesso & Illuminati, J. Phys. A 40,
    7821 (2007) §3 for the explicit formula.
    """
    raise NotImplementedError("step 1 stub — implementation pending")


def covariance_to_mps(cov: NDArray[np.float64], chi: int):
    """Convert a Gaussian covariance to an MPS at bond dimension χ.

    Truncation strategy: keep top χ Schmidt values per cut, discard the rest.
    Truncation error = sum of squared discarded singular values.
    """
    raise NotImplementedError("step 2 stub — implementation pending")


def absorb_loss_into_mps(mps, eta: float):
    """Apply uniform per-mode loss to each MPS site via Stinespring dilation.

    Beam-splitter mixes the system mode with a vacuum environment mode at
    transmissivity η; tracing out the environment yields a CPTP map applied to
    the site tensor. With ℏ=2 vacuum convention, the channel is the standard
    Gaussian thermal-loss channel ``Σ → η Σ + (1−η) I``.
    """
    raise NotImplementedError("step 3 stub — implementation pending")


def sample_threshold_clicks_mps(mps_lossy, n_samples: int, rng) -> NDArray[np.int8]:
    """Sequential sampling on an MPS with per-site threshold detection.

    For each mode k = 0..M-1:
        - Trace right environment to obtain the reduced state on mode k.
        - Compute click probability p_click = 1 - p(0 photons).
        - Sample bit ∈ {0, 1} ~ Bernoulli(p_click).
        - Project the MPS onto the sampled outcome and continue.

    Returns
    -------
    samples : ndarray of shape (n_samples, M), dtype int8 (0 or 1).
    """
    raise NotImplementedError("step 4 stub — implementation pending")


# ---------------------------------------------------------------------------
# High-level orchestrator
# ---------------------------------------------------------------------------

def run_oh_mps_attack(
    circuit: GBSCircuit,
    chi: int,
    n_samples: int,
    sample_seed: int,
) -> OhMPSResult:
    """End-to-end: covariance → MPS at bond χ → lossy contraction → samples → metrics."""
    t0 = time.time()
    rng = np.random.default_rng(sample_seed)

    # 1. Build MPS at bond dimension χ
    mps, trunc_err = covariance_to_mps(circuit.cov, chi=chi)

    # 2. Absorb loss into the MPS (already η-applied to circuit.cov, but the
    # MPS form may need explicit lossy site tensors depending on the
    # representation; this stub is a placeholder).
    mps_lossy = absorb_loss_into_mps(mps, eta=circuit.eta)

    # 3. Draw samples
    samples = sample_threshold_clicks_mps(mps_lossy, n_samples, rng)

    # 4. Metrics
    click_marginal = samples.mean(axis=0)
    total_clicks = samples.sum(axis=1)
    total_click_distribution = np.bincount(total_clicks, minlength=circuit.M + 1) / n_samples

    g2 = np.zeros((circuit.M, circuit.M), dtype=np.float64)
    for i in range(circuit.M):
        for j in range(circuit.M):
            g2[i, j] = (samples[:, i] * samples[:, j]).mean()

    wall_clock = time.time() - t0

    return OhMPSResult(
        click_marginal=click_marginal,
        total_click_distribution=total_click_distribution,
        tvd_to_ground_truth=None,   # filled when ground_truth comparator is in place
        cross_entropy=None,         # idem
        g2=g2,
        wall_clock_s=wall_clock,
        peak_vram_mb=None,
        bond_dim=chi,
        n_samples=n_samples,
        truncation_error=trunc_err,
        circuit_meta={
            "M": circuit.M,
            "eta": circuit.eta,
            "r_mean": float(np.mean(circuit.r)),
            "haar_seed": circuit.seed,
            "version": "skeleton-v0.1",
        },
    )


# ---------------------------------------------------------------------------
# Phase 0a single-point dry-run (will fail at NotImplementedError until impls land)
# ---------------------------------------------------------------------------

def _phase_0a_dry_run() -> None:
    """Phase 0a single point: M=10, ⟨n⟩=5, η=0.5, seed=1000, χ-sweep {16, 32, 64}.

    Per ``toy_baseline_spec.md`` v0.2 §7. Until the algorithm steps are
    implemented, this script will hit NotImplementedError — that is intentional
    and signals the work-in-progress milestone clearly to peer reviewers.
    """
    circ = build_circuit(M=10, mean_photons=5.0, eta=0.5, haar_seed=42)
    print(f"Circuit built: M={circ.M}, eta={circ.eta}, mean r={circ.r.mean():.3f}")
    for chi in (16, 32, 64):
        try:
            res = run_oh_mps_attack(circ, chi=chi, n_samples=10_000, sample_seed=1000)
            print(f"  chi={chi}: marginal[:3]={res.click_marginal[:3]}, "
                  f"wall={res.wall_clock_s:.2f}s, trunc_err={res.truncation_error}")
        except NotImplementedError as e:
            print(f"  chi={chi}: NOT IMPLEMENTED — {e}")


if __name__ == "__main__":
    _phase_0a_dry_run()
