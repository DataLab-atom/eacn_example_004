"""
T8 HOG / TVD benchmark — claude5 Gaussian baseline vs claude8 hafnian oracle.

Per t-modywqdx allocation correction + cascade Option B (claude5 endorsed):
  - claude5 lead: Option B Gaussian baseline sampler `branches/claude5/work/T8_jiuzhang3/
    gaussian_baseline_sampler_t8.py` (commit 60a92a8); JSON `jz30_gaussian_baseline_samples.json`
  - claude8 副 (this file): HOG + TVD-on-shared-support cross-check vs hafnian oracle

§D5 cross-validation logic (Option B level):
  - claude8 oracle gives EXACT click-pattern probabilities within Fock cutoff=4 captured-mass
    (sum_probs ≈ 0.293, n_subset=6).
  - claude5 sampler draws 10000 click samples per subset from analytical click distribution
    at the SAME Fock cutoff (verified bytewise: sum_probs ↔ matched exactly to 6 decimals).
  - Cross-check: claude5 empirical click distribution should match claude8 oracle on the
    captured-mass shared support, after renormalization `p_renorm = p / sum_probs`.

Three deliverables in this file:
  1. HOG (heavy-output generation): for each subset, compute fraction of claude5 samples
     whose oracle probability >= median oracle probability. Aaronson-Brod definition.
  2. TVD-on-shared-support: 0.5 * sum_x |P_claude5_empirical(x) - P_oracle_renorm(x)|.
  3. Markdown table summary for §D5 paper-grade cross-validation.

Extension hooks (deferred):
  - chi_corrected_path: NotImplementedError -- waits on claude5 oh_mps_sampler_t8.py M2-M5
    (cascade Option A path, post-spine)
  - torontonian_direct_sampling_path: NotImplementedError -- second-tier non-truncated §D5
  - claude2 d6ca180 leg: 20-mode subset, schema-misaligned with 6-mode oracle; pull-in
    for triple-impl §D5 requires schema-aligned re-run (not in scope this tick)

Status: Tick N+3 deliverable — final piece of cascade Option B sequence.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List

import numpy as np


CLAUDE5_PATH = "branches/claude5/work/T8_jiuzhang3/jz30_gaussian_baseline_samples.json"
CLAUDE8_ORACLE_PATH = "work/claude8/T8/jz30_hafnian_oracle.json"


def load_claude5_samples() -> Dict[str, Any]:
    """Read claude5 Gaussian baseline samples JSON via origin/claude5 (read-only)."""
    blob = subprocess.check_output(
        ["git", "show", f"origin/claude5:{CLAUDE5_PATH}"],
        text=True, encoding="utf-8",
    )
    return json.loads(blob)


def load_claude8_oracle() -> Dict[str, Any]:
    """Read claude8 hafnian oracle JSON locally (this branch)."""
    with open(CLAUDE8_ORACLE_PATH, "r") as f:
        return json.load(f)


def chi_corrected_path() -> None:
    """Reserved for cascade Option A: claude5 chi-corrected Oh-MPS sampler output."""
    raise NotImplementedError(
        "Cascade Option A deferred to §future work — see "
        "branches/claude5/work/T8_jiuzhang3/oh_mps_sampler_t8.py M2-M5 plan"
    )


def torontonian_direct_sampling_path() -> None:
    """Reserved for second-tier non-truncated §D5 cross-check."""
    raise NotImplementedError(
        "Torontonian-direct full-Fock §D5 deferred — second-tier paper §future work"
    )


def claude2_triple_impl_path() -> None:
    """Reserved for triple-impl §D5 (claude2 d6ca180 schema-aligned re-run required)."""
    raise NotImplementedError(
        "Triple-impl §D5 deferred — claude2 d6ca180 sampler is 20-mode subset, "
        "needs schema-aligned re-run at n_subset=6 to plug into 6-mode oracle"
    )


def empirical_click_dist(samples: List[List[int]], n_subset: int) -> Dict[tuple, float]:
    """Convert (n_samples, n_subset) binary array to empirical click pattern dict."""
    n = len(samples)
    counts: Dict[tuple, int] = {}
    for s in samples:
        c = tuple(s)
        counts[c] = counts.get(c, 0) + 1
    return {c: counts[c] / n for c in counts}


def renormalize_oracle(oracle_subset: Dict, n_subset: int) -> Dict[tuple, float]:
    """Convert oracle's click-pattern dict to renormalized {tuple: prob}."""
    raw = oracle_subset["all_click_probs"]  # {"01010" -> p}
    sum_p = oracle_subset["sum_probs"]
    out: Dict[tuple, float] = {}
    for k, v in raw.items():
        c = tuple(int(b) for b in k)
        out[c] = v / sum_p
    return out


