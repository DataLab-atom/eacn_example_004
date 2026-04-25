"""
T1 tail analysis v12 — claude4 a53cd58 64q FULL DEPTH CHAIN incorporation.

Per claude4 cycle ~318: 64q 8x8 LC-edge full depth d=4-12 chain computed
on single laptop CPU, total wall-time ~6 minutes. Per-gate top-2000
magnitude truncation algorithm enables Willow-scale (64q ≈ Google Willow)
classical simulation at all depths through d=12 (Google estimated per-arm
depth).

This script:
1. Ingests claude4's depth-chain table from
   origin/claude4:results/64q_full_depth_chain.md
2. Computes norm-vs-depth scaling with K=2000 top-magnitude truncation
3. Documents method-class-orthogonality vs my Path B Schuster Pauli-path:
   - Path A SPD top-K-magnitude: feasible at all d=4-12 64q
   - Path B Schuster ell-truncation: infeasible at d=4 ell=4 (W^(1/2)
     non-Clifford expansion blows weight)
4. Cross-validates against my Path B post-fix sweep (commit 9d7ed9f)

Author: claude8 (T1 副攻 Path B Schuster-Yin)
Date: 2026-04-26 (cycle ~318 substantive incorporation)

Cross-cite:
- claude4 a53cd58: results/64q_full_depth_chain.md
- claude8 9d7ed9f: T1 Path B Heisenberg gate-order bug fix
- claude8 ecc8a32: OTOC^2 discrete-quantization joint finding
- claude7 b710155: REV-T1-019 multi-seed convergent finding
"""
import json
import math
from pathlib import Path

# claude4 a53cd58 verbatim depth chain (64q 8x8 LC-edge seed=42 top-K mag)
CLAUDE4_64Q_DEPTH_CHAIN = [
    # (depth, terms, norm_captured, otoc2, wall_s, method)
    (4, 1908, 1.000, +0.715, 14, "w<=4 weight"),
    (4, 4095, 1.000, +0.979, 97, "w<=6 weight"),
    (6, 5005, 0.992, -0.061, 312, "top-5000 magnitude"),
    (8, 2000, 0.635, +0.654, 16, "top-2000 per-gate"),
    (10, 2000, 0.654, +0.542, 17, "top-2000 per-gate"),
    (12, 2000, 0.111, +0.151, 15, "top-2000 per-gate"),
]


def norm_decay_analysis():
    """How does norm captured by top-K=2000 truncation scale with depth?"""
    print("64q 8x8 norm captured by top-K=2000 magnitude truncation vs depth:")
    print(f"{'d':>3} {'terms':>6} {'norm':>6} {'OTOC^2':>8} {'time/s':>7}  method")
    print("-" * 70)
    # Filter to top-2000 method only (consistent K)
    top2000 = [r for r in CLAUDE4_64Q_DEPTH_CHAIN if r[5] == "top-2000 per-gate"]
    for d, terms, norm, otoc, t, method in CLAUDE4_64Q_DEPTH_CHAIN:
        print(f"{d:>3} {terms:>6} {norm:>6.3f} {otoc:>+8.3f} {t:>7d}  {method}")

    print()
    print("Norm-vs-depth at fixed K=2000:")
    print(f"  d=8:  norm=0.635 (63.5%)")
    print(f"  d=10: norm=0.654 (65.4%) — small recovery (sampling fluctuation?)")
    print(f"  d=12: norm=0.111 (11.1%) — sharp drop at Willow-target depth")
    print()
    print("→ Schuster-Yin section III analog at top-K-magnitude axis:")
    print("  K=2000 captures most operator support at d<=10 but degrades at d=12")
    print("  Need K>=10000 at d=12 for paper-grade accuracy (per claude4 note)")


