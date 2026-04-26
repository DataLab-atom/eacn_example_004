"""5-method §D5 TVD pairwise matrix on T8 JZ 3.0 canonical 4 subsets.

Per claude2 commit 927b766 + claude2 message ts=1777161057742:
  "5-method §D5 已完成! commit 927b766, results/T8/T8_positive_p_4subsets.json.
   4 subsets 全部 64 patterns populated, mean clicks 4.19-4.25.
   请跑 TVD pairwise matrix."

This script:
  (1) Re-implements Goodman positive-P + WC sampler (transcribed from claude2's
      `code/T8/goodman_positive_p_sampler.py` 927b766 — independent verification
      via shared cov-construction conventions).
  (2) Runs positive-P on the 4 canonical subsets at n_samples=10000.
  (3) Computes pairwise TVD matrix between:
       - method 1 (claude5 60a92a8): Fock-aggregate-sample Gaussian baseline
       - method 2 (Goodman positive-P + WC, this script)
       - method 3 (claude8 540e632): Fock-aggregate-analytical (exact Hafnian
         click probabilities at cutoff=4)
       additional methods (claude2 d6ca180 Gaussian quadrature full-regime +
       claude2 a843594 pairwise chi correction NEGATIVE result) deferred to
       cross-branch JSON ingestion (claude2 has those click outputs locally).

  (4) Writes `t8_5method_d5_tvd.json` + `t8_5method_d5_tvd_interpretation.md`.

Honest scope (§H1):
  - This is a *3-method* implementation in the strict sense (claude5 / Goodman /
    claude8); the full 5-method matrix requires claude2's d6ca180 + a843594
    sample dumps to align on identical 4 subsets (currently not on my branch
    in click-sample-level format).
  - Goodman positive-P + WC follows claude2's 927b766 transcription with
    identical algorithm; this is independent re-implementation, not a deep
    algorithmic alternative.
  - Mean-click match (positive-P 4.24 vs my Gaussian baseline cutoff=4 ~3.5
    inferred) is the first sanity check; large discrepancy indicates regime
    boundary effects (positive-P captures more high-photon mass than cutoff=4
    truncation, as expected).

Author: claude5
"""
from __future__ import annotations

import json
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from scipy.linalg import cholesky

import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from gaussian_baseline_sampler_t8 import (
    JZ30_PARAMS,
    construct_jz30_covariance_matrix,
    select_mode_subset,
    reduce_cov_to_subset,
    click_probability_distribution,
    sample_clicks_from_distribution,
)


# ---------------------------------------------------------------------------
# Goodman positive-P + Whitening-Coloring (transcribed from claude2 927b766)
# ---------------------------------------------------------------------------
# Convention: claude2 uses xpxp ordering for cov_xp; my construct_jz30_covariance
# returns xxpp ordering. Need to convert for compatibility.

def xxpp_to_xpxp(cov_xxpp: np.ndarray, n_modes: int) -> np.ndarray:
    """Reorder cov from xxpp (q1,...,qN, p1,...,pN) to xpxp (q1,p1,q2,p2,...)."""
    perm = []
    for i in range(n_modes):
        perm.extend([i, n_modes + i])
    return cov_xxpp[np.ix_(perm, perm)]


def build_complex_covariance(cov_xp: np.ndarray, n_modes: int):
    """xpxp covariance -> (sigma_normal, sigma_anomalous) per claude2 927b766."""
    sigma_normal = np.zeros((n_modes, n_modes), dtype=complex)
    sigma_anomalous = np.zeros((n_modes, n_modes), dtype=complex)
    for i in range(n_modes):
        for j in range(n_modes):
            sxx = cov_xp[2 * i, 2 * j]
            spp = cov_xp[2 * i + 1, 2 * j + 1]
            sxp = cov_xp[2 * i, 2 * j + 1]
            spx = cov_xp[2 * i + 1, 2 * j]
            sigma_normal[i, j] = (sxx + spp + 1j * (spx - sxp)) / 2
            sigma_anomalous[i, j] = (sxx - spp + 1j * (spx + sxp)) / 2
    return sigma_normal, sigma_anomalous


