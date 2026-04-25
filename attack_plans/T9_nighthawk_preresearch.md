# T9 Pre-Research: IBM Nighthawk

**Attacker**: claude2
**Branch**: claude2
**Status**: Pre-research only (per README.md T9 trigger condition)
**Last updated**: 2026-04-26

---

## Target Summary

| Field | Value |
|---|---|
| **Hardware** | IBM Nighthawk 120 qubit, 218 couplers, square lattice |
| **Claim** | Supports 5000 2-qubit gates; roadmap: verified QA by 2026 |
| **Status** | Hardware announced, NO formal paper yet |
| **README trigger** | "论文一旦发布, 立即从预研切换到反击" |

## Pre-Research: Framework Ready

### gPEPS + Belief Propagation
- Square lattice perfectly fits gPEPS (Patra et al. PRR 2024)
- Tindall TN+BP (PRXQ 2024) broke IBM Eagle on heavy-hex
- Square lattice is SIMPLER than heavy-hex → BP should work better
- Pre-build: gPEPS framework on 120-qubit square lattice connectivity

### SPD (from T2 analysis)
- IBM architecture → SPD directly applicable (Begusic SA 2024 precedent)
- T2 analysis shows Heron/Eagle ratio = 1.39x
- Nighthawk 120 qubit < Eagle 127 qubit → SPD should be EASIER
- SPD weight cutoff w=3: ~10^7 terms, feasible on laptop

### IBM Eagle Lesson
- Eagle utility experiment broken within WEEKS of publication
- By Tindall (TN+BP) and Begusic (SPD) independently
- Nighthawk likely faces same fate if it makes utility-type claims

## Prepared Attack Templates
1. SPD code: adapt from claude4's T1 spd_otoc_core.py
2. gPEPS: use cotengra/quimb for square lattice contraction
3. Benchmark: prepare HOG/XEB comparison framework

## Waiting For
- IBM formal paper with specific QA claim
- Circuit specification and benchmark details
