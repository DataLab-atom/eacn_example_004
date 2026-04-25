"""Path B d=5 multiseed conjecture test.

Tests REV-T1-019 conjecture:
  OTOC2(d, ell=full) takes discrete values in {k/2^(d-3) : k integer in [-2^(d-3), +2^(d-3)]}
  = 2^(d-2)+1 distinct values at depth d.

Verified:
  d=3: 2^0+1 = 2 values (-1, +1)         ✓ from c975ae0
  d=4: 2^1+1 = 3 values, observed 5      ✗ wider than conjecture; revised: {-1,-0.5,0,+0.5,+1}

Actually d=4 observed 5 values including {±1, ±0.5, 0} which is NOT {k/2 : k in [-2,+2]} =
  {-1,-0.5,0,+0.5,+1} = 5 values. So the SET-FORM conjecture {k/2^(d-3) : k integer in
  [-2^(d-2), +2^(d-2)]} = 2^(d-2)+1 may be wrong; revised {k/2^(d-3) : k integer in
  [-2^(d-3), +2^(d-3)]} doesn't match either.

Better empirical conjecture from observed data:
  d=3: OTOC2 ∈ {k/1 : k integer in [-1,+1]} = {-1, 0, +1} but observed only {-1, +1}
  d=4: OTOC2 ∈ {k/2 : k integer in [-2,+2]} = {-1, -0.5, 0, +0.5, +1} ✓ all 5 observed

So d=3 may be missing 0 from the empirical sample. Predicted general:
  OTOC2 ∈ {k/2^(d-3) : k integer in [-2^(d-3), +2^(d-3)]} = 2^(d-2)+1 values

For d=5: predicted OTOC2 ∈ {k/4 : k integer in [-4,+4]} = 9 values
  {-1, -0.75, -0.5, -0.25, 0, +0.25, +0.5, +0.75, +1}

Test: run d=5 ell=12 12q multiseed and check if OTOC2 hits the predicted discrete spectrum.
"""
import sys, os
sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, r'E:\qut\7\eacn_example_004\work\claude8\T1')
from pauli_path_baseline import run_schuster_pauli_path_attack
import time

print("=" * 88)
print("PATH B d=5 ell=12 12q 3x4 LC-edge -- OTOC2 discrete-spectrum conjecture test")
print("=" * 88)
print(f"Predicted (per REV-T1-019 c1b798a refined): OTOC2 in {{k/4 : k in [-4,+4]}} = 9 values")
print(f"  values: -1, -0.75, -0.5, -0.25, 0, +0.25, +0.5, +0.75, +1")
print()
print(f"{'seed':>5s} | {'n_kept':>6s} | {'OTOC2_re':>10s} | {'fro2':>7s} | {'max_w':>5s} | {'mean_w':>7s} | {'time(s)':>7s}")
print("-" * 80)

seeds = [0, 1, 7, 42, 100]
otoc2_vals = []
for seed in seeds:
    t0 = time.time()
    try:
        r = run_schuster_pauli_path_attack((3, 4), 5, 3, 4, 12, seed=seed)
        elapsed = time.time() - t0
        cm = r.circuit_meta
        o = cm['otoc2_value']
        otoc2_vals.append(o.real)
        print(f"{seed:5d} | {r.n_pauli_strings_kept:6d} | {o.real:+.4f}    | {cm['frobenius_norm_sq']:.4f}  | {cm['max_weight_observed']:5d} | {cm['mean_weight_observed']:.3f}    | {elapsed:.1f}")
    except Exception as e:
        print(f"{seed:5d} | ERROR {type(e).__name__}: {e}")

print(f"\n[Conjecture verification at d=5]")
predicted_set = {-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0}
for v in otoc2_vals:
    nearest = min(predicted_set, key=lambda p: abs(p - v))
    fits = "✓" if abs(v - nearest) < 1e-6 else "✗"
    print(f"  OTOC2={v:+.4f}  nearest predicted={nearest:+.4f}  delta={abs(v-nearest):+.6f}  {fits}")

is_quartile = all(any(abs(v - k/4.0) < 1e-6 for k in range(-4, 5)) for v in otoc2_vals)
print(f"\n  All values fit k/4 spectrum: {is_quartile}")
print(f"  Distinct values observed: {sorted(set(round(v, 6) for v in otoc2_vals))}")
