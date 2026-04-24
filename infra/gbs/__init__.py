"""GBS classical-attack infrastructure (T7 + T8).

Status: DRAFT v0.1 — on `claude5` branch only. Promotion to `main` requires §5.2 consensus.

Modules
-------
- ``gbs_circuit``  : circuit construction (covariance + Haar U + loss). Shared.
- ``critical_eta`` : (TBD, planned with claude2) Oh-2024 critical η_crit(r, M) judgment.
- Sampler-specific code (Oh-MPS / Bulmer phase-space) lives in caller branches
  (claude5 for T7 attack, claude2 for T8 attack, claude8 for independent baseline).
"""

from .gbs_circuit import (  # noqa: F401
    GBSCircuit,
    build_circuit,
    gen_haar_unitary,
    smsv_cov,
    vacuum_cov,
    apply_passive_unitary,
    apply_uniform_loss,
)
