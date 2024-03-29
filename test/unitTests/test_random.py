import unittest

from src.Constants import Constants
from src.Random import Random
from src.Parameters import Parameters


class TestRandom(unittest.TestCase):

    def setWithShifts(self, value):
        param = Parameters()
        param.WITH_SHIFTS = value
        self.randObj = Random()
        self.randObj.initialization()

    def setUp(self):
        self.setWithShifts(True)

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

    def test_range_of_source_increment_NO_SHIFTS(self):
        self.setWithShifts(False)
        i = self.randObj.sourceIncrement(None)
        self.assertGreater(i, 0, "The number returned must be greater than 0")

    def test_range_of_processor_increment_ENTREGA(self):
        i = self.randObj.processorIncrement(Constants.ENTREGA)
        self.assertGreaterEqual(i, Constants.MINIMUM_TIME_ENTREGA,
                                "The number returned must be greater than MINIMUM_TIME_ENTREGA")
        self.assertLessEqual(i, Constants.MAXIMUM_TIME_ENTREGA,
                             "The number returned must be lower than MAXIMUM_TIME_ENTREGA")

    def test_range_of_processor_increment_RECOGIDA(self):
        i = self.randObj.processorIncrement(Constants.RECOGIDA)
        self.assertGreaterEqual(i, Constants.MINIMUM_TIME_RECOGIDA,
                                "The number returned must be greater than MINIMUM_TIME_RECOGIDA")
        self.assertLessEqual(i, Constants.MAXIMUM_TIME_RECOGIDA,
                             "The number returned must be lower than MAXIMUM_TIME_RECOGIDA")

    def test_range_of_processor_increment_DUALES(self):
        i = self.randObj.processorIncrement(Constants.DUAL)
        self.assertGreaterEqual(i, Constants.MINIMUM_TIME_DUAL,
                                "The number returned must be greater than MINIMUM_TIME_DUAL")
        self.assertLessEqual(i, Constants.MAXIMUM_TIME_DUAL,
                             "The number returned must be lower than MAXIMUM_TIME_DUAL")

    def test_range_of_processor_increment_NO_SHIFTS(self):
        self.setWithShifts(False)
        i = self.randObj.processorIncrement(None)
        self.assertGreaterEqual(i, Constants.MINIMUM_TIME,
                                "The number returned must be greater than MINIMUM_TIME")
        self.assertLessEqual(i, Constants.MAXIMUM_TIME,
                             "The number returned must be lower than MAXIMUM_TIME")

    def test_get_num_trucks_ENTREGA(self):
        i = self.randObj.getNumTrucks(Constants.ENTREGA)
        self.assertGreaterEqual(i, Constants.MINIMUM_TRUCKS_ENTREGA,
                                "The number returned must be greater than MINIMUM_TRUCKS_ENTREGA")
        self.assertLessEqual(i, Constants.MAXIMUM_TRUCKS_ENTREGA,
                             "The number returned must be lower than MAXIMUM_TRUCKS_ENTREGA")

    def test_get_num_trucks_RECOGIDA(self):
        i = self.randObj.getNumTrucks(Constants.RECOGIDA)
        self.assertGreaterEqual(i, Constants.MINIMUM_TRUCKS_RECOGIDA,
                                "The number returned must be greater than MINIMUM_TRUCKS_RECOGIDA")
        self.assertLessEqual(i, Constants.MAXIMUM_TRUCKS_RECOGIDA,
                             "The number returned must be lower than MAXIMUM_TRUCKS_RECOGIDA")

    def test_test_get_num_trucks_DUALES(self):
        i = self.randObj.getNumTrucks(Constants.DUAL)
        self.assertGreaterEqual(i, Constants.MINIMUM_TRUCKS_DUAL,
                                "The number returned must be greater than MINIMUM_TRUCKS_DUAL")
        self.assertLessEqual(i, Constants.MAXIMUM_TRUCKS_DUAL,
                             "The number returned must be lower than MAXIMUM_TRUCKS_DUAL")

    def test_test_get_num_trucks_NO_SHIFTS(self):
        self.setWithShifts(False)
        i = self.randObj.getNumTrucks(None)
        self.assertGreaterEqual(i, Constants.MINIMUM_TRUCKS,
                                "The number returned must be greater than MINIMUM_TRUCKS")
        self.assertLessEqual(i, Constants.MAXIMUM_TRUCKS,
                             "The number returned must be lower than MAXIMUM_TRUCKS")

    def test_ensure_there_s_one_instance(self):
        rand = Random()
        assert rand is self.randObj


if __name__ == "main":
    unittest.main()
