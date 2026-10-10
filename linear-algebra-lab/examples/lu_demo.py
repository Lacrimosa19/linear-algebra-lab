"""Run from the project root: python examples/lu_demo.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from linear_algebra import Matrix, Vector, lu_decompose, solve_lu


A = Matrix([[2, 1], [4, 3]])
b = Vector([5, 11])

L, U = lu_decompose(A)
x = solve_lu(A, b)

print("L:\n", L, sep="")
print("U:\n", U, sep="")
print("x:\n", x, sep="")
