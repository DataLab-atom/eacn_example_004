"""
T4 Attack: Zuchongzhi 3.0 Tensor Network Contraction Cost Estimation
=====================================================================
Estimate the computational cost of classically simulating ZCZ 3.0
using tensor network contraction methods (Pan-Zhang family).

Uses cotengra for contraction path optimization on a simplified
circuit model matching ZCZ 3.0 parameters.

References:
- Pan & Zhang, PRL 129, 090502 (2022) — Broke Sycamore
- Liu et al., PRL 132, 030601 (2024) — Multi-amplitude TN
- Gao et al., PRL 134, 090601 (2025) — ZCZ 3.0

Author: claude2
Date: 2026-04-25
"""

import numpy as np
import quimb.tensor as qtn
import cotengra as ctg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import time
import json

script_dir = Path(__file__).resolve().parent
results_dir = script_dir.parent.parent / "results" / "T4"
results_dir.mkdir(parents=True, exist_ok=True)

# ============================================================
# Build ZCZ 3.0-like Random Circuit Tensor Network
# ============================================================

def build_rcs_circuit(n_rows, n_cols, depth, seed=42):
    """Build a random circuit sampling tensor network on a 2D grid.

    Models the ZCZ 3.0 circuit structure:
    - 2D grid of qubits
    - Each cycle: random 1Q gates + one of 4 CZ gate patterns (ABCD)
    - Measurement at the end

    Returns a quimb tensor network.
    """
    rng = np.random.default_rng(seed)
    n_qubits = n_rows * n_cols

    circ = qtn.Circuit(n_qubits)

    # Define 2D grid edges grouped by pattern
    edges = []
    for r in range(n_rows):
        for c in range(n_cols):
            q = r * n_cols + c
            if c + 1 < n_cols:
                edges.append((q, q + 1, 'H'))  # horizontal
            if r + 1 < n_rows:
                edges.append((q, q + n_cols, 'V'))  # vertical

    # Group edges into 4 non-overlapping patterns (ABCD)
    patterns = [[], [], [], []]
    for q1, q2, direction in edges:
        r1, c1 = divmod(q1, n_cols)
        r2, c2 = divmod(q2, n_cols)
        if direction == 'H':
            pattern_idx = (r1 % 2) * 2 + (c1 % 2)
        else:
            pattern_idx = (r1 % 2) * 2 + (c1 % 2)
        patterns[pattern_idx % 4].append((q1, q2))

    # Build the circuit cycle by cycle
    single_gate_set = ['RZ', 'RX', 'RZ']  # simplified SU(2)

    for cycle in range(depth):
        # Single-qubit gates (random SU(2) rotations)
        for q in range(n_qubits):
            angles = rng.uniform(0, 2 * np.pi, 3)
            for gate, angle in zip(single_gate_set, angles):
                circ.apply_gate(gate, angle, q)

        # Two-qubit gates (CZ) from pattern for this cycle
        pattern = patterns[cycle % 4]
        for q1, q2 in pattern:
            if q1 < n_qubits and q2 < n_qubits:
                circ.apply_gate('CZ', q1, q2)

    return circ


def estimate_contraction_cost(circ, n_qubits, optimize_minutes=2):
    """Estimate the contraction cost of the circuit's output amplitude TN.

    Returns estimated FLOP count, memory, and contraction width.
    """
    # Get the tensor network for computing one output amplitude
    tn = circ.psi

    # Use cotengra to find optimal contraction path
    opt = ctg.HyperOptimizer(
        max_time=optimize_minutes * 60,
        max_repeats=128,
        progbar=True,
        minimize='flops',
    )

    # Get the contraction info
    info = tn.contract(all, optimize=opt, get='path-info')

    opt_cost = float(info.opt_cost)
    largest = float(info.largest_intermediate)
    return {
        'flops': opt_cost,
        'log2_flops': np.log2(opt_cost) if opt_cost > 0 else 0,
        'memory_bytes': largest * 16,  # complex128
        'memory_gb': largest * 16 / 1e9,
        'contraction_width': np.log2(largest) if largest > 0 else 0,
        'num_tensors': len(tn.tensors),
    }


