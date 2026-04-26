"""Path B d=5 ell=11 multi-seed conjecture verification.

claude8 4d942aa: d=5 ell=11 takes 8.9s/seed — feasible for multi-seed.
ell=12 hangs (>15min). ell=10 captures fro2=0.25 only; ell=11 captures fro2=0.75
in 8.9s; ell=12 would be full retain but too slow.

This test: 8 seeds at d=5 ell=11 to verify conjecture 2^(d-2)+1 = 9 values
({k/4 : k in [-4, +4]} = {-1, -0.75, -0.5, -0.25, 0, +0.25, +0.5, +0.75, +1}).

NOTE: ell=11 not full-retain (fro2=0.75) so OTOC2 may not represent ell=full
quantization. Still informative as PARTIAL conjecture verification at d=5.
"""
import sys, os
sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, r'E:\qut\7\eacn_example_004\work\claude8\T1')
from pauli_path_baseline import run_schuster_pauli_path_attack
import time

print("=" * 88)
print("PATH B d=5 ell=11 12q 3x4 LC-edge -- multi-seed conjecture partial test")
print("=" * 88)
print(f"Predicted (REV-T1-019/020): OTOC2 in {{k/4 : k in [-4,+4]}} = 9 values at d=5 ell=full")
print(f"NOTE: ell=11 captures fro2~0.75 only (not full), so OTOC2 may show subset")
print()
print(f"{'seed':>5s} | {'n_kept':>6s} | {'OTOC2_re':>10s} | {'fro2':>7s} | {'max_w':>5s} | {'mean_w':>7s} | {'time(s)':>7s}")
print("-" * 80)

seeds = [0, 1, 7, 42, 100, 1000, 12345, 99999]
otoc2_vals = []
n_kept_vals = []
times = []
for seed in seeds:
    t0 = time.time()
    try:
        r = run_schuster_pauli_path_attack((3, 4), 5, 3, 4, 11, seed=seed)
        elapsed = time.time() - t0
        cm = r.circuit_meta
        o = cm['otoc2_value']
        otoc2_vals.append(o.real)
        n_kept_vals.append(r.n_pauli_strings_kept)
        times.append(elapsed)
        print(f"{seed:5d} | {r.n_pauli_strings_kept:6d} | {o.real:+.4f}    | {cm['frobenius_norm_sq']:.4f}  | {cm['max_weight_observed']:5d} | {cm['mean_weight_observed']:.3f}    | {elapsed:.1f}")
    except Exception as e:
        print(f"{seed:5d} | ERROR {type(e).__name__}: {e}")

print(f"\n[Summary]")
distinct_vals = sorted(set(round(v, 6) for v in otoc2_vals))
print(f"  distinct OTOC2 observed: {distinct_vals} ({len(distinct_vals)} values)")
print(f"  predicted at ell=full d=5: {{k/4 : k in [-4,+4]}} = 9 values")
print(f"  observed values fit predicted set: {all(any(abs(v - k/4.0) < 1e-6 for k in range(-4,5)) for v in otoc2_vals)}")
print(f"  n_kept range: [{min(n_kept_vals)}, {max(n_kept_vals)}]")
print(f"  time range: [{min(times):.1f}s, {max(times):.1f}s]")
