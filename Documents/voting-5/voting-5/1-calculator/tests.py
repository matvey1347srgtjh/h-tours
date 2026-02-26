import unittest
from calc import add, substract, multiply, divide

class Tests(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(25, 50), 75)
        self.assertEqual(add(-10, 10), 0)

    def test_substract(self):
        self.assertEqual(substract(20, 10), 10)
        self.assertEqual(substract(10, -20), 30)

    def test_multiply(self):
        self.assertEqual(multiply(10000, 0), 0)
        self.assertEqual(multiply(5, 5), 25)

    def test_divide(self):
        self.assertEqual(divide(50, 5), 10)
        with self.assertRaises(ValueError):divide(10, 0)

if __name__ == '__main__': unittest.main()