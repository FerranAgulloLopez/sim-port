from unittest import TestCase

from src.Constants import Constants
from src.Core import Core
from src.Entity import Entity
from src.Event import Event
from src.Processor import Processor
from src.Queue import Queue


class TestIntegrationCoreProcessor(TestCase):
    def setUp(self):
        self.coreObj = Core()
        self.processorObj = Processor(self.coreObj)

    def tearDown(self):
        self.coreObj = None
        self.processorObj = None

    def test_isIdle(self):
        self.assertTrue(self.processorObj.isIdle(), "The processor should be idle")

    def test_isIdle_notIdle(self):
        self.processorObj.hostedEntity = 1
        self.assertFalse(self.processorObj.isIdle(), "The processor shouldn't be idle")

    def test_execute_Event_END_SERVICE(self):
        input_queue = Queue()
        self.processorObj.addInput(input_queue)
        self.processorObj.hostedEntity = 1

        self.assertFalse(self.processorObj.isIdle(), "The processor shouldn't be idle")
        self.processorObj.executeEvent(Event(eventName=Constants.END_SERVICE))
        self.assertTrue(self.processorObj.isIdle(), "The processor should be idle")

    def test_execute_Event_Another_Type_Of_Event(self):
        input_queue = Queue()
        self.processorObj.addInput(input_queue)
        self.processorObj.hostedEntity = 1

        self.assertFalse(self.processorObj.isIdle(), "The processor shouldn't be idle")
        self.processorObj.executeEvent(Event(eventName=Constants.END_SIMULATION))
        self.assertFalse(self.processorObj.isIdle(), "The processor shouldn't be idle")

    def test_endService_empty_queue(self):
        mock_input = Queue()
        self.processorObj.addInput(mock_input)
        self.processorObj.hostedEntity = 1

        self.assertFalse(self.processorObj.isIdle(), "The processor shouldn't be idle")
        self.processorObj.endService()
        self.assertTrue(self.processorObj.isIdle(), "The processor should be idle")

    def test_endService_non_empty_queue(self):
        input = Queue()
        input.addOutput(self.processorObj)
        self.processorObj.addInput(input)
        self.processorObj.hostedEntity = 1

        input.nextArrival(Entity(Constants.DUAL))

        self.assertFalse(self.processorObj.isIdle(), "The processor shouldn't be idle")
        self.processorObj.endService()
        self.assertFalse(self.processorObj.isIdle(), "The processor shouldn't be idle")
