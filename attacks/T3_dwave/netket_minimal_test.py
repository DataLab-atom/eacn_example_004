"""
T3 Attack: Minimal NetKet integration test.

Purpose: verify that NetKet can build the diamond lattice spin glass
Hamiltonian, run VMC with an RBM ansatz, and reach lower energy than
our naive numpy 2nd-order Jastrow on N=16.

Success criterion: RBM achieves rel_err vs ED < 32.84% (numpy 2nd-order).
If yes → NetKet path is viable for the full T3 attack (then upgrade to
deeper MLP / proper 4-body variants).
If no → diagnose and document.

Note: JAX is CPU-only on this machine (no GPU), but JIT should still
speed up the inner loop substantially.
"""

import numpy as np
import jax
import jax.numpy as jnp
import netket as nk
import time
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from fast_tVMC_benchmark import diamond_lattice
from tVMC_jastrow4_integrated import exact_ground_state


def build_netket_diamond(L_perp, L_vert):
    """Build NetKet graph + Hilbert + Hamiltonian for diamond lattice."""
    N, edges = diamond_lattice(L_perp, L_vert)
    rng = np.random.RandomState(42)
    J = rng.uniform(-1, 1, size=len(edges))

    graph = nk.graph.Graph(edges=[list(e) for e in edges], n_nodes=N)
    hilbert = nk.hilbert.Spin(s=0.5, N=N)

    # Build Ising Hamiltonian: H = -sum_(i,j) J_ij σz_i σz_j
    # NetKet's expected sign convention: Ising operator is
    # H_Ising = -sum J_ij σz σz, but check convention.
    # We use LocalOperator to be explicit.
    H = nk.operator.LocalOperator(hilbert, dtype=np.float64)
    sigma_z = [[1.0, 0.0], [0.0, -1.0]]
    for k, (i, j) in enumerate(edges):
        # For spin-1/2, σz has eigenvalues ±1, matching s = ±1
        zz = np.kron(sigma_z, sigma_z)
        H -= J[k] * nk.operator.LocalOperator(hilbert, zz, [i, j])

    return N, edges, J, graph, hilbert, H