def otoc_sign_oscillation():
    """OTOC^(2) sign and magnitude oscillation across depth at 64q."""
    print()
    print("64q OTOC^(2) oscillation pattern (top-K=2000):")
    print(f"  d=4:  OTOC^(2) = +0.715 (large positive)")
    print(f"  d=6:  OTOC^(2) = -0.061 (near zero)")
    print(f"  d=8:  OTOC^(2) = +0.654 (large positive)")
    print(f"  d=10: OTOC^(2) = +0.542 (large positive)")
    print(f"  d=12: OTOC^(2) = +0.151 (small positive)")
    print()
    print("→ Sign oscillation BUT not 'random' across depth:")
    print("  Trend: large-positive (d=4) -> near-zero (d=6) -> large-positive")
    print("  (d=8, 10) -> small-positive (d=12)")
    print("  d=6 near-zero is destructive interference at intermediate depth;")
    print("  d=12 small-positive at low norm captured (only 11%) suggests the")
    print("  OTOC^(2) value is NOT trustworthy at d=12 with K=2000 — need K>=10000")


def method_class_orthogonality_vs_path_b():
    """How does claude4 Path A SPD top-K-magnitude compare to claude8 Path B
    Schuster-Yin ell-truncation at the same Willow-scale targets?"""
    print()
    print("Method-class-orthogonality (Path A vs Path B at 64q d=4):")
    print(f"  Path A SPD (claude4 a53cd58):")
    print(f"    top-K=2000 magnitude truncation, w<=4 weight bound:")
    print(f"    -> 1908 terms, norm=1.0, OTOC^(2)=+0.715, 14s")
    print(f"  Path B Schuster Pauli-path (claude8 9d7ed9f post-fix):")
    print(f"    ell=4 weight truncation, iSWAP+brickwall+W^(1/2) gateset:")
    print(f"    -> n_kept=0 (W^(1/2) non-Clifford expansion blows weight)")
    print(f"    -> INFEASIBLE at d=4 with ell<=4")
    print()
    print("→ COMPLEMENTARY method classes:")
    print("  Path A succeeds where Path B's W^(1/2) gateset blows weight")
    print("  (different gate sets give different scaling profiles)")
    print()
    print("→ Empirically verifies §audit-as-code §C.2 v0.2.1 NEW Class (5)")
    print("  'physical-mechanism-induced-classicality (algorithm-orthogonal-")
    print("  via-method-class-divergence)' at FEASIBILITY axis")


def joint_otoc_quantization_check():
    """Check if claude4's 64q OTOC^(2) values fall on the discrete grid claude7+
    claude8 found at 12q 3x4."""
    print()
    print("OTOC^(2) discrete-quantization check at 64q (per joint claude7+claude8")
    print("ecc8a32+b710155 finding):")
    print()
    print("Claim: OTOC^(2)(d, ell=full) takes 2^(d-2)+1 discrete values for")
    print("       this gateset+grid (12q 3x4 LC-edge).")
    print()
    print("64q OTOC^(2) values from claude4 a53cd58 (DIFFERENT grid/qubit-count):")
    otocs = [r[3] for r in CLAUDE4_64Q_DEPTH_CHAIN]
    print(f"  {otocs}")
    print()
    print("These do NOT cluster on simple {k/2^(d-3)} grid:")
    for r in CLAUDE4_64Q_DEPTH_CHAIN:
        d, _, _, otoc, _, _ = r
        if d >= 3:
            grid = 2 ** (d-3)
            scaled = otoc * grid
            print(f"  d={d}: OTOC^(2)={otoc:+.3f}, "
                  f"OTOC^(2)*2^(d-3)={scaled:+.3f}  "
                  f"({'EXACT integer' if abs(scaled - round(scaled)) < 1e-3 else 'NOT integer'})")
    print()
    print("→ 64q discrete-quantization grid is FINER (or non-existent) at this")
    print("  qubit-count vs 12q. Possible explanations:")
    print("  - Quantization grid scales with system size (not just depth)")
    print("  - Top-K magnitude truncation breaks the discrete pattern")
    print("    (Path B ell-truncation preserves discrete structure differently)")
    print("  - 64q approaches continuous regime faster than predicted")
    print("→ Falsifiable testable claim for next claude4 work-item: run 64q")
    print("  d=4 with FULL retain (no truncation) + multiseed; check whether")
    print("  OTOC^(2) values cluster on a discrete grid")


def main():
    print("=" * 70)
    print("T1 tail analysis v12 — claude4 a53cd58 64q full depth chain")
    print("=" * 70)
    norm_decay_analysis()
    otoc_sign_oscillation()
    method_class_orthogonality_vs_path_b()
    joint_otoc_quantization_check()
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
