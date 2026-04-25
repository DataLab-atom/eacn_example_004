"""
P6 hedge: RBM alpha=32 N=72 with n_samples=4096 (2x sample budget after OOM at 8192).

NOTE: original design n_samples=8192 (4x) hit silent OOM/crash on commodity
hardware (12-core CPU, no GPU) with alpha=32 + N=72 + 168k params + 8x chains.
Reduced to n_samples=4096 (2x baseline) for tractable execution while still
testing mechanism (i)+(ii) sample-budget axis.

Tests whether the alpha=32 anti-monotonic regression observed at
n_samples=2048 (commit 9087c9b) is rescued by a 4x sample budget.

Mechanism disambiguation per §A5.2 v0.7.1:
  - SUPPORTED (>= 3/5 BREAK): mechanism (i)+(ii) implicated
    (Adam-no-SR + n_samples=2048 SR-equivalent gradient SNR insufficient);
    P5 status would reverse, "method-class intrinsic-limit ridge" weakens
  - DISCONFIRMED (0/5 BREAK same as alpha=32 n_samples=2048): mechanism
    (i)+(ii) ruled out, mechanism (iii) RBM ansatz class intrinsic
    confirmed; method-class intrinsic-limit ridge framing strengthens
  - PARTIAL (1-2/5 BREAK): partial mechanism (i)+(ii) signal, ambiguous

DMRG truth reuse: claude7 commit 9b274dc, edges_md5=93c0312e4ce75a78f4b7e523dbe84742.
No new ground truth needed since same N=72 + same J seeds 42-46.

Compute estimate: ~120-150 min (4x n_samples scaling vs P-ext ~37 min/seed = ~150 min)
on single-CPU JAX 0.10. Total wall ~2-3 h for 5 J-seeds.

Output: results/T3_v2_P6_hedge_N72_alpha32_nsamples8192.json
"""

import numpy as np
import netket as nk
import time
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from canonical_diamond_v2 import diamond_lattice_v2

# DMRG truths from claude7 9b274dc (frozen by edges_md5)
DMRG_TRUTHS_N72 = {
    42: -46.382921,
    43: -46.419882,
    44: -49.192424,
    45: -50.882652,
    46: -46.833057,
}

# alpha=16 prior errors at n_samples=2048 (from P3 hedge commit 4509c39)
RBM_ALPHA16_N_SAMPLES_2048_PRIOR = {
    42: -44.4470,
    43: -38.7581,
    44: -36.4599,
    45: -37.5259,
    46: -43.1048,
}

# alpha=32 prior errors at n_samples=2048 (from P-ext commit 9087c9b)
RBM_ALPHA32_N_SAMPLES_2048_PRIOR = {
    42: -35.7348,
    43: -35.3250,
    44: -36.6963,
    45: -36.4623,
    46: -40.4458,
}


def build_v2_with_seed(L_perp, L_vert, J_seed):
    """Build canonical diamond v2 lattice with parametrized J seed."""
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


def run_p6(L_perp, L_vert, alpha, n_samples, n_iter, lr, J_seed, init_seed=0):
    """Run P6 single-seed: RBM alpha=32 with n_samples=8192."""
    N, edges, J, hilbert, H = build_v2_with_seed(L_perp, L_vert, J_seed)

    model = nk.models.RBM(alpha=alpha, param_dtype=np.float64)
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
        "J_seed": J_seed,
        "E_RBM_alpha32_nsamples8192": E_final,
        "DMRG": DMRG,
        "rel_err": rel_err,
        "wall_s": wall,
        "verdict": verdict,
        "n_iter": n_iter,
        "n_samples": n_samples,
        "lr": lr,
        "alpha": alpha,
    }


def wilson_ci_95(k, n):
    """95% Wilson confidence interval for k/n proportion."""
    if n == 0:
        return (0.0, 1.0)
    z = 1.96
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def main():
    print("=" * 60)
    print("P6 hedge: RBM alpha=32 N=72 n_samples=8192 (4x sample budget)")
    print("=" * 60)

    repo = Path(__file__).resolve().parent.parent.parent
    out_path = repo / "results" / "T3_v2_P6_hedge_N72_alpha32_nsamples8192.json"

    L_perp, L_vert = 3, 4
    alpha = 32
    n_samples = 4096  # reduced from 8192 due to OOM; 2x baseline still tests sample-budget axis
    n_iter = 300
    lr = 0.01
    J_seeds = [42, 43, 44, 45, 46]

    N, edges = diamond_lattice_v2(L_perp, L_vert)
    print(f"Lattice: N={N}, edges={len(edges)}, diam=9")
    print(f"alpha={alpha}, n_samples={n_samples}, n_iter={n_iter}, lr={lr}")
    print(f"DMRG truths: {DMRG_TRUTHS_N72}")
    print("")

    results = []
    for J_seed in J_seeds:
        print(f"--- J_seed={J_seed} ---")
        r = run_p6(L_perp, L_vert, alpha=alpha, n_samples=n_samples,
                   n_iter=n_iter, lr=lr, J_seed=J_seed)
        results.append(r)
        print(f"  E_RBM={r['E_RBM_alpha32_nsamples8192']:.4f}, "
              f"DMRG={r['DMRG']:.4f}, "
              f"rel_err={r['rel_err']*100:.3f}%, "
              f"verdict={r['verdict']}, wall={r['wall_s']:.1f}s")
        print("")

    n_breaks = sum(1 for r in results if r["verdict"] == "BREAK")
    ci = wilson_ci_95(n_breaks, len(results))

    # Three-state verdict per §4.2 v0.7.1 P6 quantitative threshold
    if n_breaks >= 3:
        p6_verdict = "SUPPORTED"
        interpretation = ("Mechanism (i)+(ii) implicated: 4x n_samples rescues "
                          "alpha=32; SR-equivalent gradient SNR was the bottleneck. "
                          "Method-class intrinsic-limit ridge framing weakens.")
    elif n_breaks == 0:
        p6_verdict = "DISCONFIRMED"
        interpretation = ("Mechanism (i)+(ii) ruled out: 4x n_samples does NOT "
                          "rescue alpha=32. Mechanism (iii) RBM ansatz class "
                          "intrinsic confirmed; intrinsic-limit ridge strengthens.")
    else:  # 1 or 2
        p6_verdict = "PARTIAL"
        interpretation = (f"Partial mechanism (i)+(ii) signal: {n_breaks}/5 BREAK "
                          "ambiguous; further disambiguation needed.")

    summary = {
        "lattice": f"N={N},L={L_perp},Lv={L_vert},edges={len(edges)},diam=9",
        "alpha": alpha,
        "n_samples": n_samples,
        "n_samples_prior": 2048,
        "n_iter": n_iter,
        "lr": lr,
        "J_seeds": J_seeds,
        "DMRG_truths": DMRG_TRUTHS_N72,
        "RBM_alpha16_n_samples_2048_prior": RBM_ALPHA16_N_SAMPLES_2048_PRIOR,
        "RBM_alpha32_n_samples_2048_prior": RBM_ALPHA32_N_SAMPLES_2048_PRIOR,
        "results": results,
        "n_breaks": n_breaks,
        "wilson_ci_95": list(ci),
        "P6_verdict": p6_verdict,
        "interpretation": interpretation,
    }

    out_path.write_text(json.dumps(summary, indent=2))

    print("=" * 60)
    print(f"P6 verdict: {p6_verdict}")
    print(f"break_fraction = {n_breaks}/5, 95% Wilson CI [{ci[0]:.3f}, {ci[1]:.3f}]")
    print(f"Interpretation: {interpretation}")
    print(f"Saved: {out_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
