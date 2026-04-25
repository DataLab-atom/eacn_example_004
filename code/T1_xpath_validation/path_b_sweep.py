"""
Path B (claude8 Schuster-Yin Pauli-path) numerical sweep.

Runs claude8's run_schuster_pauli_path_attack across 12q 3x4 d=2/4/6 with
ell=4 weight bound, M=Z@q3 B=X@q4, to triangulate against:
  - Path A (claude4 SPD heavy-trunc) reproduction in path_a_corrected.py
  - Path C (claude7 v0.10 measurement-derived top-K) cost projection
"""
import sys, os
sys.path.insert(0, r'E:\qut\7\eacn_example_004\work\claude8\T1')
from pauli_path_baseline import run_schuster_pauli_path_attack

print("=" * 78)
print("PATH B SWEEP (claude8 Schuster-Yin Pauli-path) -- 12q 3x4 LC-edge")
print("=" * 78)

# Note: claude8 brickwall uses iSWAP+sqrt(W)+sqrt(X)+sqrt(Y) gate set
# (Bermejo II.1.3). Path A uses CZ+random-SU(2). The two are NOT structurally
# identical at the gate level but BOTH are universal random circuits, so the
# cross-validation question is: at fixed (n, d, ell), do the structural metrics
# (n_kept, max_weight, frobenius_norm_sq, identity_fraction) align?

configs = [
    # (grid, d, M, B, ell)
    ((3, 4), 2, 3, 4, 8),
    ((3, 4), 2, 3, 4, 4),
    ((3, 4), 4, 3, 4, 8),
    ((3, 4), 4, 3, 4, 4),
    ((3, 4), 6, 3, 4, 8),
    ((3, 4), 6, 3, 4, 4),
]

print("\n%-22s | %s" % ("config", "n_kept | OTOC2     | fro2     | max_w | mean_w | id_frac"))
print("-" * 90)

for grid, d, M, B, ell in configs:
    try:
        r = run_schuster_pauli_path_attack(grid, d, M, B, ell, seed=42)
        cm = r.circuit_meta
        config_str = f"{grid[0]}x{grid[1]} d={d} ell={ell}"
        print(f"{config_str:<22s} | {r.n_pauli_strings_kept:6d} | {cm['otoc2_value']:+.4f}    | {cm['frobenius_norm_sq']:.4f}   | {cm['max_weight_observed']:5d} | {cm['mean_weight_observed']:.3f}  | {cm['identity_fraction']:.4f}")
    except Exception as e:
        print(f"{grid[0]}x{grid[1]} d={d} ell={ell}: ERROR {type(e).__name__}: {e}")

print("\n[Path B at d=2 vs Path A claim 12 terms]")
r = run_schuster_pauli_path_attack((3, 4), 2, 3, 4, 12, seed=42)
print(f"  Path B 12q d=2 ell=12 (no truncation): n_kept={r.n_pauli_strings_kept}  OTOC2={r.circuit_meta['otoc2_value']:+.4f}  fro2={r.circuit_meta['frobenius_norm_sq']:.4f}")
print(f"  Note: gate sets differ (claude8 iSWAP+sqrt(W) vs claude4 CZ+random-SU(2)) so n_kept comparison is method-class-orthogonal not numerical-exact.")
