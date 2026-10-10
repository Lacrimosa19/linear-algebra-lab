"""Record the individual steps of a simple LU solve for visualization."""

from linear_algebra import Matrix, Vector


def build_lu_steps(coefficients, constants):
    """Return snapshots for A = LU, L @ y = b, and U @ x = y.

    This module intentionally does not alter the project's LU solver.  It
    repeats the same elementary row operations only to preserve each state for
    the visualizer.
    """
    size = coefficients.row_count
    if size != coefficients.column_count:
        raise ValueError("Coefficient matrix must be square")
    if len(constants) != size:
        raise ValueError("Coefficient matrix and constants do not match")

    upper = [row.components[:] for row in coefficients.rows]
    lower = [[0] * size for _ in range(size)]
    steps = []

    def snapshot(title, operation, y=None, x=None, phase="start", pivot=None, target=None, multiplier=None, active_row=None):
        steps.append({
            "title": title,
            "operation": operation,
            "phase": phase,
            "pivot": pivot,
            "target": target,
            "multiplier": multiplier,
            "active_row": active_row,
            "lower": [row[:] for row in lower],
            "upper": [row[:] for row in upper],
            "y": None if y is None else y[:],
            "x": None if x is None else x[:],
        })

    snapshot("开始", "输入 A 和 b，准备将 A 分解为 L 和 U。")

    for pivot_column in range(size):
        pivot = upper[pivot_column][pivot_column]
        if pivot == 0:
            raise ValueError("A non-zero pivot is required by this simple LU solver")

        lower[pivot_column][pivot_column] = 1
        for row in range(pivot_column + 1, size):
            multiplier = upper[row][pivot_column] / pivot
            lower[row][pivot_column] = multiplier
            for column in range(pivot_column, size):
                upper[row][column] -= multiplier * upper[pivot_column][column]
            snapshot(
                "高斯消元",
                f"R{row + 1} = R{row + 1} - ({multiplier:g}) × R{pivot_column + 1}",
                phase="eliminate",
                pivot=(pivot_column, pivot_column),
                target=row,
                multiplier=multiplier,
            )

    snapshot("得到 L 和 U", "现在 A = L @ U。", phase="decomposed")

    y = [None] * size
    for row in range(size):
        y[row] = constants.components[row]
        for column in range(row):
            y[row] -= lower[row][column] * y[column]
        snapshot("前代：求 y", f"由第 {row + 1} 行求得 y{row + 1} = {y[row]:g}。", y=y, phase="forward", active_row=row)

    x = [None] * size
    for row in range(size - 1, -1, -1):
        x[row] = y[row]
        for column in range(row + 1, size):
            x[row] -= upper[row][column] * x[column]
        x[row] /= upper[row][row]
        snapshot("回代：求 x", f"由第 {row + 1} 行求得 x{row + 1} = {x[row]:g}。", y=y, x=x, phase="backward", active_row=row)

    return {
        "coefficients": [row.components[:] for row in coefficients.rows],
        "constants": constants.components[:],
        "steps": steps,
        "lower": Matrix(lower),
        "upper": Matrix(upper),
        "solution": Matrix([[value] for value in x]),
    }
