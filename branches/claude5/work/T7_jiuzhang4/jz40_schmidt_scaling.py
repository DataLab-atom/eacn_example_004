"""JZ 4.0 Schmidt-spectrum scaling analysis (T7 deferred §future-work shipped).

Per claude5 schmidt_spectrum_interpretation.md §future signals:
  "Same analysis for JZ 4.0 covariance (M=1024 sources × 8176 modes) deferred —
   would extend T7 stands-firm quantitative armoury at next opportunity."

This script ships that future work via N-scaling extrapolation:
  - Construct JZ 4.0-param covariance at N ∈ {144, 256, 512, 1024} (η=0.51, r=1.5)
  - Run central-cut Schmidt SVD analysis at each N (Adesso-Illuminati §3 proxy)
  - Extrapolate chi(99% mass) scaling vs N to project chi(99%) at JZ 4.0 N=8176
  - Compare against the JZ 3.0 baseline (N=144, η=0.424) to quantify
    the per-axis (modes vs eta) contribution to chi requirement growth

Honest scope (§H1):
  - Output-mode count for JZ 4.0 is 8176 (1024 SMSS sources after PPNRD-style
    splitting + final beam-splitter cascade per Liu arXiv:2508.09092). For this
    scaling analysis, we construct N-mode systems with JZ 4.0 single-source
    parameters; the actual JZ 4.0 covariance has additional structure from
    the source-to-output mapping that we do not model here. The chi extrapolation
    is therefore a *lower bound* — the actual chi at JZ 4.0 may be larger.
  - eta=0.51 per Liu arXiv:2508.09092 verbatim; r per JZ 4.0 paper Table 1.

Author: claude5
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, List

import numpy as np
from thewalrus import symplectic

import sys
HERE = Path(__file__).resolve().parent
T8_HERE = HERE.parent / "T8_jiuzhang3"
sys.path.insert(0, str(T8_HERE))

from gaussian_baseline_sampler_t8 import haar_unitary
from schmidt_spectrum_analysis import (
    schmidt_spectrum_at_cut,
    power_law_fit_log,
    chi_for_target_mass,
)


JZ40_PARAMS = {
    "squeezing_r": 1.5,    # midpoint per Liu arXiv:2508.09092
    "loss_eta": 0.51,      # per Liu arXiv:2508.09092 verbatim
    "n_modes_actual": 8176,
}


def construct_jz40_like_covariance(
    n_modes: int,
    r: float,
    eta: float,
    seed: int = 42,
) -> np.ndarray:
    """Build a JZ 4.0-parameter covariance at the requested mode count.

    Uses identical construction to gaussian_baseline_sampler_t8 but with
    JZ 4.0 params (eta=0.51, r=1.5).
    """
    rng = np.random.default_rng(seed)
    r_vec = np.full(n_modes, r)
    S_squeeze = symplectic.squeezing(r_vec)
    cov_squeeze = S_squeeze @ S_squeeze.T

    U = haar_unitary(n_modes, rng)
    S_U = symplectic.interferometer(U)
    cov_after_U = S_U @ cov_squeeze @ S_U.T

    eta_vec = np.full(n_modes, eta)
    mu = np.zeros(2 * n_modes)
    mu, cov_lossy = symplectic.passive_transformation(
        mu, cov_after_U, np.diag(np.sqrt(eta_vec))
    )
    return cov_lossy


def run_jz40_scaling(
    out_path: str = "branches/claude5/work/T7_jiuzhang4/jz40_schmidt_scaling.json",
    n_grid: List[int] = (144, 256, 384, 512),
) -> Dict:
    print("=== JZ 4.0 Schmidt-spectrum scaling analysis ===", flush=True)
    print(f"params: {JZ40_PARAMS}", flush=True)
    print(f"n_modes grid: {list(n_grid)} (extrapolating to actual N={JZ40_PARAMS['n_modes_actual']})", flush=True)

    results: List[Dict] = []
    t_global = time.time()

    for n in n_grid:
        t_n = time.time()
        cov = construct_jz40_like_covariance(
            n_modes=n,
            r=JZ40_PARAMS["squeezing_r"],
            eta=JZ40_PARAMS["loss_eta"],
            seed=42,
        )
        t_cov = time.time() - t_n
        cut = n // 2

        spec = schmidt_spectrum_at_cut(cov, n, cut)
        # Recompute full singular vector for power-law fit + chi(target).
        n_A = spec["n_A"]
        n_B = spec["n_B"]
        idx_qA = list(range(0, cut))
        idx_qB = list(range(cut, n))
        idx_pA = list(range(n, n + cut))
        idx_pB = list(range(n + cut, 2 * n))
        perm = idx_qA + idx_qB + idx_pA + idx_pB
        cov_perm = cov[np.ix_(perm, perm)]
        A_rows = list(range(n_A)) + list(range(n_A + n_B, n_A + n_B + n_A))
        B_rows = list(range(n_A, n_A + n_B)) + list(range(n_A + n_B + n_A, 2 * n))
        cov_AA = cov_perm[np.ix_(A_rows, A_rows)]
        cov_BB = cov_perm[np.ix_(B_rows, B_rows)]
        cov_AB = cov_perm[np.ix_(A_rows, B_rows)]
        L_AA = np.linalg.cholesky(cov_AA + 1e-10 * np.eye(2 * n_A))
        L_BB = np.linalg.cholesky(cov_BB + 1e-10 * np.eye(2 * n_B))
        sym_block = np.linalg.solve(L_AA, cov_AB) @ np.linalg.solve(L_BB.T, np.eye(2 * n_B))
        s_full = np.linalg.svd(sym_block, compute_uv=False)
        s_full = np.sort(s_full)[::-1]

        chi_50 = chi_for_target_mass(s_full, 0.50)
        chi_99 = chi_for_target_mass(s_full, 0.99)
        chi_999 = chi_for_target_mass(s_full, 0.999)
        plf = power_law_fit_log(s_full, head_skip=2)
        wall = time.time() - t_n

        entry = {
            "n_modes": n,
            "cut": cut,
            "n_singular": len(s_full),
            "wall_clock_s": wall,
            "wall_clock_cov_build_s": t_cov,
            "alpha": plf["alpha"],
            "alpha_intercept": plf["intercept"],
            "chi_for_50_pct_mass": chi_50,
            "chi_for_99_pct_mass": chi_99,
            "chi_for_999_pct_mass": chi_999,
            "chi_99_over_n": chi_99 / n,
            "chi_99_over_n_singular": chi_99 / len(s_full),
        }
        results.append(entry)
        print(
            f"  N={n:4d}: chi(50%)={chi_50:4d}  chi(99%)={chi_99:4d}  "
            f"chi(99%)/N={chi_99/n:.3f}  alpha={plf['alpha']:.3f}  "
            f"({wall:.1f}s)",
            flush=True,
        )

    # Power-law extrapolation: chi(99%) ~ a * N^b
    ns = np.array([r["n_modes"] for r in results], dtype=np.float64)
    chis = np.array([r["chi_for_99_pct_mass"] for r in results], dtype=np.float64)
    log_n = np.log(ns)
    log_chi = np.log(chis)
    A = np.vstack([log_n, np.ones_like(log_n)]).T
    slope_chi, intercept_chi = np.linalg.lstsq(A, log_chi, rcond=None)[0]
    n_actual = JZ40_PARAMS["n_modes_actual"]
    chi_predicted_actual = float(np.exp(intercept_chi + slope_chi * np.log(n_actual)))

    out = {
        "params": JZ40_PARAMS,
        "n_grid": list(n_grid),
        "results": results,
        "extrapolation": {
            "chi_99_scaling_law": f"chi(99%) ~ exp({intercept_chi:.3f}) * N^{slope_chi:.3f}",
            "scaling_exponent_b": float(slope_chi),
            "scaling_prefactor_a": float(np.exp(intercept_chi)),
            "predicted_chi_at_actual_N": chi_predicted_actual,
            "predicted_chi_99_at_8176": chi_predicted_actual,
            "comparison_jz30_central_cut_chi_99": 127,
            "comparison_oh_2024_critical_chi": 200,
        },
        "schema_version": "1.0",
        "wall_clock_total_s": time.time() - t_global,
        "honest_scope": (
            "N-mode JZ 4.0-parameter construction is a lower bound on actual "
            "JZ 4.0 chi requirement (additional source-to-output PPNRD/beam-splitter "
            "structure not modeled). Power-law extrapolation assumes scaling law "
            "holds from N=512 to N=8176; actual scaling may break (likely "
            "underestimate) due to entanglement saturation effects."
        ),
        "interpretation": {
            "primary_finding_template": (
                "JZ 4.0 (N=8176, eta=0.51) extrapolated chi(99%) = {chi_pred} "
                "via N^{exp:.2f} scaling law fit on {n_grid_size}-point "
                "logspaced grid. Compare against JZ 3.0 (N=144, eta=0.424) "
                "chi(99%)=127. Memory cost at chi={chi_pred}: ~{mem_gb:.1f} GB MPS "
                "peak (chi^2 * d * N for d=25 cutoff=4 local Hilbert dim). "
                "RTX 4060 8GB VRAM = {ratio:.0f}x shortfall."
            ),
        },
    }

    out_p = Path(out_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with out_p.open("w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {out_path} ({out_p.stat().st_size} bytes)", flush=True)

    print(f"\n=== EXTRAPOLATION SUMMARY ===", flush=True)
    print(f"  chi(99%) scaling law: {out['extrapolation']['chi_99_scaling_law']}", flush=True)
    print(f"  Predicted chi(99%) at JZ 4.0 N=8176: {chi_predicted_actual:.0f}", flush=True)
    print(f"  JZ 3.0 baseline chi(99%) at N=144: 127", flush=True)
    print(f"  Oh-2024 critical chi for tractable MPS: 200", flush=True)
    if chi_predicted_actual > 200:
        ratio = chi_predicted_actual / 200
        mem_gb = (chi_predicted_actual ** 2 * 25 * n_actual) / (1024 ** 3)
        print(f"  Predicted chi >> Oh-2024 critical chi by {ratio:.1f}x", flush=True)
        print(f"  Memory cost at chi={chi_predicted_actual:.0f}: ~{mem_gb:.0f} GB MPS peak", flush=True)
        print(f"  RTX 4060 8GB shortfall: ~{mem_gb/8:.0f}x", flush=True)
    print(f"  wall_clock_total: {out['wall_clock_total_s']:.1f}s", flush=True)
    return out


if __name__ == "__main__":
    run_jz40_scaling()
