"""GBS circuit construction interface (shared between Oh-MPS and Bulmer phase-space samplers).

Status: DRAFT v0.1 — on `claude5` branch only. Promotion to `main` requires §5.2 consensus.

Convention
----------
- Mode ordering: ``[a_1, ..., a_M, a_1^†, ..., a_M^†]`` (xpxp) — matches `thewalrus` and `strawberryfields`.
- Covariance ``Σ`` is the symmetric ``2M × 2M`` real matrix in the ``(x, p)`` quadrature basis with
  vacuum at ``Σ = (ℏ/2) · I``. We use ``ℏ = 2`` so vacuum ``Σ = I``.
- Single-mode squeezed vacuum (SMSV) at parameter ``r`` (nepers) has ``⟨n⟩ = sinh²(r)`` photons
  and the squeezed quadrature variances ``e^{∓2r}`` (vacuum scale).
- "Uniform loss" = identical beam-splitter loss with transmissivity ``η`` applied to every mode.
- Haar-random unitary ``U ∈ U(M)`` is realized via QR decomposition of a complex-normal matrix
  with Mezzadri's diagonal sign correction.

The skeleton intentionally avoids depending on `thewalrus` / `strawberryfields` so both samplers
can target the same primitive. Sampler-specific code (Oh-MPS lossy contraction, Bulmer
phase-space) lives in sibling modules.

Author: claude5  (claude-opus-4-7, 1M ctx)
Issue tracker: branches/claude5/work/T7_jiuzhang4/toy_baseline_spec.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from numpy.typing import NDArray


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class GBSCircuit:
    """A constructed lossy-GBS circuit ready to be sampled.

    Attributes
    ----------
    M : int
        Number of optical modes.
    r : NDArray[np.float64]
        Per-mode squeezing parameter in nepers, shape (M,).
    eta : float
        Uniform per-mode transmissivity, ``0 ≤ η ≤ 1``.
    U : NDArray[np.complex128]
        ``M × M`` Haar-random unitary applied to the squeezed vacua.
    cov : NDArray[np.float64]
        ``2M × 2M`` covariance matrix of the Gaussian state at the detectors,
        post-loss. Vacuum convention: ``ℏ = 2``, so vacuum ``Σ = I``.
    seed : int
        Random seed used for the Haar unitary (reproducibility).

    Notes
    -----
    Threshold detection is the assumed measurement; sampler implementations
    can additionally honour photon-number-resolving readout if needed.
    """

    M: int
    r: NDArray[np.float64]
    eta: float
    U: NDArray[np.complex128]
    cov: NDArray[np.float64]
    seed: int
    metadata: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Haar random unitary
# ---------------------------------------------------------------------------

def gen_haar_unitary(M: int, seed: int) -> NDArray[np.complex128]:
    """Sample an ``M × M`` Haar-random unitary via Mezzadri's QR construction."""
    rng = np.random.default_rng(seed)
    z = (rng.standard_normal((M, M)) + 1j * rng.standard_normal((M, M))) / np.sqrt(2.0)
    Q, R = np.linalg.qr(z)
    diag = np.diag(R)
    Lambda = diag / np.abs(diag)
    return Q * Lambda  # broadcast multiply across columns


# ---------------------------------------------------------------------------
# Covariance construction (xpxp ordering, ℏ = 2)
# ---------------------------------------------------------------------------

def vacuum_cov(M: int) -> NDArray[np.float64]:
    return np.eye(2 * M)


def smsv_cov(r: NDArray[np.float64]) -> NDArray[np.float64]:
    """Block-diagonal covariance of M independent SMSVs at parameters r[i].

    Convention: x quadrature squeezed (variance ``e^{-2r}``), p anti-squeezed
    (variance ``e^{+2r}``). Modes are interleaved xpxp.
    """
    M = r.shape[0]
    cov = np.zeros((2 * M, 2 * M), dtype=np.float64)
    for i, ri in enumerate(r):
        cov[2 * i, 2 * i] = np.exp(-2.0 * ri)
        cov[2 * i + 1, 2 * i + 1] = np.exp(+2.0 * ri)
    return cov


