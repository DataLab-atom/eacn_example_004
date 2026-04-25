"""
T3 §H3 quench dynamics: NetKet RBM + TDVP for t-VMC simulation
of D-Wave annealing schedule.

Background: my prior commits matched ground-state energy on diamond
lattice up to N=24. Per King et al. 2025-04-10 comment (arXiv:2504.06283),
this is the EASIEST corner of T3. The actual King claim involves quench
dynamics at t_a = 7-40 ns and 4-point Binder cumulant.

This module:
  1. Builds time-dependent Hamiltonian H(t) = -Σ J s_i s_j - Γ(t) Σ σx_i
  2. Uses NetKet's TDVP driver to evolve RBM(α=4) state from |+⟩^N
     under H(t) for total time t_a (in ns, scaled to dimensionless units)
  3. At t = t_a, computes Edwards-Anderson order parameter ⟨q²⟩
     averaged over disorder realizations
  4. Compares against expected scaling vs King QPU data (TBD)

Status: SKELETON — NetKet TDVP API needs verification with this version.
Initial test on N=8.

Author: claude3
Date: 2026-04-25
"""

import numpy as np
import netket as nk
import netket.experimental as nkx
import time
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from canonical_diamond_v2 import diamond_lattice_v2


def build_quench_hamiltonian(L_perp, L_vert, gamma):
    """H(γ) = -Σ_(i,j) J_ij σz_i σz_j - γ Σ_i σx_i"""
    N, edges = diamond_lattice_v2(L_perp, L_vert)
    rng = np.random.RandomState(42)
    J = rng.uniform(-1, 1, size=len(edges))

    hilbert = nk.hilbert.Spin(s=0.5, N=N)
    H = nk.operator.LocalOperator(hilbert, dtype=np.complex128)

    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]])
    sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]])
    zz = np.kron(sigma_z, sigma_z)

    for k, (i, j) in enumerate(edges):
        H -= J[k] * nk.operator.LocalOperator(hilbert, zz, [i, j])
    for i in range(N):
        H -= gamma * nk.operator.LocalOperator(hilbert, sigma_x, [i])

    return N, edges, J, hilbert, H


def annealing_schedule(t, t_a, gamma_max=3.0):
    """Linear ramp γ: γ_max -> 0 over [0, t_a]."""
    return gamma_max * max(0.0, 1.0 - t / t_a)


def edwards_anderson_q2(samples):
    """⟨q²⟩ = (1/N²) Σ_i ⟨σz_i⟩² where ⟨σz_i⟩ is sample mean."""
    sigma_z_means = samples.mean(axis=0)  # shape (N,)
    return float(np.mean(sigma_z_means ** 2))


def run_quench_n8_minimal():
    """Minimal smoke test: N=8 (L=2,Lv=1), t_a = 7 ns dimensionless."""
    print("=" * 60)
    print("T3 §H3: NetKet TDVP quench dynamics (smoke test N=8)")
    print("=" * 60)

    L_perp, L_vert = 2, 1  # N=8

    # Build at γ_max for initial state preparation
    gamma_max = 3.0
    N, edges, J, hilbert, H_init = build_quench_hamiltonian(
        L_perp, L_vert, gamma_max)
    print(f"  N={N}, |E|={len(edges)}")

    # Initial state: ground state of -γ Σ σx_i is uniform superposition |+⟩^N
    # Use RBM as ansatz; train briefly at γ_max to set state ≈ |+⟩^N

    model = nk.models.RBM(alpha=4, param_dtype=np.complex128)
    sampler = nk.sampler.MetropolisLocal(hilbert, n_chains=8)
    vstate = nk.vqs.MCState(sampler, model, n_samples=512, seed=42)

    # Quick prep at γ_max
    print("\n  Phase 1: prepare initial state at γ_max...")
    optimizer = nk.optimizer.Adam(learning_rate=0.05)
    gs = nk.driver.VMC(H_init, optimizer, variational_state=vstate)
    t0 = time.time()
    for step in range(40):
        gs.advance()
    t_prep = time.time() - t0
    E_prep = float(gs.energy.mean.real)
    print(f"    prep done in {t_prep:.1f}s, E = {E_prep:.4f}")

    # Annealing: linear γ ramp
    t_a = 7.0  # dimensionless time units (7 ns scale)
    n_t_steps = 50
    dt = t_a / n_t_steps
    gamma_trajectory = []
    energy_trajectory = []
    q2_trajectory = []

    print(f"\n  Phase 2: anneal γ_max -> 0 over t_a = {t_a}, dt = {dt:.3f}")
    print(f"  (Approximated as γ-quench using stepwise VMC re-equilibration —")
    print(f"   not a true TDVP. Real attack needs nkx.driver.TDVP integration.)")
    t0 = time.time()
    for step in range(n_t_steps + 1):
        t = step * dt
        gamma = annealing_schedule(t, t_a, gamma_max)
        # Update Hamiltonian with new γ
        _, _, _, _, H_t = build_quench_hamiltonian(L_perp, L_vert, gamma)
        gs._H = H_t  # surgical update; not officially supported but works
        gs.advance()  # one VMC step at new γ

        E_t = float(gs.energy.mean.real)
        # Sample σz to get q² estimator
        samples = vstate.samples.reshape(-1, N)
        q2 = edwards_anderson_q2(np.asarray(samples))

        gamma_trajectory.append(gamma)
        energy_trajectory.append(E_t)
        q2_trajectory.append(q2)
        if step % max(1, n_t_steps // 5) == 0:
            print(f"    t = {t:5.2f}  γ = {gamma:5.2f}  E = {E_t:+.3f}  ⟨q²⟩ = {q2:.3f}")

    t_quench = time.time() - t0
    print(f"\n  Quench dynamics: {t_quench:.1f}s wall, "
          f"final ⟨q²⟩ = {q2_trajectory[-1]:.4f}")

    # Save
    repo = Path(__file__).resolve().parent.parent.parent
    out_path = repo / "results" / "T3_v2_quench_n8_smoke.json"
    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w") as f:
        json.dump({
            "N": N, "L_perp": L_perp, "L_vert": L_vert,
            "t_a": t_a, "n_t_steps": n_t_steps,
            "alpha": 4,
            "gamma_trajectory": gamma_trajectory,
            "energy_trajectory": energy_trajectory,
            "q2_trajectory": q2_trajectory,
            "wall_prep_s": t_prep,
            "wall_quench_s": t_quench,
            "method": "stepwise-VMC-quench (not full TDVP)",
            "caveat": "NetKet TDVP driver compatibility issues; this is a sub-baseline",
        }, f, indent=2, default=str)
    print(f"  Saved: {out_path}")
    print("\n" + "=" * 60)
    print("STATUS: smoke test only — NOT a valid §H3 attack data point")
    print("Real attack requires:")
    print("  - Disorder average over many J realizations")
    print("  - Multiple t_a values from 7 ns to 40 ns")
    print("  - Larger N (54, 128, ideally 567)")
    print("  - Comparison vs King QPU / Mauron-Carleo published data")
    print("  - True TDVP integration (not stepwise VMC)")
    print("=" * 60)


if __name__ == "__main__":
    run_quench_n8_minimal()
