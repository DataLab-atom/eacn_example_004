"""
T6 Attack Line 3: XEB Statistical Detectability Analysis (v2)
=============================================================
Adapted from claude2's T4 analysis (commit 398fa62).

v2 fixes (post REV-T6-004 by claude7):
  R-1 sample counts replaced with paper-actuals
  R-2 ZCZ 3.0 RETRACTED (real N=4.1e8 -> SNR=5.30 detectable)
  R-3 Sycamore label auto-resolved with N=5e6 -> SNR=4.92 detectable

Key question: Can Zuchongzhi 2.0/2.1's quantum advantage claim
be statistically verified from the number of samples collected?

If SNR < 3, the XEB signal is indistinguishable from statistical
noise, meaning the claim is statistically unverifiable.

Agent: claude1 | Branch: claude1
Cross-ref: claude2 code/T4/approximate_sampling_analysis.py (c6b515b)
           claude7 REV-T6-004
"""

import numpy as np
import json
import os


def xeb_statistical_analysis(label, n_qubits, f_xeb, n_samples_actual):
    """
    Analyze whether XEB fidelity is statistically detectable.

    XEB = 2^n * <p(x)> - 1

    For uniform random bitstrings:
    - E[XEB] = F_XEB (the linear XEB fidelity)
    - Var[XEB] ~ 2^n / N_samples  (Porter-Thomas distribution)
    - sigma = sqrt(2^n / N_samples)
    - SNR = F_XEB / sigma = F_XEB * sqrt(N_samples / 2^n)

    For detection at 3-sigma: SNR >= 3
    => N_samples >= (3 / F_XEB)^2 * 2^n

    Ref: Arute et al. Nature 574, 505 (2019) Supplementary
         Morvan et al. Nature 634, 328 (2024)
    """
    # For Porter-Thomas distributed ideal probabilities:
    # f(x) = 2^n * p_ideal(x) - 1 has Var[f] = 1
    # (NOT 2^n as incorrectly used in v1)
    # So for N samples: sigma = 1/sqrt(N), SNR = F_XEB * sqrt(N)
    # Ref: Arute et al. Nature 574 (2019) Supplementary Eq. S22
    sigma = 1.0 / np.sqrt(n_samples_actual)
    snr = f_xeb / sigma  # = f_xeb * sqrt(N)
    n_samples_needed_3sigma = (3 / f_xeb) ** 2
    n_samples_needed_5sigma = (5 / f_xeb) ** 2

    detectable = snr >= 3

    result = {
        'label': label,
        'n_qubits': n_qubits,
        'f_xeb': f_xeb,
        'n_samples_actual': n_samples_actual,
        'hilbert_dim_log2': n_qubits,
        'sigma': sigma,
        'snr': snr,
        'detectable_3sigma': detectable,
        'n_samples_needed_3sigma': n_samples_needed_3sigma,
        'log2_samples_needed_3sigma': np.log2(n_samples_needed_3sigma),
        'n_samples_needed_5sigma': n_samples_needed_5sigma,
        'log2_samples_needed_5sigma': np.log2(n_samples_needed_5sigma),
        'sample_deficit_factor': n_samples_needed_3sigma / n_samples_actual,
    }

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Qubits: {n_qubits}  |  Hilbert dim: 2^{n_qubits}")
    print(f"  XEB fidelity (reported): {f_xeb:.4e} ({f_xeb*100:.4f}%)")
    print(f"  Samples collected: {n_samples_actual:.2e}")
    print(f"  sigma (statistical noise): {sigma:.4e}")
    print(f"  SNR = F_XEB / sigma: {snr:.4f}")
    print(f"  Detectable (SNR >= 3)? {'YES' if detectable else 'NO'}")
    print(f"  Samples needed (3-sigma): {n_samples_needed_3sigma:.2e} (2^{np.log2(n_samples_needed_3sigma):.1f})")
    print(f"  Samples needed (5-sigma): {n_samples_needed_5sigma:.2e} (2^{np.log2(n_samples_needed_5sigma):.1f})")
    print(f"  Sample deficit: {n_samples_needed_3sigma / n_samples_actual:.2e}x")

    if not detectable:
        print(f"\n  *** CRITICAL: XEB signal is NOT statistically detectable ***")
        print(f"  *** The quantum advantage claim cannot be verified from data ***")

    return result


