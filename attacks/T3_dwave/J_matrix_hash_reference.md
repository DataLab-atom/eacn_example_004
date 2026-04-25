# T3 Diamond Lattice J Matrix Hash Reference

For reproducible cross-validation between t-VMC (claude3) and
ED/DMRG (claude7).

## Spec
- Geometry: 3D diamond cubic, A/B sublattice, FCC
- Periodic in z, open in x/y
- Connections: A→4×B at offsets (0,0,0), (-1,0,0), (0,-1,0), (0,0,-1)
- Coordination: 4 (bulk)
- Hamiltonian: H = -Σ_{(i,j)∈E} J_ij σz_i σz_j
- J spec: `np.random.RandomState(42).uniform(-1, 1, size=len(edges))`
- Edge ordering: deterministic, defined by `diamond_lattice(L_perp, L_vert)` in `fast_tVMC_benchmark.py`

## Available diamond sizes (N = 2 × L_perp² × L_vert)

| N   | L_perp | L_vert | edges | J md5 hash                       | feasibility       |
|-----|--------|--------|-------|----------------------------------|-------------------|
| 8   | 2      | 1      | 8     | 26b469e746f5ae5a3fbf8f9dfb3cab01 | ED dense          |
| 16  | 2      | 2      | 24    | 424e74310832a0b11b650fbe0342f3fb | ED dense / Lanczos|
| 18  | 3      | 1      | 22    | (compute on request)             | ED Lanczos        |
| 24  | 2      | 3      | 40    | (compute on request)             | ED Lanczos        |
| 32  | 2      | 4      | 56    | (compute on request)             | ED Lanczos border |
| 36  | 3      | 2      | 56    | (compute on request)             | DMRG              |
| 54  | 3      | 3      | 90    | 80e6499c7aad3933e7d0ea26dcef5a3c | DMRG only         |
| 64  | 4      | 2      | 112   | (compute on request)             | DMRG              |
| 128 | 4      | 4      | 224   | bcfa8eda467e97f78d260691b01d68c0 | t-VMC only        |

Note: N=27 is NOT a natural diamond size. Use cubic lattice at L=3 if
that geometry is desired (different topology).

## Reproduce hash

```python
import numpy as np, hashlib
from fast_tVMC_benchmark import diamond_lattice

L_perp, L_vert = 2, 2
N, edges = diamond_lattice(L_perp, L_vert)
J = np.random.RandomState(42).uniform(-1, 1, size=len(edges))
print(hashlib.md5(np.array_str(J).encode()).hexdigest())
# expect: 424e74310832a0b11b650fbe0342f3fb
```
