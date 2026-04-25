"""
Pauli weight tail analysis for T1 SPD/Pauli-path attack feasibility.

Reads claude4's exported Pauli term JSON files via `git show origin/claude4:<path>`
to avoid copying peer artifacts into the claude8 branch (branch-fence compliant).

For each file (3 cases below), computes:
  (a) Spatial distribution: per-qubit count of non-trivial Pauli factors.
  (b) Cumulative |c|^2 vs rank curve.
  (c) Tail-decay fit: exponential vs power-law on sorted |c|^2.
  (d) Direct comparison scrambled vs unscrambled (same n_qubits = 8).

Output: writes a markdown summary to stdout for capture into
`work/claude8/T1/phase0b_results/tail_analysis_v1.md`.

Caveats (per claude4 commit messages):
  - All inputs are NOISELESS SPD evolutions.
  - 8q cases are small enough that n_eff ≈ n (limited geometric room for
    hotspot rescue). 16q is unscrambled (distant M,B) only — claude4 16q
    scrambled exhausted RAM (>8GB).
  - Tail behaviour at 8q may not extrapolate cleanly to 65q on 8x8 / 9x9
    grids; this analysis is DIAGNOSTIC, not predictive of Willow scale.

References:
  Schuster, Yin, Gao, Yao 2024 (arXiv:2407.12768) — predicts exponential tail
    decay under noise; noiseless circuits expected power-law tails.
  Begusic, Gray, Chan 2024 (Sci. Adv. 10, eadk4321) — SPD baseline.
  claude4 commits: 1f511ee / 0775fa7 / 3bb7ed2 / 575b59b.
"""

from __future__ import annotations

import json
import math
import subprocess
from collections import Counter
from typing import Dict, List, Tuple

import numpy as np


CASES = [
    {
        "tag": "16q_4x4_unscrambled_d=4_distant_M-B",
        "path": "results/16q_4x4_d4_pauli_terms.json",
        "n_qubits": 16,
        "depth": 4,
        "scrambled": False,
        "expected_terms": 233,
    },
    {
        "tag": "8q_2x4_unscrambled_d=4_distant(q0,q7)",
        "path": "results/8q_2x4_d4_q0q7_distant_d5_terms.json",
        "n_qubits": 8,
        "depth": 4,
        "scrambled": False,
        "expected_terms": 1023,
    },
    {
        "tag": "8q_2x4_scrambled_d=4_adjacent(q0,q1)",
        "path": "results/8q_2x4_d4_q0q1_adjacent_d1_terms.json",
        "n_qubits": 8,
        "depth": 4,
        "scrambled": True,
        "expected_terms": 4007,
    },
    {
        # 4th case (added in v2): 6x6 grid d=4 unscrambled distant — completes
        # the 4q?/8q/16q/36q n-scaling chain for slope-vs-n extrapolation.
        # Path: results/6x6_d4_pauli_terms.json on origin/claude4 commit 2477bac.
        "tag": "36q_6x6_unscrambled_d=4_distant(q0,q35)",
        "path": "results/6x6_d4_pauli_terms.json",
        "n_qubits": 36,
        "depth": 4,
        "scrambled": False,
        "expected_terms": 3839,
    },
    {
        # 5th case (added in v3): 12q 3x4 d=4 scrambled adjacent (q0,q1) —
        # closes the critical 8q→12q→(?16q OOM) scrambled n-scaling gap.
        # Path: results/12q_3x4_d4_q0q1_scrambled_w4_terms.json on origin/claude4
        # commit 21519b3. Preview: 3884 terms, hot 6/12, top-10 88% (lighter
        # tail than 8q scrambled — supports "wider grid concentrates more").
        "tag": "12q_3x4_scrambled_d=4_adjacent(q0,q1)",
        "path": "results/12q_3x4_d4_q0q1_scrambled_w4_terms.json",
        "n_qubits": 12,
        "depth": 4,
        "scrambled": True,
        "expected_terms": 3884,
    },
    {
        # 6th case (added in v4): 24q 4x6 d=4 scrambled adjacent. claude4
        # commit a6b1697. Striking result: term count DROPS from 4007/3884
        # to just 255 — wider grid concentrates AND prunes simultaneously.
        # Hot ratio 21%, top-10 96.7%. This is the third scrambled scaling
        # point (after 8q, 12q) and provides reliable n-extrapolation toward 65q.
        "tag": "24q_4x6_scrambled_d=4_adjacent(q0,q1)",
        "path": "results/24q_4x6_d4_scrambled_w4_terms.json",
        "n_qubits": 24,
        "depth": 4,
        "scrambled": True,
        "expected_terms": 255,
    },
]


