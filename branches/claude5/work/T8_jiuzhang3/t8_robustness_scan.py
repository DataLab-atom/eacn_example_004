"""§E3-style within-method robustness scan on T8 Gaussian baseline sampler.

Per claude7 cycle 291 REV-DISCIPLINE-002 v0.1 (`983ce80`) explicit framework
extension: §E3-style robustness scan applicable to **T8 GBS (within-method
dimension orthogonal to §D5 cross-validation)**. This complements the §D5
cross-method dual-impl by scanning hyperparameter sensitivity within the
Gaussian baseline method itself.

Scan grid (3 × 3 = 9 configurations):
  - Fock cutoff ∈ {3, 4, 5}: cutoff=4 is canonical (claude5 60a92a8 + claude8 540e632)
  - Sample RNG seed ∈ {1234, 9999, 42}: cutoff=4 seed=1234 is canonical

Fixed (matching canonical):
  - n_modes = 144 (JZ 3.0)
  - r = 1.5
  - eta = 0.424
  - n_subset = 6
  - n_samples = 10_000
  - 4 subsets: random run0/run1 + lc_aligned run0/run1
  - Haar seed = 42 (matches claude8 oracle)

Outputs:
  - per-config (sum_probs, click distribution histogram, wall_clock)
  - cross-config TVD on shared support: cutoff sensitivity (at fixed seed)
    + sampling sensitivity (at fixed cutoff)
  - interpretation note: stability vs perturbation = robustness-of-method

Author: claude5
"""
from __future__ import annotations

import json
import time
from collections import Counter
from itertools import product
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

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


CUTOFF_GRID = [3, 4]  # cutoff=5 dropped (5^6 = 15625 Fock states/call too expensive)
SEED_GRID = [1234, 9999, 42, 11111]
N_SUBSET = 6
N_SAMPLES = 10_000
SUBSETS = [("random", 0), ("random", 1), ("lc_aligned", 0), ("lc_aligned", 1)]


def empirical_click_histogram(samples: np.ndarray) -> Dict[Tuple[int, ...], float]:
    """Count empirical click-pattern frequencies, normalized to a probability."""
    n = samples.shape[0]
    counts = Counter(tuple(row.tolist()) for row in samples)
    return {pat: c / n for pat, c in counts.items()}


def tvd_on_shared_support(
    p1: Dict[Tuple[int, ...], float],
    p2: Dict[Tuple[int, ...], float],
) -> float:
    """Total-variation distance on the shared support of two click distributions."""
    keys = set(p1) | set(p2)
    return 0.5 * sum(abs(p1.get(k, 0.0) - p2.get(k, 0.0)) for k in keys)


def run_one_config(
    cov: np.ndarray,
    n_modes: int,
    cutoff: int,
    sample_seed: int,
) -> List[Dict]:
    """Run the Gaussian baseline sampler on the 4 canonical subsets."""
    sample_rng = np.random.default_rng(sample_seed)
    out: List[Dict] = []
    for strategy, run_id in SUBSETS:
        subset = select_mode_subset(strategy, n_subset=N_SUBSET, n_modes=n_modes, seed=run_id)
        cov_subset = reduce_cov_to_subset(cov, subset, n_modes)
        t0 = time.time()
        click_probs = click_probability_distribution(cov_subset, N_SUBSET, cutoff)
        samples, sum_probs = sample_clicks_from_distribution(click_probs, N_SAMPLES, sample_rng)
        wall = time.time() - t0
        emp = empirical_click_histogram(samples)
        out.append(
            {
                "strategy": strategy,
                "run_id": run_id,
                "modes": subset,
                "sum_probs_pre_renorm": sum_probs,
                "n_unique_patterns": len(emp),
                "empirical_histogram": {",".join(map(str, k)): v for k, v in emp.items()},
                "wall_clock_s": wall,
            }
        )
    return out


