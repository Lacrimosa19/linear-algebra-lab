"""Algorithms built on the core Matrix and Vector types."""

from .elimination import solve
from .lu import decompose as lu_decompose
from .lu import solve as solve_lu
from .operations import augment, identity

__all__ = ["augment", "identity", "lu_decompose", "solve", "solve_lu"]
