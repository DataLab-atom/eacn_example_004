# Willow-Scale (64q 8x8) Depth + Truncation Sweep — MEASURED

## d=4
| w_max | Terms | OTOC^(2) | Time | Converged? |
|-------|-------|----------|------|-----------|
| 4 | 1,908 | +0.715 | 14s | partial |
| 6 | 4,095 | +0.979 | 97s | near-converged |

## d=6
| w_max | Terms | OTOC^(2) | Time |
|-------|-------|----------|------|
| 4 | 20,408 | +0.019 | 416s |

## d=8 (running)
Pending...

## Comparison: 64q is Willow's OTOC^(2) target scale
- Google claims: 65q OTOC^(2), 13000x faster than Frontier TN
- Our SPD: 64q d=4 w≤6 in 97 seconds on laptop CPU
- At d=4, SPD produces near-converged OTOC^(2) = 0.979

## Critical depth question
- d=4: fully feasible (97s at w≤6)
- d=6: 20k terms at w≤4, likely needs w≤6-8 (~hours estimate)
- d=8+: pending, may require streaming or GPU

*Generated 2026-04-26. All results on single laptop CPU, seed=42.*
