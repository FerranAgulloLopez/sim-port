from unittest import TestCase
from unittest.mock import MagicMock

from src.Core import Core
from src.Processor import Processor
from src.Queue import Queue


class TestProcessor(TestCase):
    def setUp(self):
        mock_output = Core()
        mock_output.canHostEntity = MagicMock(return_value=True)
        mock_output.nextArrival = MagicMock()
        mock_output.decreaseEntitiesSystem = MagicMock()
        self.processorObj = Processor(mock_output)

    def tearDown(self):
        self.processorObj = None

    def test_isIdle(self):
        self.assertTrue(self.processorObj.isIdle(), "The processor should be idle")

    def test_isIdle_notIdle(self):
        self.processorObj.hostedEntity = 1
        self.assertFalse(self.processorObj.isIdle(), "The processor shouldn't be idle")

    def test_endService_empty_queue(self):
        mock_input = Queue()
        mock_input.getQueueLength = MagicMock(return_value=0)
        self.processorObj.addInput(mock_input)
        self.processorObj.hostedEntity = 1

        self.assertFalse(self.processorObj.isIdle(), "The processor shouldn't be idle")
        self.processorObj.endService()
        self.assertTrue(self.processorObj.isIdle(), "The processor should be idle")

    def test_endService_non_empty_queue(self):
        mock_input = Queue()
        mock_input.getQueueLength = MagicMock(return_value=1)
        mock_input.getEntity = MagicMock()
        self.processorObj.addInput(mock_input)
        self.processorObj.hostedEntity = 1

        self.assertFalse(self.processorObj.isIdle(), "The processor shouldn't be idle")
        self.processorObj.endService()
        self.assertFalse(self.processorObj.isIdle(), "The processor shouldn't be idle")
