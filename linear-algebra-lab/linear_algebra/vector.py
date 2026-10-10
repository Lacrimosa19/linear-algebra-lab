"""Vector primitives."""

from __future__ import annotations

import math
from collections.abc import Iterable


class Vector:
    """An immutable-length vector of numeric components."""

    def __init__(self, components: Iterable[float]) -> None:
        self.components = list(components)
        if not self.components:
            raise ValueError("Vector cannot be empty")

    def __repr__(self) -> str:
        return f"Vector({self.components!r})"

    def __str__(self) -> str:
        return str(self.components)

    def __len__(self) -> int:
        return len(self.components)

    def _check_length(self, other: object) -> "Vector":
        if not isinstance(other, Vector):
            raise TypeError("Operation requires another Vector")
        if len(self) != len(other):
            raise ValueError("Vectors must have the same length")
        return other

    def __add__(self, other: object) -> "Vector":
        other = self._check_length(other)
        return Vector(a + b for a, b in zip(self.components, other.components))

    def __sub__(self, other: object) -> "Vector":
        other = self._check_length(other)
        return Vector(a - b for a, b in zip(self.components, other.components))

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(component * scalar for component in self.components)

    def __rmul__(self, scalar: float) -> "Vector":
        return self * scalar

    def dot(self, other: object) -> float:
        other = self._check_length(other)
        return sum(a * b for a, b in zip(self.components, other.components))

    def magnitude(self) -> float:
        return math.sqrt(sum(component**2 for component in self.components))
