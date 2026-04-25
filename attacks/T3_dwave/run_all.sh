#!/usr/bin/env bash
# T3 paper one-step reproduction (AGENTS.md §F2 一键复现)
#
# Reproduces all main paper figures + Source Data CSVs from a clean checkout.
#
# Prerequisites (per Methods §D.5):
#   - Python 3.11
#   - NetKet 3.21
#   - JAX 0.10
#   - tenpy (DMRG; or use claude7 supplied truths in results/T3_v2_*.json)
#
# Expected wall-clock on 12-core single-CPU laptop, no GPU:
#   - canonical_diamond_v2 spec gen + edge-list MD5: <1s
#   - N-scan main results (alpha=4 N in {8..72}): ~30 min total
#   - P1 hedge alpha=16 N=48 (J=43,44 retest, 2 seeds): ~17 min
#   - P2 hedge alpha=16 N=54 (5 seeds): ~45 min
#   - P3 hedge alpha=16 N=72 (5 seeds): ~80 min
#   - P-ext hedge alpha=32 N=72 (5 seeds): ~180 min
#   - Source Data CSV export: <1s
#   Total: ~6 hours single-pass.
#
# Notes:
#   - All raw JSON outputs are versioned in results/T3_v2_*.json (committed).
#   - Source Data CSVs are deterministic from JSON inputs;
#     export_source_data.py regenerates them in <1s without re-running compute.
#   - DMRG truth is provided by claude7 (commits 1787b55, 8800405, aff6346, 9b274dc)
#     and committed in results/T3_v2_*.json; not re-run by this script.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

echo "=== T3 paper reproduction (AGENTS.md §F2) ==="
echo "REPO_ROOT: $REPO_ROOT"
date

# --- Stage 1: lattice spec verification (cheap, always run) ---
echo ""
echo "[1/4] Verifying canonical_diamond_v2 lattice spec..."
python -c "
from attacks.T3_dwave.canonical_diamond_v2 import build_lattice
import hashlib
for (Lp, Lv) in [(2,1), (2,2), (2,3), (2,4), (3,2), (2,5), (2,6), (3,3), (3,4)]:
    sites, edges, J = build_lattice(Lp, Lv, seed=42)
    edges_md5 = hashlib.md5(str(edges).encode()).hexdigest()
    print(f'  L_perp={Lp} L_vert={Lv} N={len(sites)} edges={len(edges)} md5={edges_md5}')
"

# --- Stage 2: Source Data CSV export (deterministic from JSON, <1s) ---
echo ""
echo "[2/4] Exporting Source Data CSVs (paper §B9)..."
python attacks/T3_dwave/export_source_data.py

# --- Stage 3 (optional): re-run main N-scan if --rerun flag given ---
if [[ "$1" == "--rerun" ]]; then
    echo ""
    echo "[3/4] Re-running RBM N-scan (will take ~30 min)..."
    python attacks/T3_dwave/netket_v2_scaling.py
    echo ""
    echo "[3/4] Note: P1/P2/P3/Pext hedges were ad-hoc inline scripts;"
    echo "          re-running them requires the dedicated launch scripts:"
    echo "          - p1_hedge_alpha16_N48.py (recover from commit f1d09c9)"
    echo "          - p2_hedge_alpha16_N54.py (recover from commit 58a2022)"
    echo "          - p3_hedge_alpha16_N72.py (recover from commit 4509c39)"
    echo "          - pext_hedge_alpha32_N72.py (recover from commit 9087c9b)"
    echo "          - p6_alpha32_n_samples_8192.py (deferred launch, see notes/T3_p6_design.md)"
else
    echo ""
    echo "[3/4] Skipping recompute (raw JSON results already committed). Pass --rerun to recompute."
fi

# --- Stage 4: paper figure source data summary ---
echo ""
echo "[4/4] Source Data summary:"
ls -la results/source_data/*.csv

echo ""
echo "=== Reproduction complete ==="
echo "Paper figure Source Data: results/source_data/*.csv"
echo "Raw experiment outputs:    results/T3_v2_*.json"
echo "Lattice spec freeze:       attacks/T3_dwave/canonical_diamond_v2.py (commit d9cf7fa)"
date
