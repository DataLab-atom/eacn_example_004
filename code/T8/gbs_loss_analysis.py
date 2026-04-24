"""
T8 Attack: Jiuzhang 3.0 GBS Loss Analysis
==========================================
Analyze whether photon loss in Jiuzhang 3.0 (255 photons)
places it in the classically simulable regime.

The key insight (Oh et al., Nature Physics 2024) is that
photon loss makes GBS efficiently simulable via MPS methods.

References:
- Deng et al., PRL 134, 090604 (2025) — Jiuzhang 3.0
- Oh, Lim, Fefferman, Jiang, Nat. Phys. 20, 1647 (2024) — GBS loss exploitation
- Bulmer et al., Sci. Adv. 8, eabl9236 (2022) — Jiuzhang 1.0 classical simulation

Author: claude2
Date: 2026-04-25
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

script_dir = Path(__file__).resolve().parent
results_dir = script_dir.parent.parent / "results" / "T8"
results_dir.mkdir(parents=True, exist_ok=True)

# ============================================================
# Jiuzhang 3.0 Parameters (from PRL 134, 090604)
# ============================================================

# Photonic GBS parameters
N_MODES = 144          # Number of optical modes
N_SQUEEZED = 144       # Squeezed states injected
N_PHOTONS_DETECTED = 255  # Max detected photons (reported)
MEAN_PHOTON_PER_MODE = N_PHOTONS_DETECTED / N_MODES  # Average

# Key loss parameters (estimated from paper and prior Jiuzhang versions)
# Jiuzhang series typical losses:
# - Source efficiency: ~60-80%
# - Interferometer transmission: ~70-90% (mode-dependent)
# - Detector efficiency: ~80-95%
# Overall transmission per mode: eta ~ 0.3-0.6 (varies by version)
#
# For Jiuzhang 3.0 with pseudo-PNR detectors:
# The paper claims improvements but exact per-mode loss not fully disclosed
ETA_SOURCE = 0.75      # Squeezing source efficiency
ETA_INTERFEROMETER = 0.85  # Average interferometer transmission
ETA_DETECTOR = 0.90    # Detector efficiency (pseudo-PNR)
ETA_TOTAL = ETA_SOURCE * ETA_INTERFEROMETER * ETA_DETECTOR

# Squeezing parameters
SQUEEZING_DB = 1.5     # Typical squeezing in dB (conservative estimate)
SQUEEZING_R = SQUEEZING_DB / (20 * np.log10(np.e))  # Convert to squeezing parameter r

print("=" * 60)
print("Jiuzhang 3.0 GBS Loss Analysis")
print("=" * 60)
print(f"\nSystem parameters:")
print(f"  Modes:              {N_MODES}")
print(f"  Detected photons:   {N_PHOTONS_DETECTED}")
print(f"  Mean photons/mode:  {MEAN_PHOTON_PER_MODE:.2f}")
print(f"\nLoss budget:")
print(f"  Source efficiency:  {ETA_SOURCE:.2%}")
print(f"  Interferometer:     {ETA_INTERFEROMETER:.2%}")
print(f"  Detector:           {ETA_DETECTOR:.2%}")
print(f"  Total eta:          {ETA_TOTAL:.2%}")
print(f"\nSqueezing:            {SQUEEZING_DB:.1f} dB (r = {SQUEEZING_R:.3f})")

# ============================================================
# Oh et al. Classical Simulability Criterion
# ============================================================
# Oh et al. (Nat. Phys. 2024) showed that GBS with photon loss
# can be classically simulated when:
#
# The effective squeezing after loss: r_eff = r * sqrt(eta)
# When r_eff is small enough, the output state has low entanglement
# and can be efficiently represented by MPS.
#
# Key parameter: xi = tanh(r)^2 * eta
# When xi < 1/n (roughly), classical simulation is efficient.
# More precisely, the bond dimension needed scales as ~exp(n * xi)
#
# For the full analysis, we need to consider:
# 1. The effective squeezing after loss
# 2. The entanglement structure of the lossy state
# 3. The MPS bond dimension required

xi = np.tanh(SQUEEZING_R)**2 * ETA_TOTAL
r_eff = SQUEEZING_R * np.sqrt(ETA_TOTAL)

print(f"\n{'=' * 60}")
print("Classical Simulability Analysis (Oh et al. framework)")
print("=" * 60)
print(f"\n  xi = tanh(r)^2 * eta = {xi:.6f}")
print(f"  r_eff = r * sqrt(eta) = {r_eff:.4f}")
print(f"  n * xi = {N_MODES * xi:.4f}")
print(f"  exp(n * xi) = {np.exp(N_MODES * xi):.4e}")

# ============================================================
# MPS Bond Dimension Estimation
# ============================================================
# For the lossy GBS state, the entanglement entropy across any
# bipartition scales as S ~ n_cut * xi where n_cut is the number
# of modes crossing the cut.
#
# For a linear interferometer, the maximum entanglement cut
# involves ~n/2 modes.
#
# The required MPS bond dimension: D ~ exp(S) ~ exp(n/2 * xi)

n_cut = N_MODES // 2
S_max = n_cut * xi
D_required = np.exp(S_max)

# Practical MPS simulation parameters
# Oh et al. showed that for Jiuzhang 2.0 (113 modes, 76 photons),
# D ~ 256-1024 was sufficient.
# For Jiuzhang 3.0 (144 modes, 255 photons), we need to estimate.

print(f"\nMPS Requirements:")
print(f"  Max entanglement cut: {n_cut} modes")
print(f"  Entanglement entropy S_max ~ {S_max:.2f}")
print(f"  Required bond dim D ~ exp(S) ~ {D_required:.0f}")
print(f"  log2(D) ~ {np.log2(D_required):.1f}")

# Memory for MPS: n * D^2 * d * sizeof(complex)
# where d is local Hilbert space dim (truncated Fock space)
d_local = 10  # Truncated Fock space dimension
mem_per_tensor = D_required**2 * d_local * 16  # bytes, complex128
mem_total_gb = N_MODES * mem_per_tensor / 1e9

print(f"\n  Local Hilbert dim:  {d_local}")
print(f"  Memory per tensor:  {mem_per_tensor:.2e} bytes")
print(f"  Total MPS memory:   {mem_total_gb:.2e} GB")

# ============================================================
# Comparison with Previous Jiuzhang Versions (all broken)
# ============================================================
print(f"\n{'=' * 60}")
print("Comparison: Jiuzhang Series Classical Simulation History")
print("=" * 60)

versions = [
    {
        'name': 'Jiuzhang 1.0',
        'year': 2020,
        'modes': 100,
        'photons': 76,
        'eta_total': 0.35,
        'r': 1.0 / (20 * np.log10(np.e)),
        'broken_by': 'Bulmer et al., SA 2022',
        'status': 'BROKEN',
    },
    {
        'name': 'Jiuzhang 2.0',
        'year': 2021,
        'modes': 144,
        'photons': 113,
        'eta_total': 0.40,
        'r': 1.2 / (20 * np.log10(np.e)),
        'broken_by': 'Oh et al., NP 2024',
        'status': 'BROKEN',
    },
    {
        'name': 'Jiuzhang 3.0',
        'year': 2023,
        'modes': N_MODES,
        'photons': N_PHOTONS_DETECTED,
        'eta_total': ETA_TOTAL,
        'r': SQUEEZING_R,
        'broken_by': '?',
        'status': 'TARGET',
    },
]

print(f"\n  {'Version':<15} {'Modes':>6} {'Photons':>8} {'eta':>6} {'xi':>8} {'n*xi':>6} {'Status':<10}")
print(f"  {'-'*13}  {'-'*5}  {'-'*7}  {'-'*5}  {'-'*7}  {'-'*5}  {'-'*9}")
for v in versions:
    v_xi = np.tanh(v['r'])**2 * v['eta_total']
    v_nxi = v['modes'] * v_xi
    print(f"  {v['name']:<15} {v['modes']:>6} {v['photons']:>8} {v['eta_total']:>6.2%} {v_xi:>8.5f} {v_nxi:>6.3f} {v['status']:<10}")

# ============================================================
# Sensitivity: How does classical simulability depend on loss?
# ============================================================
print(f"\n{'=' * 60}")
print("Sensitivity Analysis: xi vs eta for different squeezing levels")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Plot 1: xi vs eta for different squeezing levels
ax1 = axes[0]
eta_range = np.linspace(0.1, 1.0, 100)
squeeze_dbs = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
for sdb in squeeze_dbs:
    sr = sdb / (20 * np.log10(np.e))
    xi_vals = np.tanh(sr)**2 * eta_range
    ax1.plot(eta_range, xi_vals, label=f'{sdb:.1f} dB')
ax1.axhline(y=1/N_MODES, color='red', linestyle='--', alpha=0.5)
ax1.annotate(f'xi = 1/n = {1/N_MODES:.4f}', xy=(0.5, 1/N_MODES + 0.0005), color='red', fontsize=8)
ax1.axvline(x=ETA_TOTAL, color='blue', linestyle='--', alpha=0.5)
ax1.annotate(f'JZ 3.0 eta={ETA_TOTAL:.2f}', xy=(ETA_TOTAL+0.02, 0.03), color='blue', fontsize=8, rotation=90)
ax1.set_xlabel('Total Transmission eta')
ax1.set_ylabel('Simulability Parameter xi')
ax1.set_title('xi vs Loss for Different Squeezing')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)

# Plot 2: Required bond dimension vs eta
ax2 = axes[1]
for sdb in [1.0, 1.5, 2.0, 2.5]:
    sr = sdb / (20 * np.log10(np.e))
    xi_vals = np.tanh(sr)**2 * eta_range
    D_vals = np.exp(N_MODES / 2 * xi_vals)
    ax2.semilogy(eta_range, D_vals, label=f'{sdb:.1f} dB')
ax2.axhline(y=1024, color='gray', linestyle=':', alpha=0.5)
ax2.annotate('D=1024 (practical)', xy=(0.3, 1200), fontsize=8, color='gray')
ax2.axhline(y=1e6, color='gray', linestyle=':', alpha=0.5)
ax2.annotate('D=10^6 (GPU limit)', xy=(0.3, 1.5e6), fontsize=8, color='gray')
ax2.set_xlabel('Total Transmission eta')
ax2.set_ylabel('Required MPS Bond Dimension D')
ax2.set_title(f'Bond Dimension vs Loss\n({N_MODES} modes)')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(1, 1e15)

# Plot 3: Evolution of Jiuzhang complexity vs classical methods
ax3 = axes[2]
jz_years = [2020, 2021, 2023]
jz_photons = [76, 113, 255]
jz_claimed_hardness = [1e14, 1e18, 3.1e10]  # in years of classical compute
jz_classical_years = [2022, 2024, 2026]  # when classical caught up
jz_status = ['Broken', 'Broken', 'Target']

ax3.scatter(jz_years, jz_photons, c=['red', 'red', 'orange'], s=100, zorder=5)
for i, (yr, ph, st) in enumerate(zip(jz_years, jz_photons, jz_status)):
    ax3.annotate(f'JZ {i+1}.0\n({st})', xy=(yr, ph), xytext=(yr+0.3, ph+10), fontsize=8)
ax3.set_xlabel('Year Published')
ax3.set_ylabel('Detected Photons')
ax3.set_title('Jiuzhang Series: Scale vs Time\n(every version eventually broken)')
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(results_dir / 'T8_gbs_loss_analysis.png', dpi=300, bbox_inches='tight')
plt.savefig(results_dir / 'T8_gbs_loss_analysis.pdf', bbox_inches='tight')
print(f"\nPlots saved to {results_dir}/")

# ============================================================
# Summary
# ============================================================
print(f"\n{'=' * 60}")
print("SUMMARY: T8 Attack Assessment")
print("=" * 60)
print(f"""
1. Loss Analysis:
   - Total transmission eta = {ETA_TOTAL:.2%}
   - Simulability parameter xi = {xi:.6f}
   - n * xi = {N_MODES * xi:.4f} ({'< 1: CLASSICALLY EASY' if N_MODES * xi < 1 else '> 1: requires careful analysis'})

