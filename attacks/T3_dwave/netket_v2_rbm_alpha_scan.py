"""
T3 §D5 v2: NetKet RBM with α=2/4/8 on canonical_diamond_v2.

Re-runs the NetKet test on the §D5 canonical spec (lexicographic
site indexing + sorted edges), then scans RBM expressivity α=2/4/8
to address claude7's reviewer ping that α=2 may not cross the
Mauron-Carleo 7% fidelity threshold.

Output: results/T3/v2_netket_rbm_alpha_scan.json
"""

import numpy as np
import netket as nk
import time
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from canonical_diamond_v2 import diamond_lattice_v2


def build_v2(L_perp, L_vert):
    N, edges = diamond_lattice_v2(L_perp, L_vert)
    rng = np.random.RandomState(42)
    J = rng.uniform(-1, 1, size=len(edges))

    hilbert = nk.hilbert.Spin(s=0.5, N=N)
    H = nk.operator.LocalOperator(hilbert, dtype=np.float64)
    sigma_z = [[1.0, 0.0], [0.0, -1.0]]
    zz = np.kron(sigma_z, sigma_z)
    for k, (i, j) in enumerate(edges):
        H -= J[k] * nk.operator.LocalOperator(hilbert, zz, [i, j])
    return N, edges, J, hilbert, H


def ed_v2(N, edges, J):
    """Brute force ED for N <= 18."""
    best_E = np.inf
    for bits in range(2 ** N):
        s = np.array([1.0 if (bits >> i) & 1 else -1.0 for i in range(N)])
        E = -sum(J[k] * s[i] * s[j] for k, (i, j) in enumerate(edges))
        if E < best_E:
            best_E = E
    return float(best_E)


def run_rbm(L_perp, L_vert, alpha, n_samples=512, n_iter=120, lr=0.05, seed=42):
    N, edges, J, hilbert, H = build_v2(L_perp, L_vert)
    model = nk.models.RBM(alpha=alpha, param_dtype=np.float64)
    sampler = nk.sampler.MetropolisLocal(hilbert, n_chains=8)
    vstate = nk.vqs.MCState(sampler, model, n_samples=n_samples, seed=seed)
    optimizer = nk.optimizer.Adam(learning_rate=lr)
    gs = nk.driver.VMC(H, optimizer, variational_state=vstate)
    t0 = time.time()
    es, vs = [], []
    for step in range(n_iter):
        gs.advance()
        es.append(float(gs.energy.mean.real))
        vs.append(float(gs.energy.variance))
    return {
        "N": N, "alpha": alpha,
        "E_final": es[-1], "E_var_final": vs[-1],
        "wall_time_s": time.time() - t0,
        "n_iter": n_iter,
    }


def main():
    print("=" * 60)
    print("T3 §D5 v2: NetKet RBM α-scan on canonical_diamond_v2")
    print("=" * 60)

    repo = Path(__file__).resolve().parent.parent.parent
    out_path = repo / "results" / "T3_v2_netket_rbm_alpha_scan.json"

    L_perp, L_vert = 2, 2  # N=16
    N, edges, J, _, _ = build_v2(L_perp, L_vert)
    print(f"\nv2 N=16: edges_md5 = (computed in canonical_diamond_v2.main())")
    print(f"  |E| = {len(edges)}")

    # ED ground truth on v2 spec
    print("\nED brute force on v2 spec (N=16):")
    t0 = time.time()
    E_GS = ed_v2(N, edges, J)
    print(f"  E_GS = {E_GS:.6f}, E/edge = {E_GS/len(edges):.4f}  ({time.time()-t0:.1f}s)")

    # RBM scan
    results = {"E_GS": E_GS, "rbm_runs": {}}
    for alpha in [2, 4, 8]:
        print(f"\nRBM alpha = {alpha}:")
        r = run_rbm(L_perp, L_vert, alpha=alpha, n_samples=512,
                    n_iter=120, lr=0.05, seed=42)
        rel_err = (r["E_final"] - E_GS) / abs(E_GS)
        r["rel_err_vs_ED"] = rel_err
        print(f"  E_final = {r['E_final']:.4f}, "
              f"rel_err = {rel_err:+.2%}, "
              f"wall = {r['wall_time_s']:.1f}s")
        results["rbm_runs"][f"alpha={alpha}"] = r

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY (v2 spec, N=16)")
    print("=" * 60)
    print(f"  ED ground truth: E_GS = {E_GS:.4f}")
    print(f"  Mauron-Carleo target: rel_err < 7%")
    crossed = []
    for k, r in results["rbm_runs"].items():
        rel_err = abs(r["rel_err_vs_ED"])
        cross = "✓" if rel_err < 0.07 else "✗"
        print(f"  RBM {k}: err = {rel_err:.2%}  ({cross})  [{r['wall_time_s']:.1f}s]")
        if rel_err < 0.07:
            crossed.append(k)

    if crossed:
        print(f"\n  ✓ Threshold crossed: {crossed}")
    else:
        print(f"\n  ✗ None below 7%; deeper net or longer training needed")

    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
