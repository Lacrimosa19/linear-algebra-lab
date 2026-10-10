import unittest

from linear_algebra import Matrix, Vector
from linear_algebra.algorithms import augment, identity, solve


class LinearAlgebraTests(unittest.TestCase):
    def test_matrix_vector_product(self):
        self.assertEqual((Matrix([[2, 0], [0, 3]]) @ Vector([1, 2])).components, [2, 6])

    def test_matrix_product_and_transpose(self):
        matrix = Matrix([[1, 2], [3, 4]])
        self.assertEqual((matrix @ matrix).rows[0].components, [7, 10])
        self.assertEqual(matrix.transpose().rows[1].components, [2, 4])

    def test_helpers_and_solve_without_mutation(self):
        self.assertEqual(identity(2).shape, (2, 2))
        self.assertEqual(augment(Matrix([[1], [2]]), Matrix([[3], [4]])).shape, (2, 2))
        system = Matrix([[2, 1, 5], [1, -1, 1]])
        self.assertEqual(solve(system).components, [2.0, 1.0])
        self.assertEqual(system.rows[0].components, [2, 1, 5])


if __name__ == "__main__":
    unittest.main()
