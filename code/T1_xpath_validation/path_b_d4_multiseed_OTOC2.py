"""Path B d=4 ell=12 multi-seed OTOC2=0 structural test.

claude8 c037ff8 finding: d=4 ell=12 12q LC-edge OTOC2=0.0 fro2=1.0
(destructive Pauli interference seed=42).

This sweep: 10 seeds at d=4 ell=12 to test whether OTOC2=0 is
- STRUCTURAL (always 0 across seeds for this M=Z@q3 B=X@q4 12q config)
- SEED-SPECIFIC (depends on random circuit instance)

Pairs with claude8's parallel multiseed run (DM cycle 301).
"""
import sys, os
sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, r'E:\qut\7\eacn_example_004\work\claude8\T1')
from pauli_path_baseline import run_schuster_pauli_path_attack

print("=" * 88)
print("PATH B d=4 ell=12 12q 3x4 LC-edge M=Z@q3 B=X@q4 — multi-seed OTOC2=0 structural test")
print("=" * 88)
print(f"{'seed':>5s} | {'n_kept':>6s} | {'OTOC2_re':>10s} | {'OTOC2_im':>10s} | {'fro2':>7s} | {'max_w':>5s} | {'mean_w':>7s} | {'id_frac':>7s}")
print("-" * 90)

seeds = [0, 1, 7, 42, 100, 1000, 2025, 31415, 65535, 1024]
otoc2_values = []
n_kept_values = []
for seed in seeds:
    r = run_schuster_pauli_path_attack((3, 4), 4, 3, 4, 12, seed=seed)
    cm = r.circuit_meta
    o = cm['otoc2_value']
    otoc2_values.append(o.real)
    n_kept_values.append(r.n_pauli_strings_kept)
    print(f"{seed:5d} | {r.n_pauli_strings_kept:6d} | {o.real:+.4f}    | {o.imag:+.4f}    | {cm['frobenius_norm_sq']:.4f}  | {cm['max_weight_observed']:5d} | {cm['mean_weight_observed']:.3f}    | {cm['identity_fraction']:.4f}")

print(f"\n[Summary]")
print(f"  OTOC2(real) range:  [{min(otoc2_values):+.4f}, {max(otoc2_values):+.4f}]  mean={sum(otoc2_values)/len(otoc2_values):+.4f}")
print(f"  n_kept range:       [{min(n_kept_values):d}, {max(n_kept_values):d}]  mean={sum(n_kept_values)/len(n_kept_values):.0f}")
otoc2_zero_count = sum(1 for o in otoc2_values if abs(o) < 1e-10)
print(f"  OTOC2=0 (|.|<1e-10): {otoc2_zero_count}/{len(seeds)} seeds")
print(f"  -> if 10/10: OTOC2=0 is STRUCTURAL; otherwise SEED-SPECIFIC")
