"""
Alternative ansatz attack on T3 N=72: Jastrow + MLP test.

Per §A5.3 future-work bound: tests whether the method-class intrinsic-limit
ridge at alpha~16 is RBM-specific (mechanism iii) or NQS-class-wide.

Tests two NetKet ansatz alternatives on N=72 J seeds 42-46 (where RBM
alpha=16 gave 1/5 BREAK in P3 hedge):
  1. Jastrow: psi(s) = exp(sum_{i!=j} s_i W_ij s_j) — symmetric W
  2. MLP: multi-layer perceptron with hidden_dims=(2N, 2N) — different
     architecture from RBM

Verdict matrix:
  - If Jastrow OR MLP gets BREAK on any seed where RBM alpha=16 FAILed:
    mechanism (iii) RBM ansatz class intrinsic LIKELY (boundary is
    method-class-wide, not RBM-specific) — STRENGTHENS intrinsic-limit
    ridge framing
  - If Jastrow + MLP both also FAIL on the same seeds: boundary is
    NQS-class-wide pathology, not RBM-specific
  - If alternatives BREAK where RBM FAILED: RBM-specific failure;
    intrinsic-limit ridge framing weakens

DMRG truth N=72 reuse: claude7 9b274dc, edges_md5=93c0312e4ce75a78f4b7e523dbe84742.

Compute estimate: ~10-15 min/seed for Jastrow, ~15-25 min/seed for MLP
(simpler models converge faster than RBM alpha=16). Total ~2-4h for 5 seeds
each ansatz. Run sequentially.

Output: results/T3_v2_alt_ansatz_jastrow_mlp_N72.json
"""

import numpy as np
import netket as nk
import time
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from canonical_diamond_v2 import diamond_lattice_v2

DMRG_TRUTHS_N72 = {
    42: -46.382921,
    43: -46.419882,
    44: -49.192424,
    45: -50.882652,
    46: -46.833057,
}

# RBM alpha=16 prior (P3 hedge commit 4509c39)
RBM_ALPHA16_N72_PRIOR = {
    42: -44.4470,  # +4.17% BREAK
    43: -38.7581,  # +16.51% FAIL
    44: -36.4599,  # +25.88% FAIL
    45: -37.5259,  # +26.25% FAIL
    46: -43.1048,  # +7.96% FAIL
}


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


