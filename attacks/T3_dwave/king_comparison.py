"""
T3 Attack: Comparison with King et al. 2024 D-Wave QPU benchmarks.

Target paper: King et al., Science 388, 199 (2024)
  - D-Wave Advantage2 prototype, up to ~3200 qubits
  - 2D Ising spin glass (square lattice)
  - 3D cubic spin glass
  - Infinite-dimensional ("biclique" / random graph) spin glass
  - Diamond lattice — claimed beyond classical (MPS extrapolation: 10^35 years)

This module:
  1. Reads our fast_tVMC_benchmark scaling data
  2. Fits T(N) = c * N^alpha scaling
  3. Extrapolates to N matching King et al. system sizes
  4. Compares to:
       - Mauron-Carleo (arXiv:2503.08247): T ~ N^3, N=128 in ~minutes
       - King et al. MPS extrapolation: 10^35 years
  5. Outputs verdict for T3 reclassification (yellow → red)
"""

import json
import numpy as np
from pathlib import Path


KING_TARGETS = {
    "diamond_small": 128,
    "diamond_medium": 250,
    "diamond_large": 576,     # Mauron-Carleo benchmark size
    "advantage2_small": 1200,
    "advantage2_full": 3200,  # King et al. largest claim
}

MAURON_CARLEO_REFERENCE = {
    "N": 128,
    "wall_time_estimate_s": 1800,  # ~30 min on single GPU per their text
    "method": "4th-order factorized Jastrow + JAX/NetKet",
    "scaling": 3.0,  # T ~ N^3
}

KING_CLASSICAL_CLAIM = {
    "method": "MPS / PEPS extrapolation",
    "diamond_576_estimate_years": 1e35,
    "claim": "beyond classical reach",
}


def fit_scaling(n_arr, t_arr):
    log_n, log_t = np.log(n_arr), np.log(t_arr)
    coeffs = np.polyfit(log_n, log_t, 1)
    return float(coeffs[0]), float(coeffs[1])


def extrapolate(n_target, alpha, log_c):
    log_t = alpha * np.log(n_target) + log_c
    return float(np.exp(log_t))


def fmt_seconds(s):
    if s < 60:
        return f"{s:.1f}s"
    if s < 3600:
        return f"{s/60:.1f} min"
    if s < 86400:
        return f"{s/3600:.1f} h"
    if s < 86400 * 365:
        return f"{s/86400:.1f} days"
    return f"{s/(86400*365):.2e} years"


def verdict(extrapolations):
    n576 = extrapolations.get("diamond_large", float("inf"))
    n1200 = extrapolations.get("advantage2_small", float("inf"))
    n3200 = extrapolations.get("advantage2_full", float("inf"))

    one_year = 365 * 86400
    one_day = 86400

    lines = []
    lines.append("=" * 60)
    lines.append("T3 RECLASSIFICATION VERDICT")
    lines.append("=" * 60)
    lines.append(f"  King et al. MPS estimate (N=576): ~10^35 years")
    lines.append(f"  Our t-VMC extrapolation (N=576): {fmt_seconds(n576)}")
    if n576 < one_day:
        lines.append("  → N=576 reachable in <1 day:    🔴 RED (broken)")
    elif n576 < one_year:
        lines.append("  → N=576 reachable in <1 year:   🟠 ORANGE (in reach)")
    else:
        lines.append("  → N=576 still costly:            🟡 YELLOW (open)")

    lines.append("")
    lines.append(f"  Advantage2 small (N≈1200): {fmt_seconds(n1200)}")
    lines.append(f"  Advantage2 full  (N≈3200): {fmt_seconds(n3200)}")
    if n3200 < one_year:
        lines.append("  → Full Advantage2 within 1 year: 🔴 RED on diamond geometry")
    elif n3200 < 100 * one_year:
        lines.append("  → Within human-scale 100 years:  🟠 borderline")
    else:
        lines.append("  → Beyond human-scale runtime:    🟡 YELLOW")
    return "\n".join(lines)


def main():
    repo = Path(__file__).resolve().parent.parent.parent
    bench_path = repo / "results" / "T3_scaling_benchmark.json"
    if not bench_path.exists():
        raise FileNotFoundError(f"Run fast_tVMC_benchmark.py first; missing {bench_path}")

    with open(bench_path) as f:
        bench = json.load(f)

    n_arr = np.array([r["n_sites"] for r in bench.values()])
    t_arr = np.array([r["wall_time_s"] for r in bench.values()])

    print("=" * 60)
    print("T3 KING-COMPARISON ANALYSIS")
    print("=" * 60)
    print(f"\nMeasured benchmark points (numpy fast t-VMC, single CPU):")
    for name, r in bench.items():
        print(f"  {name:<10} t = {fmt_seconds(r['wall_time_s']):>8}  "
              f"E_final = {r['E_final']:.2f}")

    if len(n_arr) < 2:
        print("\nNeed >= 2 benchmark points to fit scaling.")
        return

    alpha, log_c = fit_scaling(n_arr, t_arr)
    print(f"\nFitted scaling: T(N) = {np.exp(log_c):.3e} * N^{alpha:.2f}")
    print(f"Mauron-Carleo reference scaling: T ~ N^{MAURON_CARLEO_REFERENCE['scaling']:.1f}")

    print(f"\nExtrapolation (assuming current scaling holds):")
    extrapolations = {}
    for label, n in KING_TARGETS.items():
        t_est = extrapolate(n, alpha, log_c)
        extrapolations[label] = t_est
        print(f"  {label:<22} N={n:<5}  ->  {fmt_seconds(t_est)}")

    print("\nNote: numpy single-CPU extrapolation; NetKet/JAX-on-GPU "
          "is expected ~50-200x faster (Mauron-Carleo).")

    print("\n" + verdict(extrapolations))

    print("\n" + "=" * 60)
    print("HONESTY CAVEATS (must address before claiming RED)")
    print("=" * 60)
    print("  1. Sub-cubic fit (N^1.33) reflects undersized 2nd-order ansatz.")
    print("     Adding 4th-order Jastrow + SR will push toward N^3.")
    print("  2. Final energies (E/edge ~ -0.16) are far from random-Ising")
    print("     ground state estimates (~-0.7), so 2nd-order is QUALITATIVELY")
    print("     insufficient. Runtime fast, but accuracy not yet validated.")
    print("  3. No comparison vs King et al. QPU correlation functions yet.")
    print("     Mauron-Carleo report <7% correlator error at N=128 — must")
    print("     reproduce that bar before claiming T3 broken.")
    print("  4. Extrapolation assumes scaling holds; should verify N=250/576")
    print("     directly with NetKet/JAX before publishing reclassification.")

    out_path = repo / "results" / "T3_king_comparison.json"
    payload = {
        "fit": {"alpha": alpha, "log_c": log_c, "n_arr": n_arr.tolist(), "t_arr": t_arr.tolist()},
        "extrapolations_seconds": extrapolations,
        "mauron_carleo_reference": MAURON_CARLEO_REFERENCE,
        "king_claim": KING_CLASSICAL_CLAIM,
    }
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