def apply_passive_unitary(cov: NDArray[np.float64], U: NDArray[np.complex128]) -> NDArray[np.float64]:
    """Apply a passive linear-optics unitary to a Gaussian covariance.

    The xpxp covariance transforms as ``S Σ Sᵀ`` with ``S`` the real symplectic
    representation of ``U`` (block matrix of Re U, -Im U / Im U, Re U).
    """
    M = U.shape[0]
    Re, Im = U.real, U.imag
    # Build the 2M x 2M real symplectic representation in xpxp ordering.
    S = np.zeros((2 * M, 2 * M), dtype=np.float64)
    for i in range(M):
        for j in range(M):
            S[2 * i, 2 * j] = Re[i, j]
            S[2 * i, 2 * j + 1] = -Im[i, j]
            S[2 * i + 1, 2 * j] = Im[i, j]
            S[2 * i + 1, 2 * j + 1] = Re[i, j]
    return S @ cov @ S.T


def apply_uniform_loss(cov: NDArray[np.float64], eta: float) -> NDArray[np.float64]:
    """Uniform per-mode beam-splitter loss with transmissivity η.

    Σ_out = η · Σ + (1 − η) · I    (with ℏ = 2 vacuum convention)
    """
    if not 0.0 <= eta <= 1.0:
        raise ValueError(f"eta must be in [0, 1], got {eta}")
    return eta * cov + (1.0 - eta) * np.eye(cov.shape[0])


# ---------------------------------------------------------------------------
# Top-level constructor (the single function callers should use)
# ---------------------------------------------------------------------------

def build_circuit(
    M: int,
    mean_photons: float,
    eta: float,
    haar_seed: int = 42,
    r_per_mode: Optional[NDArray[np.float64]] = None,
) -> GBSCircuit:
    """Construct a complete lossy GBS circuit from physical parameters.

    Parameters
    ----------
    M : int
        Number of modes.
    mean_photons : float
        Per-mode ⟨n⟩. If ``r_per_mode`` is None, uniform ``r = arsinh(√⟨n⟩)``.
    eta : float
        Uniform transmissivity in [0, 1].
    haar_seed : int
        Seed for the Haar unitary (default 42, matches toy_baseline_spec v0.1).
    r_per_mode : Optional array of shape (M,)
        Override per-mode squeezing in nepers. If given, ``mean_photons`` is ignored.

    Returns
    -------
    GBSCircuit
    """
    if r_per_mode is None:
        r = np.full(M, np.arcsinh(np.sqrt(mean_photons)), dtype=np.float64)
    else:
        r = np.asarray(r_per_mode, dtype=np.float64)
        if r.shape != (M,):
            raise ValueError(f"r_per_mode must have shape ({M},), got {r.shape}")

    U = gen_haar_unitary(M, haar_seed)
    cov0 = smsv_cov(r)
    cov_after_U = apply_passive_unitary(cov0, U)
    cov_after_loss = apply_uniform_loss(cov_after_U, eta)

    return GBSCircuit(
        M=M,
        r=r,
        eta=eta,
        U=U,
        cov=cov_after_loss,
        seed=haar_seed,
        metadata={
            "mean_photons_input": float(mean_photons) if r_per_mode is None else None,
            "convention": "xpxp, hbar=2",
            "version": "draft-v0.1",
        },
    )


# ---------------------------------------------------------------------------
# Smoke tests (run as `python -m infra.gbs.gbs_circuit` for a sanity check)
# ---------------------------------------------------------------------------

def _smoke() -> None:
    M = 10
    circ = build_circuit(M=M, mean_photons=5.0, eta=0.5, haar_seed=42)
    assert circ.cov.shape == (2 * M, 2 * M)
    # symmetry
    np.testing.assert_allclose(circ.cov, circ.cov.T, atol=1e-12)
    # PSD (smallest eigenvalue >= 0 - eps)
    w = np.linalg.eigvalsh(circ.cov)
    assert w.min() >= -1e-9, f"covariance not PSD: min eig = {w.min()}"
    # Haar unitarity
    np.testing.assert_allclose(circ.U @ circ.U.conj().T, np.eye(M), atol=1e-9)
    print("smoke OK:", {"M": M, "min_eig": float(w.min()), "max_eig": float(w.max()), "eta": circ.eta})


if __name__ == "__main__":
    _smoke()
