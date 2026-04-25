"""Path B truncation-cliff mapping at d=3 12q 3x4 LC-edge.

Sweeps ell in {2..12} at d=3 to characterize the structural weight-floor JUMP
between d=2 (max_w=4) and d=4 (max_w=12) per cycle 298 finding F-B.

Pairs with claude8 d=4 ell∈{9..12} cliff mapping (DM 2026-04-26 cycle 301).
Joint d=3 + d=4 sweep characterizes the full d=2→d=3→d=4 structural transition.
"""
import sys, os
sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, r'E:\qut\7\eacn_example_004\work\claude8\T1')
from pauli_path_baseline import run_schuster_pauli_path_attack
import time

print("=" * 80)
print("PATH B truncation-cliff mapping at d=3 12q 3x4 LC-edge M=Z@q3 B=X@q4 seed=42")
print("=" * 80)
print(f"{'ell':>4s} | {'n_kept':>6s} | {'OTOC2_re':>10s} | {'fro2':>7s} | {'max_w':>5s} | {'mean_w':>7s} | {'time(s)':>7s}")
print("-" * 75)

for ell in [2, 4, 6, 7, 8, 9, 10, 11, 12]:
    t0 = time.time()
    r = run_schuster_pauli_path_attack((3, 4), 3, 3, 4, ell, seed=42)
    elapsed = time.time() - t0
    cm = r.circuit_meta
    o = cm['otoc2_value']
    print(f"{ell:>4d} | {r.n_pauli_strings_kept:6d} | {o.real:+.4f}    | {cm['frobenius_norm_sq']:.4f}  | {cm['max_weight_observed']:5d} | {cm['mean_weight_observed']:.3f}    | {elapsed:.3f}")

print("\n[d=2 baseline reminder]")
r = run_schuster_pauli_path_attack((3, 4), 2, 3, 4, 12, seed=42)
print(f"  d=2 ell=12: n_kept={r.n_pauli_strings_kept}, max_w={r.circuit_meta['max_weight_observed']}, OTOC2={r.circuit_meta['otoc2_value']}")

print("\n[multiseed d=3 ell=10 to confirm weight-floor not seed-specific]")
for seed in [0, 1, 7, 42, 100]:
    r = run_schuster_pauli_path_attack((3, 4), 3, 3, 4, 10, seed=seed)
    cm = r.circuit_meta
    print(f"  seed={seed:3d}: n_kept={r.n_pauli_strings_kept:4d}  max_w={cm['max_weight_observed']:2d}  mean_w={cm['mean_weight_observed']:.3f}  OTOC2={cm['otoc2_value']}  fro2={cm['frobenius_norm_sq']:.4f}")