def positive_p_sample(
    cov_xxpp: np.ndarray,
    n_modes: int,
    n_samples: int,
    n_wc_iter: int = 10,
    seed: int = 42,
) -> np.ndarray:
    """Positive-P + WC sampler (per claude2 927b766). Returns (n_samples, n_modes) clicks."""
    cov_xp = xxpp_to_xpxp(cov_xxpp, n_modes)
    rng = np.random.default_rng(seed)
    sigma_n, sigma_a = build_complex_covariance(cov_xp, n_modes)
    n_bar = np.real(np.diag(sigma_n)) - 0.5

    # Build target real covariance
    C_target = np.zeros((2 * n_modes, 2 * n_modes))
    for i in range(n_modes):
        for j in range(n_modes):
            val = sigma_n[i, j] / 2
            C_target[i, j] = val.real
            C_target[i, j + n_modes] = -val.imag
            C_target[i + n_modes, j] = val.imag
            C_target[i + n_modes, j + n_modes] = val.real
    C_target += 1e-8 * np.eye(2 * n_modes)

    # Initial thermal
    alphas_re = np.zeros((n_samples, n_modes))
    alphas_im = np.zeros((n_samples, n_modes))
    for i in range(n_modes):
        sigma_i = np.sqrt(max(n_bar[i] + 0.5, 0.01) / 2)
        alphas_re[:, i] = rng.normal(0, sigma_i, n_samples)
        alphas_im[:, i] = rng.normal(0, sigma_i, n_samples)
    X = np.column_stack([alphas_re, alphas_im])

    # WC iterations
    for _ in range(n_wc_iter):
        X_centered = X - X.mean(axis=0)
        C_curr = np.cov(X_centered.T) + 1e-8 * np.eye(2 * n_modes)
        try:
            L_curr = cholesky(C_curr, lower=True)
            X_white = np.linalg.solve(L_curr, X_centered.T).T
            L_target = cholesky(C_target, lower=True)
            X = (L_target @ X_white.T).T + X.mean(axis=0)
        except np.linalg.LinAlgError:
            break

    alphas = X[:, :n_modes] + 1j * X[:, n_modes:]
    intensities = np.abs(alphas) ** 2
    photons = rng.poisson(np.maximum(intensities, 0))
    clicks = (photons > 0).astype(np.int8)
    return clicks


# ---------------------------------------------------------------------------
# Gaussian baseline samples loader (claude5 60a92a8 canonical)
# ---------------------------------------------------------------------------

def load_canonical_gaussian_baseline_samples() -> Dict[Tuple[str, int], np.ndarray]:
    """Load samples from `jz30_gaussian_baseline_samples.json` (60a92a8 canonical)."""
    json_path = HERE / "jz30_gaussian_baseline_samples.json"
    with json_path.open("r") as f:
        data = json.load(f)
    out: Dict[Tuple[str, int], np.ndarray] = {}
    for entry in data["subsets"]:
        key = (entry["strategy"], entry["run_id"])
        out[key] = np.array(entry["samples"], dtype=np.int8)
    return out


# ---------------------------------------------------------------------------
# Hafnian-oracle analytical click distribution (claude8 540e632 equivalent)
# ---------------------------------------------------------------------------

def analytical_click_distribution(
    cov_subset: np.ndarray,
    n_subset: int,
    cutoff: int = 4,
) -> Dict[Tuple[int, ...], float]:
    """Identical to claude8 540e632 oracle (using thewalrus exact)."""
    return click_probability_distribution(cov_subset, n_subset, cutoff)


# ---------------------------------------------------------------------------
# TVD utilities
# ---------------------------------------------------------------------------

def empirical_histogram(samples: np.ndarray) -> Dict[Tuple[int, ...], float]:
    n = samples.shape[0]
    counts = Counter(tuple(row.tolist()) for row in samples)
    return {pat: c / n for pat, c in counts.items()}


def tvd_renormalized_full(
    p1: Dict[Tuple[int, ...], float],
    p2: Dict[Tuple[int, ...], float],
) -> float:
    """TVD between two distributions, both renormalized to sum=1 over their union support."""
    keys = set(p1) | set(p2)
    s1 = sum(p1.get(k, 0.0) for k in keys)
    s2 = sum(p2.get(k, 0.0) for k in keys)
    if s1 == 0 or s2 == 0:
        return float("nan")
    return 0.5 * sum(abs(p1.get(k, 0.0) / s1 - p2.get(k, 0.0) / s2) for k in keys)


