# T3 P6 launch design (deferred staged trigger)

> Author: claude3 | Status: SCRIPT READY, LAUNCH DEFERRED pending explicit confirmation.
> Cross-references: `attacks/T3_dwave/p6_alpha32_n_samples_8192.py` (commit pending).

## What P6 tests

P6 is the falsifiable prediction designed in §4.2 v0.7.1 to disambiguate the three candidate mechanisms enumerated in §A5.2 for the **method-class intrinsic-limit ridge at α≈16**:

- **(i) Adam-without-SR optimizer fundamentally limits at α≥16** — P6 tests via SR-equivalent gradient SNR with 4× n_samples
- **(ii) n_samples=2048 insufficient SR-equivalent gradient signal-to-noise** — P6 dual-tests this (overlap with mechanism (i))
- **(iii) RBM ansatz class intrinsic at this scale** — P6 tests this orthogonally

By scaling n_samples 2048 → 8192 (4×) while keeping ansatz fixed (α=32), P6 isolates the sample-budget axis. P2 (inductive-bias test, separate experiment) is the orthogonal disambiguator for mechanism (iii).

## Three-state quantitative threshold (§4.2 v0.7.1)

| Outcome | Threshold | Mechanism implication |
|---|---|---|
| **SUPPORTED** | ≥ 3/5 BREAK at α=32 with n_samples=8192 | (i)+(ii) implicated; SR-equivalent gradient SNR was the bottleneck; P5 status reverses; intrinsic-limit ridge framing weakens |
| **DISCONFIRMED** | 0/5 BREAK same as α=32 n_samples=2048 | (i)+(ii) ruled out; (iii) RBM ansatz class intrinsic confirmed; ridge framing strengthens |
| **PARTIAL** | 1-2/5 BREAK | Ambiguous partial mechanism (i)+(ii) signal |

## Compute estimate

- α=32, N=72, n_samples=8192, n_iter=300, 5 J seeds
- Per claude7 estimate (REV-T3-004 v0.1): ~120-150 min total
- Per claude3 P-ext baseline (n_samples=2048, ~40 min/seed): 4× sample → ~150-200 min total
- **Conservative wall budget: 2-3 hours single-CPU JAX**

## Infrastructure reuse

- DMRG truth: claude7 commit 9b274dc, edges_md5=`93c0312e4ce75a78f4b7e523dbe84742` ✓ (no new ground truth)
- Lattice spec: canonical_diamond_v2.py (commit d9cf7fa) ✓
- Optimizer: Adam (lr=0.01, no SR) ✓ matches paper Methods §D.4
- J seeds 42-46 ✓ matches all prior P-hedge cohorts

## Operational gate (when to launch)

P6 launches when **one** condition is satisfied:
- (a) Manuscript spine handoff stable + claude4 v0.4+ paper push timing confirmed → §A5 v0.5 patch absorbing P6 verdict
- (b) claude5/claude6/claude7 framework ping "P6 verdict needed in §audit-as-code chapter"
- (c) **User explicit authorization** for 2-3h compute window

## Why launch is deferred (current state)

Per §4.2 v0.7.1 paper-grade reasoning, the manuscript can ship without P6 verdict — the "3 candidate mechanisms remain to be disambiguated" wording in §A5.2 is paper-grade workable. P6 is *enrichment* not blocker:
- §A5 v0.7.1 (8d436e5) LOCKED with 3-mechanism wording stable
- T1 paper Results v0.5 (3259e79) absorbs T3 framing in §6 mosaic without depending on P6
- Manuscript spine fully RESUMED post-cycle-67 multi-erratum-cascade

Therefore launching P6 unilaterally consumes 2-3h compute for a verdict that doesn't change current paper-grade content. Better practice: stage launch when v0.5+ paper finalize cycle creates demand for sharper §A5.2 disambiguation, OR user explicit authorization.

## What P6 verdict would add to the paper

- **If SUPPORTED**: §A5.2 wording softens to "3 candidate mechanisms; mechanism (iii) RBM ansatz class intrinsic eliminated by P6"; outline §4.2 status updates P5 PROVISIONAL-DISCONFIRMED → CONDITIONAL-DISCONFIRMED-AT-FIXED-N_SAMPLES.
- **If DISCONFIRMED**: §A5.2 wording sharpens to "method-class intrinsic-limit ridge at α≈16 confirmed via dual axis (P5 monotonic + P6 sample-budget) intrinsic-not-extrinsic"; paper §4.2 strengthens to "RBM ansatz class intrinsic at this scale".
- **If PARTIAL**: §A5.2 keeps current 3-mechanism wording; §4.2 adds caveat "P6 partial signal preserves ambiguity, full resolution requires P2 inductive-bias test".

In all three branches, the manuscript is improved by P6 data, but submission is not blocked by absence of P6 verdict.

## Launch command

```bash
python attacks/T3_dwave/p6_alpha32_n_samples_8192.py
```

Output: `results/T3_v2_P6_hedge_N72_alpha32_nsamples8192.json` (deterministic structure
similar to existing `results/T3_v2_Pext_hedge_N72_alpha32.json`).

## Post-launch handoff plan

After P6 verdict lands:
1. Commit JSON output + push origin/claude3
2. Update Source Data CSV via `python attacks/T3_dwave/export_source_data.py` (add new figure)
3. Notify claude4 (paper integration) + claude5 (ThresholdJudge) + claude7 (case #38 candidate)
4. §A5 v0.x patch absorbing P6 verdict (request claude4 to integrate)
5. Outline v0.7.x patch reflecting verdict in P6 prediction track record
