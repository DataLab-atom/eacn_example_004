# T8 hafnian_oracle real-run summary (Tick N+2)

> **Cascade 2/4 dual-impl §D5 contribution** — claude8 hafnian-direct exact-subset oracle.
> Per t-modywqdx allocation correction: claude5 lead Oh-MPS chi-corrected sampler (subtask 2);
> claude8 副 hafnian-direct probability oracle (subtask 1) + HOG/TVD benchmark (subtask 3, Tick N+3).

## Run parameters

| Param | Value |
|---|---|
| n_modes | 144 |
| squeezing r (single-mode) | 1.5 |
| loss eta (uniform) | 0.424 |
| Haar unitary seed | 42 |
| n_subset | 6 |
| Fock cutoff per mode | 4 |
| n_runs per strategy | 2 |
| strategies | random + lc_aligned |
| total subsets | 4 |
| wall clock | 126.97s |

## Result summary

| Strategy | Run | First 4 modes | sum_probs | Wall clock (s) |
|---|---|---|---|---|
| random | 0 | [5, 38, 44, 72] | 0.293 | 33.7 |
| random | 1 | [4, 20, 65, 71] | 0.292 | 31.2 |
| lc_aligned | 0 | [0, 1, 2, 3] | 0.293 | 31.3 |
| lc_aligned | 1 | [0, 1, 2, 3] | 0.293 | 30.7 |

## Critical finding — Fock cutoff truncation captures only ~29% of mass

**sum_probs ≈ 0.293** across all 4 subsets means that summing the truncated 4^6 = 4096
Fock-distribution entries (with cutoff=4 photons per mode) captures only ~29% of the
total probability mass.

**Why this matters at JZ 3.0**:
- mean photon per mode (vacuum-input squeezing then loss) ≈ eta · sinh²(r) ≈ 0.424 · sinh²(1.5) ≈ 1.91
- per-mode photon distribution has substantial tail above 4 photons → naive truncation cuts ~70%
- For paper-grade comparison vs claude5 Oh-MPS sampler, the **captured-mass renormalization** must be made explicit

**Implication for Tick N+3 hog_tvd_benchmark**:
- Use renormalized click-pattern probabilities `p_renormalized(c) = p_truncated(c) / sum_probs`
- Tag results as "**tail-bounded oracle**" — the hafnian-direct oracle is correct on the ~29% support
  it computes; comparing it to claude5 Oh-MPS at chi=100-400 reveals truncation systematic of EITHER side
- For decisive cross-validation, would need cutoff ≥ 8 (8^6 = 262144 entries; ~16x current cost ≈ 8min/subset)

## Implementation notes

- Used `thewalrus.symplectic.passive_transformation` for the lossy unitary application
  (the loss matrix encoded as `diag(sqrt(eta_vec))` produces the correct lossy GBS covariance)
- xxpp ordering throughout; cov.shape == (2*n_modes, 2*n_modes) == (288, 288)
- mu = 0 (vacuum-input squeezed state with passive interferometer + loss preserves zero-mean)
- Subset reduction via index slicing: x indices 0..n-1, p indices n..2n-1 in xxpp ordering
- Click pattern aggregation: for each Fock index (k_1, ..., k_6), bucket by (1 if k>0 else 0)

## Cross-cite to claude5 Oh-MPS path

For the dual-implementation §D5 cross-check (claude5 lead, claude8 副):
- claude5 Oh-MPS at chi=100-400 produces samples; bin into click patterns
- claude8 oracle gives **truth values** for the 64 click patterns within tail-bounded support
- TVD between renormalized claude5 click distribution and claude8 oracle =
  TVD-on-shared-support divergence; this is a tighter test than full-Fock TVD

If TVD-on-support is small (<0.05): both methods agree on the captured-mass region;
chi-truncation is sufficient for that region.
If large (>0.10): chi-truncation insufficient OR projection onto tail-bounded support invalid.

## Status

- ✅ Pipeline works on JZ 3.0 (144 mode, r=1.5, eta=0.424)
- ✅ JSON output `work/claude8/T8/jz30_hafnian_oracle.json` has 4 subsets × 64 click patterns each
- ⏳ Tick N+3: hog_tvd_benchmark.py will load this JSON + claude5 Oh-MPS output (commit 9c6ed40 downstream) + claude2 d6ca180 Gaussian baseline → compute final §D5 cross-validation table
- 📝 Caveat documented: cutoff=4 captures ~29% of mass → renormalization required for fair comparison

## Reproducibility

- script: `work/claude8/T8/hafnian_oracle.py`
- output JSON: `work/claude8/T8/jz30_hafnian_oracle.json`
- env: numpy + thewalrus 0.22.0
- seed: 42 (Haar U); 0 + 1 (subset selection)
- wall clock: 126.97s on CPU
- Windows note: PYTHONIOENCODING=utf-8 required for stdout
