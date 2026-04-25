"""
T3 §H3: piecewise-TDVP quench dynamics on canonical_diamond_v2.

Builds on commit 0faf710 which verified the NetKet 3.21 TDVP API
on a static H. This module implements a γ-ramp by piecewise-static
TDVP: at each window the Hamiltonian is held fixed, then rebuilt at
the next γ value. As n_pieces grows, this approaches the true
time-dependent Schrödinger equation.

Outputs:
  - ⟨σz_i⟩ trajectories
  - ⟨q²⟩ Edwards-Anderson order parameter at each time slice
  - Energy expectation under instantaneous H (for sanity)

Status: FIRST real quench dynamics attempt for §H3. Not yet at
King's reported sizes (N≥72) — first verifies behavior at N=8/16
where I can sanity-check against intuition (q² should go from 0
toward something nonzero as Γ→0 if the system orders).
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


def build_H(hilbert, edges, J, gamma, dtype=np.complex128):
    """H(γ) = -Σ_(i,j) J_ij σz_i σz_j - γ Σ_i σx_i"""
    H = nk.operator.LocalOperator(hilbert, dtype=dtype)
    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]])
    sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]])
    zz = np.kron(sigma_z, sigma_z)
    for k, (i, j) in enumerate(edges):
        H -= J[k] * nk.operator.LocalOperator(hilbert, zz, [i, j])
    for i in range(hilbert.size):
        H -= gamma * nk.operator.LocalOperator(hilbert, sigma_x, [i])
    return H


def init_plus_state(vstate, hilbert, n_steps_init=60, lr=0.05):
    """Initialize variational state to approximately |+⟩^N
    by VMC-minimizing -Σ σx_i (whose ground state is |+⟩^N)."""
    H_x = nk.operator.LocalOperator(hilbert, dtype=np.complex128)
    sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]])
    for i in range(hilbert.size):
        H_x -= nk.operator.LocalOperator(hilbert, sigma_x, [i])
    optimizer = nk.optimizer.Adam(learning_rate=lr)
    gs = nk.driver.VMC(H_x, optimizer, variational_state=vstate)
    for _ in range(n_steps_init):
        gs.advance()


def compute_q2(vstate, hilbert):
    """⟨q²⟩ = (1/N) Σ_i ⟨σz_i⟩²  (one-replica EA approximation).

    Note: true Edwards-Anderson uses two-replica overlap.
    For single-state simulation, the proxy is mean square magnetization.
    """
    N = hilbert.size
    q2_total = 0.0
    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]])
    for i in range(N):
        op = nk.operator.LocalOperator(hilbert, sigma_z, [i], dtype=np.complex128)
        m_i = float(vstate.expect(op).mean.real)
        q2_total += m_i ** 2
    return q2_total / N


def run_quench(L_perp, L_vert, t_a=7.0, gamma_max=3.0,
               n_pieces=20, dt_per_piece=0.05,
               n_samples=512, alpha=4, seed=42,
               compute_q2_every=5):
    rng = np.random.RandomState(42)
    N, edges = diamond_lattice_v2(L_perp, L_vert)
    J = rng.uniform(-1, 1, size=len(edges))
    print(f"  Diamond N={N}, |E|={len(edges)}, t_a={t_a}, n_pieces={n_pieces}")

    hilbert = nk.hilbert.Spin(s=0.5, N=N)
    model = nk.models.RBM(alpha=alpha, param_dtype=np.complex128)
    sampler = nk.sampler.MetropolisLocal(hilbert, n_chains=8)
    vstate = nk.vqs.MCState(sampler, model, n_samples=n_samples, seed=seed)

    # Initial state: |+⟩^N (start of anneal, all spins maximally x-polarized)
    print("\n  Phase 1: initialize to |+⟩^N (VMC against -Σ σx_i)")
    t0 = time.time()
    init_plus_state(vstate, hilbert, n_steps_init=40, lr=0.05)
    print(f"    init done in {time.time() - t0:.1f}s")

    # Anneal: piecewise-static TDVP
    print("\n  Phase 2: piecewise TDVP quench")
    dt_piece = t_a / n_pieces
    n_inner = max(1, int(round(dt_piece / dt_per_piece)))
    dt_actual = dt_piece / n_inner
    print(f"    dt_piece = {dt_piece:.3f}, "
          f"n_inner = {n_inner}, dt_actual = {dt_actual:.4f}")

    trajectory = []
    t0 = time.time()
    for piece in range(n_pieces + 1):
        t_now = piece * dt_piece
        gamma = gamma_max * max(0.0, 1.0 - t_now / t_a)
        H_now = build_H(hilbert, edges, J, gamma)

        if piece > 0:  # advance from previous piece end
            ode_solver = nkx.dynamics.RK4(dt=dt_actual)
            td = nkx.driver.TDVP(
                operator=H_now,
                variational_state=vstate,
                ode_solver=ode_solver,
                propagation_type="real",
            )
            td.advance(dt_piece)

        # Observables (subset for speed)
        E_now = float(vstate.expect(H_now).mean.real)
        q2 = None
        if piece % compute_q2_every == 0 or piece == n_pieces:
            q2 = compute_q2(vstate, hilbert)
        trajectory.append({"piece": piece, "t": t_now, "gamma": gamma,
                           "E": E_now, "q2": q2})
        if piece % max(1, n_pieces // 5) == 0:
            print(f"    piece {piece:2d}/{n_pieces}  t={t_now:5.2f}  "
                  f"γ={gamma:5.2f}  E={E_now:+.3f}  "
                  f"q² = {q2 if q2 is not None else 'skipped'}")

    wall_time = time.time() - t0
    return {
        "N": N, "n_edges": len(edges), "alpha": alpha,
        "t_a": t_a, "gamma_max": gamma_max,
        "n_pieces": n_pieces, "dt_per_piece": dt_per_piece,
        "trajectory": trajectory, "wall_time_s": wall_time,
    }


def main():
    print("=" * 60)
    print("T3 §H3: piecewise-TDVP quench dynamics on N=8")
    print("=" * 60)

    repo = Path(__file__).resolve().parent.parent.parent
    out = repo / "results" / "T3_v2_tdvp_quench_n8.json"

    r = run_quench(L_perp=2, L_vert=1,  # N=8
                    t_a=7.0, gamma_max=3.0,
                    n_pieces=12, dt_per_piece=0.05)

    print(f"\n  Wall time: {r['wall_time_s']:.1f}s")
    final = r["trajectory"][-1]
    print(f"  Final: γ={final['gamma']:.2f} E={final['E']:.3f} q²={final['q2']:.4f}")

    out.parent.mkdir(exist_ok=True)
    with open(out, "w") as f:
        json.dump(r, f, indent=2, default=str)
    print(f"\n  Saved: {out}")


if __name__ == "__main__":
    main()