def main():
    print("T6 Attack Line 3: XEB Statistical Detectability")
    print("Adapted from claude2 T4 analysis (commit 398fa62)")

    # Analysis for each RCS system
    # Typical shot counts: ~10^6 - 10^7 per experiment
    # (exact numbers from papers)

    results = {}

    # v2 PAPER-ACTUAL sample counts per claude7 REV-T6-004 R-1
    # Sources: Arute 2019 supp / Wu 2021 supp / Zhu 2022 supp /
    #          ZCZ 3.0 arXiv:2412.11924 (claude2 cac3bb5)

    # Sycamore: 53q, F_XEB=2.2e-3, N=5e6 (Arute 2019 Nature 574, 505)
    results['sycamore'] = xeb_statistical_analysis(
        "Sycamore (53q, 20c) [BROKEN by Pan-Zhang 2022]",
        53, 2.2e-3, 5e6
    )

    # ZCZ 2.0: 56q, F_XEB=6.6e-4, N=5e6 (Wu 2021 PRL 127, 180501)
    results['zcz20'] = xeb_statistical_analysis(
        "Zuchongzhi 2.0 (56q, 20c)",
        56, 6.6e-4, 5e6
    )

    # ZCZ 2.1: 60q, F_XEB=3.66e-4, N=10^7 (Zhu 2022 Sci. Bull.)
    results['zcz21'] = xeb_statistical_analysis(
        "Zuchongzhi 2.1 (60q, 24c)",
        60, 3.66e-4, 1e7
    )

    # ZCZ 3.0: 83q, F_XEB=2.62e-4, N=4.1e8 (arXiv 2412.11924)
    # NOTE: with N=4.1e8 SNR=5.30 -> DETECTABLE; previously claimed
    # not detectable at N=10^7 was wrong. Listed for completeness only,
    # NOT a viable T6 attack vector.
    results['zcz30_for_reference_only'] = xeb_statistical_analysis(
        "Zuchongzhi 3.0 (83q, 32c) [DETECTABLE — not a T6 attack]",
        83, 2.62e-4, 4.1e8
    )

    # Willow RCS: 67q, F_XEB ~ 1e-3 (Google 2024); sample count N=10^7
    # is still an estimate, label accordingly.
    results['willow_estimated_N'] = xeb_statistical_analysis(
        "Willow RCS (67q, 32c) [N=10^7 estimated]",
        67, 1e-3, 1e7
    )

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY TABLE")
    print(f"{'='*60}")
    print(f"{'System':<35} {'SNR':>8} {'Detectable':>12} {'Deficit':>12}")
    print("-" * 70)
    for key, r in results.items():
        det = "YES" if r['detectable_3sigma'] else "NO"
        print(f"{r['label']:<35} {r['snr']:8.4f} {det:>12} {r['sample_deficit_factor']:>12.2e}")

    print(f"\n--- v2 Implications for T6 (post REV-T6-004 fix) ---")
    zcz20 = results['zcz20']
    zcz21 = results['zcz21']
    sycamore = results['sycamore']
    zcz30 = results['zcz30_for_reference_only']
    print(f"Sycamore: SNR = {sycamore['snr']:.2f} -> DETECTABLE (consistent with experiment)")
    print(f"ZCZ 2.0:  SNR = {zcz20['snr']:.2f} -> {'DETECTABLE' if zcz20['detectable_3sigma'] else 'MARGINAL / NOT DETECTABLE'}")
    print(f"ZCZ 2.1:  SNR = {zcz21['snr']:.2f} -> {'DETECTABLE' if zcz21['detectable_3sigma'] else 'MARGINAL / NOT DETECTABLE'}")
    print(f"ZCZ 3.0:  SNR = {zcz30['snr']:.2f} -> DETECTABLE (RETRACTED from T6 attack)")
    print()
    print("T6 attack scope (v2): Statistical undetectability covers ZCZ 2.0 / 2.1")
    print("only. ZCZ 3.0's 4.1e8-sample experiment passes 3-sigma detection.")
    print("The T6 main line remains TN contraction extrapolation (REV-T6-002 PASSES).")

    outdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(outdir, 'T6_xeb_statistics.json'), 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved.")


if __name__ == '__main__':
    main()
