"""
Bulmer phase-space classical attack on Gaussian Boson Sampling (T7/T8).

⚠️⚠️ DEPRECATED FOR JIUZHANG 4.0 FULL-SCALE ATTACK ⚠️⚠️

Status update 2026-04-25: Bulmer 2022 (Sci. Adv. 8, eabl9236) wall-clock
cost per sample scales as O(2^(K_c/2)) for threshold detection, where K_c
is the click count per sample. For Jiuzhang 4.0 actual parameters
(N=1024, ⟨n⟩≈9.5, η=0.51), expected K_c ≈ 1015 clicks/sample, giving
cost ~ 2^507 ≈ 10^152 seconds per sample — ~10^135× the age of the
universe. Bulmer phase-space sampler is INFEASIBLE at JZ 4.0 full scale.

Combined with Oh-MPS path being dead at η=0.51 > η_c_Oh=0.21 (claude2
commit 9cbaa9b), BOTH leading classical GBS attacks are dead on JZ 4.0
actual parameters. T7 strategy pivots to Option B (overclaim audit /
Liu-style multi-amplitude / other classical methods).

Sources for the deprecation verdict:
  - PMC PMC8791606 §III/§V Bulmer 2022 wall-clock formula:
      "(0.58 + 3.15 × 10⁻⁷ × 2^(N_c/2)) s" — Fig 5B 100-mode threshold
      "complexity reduced from O(N_c³ 2^N_c) to O(N_c³ 2^(N_c/2))"
  - claude2 commit 9cbaa9b: oh_2024_critical_eta(r=1.8, N=1024) = 0.210
  - claude5 jz40 v0.3 (and forthcoming v0.4): JZ 4.0 reported η = 0.51
  - This file's audit trail: see PLAN.md (claude8 branch) when F3 entry is added.

This file's REMAINING UTILITY:
  1. As a TOY/DEBUG sampler for small (N<=20) cross-validation against
     Oh-MPS path during Phase 0a/0b. The smoke test still passes and the
     skeleton APIs are correct — just don't expect the full implementation
     to ever be filled in for JZ 4.0 full-scale benchmarking.
  2. As a BaselineResult schema reference for any future GBS attack
     scripts. The dataclass mirrors infra/gbs/baseline_result.py from
     claude5 commit 9950ebd verbatim.

Original docstring continues below (still accurate for design intent;
just no longer feasible to deploy at JZ 4.0 scale).

---

Path B of the T7 (Jiuzhang 4.0, 🟢) two-method §D5 cross-validation:
  - Path A (claude5): Oh et al. Nature Physics 20, 1647 (2024) — lossy MPS sampler
  - Path B (claude8, this file): Bulmer et al. Sci. Adv. 8, eabl9236 (2022) — phase-space sampler

Strategy: re-implement Bulmer 2022 §III algorithm independently of Path A's MPS
codepath. We share only the upstream physical setup (`infra.gbs.gbs_circuit.build_circuit`,
authored by claude5 on origin/claude5 commit 4f41f97) which provides covariance / Haar
unitary / per-mode squeezing / loss model. All algorithmic decisions below — Williamson
normal form, bipartite decomposition, phase-space sampler — are written here with
direct reference to the Bulmer 2022 paper, NOT by porting Path A's code.

Numerical primitives (hafnian, threshold-detection probabilities) come from `thewalrus`
to avoid re-implementing already-optimised mathematics. The end-to-end algorithmic
pipeline is independent.

Status: SKELETON. All 5 algorithmic stubs raise NotImplementedError. The class signature,
result dataclass and parameter loader compile and pass a smoke test.

Schema mirrors OhMPSResult from `oh_mps_sampler.py` on origin/claude5 commit db01622:
field names match 1:1 so a single metric-comparison module can ingest both paths'
outputs polymorphically.

Dependencies (must be on `sys.path` before this module can run end-to-end):
  - infra/gbs/gbs_circuit.py            (claude5 branch, commit 4f41f97 — pending §5.2 merge to main)
  - thewalrus                           (PyPI; install separately, NOT yet in conda env)
  - numpy, scipy                        (base env confirmed)

References (full bibliography in work/claude8/arxiv_refs.md):
  [Bulmer2022]  Bulmer, Bell, Chadwick et al. Sci. Adv. 8, eabl9236 (2022)
                DOI 10.1126/sciadv.abl9236
  [Oh2024]      Oh, Lim, Fefferman, Jiang. Nat. Phys. 20, 1647 (2024)
                DOI 10.1038/s41567-024-02535-8 — for the Path A baseline we cross-check
  [Adesso2007]  Adesso, Illuminati. J. Phys. A 40, 7821 (2007) — Williamson normal form

Author: claude8 (branch `claude8`)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

import numpy as np


# ---------------------------------------------------------------------------
# Result schema — mirrors OhMPSResult (claude5 db01622) so a single metric
# comparison module can polymorphically consume both paths.
# ---------------------------------------------------------------------------

try:
    # Preferred path: shared dataclass authored by claude5 at commit 9950ebd on
    # origin/claude5, lives at `infra/gbs/baseline_result.py`. Becomes available
    # to all branches once the GBS shared infrastructure clears §5.2 review and
    # is merged to `main`.
    from infra.gbs.baseline_result import BaselineResult  # type: ignore[import-not-found]
except ImportError:
    # Fallback definition while `infra/gbs/` is not yet on `main` / not on
    # `sys.path`. Mirrors claude5 commit 9950ebd schema verbatim so the same
    # field names remain valid once the shared module is imported. Drop this
    # block once §5.2 merge lands.
    @dataclass
    class BaselineResult:
        # ---- shared fields (sampler-agnostic) ----
        click_marginal: np.ndarray                                  # (M,)
        total_click_distribution: np.ndarray                        # (M+1,)
        tvd: float
        cross_entropy: float
        g2: np.ndarray                                              # (M, M)
        wall_clock_s: float
        peak_vram_mb: float
        n_samples: int
        sample_seed: int
        truncation_error: float                                     # sampler-specific semantics, see docstring
        sampler_method: Literal["oh_mps", "bulmer_phasespace", "thewalrus_check"] = "bulmer_phasespace"

        # ---- Path A (Oh-MPS) optional ----
        bond_dim: Optional[int] = None

        # ---- Path B (Bulmer phase-space) optional ----
        williamson_rank: Optional[int] = None
        bipartite_schmidt_rank: Optional[int] = None
        hafnian_calls: Optional[int] = None

        # ---- shared metadata ----
        circuit_meta: dict = field(default_factory=dict)


# In-module alias kept for the (1) original BulmerResult symbol and (2)
# documentation continuity. Prefer BaselineResult in new code.
BulmerResult = BaselineResult


# ---------------------------------------------------------------------------
# Algorithmic stubs — all 5 raise NotImplementedError until Phase 0b coding.
# Order of implementation: 1 → 2 → 3 → 4 → 5.
# ---------------------------------------------------------------------------

def williamson_normal_form(cov: np.ndarray, hbar: float = 2.0):
    """
    Step 1. Williamson normal form of a 2M×2M covariance matrix.

    Returns
    -------
    S : (2M, 2M) symplectic matrix
    D : (2M, 2M) diagonal matrix of symplectic eigenvalues, structure diag(d_1, ..., d_M, d_1, ..., d_M)
    such that  cov = S @ D @ S.T  with S symplectic w.r.t. Omega.

    Reference: Adesso & Illuminati 2007 §3; the construction is computed via the
    matrix square-root of (Omega @ cov)^2 followed by diagonalisation.
    """
    raise NotImplementedError("Step 1: williamson_normal_form pending Phase 0b implementation")


def bipartite_decomposition(S: np.ndarray, D: np.ndarray):
    """
    Step 2. Decompose the post-Williamson Gaussian state into a tensor of bipartite
    two-mode squeezed components per Bulmer 2022 §III.B.

    Returns
    -------
    blocks : list of length k of (2, 2) covariance blocks for each bipartite pair
    schmidt_ranks : array of shape (k,) — local Schmidt rank per pair under the
                    target truncation tolerance
    """
    raise NotImplementedError("Step 2: bipartite_decomposition pending after Step 1")


def phasespace_sample(blocks, schmidt_ranks, n_samples: int, rng: np.random.Generator):
    """
    Step 3. Phase-space sampling per Bulmer 2022 §III.C.

    For each sample: draw quadrature point in each bipartite block, propagate through
    the global symplectic transform, project onto threshold detection events.
    """
    raise NotImplementedError("Step 3: phasespace_sample pending after Step 2")


def threshold_clicks(quadrature_samples: np.ndarray, eta: float):
    """
    Step 4. Apply threshold detection (click vs no-click per mode) to phase-space
    samples drawn in Step 3. With uniform per-mode loss eta, a mode registers a click
    iff its post-loss photon-number probability exceeds the dark-count-corrected
    threshold derived from the SMSV statistics.
    """
    raise NotImplementedError("Step 4: threshold_clicks pending after Step 3")


def compute_metrics(click_samples: np.ndarray, ground_truth_p: Optional[np.ndarray] = None):
    """
    Step 5. Compute all OhMPSResult-shaped metrics from a sample array.

    Returns
    -------
    dict with keys: click_marginal, total_click_distribution, tvd, cross_entropy, g2.
    `ground_truth_p` is required for tvd / cross_entropy; None means we only fill
    self-consistent fields (marginal, total_click_distribution, g2).
    """
    raise NotImplementedError("Step 5: compute_metrics pending after Step 4")


# ---------------------------------------------------------------------------
# Top-level driver — equivalent in signature to claude5's `run_oh_mps_attack`.
# ---------------------------------------------------------------------------

def run_bulmer_attack(
    circuit,                      # GBSCircuit from infra.gbs.gbs_circuit
    n_samples: int,
    sample_seed: int,
    truncation_tol: float = 1e-6,
) -> BulmerResult:
    """
    End-to-end Bulmer phase-space attack on a GBSCircuit.

    Parameter parity with `run_oh_mps_attack(circuit, chi, n_samples, sample_seed)`:
    `chi` (Oh-side bond dimension) has no Bulmer-side analogue — Bulmer expressivity
    is governed by `truncation_tol` for the bipartite Schmidt decomposition instead.

    The function is a SKELETON: it currently raises NotImplementedError as soon as
    Step 1 is reached. Smoke test only exercises argument validation.
    """
    if n_samples <= 0:
        raise ValueError("n_samples must be positive")
    if not (0 < truncation_tol < 1):
        raise ValueError("truncation_tol must lie in (0, 1)")

    # rng = np.random.default_rng(sample_seed)
    # cov = circuit.cov
    # S, D = williamson_normal_form(cov)
    # blocks, schmidt_ranks = bipartite_decomposition(S, D)
    # quadrature_samples = phasespace_sample(blocks, schmidt_ranks, n_samples, rng)
    # click_samples = threshold_clicks(quadrature_samples, circuit.eta)
    # metrics = compute_metrics(click_samples)
    # return BulmerResult(**metrics, ...)

    raise NotImplementedError("run_bulmer_attack: pipeline not yet wired (Phase 0b TODO)")


# ---------------------------------------------------------------------------
# Smoke test — runs without `infra.gbs.gbs_circuit` available.
# Exercises BulmerResult dataclass + driver argument validation only.
# ---------------------------------------------------------------------------

def _smoke():
    M = 4
    fake = BaselineResult(
        click_marginal=np.zeros(M),
        total_click_distribution=np.zeros(M + 1),
        tvd=0.0,
        cross_entropy=0.0,
        g2=np.zeros((M, M)),
        wall_clock_s=0.0,
        peak_vram_mb=0.0,
        n_samples=0,
        sample_seed=42,
        truncation_error=0.0,
    )
    assert fake.bond_dim is None
    assert fake.sampler_method == "bulmer_phasespace"
    # Aliasing check: BulmerResult must remain a synonym for BaselineResult.
    assert BulmerResult is BaselineResult

    try:
        run_bulmer_attack(circuit=None, n_samples=-1, sample_seed=0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError on n_samples=-1")

    try:
        run_bulmer_attack(circuit=None, n_samples=10, sample_seed=0)
    except NotImplementedError:
        pass
    else:
        raise AssertionError("expected NotImplementedError once validation passes")

    print("bulmer_baseline.py smoke test OK — schema + driver validation pass")


if __name__ == "__main__":
    _smoke()
