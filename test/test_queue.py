import unittest
from unittest.mock import MagicMock

from src.Queue import Queue


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

    def test_can_host_entity_limited_not_busy_output(self):
        self.queueObj = Queue(1)

        mock_output = Queue()
        mock_output.canHostEntity = MagicMock(return_value=True)
        mock_output.nextArrival = MagicMock()
        self.queueObj.addOutput(mock_output)

        self.queueObj.nextArrival(0)
        self.queueObj.nextArrival(0)
        self.queueObj.nextArrival(0)

        self.assertEqual(self.queueObj.getQueueLength(), 0, "The queue must be empty")
        self.assertEqual(self.queueObj.getMaxQueueLength(), 0, "The queue must be empty")

    def test_can_host_entity_limited_busy_output(self):
        self.queueObj = Queue(1)

        mock_output = Queue()
        mock_output.canHostEntity = MagicMock(return_value=False)
        mock_output.nextArrival = MagicMock()
        self.queueObj.addOutput(mock_output)

        self.queueObj.nextArrival(0)

        self.assertEqual(self.queueObj.getQueueLength(), 1, "The queue mustn't be empty")
        self.assertEqual(self.queueObj.getMaxQueueLength(), 1, "The queue mustn't be empty")
        try:
            self.queueObj.nextArrival(0)
            self.fail()
        except:
            pass

    def test_canHostEntity_unlimited_queue(self):
        self.queueObj.nextArrival(0)
        self.queueObj.nextArrival(0)
        self.queueObj.nextArrival(0)

        self.assertTrue(self.queueObj.canHostEntity(), "The queue should hold all elements")

    def test_canHostEntity_limited_queue(self):
        self.queueObj = Queue(1)
        self.queueObj.nextArrival(0)

        self.assertFalse(self.queueObj.canHostEntity(), "The queue shouldn't hold more elements")

    def test_getEntity(self):
        # def getEntity(self, outputModule)
        # queue2 <-> main queue -> mock output
        self.queueObj = Queue(1)

        queueObj2 = Queue()
        queueObj2.addOutput(self.queueObj)

        mock_output = Queue()
        mock_output.canHostEntity = MagicMock(return_value=False)
        mock_output.nextArrival = MagicMock()

        self.queueObj.addInput(queueObj2)
        self.queueObj.addOutput(mock_output)

        queueObj2.nextArrival(1)
        queueObj2.nextArrival(1)

        self.assertEqual(self.queueObj.getQueueLength(), 1, "The queue mustn't be empty")
        self.assertEqual(queueObj2.getQueueLength(), 1, "The queue mustn't be empty")

        # The exception is risen because que mock_output queue cannot host any entity
        try:
            self.queueObj.getEntity(mock_output)
        except:
            pass
        try:
            self.queueObj.getEntity(mock_output)
        except:
            pass

        self.assertEqual(self.queueObj.getQueueLength(), 0, "The queue must be empty")
        self.assertEqual(queueObj2.getQueueLength(), 0, "The queue must be empty")


if __name__ == "main":
    unittest.main()
