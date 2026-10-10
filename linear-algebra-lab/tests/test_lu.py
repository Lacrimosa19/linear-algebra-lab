import unittest

from linear_algebra import Matrix, Vector, lu_decompose, solve_lu


class LUDecompositionTests(unittest.TestCase):
    def test_decomposes_matrix_into_lower_and_upper(self):
        coefficients = Matrix([[2, 1], [4, 3]])

        lower, upper = lu_decompose(coefficients)

        self.assertEqual(lower.rows[0].components, [1.0, 0.0])
        self.assertEqual(lower.rows[1].components, [2.0, 1.0])
        self.assertEqual(upper.rows[0].components, [2, 1])
        self.assertEqual(upper.rows[1].components, [0.0, 1.0])
        self.assertEqual((lower @ upper).rows[1].components, [4.0, 3.0])

    def test_solves_by_forward_then_backward_substitution(self):
        coefficients = Matrix([[2, 1], [4, 3]])
        constants = Vector([5, 11])

        solution = solve_lu(coefficients, constants)

        self.assertEqual(solution.rows[0].components, [2.0])
        self.assertEqual(solution.rows[1].components, [1.0])
        self.assertEqual(coefficients.rows[1].components, [4, 3])

    def test_rejects_zero_pivot_without_row_exchange(self):
        with self.assertRaisesRegex(ValueError, "non-zero pivot"):
            lu_decompose(Matrix([[0, 1], [1, 1]]))

    def test_rejects_non_square_coefficient_matrix(self):
        with self.assertRaisesRegex(ValueError, "square"):
            solve_lu(Matrix([[1, 2, 3], [4, 5, 6]]), Vector([1, 2]))


if __name__ == "__main__":
    unittest.main()
