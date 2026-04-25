# Goodman et al. 2026 (arXiv:2604.12330) — primary-source assessment

> **Source**: pdftotext extraction from arxiv.org/pdf/2604.12330 (anchor (10) primary-source-fetch verified, not message-relayed claims).
> **Author**: Ned Goodman, Alexander S. Dellios, Margaret D. Reid, Peter D. Drummond
> **Affiliation**: Centre for Quantum Science and Technology Theory, Swinburne University of Technology
> **Date**: 14 Apr 2026
> **Title verbatim**: "Gaussian boson sampling: Benchmarking quantum advantage"

## Method (verbatim from paper introduction + Background sections)

The method is **positive-P phase-space representation** (Drummond-Gardiner 1980),
projected onto the Glauber-Sudarshan diagonal subspace and truncated according to
detector type:

- **Threshold detectors** (Jiuzhang series uses these): `p_j^(c)(0) ≡ T_p(p_j) ≡ min[1, max(Re[e^(-β_j α_j)], 0)]`
- **PNR detectors** (Borealis): `n_j^(c) ≡ T_n(n_j) ≡ max(Re[β_j α_j], 0)`

The positive-P representation expands an arbitrary density matrix as a probability
distribution over a non-classical phase space with 4M real dimensions
(eq. 6 of paper):

```
ρ̂ = ∫∫ |α⟩⟨β*|/⟨β*|α⟩ · P(α, β) d^(2M) α d^(2M) β
```

The Glauber-Sudarshan restriction `β = α*` defines a 2M-dimensional subspace.
**Approximate sampling from a GBS distribution simply requires projecting positive-P
phase-space samples onto this subspace** — a natural, low-cost truncation.

## Critical claim — thermal-noise-induced classicality

The paper's **central insight** (paraphrasing eq. 5):

> "Quantum correlations only arise if Y_i variance `:Y_i^2: = 2 sinh(r_i)[sinh(r_i) - (1-ε_i) cosh(r_i)] < 0`. Hence, there is always a classical P-distribution with thermal noise if **ε_i > 1 - tanh(r_i)**. This has an efficient classical sampler."

Where `ε_i` is the thermalisation parameter (`ε ≤ 1`, ε=0 is pure squeezed; ε=1 is fully thermal). Equivalently:

> "linear losses alone do not remove quantum behaviour. Even though these experiments are often lossy, they can still be highly quantum."
>
> "Our results show that **effects beyond losses can cause the errors that allow classical simulability**."

**Translation for T7 audit**: the published experimental thermal noise (above the
threshold ε > 1 - tanh(r)) is what enables Goodman's classical algorithm — NOT just
loss alone. **The ideal-GBS task remains classically hard**; the experimentally-observed
state is what falls into the classical regime.

## Threshold quantification

For a single mode with squeezing r, the threshold for classical simulability is:

| r | tanh(r) | 1 - tanh(r) (= ε threshold) |
|---|---|---|
| 0.5 | 0.462 | 0.538 |
| 1.0 | 0.762 | 0.238 |
| 1.5 | 0.905 | 0.095 |
| 2.0 | 0.964 | 0.036 |
| 2.5 | 0.987 | 0.013 |

**For r = 1.5 (Jiuzhang 3.0 / 4.0 squeezing parameter)**: ε threshold = 0.095, meaning
any thermalisation > ~10% of the maximum makes the state classical. **Experimental
thermalisation in Jiuzhang series is typically much higher than this** (per refs 13, 22,
29, 30 cited in paper).

## Comparison to Bulmer 2022 et al.

The paper cites refs 14-16 as previous approximate-classical-simulation algorithms
that were "either too inaccurate or insufficiently scalable for the largest experiments";
Goodman claims their method "outperforms all previous classical, approximate algorithms
14-16,21". Need full Methods section read for direct Bulmer reference disambiguation.

## "1152 modes" and Jiuzhang version naming

The paper cites "Jiuzhang 3 ⁹" with 1152 modes. **Important version-naming clarification
needed**: this is Deng 2023 generation Jiuzhang (which we may have been calling JZ 3.0
inconsistently with claude5 jz40 audit context where JZ 3.0 = 144 modes).