def run_netket_vmc(L_perp, L_vert, model_type="RBM", alpha=2,
                    n_samples=512, n_iter=80, learning_rate=0.05,
                    seed=42, verbose=True):
    N, edges, J, graph, hilbert, H = build_netket_diamond(L_perp, L_vert)
    if verbose:
        print(f"  Diamond N={N}, |E|={len(edges)}, model={model_type}, alpha={alpha}")

    # Choose model
    if model_type == "RBM":
        model = nk.models.RBM(alpha=alpha, param_dtype=np.float64)
    elif model_type == "Jastrow":
        model = nk.models.Jastrow(param_dtype=np.float64)
    elif model_type == "MLP":
        model = nk.models.MLP(hidden_dims=[2 * N, N], param_dtype=np.float64)
    else:
        raise ValueError(f"Unknown model: {model_type}")

    # Sampler
    sampler = nk.sampler.MetropolisLocal(hilbert, n_chains=8)

    # Variational state
    vstate = nk.vqs.MCState(sampler, model, n_samples=n_samples, seed=seed)

    # NetKet 3.21 + JAX recent has a pvary incompatibility for VMC_SR
    # and a plum dispatch bug for VMC + SR(). Use plain VMC + Adam
    # (no preconditioner) as a baseline test of the NetKet path.
    optimizer = nk.optimizer.Adam(learning_rate=learning_rate)
    gs = nk.driver.VMC(H, optimizer, variational_state=vstate)

    # Train
    t0 = time.time()
    log = {"E": [], "E_var": []}
    for step in range(n_iter):
        gs.advance()
        E_mean = float(gs.energy.mean.real)
        E_var = float(gs.energy.variance)
        log["E"].append(E_mean)
        log["E_var"].append(E_var)
        if verbose and step % max(1, n_iter // 5) == 0:
            print(f"    iter {step:3d}/{n_iter} | E={E_mean:.4f} | var={E_var:.3f}")
    wall_time = time.time() - t0

    return {
        "N": N, "n_edges": len(edges), "model": model_type,
        "E_final": log["E"][-1],
        "E_var_final": log["E_var"][-1],
        "wall_time_s": wall_time,
        "n_iter": n_iter,
        "log": log,
    }


def main():
    print("=" * 60)
    print("T3 NetKet Minimal Test")
    print("=" * 60)

    repo = Path(__file__).resolve().parent.parent.parent
    out_path = repo / "results" / "T3_netket_minimal.json"

    # Get ED ground state for N=16 baseline
    print("\nED ground truth (N=16):")
    N, edges = diamond_lattice(2, 2)
    rng = np.random.RandomState(42)
    J = rng.uniform(-1, 1, size=len(edges))
    E_ED, gs_state, corr_ED = exact_ground_state(N, edges, J)
    print(f"  E_GS = {E_ED:.4f}, E/edge = {E_ED/len(edges):.3f}")

    # Re-run numpy 2nd-order with fresh-RNG J for fair comparison
    from fast_tVMC_benchmark import run_tvmc_fast
    print("\nRe-running numpy 2nd-order baseline with fresh-RNG J (matching this run):")
    traj_np = run_tvmc_fast(
        N, edges, J,
        gamma_schedule=[(0, 3.0), (5.0, 0.0)],
        n_samples=500, n_steps=20, seed=42)
    NUMPY_2ND_ORDER_E = traj_np[-1]["E"]
    print(f"  Numpy 2nd-order final E = {NUMPY_2ND_ORDER_E:.4f}, "
          f"rel_err = {(NUMPY_2ND_ORDER_E - E_ED)/abs(E_ED):+.2%}")

    # Try NetKet RBM
    print("\nNetKet RBM (alpha=2):")
    rbm_result = run_netket_vmc(2, 2, model_type="RBM", alpha=2,
                                  n_samples=512, n_iter=80)
    print(f"  RBM final E: {rbm_result['E_final']:.4f}, "
          f"rel_err = {(rbm_result['E_final'] - E_ED)/abs(E_ED):+.2%}")
    print(f"  Wall time: {rbm_result['wall_time_s']:.1f}s")

    # Try NetKet Jastrow (2-body for direct comparison)
    print("\nNetKet Jastrow (2-body):")
    j_result = run_netket_vmc(2, 2, model_type="Jastrow",
                                n_samples=512, n_iter=80)
    print(f"  Jastrow final E: {j_result['E_final']:.4f}, "
          f"rel_err = {(j_result['E_final'] - E_ED)/abs(E_ED):+.2%}")
    print(f"  Wall time: {j_result['wall_time_s']:.1f}s")

    # Verdict
    rbm_err = abs(rbm_result['E_final'] - E_ED) / abs(E_ED)
    numpy_err = abs(NUMPY_2ND_ORDER_E - E_ED) / abs(E_ED)
    print("\n" + "=" * 60)
    print("VERDICT")
    print("=" * 60)
    if rbm_err < numpy_err:
        print(f"  ✓ NetKet RBM ({rbm_err:+.2%}) BEATS numpy 2nd-order ({numpy_err:+.2%})")
        print(f"  Improvement: {(numpy_err - rbm_err)*100:+.1f} pp")
        print(f"  → NetKet path IS viable; proceed to scaling test")
    else:
        print(f"  ✗ NetKet RBM ({rbm_err:+.2%}) does NOT beat numpy ({numpy_err:+.2%})")
        print(f"  → Investigate: convergence? sampler? model capacity?")

    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w") as f:
        json.dump({
            "E_ED": E_ED,
            "numpy_2nd_order_ref": NUMPY_2ND_ORDER_E,
            "RBM": rbm_result,
            "Jastrow": j_result,
        }, f, indent=2, default=str)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
