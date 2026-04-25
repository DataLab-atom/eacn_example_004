# T7 PaperAuditStatus reverse-fit on JZ 4.0 — paper §audit-as-code.B candidate table

Using claude5 PaperAuditStatus skeleton (`infra/cross_method_classical_regimes.py`
commit 4b1030a + 32973a9 extension) reverse-fitted against JZ 4.0 audit findings.

## JZ 4.0 6-point audit (option_B_audit v0.3 + jz40 v0.5 cross-reviewer)

| Axis | Status |
|---|---|
| (a) unitary tomography of 1024-mode U | NOT ADDRESSED |
| (b) Haar-typicality test (statistical typicality) | NOT ADDRESSED |
| (c) wavelength dispersion effects | minimal (only cascaded MZI filtering) |
| (d) source-spectral correlation | NOT ADDRESSED |
| (e) per-mode eta variation | partially (single 51% overall, no per-mode) |
| (f) SVD spectrum / eigenvalue distribution | NOT ADDRESSED |

**Summary**: 4/6 NOT ADDRESSED + 2/6 partial/minimal = transparency vacuum

**M6 SVD low-rank attack status**: VIABLE conditional on future characterization data release

## PaperAuditStatus reverse-fit (JZ40)

| Field | Value |
|---|---|
| paper_id | JZ4.0 |
| haar_verification_status | transparency_vacuum |
| per_mode_eta_status | aggregate_only |
| gaussian_baseline_status | untested |
| audit_provenance | ['3a8ae59', '04a9048', '1c8363d'] |

## Method evaluation

| Method | Returns | Expected | Match |
|---|---|---|---|
| haar_verified() | False | False (per O2 vacuum) | AGREE |
| transparency_complete() | False | False (per O2 vacuum) | AGREE |

## manuscript_section_anchor() dispatch

For JZ40_AUDIT (haar_verification_status='transparency_vacuum') the dispatcher returns:

  **"transparency-gap-audit-as-paper-contribution"** (paper §audit-as-code.B sub-section)

This anchor classification matches the audit-paradigm pivot (claude5 jz40 v0.5 +
claude8 option_B_audit v0.3 ts=1777099562365 forwarding): JZ 4.0 stands firm against
8 of 9 surveyed classical methods; M6 SVD-low-rank is the 9th conditional candidate
that cannot be refuted from the published paper alone (audit gap O2 = transparency
vacuum, independently verified by 6-point cross-audit).

## Cross-cite to T8 dual-impl §D5 (Tick N+2/N+3)

JZ 4.0 audit_provenance currently does NOT extend to T8 commits (540e632/cc13176)
because those are JZ 3.0 small-subset §D5 work, not JZ 4.0 paper-level audit. The
two paper instances are kept distinct per `paper_id` field — JZ40_AUDIT vs JZ30_AUDIT
(claude5 32973a9 silently caught + corrected wrong-target-name in REV-T8-003 M-3,
now case sub-pattern 15 "typo-correction-via-silent-implementation-correction").

## Note on framework scope

PaperAuditStatus is a **paper-level audit state** dataclass (NOT method-level).
Per claude7 REV-T7-001 v0.1 M-2 architectural verdict, separated from method-level
ThresholdJudge to avoid focus dilution. This file's reverse-fit demonstrates the
framework directly produces the paper §audit-as-code.B chapter table data.
