import unittest

from linear_algebra import Matrix, Vector, solve


class SolverTests(unittest.TestCase):
    def test_solves_equation_from_coefficients_and_constants(self):
        coefficients = Matrix([[2, 1], [1, -1]])
        constants = Vector([5, 1])

        self.assertEqual(solve(coefficients, constants).components, [2.0, 1.0])

    def test_handles_zero_leading_pivot(self):
        coefficients = Matrix([[0, 1], [2, 3]])
        constants = Vector([1, 5])

        self.assertEqual(solve(coefficients, constants).components, [1.0, 1.0])

    def test_rejects_mismatched_equation_count(self):
        with self.assertRaisesRegex(ValueError, "方程个数"):
            solve(Matrix([[1, 2], [3, 4]]), Vector([1]))

    def test_rejects_system_without_unique_solution(self):
        with self.assertRaisesRegex(ValueError, "no unique solution"):
            solve(Matrix([[1, 1], [2, 2]]), Vector([3, 6]))


if __name__ == "__main__":
    unittest.main()
