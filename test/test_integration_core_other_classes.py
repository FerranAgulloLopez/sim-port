from unittest import TestCase

from src.Constants import Constants
from src.Core import Core
from src.Event import Event
from src.Parameters import Parameters
from src.Source import Source


class TestIntegrationCoreProcessor(TestCase):
    def setUp(self):
        self.coreObj = Core()

    def tearDown(self):
        self.coreObj = None

    def test_startSimulation(self):
        source_obj = Source(self.coreObj)
        self.coreObj.output_file = open('./TEST.txt', "w+")
        self.coreObj.sources.append(source_obj)
        self.coreObj.startSimulation()
        self.coreObj.output_file.close()
        self.assertEquals(self.coreObj.eventsList.qsize(), 2,
                          "The length should be two: start simulation event + first event from source")
        obj = self.coreObj.eventsList
        self.assertIsNotNone(obj, "The object is not none")
        with open('./TEST.txt', "r") as read:
            self.assertNotEquals(len(read.read()), 0, "The file should not be empty")

    def test_executeEvent_Start_Simulation(self):
        source_obj = Source(self.coreObj)
        self.coreObj.output_file = open('./TEST.txt', "w+")
        self.coreObj.sources.append(source_obj)
        self.coreObj.executeEvent(Event(eventName=Constants.START_SIMULATION))
        self.coreObj.output_file.close()
        self.assertEquals(self.coreObj.eventsList.qsize(), 2,
                          "The length should be two: start simulation event + first event from source")
        obj = self.coreObj.eventsList
        self.assertIsNotNone("The object is not none", obj)
        with open('./TEST.txt', "r") as read:
            self.assertNotEquals(len(read.read()), 0, "The file should not be empty")

    def test_executeEvent_OtherEvent(self):
        source_obj = Source(self.coreObj)
        self.coreObj.output_file = open('./TEST.txt', "w+")
        self.coreObj.sources.append(source_obj)
        self.coreObj.executeEvent(Event(eventName=Constants.END_SIMULATION))
        self.coreObj.output_file.close()
        self.assertEquals(self.coreObj.eventsList.qsize(), 0,
                          "The length should be 0 because the simulation did not start")
        obj = self.coreObj.eventsList
        self.assertIsNotNone("The object is not none", obj)
        with open('./TEST.txt', "r") as read:
            self.assertEquals(len(read.read()), 0, "The file should be empty")

    def test_endSimulation(self):
        self.coreObj.output_file = open('./TEST.txt', "w+")
        self.coreObj.endSimulation()
        self.coreObj.output_file.close()
        self.assertEquals(self.coreObj.eventsList.qsize(), 0,
                          "The length should be 0 because the simulation ended")
        obj = self.coreObj.eventsList
        self.assertIsNotNone("The object is not none", obj)
        with open('./TEST.txt', "r") as read:
            self.assertNotEquals(len(read.read()), 0, "The file should not be empty")

    def test_run(self):
        param = Parameters()
        param.num_processors = 2
        self.coreObj = Core(param)
        self.coreObj.output_file = open('./TEST.txt', "w+")
        self.coreObj.parameters.output_file = "TEST"
        self.coreObj.run()
        self.coreObj.output_file.close()
        self.assertEquals(self.coreObj.eventsList.qsize(), 0,
                          "The length should be 0 because the simulation ended")
        obj = self.coreObj.eventsList
        self.assertIsNotNone("The object is not none", obj)
        with open('./TEST.stats.csv', "r") as read:
            self.assertNotEquals(len(read.read()), 0, "The file should not be empty")

    def test_getCurrentShift(self):
        source_obj = Source(self.coreObj)
        self.coreObj.sources.append(source_obj)
        self.coreObj.output_file = open('./TEST.txt', "w+")
        self.coreObj.executeEvent(Event(eventName=Constants.START_SIMULATION))
        self.coreObj.output_file.close()
        self.assertEquals(self.coreObj.getCurrentShift(), Constants.ENTREGA,
                          "The first shift should be of type ENTREGA")
