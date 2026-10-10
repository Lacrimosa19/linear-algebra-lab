"""Matrix type and fundamental matrix operations."""

from __future__ import annotations

from collections.abc import Iterable

from .vector import Vector


class Matrix:
    """A rectangular matrix stored as row vectors."""

    def __init__(self, rows: Iterable[Iterable[float] | Vector]) -> None:
        self.rows = [row if isinstance(row, Vector) else Vector(row) for row in rows]
        if not self.rows:
            raise ValueError("Matrix cannot be empty")
        column_count = len(self.rows[0])
        if any(len(row) != column_count for row in self.rows):
            raise ValueError("All rows must have the same number of columns")

    def __repr__(self) -> str:
        return f"Matrix({[row.components for row in self.rows]!r})"

    def __str__(self) -> str:
        return "\n".join(str(row) for row in self.rows)

    @property
    def shape(self) -> tuple[int, int]:
        return self.row_count, self.column_count

    @property
    def row_count(self) -> int:
        return len(self.rows)

    @property
    def column_count(self) -> int:
        return len(self.rows[0])

    def copy(self) -> "Matrix":
        return Matrix([row.components[:] for row in self.rows])

    def column(self, index: int) -> Vector:
        if not 0 <= index < self.column_count:
            raise IndexError("Column index out of range")
        return Vector(row.components[index] for row in self.rows)

    def transpose(self) -> "Matrix":
        return Matrix([self.column(index).components for index in range(self.column_count)])

    def _check_same_shape(self, other: object) -> "Matrix":
        if not isinstance(other, Matrix):
            raise TypeError("Operation requires another Matrix")
        if self.shape != other.shape:
            raise ValueError("Matrices must have the same shape")
        return other

    def __add__(self, other: object) -> "Matrix":
        other = self._check_same_shape(other)
        return Matrix(left + right for left, right in zip(self.rows, other.rows))

    def __sub__(self, other: object) -> "Matrix":
        other = self._check_same_shape(other)
        return Matrix(left - right for left, right in zip(self.rows, other.rows))

    def __mul__(self, other: object) -> "Matrix | Vector":
        if isinstance(other, Matrix):
            return self._multiply_matrix(other)
        if isinstance(other, Vector):
            return self._multiply_vector(other)
        return Matrix(row * other for row in self.rows)

    def __rmul__(self, scalar: float) -> "Matrix":
        return self * scalar  # type: ignore[return-value]

    def __matmul__(self, other: object) -> "Matrix | Vector":
        if not isinstance(other, (Matrix, Vector)):
            raise TypeError("Matrix multiplication requires a Matrix or Vector")
        return self * other

    def _multiply_vector(self, vector: Vector) -> Vector:
        if self.column_count != len(vector):
            raise ValueError("Matrix columns must match vector size")
        return Vector(row.dot(vector) for row in self.rows)

    def _multiply_matrix(self, other: "Matrix") -> "Matrix":
        if self.column_count != other.row_count:
            raise ValueError("Matrix A columns must match Matrix B rows")
        return Matrix(
            [row.dot(other.column(index)) for index in range(other.column_count)]
            for row in self.rows
        )
