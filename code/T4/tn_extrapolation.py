"""
T4: Tensor Network Cost Extrapolation from Calibration Data
============================================================
Uses small-scale cotengra results to extrapolate contraction cost
for ZCZ 3.0 (83 qubits, 32 cycles).

Data from cotengra runs on calibration circuits.

Author: claude2
Date: 2026-04-25
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import json

script_dir = Path(__file__).resolve().parent
results_dir = script_dir.parent.parent / "results" / "T4"
results_dir.mkdir(parents=True, exist_ok=True)

# Calibration data from cotengra runs
data = [
    {'label': '9q/8d', 'n': 9, 'd': 8, 'log2_flops': 15.7, 'width': 9.0},
    {'label': '16q/10d', 'n': 16, 'd': 10, 'log2_flops': 24.7, 'width': 16.0},
    {'label': '20q/12d', 'n': 20, 'd': 12, 'log2_flops': 29.8, 'width': 20.0},
]

volumes = np.array([d['n'] * d['d'] for d in data])
log2_flops = np.array([d['log2_flops'] for d in data])
widths = np.array([d['width'] for d in data])

# Fit linear model: log2(FLOPS) = a * volume + b
coeffs = np.polyfit(volumes, log2_flops, 1)
a, b = coeffs

# Also fit width
w_coeffs = np.polyfit(volumes, widths, 1)

# Target: ZCZ 3.0
zcz_n = 83
zcz_d = 32
zcz_volume = zcz_n * zcz_d  # = 2656

# Extrapolate
zcz_log2_flops = a * zcz_volume + b
zcz_flops = 2 ** zcz_log2_flops
zcz_width = np.polyval(w_coeffs, zcz_volume)
zcz_mem_gb = 2**zcz_width * 16 / 1e9

# Also compare with known result:
# Pan-Zhang broke Sycamore (53q, 20c, volume=1060) in ~seconds on GPU cluster
# Estimated log2(FLOPS) for Sycamore ~ 50-60 (from literature)
syc_volume = 53 * 20  # = 1060
syc_log2_flops_extrapolated = a * syc_volume + b
# Literature value: Pan-Zhang needed ~2^43 FLOPS for Sycamore
syc_log2_flops_literature = 43  # approximate

print("=" * 60)
print("TN Contraction Cost Extrapolation")
print("=" * 60)

print(f"\nCalibration data:")
for d in data:
    print(f"  {d['label']}: volume={d['n']*d['d']}, log2(FLOPS)={d['log2_flops']:.1f}, width={d['width']:.0f}")

print(f"\nFit: log2(FLOPS) = {a:.4f} * volume + {b:.2f}")
print(f"Width fit: width = {w_coeffs[0]:.4f} * volume + {w_coeffs[1]:.2f}")

print(f"\nSycamore validation:")
print(f"  Our extrapolation: log2(FLOPS) = {syc_log2_flops_extrapolated:.1f}")
print(f"  Literature value:  log2(FLOPS) ~ {syc_log2_flops_literature}")
print(f"  {'REASONABLE' if abs(syc_log2_flops_extrapolated - syc_log2_flops_literature) < 20 else 'DIVERGES — need better model'}")

print(f"\nZCZ 3.0 extrapolation (83q x 32d, volume={zcz_volume}):")
print(f"  log2(FLOPS) = {zcz_log2_flops:.1f}")
print(f"  FLOPS       = 2^{zcz_log2_flops:.1f} = {zcz_flops:.2e}")
print(f"  Width       = {zcz_width:.1f}")
print(f"  Memory      = {zcz_mem_gb:.2e} GB")

# Wallclock estimates
gpu_rates = {
    '1x A100': 3.12e14,
    '1x H100': 9.9e14,
    '100x H100': 100 * 9.9e14,
    '1000x H100': 1000 * 9.9e14,
    '10000x H100 (Frontier-scale)': 10000 * 9.9e14,
}

print(f"\nWallclock estimates (exact single-amplitude contraction):")
for hw, rate in gpu_rates.items():
    time_s = zcz_flops / rate
    time_yr = time_s / (3600 * 24 * 365)
    print(f"  {hw:<35}: {time_s:.2e}s = {time_yr:.2e} years")

# Key context
print(f"\nOriginal claim: 6.4e9 years on Frontier")
frontier_rate = 1.7e18  # Frontier: 1.7 ExaFLOPS
time_frontier = zcz_flops / frontier_rate
print(f"Our estimate on Frontier: {time_frontier:.2e}s = {time_frontier/3600/24/365:.2e} years")

print(f"""
IMPORTANT CAVEATS:
1. This is a LINEAR extrapolation from 3 small-scale data points
   (volume 72-240) to volume 2656 — a 10x extrapolation gap.
