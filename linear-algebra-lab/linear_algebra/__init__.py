"""Small, dependency-free linear algebra toolkit."""

from .matrix import Matrix
from .algorithms.lu import decompose as lu_decompose
from .algorithms.lu import solve as solve_lu
from .vector import Vector
from .solver import solve


__all__ = ["Matrix", "Vector", "lu_decompose", "solve", "solve_lu"]
