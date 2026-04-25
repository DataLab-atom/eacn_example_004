"""
T1 Path C v0.7: dual-chain scaling (adjacent vs LC-edge)

Combines two 3-point scaling chains from claude4 commits (21519b3 / a6b1697 / ddb5c05):
- Adjacent (M-B distance 1): 8q 4007 / 12q 3884 / 24q 255 terms
- LC-edge (M-B distance 2, Google Willow config): 8q 780 / 12q 780 / 24q 255 terms

Key observation: both chains CONVERGE at 24q wide grid (both give 255 terms).
At narrow grids (8q/12q), LC-edge has ~5x fewer terms than adjacent.
At wide grid (24q), once depth > M-B distance, distance ladder effect
diminishes because the light-cone has fully formed.

This is the data backing for claude4 Paper v0.2 R4:
"Google's choice of M-B placement, made to maximize quantum signal,
simultaneously minimizes the classical simulation cost."
"""
import json, numpy as np
from pathlib import Path

repo = Path(__file__).resolve().parent.parent

chains = {
    "Adjacent (d=1, scrambled worst case)": {
        "Ns": [8, 12, 24],
        "terms": [4007, 3884, 255],
        "hot_pct": [87.5, 50.0, 20.8],
        "sources": ["claude4 commit a6b1697 / 8q", "claude4 commit 21519b3 / 12q", "claude4 commit a6b1697 / 24q"],
    },
    "LC-edge (d=2, Google Willow config)": {
        "Ns": [8, 12, 24],
        "terms": [780, 780, 255],
        "sources": ["claude4 commit ddb5c05"],
    },
}

results = {}
for label, chain in chains.items():
    Ns = chain["Ns"]
    terms = chain["terms"]
    log_n = np.log(Ns)
    log_t = np.log(terms)
    slope, intercept = np.polyfit(log_n, log_t, 1)
    # R² is trivially near 1 for 3-point linear fit (caveat per REV-T1-002 v0.2 M-2)
    pred = slope * log_n + intercept
    r2 = 1 - np.sum((log_t - pred)**2) / max(np.sum((log_t - np.mean(log_t))**2), 1e-12)
    Willow_terms = np.exp(intercept) * (65 ** slope)
    results[label] = {
        "slope": slope,
        "intercept": intercept,
        "R2_formal_not_statistical": r2,
        "data": list(zip(Ns, terms)),
        "Willow_65q_proj_terms": float(Willow_terms),
    }
    print(f"{label}:")
    print(f"  data points: {list(zip(Ns, terms))}")
    print(f"  slope = {slope:.3f} (R² = {r2:.4f} — formal 3-point fit, statistical CI needs 4-5 pts)")
    for N_p in [36, 65, 100]:
        t_p = np.exp(intercept) * (N_p ** slope)
        print(f"  N={N_p}: terms ≈ {t_p:.1f}")
    print()

# Summary table
print("=" * 60)
print("Willow 65q projections (two independent chains):")
for label, res in results.items():
    print(f"  {label}: ~{res['Willow_65q_proj_terms']:.1f} terms")
print()
print("Key observation: Both chains CONVERGE at 24q wide grid (255 terms).")
print("LC-edge projection (~96 terms @ 65q) matches claude4 Paper v0.2 R4")
print("'fewer than 100 Pauli terms' claim with dual-chain data backing.")

out_path = repo / "results" / "T1" / "hotspot_v07_dual_chain.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
out = {
    "method": "dual-chain power-law fit; adjacent and LC-edge M-B configurations",
    "caveat": "3-point fits per chain; R² trivially near 1 for log-log-linear data; confidence intervals require 4-5 points",
    "chains": results,
    "convergence": {
        "at_N_24": "both chains give 255 terms; distance ladder effect diminishes at wide grids where light-cone has fully formed",
        "at_narrow": "LC-edge has ~5x fewer terms than adjacent at 8q/12q",
    },
    "paper_implications": "supports claude4 Paper v0.2 R4 '<100 terms @ 65q LC-edge' with empirical dual-chain backing",
}
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)
print(f"\n-> {out_path}")
