"""Schmidt-decomposition singular-value spectrum analysis for JZ 3.0 covariance.

Per Oh et al. Nat. Phys. 20, 1647 (2024): MPS-based GBS sampling with bond
dimension chi works iff the entanglement spectrum decays fast enough that
top-chi Schmidt values capture sufficient mass. The critical eta for tractable
chi at fixed N is set by the Schmidt-spectrum decay rate.

This analysis: compute the symplectic-style Schmidt spectrum of the JZ 3.0
covariance at the central cut (mode 72 vs mode 72), then quantify:
  (a) singular-value decay slope (alpha in s_i ~ i^{-alpha})
  (b) cumulative mass captured at chi ∈ {10, 50, 100, 200, 400, full}
  (c) effective Schmidt rank epsilon-truncation = min chi s.t. captured >= 1-eps

Per Adesso-Illuminati J. Phys. A 40, 7821 (2007) §3, the entanglement of
a Gaussian state on partition A|B is set by the symplectic singular values
of the marginal-symmetrised cross-covariance Sigma_{AB}^sym = Sigma_AA^{-1/2}
* Sigma_AB * Sigma_BB^{-1/2}.

Honest scope (§H1):
  - Pure-state Schmidt formula assumes the state is Gaussian-pure on A∪B;
    JZ 3.0 has loss eta=0.424 → state is mixed.
  - For mixed state, we use the SVD of the cross-block as a *proxy* for
    the genuine bipartite entanglement spectrum. A rigorous treatment
    would symplectically diagonalise the marginal covariances first.
  - This proxy gives an upper bound on the chi required for MPS truncation;
    the actual chi may be smaller after marginal symplectic re-shaping.

Author: claude5
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, List

import numpy as np

import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from gaussian_baseline_sampler_t8 import (
    JZ30_PARAMS,
    construct_jz30_covariance_matrix,
)


def schmidt_spectrum_at_cut(cov: np.ndarray, n_modes: int, cut: int) -> Dict:
    """Compute the singular-value spectrum of the cross-block of cov across a cut.

    cov is in xxpp ordering: cov[i,j] for i,j ∈ [0..2N).
    Block layout for partition A=[0..cut), B=[cut..N):
      (q_A, q_B, p_A, p_B) ordering -> reorder rows/cols.
    """
    n_A = cut
    n_B = n_modes - cut

    # Re-index xxpp -> (q_A | q_B | p_A | p_B) layout
    idx_qA = list(range(0, cut))
    idx_qB = list(range(cut, n_modes))
    idx_pA = list(range(n_modes, n_modes + cut))
    idx_pB = list(range(n_modes + cut, 2 * n_modes))
    perm = idx_qA + idx_qB + idx_pA + idx_pB
    cov_perm = cov[np.ix_(perm, perm)]

    dim_A = 2 * n_A
    dim_B = 2 * n_B
    # In permuted layout, A modes occupy first dim_A rows/cols (q_A, p_A
    # interleaved across the qA/pA blocks).  Reorder again to (q_A, p_A, q_B, p_B):
    # Actually simpler: just extract A block (qA + pA) and B block (qB + pB).
    A_rows = list(range(n_A)) + list(range(n_A + n_B, n_A + n_B + n_A))
    B_rows = list(range(n_A, n_A + n_B)) + list(range(n_A + n_B + n_A, 2 * n_modes))

    cov_AA = cov_perm[np.ix_(A_rows, A_rows)]
    cov_BB = cov_perm[np.ix_(B_rows, B_rows)]
    cov_AB = cov_perm[np.ix_(A_rows, B_rows)]

    # Marginal-symmetrised cross-block per Adesso-Illuminati §3.
    # Use Cholesky-based whitening to avoid eigendecomposition instabilities.
    try:
        L_AA = np.linalg.cholesky(cov_AA + 1e-10 * np.eye(dim_A))
        L_BB = np.linalg.cholesky(cov_BB + 1e-10 * np.eye(dim_B))
        sym_block = np.linalg.solve(L_AA, cov_AB) @ np.linalg.solve(L_BB.T, np.eye(dim_B))
    except np.linalg.LinAlgError:
        # Fallback: skip whitening.
        sym_block = cov_AB

    s = np.linalg.svd(sym_block, compute_uv=False)
    s = np.sort(s)[::-1]  # descending
    return {
        "cut": cut,
        "n_A": n_A,
        "n_B": n_B,
        "dim_AB_block": list(sym_block.shape),
        "n_singular_values": int(len(s)),
        "singular_values_top_50": s[:50].tolist(),
        "total_mass_squared": float(np.sum(s ** 2)),
        "mass_squared_in_top_chi": {
            int(chi): float(np.sum(s[:chi] ** 2))
            for chi in [10, 20, 50, 100, 200, 400, len(s)]
            if chi <= len(s) or chi == len(s)
        },
    }


def power_law_fit_log(s: np.ndarray, head_skip: int = 2) -> Dict:
    """Fit log(s_i) = -alpha * log(i) + const on i >= head_skip + 1.

    head_skip removes outlier head values that often deviate from the
    asymptotic power-law tail.
    """
    s = np.asarray(s, dtype=np.float64)
    s = s[s > 1e-15]  # drop numerical zeros
    if len(s) < head_skip + 5:
        return {"alpha": None, "intercept": None, "n_points_used": len(s)}
    indices = np.arange(head_skip + 1, len(s) + 1)
    log_i = np.log(indices)
    log_s = np.log(s[head_skip:])
    A = np.vstack([log_i, np.ones_like(log_i)]).T
    slope, intercept = np.linalg.lstsq(A, log_s, rcond=None)[0]
    return {
        "alpha": float(-slope),
        "intercept": float(intercept),
        "n_points_used": int(len(log_i)),
        "head_skip": head_skip,
    }


def chi_for_target_mass(s: np.ndarray, target: float) -> int:
    """Find min chi s.t. cumulative s^2 mass >= target * total_mass."""
    sq = s ** 2
    total = sq.sum()
    cum = np.cumsum(sq)
    idx = np.searchsorted(cum, target * total)
    return int(idx + 1)


def run_spectrum_analysis(
    out_path: str = "branches/claude5/work/T8_jiuzhang3/jz30_schmidt_spectrum.json",
    cuts: List[int] = (12, 36, 72, 108, 132),
) -> Dict:
    print("=== JZ 3.0 Schmidt-decomposition spectrum analysis ===")
    print(f"params: {JZ30_PARAMS}")
    print(f"cuts (mode index): {list(cuts)}")

    t0 = time.time()
    cov, _ = construct_jz30_covariance_matrix(
        n_modes=JZ30_PARAMS["n_modes"],
        r=JZ30_PARAMS["squeezing_r"],
        eta=JZ30_PARAMS["loss_eta"],
        seed=42,
    )
    print(f"covariance built ({cov.shape}) in {time.time()-t0:.2f}s")

    n_modes = JZ30_PARAMS["n_modes"]

    spectra = []
    for cut in cuts:
        t_cut = time.time()
        spec = schmidt_spectrum_at_cut(cov, n_modes, cut)
        s = np.array(spec["singular_values_top_50"])
        # also compute power-law fit on full vector reproduced from sym block
        # (recompute since we only stored top 50; redo quickly)
        n_A = spec["n_A"]
        n_B = spec["n_B"]
        idx_qA = list(range(0, cut))
        idx_qB = list(range(cut, n_modes))
        idx_pA = list(range(n_modes, n_modes + cut))
        idx_pB = list(range(n_modes + cut, 2 * n_modes))
        perm = idx_qA + idx_qB + idx_pA + idx_pB
        cov_perm = cov[np.ix_(perm, perm)]
        A_rows = list(range(n_A)) + list(range(n_A + n_B, n_A + n_B + n_A))
        B_rows = list(range(n_A, n_A + n_B)) + list(range(n_A + n_B + n_A, 2 * n_modes))
        cov_AA = cov_perm[np.ix_(A_rows, A_rows)]
        cov_BB = cov_perm[np.ix_(B_rows, B_rows)]
        cov_AB = cov_perm[np.ix_(A_rows, B_rows)]
        L_AA = np.linalg.cholesky(cov_AA + 1e-10 * np.eye(2 * n_A))
        L_BB = np.linalg.cholesky(cov_BB + 1e-10 * np.eye(2 * n_B))
        sym_block = np.linalg.solve(L_AA, cov_AB) @ np.linalg.solve(L_BB.T, np.eye(2 * n_B))
        s_full = np.linalg.svd(sym_block, compute_uv=False)
        s_full = np.sort(s_full)[::-1]

        spec["power_law_fit"] = power_law_fit_log(s_full, head_skip=2)
        spec["chi_for_99_pct_mass"] = chi_for_target_mass(s_full, 0.99)
        spec["chi_for_999_pct_mass"] = chi_for_target_mass(s_full, 0.999)
        spec["chi_for_50_pct_mass"] = chi_for_target_mass(s_full, 0.50)
        spec["wall_clock_s"] = time.time() - t_cut

        spectra.append(spec)
        print(
            f"  cut={cut:3d}: n_singular={spec['n_singular_values']:3d}  "
            f"alpha={spec['power_law_fit']['alpha']:.3f}  "
            f"chi(50%)={spec['chi_for_50_pct_mass']:3d}  "
            f"chi(99%)={spec['chi_for_99_pct_mass']:3d}  "
            f"chi(99.9%)={spec['chi_for_999_pct_mass']:3d}  "
            f"({spec['wall_clock_s']:.1f}s)"
        )

    out = {
        "params": JZ30_PARAMS,
        "cuts": list(cuts),
        "spectra": spectra,
        "schema_version": "1.0",
        "wall_clock_total_s": time.time() - t0,
        "honest_scope": (
            "Symplectic-symmetrised cross-block SVD as proxy for entanglement "
            "spectrum (Adesso-Illuminati §3); upper bound on chi required for "
            "MPS truncation since marginal symplectic re-shaping not applied."
        ),
        "interpretation": {
            "expectation": (
                "If alpha > 1 across cuts, MPS chi truncation is asymptotically "
                "tractable (mass concentrates in head); if alpha << 1 or chi(99%) "
                "scales with system size, full Oh-MPS at JZ 3.0 N=144 is "
                "infeasible at chi <= 400."
            ),
            "what_to_compare_with": (
                "Oh et al. Nat Phys 20, 1647 (2024) Fig 3: critical eta for "
                "MPS-tractable GBS at given chi.  Their finding: eta_c ~ 0.21 "
                "for chi=200; JZ 3.0 eta=0.424 > 0.21 → marginally infeasible "
                "at fixed chi=200."
            ),
        },
    }

    out_p = Path(out_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with out_p.open("w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {out_path} ({out_p.stat().st_size} bytes)")
    print(f"wall_clock_total: {out['wall_clock_total_s']:.1f}s")
    return out


if __name__ == "__main__":
    run_spectrum_analysis()
