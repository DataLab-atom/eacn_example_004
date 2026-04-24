import importlib, sys
PKGS = ['numpy','scipy','torch','jax','jaxlib','qiskit','cirq','quimb','tenpy','cotengra',
        'strawberryfields','thewalrus','netket','pennylane','sympy','matplotlib','numba']
print(f"python={sys.version.split()[0]}  exe={sys.executable}")
for pkg in PKGS:
    try:
        m = importlib.import_module(pkg)
        v = getattr(m, '__version__', '?')
        print(f"  {pkg:20s} {v}")
    except Exception as e:
        print(f"  {pkg:20s} MISSING")
