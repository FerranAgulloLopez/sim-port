from unittest import TestCase

from src.Constants import Constants
from src.Core import Core
from src.Event import Event
from src.Queue import Queue
from src.Source import Source


# Testing Source functions Integration
class TestIntegrationCoreSource(TestCase):

    def setUp(self):
        self.coreObj = Core()

    def tearDown(self):
        self.coreObj = None

    def test_addOutput(self):
        source = Source(self.coreObj)
        self.assertIsNone(source.outputModule, "The output module should be empty")
        source.addOutput(Queue())
        self.assertIsNotNone(source.outputModule, "The output module shouldn't be empty")

    def test_removeOutput(self):
        source = Source(self.coreObj)
        self.assertIsNone(source.outputModule, "The output module should be empty")
        source.addOutput(Queue())
        self.assertIsNotNone(source.outputModule, "The output module shouldn't be empty")
        source.removeOutput()
        self.assertIsNone(source.outputModule, "The output module should be empty")

    def test_scheduleNextArrival(self):
        source = Source(self.coreObj)
        event = source.scheduleNextArrival()
        self.assertEqual(event.eventName, Constants.NEXT_ARRIVAL, "The returned event should be NEXT_ARRIVAL")
        self.assertEqual(event.eventScheduled, self.coreObj.currentTime,
                         "The returned event should have the same time as the core")
        self.assertGreater(event.eventTime, self.coreObj.currentTime,
                           "The returned event should have a time greater than the core")

    def test_startSimulation(self):
        source = Source(self.coreObj)
        self.assertTrue(self.coreObj.eventsList.empty(), "The list of events in the Core should be empty")
        source.startSimulation()
        self.assertFalse(self.coreObj.eventsList.empty(), "The list of events in the Core shouldn't be empty")

    def test_executeEvent_NEXT_ARRIVAL(self):
        source = Source(self.coreObj)
        source.addOutput(Queue(1))
        self.assertEqual(self.coreObj.entitiesSystem, 0,
                         "The system should not have any entity")
        event = Event(eventName=Constants.NEXT_ARRIVAL)
        source.executeEvent(event)
        self.assertEqual(self.coreObj.entitiesSystem, 1,
                         "The system should have one entity")

    def test_executeEvent_Not_NEXT_ARRIVAL(self):
        source = Source(self.coreObj)
        source.addOutput(Queue(1))
        self.assertEqual(self.coreObj.entitiesSystem, 0,
                         "The system should not have any entity")
        event = Event(eventName=Constants.END_SERVICE)
        source.executeEvent(event)
        self.assertEqual(self.coreObj.entitiesSystem, 0,
                         "The system should not have any entity")

    def test_executeEvent_None_output(self):
        source = Source(self.coreObj)
        self.assertEqual(self.coreObj.entitiesSystem, 0,
                         "The system should not have any entity")
        event = Event(eventName=Constants.NEXT_ARRIVAL)
        source.executeEvent(event)
        self.assertEqual(self.coreObj.entitiesSystem, 1,
                         "The system should have one entity")

    def test_executeEvent_Not_None_output(self):
        source = Source(self.coreObj)
        queue = Queue(1)
        source.addOutput(queue)
        self.assertEqual(len(queue.entitiesList), 0,
                         "The queue should not have any entity")
        source.nextArrival()
        self.assertEqual(len(queue.entitiesList), 1,
                         "The queue should have one entity")

    def test_executeEvent_before_SIMULATION_DURATION(self):
        source = Source(self.coreObj)
        queue = Queue(1)
        source.addOutput(queue)
        self.assertTrue(self.coreObj.eventsList.empty(), "The system should not have any entity")
        source.nextArrival()
        self.assertFalse(self.coreObj.eventsList.empty(), "The system should have one entity")

    def test_executeEvent_after_SIMULATION_DURATION(self):
        self.coreObj.currentTime = Constants.SIMULATION_DURATION
        source = Source(self.coreObj)
        queue = Queue(1)
        source.addOutput(queue)
        self.assertTrue(self.coreObj.eventsList.empty(), "The system should not have any entity")
        source.nextArrival()
        self.assertTrue(self.coreObj.eventsList.empty(), "The system should not have any entity")