def compute_tvd(emp: Dict[tuple, float], oracle: Dict[tuple, float]) -> float:
    """0.5 * sum_x |P_emp(x) - P_oracle(x)| over union of supports."""
    keys = set(emp.keys()) | set(oracle.keys())
    diff = sum(abs(emp.get(k, 0.0) - oracle.get(k, 0.0)) for k in keys)
    return 0.5 * diff


def compute_hog(samples: List[List[int]], oracle: Dict[tuple, float]) -> float:
    """Aaronson-Brod HOG: fraction of samples whose oracle prob >= median oracle prob."""
    probs_sorted = sorted(oracle.values())
    median_idx = len(probs_sorted) // 2
    median_p = probs_sorted[median_idx]
    above = sum(1 for s in samples if oracle.get(tuple(s), 0.0) >= median_p)
    return above / len(samples)


def main(out_path: str = "work/claude8/T8/hog_tvd_results.json") -> Dict[str, Any]:
    print("=== T8 hog_tvd_benchmark.py (Tick N+3) ===")
    c5 = load_claude5_samples()
    c8 = load_claude8_oracle()

    assert c5["n_subset"] == c8["n_subset"], "subset size mismatch"
    n_subset = c5["n_subset"]
    print(f"n_subset={n_subset}, c5 subsets={len(c5['subsets'])}, "
          f"c8 subsets={len(c8['subsets'])}")

    results: List[Dict[str, Any]] = []
    for c5_sub, c8_sub in zip(c5["subsets"], c8["subsets"]):
        # Sanity-check subset alignment via modes + sum_probs
        assert c5_sub["modes"] == c8_sub["modes"], (
            f"mode mismatch: c5={c5_sub['modes']} vs c8={c8_sub['modes']}"
        )
        assert abs(c5_sub["sum_probs_pre_renorm"] - c8_sub["sum_probs"]) < 1e-9, (
            f"sum_probs mismatch: c5={c5_sub['sum_probs_pre_renorm']} "
            f"vs c8={c8_sub['sum_probs']}"
        )

        oracle_renorm = renormalize_oracle(c8_sub, n_subset)
        emp = empirical_click_dist(c5_sub["samples"], n_subset)
        tvd = compute_tvd(emp, oracle_renorm)
        hog = compute_hog(c5_sub["samples"], oracle_renorm)

        results.append({
            "strategy": c5_sub["strategy"],
            "run_id": c5_sub["run_id"],
            "modes": c5_sub["modes"],
            "n_samples": len(c5_sub["samples"]),
            "sum_probs": c5_sub["sum_probs_pre_renorm"],
            "tvd_on_shared_support": tvd,
            "hog": hog,
            "n_oracle_patterns": len(oracle_renorm),
            "n_empirical_patterns": len(emp),
        })
        print(f"[{c5_sub['strategy']} run={c5_sub['run_id']}] modes={c5_sub['modes'][:4]}... "
              f"TVD={tvd:.5f}  HOG={hog:.5f}  sum_probs={c5_sub['sum_probs_pre_renorm']:.6f}")

    # Aggregate
    summary = {
        "tvd_mean": float(np.mean([r["tvd_on_shared_support"] for r in results])),
        "tvd_max": float(np.max([r["tvd_on_shared_support"] for r in results])),
        "hog_mean": float(np.mean([r["hog"] for r in results])),
        "hog_max_dev_from_half": float(
            np.max([abs(r["hog"] - 0.5) for r in results])
        ),
        "n_subsets": len(results),
        "n_samples_total": sum(r["n_samples"] for r in results),
    }
    output = {
        "schema_version": "1.0",
        "comparison": "claude5 60a92a8 Gaussian baseline vs claude8 540e632 hafnian oracle",
        "level": "Option B (Gaussian-baseline level §D5)",
        "results_per_subset": results,
        "summary": summary,
        "extension_hooks_recorded": [
            "chi_corrected_path (Option A, deferred §future work)",
            "torontonian_direct_sampling_path (second-tier §D5)",
            "claude2_triple_impl_path (schema-aligned re-run required)",
        ],
        "honest_scope": (
            "Option B level §D5 cross-check: validates Gaussian baseline sampler against "
            "exact hafnian oracle on captured-mass shared support (sum_probs ≈ 0.293 at "
            "Fock cutoff=4). Chi-corrected dual-impl is deferred work; framework wired up "
            "via NotImplementedError stubs."
        ),
    }
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSummary: TVD mean={summary['tvd_mean']:.5f}, max={summary['tvd_max']:.5f} | "
          f"HOG mean={summary['hog_mean']:.5f}, max|dev|={summary['hog_max_dev_from_half']:.5f}")
    print(f"wrote {out_path}")
    return output


def _smoke():
    main()


if __name__ == "__main__":
    _smoke()
