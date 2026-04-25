"""
Robustness scan §E3 — perturb hyperparameters at alpha=16 N=48 J=43 BREAK regime.

AGENTS.md §E3 requires "扰动超参 ±10%、±50%, 结果不应翻转".

Baseline: P1 hedge alpha=16 N=48 J=43 -> rel_err = 6.39% (BREAK).

Perturbations tested (single-J-seed, 1 run each):
  - lr ±10% / ±50%: 0.005, 0.009, 0.01 (baseline), 0.011, 0.015
  - n_samples ±50%: 1024, 2048 (baseline), 3072, 4096

Verdict: result is robust if all perturbations stay BREAK (rel_err <= 7%).

Compute estimate: ~5-8 min per run x ~9 runs = ~45-70 min total.

Output: results/T3_v2_robustness_E3_alpha16_N48_J43.json
"""

import numpy as np
import netket as nk
import time
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from canonical_diamond_v2 import diamond_lattice_v2

DMRG_TRUTH_N48_J43 = -29.279701  # from P1 hedge JSON


def build_v2_with_seed(L_perp, L_vert, J_seed):
    N, edges = diamond_lattice_v2(L_perp, L_vert)
    rng = np.random.RandomState(J_seed)
    J = rng.uniform(-1, 1, size=len(edges))

    hilbert = nk.hilbert.Spin(s=0.5, N=N)
    H = nk.operator.LocalOperator(hilbert, dtype=np.float64)
    sigma_z = [[1.0, 0.0], [0.0, -1.0]]
    zz = np.kron(sigma_z, sigma_z)
    for k, (i, j) in enumerate(edges):
        H -= J[k] * nk.operator.LocalOperator(hilbert, zz, [i, j])
    return N, edges, J, hilbert, H


def run_perturbation(L_perp, L_vert, alpha, n_samples, n_iter, lr, J_seed, init_seed=0):
    N, edges, J, hilbert, H = build_v2_with_seed(L_perp, L_vert, J_seed)
    model = nk.models.RBM(alpha=alpha, param_dtype=np.float64)
    sampler = nk.sampler.MetropolisLocal(hilbert, n_chains=8)
    vstate = nk.vqs.MCState(sampler, model, n_samples=n_samples, seed=init_seed)
    optimizer = nk.optimizer.Adam(learning_rate=lr)
    gs = nk.driver.VMC(H, optimizer, variational_state=vstate)

    t0 = time.time()
    for step in range(n_iter):
        gs.advance()
    wall = time.time() - t0
    E_final = float(gs.energy.mean.real)
    rel_err = abs(E_final - DMRG_TRUTH_N48_J43) / abs(DMRG_TRUTH_N48_J43)
    verdict = "BREAK" if rel_err <= 0.07 else "FAIL"
    return {
        "lr": lr, "n_samples": n_samples, "n_iter": n_iter,
        "E_final": E_final, "rel_err": rel_err,
        "verdict": verdict, "wall_s": wall,
    }


def main():
    print("=" * 60)
    print("Robustness scan §E3 — alpha=16 N=48 J=43 BREAK regime")
    print("=" * 60)

    repo = Path(__file__).resolve().parent.parent.parent
    out_path = repo / "results" / "T3_v2_robustness_E3_alpha16_N48_J43.json"

    L_perp, L_vert = 2, 6
    alpha = 16
    J_seed = 43

    # Baseline params (from P1 hedge commit f1d09c9)
    base_lr = 0.01
    base_n_samples = 2048
    n_iter = 250  # match P1 hedge

    perturbations = [
        # (label, lr, n_samples)
        ("baseline",        0.01,  2048),
        ("lr_-50%",         0.005, 2048),
        ("lr_-10%",         0.009, 2048),
        ("lr_+10%",         0.011, 2048),
        ("lr_+50%",         0.015, 2048),
        ("n_samples_-50%",  0.01,  1024),
        ("n_samples_+50%",  0.01,  3072),
        ("n_samples_+100%", 0.01,  4096),
    ]

    print(f"DMRG truth N=48 J=43: {DMRG_TRUTH_N48_J43}")
    print(f"Baseline P1 hedge rel_err = 6.39% (BREAK)")
    print(f"Perturbations: {len(perturbations)}")
    print("")

    results = []
    for label, lr, n_samples in perturbations:
        print(f"--- {label}: lr={lr}, n_samples={n_samples} ---")
        r = run_perturbation(L_perp, L_vert, alpha=alpha,
                             n_samples=n_samples, n_iter=n_iter, lr=lr,
                             J_seed=J_seed)
        r["label"] = label
        results.append(r)
        print(f"  E={r['E_final']:.4f}, rel_err={r['rel_err']*100:.3f}%, "
              f"verdict={r['verdict']}, wall={r['wall_s']:.1f}s")
        print("")

    n_break = sum(1 for r in results if r["verdict"] == "BREAK")
    n_total = len(results)

    summary = {
        "scan": "E3 robustness — alpha=16 N=48 J=43 BREAK regime",
        "DMRG_truth": DMRG_TRUTH_N48_J43,
        "baseline_P1_rel_err": 0.06394928,
        "alpha": alpha, "N": 48, "J_seed": J_seed, "n_iter": n_iter,
        "perturbations": results,
        "n_break_under_perturbation": n_break,
        "n_total": n_total,
        "robust": n_break == n_total,
        "AGENTS_E3_compliance": "PASS" if n_break == n_total else "FAIL",
    }

    out_path.write_text(json.dumps(summary, indent=2))

    print("=" * 60)
    print(f"Robustness scan §E3 verdict:")
    print(f"  {n_break}/{n_total} perturbations preserve BREAK")
    print(f"  AGENTS.md §E3 compliance: {summary['AGENTS_E3_compliance']}")
    print(f"Saved: {out_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
