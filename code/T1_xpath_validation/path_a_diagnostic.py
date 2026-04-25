"""Path A claude4 SPD reproducibility audit (diagnoses claim vs file mismatch)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from spd_otoc_core import PauliOperator

src = open(os.path.join(os.path.dirname(__file__), "t1_spd_attack.py"), encoding='utf-8').read()
cut = src.find("# Run SPD attack")
ns = {}
exec(src[:cut], ns)
spd_evolve_circuit = ns['spd_evolve_circuit']
apply_cz_conjugation = ns['apply_cz_conjugation']
apply_single_qubit_rotation = ns['apply_single_qubit_rotation']
build_2d_grid_edges = ns['build_2d_grid_edges']

import numpy as np
print("=" * 70)
print("PATH A DIAGNOSTIC -- claude4 commit 15ffd1b reproducibility audit")
print("=" * 70)

print("\n[Test 1] As-is run: Z@q3 initial (claude4 default per script)")
for d in [2, 4, 6, 8]:
    op, h = spd_evolve_circuit(12, 3, 4, d, weight_cutoff=6, seed=42)
    norm2 = sum(abs(c)**2 for c in op.terms.values())
    print(f"  d={d}: terms={len(op.terms):4d}  max_w={h[-1]['max_weight']}  norm2={norm2:.4f}")

print("\n[Test 2] X@q3 initial -- CZ X->XZ should propagate weight")
edges = build_2d_grid_edges(3, 4)
patterns = [[], [], [], []]
for i, e in enumerate(edges):
    patterns[i % 4].append(e)

for D in [2, 4, 6]:
    op = PauliOperator.single_pauli(12, 3, 1)  # X@q3
    for d in range(D):
        for q in range(12):
            op = apply_single_qubit_rotation(op, q, seed=42 + d*12 + q)
        for q1, q2 in patterns[d % 4]:
            op = apply_cz_conjugation(op, q1, q2)
        truncated = PauliOperator(12)
        for paulis, coeff in op.terms.items():
            w = sum(1 for p in paulis if p != 0)
            if w <= 6:
                truncated.terms[paulis] = coeff
        op = truncated
    max_w = max((sum(1 for p in k if p != 0) for k in op.terms), default=0)
    norm2 = sum(abs(c)**2 for c in op.terms.values())
    print(f"  X@q3 d={D}: terms={len(op.terms):4d}  max_w={max_w}  norm2={norm2:.4f}")

print("\n[Test 3] apply_single_qubit_rotation -- Pauli-mixing audit")
op = PauliOperator.single_pauli(12, 3, 1)  # X@q3
print(f"  Before rotation: terms={len(op.terms)}  pattern={[v for v in op.terms.values()][0]}")
op2 = apply_single_qubit_rotation(op, 3, seed=0)
print(f"  After rotation:  terms={len(op2.terms)}")
print(f"  -> Rotation is phase-only; does NOT decompose SU(2)*X into X+Y+Z linear combo.")
print(f"  -> This is why initial Z@q3 stays Z forever; no Pauli mixing can occur.")

print("\n[Test 4] No-truncation run (cutoff=None): does the operator GROW at all?")
for D in [2, 4]:
    op, h = spd_evolve_circuit(12, 3, 4, D, weight_cutoff=None, seed=42)
    norm2 = sum(abs(c)**2 for c in op.terms.values())
    print(f"  Z@q3 d={D} (no cutoff): terms={len(op.terms):4d}  max_w={h[-1]['max_weight']}  norm2={norm2:.4f}")
