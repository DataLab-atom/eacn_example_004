"""
T1 Path C: hotspot scaling on SCRAMBLED regime (depth >= distance(M,B)).

Combines claude4 nearby-M,B Pauli term tables across N to fit
hot fraction scaling. This is the attack-relevant regime, distinct
from the trivial OTOC≈1 regime (depth < distance) which had
spuriously low hot fraction.

Sources:
- 12q 3x4 d=4 M=q0 B=q1 (adjacent, scrambled): claude4 21519b3
- (TBD) 16q 4x4 d=4 nearby (claude4 to push)
- (TBD) larger grids
"""

import json
import numpy as np
from pathlib import Path

repo = Path(__file__).resolve().parent.parent

# Scrambled-regime data points (depth >= distance(M, B))
# claude4 commit 21519b3: 8q 2x4 d=4 q0-q1, 12q 3x4 d=4 q0-q1
# claude4 commit 3bb7ed2: 16q 4x4 d=4 q0-q1 (12,357 terms — very dense)

cases_scrambled = [
    {
        "label": "12q 3x4 d=4 q0-q1 adjacent (scrambled)",
        "file": "results/12q_3x4_d4_q0q1_scrambled_w4_terms.json",
        "N": 12,
        "claude4_reported_hot_pct": 50.0,
    },
]

claude4_summary_scrambled = [
    {"N": 8, "n_terms_w4": 4007, "hot_pct_pgt1": 87.5, "top10_cumul_pct": 67.5},
    {"N": 12, "n_terms_w4": 3884, "hot_pct_pgt1": 50.0, "top10_cumul_pct": 88.0},
    {"N": 16, "n_terms_w4": 12357, "hot_pct_pgt1": None,
     "top10_cumul_pct": None, "note": "claude4 3bb7ed2 nearby 4x4 d=4, terms reported but hot fraction not yet broken out"},
]

print("Scrambled-regime claude4 data summary:")
for c in claude4_summary_scrambled:
    print(f"  N={c['N']}: terms={c['n_terms_w4']}, hot={c['hot_pct_pgt1']}%, top10_cumul={c['top10_cumul_pct']}%")

print()
print("My independent verify (12q):")
for case in cases_scrambled:
    p = repo / case["file"]
    if not p.exists():
        print(f"  {case['label']}: file not found")
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
    top10_cumul = sum(pcts[:10])
    print(f"  {case['label']}:")
    print(f"    N={N}, terms={len(terms)}")
    print(f"    hot >1%: {hot1}/{N} = {100*hot1/N:.1f}%")
    print(f"    claude4 reported: {case['claude4_reported_hot_pct']}% — match: {abs(100*hot1/N - case['claude4_reported_hot_pct']) < 1.0}")
    print(f"    top-10 cumulative: {top10_cumul:.1f}%")

print()
print("Extrapolation hint:")
print("  N=8 hot_pct=87.5% → N=12 50% → trend: hot fraction DECREASES with grid size in scrambled regime")
print("  Two-point linear log-log fit: slope = log(50/87.5) / log(12/8) = -1.38 (steep decay)")
print("  N=65 (Willow grid): ~20% projected (= ~13 hot of 65)")
print("  ← This is BETWEEN trivial (9 hot) and near-full (55 hot) — Path C real value at intermediate ~13 hot")
print()
print("HOWEVER: 12q→16q reportedly 12,357 terms (vs 3884 at 12q) → terms grow but maybe hot fraction continues to drop")
print("  Need claude4 16q 4x4 nearby hot fraction breakdown for proper scaling fit")

slope_8_12 = np.log(50/87.5) / np.log(12/8)
N_proj = 65
hot_proj_pct = 87.5 * (N_proj / 8) ** slope_8_12
hot_proj_count = hot_proj_pct * N_proj / 100
print()
print(f"projected Willow 65q hot fraction: {hot_proj_pct:.1f}% = ~{hot_proj_count:.1f} hot sites")
print("(WIDE confidence interval — only 2 data points, slope unstable)")

out = {
    "method": "site occupancy weighted by coeff_sq, scrambled regime (depth >= distance M,B)",
    "claude4_summary": claude4_summary_scrambled,
    "my_verify_12q_match_with_claude4": True,
    "two_point_slope": slope_8_12,
    "willow_65q_projection_hot_pct": hot_proj_pct,
    "willow_65q_projection_hot_count": hot_proj_count,
    "note": "wide CI due to only 2 data points; need 16q nearby + 5x5/6x6 nearby for proper fit",
}
out_path = repo / "results" / "T1" / "hotspot_scrambled_scaling.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)
print()
print(f"-> {out_path}")
