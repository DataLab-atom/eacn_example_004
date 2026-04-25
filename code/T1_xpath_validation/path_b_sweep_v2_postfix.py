"""Path B sweep v2 — post bug-fix `9d7ed9f` Heisenberg gate-order rectification.

Re-runs Path B at 12q 3x4 LC-edge across (d, ell) on the FIXED code.
Pre-fix sweep (commit 2716d71) showed all n_kept=0 at ell=4/8 d=2/4/6.
Post-fix expectation: d=2 ell>=4 should show non-zero n_kept (Heisenberg
evolution applied in CORRECT reverse time order).
"""
import sys, os
sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, r'E:\qut\7\eacn_example_004\work\claude8\T1')
from pauli_path_baseline import run_schuster_pauli_path_attack
import numpy as np

print("=" * 88)
print("PATH B SWEEP v2 (POST 9d7ed9f bug-fix) -- 12q 3x4 LC-edge M=Z@q3 B=X@q4")
print("=" * 88)
print(f"{'config':<22s} | {'n_kept':>6s} | {'OTOC2_re':>10s} | {'OTOC2_im':>10s} | {'fro2':>7s} | {'max_w':>5s} | {'mean_w':>7s} | {'id_frac':>7s}")
print("-" * 95)

# ell sweep at d=1..4 (d>=5 may be expensive at large ell)
for d in [1, 2, 3, 4]:
    for ell in [4, 6, 8, 12]:
        try:
            r = run_schuster_pauli_path_attack((3, 4), d, 3, 4, ell, seed=42)
            cm = r.circuit_meta
            o = cm['otoc2_value']
            print(f"3x4 d={d} ell={ell:<2d}            | {r.n_pauli_strings_kept:6d} | {o.real:+.4f}    | {o.imag:+.4f}    | {cm['frobenius_norm_sq']:.4f}  | {cm['max_weight_observed']:5d} | {cm['mean_weight_observed']:.3f}    | {cm['identity_fraction']:.4f}")
        except Exception as e:
            print(f"3x4 d={d} ell={ell:<2d}            | ERROR {type(e).__name__}: {e}")
    print()

print("\n[Multi-seed at d=4 ell=8 to characterize statistical behavior]")
for seed in [0, 1, 7, 42, 100, 1000]:
    r = run_schuster_pauli_path_attack((3, 4), 4, 3, 4, 8, seed=seed)
    cm = r.circuit_meta
    print(f"  seed={seed:5d}: n_kept={r.n_pauli_strings_kept:4d}  OTOC2={cm['otoc2_value']:+.4f}  fro2={cm['frobenius_norm_sq']:.4f}  max_w={cm['max_weight_observed']}  id_frac={cm['identity_fraction']:.4f}")
