"""
T1 Path C hotspot scaling: 4x4 vs 6x6 vs (TBD 8x8) Pauli weight concentration.

Scans claude4-exported Pauli term files of varying grid size and
quantifies how the "hot fraction" (sites with >1% occupancy)
scales with N. Linear extrapolation projects the active sub-grid
size for Willow ~10x10 to inform Path C complexity estimate.
"""

import json
import numpy as np
from pathlib import Path

repo = Path(__file__).resolve().parent.parent

cases = [
    {"file": "results/16q_4x4_d4_pauli_terms.json", "N": 16, "grid": "4x4"},
    {"file": "results/6x6_d4_pauli_terms.json", "N": 36, "grid": "6x6"},
]

results = []
for c in cases:
    p = repo / c["file"]
    if not p.exists():
        continue
    d = json.load(open(p))
    terms = d["terms"]
    N = d["n_qubits"]
    occ = np.zeros(N)
    for t in terms:
        for s in t["sites"]:
            occ[s] += t["coeff_sq"]
    total = sum(t["coeff_sq"] for t in terms)
    pcts = sorted([100 * o / total for o in occ], reverse=True)
    hot1 = sum(1 for p in pcts if p > 1.0)
    hot5 = sum(1 for p in pcts if p > 5.0)
    results.append({
        "grid": c["grid"],
        "N": N,
        "n_terms": len(terms),
        "max_weight": d.get("max_weight"),
        "hot_above_1pct": hot1,
        "hot_above_5pct": hot5,
        "hot_fraction_pct": 100 * hot1 / N,
        "top_5_sites_pct_each": pcts[:5],
        "M_q": d["obs_q"],
        "B_q": d["pert_q"],
    })

print("Hotspot scaling across grid sizes (4x4, 6x6):")
print()
for r in results:
    print(f"  {r['grid']} N={r['N']:2d} terms={r['n_terms']:4d}: "
          f"{r['hot_above_1pct']}/{r['N']} hot ({r['hot_fraction_pct']:.1f}%) | "
          f"top-5: {[f'{p:.1f}%' for p in r['top_5_sites_pct_each']]}")

if len(results) >= 2:
    fractions = [r["hot_fraction_pct"] for r in results]
    Ns = [r["N"] for r in results]
    print()
    print(f"Linear log-log fit (hot_pct vs N):")
    if len(results) == 2:
        log_n = np.log(Ns)
        log_f = np.log(fractions)
        slope = (log_f[1] - log_f[0]) / (log_n[1] - log_n[0])
        intercept = log_f[0] - slope * log_n[0]
        print(f"  slope = {slope:.3f}")
        print(f"  hot_pct(N) ≈ {np.exp(intercept):.2f} × N^{slope:.3f}")
        for N_proj in [64, 65, 81, 100]:
            pct = np.exp(intercept) * (N_proj ** slope)
            count = pct * N_proj / 100
            print(f"  N={N_proj:3d}: hot_pct ≈ {pct:.1f}% → ~{count:.1f} hot sites")

out_path = repo / "results" / "T1" / "hotspot_scaling.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w") as f:
    json.dump({
        "method": "occupancy = Σ coeff_sq × 1[site in term]; hot = occupancy > 1%",
        "cases": results,
        "extrapolation": "log-log slope from 2 grid points; linear fit only",
        "note": "Two data points → trend not robust; need 8x8 d=4 for cubic fit",
    }, f, indent=2)
print()
print(f"-> {out_path}")
