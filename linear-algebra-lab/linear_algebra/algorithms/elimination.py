"""Gaussian elimination for augmented linear systems."""

from ..matrix import Matrix
from ..vector import Vector


def solve(augmented: Matrix) -> Vector:
    """Solve an n-by-(n+1) augmented system using partial pivoting.

    The supplied matrix is not modified. Singular or non-square systems are
    rejected because they do not have one unique solution.
    """
    rows, columns = augmented.shape
    if columns != rows + 1:
        raise ValueError("Expected an n-by-(n+1) augmented matrix")

    data = [row.components[:] for row in augmented.rows]
    for pivot_column in range(rows):
        pivot_row = max(range(pivot_column, rows), key=lambda row: abs(data[row][pivot_column]))
        if data[pivot_row][pivot_column] == 0:
            raise ValueError("System has no unique solution")
        data[pivot_column], data[pivot_row] = data[pivot_row], data[pivot_column]

        pivot = data[pivot_column][pivot_column]
        for row in range(pivot_column + 1, rows):
            factor = data[row][pivot_column] / pivot
            for column in range(pivot_column, columns):
                data[row][column] -= factor * data[pivot_column][column]

    solution = [0.0] * rows
    for row in range(rows - 1, -1, -1):
        remainder = data[row][-1] - sum(data[row][column] * solution[column] for column in range(row + 1, rows))
        solution[row] = remainder / data[row][row]
    return Vector(solution)
