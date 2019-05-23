from unittest import TestCase
from unittest.mock import MagicMock

from src.Core import Core
from src.Event import Event


class TestCore(TestCase):

    def setUp(self):
        self.coreObj = Core()

    def tearDown(self):
        self.coreObj = None

    def test_increaseEntitiesSystem(self):
        self.assertEquals(self.coreObj.entitiesSystem, 0, "The core should not have any entity")
        self.coreObj.increaseEntitiesSystem()
        self.assertEquals(self.coreObj.entitiesSystem, 1, "The core should have 1 entity")

    def test_decreaseEntitiesSystem(self):
        self.coreObj.increaseEntitiesSystem()
        self.assertEquals(self.coreObj.entitiesSystem, 1, "The core should have 1 entity")
        self.coreObj.decreaseEntitiesSystem()
        self.assertEquals(self.coreObj.entitiesSystem, 0, "The core should not have any entity")

    def test_executeEvent(self):
        self.fail()

    def test_run(self):
        mock_event = Event()
        mock_event.executeEvent = MagicMock()
        # eventsList is a Priority Queue
        self.coreObj.eventsList.append(1)
        self.coreObj.run()

    def test_addEvent(self):
        self.fail()

    def test_getCurrentTime(self):
        self.fail()

    def test_getCurrentShift(self):
        self.fail()

    def test_updateState(self):
        self.fail()

    def test_logHeaders(self):
        self.fail()

    def test_logEvent(self):
        self.fail()

    def test_stats(self):
        self.fail()
