"""Construction and composition helpers for matrices."""

from ..matrix import Matrix


def identity(size: int) -> Matrix:
    if size <= 0:
        raise ValueError("Identity matrix size must be positive")
    return Matrix([[1 if row == column else 0 for column in range(size)] for row in range(size)])


def augment(left: Matrix, right: Matrix) -> Matrix:
    if left.row_count != right.row_count:
        raise ValueError("Matrices must have the same number of rows")
    return Matrix(
        left_row.components + right_row.components
        for left_row, right_row in zip(left.rows, right.rows)
    )
