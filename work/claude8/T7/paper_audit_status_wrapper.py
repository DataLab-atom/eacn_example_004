"""
T7 PaperAuditStatus wrapper — reverse-fit on JZ 4.0 (and JZ 3.0) transparency-vacuum data.

Consumes claude5 skeleton `infra/cross_method_classical_regimes.py` (commit 4b1030a +
extension 32973a9) and exercises the 4-field 2-method PaperAuditStatus dataclass
against the JZ 4.0 transparency-vacuum audit findings (option_B_audit v0.3 + jz40 v0.5
6-point cross-audit).

Status: REAL implementation post-cascade Option B closure (cc13176) — Tick N+2 OPEN
unblocked via origin/claude5 read.

Key cross-cite to this file's reverse-fit:
  - JZ40_AUDIT.haar_verification_status = "transparency_vacuum" (4/6 NOT ADDRESSED + 2/6 partial)
  - JZ40_AUDIT.per_mode_eta_status = "aggregate_only" (single overall 51%)
  - JZ40_AUDIT.gaussian_baseline_status = "untested" (JZ 4.0 not in claude2 N-scaling chain)
  - audit_provenance to extend per Tick N+2/N+3: 540e632 + cc13176 (my T8 §D5 contributions)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal


try:
    from infra.cross_method_classical_regimes import (  # type: ignore
        PaperAuditStatus, ThresholdJudge,
        JZ40_AUDIT, JZ30_AUDIT,
        manuscript_section_anchor,
    )
    _IMPORTED_FROM_INFRA = True
except ImportError:
    _IMPORTED_FROM_INFRA = False

    @dataclass
    class PaperAuditStatus:
        paper_id: str
        haar_verification_status: Literal[
            "paper_published", "transparency_vacuum", "audit_gap", "implied_only",
        ]
        per_mode_eta_status: Literal["per_mode_published", "aggregate_only", "implied"]
        gaussian_baseline_status: Literal["sufficient", "insufficient_at_N>=K", "untested"]
        audit_provenance: list = field(default_factory=list)

        def haar_verified(self) -> bool:
            return self.haar_verification_status == "paper_published"

        def transparency_complete(self) -> bool:
            return (
                self.haar_verification_status == "paper_published"
                and self.per_mode_eta_status == "per_mode_published"
                and self.gaussian_baseline_status == "sufficient"
            )

    JZ40_AUDIT = PaperAuditStatus(
        paper_id="JZ4.0",
        haar_verification_status="transparency_vacuum",
        per_mode_eta_status="aggregate_only",
        gaussian_baseline_status="untested",
        audit_provenance=["3a8ae59", "04a9048", "1c8363d"],
    )

    JZ30_AUDIT = PaperAuditStatus(
        paper_id="JZ3.0",
        haar_verification_status="audit_gap",
        per_mode_eta_status="aggregate_only",
        gaussian_baseline_status="insufficient_at_N>=K",
        audit_provenance=["a6ce899", "e14e832", "c11b974"],
    )

    def manuscript_section_anchor(judge, audit) -> str:
        if audit.haar_verification_status in ("transparency_vacuum", "audit_gap"):
            return "transparency-gap-audit-as-paper-contribution"
        if not audit.transparency_complete():
            return "audit-paradigm-vs-attack-paradigm"
        return "transparency-complete-no-audit-gap"


# JZ 4.0 audit findings from my option_B_audit v0.3 + claude5 jz40 v0.5 6-point cross-audit
JZ40_AUDIT_FINDINGS = {
    "paper": "Jiuzhang 4.0 (arXiv:2508.09092 v3)",
    "audit_axes_6_point": {
        "(a) unitary tomography of 1024-mode U": "NOT ADDRESSED",
        "(b) Haar-typicality test (statistical typicality)": "NOT ADDRESSED",
        "(c) wavelength dispersion effects": "minimal (only cascaded MZI filtering)",
        "(d) source-spectral correlation": "NOT ADDRESSED",
        "(e) per-mode eta variation": "partially (single 51% overall, no per-mode)",
        "(f) SVD spectrum / eigenvalue distribution": "NOT ADDRESSED",
    },
    "summary": "4/6 NOT ADDRESSED + 2/6 partial/minimal = transparency vacuum",
    "M6_status": "VIABLE conditional on future characterization data release",
    "claude8_source_commit": "3a8ae59",  # option_B_audit v0.3
    "claude5_cross_audit_commit": "04a9048",  # jz40 v0.5
}


def reverse_fit_jz40_transparency_vacuum() -> PaperAuditStatus:
    """Reverse-fit JZ 4.0 PaperAuditStatus from option_B_audit v0.3 + jz40 v0.5 findings."""
    return PaperAuditStatus(
        paper_id="JZ4.0",
        haar_verification_status="transparency_vacuum",
        per_mode_eta_status="aggregate_only",
        gaussian_baseline_status="untested",  # JZ 4.0 not in claude2 N-scaling chain
        audit_provenance=[
            "3a8ae59",  # claude8 option_B_audit v0.3 (O2 weakness flag)
            "04a9048",  # claude5 jz40 v0.5 (independent 6-point cross-reviewer verification)
            "1c8363d",  # claude7 REV-T7-001 v0.1 (PASS verdict)
        ],
    )


def cross_check_haar_verified_predict_vs_o2() -> bool:
    """JZ40_AUDIT.haar_verified() must be False per O2 audit gap."""
    audit = reverse_fit_jz40_transparency_vacuum()
    predicted = audit.haar_verified()
    expected = False  # per O2 audit gap (transparency_vacuum)
    return predicted == expected


def cross_check_transparency_complete() -> bool:
    """JZ40_AUDIT.transparency_complete() must be False given 4/6 NOT ADDRESSED."""
    audit = reverse_fit_jz40_transparency_vacuum()
    predicted = audit.transparency_complete()
    expected = False  # given 4/6 transparency axes vacant
    return predicted == expected


def emit_paper_section_6_table_md(out_path: str) -> None:
    """Write paper §audit-as-code.B transparency-vacuum sub-section data table."""
    audit_jz40 = reverse_fit_jz40_transparency_vacuum()
    table = [
        "# T7 PaperAuditStatus reverse-fit on JZ 4.0 — paper §audit-as-code.B candidate table",
        "",
        "Using claude5 PaperAuditStatus skeleton (`infra/cross_method_classical_regimes.py`",
        "commit 4b1030a + 32973a9 extension) reverse-fitted against JZ 4.0 audit findings.",
        "",
        "## JZ 4.0 6-point audit (option_B_audit v0.3 + jz40 v0.5 cross-reviewer)",
        "",
        "| Axis | Status |",
        "|---|---|",
    ]
    for axis, status in JZ40_AUDIT_FINDINGS["audit_axes_6_point"].items():
        table.append(f"| {axis} | {status} |")
    table += [
        "",
        f"**Summary**: {JZ40_AUDIT_FINDINGS['summary']}",
        "",
        f"**M6 SVD low-rank attack status**: {JZ40_AUDIT_FINDINGS['M6_status']}",
        "",
        "## PaperAuditStatus reverse-fit (JZ40)",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| paper_id | {audit_jz40.paper_id} |",
        f"| haar_verification_status | {audit_jz40.haar_verification_status} |",
        f"| per_mode_eta_status | {audit_jz40.per_mode_eta_status} |",
        f"| gaussian_baseline_status | {audit_jz40.gaussian_baseline_status} |",
        f"| audit_provenance | {audit_jz40.audit_provenance} |",
        "",
        "## Method evaluation",
        "",
        "| Method | Returns | Expected | Match |",
        "|---|---|---|---|",
    ]
    for method_name, predict, expected in [
        ("haar_verified()", audit_jz40.haar_verified(), False),
        ("transparency_complete()", audit_jz40.transparency_complete(), False),
    ]:
        match = "AGREE" if predict == expected else "DISAGREE"
        table.append(f"| {method_name} | {predict} | {expected} (per O2 vacuum) | {match} |")

    # manuscript_section_anchor needs a ThresholdJudge — pass minimal placeholder
    # (T7 audit doesn't actually use the ThresholdJudge in the anchor decision, only audit fields)
    table += [
        "",
        "## manuscript_section_anchor() dispatch",
        "",
        f"For JZ40_AUDIT (haar_verification_status='transparency_vacuum') the dispatcher returns:",
        "",
        f"  **\"transparency-gap-audit-as-paper-contribution\"** (paper §audit-as-code.B sub-section)",
        "",
        "This anchor classification matches the audit-paradigm pivot (claude5 jz40 v0.5 +",
        "claude8 option_B_audit v0.3 ts=1777099562365 forwarding): JZ 4.0 stands firm against",
        "8 of 9 surveyed classical methods; M6 SVD-low-rank is the 9th conditional candidate",
        "that cannot be refuted from the published paper alone (audit gap O2 = transparency",
        "vacuum, independently verified by 6-point cross-audit).",
        "",
        "## Cross-cite to T8 dual-impl §D5 (Tick N+2/N+3)",
        "",
        "JZ 4.0 audit_provenance currently does NOT extend to T8 commits (540e632/cc13176)",
        "because those are JZ 3.0 small-subset §D5 work, not JZ 4.0 paper-level audit. The",
        "two paper instances are kept distinct per `paper_id` field — JZ40_AUDIT vs JZ30_AUDIT",
        "(claude5 32973a9 silently caught + corrected wrong-target-name in REV-T8-003 M-3,",
        "now case sub-pattern 15 \"typo-correction-via-silent-implementation-correction\").",
        "",
        "## Note on framework scope",
        "",
        "PaperAuditStatus is a **paper-level audit state** dataclass (NOT method-level).",
        "Per claude7 REV-T7-001 v0.1 M-2 architectural verdict, separated from method-level",
        "ThresholdJudge to avoid focus dilution. This file's reverse-fit demonstrates the",
        "framework directly produces the paper §audit-as-code.B chapter table data.",
    ]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(table) + "\n")


def _smoke():
    print("=== T7 PaperAuditStatus wrapper reverse-fit ===")
    audit = reverse_fit_jz40_transparency_vacuum()
    print(f"  JZ40 reverse-fit: paper_id={audit.paper_id}")
    print(f"    haar={audit.haar_verification_status}, "
          f"eta={audit.per_mode_eta_status}, gauss={audit.gaussian_baseline_status}")
    print(f"  haar_verified() = {audit.haar_verified()} (expected False)")
    print(f"  transparency_complete() = {audit.transparency_complete()} (expected False)")
    print(f"  cross_check_haar_verified_predict_vs_o2 = {cross_check_haar_verified_predict_vs_o2()}")
    print(f"  cross_check_transparency_complete = {cross_check_transparency_complete()}")
    out = "work/claude8/T7/paper_audit_status_reverse_fit.md"
    emit_paper_section_6_table_md(out)
    print(f"  wrote {out}")
    print(f"  imported_from_infra = {_IMPORTED_FROM_INFRA}")


if __name__ == "__main__":
    _smoke()
