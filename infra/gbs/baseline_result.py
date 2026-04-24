"""Shared result schema for all GBS classical-attack baselines.

Status: DRAFT v0.1 — on `claude5` branch only. Promotion to `main` requires §5.2 consensus.

Both Oh-MPS (claude5) and Bulmer phase-space (claude8) baselines emit a
``BaselineResult`` so the cross-validation comparator can iterate over a single
type. Path-specific fields default to ``None`` and are populated only by the
relevant sampler; the comparator skips ``None`` entries.

Designed jointly by claude5 + claude8 on 2026-04-25 to ensure §D5 multi-method
cross-validation evidence (TVD / cross-entropy / two-sample distinguishability)
is one piece of code, not two.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

import numpy as np
from numpy.typing import NDArray


SamplerMethod = Literal["oh_mps", "bulmer_phasespace", "thewalrus_check"]


@dataclass
class BaselineResult:
    """Output of one (config, sampler) run, mirroring spec §5(a)+(b).

    Notes
    -----
    - Generic statistical fields (``click_marginal``, ``total_click_distribution``,
      ``tvd``, ``cross_entropy``, ``g2``) are always populated.
    - ``bond_dim`` and ``truncation_error`` are interpreted per-sampler:
        - Oh-MPS: bond_dim = MPS bond χ; truncation_error = sum of squared
          discarded Schmidt singular values at the bipartite cut.
        - Bulmer: bond_dim is None; truncation_error is the
          ``bipartite_schmidt_truncation`` quantity (rank reduction in
          Williamson form). Set the corresponding *_rank fields below for
          richer Bulmer telemetry.
    - Path-specific fields default to ``None``.
    """

    # --- generic distribution stats (§5(a)) -----------------------------------
    click_marginal: NDArray[np.float64]            # (M,) per-mode click prob
    total_click_distribution: NDArray[np.float64]  # (M+1,) histogram
    tvd: Optional[float]                           # vs ground-truth (None if M too large)
    cross_entropy: Optional[float]
    g2: NDArray[np.float64]                        # (M, M) second-order corr

    # --- generic execution -----------------------------------------------------
    wall_clock_s: float
    peak_vram_mb: Optional[float]                  # None for CPU-only runs

    # --- generic convergence (§5(b)) ------------------------------------------
    n_samples: int
    bond_dim: Optional[int] = None                  # Oh-MPS only
    truncation_error: Optional[float] = None        # both, with sampler-specific meaning
    sampler_method: SamplerMethod = "oh_mps"

    # --- Bulmer-specific telemetry --------------------------------------------
    williamson_rank: Optional[int] = None
    bipartite_schmidt_rank: Optional[int] = None
    hafnian_calls: Optional[int] = None

    # --- provenance -----------------------------------------------------------
    circuit_meta: dict = field(default_factory=dict)
    extra: dict = field(default_factory=dict)        # free-form per-sampler


# Backwards-compatibility alias (some callers may have imported `OhMPSResult`
# from `oh_mps_sampler.py` before the refactor; do not break them.)
OhMPSResult = BaselineResult
BulmerResult = BaselineResult
