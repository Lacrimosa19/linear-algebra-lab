"""A small LU decomposition solver."""

from ..matrix import Matrix
from ..vector import Vector


def decompose(matrix):
    """Return L and U such that matrix = L @ U."""
    size = matrix.row_count
    if size != matrix.column_count:
        raise ValueError("LU decomposition requires a square matrix")

    # U starts as a copy of A. L records each elimination multiplier.
    upper = [row.components[:] for row in matrix.rows]
    lower = [[0] * size for _ in range(size)]

    for pivot_column in range(size):
        pivot = upper[pivot_column][pivot_column]
        if pivot == 0:
            raise ValueError("A non-zero pivot is required by this simple LU solver")

        lower[pivot_column][pivot_column] = 1

        for row in range(pivot_column + 1, size):
            multiplier = upper[row][pivot_column] / pivot
            lower[row][pivot_column] = multiplier

            # R_row = R_row - multiplier * R_pivot
            for column in range(pivot_column, size):
                upper[row][column] -= multiplier * upper[pivot_column][column]

    return Matrix(lower), Matrix(upper)


def solve(coefficients, constants):
    """Solve A @ x = b and return x as a one-column Matrix."""
    size = coefficients.row_count
    if size != coefficients.column_count:
        raise ValueError("Coefficient matrix must be square")
    if len(constants) != size:
        raise ValueError("Coefficient matrix and constants do not match")

    lower, upper = decompose(coefficients)

    # Forward substitution: L @ y = b
    y = [0] * size
    for row in range(size):
        y[row] = constants.components[row]
        for column in range(row):
            y[row] -= lower.rows[row].components[column] * y[column]

    # Back substitution: U @ x = y
    x = [0] * size
    for row in range(size - 1, -1, -1):
        x[row] = y[row]
        for column in range(row + 1, size):
            x[row] -= upper.rows[row].components[column] * x[column]
        x[row] /= upper.rows[row].components[row]

    return Matrix([[value] for value in x])
