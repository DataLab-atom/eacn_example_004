#!/bin/bash
# T8: One-click reproduction script per AGENTS.md §F2
# Usage: bash run_all.sh
# Environment: Python 3.11+ with numpy, scipy, quimb, cotengra, thewalrus, matplotlib
set -e

echo "=== T8 Classical Simulation of Jiuzhang 3.0 — Full Reproduction ==="
echo ""

# T8 analyses
echo "[1/8] Noise budget analysis (T4 cross-reference)..."
python code/T4/noise_budget_analysis.py

echo "[2/8] T8 GBS loss analysis v2 (real parameters)..."
python code/T8/gbs_loss_analysis_v2.py

echo "[3/8] T8 eta sweep..."
python code/T8/eta_sweep.py

echo "[4/8] T8 Oh critical condition analysis..."
python code/T8/oh_critical_analysis.py

echo "[5/8] T8 Oh MPS correction analysis..."
python code/T8/oh_mps_correction.py

echo "[6/8] T8 Full 144-mode sampler..."
python code/T8/oh_full_sampler.py

echo "[7/8] T8 HOG benchmark (exact Hafnian)..."
python code/T8/hog_benchmark.py

echo "[8/8] T8 Goodman positive-P sampler..."
python code/T8/goodman_positive_p_sampler.py

echo ""
echo "=== All T8 analyses complete. Results in results/T8/ ==="
echo "=== Figures in results/T8/*.png and manuscript/Fig1_T8_main.* ==="
