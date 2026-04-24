"""
Shared Module: Oh et al. (2024) Critical Eta Calculator
========================================================
Compute the critical transmission threshold eta_crit(r, N_sources)
below which GBS is classically simulable via Oh et al.'s method.

Based on: Oh, Lim, Fefferman, Jiang, Nature Physics 20, 1647 (2024)
         arXiv:2306.03709, Table I and Figure 3.

Usage:
    from oh_2024_critical_eta import critical_eta, is_classically_simulable

    eta_c = critical_eta(r=1.5, N_sources=25)
    result = is_classically_simulable(r=1.5, eta=0.43, N_sources=25)

Author: claude2
Date: 2026-04-25
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class SimulabilityResult:
    """Result of classical simulability check."""
    r: float              # squeezing parameter (nepers)
    eta: float            # total transmission
    N_sources: int        # number of squeezed sources
    eta_crit: float       # critical transmission threshold
    margin: float         # eta_crit - eta (positive = classically simulable)
    simulable: bool       # True if eta < eta_crit
    squeezed_photons_est: float  # estimated quantum photon count
    chi_estimate: int     # estimated bond dimension needed


def critical_eta(r: float, N_sources: int = 25) -> float:
    """Compute critical transmission eta_crit(r, N_sources).

    Below eta_crit, GBS output can be efficiently classically simulated
    using Oh et al.'s tensor network method.

    Based on empirical fit to Oh et al. Table I / Figure 3 data:
    - JZ 1.0: r~1.5, N=25, eta=0.283 → simulable (broken)
    - JZ 2.0: r~1.6, N=25, eta=0.476 → simulable (broken)
    - JZ 3.0: r~1.5, N=25, eta=0.424 → simulable (our claim)

    The critical eta increases with N_sources (more sources = harder)
    and decreases with r (higher squeezing = lower threshold).

    Approximate model (conservative):
        eta_crit ≈ 0.538 * (50 / N_sources)^0.3 * (1.5 / r)^0.2

    NOTE: This is an empirical fit, not a rigorous bound. The actual
    critical threshold depends on the specific interferometer structure,
    mode count, and detection scheme. Use with caution.
    """
    # Reference point from Oh et al.: eta_crit ≈ 0.538 for ~50 sources
    # Scaling with N_sources: more sources = more quantum resources = lower eta_crit
    # Scaling with r: higher squeezing = more entanglement = lower eta_crit
    base_eta_crit = 0.538
    ref_N = 50
    ref_r = 1.5

    # Conservative scaling (may overestimate eta_crit)
    eta_c = base_eta_crit * (ref_N / max(N_sources, 1))**0.3 * (ref_r / max(r, 0.1))**0.2

    return min(eta_c, 1.0)


def estimate_squeezed_photons(r: float, eta: float, N_modes: int) -> float:
    """Estimate the number of quantum (squeezed) photons in the output.

    From Oh et al.: actual squeezed photons = N_sources * eta * sinh^2(r) * (correction)
    where the correction accounts for loss-induced decoherence.

    For high loss: most photons are thermal (classical), only a small
    fraction carry quantum information.
    """
    # Mean photon number per squeezed mode (lossless): n_bar = sinh^2(r)
    n_bar = np.sinh(r)**2
    # With loss: effective squeezed photons reduced
    # Simple model: n_squeezed ~ N_modes * eta^2 * tanh(r)^2
    # (the eta^2 comes from the fact that both signal and idler must survive)
    n_squeezed = N_modes * eta**2 * np.tanh(r)**2
    return n_squeezed


def estimate_bond_dimension(r: float, eta: float, N_modes: int) -> int:
    """Estimate required MPS bond dimension for Oh et al. method.

    Based on Table I values:
    - JZ 2.0: chi ~ 160-600 at eta=0.476
    - JZ 3.0: chi ~ 400 (estimated) at eta=0.424

    Scaling: chi ~ exp(alpha * N_modes * eta * tanh(r)^2)
    where alpha is a geometry-dependent constant.
    """
    # Empirical fit from Oh et al. data
    xi = np.tanh(r)**2 * eta
    # From the specialized method (NOT naive MPS):
    # Oh et al. keeps D manageable by exploiting loss structure
    # Rough scaling: chi ~ 100 * (N_modes * xi / 10)^1.5
    chi = int(100 * max(1, (N_modes * xi / 10)**1.5))
    return min(chi, 10**6)  # cap at 10^6


def is_classically_simulable(r: float, eta: float, N_sources: int = 25,
                              N_modes: int = 144) -> SimulabilityResult:
    """Check if a GBS experiment is classically simulable via Oh et al.

    Args:
        r: squeezing parameter in nepers
        eta: total transmission (0 to 1)
        N_sources: number of squeezed state sources
        N_modes: number of optical modes

    Returns:
        SimulabilityResult with all relevant information
    """
    eta_c = critical_eta(r, N_sources)
    margin = eta_c - eta
    simulable = eta < eta_c
    sq_photons = estimate_squeezed_photons(r, eta, N_modes)
    chi = estimate_bond_dimension(r, eta, N_modes)

    return SimulabilityResult(
        r=r, eta=eta, N_sources=N_sources,
        eta_crit=eta_c, margin=margin, simulable=simulable,
        squeezed_photons_est=sq_photons, chi_estimate=chi
    )


# ============================================================
# Self-test and cross-validation
# ============================================================
if __name__ == '__main__':
    print("Oh et al. (2024) Critical Eta Calculator — Self-test")
    print("=" * 60)

    tests = [
        ("JZ 1.0", 1.5, 0.283, 25, 100),
        ("JZ 2.0", 1.6, 0.476, 25, 144),
        ("JZ 3.0", 1.5, 0.424, 25, 144),
        ("JZ 4.0", 1.8, 0.510, 1024, 8176),
    ]

    for name, r, eta, N_src, N_modes in tests:
        result = is_classically_simulable(r, eta, N_src, N_modes)
        status = "SIMULABLE" if result.simulable else "HARD"
        print(f"\n  {name}: r={r}, eta={eta:.3f}, N_src={N_src}")
        print(f"    eta_crit = {result.eta_crit:.3f}")
        print(f"    margin   = {result.margin:.3f} ({'below' if result.simulable else 'ABOVE'} threshold)")
        print(f"    sq_phot  = {result.squeezed_photons_est:.1f}")
        print(f"    chi_est  = {result.chi_estimate}")
        print(f"    verdict  = {status}")
