import unittest

from linear_algebra import Matrix, Vector
from visualization.lu_steps import build_lu_steps


class LUVisualizationTests(unittest.TestCase):
    def test_steps_show_decomposition_and_solution(self):
        result = build_lu_steps(Matrix([[2, 1], [4, 3]]), Vector([5, 11]))

        self.assertEqual(result["lower"].rows[1].components, [2.0, 1])
        self.assertEqual(result["upper"].rows[1].components, [0.0, 1.0])
        self.assertEqual(result["solution"].rows[0].components, [2.0])
        self.assertEqual(result["solution"].rows[1].components, [1.0])
        self.assertEqual(result["steps"][0]["title"], "开始")
        self.assertEqual(result["steps"][-1]["title"], "回代：求 x")

    def test_steps_keep_input_matrix_unchanged(self):
        coefficients = Matrix([[2, 1], [4, 3]])

        build_lu_steps(coefficients, Vector([5, 11]))

        self.assertEqual(coefficients.rows[1].components, [4, 3])


if __name__ == "__main__":
    unittest.main()