def tvd_raw(
    p1: Dict[Tuple[int, ...], float],
    p2: Dict[Tuple[int, ...], float],
) -> float:
    """TVD without renormalization (interpret p1, p2 as already-normalized empirical histograms)."""
    keys = set(p1) | set(p2)
    return 0.5 * sum(abs(p1.get(k, 0.0) - p2.get(k, 0.0)) for k in keys)


# ---------------------------------------------------------------------------
# Top-level orchestration
# ---------------------------------------------------------------------------

def run_5method_d5_tvd(
    out_path: str = "branches/claude5/work/T8_jiuzhang3/t8_5method_d5_tvd.json",
    n_samples: int = 10_000,
    cutoff: int = 4,
) -> Dict:
    print("=== 5-method §D5 TVD pairwise matrix on T8 JZ 3.0 ===", flush=True)
    print(f"params: {JZ30_PARAMS}", flush=True)
    print(f"n_samples={n_samples}, cutoff={cutoff}", flush=True)

    t_global = time.time()
    cov, _ = construct_jz30_covariance_matrix(
        n_modes=JZ30_PARAMS["n_modes"],
        r=JZ30_PARAMS["squeezing_r"],
        eta=JZ30_PARAMS["loss_eta"],
        seed=42,
    )
    print(f"cov built ({cov.shape})", flush=True)

    n_modes = JZ30_PARAMS["n_modes"]
    n_subset = 6

    canonical_gaussian_samples = load_canonical_gaussian_baseline_samples()

    subsets = [("random", 0), ("random", 1), ("lc_aligned", 0), ("lc_aligned", 1)]

    per_subset_results = []
    for strategy, run_id in subsets:
        modes = select_mode_subset(strategy, n_subset=n_subset, n_modes=n_modes, seed=run_id)
        cov_subset = reduce_cov_to_subset(cov, modes, n_modes)

        # Method A — claude5 60a92a8 Gaussian baseline (load canonical samples)
        gaussian_samples = canonical_gaussian_samples[(strategy, run_id)]
        gaussian_hist = empirical_histogram(np.array(gaussian_samples, dtype=np.int8))

        # Method B — Goodman positive-P + WC (re-implementation of claude2 927b766)
        t_pp = time.time()
        pp_samples = positive_p_sample(
            cov_subset, n_subset, n_samples=n_samples, n_wc_iter=10, seed=42 + run_id
        )
        t_pp = time.time() - t_pp
        pp_hist = empirical_histogram(pp_samples)

        # Method C — claude8 540e632 hafnian oracle (analytical at cutoff=4)
        t_anal = time.time()
        analytical_dist = analytical_click_distribution(cov_subset, n_subset, cutoff=cutoff)
        t_anal = time.time() - t_anal

        # Pairwise TVDs
        # AB: gaussian_baseline (cutoff=4 sample) vs positive-P (full-regime sample)
        tvd_AB = tvd_raw(gaussian_hist, pp_hist)
        # AC: gaussian_baseline vs hafnian_oracle (sample-vs-analytical at SAME cutoff=4 → tier-1 sampling-noise tier)
        tvd_AC_renorm = tvd_renormalized_full(gaussian_hist, analytical_dist)
        # BC: positive-P vs hafnian_oracle (cross-method tier — positive-P is full-regime, oracle is cutoff=4 → regime-disparity tier)
        tvd_BC_renorm = tvd_renormalized_full(pp_hist, analytical_dist)

        per_subset_results.append(
            {
                "strategy": strategy,
                "run_id": run_id,
                "modes": modes,
                "n_samples_gaussian_baseline": len(gaussian_samples),
                "n_samples_positive_p": pp_samples.shape[0],
                "wall_clock_positive_p_s": t_pp,
                "wall_clock_analytical_s": t_anal,
                "mean_clicks_gaussian_baseline": float(gaussian_samples.sum() / len(gaussian_samples)),
                "mean_clicks_positive_p": float(pp_samples.sum() / pp_samples.shape[0]),
                "n_unique_patterns_gaussian_baseline": len(gaussian_hist),
                "n_unique_patterns_positive_p": len(pp_hist),
                "tvd_AB_gaussian_vs_positive_p_raw": tvd_AB,
                "tvd_AC_gaussian_vs_analytical_renorm": tvd_AC_renorm,
                "tvd_BC_positive_p_vs_analytical_renorm": tvd_BC_renorm,
            }
        )
        print(
            f"  {strategy} run={run_id} modes={modes}: "
            f"<n>_G={gaussian_samples.sum()/len(gaussian_samples):.3f} "
            f"<n>_PP={pp_samples.sum()/pp_samples.shape[0]:.3f} "
            f"TVD_AB={tvd_AB:.4f} TVD_AC={tvd_AC_renorm:.4f} TVD_BC={tvd_BC_renorm:.4f} "
            f"({t_pp:.1f}s pp)",
            flush=True,
        )

    # Aggregate
    aggregate = {
        "tvd_AB_mean": float(np.mean([r["tvd_AB_gaussian_vs_positive_p_raw"] for r in per_subset_results])),
        "tvd_AB_max": float(np.max([r["tvd_AB_gaussian_vs_positive_p_raw"] for r in per_subset_results])),
        "tvd_AC_mean": float(np.mean([r["tvd_AC_gaussian_vs_analytical_renorm"] for r in per_subset_results])),
        "tvd_AC_max": float(np.max([r["tvd_AC_gaussian_vs_analytical_renorm"] for r in per_subset_results])),
        "tvd_BC_mean": float(np.mean([r["tvd_BC_positive_p_vs_analytical_renorm"] for r in per_subset_results])),
        "tvd_BC_max": float(np.max([r["tvd_BC_positive_p_vs_analytical_renorm"] for r in per_subset_results])),
        "mean_clicks_positive_p_overall": float(np.mean([r["mean_clicks_positive_p"] for r in per_subset_results])),
        "mean_clicks_gaussian_overall": float(np.mean([r["mean_clicks_gaussian_baseline"] for r in per_subset_results])),
    }

    out = {
        "params": JZ30_PARAMS,
        "n_samples": n_samples,
        "cutoff": cutoff,
        "n_subset": n_subset,
        "subsets_evaluated": [list(s) for s in subsets],
        "methods": {
            "A_gaussian_baseline": "claude5 60a92a8 Fock-aggregate-sample (cutoff=4)",
            "B_goodman_positive_p": "claude2 927b766 reimplementation (positive-P + WC 10 iter, full-regime)",
            "C_hafnian_oracle": "claude8 540e632 Fock-aggregate-analytical (cutoff=4, exact)",
        },
        "per_subset": per_subset_results,
        "aggregate": aggregate,
        "schema_version": "1.0",
        "wall_clock_total_s": time.time() - t_global,
        "honest_scope": (
            "3-method §D5 (claude5 / Goodman positive-P / claude8); claude2 d6ca180 "
            "Gaussian-quadrature full-regime + claude2 a843594 pairwise-chi-correction "
            "deferred (require sample-level data dumps from claude2 branch). "
            "Goodman positive-P transcribed from claude2 927b766 — algorithm-identical "
            "re-implementation, not deeper algorithmic alternative."
        ),
    }

    out_p = Path(out_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with out_p.open("w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {out_path} ({out_p.stat().st_size} bytes)", flush=True)
    print(f"\n=== AGGREGATE TVD MATRIX ===", flush=True)
    print(f"  TVD(Gaussian vs PositiveP, raw):              mean={aggregate['tvd_AB_mean']:.4f} max={aggregate['tvd_AB_max']:.4f}", flush=True)
    print(f"  TVD(Gaussian vs Analytical, renorm shared):   mean={aggregate['tvd_AC_mean']:.4f} max={aggregate['tvd_AC_max']:.4f}", flush=True)
    print(f"  TVD(PositiveP vs Analytical, renorm shared):  mean={aggregate['tvd_BC_mean']:.4f} max={aggregate['tvd_BC_max']:.4f}", flush=True)
    print(f"  mean clicks: Gaussian={aggregate['mean_clicks_gaussian_overall']:.3f} PositiveP={aggregate['mean_clicks_positive_p_overall']:.3f}", flush=True)
    print(f"  wall_clock_total: {out['wall_clock_total_s']:.1f}s", flush=True)
    return out


if __name__ == "__main__":
    run_5method_d5_tvd()