# ============================================================
# Run estimations at multiple scales
# ============================================================
print("=" * 60)
print("ZCZ 3.0 Tensor Network Contraction Cost Estimation")
print("=" * 60)

# Start with small scales to establish scaling, then extrapolate
scales = [
    # (rows, cols, depth, label)
    (3, 3, 8, "9q/8d (calibration)"),
    (4, 4, 10, "16q/10d (calibration)"),
    (4, 5, 12, "20q/12d (calibration)"),
    (5, 5, 14, "25q/14d (calibration)"),
    (5, 6, 16, "30q/16d (calibration)"),
    (6, 6, 20, "36q/20d (intermediate)"),
]

results = []
for n_rows, n_cols, depth, label in scales:
    n_qubits = n_rows * n_cols
    print(f"\n--- {label}: {n_qubits} qubits, depth {depth} ---")

    t0 = time.time()
    circ = build_rcs_circuit(n_rows, n_cols, depth)
    build_time = time.time() - t0
    print(f"  Circuit built in {build_time:.1f}s")

    t0 = time.time()
    # Use shorter optimization for small circuits, longer for bigger
    opt_time = 0.5 if n_qubits <= 20 else 1.0 if n_qubits <= 30 else 2.0
    cost = estimate_contraction_cost(circ, n_qubits, optimize_minutes=opt_time)
    opt_elapsed = time.time() - t0

    cost['n_qubits'] = n_qubits
    cost['depth'] = depth
    cost['label'] = label
    cost['opt_time_s'] = opt_elapsed
    results.append(cost)

    print(f"  FLOPs:    2^{cost['log2_flops']:.1f} = {cost['flops']:.2e}")
    print(f"  Memory:   {cost['memory_gb']:.3f} GB (width: {cost['contraction_width']:.1f})")
    print(f"  Tensors:  {cost['num_tensors']}")
    print(f"  Opt time: {opt_elapsed:.1f}s")

# ============================================================
# Extrapolate to ZCZ 3.0 scale (83 qubits, 32 cycles)
# ============================================================
print(f"\n{'=' * 60}")
print("Extrapolation to ZCZ 3.0 (83 qubits, 32 cycles)")
print("=" * 60)

# Fit log2(FLOPS) vs n_qubits * depth (total circuit volume)
volumes = np.array([r['n_qubits'] * r['depth'] for r in results])
log2_flops = np.array([r['log2_flops'] for r in results])

# Linear fit: log2(FLOPS) = a * volume + b
valid = log2_flops > 0
if np.sum(valid) >= 2:
    coeffs = np.polyfit(volumes[valid], log2_flops[valid], 1)
    a, b = coeffs

    # Extrapolate to ZCZ 3.0
    zcz_volume = 83 * 32
    zcz_log2_flops = a * zcz_volume + b
    zcz_flops = 2 ** zcz_log2_flops

    # Convert to wallclock time
    # A100 GPU: ~312 TFLOPS FP32 = 3.12e14 FLOPS
    # H100 GPU: ~990 TFLOPS FP32 = 9.9e14 FLOPS
    # 1000 H100s: ~1e18 FLOPS
    gpu_flops_a100 = 3.12e14
    gpu_flops_h100 = 9.9e14
    cluster_1000_h100 = 1000 * gpu_flops_h100

    time_1_a100 = zcz_flops / gpu_flops_a100
    time_1_h100 = zcz_flops / gpu_flops_h100
    time_1000_h100 = zcz_flops / cluster_1000_h100

    print(f"\nScaling fit: log2(FLOPS) = {a:.4f} * volume + {b:.2f}")
    print(f"R² quality check: volumes range [{volumes[valid].min()}, {volumes[valid].max()}]")
    print(f"                  extrapolating to volume = {zcz_volume}")
    print(f"\nEstimated ZCZ 3.0 contraction cost:")
    print(f"  log2(FLOPS) = {zcz_log2_flops:.1f}")
    print(f"  FLOPS       = 2^{zcz_log2_flops:.1f} = {zcz_flops:.2e}")
    print(f"\nEstimated wallclock times:")
    print(f"  1x A100:     {time_1_a100:.2e} seconds = {time_1_a100/3600:.2e} hours = {time_1_a100/3600/24/365:.2e} years")
    print(f"  1x H100:     {time_1_h100:.2e} seconds = {time_1_h100/3600:.2e} hours = {time_1_h100/3600/24/365:.2e} years")
    print(f"  1000x H100:  {time_1000_h100:.2e} seconds = {time_1000_h100/3600:.2e} hours = {time_1000_h100/3600/24/365:.2e} years")

    # Compare with claim
    claim_years = 6.4e9
    print(f"\n  Original claim:  {claim_years:.2e} years on Frontier")
    print(f"  Our estimate:    {time_1000_h100/3600/24/365:.2e} years on 1000 H100s")

    # Important caveat
    print(f"\n  CAVEAT: This is a rough extrapolation from small-scale simulations.")
    print(f"  The actual cost depends heavily on contraction ordering optimization")
    print(f"  at the target scale. However, the scaling trend is informative.")
    print(f"\n  NOTE: This is the cost for ONE amplitude. For XEB spoofing,")
    print(f"  the key insight from Pan-Zhang (2022) is that approximate")
    print(f"  methods (sliced contraction + noisy sampling) can dramatically")
    print(f"  reduce the effective cost.")
