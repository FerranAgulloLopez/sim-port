import unittest

from src.Auxiliary import Auxiliary


class TestAuxiliaryClass(unittest.TestCase):
    def setUp(self):
        self.auxObj = Auxiliary()

    def tearDown(self):
        self.auxObj = None

    def assert_with_number(self, arr, i, o):
        tmp = self.auxObj.binarySearch(arr, 0, len(arr), i)
        self.assertEqual(tmp, o, "The number returned must be " + str(o))

    def test_normal_binarySearch(self):
        arr = [0, 3, 6]
        tmp = self.auxObj.binarySearch(arr, 0, len(arr), 0)
        self.assertEqual(tmp, 0, "The number returned must be " + str(0))
        tmp = self.auxObj.binarySearch(arr, 0, len(arr), 3)
        self.assertEqual(tmp, 1, "The number returned must be " + str(1))
        tmp = self.auxObj.binarySearch(arr, 0, len(arr), 6)
        self.assertEqual(tmp, 2, "The number returned must be " + str(2))

    def test_inside_binarySearch(self):
        arr = [0, 3, 6]
        self.assert_with_number(arr, 1, 0)
        self.assert_with_number(arr, 2, 0)
        self.assert_with_number(arr, 4, 1)
        self.assert_with_number(arr, 5, 1)
        self.assert_with_number(arr, 7, 2)
        self.assert_with_number(arr, 8, 2)


if __name__ == "main":
    unittest.main()
