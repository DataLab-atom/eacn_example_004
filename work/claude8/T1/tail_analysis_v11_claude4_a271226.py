"""
T1 tail analysis v11 — incorporating claude4 a271226 measurement data.

Per claude4 message (cycle ~298): 64q=1908terms/14s, 100q=239terms/2s,
LC-edge d=4 measured directly (NOT extrapolation), commit a271226.

This script:
1. Ingests claude4's measurement table from
   origin/claude4:results/large_scale_attack_results.md
2. Computes term-count-vs-system-size scaling at fixed depth=4
3. Reports hot-site fraction stability across qubit count
4. Documents what cross-validation against my Path B would require
   (M_qubit, B_qubit specs not in claude4's table — must confirm via
   eacn3 message before running Path B comparison)

Author: claude8 (T1 副攻 Path B Schuster-Yin per allocation v2)
Date: 2026-04-26 (cycle 299 substantive data incorporation)

Cross-cite:
- claude4 a271226: results/large_scale_attack_results.md
- claude8 9d7ed9f: T1 Path B Heisenberg gate-order bug fix (D5 6/6 PASS)
- claude8 b886633: T1 D5 cross-validation harness exposing the bug
"""
import json
import math
from pathlib import Path

# claude4 a271226 measurement data verbatim
CLAUDE4_DATA = [
    # (n_qubits, grid, terms, hot_sites, hot_pct, otoc2, wall_s)
    (36, (6, 6), 255, 4, 0.11, -0.354, 3.0),
    (48, (6, 8), 12792, 6, 0.12, +0.393, 165.0),
    (64, (8, 8), 1908, 6, 0.09, +0.715, 14.0),
    (80, (8, 10), 19709, 9, 0.11, +0.014, 438.0),
    (100, (10, 10), 239, 5, 0.05, +1.000, 2.0),
]


def term_count_scaling_analysis():
    """Examine term-count vs n_qubits at depth=4.

    Key claim from claude4: term count topology-dependent (non-monotonic).
    Verified here:
    - 36q (6x6, square): 255 terms
    - 48q (6x8, rectangular): 12792 terms (50x more than 36q!)
    - 64q (8x8, square): 1908 terms
    - 80q (8x10, rectangular): 19709 terms (10x more than 64q)
    - 100q (10x10, square): 239 terms (less than 36q!)

    Pattern: square grids (6x6, 8x8, 10x10) give consistently SMALL
    term counts; rectangular grids (6x8, 8x10) give LARGE term counts.

    Hypothesis: square symmetry causes coefficient cancellation in
    Pauli-string superposition; rectangular asymmetry breaks this and
    leaves more uncanceled terms.
    """
    print("Term-count scaling (LC-edge d=4, claude4 a271226):")
    print(f"{'n_q':>4} {'grid':>8} {'terms':>8} {'hot':>4} {'hot%':>5} "
          f"{'OTOC^2':>8} {'time/s':>7}  topology")
    print("-" * 70)
    for nq, grid, terms, hot, hp, otoc, t in CLAUDE4_DATA:
        topology = "square" if grid[0] == grid[1] else "rect"
        print(
            f"{nq:>4} {str(grid):>8} {terms:>8d} {hot:>4d} {hp:>5.2f} "
            f"{otoc:>+8.3f} {t:>7.1f}  {topology}"
        )

    # Square vs rectangular grouping
    sq_terms = [t for nq, g, t, _, _, _, _ in CLAUDE4_DATA if g[0] == g[1]]
    rect_terms = [t for nq, g, t, _, _, _, _ in CLAUDE4_DATA if g[0] != g[1]]
    print()
    print(f"Square-grid term counts: {sq_terms} (mean {sum(sq_terms)/len(sq_terms):.0f})")
    print(f"Rect-grid   term counts: {rect_terms} (mean {sum(rect_terms)/len(rect_terms):.0f})")
    print(
        f"Square/rect ratio: "
        f"{(sum(sq_terms)/len(sq_terms)) / (sum(rect_terms)/len(rect_terms)):.3f}"
    )


def hot_site_fraction_stability():
    """Hot-site fraction across all 5 measurements stays in 5%-12% range.

    This is a NON-trivial structural finding: even at 100q (10x10), only
    5% of qubits acquire non-trivial Pauli operators after d=4 evolution.
    The Pauli operator support remains LOCALIZED at all qubit counts —
    direct empirical falsification of "all qubits become entangled
    immediately" intuition.
    """
    fractions = [hp for _, _, _, _, hp, _, _ in CLAUDE4_DATA]
    print()
    print("Hot-site fraction stability:")
    print(f"  range: [{min(fractions):.2f}, {max(fractions):.2f}]")
    print(f"  mean:  {sum(fractions)/len(fractions):.3f}")
    print(f"  spread: {max(fractions) - min(fractions):.2f}")
    print(
        "  -> stable 5-12% bandwidth across 36q -> 100q "
        "(2.8x qubit-count range)"
    )
    print(
        "  -> Pauli operator support stays localized; SPD/Pauli-path "
        "feasibility scales benignly"
    )


def cross_validation_path_b_status():
    """What's needed to cross-validate my Path B against claude4's data.

    AGENTS.md §D5 demands multi-method cross-validation: same problem,
    2+ independent paths, deviation in combined uncertainty.

    Status:
    - claude4 reports OTOC^(2) values at depth=4, qubit-counts 36/48/64/80/100
    - My Path B run_schuster_pauli_path_attack can run these configs
      (post commit 9d7ed9f Heisenberg-gate-order fix; D5 6/6 PASS at small
      systems verified)
    - BLOCKER: claude4's M_qubit + B_qubit specifications not stated in
      large_scale_attack_results.md. Need to confirm via eacn3 message
      before Path B comparison.

    Once M_qubit, B_qubit confirmed, expected workflow:
        for n_qubits, grid, _, _, _, otoc4_otoc, _ in CLAUDE4_DATA:
            result = run_schuster_pauli_path_attack(
                grid_shape=grid, depth=4, M_qubit=..., B_qubit=...,
                weight_bound_l=4, seed=42,
            )
            path_b_otoc = result.circuit_meta["otoc2_value"]
            diff = abs(path_b_otoc - otoc4_otoc)
            # Pass if diff < combined_uncertainty (~1e-3 conservative)

    NOTE: Path B is Schuster Pauli-path with ell-truncation; claude4's
    Path A is SPD with magnitude-threshold truncation. Both should
    converge to same OTOC^(2) when truncation is loose enough; partial
    disagreement indicates ell-truncation regime.
    """
    print()
    print("Cross-validation Path B vs Path A status (post 9d7ed9f bug fix):")
    print("  - D5 cross-validation harness 6/6 PASS at 1e-10 (small 4q/6q)")
    print(
        "  - claude4 measurements at 36-100q d=4: OTOC^(2) values reported"
    )
    print(
        "  - BLOCKER: M_qubit, B_qubit specs not in claude4 a271226 markdown"
    )
    print(
        "  - ACTION: confirm via eacn3 message; then run Path B vs Path A "
        "at all 5 configs"
    )
    print(
        "  - Expected: |Path_B_OTOC - Path_A_OTOC| < combined_uncertainty"
    )


def main():
    print("=" * 70)
    print("T1 tail analysis v11 — claude4 a271226 incorporation")
    print("=" * 70)
    term_count_scaling_analysis()
    hot_site_fraction_stability()
    cross_validation_path_b_status()
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
