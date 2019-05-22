from unittest import TestCase

from src.Constants import Constants
from src.Parameters import Parameters


class TestParameters(TestCase):

    def setUp(self):
        self.parametersObj = Parameters()

    def tearDown(self):
        self.parametersObj = None

    def test_getTotalTime(self):
        shift_duration = [5, 9, 2, 1]
        shift_type = [Constants.ENTREGA, Constants.ENTREGA, Constants.RECOGIDA, Constants.DUAL]
        shift_factor = 3600  # hours
        self.parametersObj.setParameters(shift_duration, shift_type, shift_factor)

        self.assertEquals(self.parametersObj.getTotalTime(Constants.ENTREGA), 14, "The delivery time should be 5 + 9")
        self.assertEquals(self.parametersObj.getTotalTime(Constants.RECOGIDA), 2, "The collection time should be 2")
        self.assertEquals(self.parametersObj.getTotalTime(Constants.DUAL), 1, "The dual time should be 1")
