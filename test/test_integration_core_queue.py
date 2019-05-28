from unittest import TestCase

from src.Core import Core
from src.Queue import Queue


# Testing Queue functions Integration
class TestIntegrationCoreQueue(TestCase):

    def setUp(self):
        self.coreObj = Core()

    def tearDown(self):
        self.coreObj = None

    def test_can_host_entity_unlimited_not_busy_output(self):
        queueObj2 = Queue(0)
        queueObj = Queue(0)
        queueObj.addOutput(queueObj2)

        queueObj.nextArrival(0)

        self.assertEqual(queueObj.getQueueLength(), 0, "The queue must be empty")

    def test_can_host_entity_unlimited_busy_output(self):
        output_queue = Queue(1)
        output_queue.nextArrival(1)

        queueObj = Queue()
        queueObj.addOutput(output_queue)

        queueObj.nextArrival(0)

        self.assertEqual(queueObj.getQueueLength(), 1, "The queue mustn't be empty")
        self.assertEqual(queueObj.getMaxQueueLength(), 1, "The queue mustn't be empty")

    def test_can_host_entity_limited_not_busy_output(self):
        queueObj = Queue(1)

        output_queue = Queue(0)
        queueObj.addOutput(output_queue)

        queueObj.nextArrival(0)
        queueObj.nextArrival(0)
        queueObj.nextArrival(0)

        self.assertEqual(queueObj.getQueueLength(), 0, "The queue must be empty")
        self.assertEqual(queueObj.getMaxQueueLength(), 0, "The queue must be empty")

    def test_can_host_entity_limited_busy_output(self):
        queueObj = Queue(1)

        output_queue = Queue(1)
        output_queue.nextArrival(1)
        queueObj.addOutput(output_queue)

        queueObj.nextArrival(0)

        self.assertEqual(queueObj.getQueueLength(), 1, "The queue mustn't be empty")
        self.assertEqual(queueObj.getMaxQueueLength(), 1, "The queue mustn't be empty")
        try:
            queueObj.nextArrival(0)
            self.fail()
        except:
            pass

    def test_getEntity(self):
        # queue2 <-> main queue -> mock output
        queueObj = Queue(1)

        queueObj2 = Queue()
        queueObj2.addOutput(queueObj)

        output_queue = Queue(1)
        output_queue.nextArrival(1)

        queueObj.addInput(queueObj2)
        queueObj.addOutput(output_queue)

        queueObj2.nextArrival(1)
        queueObj2.nextArrival(1)

        self.assertEqual(queueObj.getQueueLength(), 1, "The queue mustn't be empty")
        self.assertEqual(queueObj2.getQueueLength(), 1, "The queue mustn't be empty")

        output_queue.maxCapacity = 2
        queueObj.getEntity(output_queue)
        output_queue.maxCapacity = 3
        queueObj.getEntity(output_queue)

        self.assertEqual(queueObj.getQueueLength(), 0, "The queue must be empty")
        self.assertEqual(queueObj2.getQueueLength(), 0, "The queue must be empty")