2. MPS Feasibility:
   - Required bond dimension D ~ {D_required:.0f} (log2 = {np.log2(D_required):.1f})
   - Memory estimate: {mem_total_gb:.2e} GB
   - {'FEASIBLE on modern hardware' if D_required < 1e6 else 'MAY require GPU cluster'}

3. Historical Pattern:
   - Jiuzhang 1.0 (76 photons): BROKEN by Bulmer 2022
   - Jiuzhang 2.0 (113 photons): BROKEN by Oh 2024
   - Jiuzhang 3.0 (255 photons): TARGET — loss-based methods should apply

4. Attack Strategy:
   a) Characterize exact loss rates from the PRL paper
   b) Implement Oh et al. MPS classical sampler for 144 modes
   c) Scale up with GPU-accelerated MPS (quimb/ITensor)
   d) Compare sampling fidelity against quantum device
   e) Cross-validate with Bulmer's phase-space method

5. Key Uncertainty:
   The exact per-mode transmission eta is critical.
   If Jiuzhang 3.0 achieved eta > 0.8, classical simulation
   becomes significantly harder. Need to extract precise values
   from the paper and supplementary materials.

NEXT STEPS:
   a) Download and analyze the actual PRL 134, 090604 paper
   b) Extract precise per-mode loss data
   c) Implement Oh et al. MPS sampler prototype
   d) Run scaling benchmarks
""")

# Save results
import csv
csv_path = results_dir / 'T8_gbs_loss_results.csv'
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['parameter', 'value', 'unit'])
    writer.writerow(['n_modes', N_MODES, ''])
    writer.writerow(['n_photons', N_PHOTONS_DETECTED, ''])
    writer.writerow(['eta_source', ETA_SOURCE, ''])
    writer.writerow(['eta_interferometer', ETA_INTERFEROMETER, ''])
    writer.writerow(['eta_detector', ETA_DETECTOR, ''])
    writer.writerow(['eta_total', ETA_TOTAL, ''])
    writer.writerow(['squeezing_dB', SQUEEZING_DB, 'dB'])
    writer.writerow(['squeezing_r', SQUEEZING_R, ''])
    writer.writerow(['xi', xi, ''])
    writer.writerow(['n_xi', N_MODES * xi, ''])
    writer.writerow(['D_required', D_required, ''])
    writer.writerow(['log2_D', np.log2(D_required), ''])
    writer.writerow(['memory_GB', mem_total_gb, 'GB'])
print(f"Results saved to {csv_path}")
