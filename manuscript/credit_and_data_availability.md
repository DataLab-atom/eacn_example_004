# §I Disclosures + §F Data/Code Availability

---

## CRediT Author Contributions (§I1)

| Role | Contributors |
|------|-------------|
| Conceptualization | claude4, claude5, claude6 |
| Methodology | claude4 (SPD/OTOC), claude3 (NQS/RBM), claude2 (GBS), claude7 (adaptive top-K), claude8 (Pauli-path/tail analysis) |
| Software | claude4 (spd_otoc_core.py), claude2 (GBS samplers), claude3 (T3 VMC), claude5 (infra), claude8 (tail_analysis.py) |
| Validation | claude7 (19 reviews), claude1 (cross-attack review), claude6 (DOI audit), claude8 (tail v3-v10) |
| Formal Analysis | claude4 (scaling law), claude8 (power-law alpha), claude7 (hotspot scaling) |
| Investigation | All 8 agents |
| Data Curation | claude4 (results/), claude3 (Source Data CSVs), claude2 (T8 data) |
| Writing — Original Draft | claude4 (T1 sections), claude3 (T3 sections), claude2 (T8 sections), claude1 (T6 §3 RCS) |
| Writing — Review & Editing | claude7, claude6, claude8 |
| Visualization | claude4 (Fig 1-2), claude3 (Fig 5-8 T3) |
| Supervision | User (human oversight) |
| Project Administration | claude5 (cascade coordination), claude6 (audit) |

## LLM Usage Disclosure (§I3)

All manuscript sections, code, and data analysis were produced by
Claude (Anthropic, models claude-opus-4-6 and claude-opus-4-7) under
human oversight. The human operator provided:
- Project direction and task assignment
- Repository setup and access credentials
- Periodic review of agent outputs
- Final approval of all commits

All numerical results were independently cross-validated by at least
2 of 3 independent classical paths (Path A SPD, Path B Pauli-path,
Path C adaptive top-K). All DOIs were independently web-verified
per the accepted_canon DOI verification rule established after the
Schuster-Yin DOI hallucination incident (commit 8e680ac).

## Data Availability (§I4)

All source data, code, and experimental results are available at:
- GitHub: https://github.com/DataLab-atom/eacn_example_004
  (branches: claude1-claude8, main)
- Zenodo DOI: [to be archived before submission per §F1]

Key data commits (claude4 branch):
- SPD core code: 78b05aa, 66f3608, bc65324
- Scaling data: 1f511ee, f265c51, b0d4cb0, 575b59b, 21519b3, ddb5c05
- Phase transition: 54216cd, c9784b7, ce81491
- Distance ladder: 23bd653, f6d1cac
- Tail analysis source: claude8 936c5e4, 0228d7e, 0ec8674, 627afb7, 953b155

## Code Availability (§I4)

Reproduction: `python code/spd_otoc_core.py` (validation suite)
Figures: `python code/generate_figures.py`
Environment: Python 3.11.9, NumPy 2.4.4, SciPy 1.17.1, matplotlib
License: [to be determined — MIT for code, CC-BY 4.0 for text per §F6]

---

*Draft v0.1, 2026-04-26.*
