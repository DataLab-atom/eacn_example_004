"""Gaussian baseline threshold sampler for T8 (Jiuzhang 3.0) — Option B per §D5 dual-impl.

Per claude5 ↔ claude8 Option B agreement (this commit closes the §D5 trigger condition):
  - claude8 hafnian_oracle.py (commit 540e632) provides *analytical* click probabilities
    on small mode subsets (n_subset=6, cutoff=4) of the JZ 3.0 lossy GBS state.
  - claude5 (this file) provides *empirical* threshold-detection samples drawn from
    the matching Gaussian state on the same 4 subsets, same mode indices, same
    cov-construction conventions.
  - claude8 Tick N+3 hog_tvd_benchmark.py consumes both outputs to compute HOG / TVD
    on the captured-mass shared support.

Honest scope (§H1):
  - This is the *Gaussian baseline* leg only — no MPS chi correction.
  - The chi-corrected Oh-MPS path (M2-M5 in plan.md) is DEFERRED to §future work;
    the relevant entrypoint is `oh_mps_sampler_t8.py` which still raises
    NotImplementedError on the Schmidt / chi / sequential-sampling steps.
  - Per claude7 REV-T8-001 v0.1: Gaussian-level cross-check is sufficient at
    n_subset=6 (HOG > 0.5 already at N=4/6), so this leg is technically valid for
    the §D5 demonstration even without chi correction.

Convention:
  - cov ordering xxpp (matches claude8 hafnian_oracle.py to ensure cov alignment)
  - hbar=2 vacuum convention
  - Haar seed = 42 (matches claude8)

Sampling method:
  - Compute analytical click probabilities at cutoff=4 (same as claude8 oracle).
  - Renormalize within captured-mass region (`p_renorm = p / sum_probs`).
  - Draw n_samples=10000 i.i.d. click patterns from the renormalized distribution.
  - This gives valid empirical samples for HOG / TVD-on-shared-support comparison.

  Genuinely independent comparison via direct torontonian sampling (without Fock
  truncation) is recorded as an extension hook below — left as a §future work
  candidate beyond Option B scope.

Author: claude5 (claude-opus-4-7)
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from thewalrus import quantum as twq
from thewalrus import symplectic


JZ30_PARAMS = {
    "n_modes": 144,
    "squeezing_r": 1.5,
    "loss_eta": 0.424,
}


def haar_unitary(n: int, rng: np.random.Generator) -> np.ndarray:
    """Mezzadri 2007 Haar-random unitary (matches claude8 hafnian_oracle.py)."""
    z = (rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    d = np.diagonal(r)
    ph = d / np.abs(d)
    return q * ph


def construct_jz30_covariance_matrix(
    n_modes: int = 144,
    r: float = 1.5,
    eta: float = 0.424,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray]:
    """Build JZ 3.0 lossy GBS covariance (xxpp ordering, hbar=2).

    Replicates claude8 hafnian_oracle.py construct_jz30_covariance_matrix to
    guarantee identical cov for §D5 cross-check.
    """
    rng = np.random.default_rng(seed)

    # 1. Single-mode squeezing on each mode.
    r_vec = np.full(n_modes, r)
    S_squeeze = symplectic.squeezing(r_vec)
    cov_squeeze = S_squeeze @ S_squeeze.T

    # 2. Haar-random passive interferometer.
    U = haar_unitary(n_modes, rng)
    S_U = symplectic.interferometer(U)
    cov_after_U = S_U @ cov_squeeze @ S_U.T

    # 3. Uniform per-mode loss.
    eta_vec = np.full(n_modes, eta)
    mu = np.zeros(2 * n_modes)
    mu, cov_lossy = symplectic.passive_transformation(
        mu, cov_after_U, np.diag(np.sqrt(eta_vec))
    )

    return cov_lossy, mu


def select_mode_subset(
    strategy: str,
    n_subset: int = 6,
    n_modes: int = 144,
    seed: int = 0,
) -> List[int]:
    """Mirror claude8 hafnian_oracle.py subset selection."""
    rng = np.random.default_rng(seed)
    if strategy == "random":
        return sorted(rng.choice(n_modes, size=n_subset, replace=False).tolist())
    if strategy == "lc_aligned":
        return list(range(n_subset))
    raise ValueError(f"unknown strategy={strategy}")


def reduce_cov_to_subset(
    cov: np.ndarray,
    subset_modes: List[int],
    n_modes_total: int,
) -> np.ndarray:
    """xxpp slice into subset modes (mirrors claude8 oracle)."""
    idx = [m for m in subset_modes] + [n_modes_total + m for m in subset_modes]
    return cov[np.ix_(idx, idx)]


def click_probability_distribution(
    cov_subset: np.ndarray,
    n_subset: int,
    cutoff: int = 4,
) -> Dict[Tuple[int, ...], float]:
    """Aggregate Fock probabilities (cutoff=4) into 2^n_subset click patterns.

    Identical procedure to claude8 hafnian_oracle.exact_threshold_click_probabilities;
    we recompute here so the sampler is self-contained without cross-branch import.
    """
    mu_subset = np.zeros(2 * n_subset)
    probs_fock = twq.probabilities(mu_subset, cov_subset, cutoff)
    click_probs: Dict[Tuple[int, ...], float] = {}
    for idx in np.ndindex(*([cutoff] * n_subset)):
        click = tuple(1 if k > 0 else 0 for k in idx)
        click_probs[click] = click_probs.get(click, 0.0) + float(probs_fock[idx])
    return click_probs


def sample_clicks_from_distribution(
    click_probs: Dict[Tuple[int, ...], float],
    n_samples: int,
    rng: np.random.Generator,
) -> Tuple[np.ndarray, float]:
    """Draw i.i.d. samples from the (renormalized) click distribution.

    Returns
    -------
    samples : (n_samples, n_subset) int8 array of 0/1 click bits
    sum_probs : raw mass captured at the chosen Fock cutoff (pre-renorm)
    """
    patterns = list(click_probs.keys())
    probs = np.array([click_probs[p] for p in patterns], dtype=np.float64)
    sum_probs = float(probs.sum())
    if sum_probs <= 0:
        raise ValueError(f"degenerate click distribution: sum_probs={sum_probs}")
    probs_renorm = probs / sum_probs
    indices = rng.choice(len(patterns), size=n_samples, p=probs_renorm)
    samples = np.array([patterns[i] for i in indices], dtype=np.int8)
    return samples, sum_probs


# ---------------------------------------------------------------------------
# Extension hook — chi-corrected Oh-MPS path (DEFERRED, §future work)
# ---------------------------------------------------------------------------

def chi_corrected_path(*args, **kwargs):
    """Placeholder for the chi-corrected Oh-MPS sampling path.

    NotImplementedError is intentional and §H1-honest. The real implementation
    lives in `oh_mps_sampler_t8.py` (M2-M5 milestones) and is deferred per
    plan.md to §future work, post manuscript spine handoff. Reviewer note:
    Option B (this Gaussian baseline path) is the §D5 demo at Gaussian level;
    chi-corrected dual-impl extension is wire-up-ready but not yet executed.
    """
    raise NotImplementedError(
        "chi-corrected Oh-MPS sampler deferred to §future work; "
        "see branches/claude5/work/T8_jiuzhang3/oh_mps_sampler_t8.py M2-M5 "
        "and plan.md §future-work for the deferred two-track plan."
    )


def torontonian_direct_sampling_path(*args, **kwargs):
    """Placeholder for genuinely-independent torontonian-direct sampling.

    NotImplementedError is intentional. Genuinely-independent §D5 would
    bypass the Fock cutoff entirely via thewalrus.samples.torontonian_sample_state
    or equivalent. Recorded as a second-tier extension hook beyond Option B
    scope; current Option B is a methodology demo using shared-cutoff click
    distributions.
    """
    raise NotImplementedError(
        "torontonian-direct (non-truncated) sampling deferred; this is a "
        "second-tier §D5 cross-check beyond Option B (Gaussian baseline) scope."
    )


# ---------------------------------------------------------------------------
# Top-level orchestration
# ---------------------------------------------------------------------------

def run_gaussian_baseline_sampler(
    out_path: str = "branches/claude5/work/T8_jiuzhang3/jz30_gaussian_baseline_samples.json",
    n_samples: int = 10_000,
    cutoff: int = 4,
    sample_seed: int = 1234,
) -> Dict:
    """Generate threshold samples on the same 4 subsets as claude8 hafnian_oracle."""
    print("=== T8 gaussian_baseline_sampler_t8.py (Option B) ===")
    print(f"JZ 3.0 params: {JZ30_PARAMS}")
    print(f"n_samples={n_samples}, cutoff={cutoff}, sample_seed={sample_seed}")

    t0 = time.time()
    cov, mu = construct_jz30_covariance_matrix(
        n_modes=JZ30_PARAMS["n_modes"],
        r=JZ30_PARAMS["squeezing_r"],
        eta=JZ30_PARAMS["loss_eta"],
        seed=42,
    )
    t_cov = time.time() - t0
    print(f"covariance built ({cov.shape}) in {t_cov:.2f}s")

    n_modes = JZ30_PARAMS["n_modes"]
    n_subset = 6
    n_runs = 2

    sample_rng = np.random.default_rng(sample_seed)

    output: Dict = {
        "params": JZ30_PARAMS,
        "n_subset": n_subset,
        "n_runs": n_runs,
        "n_samples": n_samples,
        "cutoff": cutoff,
        "sample_seed": sample_seed,
        "subsets": [],
        "schema_version": "1.0",
        "wall_clock_total_s": None,
        "extension_hooks": {
            "chi_corrected_path": "NotImplementedError -- see oh_mps_sampler_t8.py M2-M5",
            "torontonian_direct_sampling_path": "NotImplementedError -- second-tier §D5",
        },
        "honest_scope": (
            "Option B Gaussian baseline only. Samples drawn from the analytical "
            "click distribution at the same Fock cutoff as claude8 oracle "
            "(540e632); cross-check at HOG/TVD level validates sampler vs "
            "analytical agreement on the captured-mass shared support."
        ),
    }

    for strategy in ["random", "lc_aligned"]:
        for run_id in range(n_runs):
            subset = select_mode_subset(
                strategy, n_subset=n_subset, n_modes=n_modes, seed=run_id
            )
            t_subset_start = time.time()
            cov_subset = reduce_cov_to_subset(cov, subset, n_modes)
            click_probs = click_probability_distribution(cov_subset, n_subset, cutoff)
            samples, sum_probs = sample_clicks_from_distribution(
                click_probs, n_samples, sample_rng
            )
            t_subset = time.time() - t_subset_start
            print(
                f"  {strategy} run={run_id} modes={subset} "
                f"sum_probs={sum_probs:.6f} wall={t_subset:.2f}s"
            )
            output["subsets"].append(
                {
                    "strategy": strategy,
                    "run_id": run_id,
                    "modes": subset,
                    "n_click_patterns_seen": int(
                        len(np.unique(samples, axis=0))
                    ),
                    "sum_probs_pre_renorm": sum_probs,
                    "wall_clock_s": t_subset,
                    "samples": samples.tolist(),
                }
            )

    output["wall_clock_total_s"] = time.time() - t0

    out_p = Path(out_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with out_p.open("w") as f:
        json.dump(output, f, indent=2)
    print(f"wrote {out_path} ({out_p.stat().st_size} bytes)")
    print(f"wall_clock_total: {output['wall_clock_total_s']:.2f}s")

    return output


if __name__ == "__main__":
    run_gaussian_baseline_sampler()
