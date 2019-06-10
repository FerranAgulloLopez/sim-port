from unittest import TestCase

from src.Constants import Constants
from src.Core import Core
from src.Event import Event
from src.Source import Source


class TestIntegrationCoreProcessor(TestCase):
    def setUp(self):
        self.coreObj = Core()
        self.event = Event(eventCreator=self.coreObj)

    def tearDown(self):
        self.coreObj = None
        self.event = None

    def test_executeEvent_start_simulation_in_core(self):
        source_obj = Source(self.coreObj)
        self.coreObj.output_file = open('./TEST.txt', "w+")
        self.coreObj.sources.append(source_obj)
        self.event = Event(eventCreator=self.coreObj, eventName=Constants.START_SIMULATION)
        self.coreObj.executeEvent(self.event)
        self.coreObj.output_file.close()
        self.assertEquals(self.coreObj.eventsList.qsize(), 2,
                          "The length should be two: start simulation event + first event from source")
        obj = self.coreObj.eventsList
        self.assertIsNotNone("The object is not none", obj)
        with open('./TEST.txt', "r") as read:
            self.assertNotEquals(len(read.read()), 0, "The file should not be empty")
