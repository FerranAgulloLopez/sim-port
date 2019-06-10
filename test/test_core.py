from unittest import TestCase
from unittest.mock import MagicMock

from src.Constants import Constants
from src.Core import Core
from src.Event import Event
from src.Parameters import Parameters


class TestCore(TestCase):

    def setUp(self):
        self.coreObj = Core()

    def tearDown(self):
        self.coreObj = None

    def test_increaseEntitiesSystem(self):
        self.assertEqual(self.coreObj.entitiesSystem, 0, "The core should not have any entity")
        self.coreObj.increaseEntitiesSystem()
        self.assertEqual(self.coreObj.entitiesSystem, 1, "The core should have 1 entity")

    def test_decreaseEntitiesSystem(self):
        self.coreObj.increaseEntitiesSystem()
        self.assertEqual(self.coreObj.entitiesSystem, 1, "The core should have 1 entity")
        self.coreObj.decreaseEntitiesSystem()
        self.assertEqual(self.coreObj.entitiesSystem, 0, "The core should not have any entity")

    def test_run(self):
        mock_event = Event()
        mock_event.executeEvent = MagicMock()
        mock_event.eventName = MagicMock(return_value="Test")
        mock_event.eventScheduled = MagicMock(return_value=Constants.SIMULATION_INITIAL_TIME)
        mock_event.eventTime = Constants.SIMULATION_INITIAL_TIME + 123

        # eventsList is a Priority Queue
        self.coreObj.logEvent = MagicMock()
        self.coreObj.eventsList.put(mock_event)
        self.coreObj.updateState(mock_event)

        self.assertEqual(self.coreObj.currentTime, Constants.SIMULATION_INITIAL_TIME + 123,
                         "The current time should be updated to SIMULATION_INITIAL_TIME + 123")

    def test_updateState_No_Processors(self):
        mock_event = Event()
        mock_event.executeEvent = MagicMock()
        mock_event.eventTime = Constants.SIMULATION_INITIAL_TIME + 123

        self.coreObj.updateState(mock_event)

        self.assertEqual(self.coreObj.currentTime, Constants.SIMULATION_INITIAL_TIME + 123,
                         "The current time should be updated to SIMULATION_INITIAL_TIME + 123")

    def test_updateState_With_2Idle_Processors(self):
        param = Parameters()
        param.num_processors = 2
        self.coreObj = Core(param)
        for mock_processor in self.coreObj.processors:
            mock_processor.isIdle = MagicMock(return_value=True)

        mock_event = Event()
        mock_event.executeEvent = MagicMock()
        mock_event.eventTime = Constants.SIMULATION_INITIAL_TIME + 123

        self.coreObj.updateState(mock_event)

        self.assertEqual(self.coreObj.currentTime, Constants.SIMULATION_INITIAL_TIME + 123,
                         "The current time should be updated to SIMULATION_INITIAL_TIME + 123")
        self.assertEqual(self.coreObj.idleProcessors, 123 * 2, "The idle time should be 123 * 2 (2 idle processors)")
        self.assertEqual(self.coreObj.serviceProcessors, 0, "The service processors time should be 0")

    def test_updateState_With_2Service_Processors(self):
        print(self.coreObj.eventsList)
        param = Parameters()
        param.num_processors = 2
        self.coreObj = Core(param)
        print(self.coreObj.eventsList)
        print("LONGITUD", len(self.coreObj.processors))

        for mock_processor in self.coreObj.processors:
            mock_processor.isIdle = MagicMock(return_value=False)

        mock_event = Event()
        mock_event.executeEvent = MagicMock()
        mock_event.eventTime = Constants.SIMULATION_INITIAL_TIME + 123

        self.coreObj.updateState(mock_event)

        self.assertEqual(self.coreObj.currentTime, Constants.SIMULATION_INITIAL_TIME + 123,
                         "The current time should be updated to SIMULATION_INITIAL_TIME + 123")
        self.assertEqual(self.coreObj.serviceProcessors, 123 * 2,
                         "The service processors time should be 123 * 2 (2 service processors)")
        self.assertEqual(self.coreObj.idleProcessors, 0, "The idle time should be 0")

    def test_updateState_Not_First_Shift(self):
        print(self.coreObj.eventsList)
        param = Parameters()
        param.num_processors = 2
        self.coreObj = Core(param)

        for mock_processor in self.coreObj.processors:
            mock_processor.isIdle = MagicMock(return_value=False)

        mock_event = Event()
        mock_event.executeEvent = MagicMock()
        mock_event.eventTime = Constants.SIMULATION_INITIAL_TIME + 1*3600 + 1

        self.coreObj.updateState(mock_event)

        mock_event = Event()
        mock_event.executeEvent = MagicMock()
        mock_event.eventTime = Constants.SIMULATION_INITIAL_TIME + 5*3600 + 1

        self.coreObj.updateState(mock_event)

        self.assertEqual(self.coreObj.currentTime, Constants.SIMULATION_INITIAL_TIME + 5*3600 + 1,
                         "The current time should be updated to SIMULATION_INITIAL_TIME + 5*3600 + 1")
        print("SERVICE_PER_SHIFT", self.coreObj.service_per_shift)
        self.assertEqual(self.coreObj.serviceProcessors, (5*3600 + 1) * 2,
                         "The service processors time should be (5*3600 + 1) * 2 (2 service processors)")
        self.assertEqual(self.coreObj.idleProcessors, 0, "The idle time should be 0")