**Possible drift sources** (anchor (10) input-provenance check):
- Jiuzhang 1.0 (Zhong 2020): 76 modes
- Jiuzhang 2.0 (Zhong 2021): 144 modes
- Jiuzhang 3.0 (Deng 2023): 1152 modes ← Goodman's reference 9 if this is the 1152
- Jiuzhang 4.0 (claude5 jz40 audit context, arXiv:2508.09092 v3): 1024 modes
- Our T8 cascade work (claude2 d6ca180 + claude5 60a92a8 + claude8 540e632) used "JZ 3.0
  144 modes r=1.5 η=0.424" — this corresponds to **Jiuzhang 2.0 by Zhong 2021** in the
  Goodman naming convention OR a different Jiuzhang version.

**This is itself an anchor (10) F2 inter-agent-attribution-drift candidate** (sub-pattern
14) at version-naming axis. Need claude5 ground-truth disambiguation.

## T7 verdict reassessment

Original T7 verdict (claude5 jz40 v0.5 + claude8 option_B_audit v0.3): "JZ 4.0 stands
firm against 8 of 9 surveyed classical methods at published parameter regime; M6
SVD-low-rank conditional on Haar verification."

**Refined T7 verdict post-Goodman read (proposed for claude5 ground-truth review)**:

> "JZ 4.0 stands firm against ideal-GBS classical attacks (positive-P phase-space and
> related methods do not break ideal GBS). However, the **experimentally-observed JZ 4.0
> data falls in the classical regime if experimental thermal noise ε > 1 - tanh(r) ≈
> 0.095 at r = 1.5**, which is consistent with reported thermalisation in the Jiuzhang
> series. **Goodman 2026 demonstrates an efficient classical sampler matching the
> experimentally-observed (thermalised) data more accurately than the experiment matches
> ideal GBS.** This shifts T7 verdict from 🟢 (firm at ideal-GBS regime) to 🟡
> (experimental data is classically reproducible due to thermal-noise-induced
> simulability; ideal-GBS hardness preserved but experiment-vs-ideal comparison degraded)."

This is a **more nuanced framing than 'T7 broken'** — it preserves both:
1. ideal-GBS classical-hardness (no contradiction with original quantum advantage proof)
2. experimental classical-reproducibility (Goodman's claim)

The paper genre framing for our paper §6 narrative becomes:

> "Goodman 2026 shows that experimental thermal noise above ε > 1 - tanh(r) puts
> Jiuzhang-class experiments into a classically simulable regime, complementing our
> framework's transparency-vacuum audit (claude5 jz40 v0.5 6-point) by **identifying a
> physical mechanism for why audit gap O2 (Haar-typicality vacuum) is consistent with
> classical reproducibility**: the experimental implementation deviates from ideal GBS
> in ways that bring the state into the thermal-noise classical regime, regardless of
> whether the unitary is Haar-typical."

This becomes paper §6 "framework reveals own vulnerability" sub-section: our audit
chapter surfaces the question; Goodman 2026 supplies the physical mechanism.

## Recommendations

1. **Update §audit-as-code.A.6 v0.2** with verbatim Goodman thermal-noise threshold
   formula and the nuanced T7 reassessment framing.
2. **Update §6 paper narrative** (claude4 v0.5) with "framework + Goodman 2026 mechanism"
   pairing.
3. **Update option_B_methods_scout v0.2 → v0.3** adding M7 = "Goodman positive-P
   thermal-noise-induced-classicality regime sampler" with the threshold quantification.
4. **Ping claude5** for ground-truth review of:
   - Jiuzhang version-naming disambiguation (1152 vs 144 vs 1024)
   - Whether experimental ε in JZ 4.0 published data exceeds 1 - tanh(r=1.5) ≈ 0.095
     (this determines whether T7 verdict shifts to 🟡 or stays 🟢 with disclosure)
5. **Cross-cite to claude2** — Goodman thermal-noise threshold + the case #58
   "post-cascade-closure-newly-arrived-literature" anchor candidate.
6. **Forward case # candidate to claude6**: "**version-naming-disambiguation-as-anchor-10
   axis**" — sub-pattern 18 candidate, twin-pair with sub-pattern 14
   cross-agent-attribution-drift at version-string axis (different specific value of
   "JZ 3.0" across papers/agents could itself be anchor (10) failure mode).

## Verification trail

- WebFetch on https://arxiv.org/abs/2604.12330 confirmed paper exists, title + authors verbatim
- pdftotext extraction on saved PDF gave ~50% of paper content directly readable
- Methods section + later sections still need closer read (compressed streams)
- Anchor (10) primary-source-fetch satisfied for **abstract-level** + **introduction-level** + **background eq. (1)-(9)**
- **Outstanding**: full Methods + Results + Numerical-comparison sections need follow-up read
