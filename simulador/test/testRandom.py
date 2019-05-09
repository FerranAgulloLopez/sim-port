import unittest

from src.Random import Random
from src.Constants import Constants


class TestRandomClass(unittest.TestCase):
    def setUp(self):
        self.randObj = Random()

    def tearDown(self):
        self.randObj = None

    def test_range_of_source_increment_ENTREGA(self):
        i = self.randObj.sourceIncrement(Constants.ENTREGA)
        self.assertGreater(i, 0, "The number returned must be greater than 0")

    def test_range_of_source_increment_RECOGIDA(self):
        i = self.randObj.sourceIncrement(Constants.RECOGIDA)
        self.assertGreater(i, 0, "The number returned must be greater than 0")

    def test_range_of_source_increment_DUALES(self):
        i = self.randObj.sourceIncrement(Constants.DUAL)
        self.assertGreater(i, 0, "The number returned must be greater than 0")

    def test_range_of_processor_increment_ENTREGA(self):
        i = self.randObj.processorIncrement(Constants.ENTREGA)
        self.assertGreater(i, Constants.MINIMUM_TIME_ENTREGA,
                        "The number returned must be greater than MINIMUM_TIME_ENTREGA")
        self.assertLess(i, Constants.MAXIMUM_TIME_ENTREGA,
                           "The number returned must be lower than MAXIMUM_TIME_ENTREGA")

    def test_range_of_processor_increment_RECOGIDA(self):
        i = self.randObj.processorIncrement(Constants.RECOGIDA)
        self.assertGreater(i, Constants.MINIMUM_TIME_RECOGIDA,
                        "The number returned must be greater than MINIMUM_TIME_RECOGIDA")
        self.assertLess(i, Constants.MAXIMUM_TIME_RECOGIDA,
                           "The number returned must be lower than MAXIMUM_TIME_RECOGIDA")

    def test_range_of_processor_increment_DUALES(self):
        i = self.randObj.processorIncrement(Constants.DUAL)
        self.assertGreater(i, Constants.MINIMUM_TIME_DUAL,
                        "The number returned must be greater than MINIMUM_TIME_DUAL")
        self.assertLess(i, Constants.MAXIMUM_TIME_DUAL,
                           "The number returned must be lower than MAXIMUM_TIME_DUAL")

    def test_get_num_trucks_ENTREGA(self):
        i = self.randObj.getNumTrucks(Constants.ENTREGA)
        self.assertGreater(i, Constants.MINIMUM_TRUCKS_ENTREGA,
                        "The number returned must be greater than MINIMUM_TRUCKS_ENTREGA")
        self.assertLess(i, Constants.MAXIMUM_TRUCKS_ENTREGA,
                           "The number returned must be lower than MAXIMUM_TRUCKS_ENTREGA")

    def test_get_num_trucks_RECOGIDA(self):
        i = self.randObj.getNumTrucks(Constants.RECOGIDA)
        self.assertGreater(i, Constants.MINIMUM_TRUCKS_RECOGIDA,
                        "The number returned must be greater than MINIMUM_TRUCKS_RECOGIDA")
        self.assertLess(i, Constants.MAXIMUM_TRUCKS_RECOGIDA,
                           "The number returned must be lower than MAXIMUM_TRUCKS_RECOGIDA")

    def test_test_get_num_trucks__DUALES(self):
        i = self.randObj.getNumTrucks(Constants.DUAL)
        self.assertGreater(i, Constants.MINIMUM_TRUCKS_DUAL,
                        "The number returned must be greater than MINIMUM_TRUCKS_DUAL")
        self.assertLess(i, Constants.MAXIMUM_TRUCKS_DUAL,
                           "The number returned must be lower than MAXIMUM_TRUCKS_DUAL")


if __name__ == "main":
    unittest.main()
