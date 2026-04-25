"""
v10: Pareto alpha fit on d=8 LC-edge top-500 (cascade 4/4 trigger).

Closes claude1 verdict 42ccb8d R-N items:
  - R-3 closer: r^2 + 95% bootstrap CI on alpha + Delta-AIC/Delta-BIC vs exponential
  - R-4 closer: alpha_universal (Schuster-Yin Zipf baseline = 1.0) vs alpha_measured
  - R-2 closer: top-K convergence loop K in {100, 200, 300, 500}

R-1 acknowledged in markdown: only d=8 single case, awaiting claude4 d=10/d=12 batch.

Reads claude4 d=8 top-500 JSON via origin/claude4 (branch fence: read-only).
"""
from __future__ import annotations

import json
import subprocess
from typing import Any, Dict, List, Tuple

import numpy as np
from scipy import stats

D8_PATH = "results/12q_3x4_d8_q0q4_LCedge_top500.json"


def load_claude4_d8() -> Dict[str, Any]:
    blob = subprocess.check_output(
        ["git", "show", f"origin/claude4:{D8_PATH}"],
        text=True, encoding="utf-8",
    )
    return json.loads(blob)


def pareto_fit(coeffs_sq: List[float], k_subset: int | None = None
               ) -> Tuple[float, float, stats._stats_mstats_common.LinregressResult]:
    arr = np.array(sorted(coeffs_sq, reverse=True), dtype=np.float64)
    if k_subset is not None:
        arr = arr[:k_subset]
    arr = arr[arr > 0]
    rank = np.arange(1, len(arr) + 1)
    log_x = np.log10(rank)
    log_y = np.log10(arr)
    res = stats.linregress(log_x, log_y)
    return -res.slope, res.rvalue ** 2, res


def bootstrap_ci(coeffs_sq: List[float], n_boot: int = 1000, seed: int = 42
                 ) -> Tuple[float, float]:
    rng = np.random.default_rng(seed)
    arr = np.array(sorted(coeffs_sq, reverse=True), dtype=np.float64)
    arr = arr[arr > 0]
    alphas = []
    for _ in range(n_boot):
        idx = rng.choice(len(arr), size=len(arr), replace=True)
        sample = np.sort(arr[idx])[::-1]
        sample = sample[sample > 0]
        if len(sample) < 3:
            continue
        rank = np.arange(1, len(sample) + 1)
        slope = stats.linregress(np.log10(rank), np.log10(sample)).slope
        alphas.append(-slope)
    a = np.array(alphas)
    return float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))


def aic_bic_compare(coeffs_sq: List[float]) -> Dict[str, Any]:
    arr = np.array(sorted(coeffs_sq, reverse=True), dtype=np.float64)
    arr = arr[arr > 0]
    rank = np.arange(1, len(arr) + 1)
    log_y = np.log10(arr)
    n = len(arr)

    # Power-law: log_y = a + b * log(rank)
    log_rank = np.log10(rank)
    pl = stats.linregress(log_rank, log_y)
    pl_pred = pl.slope * log_rank + pl.intercept
    pl_rss = float(np.sum((log_y - pl_pred) ** 2))
    pl_aic = n * np.log(pl_rss / n) + 2 * 2
    pl_bic = n * np.log(pl_rss / n) + 2 * np.log(n)

    # Exponential: log_y = a + b * rank
    ex = stats.linregress(rank, log_y)
    ex_pred = ex.slope * rank + ex.intercept
    ex_rss = float(np.sum((log_y - ex_pred) ** 2))
    ex_aic = n * np.log(ex_rss / n) + 2 * 2
    ex_bic = n * np.log(ex_rss / n) + 2 * np.log(n)

    return {
        "powerlaw": {"slope": float(pl.slope), "r2": float(pl.rvalue ** 2),
                     "aic": float(pl_aic), "bic": float(pl_bic)},
        "exponential": {"slope": float(ex.slope), "r2": float(ex.rvalue ** 2),
                        "aic": float(ex_aic), "bic": float(ex_bic)},
        "delta_aic_exp_minus_pl": float(ex_aic - pl_aic),
        "delta_bic_exp_minus_pl": float(ex_bic - pl_bic),
    }


def main() -> Dict[str, Any]:
    data = load_claude4_d8()
    coeffs_sq = [t["coeff_sq"] for t in data["terms_top500"]]

    alpha, r2, _ = pareto_fit(coeffs_sq)
    ci_lo, ci_hi = bootstrap_ci(coeffs_sq)
    cmp = aic_bic_compare(coeffs_sq)

    # Schuster-Yin universal Zipf baseline alpha=1.0 for asymptotic ranked Pauli-path tail.
    # SY arXiv:2407.12768 sec III: combinatorial path multiplicity dominates in
    # post-screening regime; Zipf-Mandelbrot alpha ~ 1 is the universal floor.
    alpha_universal = 1.0
    alpha_diff = abs(alpha - alpha_universal)
    in_universal_band = ci_lo <= alpha_universal <= ci_hi

    convergence: List[Tuple[int, float, float]] = []
    for k in [100, 200, 300, 500]:
        a_k, r2_k, _ = pareto_fit(coeffs_sq, k_subset=k)
        convergence.append((k, float(a_k), float(r2_k)))

    return {
        "case": "12q_3x4_d=8_LC-edge_q0_q4",
        "n_terms_total_at_w_le_4": data["n_terms_total"],
        "total_norm_at_w_le_4": data["total_norm"],
        "top500_cum_pct": data["top500_cum_pct"],
        "weight_distribution": data["weight_distribution"],
        "alpha_main": float(alpha),
        "r2_main": float(r2),
        "alpha_ci95_low": ci_lo,
        "alpha_ci95_high": ci_hi,
        "aic_bic": cmp,
        "alpha_universal_zipf": alpha_universal,
        "alpha_diff_abs": float(alpha_diff),
        "in_universal_band": bool(in_universal_band),
        "convergence_top_k": convergence,
    }


if __name__ == "__main__":
    import pprint
    pprint.pprint(main(), sort_dicts=False)
