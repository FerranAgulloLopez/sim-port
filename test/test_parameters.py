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

    def test_getCurrentShift_Not_Edges(self):
        shift_duration = [5, 9, 2, 1]
        # 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
        # E E E E E E E E E E E  E  E  E  R  R  D
        shift_type = [Constants.ENTREGA, Constants.ENTREGA, Constants.RECOGIDA, Constants.DUAL]
        shift_factor = 3600  # hours
        self.parametersObj.setParameters(shift_duration, shift_type, shift_factor)

        self.assertEquals(self.parametersObj.getCurrentShift(Constants.SIMULATION_INITIAL_TIME + 2 * 3600),
                          Constants.ENTREGA, "The shift should be ENTREGA")
        self.assertEquals(self.parametersObj.getCurrentShift(Constants.SIMULATION_INITIAL_TIME + 7 * 3600),
                          Constants.ENTREGA,
                          "The shift should be ENTREGA")
        self.assertEquals(self.parametersObj.getCurrentShift(Constants.SIMULATION_INITIAL_TIME + 15 * 3600),
                          Constants.RECOGIDA,
                          "The shift should be RECOGIDA")
        self.assertEquals(self.parametersObj.getCurrentShift(Constants.SIMULATION_INITIAL_TIME + 17 * 3600),
                          Constants.DUAL,
                          "The shift should be DUAL")

    def test_getCurrentShift_Edges(self):
        shift_duration = [5, 9, 2, 1]
        # 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
        # E E E E E E E E E E E  E  E  E  R  R  D
        shift_type = [Constants.ENTREGA, Constants.ENTREGA, Constants.RECOGIDA, Constants.DUAL]
        shift_factor = 3600  # hours
        self.parametersObj.setParameters(shift_duration, shift_type, shift_factor)

        self.assertEquals(self.parametersObj.getCurrentShift(Constants.SIMULATION_INITIAL_TIME + 0 * 3600),
                          Constants.ENTREGA, "The shift should be ENTREGA")
        self.assertEquals(self.parametersObj.getCurrentShift(Constants.SIMULATION_INITIAL_TIME + 13 * 3600),
                          Constants.ENTREGA,
                          "The shift should be ENTREGA")
        self.assertEquals(self.parametersObj.getCurrentShift(Constants.SIMULATION_INITIAL_TIME + 14 * 3600),
                          Constants.RECOGIDA,
                          "The shift should be RECOGIDA")
        self.assertEquals(self.parametersObj.getCurrentShift(Constants.SIMULATION_INITIAL_TIME + 15 * 3600),
                          Constants.RECOGIDA,
                          "The shift should be RECOGIDA")
        self.assertEquals(self.parametersObj.getCurrentShift(Constants.SIMULATION_INITIAL_TIME + 16 * 3600),
                          Constants.DUAL,
                          "The shift should be DUAL")
