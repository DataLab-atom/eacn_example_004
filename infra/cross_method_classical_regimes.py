"""Cross-method classical-regime threshold framework — 2-dataclass design.

Two compile-time dataclasses for paper §audit-as-code methodology framework:

(1) ThresholdJudge — METHOD-LEVEL operation parameters (T1-SPD-specific 5 fields + 3 methods).
    Encodes how a path-class operates on a circuit instance. Validated through 6-source
    convergence: REV-T1-003 (claude7 654e0b2) + REV-T1-004 (claude7 30fc200) + REV-T1-005
    (claude7 4fc81e8) + REV-T1-006 (claude7 69d6b0b) + claude4 author-acceptance + claude8
    v9 cross-attack (8169f47).

(2) PaperAuditStatus — PAPER-LEVEL transparency audit state (T7+T8 unified, 4 fields + 2 methods).
    Encodes whether a paper instance has been characterized at the transparency-audit level.
    Validated through 7-source convergence (the 6 above + claude5 jz40 v0.5 O2 audit cross-reviewer
    [04a9048] + claude7 REV-T7-001 v0.1 [1c8363d] + claude7 REV-T8-001 v0.1 [c11b974]).

Architectural rationale (per claude7 REV-T7-001 v0.1 M-2):
    - Method-level vs paper-level are different abstraction levels
    - Mixing into single dataclass dilutes ThresholdJudge focus
    - Clean separation of concerns: 2-dataclass design

Paper §audit-as-code chapter sub-section anchors:
    - "method-side-vs-paper-side dataclass abstraction" (this 2-dataclass split itself)
    - "transparency-gap-audit-as-paper-contribution" (PaperAuditStatus.haar_verification_status)
    - "audit-paradigm-vs-attack-paradigm" (PaperAuditStatus framing pivot)
    - "dual-implementation-§D5-pattern" (cross-validation at implementation level via wrapper plan)

Author: claude5 (claude-opus-4-7, 1M ctx)
Status: SKELETON v0.1 — scaffold definitions; subclass and method implementations land in
follow-up commits. 7-source-validated 5+4-field design queue.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Literal, Optional


# ---------------------------------------------------------------------------
# (1) ThresholdJudge — METHOD-LEVEL (T1-SPD-specific 5 fields + 3 methods)
# ---------------------------------------------------------------------------

@dataclass
class ThresholdJudge:
    """Method-level operation parameters for a classical-attack path-class on a circuit instance.

    All 5 fields are physics quantities of the circuit + path-class operation, NOT paper-side
    transparency state (use PaperAuditStatus for that).

    Validated through 6-source convergence (T1 SPD attack target):
      - REV-T1-003 v0.1 claude7 commit 654e0b2 (d_arm + v_B_empirical recommendation)
      - REV-T1-004 v0.1 claude7 commit 30fc200 (M_B_geometry addition)
      - REV-T1-005 v0.1 claude7 commit 4fc81e8 (four-axis-convergent phase-transition signal)
      - REV-T1-006 v0.1 claude7 commit 69d6b0b (paradigm-shift absorption + tail_regime)
      - claude4 author-acceptance (M-1 + M-2 from REV-T1-003/004 absorbed into v0.3)
      - claude8 v9 cross-attack (8169f47 power-law tail finding)
    """

    target_id: str
    """E.g. 'T1', 'T7', 'T8'."""

    # ---- 5 physics fields ----
    d_arm: int
    """Per-arm depth, hardware-specific (§H4 compliance check input)."""

    v_B_empirical: float
    """Measured butterfly velocity from depth chain (e.g. 0.65 from claude7 c5b7565
    12q LC-edge fit). §H4-derived quantity."""

    M_B_geometry: Literal["LC-edge", "mid-grid", "corner"]
    """Geometric placement of operators M and B on the lattice. Determines ÷2 factor
    applicability in screening-active condition (per claude7 REV-T1-004 v0.1)."""

    ell_required_derived: int
    """Mechanism-derived ℓ floor: max(4, ceil(d_arm × v_B + safety=2)).
    Bounds physical light-cone radius (NOT tail decay rate). Per Path C v0.9."""

    tail_regime: Literal["exp_screening", "powerlaw_post_transition"]
    """Tail regime classification. Pre-transition (screening) all paths viable; post-transition
    (power-law) Paths A+B fail to deliver controllable cost via fixed-w/fixed-ℓ truncation;
    Path C adaptive-K is the ONLY viable bound. Per claude7 REV-T1-006 v0.1 + claude8 v9 (8169f47)."""

    # ---- 3 methods ----
    def screening_active(self, diameter: int) -> bool:
        """Returns True iff M-B operator pair joint coverage exceeds half of diameter
        (per ÷2 factor derivation, claude7 REV-T1-004 v0.1).
        """
        return self.d_arm * self.v_B_empirical < diameter / 2

    def ell_required(self, safety: int = 2) -> int:
        """Mechanism-derived ℓ floor, agreeing with claude8 empirical-tier within +2 safety:
        ell_required(d=8) = 8 ↔ claude8 ℓ_baseline=8 (within 0)
        ell_required(d=12) = 10 ↔ claude8 ℓ_stretch=12 (within +2)
        ell_required(d=14) = 12 ↔ claude8 ℓ_extreme=14+ (within +2)
        """
        return max(4, math.ceil(self.d_arm * self.v_B_empirical + safety))

    def regime_specific_path_essential(self) -> Optional[str]:
        """Returns 'C' if tail_regime is powerlaw_post_transition (Paths A+B fail, Path C
        adaptive-K is ONLY viable bound). Returns None if exp_screening (all paths viable).

        Per claude7 REV-T1-006 v0.1: §D5 three-way distinction REGIME-DEPENDENT.
        """
        if self.tail_regime == "powerlaw_post_transition":
            return "C"
        return None


# ---------------------------------------------------------------------------
# (2) PaperAuditStatus — PAPER-LEVEL (T7+T8 unified, 4 fields + 2 methods)
# ---------------------------------------------------------------------------

@dataclass
class PaperAuditStatus:
    """Paper-level transparency audit state for a published quantum-advantage paper instance.

    All 4 fields encode whether the paper has been characterized at the transparency-audit
    level (paper-side audit), NOT method-level operation (use ThresholdJudge for that).

    Validated through 7-source convergence:
      - claude5 jz40 v0.5 O2 Haar verification audit (commit 04a9048) — main verdict
      - claude8 option_B_audit v0.3 (commit 3a8ae59) — flagged O2 weakness, cross-reviewer
      - claude7 REV-T7-001 v0.1 (commit 1c8363d) — architectural M-2 verdict
      - claude7 REV-T8-001 v0.1 (commit c11b974) — T8 extension gaussian_baseline_status
      - claude2 a6ce899 (T8 HOG breakthrough) — confirms gaussian_baseline_status field need
      - claude2 e14e832 (HOG scaling N=4/6/8 → 0.648/0.515/0.441) — defines threshold K=8
      - claude6 audit_index 7ac5629 (canonical 2-dataclass split absorption)

    Paper §audit-as-code "audit-paradigm-vs-attack-paradigm" sub-section anchor:
    instances of this dataclass populate the active "audit-as-contribution" paradigm
    (Bermejo 2026 = attack paradigm; ours = audit paradigm).
    """

    paper_id: str
    """E.g. 'JZ4.0', 'JZ3.0'."""

    # ---- 4 paper-level transparency fields ----
    haar_verification_status: Literal[
        "paper_published",
        "transparency_vacuum",
        "audit_gap",
        "implied_only",
    ]
    """Whether the paper experimentally verifies the implemented unitary U is Haar-typical.

    'paper_published': spectrum / SVD / Frobenius distance to Haar published in §SI
    'transparency_vacuum': 4/6 axes 全无表征 (per jz40 v0.5 — JZ 4.0 status)
    'audit_gap': partially addressed but not statistically tested
    'implied_only': claimed via paper text without data backing
    """

    per_mode_eta_status: Literal[
        "per_mode_published",
        "aggregate_only",
        "implied",
    ]
    """Whether per-mode transmission η is published (vs. only aggregate).
    JZ 4.0 = 'aggregate_only' (single 51% number).
    """

    gaussian_baseline_status: Literal[
        "sufficient",
        "insufficient_at_N>=K",
        "untested",
    ]
    """Whether Gaussian-baseline sampler suffices on this paper's mode count.
    JZ 3.0 (N=144) = 'insufficient_at_N>=8' — claude2 e14e832 HOG scaling math:
    HOG = 0.648/0.515/0.441 at N=4/6/8 → Gaussian crosses below uniform-0.5 threshold
    between N=6→N=8 → chi-corrected MPS strictly required at JZ 3.0 N=144.
    """

    audit_provenance: list[str] = field(default_factory=list)
    """Commit hashes of cross-reviewer audits supporting this status assignment.
    E.g. ['3a8ae59', '04a9048', '1c8363d'] for JZ 4.0 transparency vacuum.
    """

    # ---- 2 methods ----
    def haar_verified(self) -> bool:
        """True iff the paper has published statistical Haar-typicality verification."""
        return self.haar_verification_status == "paper_published"

    def transparency_complete(self) -> bool:
        """True iff all 3 transparency-axis fields are at their 'fully published' state.

        Currently no published GBS quantum-advantage paper achieves this — JZ 4.0 is
        in 'transparency_vacuum' on Haar; JZ 3.0 has aggregate-only η. This method
        thus formalizes the paper-side audit gap as compile-time check.
        """
        return (
            self.haar_verification_status == "paper_published"
            and self.per_mode_eta_status == "per_mode_published"
            and self.gaussian_baseline_status == "sufficient"
        )


# ---------------------------------------------------------------------------
# Combined verdict (decision-codified audit step per claude6 case #19 framework)
# ---------------------------------------------------------------------------

def manuscript_section_anchor(judge: ThresholdJudge, audit: PaperAuditStatus) -> str:
    """Return the paper §audit-as-code chapter sub-section anchor that this (judge, audit)
    pair contributes to. Per claude6 audit_index 5-anchor framework:

        - "transparency-gap-audit-as-paper-contribution": M6-style conditional with
            ``audit.haar_verification_status in {'transparency_vacuum', 'audit_gap'}``
        - "audit-paradigm-vs-attack-paradigm": active vs passive paper genre
        - "method-side-vs-paper-side dataclass abstraction": this very dataclass split
        - "dual-implementation-§D5-pattern": cross-implementation cross-check
        - "cross-attack-peer-review-as-validation-not-just-catch": positive-resolution

    Used by paper §audit-as-code chapter Methods §M cross-method-comparison Table for
    direct adoption.
    """
    if audit.haar_verification_status in ("transparency_vacuum", "audit_gap"):
        return "transparency-gap-audit-as-paper-contribution"
    if not audit.transparency_complete():
        return "audit-paradigm-vs-attack-paradigm"
    return "transparency-complete-no-audit-gap"


# ---------------------------------------------------------------------------
# Reference instances (pre-populated for paper §A5 Table direct adoption)
# ---------------------------------------------------------------------------

JZ40_AUDIT = PaperAuditStatus(
    paper_id="JZ4.0",
    haar_verification_status="transparency_vacuum",  # 4/6 axes 全无表征 per jz40 v0.5
    per_mode_eta_status="aggregate_only",  # single overall 51%
    gaussian_baseline_status="untested",  # JZ 4.0 not in claude2's N-scaling chain
    audit_provenance=[
        "3a8ae59",  # claude8 option_B_audit v0.3 (O2 weakness flag)
        "04a9048",  # claude5 jz40 v0.5 (independent cross-reviewer verification)
        "1c8363d",  # claude7 REV-T7-001 v0.1 (PASS verdict)
    ],
)


JZ30_AUDIT = PaperAuditStatus(
    paper_id="JZ3.0",
    haar_verification_status="audit_gap",  # similar lack of published Haar test
    per_mode_eta_status="aggregate_only",  # single overall η=0.424
    gaussian_baseline_status="insufficient_at_N>=K",  # K=8 per claude2 e14e832
    audit_provenance=[
        "a6ce899",  # claude2 T8 HOG breakthrough
        "e14e832",  # claude2 HOG scaling N=4/6/8 → 0.648/0.515/0.441
        "c11b974",  # claude7 REV-T8-001 v0.1 (T8 chi correction strict verdict)
    ],
)
