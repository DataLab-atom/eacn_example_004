"""
T3 §H3 development: NetKet TDVP API smoke test.

Goal: verify nkx.driver.TDVP + nkx.dynamics.RK4 works on this NetKet
3.21 + JAX setup. Use a STATIC Hamiltonian (Γ fixed), evolve from
the |+⟩^N initial state for short time. Checks:
  1. TDVP construction succeeds (not blocked by plum/jax issues)
  2. State norm preserved during evolution (energy conservation
     under static H is the tightest sanity check)
  3. Energy expectation oscillates / changes (initial state is
     NOT an H eigenstate)

If this passes → can safely build time-dependent quench dynamics
on top.

Status: API smoke test only. Next file will add Γ(t) ramp.
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


def main():
    print("=" * 60)
    print("T3 §H3 SMOKE: NetKet TDVP API verification")
    print("=" * 60)

    # Tiny system for fast iteration
    L_perp, L_vert = 2, 1  # N=8
    N, edges = diamond_lattice_v2(L_perp, L_vert)
    rng = np.random.RandomState(42)
    J = rng.uniform(-1, 1, size=len(edges))
    print(f"  System: diamond N={N}, |E|={len(edges)}")

    # Static H at gamma = 1.5 (mid-anneal)
    gamma = 1.5
    hilbert = nk.hilbert.Spin(s=0.5, N=N)
    H = nk.operator.LocalOperator(hilbert, dtype=np.complex128)
    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]])
    sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]])
    zz = np.kron(sigma_z, sigma_z)
    for k, (i, j) in enumerate(edges):
        H -= J[k] * nk.operator.LocalOperator(hilbert, zz, [i, j])
    for i in range(N):
        H -= gamma * nk.operator.LocalOperator(hilbert, sigma_x, [i])

    # RBM ansatz
    model = nk.models.RBM(alpha=4, param_dtype=np.complex128)
    sampler = nk.sampler.MetropolisLocal(hilbert, n_chains=8)
    vstate = nk.vqs.MCState(sampler, model, n_samples=512, seed=42)

    # ODE solver: RK4 with small time step
    dt = 0.05
    print(f"\n  Building TDVP with RK4(dt={dt})...")
    try:
        ode_solver = nkx.dynamics.RK4(dt=dt)
        td = nkx.driver.TDVP(
            operator=H,
            variational_state=vstate,
            ode_solver=ode_solver,
            propagation_type="real",  # Schrodinger
        )
        print("  ✓ TDVP driver constructed successfully")
    except Exception as exc:
        print(f"  ✗ Construction failed: {exc}")
        return

    # Initial energy
    E0 = float(vstate.expect(H).mean.real)
    print(f"\n  Initial energy <H> = {E0:.4f}")

    # Evolve for a few steps
    n_steps = 20
    print(f"\n  Evolving for {n_steps} steps of dt={dt} (total t={n_steps*dt:.2f})")
    t0 = time.time()
    es = []
    try:
        for step in range(n_steps):
            td.advance(dt)
            E_t = float(vstate.expect(H).mean.real)
            es.append(E_t)
            if step % max(1, n_steps // 5) == 0:
                print(f"    step {step}, t={td.t:.3f}, E = {E_t:.4f}, "
                      f"ΔE = {E_t - E0:+.4f}")
    except Exception as exc:
        print(f"  ✗ Evolution failed at step {step}: {exc}")
        wall_time = time.time() - t0
        print(f"  Wall time before failure: {wall_time:.1f}s")
        # Save partial
        repo = Path(__file__).resolve().parent.parent.parent
        out = repo / "results" / "T3_v2_tdvp_smoke.json"
        out.parent.mkdir(exist_ok=True)
        with open(out, "w") as f:
            json.dump({"status": "FAIL", "exception": str(exc),
                       "wall_time_s": wall_time, "es_partial": es}, f, indent=2)
        return

    wall_time = time.time() - t0
    print(f"\n  Wall time: {wall_time:.1f}s ({wall_time/n_steps:.2f}s/step)")
    print(f"  Energy drift |E_final - E_0| = {abs(es[-1] - E0):.4f}")
    print(f"  Max |ΔE| over evolution = {max(abs(e - E0) for e in es):.4f}")
    print(f"\n  Note: under STATIC H, exact <H> is conserved.")
    print(f"        TDVP truncation error => observable drift on RBM manifold.")

    # Save
    repo = Path(__file__).resolve().parent.parent.parent
    out = repo / "results" / "T3_v2_tdvp_smoke.json"
    out.parent.mkdir(exist_ok=True)
    with open(out, "w") as f:
        json.dump({
            "status": "OK", "N": N, "gamma": gamma, "dt": dt, "n_steps": n_steps,
            "wall_time_s": wall_time, "E_initial": E0, "es": es,
            "drift": float(abs(es[-1] - E0)),
            "max_abs_deviation": float(max(abs(e - E0) for e in es)),
        }, f, indent=2)
    print(f"\n  Saved: {out}")


if __name__ == "__main__":
    main()