def run_robustness_scan(
    out_path: str = "branches/claude5/work/T8_jiuzhang3/t8_robustness_scan.json",
) -> Dict:
    print("=== T8 §E3-style robustness scan ===", flush=True)
    print(f"Cutoff grid: {CUTOFF_GRID}", flush=True)
    print(f"Sample-seed grid: {SEED_GRID}", flush=True)
    print(f"4 subsets × {len(CUTOFF_GRID)} cutoffs × {len(SEED_GRID)} seeds "
          f"= {4 * len(CUTOFF_GRID) * len(SEED_GRID)} sub-runs", flush=True)

    t_global = time.time()
    cov, _ = construct_jz30_covariance_matrix(
        n_modes=JZ30_PARAMS["n_modes"],
        r=JZ30_PARAMS["squeezing_r"],
        eta=JZ30_PARAMS["loss_eta"],
        seed=42,
    )
    print(f"covariance built ({cov.shape})", flush=True)

    n_modes = JZ30_PARAMS["n_modes"]

    configs: Dict[Tuple[int, int], List[Dict]] = {}
    for cutoff, seed in product(CUTOFF_GRID, SEED_GRID):
        t0 = time.time()
        per_subset = run_one_config(cov, n_modes, cutoff=cutoff, sample_seed=seed)
        wall = time.time() - t0
        sum_probs_list = [s["sum_probs_pre_renorm"] for s in per_subset]
        print(
            f"  cutoff={cutoff} seed={seed}: "
            f"sum_probs={[f'{x:.4f}' for x in sum_probs_list]} wall={wall:.1f}s",
            flush=True,
        )
        configs[(cutoff, seed)] = per_subset

    # Sensitivity analyses
    canonical = (4, 1234)
    canonical_cfg = configs[canonical]

    cutoff_sensitivity: List[Dict] = []
    for cutoff in CUTOFF_GRID:
        if cutoff == 4:
            continue
        cfg = configs[(cutoff, 1234)]
        for canon_subset, scan_subset in zip(canonical_cfg, cfg):
            tvd = tvd_on_shared_support(
                {tuple(map(int, k.split(","))): v for k, v in canon_subset["empirical_histogram"].items()},
                {tuple(map(int, k.split(","))): v for k, v in scan_subset["empirical_histogram"].items()},
            )
            cutoff_sensitivity.append(
                {
                    "vs_canonical_cutoff": 4,
                    "scanned_cutoff": cutoff,
                    "subset": (scan_subset["strategy"], scan_subset["run_id"]),
                    "sum_probs_canonical": canon_subset["sum_probs_pre_renorm"],
                    "sum_probs_scanned": scan_subset["sum_probs_pre_renorm"],
                    "tvd_empirical_histogram": tvd,
                }
            )

    seed_sensitivity: List[Dict] = []
    for seed in SEED_GRID:
        if seed == 1234:
            continue
        cfg = configs[(4, seed)]
        for canon_subset, scan_subset in zip(canonical_cfg, cfg):
            tvd = tvd_on_shared_support(
                {tuple(map(int, k.split(","))): v for k, v in canon_subset["empirical_histogram"].items()},
                {tuple(map(int, k.split(","))): v for k, v in scan_subset["empirical_histogram"].items()},
            )
            seed_sensitivity.append(
                {
                    "vs_canonical_seed": 1234,
                    "scanned_seed": seed,
                    "subset": (scan_subset["strategy"], scan_subset["run_id"]),
                    "tvd_empirical_histogram": tvd,
                }
            )

    cutoff_tvds = [c["tvd_empirical_histogram"] for c in cutoff_sensitivity]
    seed_tvds = [c["tvd_empirical_histogram"] for c in seed_sensitivity]
    summary = {
        "scan_dim": "cutoff_x_seed",
        "n_configs_total": len(CUTOFF_GRID) * len(SEED_GRID),
        "canonical_config": {"cutoff": canonical[0], "sample_seed": canonical[1]},
        "cutoff_sensitivity_tvd_mean": float(np.mean(cutoff_tvds)) if cutoff_tvds else None,
        "cutoff_sensitivity_tvd_max": float(np.max(cutoff_tvds)) if cutoff_tvds else None,
        "seed_sensitivity_tvd_mean": float(np.mean(seed_tvds)) if seed_tvds else None,
        "seed_sensitivity_tvd_max": float(np.max(seed_tvds)) if seed_tvds else None,
        "sum_probs_per_cutoff": {
            int(c): {
                "mean": float(np.mean([s["sum_probs_pre_renorm"]
                                        for s in configs[(c, 1234)]])),
                "min": float(np.min([s["sum_probs_pre_renorm"]
                                      for s in configs[(c, 1234)]])),
                "max": float(np.max([s["sum_probs_pre_renorm"]
                                      for s in configs[(c, 1234)]])),
            }
            for c in CUTOFF_GRID
        },
    }

    out = {
        "scan_meta": {
            "params": JZ30_PARAMS,
            "n_subset": N_SUBSET,
            "n_samples": N_SAMPLES,
            "subsets": [list(s) for s in SUBSETS],
            "cutoff_grid": CUTOFF_GRID,
            "seed_grid": SEED_GRID,
            "n_configs": len(configs),
            "schema_version": "1.0",
        },
        "configs": [
            {
                "cutoff": cutoff,
                "sample_seed": seed,
                "per_subset": per_subset,
            }
            for (cutoff, seed), per_subset in configs.items()
        ],
        "cutoff_sensitivity": cutoff_sensitivity,
        "seed_sensitivity": seed_sensitivity,
        "summary": summary,
        "wall_clock_total_s": time.time() - t_global,
    }

    out_p = Path(out_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with out_p.open("w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {out_path} ({out_p.stat().st_size} bytes)")
    print(f"=== summary ===")
    print(f"  cutoff sensitivity TVD: mean={summary['cutoff_sensitivity_tvd_mean']:.4f} "
          f"max={summary['cutoff_sensitivity_tvd_max']:.4f}")
    print(f"  seed sensitivity TVD:   mean={summary['seed_sensitivity_tvd_mean']:.4f} "
          f"max={summary['seed_sensitivity_tvd_max']:.4f}")
    for c in CUTOFF_GRID:
        print(f"  sum_probs (cutoff={c}): {summary['sum_probs_per_cutoff'][c]}")
    print(f"  wall_clock_total: {out['wall_clock_total_s']:.1f}s")
    return out


if __name__ == "__main__":
    run_robustness_scan()
