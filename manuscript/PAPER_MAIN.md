# Classical Simulation of Quantum Advantage Experiments: A Systematic Evaluation Revealing Regime-Dependent Boundaries

> **Target**: Nature / Science
> **Version**: Assembly v0.1 (2026-04-26)
> **Status**: All §A-J sections at first-version paper-grade. 58 commits on claude4.
> **Component files**: T1_abstract_intro_draft.md, T1_results_draft.md, T1_methods_draft.md, T1_discussion_draft.md, section_A5_draft.md, references.md, cover_letter_draft.md, credit_and_data_availability.md, figure_plan.md
> **Cross-target components**: claude1 §3 RCS T6 (d2676d4), claude2 T8 4-section, claude3 T3 full suite (ce6fe8b+), claude8 §audit-as-code.A (9607ead)

---

## Paper Structure Map

| Section | File | Version | Reviewer Status |
|---------|------|---------|----------------|
| Abstract | T1_abstract_intro_draft.md | v0.1 | — |
| §1 Introduction | T1_abstract_intro_draft.md | v0.1 | — |
| §2 Results | T1_results_draft.md | v0.6 | claude7 REV-T1-008 v0.2 PASSES + claude8 PASSES + claude1 REV-CROSS-T1-002 PASSES |
| §3 Methods | T1_methods_draft.md | v0.1 | claude7 REV-T1-008 v0.3 PASSES EXEMPLARY |
| §4 Discussion | T1_discussion_draft.md | v0.2 | claude5 REV-DISCUSSION-v01 PASSES + claude1 PASSES |
| §5 Limitations | section_A5_draft.md | v0.7.1 | claude3 FINAL VERIFY-PASS + claude2 REV-A5-001 PASSES |
| §6 References | references.md | v0.1 (23 refs) | — |
| Figures | figures/ | Fig 1-2 generated | Fig 3-4 planned |
| Cover Letter | cover_letter_draft.md | v0.1 + 5 Q&A | — |
| CRediT + Data | credit_and_data_availability.md | v0.1 | — |

## Cross-Target Integration Points

| Target | Lead | Paper Section | Status |
|--------|------|--------------|--------|
| T1 Quantum Echoes | claude4 | §2 R1-R7 + §3 D1-D9 + §4 mosaic | ✅ paper-headline-grade |
| T3 D-Wave | claude3 | §5 A5.1-A5.3 + §4 T3 paragraph | ✅ all deliverables ready |
| T6 ZCZ 2.0/2.1 | claude1 | §4 T6 boundary type | ✅ §3 RCS v0.1.2 |
| T7 Jiuzhang 4.0 | claude5 | §4 T7 stands firm + §5 transparency-vacuum | ✅ jz40 v0.8 |
| T8 Jiuzhang 3.0 | claude2 | §5 A5.4 + §4 T8 paragraph | ✅ 4-section draft |

## Remaining Items Before Submission

| Item | Owner | Priority | Blocked on |
|------|-------|----------|-----------|
| Canon PR to main | claude4 | HIGH | gh auth login |
| Zenodo DOI archival | user | HIGH | GitHub action |
| Fig 3 schematic (4 boundary types) | claude4 | MEDIUM | manual design |
| Fig 4 Path B+C cost bars | claude4 | MEDIUM | data in Discussion |
| v0.7+ non-blocking micros | claude4 | LOW | none |
| T3 §E3 robustness scan | claude3 | MEDIUM | background running |
| Claude8 §audit-as-code.B/C/D | claude8 | MEDIUM | drafting |
| Final cross-target assembly | claude4+all | HIGH | all sections ready ✅ |

---

*Assembly v0.1, 2026-04-26. 8 agents, 9 targets evaluated, 4 boundary types discovered.*
*58 commits on claude4 branch. All §A-J sections paper-grade first version.*
