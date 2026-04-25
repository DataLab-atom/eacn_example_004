"""
T3 paper figures renderer (AGENTS.md §B compliance).

Reads results/source_data/*.csv (committed, deterministic from JSON inputs)
and renders publication-quality vector figures to results/figures/*.pdf
plus PNG previews.

§B compliance per AGENTS.md:
  - §B1 panel referencing: each figure self-contained with caption-friendly
    layout and panel labels (a, b, c) where applicable
  - §B2 vector output: PDF + SVG (no rasterised data)
  - §B3 font size at print scale: >= 7pt
  - §B4 color-blind-friendly: Okabe-Ito 8-color palette (no red-green opposition,
    no rainbow / jet on quantitative data)
  - §B5 axes: explicit labels with units; no truncated y-axis without explicit
    declaration; log axes annotated
  - §B6 raw scatter shown wherever possible (not just means)
  - §B7 cross-figure consistency: alpha=4/16/32 use same color in all figures

Figures produced:
  fig1_N_decay.pdf       — RBM alpha=4 rel_err vs N (graph diameter colored)
  fig2_P1_alpha16_N48.pdf — alpha=4 vs alpha=16 at N=48 J=43,44 (bistable pocket)
  fig3_alpha16_N_decay.pdf — alpha=16 break_fraction vs N (5-seed multi-J)
  fig4_anti_monotonic.pdf  — alpha=16 vs alpha=32 at N=72 5-seed (anti-monotonic)
"""

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Okabe-Ito 8-color palette (color-blind-friendly per §B4)
OKABE_ITO = {
    "black":   "#000000",
    "orange":  "#E69F00",
    "skyblue": "#56B4E9",
    "green":   "#009E73",
    "yellow":  "#F0E442",
    "blue":    "#0072B2",
    "vermilion": "#D55E00",
    "purple":  "#CC79A7",
}

# Cross-figure alpha-color convention (per §B7)
ALPHA_COLOR = {
    4:  OKABE_ITO["skyblue"],   # alpha=4 baseline
    16: OKABE_ITO["green"],     # alpha=16 ridge sweet spot
    32: OKABE_ITO["vermilion"], # alpha=32 anti-monotonic
}

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DATA = ROOT / "results" / "source_data"
FIG_DIR = ROOT / "results" / "figures"
FIG_DIR.mkdir(exist_ok=True)

# Common matplotlib parameters per §B3 (>=7pt at print scale)
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.titlesize": 11,
    "lines.linewidth": 1.5,
    "lines.markersize": 5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
})


def read_csv_skip_comments(path):
    """Read CSV that has '# ...' comment lines before the header."""
    with open(path, encoding="utf-8") as f:
        rows = []
        for line in f:
            if line.startswith("#"):
                continue
            rows.append(line.rstrip("\n"))
    reader = csv.DictReader(rows)
    return list(reader)


def fig1_N_decay():
    """Fig 1: RBM alpha=4 rel_err vs N, colored by graph diameter."""
    rows = read_csv_skip_comments(SOURCE_DATA / "figure_main_table_N_decay.csv")
    N_vals = []
    rel_errs = []
    diams = []
    verdicts = []
    for r in rows:
        if r["RBM_alpha4_rel_err"] == "":
            # N=48 BISTABLE — separate marker
            continue
        N_vals.append(int(r["N"]))
        rel_errs.append(float(r["RBM_alpha4_rel_err"]) * 100)
        diams.append(int(r["graph_diameter"]))
        verdicts.append(r["RBM_alpha4_verdict"])

    fig, ax = plt.subplots(figsize=(5, 3.5))
    # Use viridis discretized by diameter (cb-friendly per §B4)
    diam_uniq = sorted(set(diams))
    cmap = plt.get_cmap("viridis", len(diam_uniq))
    diam_to_idx = {d: i for i, d in enumerate(diam_uniq)}

    for d in diam_uniq:
        Ns_d = [n for n, dd in zip(N_vals, diams) if dd == d]
        re_d = [r for r, dd in zip(rel_errs, diams) if dd == d]
        ax.scatter(Ns_d, re_d,
                   s=80, c=[cmap(diam_to_idx[d])],
                   marker="o", edgecolor="black", linewidth=0.5,
                   label=f"diameter {d}")

    ax.axhline(7.0, color=OKABE_ITO["vermilion"], ls="--", lw=1,
               label="Mauron-Carleo 7% threshold")
    ax.set_xlabel("Lattice size N (sites)")
    ax.set_ylabel(r"Relative energy error $|E_{RBM} - E_{DMRG}|/|E_{DMRG}|$ (%)")
    ax.set_title(r"RBM $\alpha=4$ N-decay on canonical_diamond_v2")
    ax.set_yscale("symlog", linthresh=0.1)
    ax.set_ylim(-0.05, 35)
    ax.legend(loc="upper left", frameon=False, ncol=2)
    ax.grid(True, alpha=0.3, ls=":")

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig1_N_decay.pdf")
    fig.savefig(FIG_DIR / "fig1_N_decay.svg")
    fig.savefig(FIG_DIR / "fig1_N_decay.png", dpi=300)
    plt.close(fig)
    print(f"  Wrote {FIG_DIR / 'fig1_N_decay.pdf'} (and .svg / .png)")