2. The fit captures the basic scaling but likely UNDERESTIMATES
   the true cost at large scales (TN contraction has exponential
   components not fully captured by linear log2(FLOPS) vs volume).
3. However, Pan-Zhang (2022) showed that SLICED contraction can
   dramatically reduce effective cost by trading space for time.
4. The real attack is NOT brute-force contraction but:
   a) Approximate methods (low-fidelity sampling matches noisy quantum)
   b) Noise exploitation (quantum output already degraded)
   c) Sliced contraction with optimal ordering
5. The XEB fidelity analysis (noise_budget_analysis.py) is more
   informative: ZCZ 3.0's 0.026% XEB fidelity means classical
   methods only need to match this very low bar.
""")

# Generate plot
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: FLOPS scaling with extrapolation
ax1 = axes[0]
vol_fit = np.linspace(0, zcz_volume * 1.1, 200)
ax1.scatter(volumes, log2_flops, c='blue', s=80, zorder=5, label='Measured (cotengra)')
ax1.plot(vol_fit, a * vol_fit + b, 'r--', alpha=0.7, label=f'Fit: {a:.4f}V + {b:.1f}')
ax1.scatter([zcz_volume], [zcz_log2_flops], c='red', s=120, marker='*', zorder=5,
            label=f'ZCZ 3.0: 2^{zcz_log2_flops:.0f} FLOPS')
ax1.scatter([syc_volume], [syc_log2_flops_extrapolated], c='green', s=80, marker='D', zorder=5,
            label=f'Sycamore (extrap): 2^{syc_log2_flops_extrapolated:.0f}')
ax1.scatter([syc_volume], [syc_log2_flops_literature], c='darkgreen', s=80, marker='s', zorder=5,
            label=f'Sycamore (literature): 2^{syc_log2_flops_literature}')
ax1.set_xlabel('Circuit Volume (qubits x depth)')
ax1.set_ylabel('log2(FLOPS)')
ax1.set_title('TN Contraction Cost Extrapolation')
ax1.legend(fontsize=7)
ax1.grid(True, alpha=0.3)

# Plot 2: Comparison with claims
ax2 = axes[1]
targets = ['Sycamore\n(53q/20c)', 'ZCZ 2.0\n(60q/24c)', 'ZCZ 3.0\n(83q/32c)']
original_claims_yr = [1e4, 4.8e4, 6.4e9]
classical_best_yr = [2e-7, 397/365/24/3600, time_frontier/3600/24/365]
# Note: Sycamore was broken in 6 seconds
# ZCZ 2.0: claude1 estimated 397 years with greedy contraction

x_pos = np.arange(len(targets))
bars1 = ax2.bar(x_pos - 0.2, np.log10(original_claims_yr), 0.35, label='Original Claim', color='red', alpha=0.7)
bars2 = ax2.bar(x_pos + 0.2, [np.log10(max(v, 1e-10)) for v in classical_best_yr], 0.35,
                label='Classical Estimate', color='blue', alpha=0.7)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(targets, fontsize=8)
ax2.set_ylabel('log10(Years)')
ax2.set_title('Claimed vs Estimated Classical Time')
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(results_dir / 'T4_tn_extrapolation.png', dpi=300, bbox_inches='tight')
plt.savefig(results_dir / 'T4_tn_extrapolation.pdf', bbox_inches='tight')
print(f"Plots saved to {results_dir}/")

# Save JSON
output = {
    'calibration_data': data,
    'fit': {'a': float(a), 'b': float(b), 'model': 'log2(FLOPS) = a * volume + b'},
    'zcz30': {
        'volume': int(zcz_volume),
        'log2_flops': float(zcz_log2_flops),
        'width': float(zcz_width),
        'memory_gb': float(zcz_mem_gb),
        'time_frontier_years': float(time_frontier / 3600 / 24 / 365),
    },
    'sycamore_validation': {
        'extrapolated_log2_flops': float(syc_log2_flops_extrapolated),
        'literature_log2_flops': float(syc_log2_flops_literature),
    },
}
json_path = results_dir / 'T4_tn_extrapolation.json'
with open(json_path, 'w') as f:
    json.dump(output, f, indent=2)
print(f"Results saved to {json_path}")
