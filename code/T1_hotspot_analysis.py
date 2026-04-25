"""
T1 Path C hotspot analysis: site occupancy weighted by coeff_sq.

Reads claude4 results/16q_4x4_d4_pauli_terms.json (commit 0775fa7),
computes for each of 16 sites (4x4 grid):
  occupancy[i] = sum_{terms} coeff_sq[t] * 1[site i in term[t].sites]

This identifies the "hot" sub-grid where Pauli weight concentrates,
which is the locus where Path C adaptive top-K refine should focus.

M = observable Z on q0, B = perturbation X on q15 (4x4 corner-to-corner).
"""

import json
import numpy as np
from pathlib import Path

repo = Path(__file__).resolve().parent.parent
data = json.load(open(repo / "results" / "16q_4x4_d4_pauli_terms.json"))

terms = data["terms"]
n_qubits = data["n_qubits"]
M_q, M_p = data["obs_q"], data["obs_p"]
B_q, B_p = data["pert_q"], data["pert_p"]

occupancy = np.zeros(n_qubits)
for t in terms:
    c2 = t["coeff_sq"]
    for s in t["sites"]:
        occupancy[s] += c2

total_norm = sum(t["coeff_sq"] for t in terms)
weight_count = {}
for t in terms:
    w = t["weight"]
    weight_count[w] = weight_count.get(w, 0) + 1

print(f"n_qubits={n_qubits}, n_terms={len(terms)}, total Σcoeff² = {total_norm:.4f}")
print(f"Observable M = {M_p} on q{M_q}; Perturbation B = {B_p} on q{B_q}")
print(f"Weight distribution: {dict(sorted(weight_count.items()))}")
print()
print("Site occupancy (Σ coeff² × 1[site in term]):")
print()
print("  4x4 grid layout (site → occupancy / total_norm × 100%):")
print()
for r in range(4):
    row = []
    for c in range(4):
        i = r * 4 + c
        pct = 100 * occupancy[i] / total_norm
        marker = " M" if (i == M_q) else ("B" if i == B_q else "  ")
        row.append(f"  q{i:2d}{marker}: {pct:5.1f}%")
    print("  " + " | ".join(row))

print()
ranked = sorted(enumerate(occupancy), key=lambda x: -x[1])
print("Ranked sites (occupancy %):")
for rank, (site, occ) in enumerate(ranked, start=1):
    pct = 100 * occ / total_norm
    print(f"  #{rank:2d}  q{site:2d}: occ={occ:.4f} ({pct:.1f}%)")

cumulative = sum(occupancy)
top4_occ = sum(o for _, o in ranked[:4])
top8_occ = sum(o for _, o in ranked[:8])
print()
print(f"Top-4 sites carry {100*top4_occ/cumulative:.1f}% of total occupancy")
print(f"Top-8 sites carry {100*top8_occ/cumulative:.1f}% of total occupancy")

light_cone_path = [0, 5, 10, 15]
light_cone_occ = sum(occupancy[s] for s in light_cone_path)
diag1_path = [0, 7, 14]
diag1_occ = sum(occupancy[s] for s in diag1_path)
print()
print(f"Diagonal q0→q5→q10→q15 ({len(light_cone_path)} sites): {100*light_cone_occ/cumulative:.1f}%")
print(f"Path q0→q7→q14 ({len(diag1_path)} sites, top term path): {100*diag1_occ/cumulative:.1f}%")

out = {
    "source_commit": "0775fa7 (claude4 origin/claude4)",
    "method": "site occupancy weighted by coeff_sq, summed over all 233 terms",
    "n_qubits": n_qubits,
    "grid": data["grid"],
    "depth": data["depth"],
    "M": {"qubit": M_q, "pauli": M_p},
    "B": {"qubit": B_q, "pauli": B_p},
    "total_coeff_sq_norm": total_norm,
    "occupancy_per_site": [{"site": i, "occupancy": float(occupancy[i]),
                            "fraction_pct": float(100 * occupancy[i] / cumulative)}
                           for i in range(n_qubits)],
    "ranked_sites_by_occupancy": [
        {"rank": r, "site": s, "occupancy": float(o),
         "fraction_pct": float(100 * o / cumulative)}
        for r, (s, o) in enumerate(ranked, start=1)
    ],
    "concentration_metrics": {
        "top4_fraction_pct": float(100 * top4_occ / cumulative),
        "top8_fraction_pct": float(100 * top8_occ / cumulative),
        "diagonal_0_5_10_15_fraction_pct": float(100 * light_cone_occ / cumulative),
        "path_0_7_14_fraction_pct": float(100 * diag1_occ / cumulative),
    },
    "interpretation": (
        "Hot sub-grid = top-K sites by occupancy. Path C adaptive refine "
        "focuses K_max budget on hot cluster; cold sites use baseline K_global. "
        "If top-K sites carry >80% of occupancy, Path C constant-factor speedup "
        "= |grid| / |hot|. For 4x4 d=4 with M=q0, B=q15, light-cone path "
        "q0→q5→q10→q15 vs full 16-site adaptive cost."
    ),
}

out_path = repo / "results" / "T1" / "path_c_hotspot_analysis_N16.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)

print()
print(f"-> {out_path}")