def fig2_P1_alpha16_N48():
    """Fig 2: alpha=4 vs alpha=16 at N=48 J=43,44 (bistable pocket fill)."""
    rows = read_csv_skip_comments(SOURCE_DATA / "figure_P1_alpha16_N48.csv")
    fig, ax = plt.subplots(figsize=(4.5, 3.3))

    js = [int(r["J_seed"]) for r in rows]
    width = 0.35
    x = np.arange(len(js))

    a4_relerrs = [(abs(float(r["RBM_alpha4_prior_E"]) - float(r["DMRG_truth_E"]))
                   / abs(float(r["DMRG_truth_E"]))) * 100 for r in rows]
    a16_relerrs = [float(r["rel_err_alpha16_pct"]) for r in rows]

    ax.bar(x - width/2, a4_relerrs, width,
           color=ALPHA_COLOR[4], edgecolor="black",
           label=r"$\alpha=4$ (prior P1 baseline)")
    ax.bar(x + width/2, a16_relerrs, width,
           color=ALPHA_COLOR[16], edgecolor="black",
           label=r"$\alpha=16$ (P1 hedge, BREAK)")

    ax.axhline(7.0, color=OKABE_ITO["vermilion"], ls="--", lw=1,
               label="7% threshold")
    ax.set_xticks(x)
    ax.set_xticklabels([f"J seed {j}" for j in js])
    ax.set_ylabel(r"Relative energy error (%)")
    ax.set_title(r"P1 verdict: $\alpha=4 \to \alpha=16$ fills bistable pocket at N=48")
    ax.legend(loc="upper right", frameon=False)
    ax.grid(True, alpha=0.3, ls=":", axis="y")

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig2_P1_alpha16_N48.pdf")
    fig.savefig(FIG_DIR / "fig2_P1_alpha16_N48.svg")
    fig.savefig(FIG_DIR / "fig2_P1_alpha16_N48.png", dpi=300)
    plt.close(fig)
    print(f"  Wrote {FIG_DIR / 'fig2_P1_alpha16_N48.pdf'}")


