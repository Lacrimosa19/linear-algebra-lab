"""Run from the project root: python examples/basic_usage.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from linear_algebra import Matrix, Vector, solve


matrix = Matrix([[2, 0], [0, 3]])
vector = Vector([1, 2])
print(matrix @ vector)  # [2, 6]

coefficients = Matrix([[2, 1], [1, -1]])
constants = Vector([5, 1])
print(solve(coefficients, constants))  # [2.0, 1.0]