def run_alt_ansatz(model_factory, ansatz_label, L_perp, L_vert, n_samples,
                   n_iter, lr, J_seed, init_seed=0):
    N, edges, J, hilbert, H = build_v2_with_seed(L_perp, L_vert, J_seed)
    model = model_factory(N)
    sampler = nk.sampler.MetropolisLocal(hilbert, n_chains=8)
    vstate = nk.vqs.MCState(sampler, model, n_samples=n_samples, seed=init_seed)
    optimizer = nk.optimizer.Adam(learning_rate=lr)
    gs = nk.driver.VMC(H, optimizer, variational_state=vstate)

    t0 = time.time()
    es = []
    for step in range(n_iter):
        gs.advance()
        E_mean = float(gs.energy.mean.real)
        es.append(E_mean)
        if step % max(1, n_iter // 10) == 0:
            print(f"    iter {step:3d}/{n_iter} | E={E_mean:.4f}")
    wall = time.time() - t0

    E_final = es[-1]
    DMRG = DMRG_TRUTHS_N72[J_seed]
    rel_err = abs(E_final - DMRG) / abs(DMRG)
    verdict = "BREAK" if rel_err <= 0.07 else "FAIL"

    return {
        "ansatz": ansatz_label,
        "J_seed": J_seed,
        "E_final": E_final,
        "DMRG": DMRG,
        "rel_err": rel_err,
        "verdict": verdict,
        "wall_s": wall,
        "n_iter": n_iter,
        "n_samples": n_samples,
        "lr": lr,
    }


def jastrow_factory(N):
    return nk.models.Jastrow(param_dtype=np.float64)


def mlp_factory(N):
    # Hidden layers 2N each — gives ~(2N)^2 + 2 * 2N parameters,
    # comparable scale to RBM alpha=16 (alpha * N^2 = 16 * N^2 = 16 * 5184 = ~83k for N=72)
    # MLP with 2N=144 hidden gives 144*144 + 144*72 + 144 ~= 31k params
    return nk.models.MLP(
        hidden_dims=(2 * N, 2 * N),
        param_dtype=np.float64,
    )


def main():
    print("=" * 60)
    print("Alt-ansatz attack T3 N=72: Jastrow + MLP")
    print("=" * 60)

    repo = Path(__file__).resolve().parent.parent.parent
    out_path = repo / "results" / "T3_v2_alt_ansatz_jastrow_mlp_N72.json"

    L_perp, L_vert = 3, 4
    n_samples = 2048
    n_iter = 250
    lr = 0.01
    J_seeds = [42, 43, 44, 45, 46]

    N, edges = diamond_lattice_v2(L_perp, L_vert)
    print(f"Lattice: N={N}, edges={len(edges)}, diam=9")
    print(f"DMRG truths: {DMRG_TRUTHS_N72}")
    print(f"RBM alpha=16 prior: {RBM_ALPHA16_N72_PRIOR}")
    print("")

    results = {"jastrow": [], "mlp": []}

    # Run Jastrow first (simpler, faster)
    print("=" * 60)
    print("PHASE 1: Jastrow ansatz")
    print("=" * 60)
    for J_seed in J_seeds:
        print(f"--- Jastrow J_seed={J_seed} ---")
        try:
            r = run_alt_ansatz(jastrow_factory, "jastrow",
                               L_perp, L_vert, n_samples=n_samples,
                               n_iter=n_iter, lr=lr, J_seed=J_seed)
            results["jastrow"].append(r)
            prior_err = abs(RBM_ALPHA16_N72_PRIOR[J_seed] -
                            DMRG_TRUTHS_N72[J_seed]) / abs(DMRG_TRUTHS_N72[J_seed])
            print(f"  E_Jastrow={r['E_final']:.4f}, rel_err={r['rel_err']*100:.3f}%, "
                  f"verdict={r['verdict']}; RBM_a16_prior={prior_err*100:.3f}%, "
                  f"wall={r['wall_s']:.1f}s")
        except Exception as exc:
            print(f"  FAILED: {exc}")
            results["jastrow"].append({"J_seed": J_seed, "error": str(exc)})
        print("")

    # Run MLP next (richer ansatz)
    print("=" * 60)
    print("PHASE 2: MLP ansatz (hidden_dims=(2N, 2N))")
    print("=" * 60)
    for J_seed in J_seeds:
        print(f"--- MLP J_seed={J_seed} ---")
        try:
            r = run_alt_ansatz(mlp_factory, "mlp",
                               L_perp, L_vert, n_samples=n_samples,
                               n_iter=n_iter, lr=lr, J_seed=J_seed)
            results["mlp"].append(r)
            prior_err = abs(RBM_ALPHA16_N72_PRIOR[J_seed] -
                            DMRG_TRUTHS_N72[J_seed]) / abs(DMRG_TRUTHS_N72[J_seed])
            print(f"  E_MLP={r['E_final']:.4f}, rel_err={r['rel_err']*100:.3f}%, "
                  f"verdict={r['verdict']}; RBM_a16_prior={prior_err*100:.3f}%, "
                  f"wall={r['wall_s']:.1f}s")
        except Exception as exc:
            print(f"  FAILED: {exc}")
            results["mlp"].append({"J_seed": J_seed, "error": str(exc)})
        print("")

    # Summary
    n_break_jastrow = sum(1 for r in results["jastrow"]
                          if "verdict" in r and r["verdict"] == "BREAK")
    n_break_mlp = sum(1 for r in results["mlp"]
                      if "verdict" in r and r["verdict"] == "BREAK")
    n_break_rbm_a16 = 1  # P3 hedge: only J=42 broke

    summary = {
        "lattice": f"N={N},L={L_perp},Lv={L_vert},edges={len(edges)},diam=9",
        "n_samples": n_samples,
        "n_iter": n_iter,
        "lr": lr,
        "DMRG_truths": DMRG_TRUTHS_N72,
        "RBM_alpha16_prior_n_break": n_break_rbm_a16,
        "ansatz_results": results,
        "n_break_summary": {
            "rbm_alpha16_prior": n_break_rbm_a16,
            "jastrow": n_break_jastrow,
            "mlp": n_break_mlp,
        },
    }

    out_path.write_text(json.dumps(summary, indent=2))

    print("=" * 60)
    print(f"Alt-ansatz attack T3 N=72 verdict:")
    print(f"  RBM alpha=16 prior: {n_break_rbm_a16}/5 BREAK")
    print(f"  Jastrow:            {n_break_jastrow}/5 BREAK")
    print(f"  MLP:                {n_break_mlp}/5 BREAK")
    if n_break_jastrow > n_break_rbm_a16 or n_break_mlp > n_break_rbm_a16:
        print(f"  → Alternative ansatz BREAKS more seeds than RBM alpha=16:")
        print(f"    mechanism (iii) RBM-specific failure indicated")
    elif n_break_jastrow == n_break_rbm_a16 and n_break_mlp == n_break_rbm_a16:
        print(f"  → All ansatzes equivalent break-fraction:")
        print(f"    boundary is NQS-class-wide; intrinsic-limit ridge ROBUST")
    else:
        print(f"  → Alternative ansatz fewer BREAKs than RBM:")
        print(f"    suggests RBM is best-of-class; intrinsic-limit ridge robust")
    print(f"Saved: {out_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