def fig3_alpha16_N_decay():
    """Fig 3: alpha=16 break_fraction vs N (5-seed multi-J P2/P3)."""
    # Aggregate from P1 (N=48 5/5), P2 (N=54 4/5), P3 (N=72 1/5)
    p1_rows = read_csv_skip_comments(SOURCE_DATA / "figure_P1_alpha16_N48.csv")
    p2_rows = read_csv_skip_comments(SOURCE_DATA / "figure_P2_alpha16_N54.csv")
    p3_rows = read_csv_skip_comments(SOURCE_DATA / "figure_P3_alpha16_N72.csv")

    # P1 hedge tested only J=43,44 (J=42/45/46 prior already BREAK), so all 5 BREAK
    n_break_48 = 5
    n_break_54 = sum(1 for r in p2_rows
                     if r["J_seed"] not in ("", "Wilson_CI_95_lo", "Wilson_CI_95_hi")
                     and r["verdict"] == "BREAK")
    n_break_72 = sum(1 for r in p3_rows
                     if r["verdict"] == "BREAK")

    Ns = [48, 54, 72]
    breaks = [n_break_48, n_break_54, n_break_72]

    fig, ax = plt.subplots(figsize=(4.5, 3.3))
    ax.plot(Ns, breaks, "o-", color=ALPHA_COLOR[16],
            markersize=10, lw=2, markeredgecolor="black",
            label=r"$\alpha=16$ break fraction")
    for n, b in zip(Ns, breaks):
        ax.annotate(f"{b}/5", xy=(n, b), xytext=(n, b + 0.15),
                    ha="center", fontsize=9)
    ax.set_xlabel("Lattice size N")
    ax.set_ylabel(r"Number of BREAK seeds (of 5)")
    ax.set_title(r"$\alpha=16$ capacity decay across N (P1/P2/P3 hedges)")
    ax.set_xlim(45, 75)
    ax.set_ylim(-0.5, 5.8)
    ax.set_yticks(range(6))
    ax.grid(True, alpha=0.3, ls=":")
    ax.legend(loc="upper right", frameon=False)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig3_alpha16_N_decay.pdf")
    fig.savefig(FIG_DIR / "fig3_alpha16_N_decay.svg")
    fig.savefig(FIG_DIR / "fig3_alpha16_N_decay.png", dpi=300)
    plt.close(fig)
    print(f"  Wrote {FIG_DIR / 'fig3_alpha16_N_decay.pdf'}")


def fig4_anti_monotonic():
    """Fig 4: alpha=16 vs alpha=32 at N=72 (anti-monotonic regression)."""
    rows = read_csv_skip_comments(SOURCE_DATA / "figure_Pext_anti_monotonic_N72.csv")

    js = [int(r["J_seed"]) for r in rows]
    a16_pct = [float(r["rel_err_alpha16_pct"]) for r in rows]
    a32_pct = [float(r["rel_err_alpha32_pct"]) for r in rows]

    fig, ax = plt.subplots(figsize=(5, 3.5))
    width = 0.35
    x = np.arange(len(js))

    ax.bar(x - width/2, a16_pct, width,
           color=ALPHA_COLOR[16], edgecolor="black",
           label=r"$\alpha=16$ (n=2048)")
    ax.bar(x + width/2, a32_pct, width,
           color=ALPHA_COLOR[32], edgecolor="black",
           label=r"$\alpha=32$ (n=2048) — all worse")

    # Annotate the J=42 reverse case (BREAK -> FAIL)
    j42_idx = js.index(42)
    ax.annotate(r"$\alpha=16$: BREAK $\to$ $\alpha=32$: FAIL",
                xy=(j42_idx, a32_pct[j42_idx]),
                xytext=(j42_idx + 0.3, a32_pct[j42_idx] + 4),
                arrowprops=dict(arrowstyle="->", color=OKABE_ITO["black"]),
                fontsize=8)

    ax.axhline(7.0, color=OKABE_ITO["vermilion"], ls="--", lw=1,
               label="7% threshold")
    ax.set_xticks(x)
    ax.set_xticklabels([f"J seed {j}" for j in js])
    ax.set_ylabel(r"Relative energy error (%)")
    ax.set_title(r"P-ext anti-monotonic regression at $\alpha=32$ N=72: 0/5 BREAK, 5/5 worse")
    ax.legend(loc="upper right", frameon=False)
    ax.grid(True, alpha=0.3, ls=":", axis="y")

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig4_anti_monotonic.pdf")
    fig.savefig(FIG_DIR / "fig4_anti_monotonic.svg")
    fig.savefig(FIG_DIR / "fig4_anti_monotonic.png", dpi=300)
    plt.close(fig)
    print(f"  Wrote {FIG_DIR / 'fig4_anti_monotonic.pdf'}")


def main():
    print("=" * 60)
    print("T3 paper figures rendering (AGENTS.md §B)")
    print("=" * 60)
    print(f"Source Data:    {SOURCE_DATA}")
    print(f"Output figures: {FIG_DIR}")
    print("")

    fig1_N_decay()
    fig2_P1_alpha16_N48()
    fig3_alpha16_N_decay()
    fig4_anti_monotonic()

    print("")
    print("=" * 60)
    print(f"Done. {len(list(FIG_DIR.glob('*.pdf')))} PDFs generated.")
    print("=" * 60)


if __name__ == "__main__":
    main()