def load_via_git(path: str) -> dict:
    out = subprocess.run(
        ["git", "show", f"origin/claude4:{path}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(out.stdout)


def extract_terms(data: dict) -> List[Tuple[str, float, List[int]]]:
    """
    Returns list of (pauli_string, |c|^2, sites_touched) tuples.
    Schema per claude4: {"pauli_string", "weight", "coeff_sq", "sites"}
    or might be wrapped in a top-level "terms" array — handle both.
    """
    if isinstance(data, dict) and "terms" in data:
        terms_list = data["terms"]
    elif isinstance(data, list):
        terms_list = data
    else:
        # try common alternates
        for k in ("pauli_terms", "items", "data"):
            if k in data:
                terms_list = data[k]
                break
        else:
            raise KeyError(f"no terms array; top-level keys = {list(data.keys())[:10]}")

    out = []
    for t in terms_list:
        ps = t.get("pauli_string", t.get("string", ""))
        c2 = float(t.get("coeff_sq", t.get("c2", t.get("|c|^2", 0.0))))
        sites = t.get("sites", t.get("support", []))
        if not sites and ps:
            sites = [i for i, ch in enumerate(ps) if ch != "I"]
        out.append((ps, c2, sites))
    return out


def site_distribution(terms, n_qubits: int) -> List[int]:
    counts = Counter()
    for _ps, _c2, sites in terms:
        counts.update(sites)
    return [counts.get(i, 0) for i in range(n_qubits)]


def cumulative_curve(terms) -> Tuple[np.ndarray, np.ndarray, float]:
    c2s = np.array(sorted((t[1] for t in terms), reverse=True), dtype=float)
    total = float(c2s.sum())
    cum = np.cumsum(c2s) / total if total > 0 else np.cumsum(c2s)
    return c2s, cum, total


def fit_tail(sorted_c2: np.ndarray, *, head_skip: int = 5):
    """
    Fit log10(|c|^2) versus:
      - rank (linear: exponential decay)
      - log10(rank+1) (linear: power-law decay)
    Skip the top `head_skip` to avoid head dominating the fit.
    Return (exp_slope, exp_R2, power_slope, power_R2).
    """
    if len(sorted_c2) < head_skip + 8:
        return None
    y = np.log10(np.maximum(sorted_c2[head_skip:], 1e-300))
    rank = np.arange(head_skip + 1, len(sorted_c2) + 1, dtype=float)
    log_rank = np.log10(rank)

    def linfit(x):
        m, b = np.polyfit(x, y, 1)
        ypred = m * x + b
        ss_res = float(np.sum((y - ypred) ** 2))
        ss_tot = float(np.sum((y - y.mean()) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        return float(m), float(r2)

    exp_slope, exp_r2 = linfit(rank)
    power_slope, power_r2 = linfit(log_rank)
    return exp_slope, exp_r2, power_slope, power_r2


def coverage_at(cum: np.ndarray, k: int) -> float:
    if k - 1 >= len(cum):
        return float(cum[-1]) if len(cum) else float("nan")
    return float(cum[k - 1])


def hotspot_share(site_counts: List[int], top_k: int = None) -> Tuple[List[int], float]:
    n = len(site_counts)
    total = sum(site_counts)
    if top_k is None:
        # define hot as count >= 50% of max
        thresh = max(site_counts) * 0.5
        hot_sites = [i for i, c in enumerate(site_counts) if c >= thresh]
    else:
        ranked = sorted(range(n), key=lambda i: -site_counts[i])
        hot_sites = ranked[:top_k]
    hot_count = sum(site_counts[i] for i in hot_sites)
    share = hot_count / total if total > 0 else 0.0
    return hot_sites, share


def analyse(case: Dict) -> Dict:
    raw = load_via_git(case["path"])
    terms = extract_terms(raw)
    n = case["n_qubits"]
    site_counts = site_distribution(terms, n)
    sorted_c2, cum, total_norm = cumulative_curve(terms)
    fit = fit_tail(sorted_c2)
    cov_top1 = coverage_at(cum, 1)
    cov_top10 = coverage_at(cum, 10)
    cov_top100 = coverage_at(cum, 100)
    n_terms = len(terms)
    cov_top_pct = coverage_at(cum, max(1, n_terms // 100))
    hot_sites_p50, hot_share_p50 = hotspot_share(site_counts)
    return {
        "tag": case["tag"],
        "scrambled": case["scrambled"],
        "n_qubits": n,
        "n_terms": n_terms,
        "expected_terms": case["expected_terms"],
        "total_norm": total_norm,
        "cov_top1": cov_top1,
        "cov_top10": cov_top10,
        "cov_top100": cov_top100,
        "cov_top1pct": cov_top_pct,
        "site_counts": site_counts,
        "hot_sites_p50": hot_sites_p50,
        "hot_share_p50": hot_share_p50,
        "fit": fit,
    }


def fmt_pct(x: float) -> str:
    return f"{100*x:.2f}%" if not math.isnan(x) else "NaN"


def md_report(results: List[Dict]) -> str:
    lines = [
        "# Pauli weight tail analysis — Phase 0b cross-check",
        "",
        "**Source**: claude4 JSON exports on `origin/claude4` (commits `0775fa7` 16q,",
        "`575b59b` 8q pair). Loaded via `git show origin/claude4:<path>` — NOT copied",
        "into the claude8 branch (branch-fence compliant).",
        "",
        "**Caveat**: all inputs are NOISELESS SPD outputs. 8q cases have n_eff ≈ n",
        "trivially. 16q is unscrambled distant M-B only — 16q scrambled OOM'd on",
        "8 GB. Conclusions are DIAGNOSTIC, not predictive of 65q Willow scale.",
        "",
        "## Summary table",
        "",
        "| Case | terms | top-1 |c|^2 | top-10 |c|^2 | top-100 |c|^2 | hot sites (p50) | hot share | tail fit (R^2 exp / R^2 pow) |",
        "|---|---:|---:|---:|---:|---|---:|---|",
    ]
    for r in results:
        fit = r["fit"]
        fitstr = "—"
        if fit is not None:
            exp_m, exp_r2, pow_m, pow_r2 = fit
            fitstr = f"exp R²={exp_r2:.3f} / pow R²={pow_r2:.3f}"
        lines.append(
            f"| {r['tag']} | {r['n_terms']} | {fmt_pct(r['cov_top1'])} "
            f"| {fmt_pct(r['cov_top10'])} | {fmt_pct(r['cov_top100'])} "
            f"| {len(r['hot_sites_p50'])}/{r['n_qubits']} | {fmt_pct(r['hot_share_p50'])} "
            f"| {fitstr} |"
        )
    lines.append("")
    for r in results:
        lines.append(f"### {r['tag']}")
        lines.append(f"- terms: {r['n_terms']} (expected {r['expected_terms']})")
        lines.append(f"- total norm Σ|c|²: {r['total_norm']:.6g}")
        lines.append(
            f"- cumulative coverage: top-1 {fmt_pct(r['cov_top1'])}, "
            f"top-10 {fmt_pct(r['cov_top10'])}, top-100 {fmt_pct(r['cov_top100'])}, "
            f"top-1% (k={max(1, r['n_terms']//100)}) {fmt_pct(r['cov_top1pct'])}"
        )
        lines.append(
            f"- per-qubit support count: {r['site_counts']}"
        )
        lines.append(
            f"- hot sites (count ≥ 50% of max site count): "
            f"{r['hot_sites_p50']} ({len(r['hot_sites_p50'])}/{r['n_qubits']}) "
            f"carrying {fmt_pct(r['hot_share_p50'])} of total support count"
        )
        if r["fit"] is not None:
            exp_m, exp_r2, pow_m, pow_r2 = r["fit"]
            verdict = (
                "tail = EXPONENTIAL" if exp_r2 > pow_r2 + 0.05
                else "tail = POWER-LAW" if pow_r2 > exp_r2 + 0.05
                else "ambiguous (R² close)"
            )
            lines.append(
                f"- tail fit (skip top-5): "
                f"log|c|² ~ exp slope={exp_m:.3g} (R²={exp_r2:.3f}); "
                f"log|c|² ~ pow slope={pow_m:.3g} (R²={pow_r2:.3f}) → **{verdict}**"
            )
        else:
            lines.append("- tail fit: skipped (too few terms)")
        lines.append("")
    return "\n".join(lines)


def main():
    results = [analyse(c) for c in CASES]
    print(md_report(results))


if __name__ == "__main__":
    main()
