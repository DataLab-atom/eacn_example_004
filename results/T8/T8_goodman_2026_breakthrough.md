# T8/T7: Goodman et al. (2026.04) — Potential Game Changer

**Paper**: arXiv:2604.12330, "Gaussian boson sampling: Benchmarking quantum advantage"
**Date discovered**: 2026-04-26

## Key Claims

1. **Positive-P phase-space sampler** — fundamentally different from Oh MPS
2. **Tested at 1152 modes** (JZ 3 high-power raw data)
3. **Beats quantum experiments**: Z-score ≤ 3 vs experiments deviate by hundreds of σ
4. **Quadratic complexity** in modes — polynomial, not exponential
5. **JZ 4.0 claimed feasible** with moderate resources

## Impact on Our Work

### T8 (JZ 3.0, 144 modes)
- Goodman tested at 1152 modes — 144 is trivial
- If their claims hold, T8 may ALREADY be broken by this paper
- Our Oh-MPS approach is superseded by positive-P

### T7 (JZ 4.0, 8176 modes)
- Authors claim quadratic scaling enables JZ 4.0
- This is the first classical method with potential for T7
- Supersedes Oh (eta_crit too low) and Bulmer (exponential cost)

## Verification Needed

1. Are the benchmarks (Z-score) comparable to XEB/HOG?
2. Is "closer to ground-truth than experiment" the same as "classical simulation"?
3. Quadratic scaling claim — does it hold at 8176 modes?
4. Peer review status — this is a fresh preprint

## Relationship to Our Oh-MPS Work

Our T8 results (Oh et al. framework, Gaussian baseline, HOG benchmark)
remain valuable as INDEPENDENT verification. If Goodman's positive-P
also works, we have TWO independent classical methods for JZ 3.0:
- Oh MPS (our work) — loss-exploitation based
- Goodman positive-P — phase-space based
This strengthens the attack by providing §D5 multi-method cross-validation.

## Code Verification (2026-04-26)

**GitHub repository verified**: github.com/peterddrummond/xqsim EXISTS
- Language: MATLAB (100%)
- Key directory: xQSimGBSExperiments (GBS-specific code)
- 4 commits, 2 stars, 1 fork
- Includes: xQSimCode (core), xQSimExamples, xQSimExpDataExtract
- Paper §F1 compliance: code publicly accessible (not Zenodo-archived yet)

This confirms Goodman et al.'s reproducibility claim at code-availability level.