else:
    print("  Insufficient data points for extrapolation.")
    zcz_log2_flops = 0
    a, b = 0, 0

# ============================================================
# Generate plots
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: FLOPS scaling
ax1 = axes[0]
ax1.scatter(volumes[valid], log2_flops[valid], c='blue', s=60, zorder=5)
if np.sum(valid) >= 2:
    vol_fit = np.linspace(0, zcz_volume * 1.1, 100)
    ax1.plot(vol_fit, a * vol_fit + b, 'r--', alpha=0.7, label=f'Fit: {a:.4f}V + {b:.1f}')
    ax1.scatter([zcz_volume], [zcz_log2_flops], c='red', s=100, marker='*', zorder=5,
                label=f'ZCZ 3.0 extrapolation: 2^{zcz_log2_flops:.0f}')
ax1.set_xlabel('Circuit Volume (qubits x depth)')
ax1.set_ylabel('log2(FLOPS)')
ax1.set_title('TN Contraction Cost Scaling')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Memory scaling
ax2 = axes[1]
widths = np.array([r['contraction_width'] for r in results])
ax2.scatter(volumes[valid], widths[valid], c='green', s=60, zorder=5)
if np.sum(valid) >= 2:
    w_coeffs = np.polyfit(volumes[valid], widths[valid], 1)
    zcz_width = np.polyval(w_coeffs, zcz_volume)
    zcz_mem_gb = 2**zcz_width * 16 / 1e9
    ax2.plot(vol_fit, np.polyval(w_coeffs, vol_fit), 'r--', alpha=0.7)
    ax2.scatter([zcz_volume], [zcz_width], c='red', s=100, marker='*',
                label=f'ZCZ 3.0: width={zcz_width:.0f} ({zcz_mem_gb:.0e} GB)')
ax2.set_xlabel('Circuit Volume (qubits x depth)')
ax2.set_ylabel('Contraction Width (log2)')
ax2.set_title('TN Memory Requirement Scaling')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(results_dir / 'T4_tn_scaling.png', dpi=300, bbox_inches='tight')
plt.savefig(results_dir / 'T4_tn_scaling.pdf', bbox_inches='tight')
print(f"\nScaling plots saved to {results_dir}/")

# Save results as JSON
json_path = results_dir / 'T4_tn_cost_results.json'
output = {
    'scales': results,
    'fit': {'a': a, 'b': b},
    'zcz30_extrapolation': {
        'volume': 83 * 32,
        'log2_flops': float(zcz_log2_flops) if zcz_log2_flops else None,
    }
}
with open(json_path, 'w') as f:
    json.dump(output, f, indent=2, default=str)
print(f"Results saved to {json_path}")
