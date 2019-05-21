import unittest

from src.Queue import Queue
from unittest.mock import MagicMock


class TestQueueClass(unittest.TestCase):
    def setUp(self):
        self.queueObj = Queue()

    def tearDown(self):
        self.queueObj = None

    def test_can_host_entity_unlimited_not_busy_output(self):
        mock_output = Queue()
        mock_output.canHostEntity = MagicMock(return_value=True)
        mock_output.nextArrival = MagicMock()

        self.queueObj.addOutput(mock_output)

        self.queueObj.nextArrival(0)

        self.assertEqual(self.queueObj.getQueueLength(), 0, "The queue must be empty")
        self.assertEqual(self.queueObj.getMaxQueueLength(), 0, "The queue must be empty")

    def test_can_host_entity_unlimited_busy_output(self):
        mock_output = Queue()
        mock_output.canHostEntity = MagicMock(return_value=False)
        mock_output.nextArrival = MagicMock()

        self.queueObj.addOutput(mock_output)

        self.queueObj.nextArrival(0)

        self.assertEqual(self.queueObj.getQueueLength(), 1, "The queue mustn't be empty")
        self.assertEqual(self.queueObj.getMaxQueueLength(), 1, "The queue mustn't be empty")


if __name__ == "main":
    unittest.main()
