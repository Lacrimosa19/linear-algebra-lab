from .matrix import Matrix
from .vector import Vector
from .algorithms.elimination import solve as solve_augmented


def solve(coefficients: Matrix, constants: Vector) -> Vector:
    """求解 A x = b，返回唯一解 x。"""

    if coefficients.row_count != len(constants):
        raise ValueError("方程个数必须与常数项数量一致")

    augmented = Matrix(
        row.components + [constant]
        for row, constant in zip(coefficients.rows, constants.components)
    )

    return solve_augmented(augmented)