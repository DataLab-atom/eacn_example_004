# claude4 Session Log — 2026-04-25

## Timeline

| Time | Action | Commit |
|------|--------|--------|
| Start | Connect EACN3, register as claude4, create branch | — |
| +10m | Team setup, target allocation broadcast | — |
| +20m | T1 literature survey: Szasz TNBP failure + Schuster-Yao theory | b46a15a |
| +30m | SPD OTOC^(1) core implementation | d63974f |
| +35m | Bug fix: Heisenberg gate ordering | 78b05aa |
| +45m | R-1: Lookup table optimization (20-77x speedup) | 66f3608 |
| +55m | R-2: OTOC^(2) second-order correlator | bc65324 |
| +65m | Phase 2: noise convergence (8q) | 9a22484 |
| +75m | Canon v2 merge (9 entries) | f03fb3e |
| +80m | T4 peer review (REV-20260425-T4-001) | 754e7a4 |
| +85m | Canon DOI hallucination fix (Schuster-Yin 404) | 8e680ac |
| +87m | Canon DOI verification rule | d7b4133 |
| +95m | Phase 3: 10q exact validation + depth scaling | 08eeb75 |
| +100m | Midterm assessment: strategy pivot to noisy OTOC^(2) | 6924855 |
| +110m | Phase 3b: noise does NOT reduce truncation | 694d65d |
| +120m | POSITIVE: grid topology makes 65q feasible | 1f511ee |
| +125m | Scaling law summary + decision matrix | 866eccc |
| +130m | Willow grid generator + cost estimator | 35361d1 |
| +140m | 16q Pauli term export for claude7 hotspot | 0775fa7 |

## Key Scientific Contributions
1. First SPD application to OTOC circuits (validated)
2. OTOC^(2) implementation with efficient A^2 computation
3. Discovery: noise does NOT help OTOC^(2) truncation (negative)
4. Discovery: grid topology dominates truncation (positive)
5. Decision matrix for 65q attack feasibility
6. Hotspot analysis: OTOC propagates along shortest M→B path

## Collaboration
- claude3: high-quality R-1/R-2 review → both fixed
- claude7: T1 SPD co-attacker, adaptive Path C
- claude8: T1 Pauli-path Path B, extracting Willow params
- claude2: T4 XEB breakthrough, reviewed by me
- claude6: canon reviewer + DOI hallucination catch

## Pending
- Willow params from claude7/claude8 (GO/NO-GO)
- Canon PR to main (need gh auth)
- M-B distance vs w_min study (running)
