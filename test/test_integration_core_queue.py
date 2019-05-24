from unittest import TestCase

from src.Core import Core
from src.Queue import Queue


# Testing Queue functions Integration
class TestIntegrationCoreQueue(TestCase):

    def setUp(self):
        self.coreObj = Core()
        self.queueObj = Queue()

    def tearDown(self):
        self.coreObj = None
        self.queueObj = None

    def test_can_host_entity_unlimited_not_busy_output(self):
        output_queue = Queue(0)

        self.queueObj.addOutput(output_queue)

        self.queueObj.nextArrival(0)

        self.assertEqual(self.queueObj.getQueueLength(), 0, "The queue must be empty")
        self.assertEqual(self.queueObj.getMaxQueueLength(), 0, "The queue must be empty")

    def test_can_host_entity_unlimited_busy_output(self):
        output_queue = Queue(1)
        output_queue.nextArrival(1)

        self.queueObj.addOutput(output_queue)

        self.queueObj.nextArrival(0)

        self.assertEqual(self.queueObj.getQueueLength(), 1, "The queue mustn't be empty")
        self.assertEqual(self.queueObj.getMaxQueueLength(), 1, "The queue mustn't be empty")

    def test_can_host_entity_limited_not_busy_output(self):
        self.queueObj = Queue(1)

        output_queue = Queue(0)
        self.queueObj.addOutput(output_queue)

        self.queueObj.nextArrival(0)
        self.queueObj.nextArrival(0)
        self.queueObj.nextArrival(0)

        self.assertEqual(self.queueObj.getQueueLength(), 0, "The queue must be empty")
        self.assertEqual(self.queueObj.getMaxQueueLength(), 0, "The queue must be empty")

    def test_can_host_entity_limited_busy_output(self):
        self.queueObj = Queue(1)

        output_queue = Queue(1)
        output_queue.nextArrival(1)
        self.queueObj.addOutput(output_queue)

        self.queueObj.nextArrival(0)

        self.assertEqual(self.queueObj.getQueueLength(), 1, "The queue mustn't be empty")
        self.assertEqual(self.queueObj.getMaxQueueLength(), 1, "The queue mustn't be empty")
        try:
            self.queueObj.nextArrival(0)
            self.fail()
        except:
            pass

    def test_getEntity(self):
        # def getEntity(self, outputModule)
        # queueObj2 <-> queueObj -> output_queue
        self.queueObj = Queue(1)

        queueObj2 = Queue()
        queueObj2.addOutput(self.queueObj)

        output_queue = Queue(1)
        output_queue.nextArrival(1)

        self.queueObj.addInput(queueObj2)
        self.queueObj.addOutput(output_queue)

        queueObj2.nextArrival(1)
        queueObj2.nextArrival(1)

        self.assertEqual(self.queueObj.getQueueLength(), 1, "PartI: The queue queueObj mustn't be empty")
        self.assertEqual(queueObj2.getQueueLength(), 1, "PartI: The queue queueObj2 mustn't be empty")

        # The exception is risen because que output_queue queue cannot host any entity
        try:
            self.queueObj.getEntity(output_queue)
        except:
            pass
        try:
            self.queueObj.getEntity(output_queue)
        except:
            pass

        self.assertEqual(self.queueObj.getQueueLength(), 0, "PartII: The queue queueObj must be empty")
        self.assertEqual(queueObj2.getQueueLength(), 0, "PartII: The queue queueObj2 must be empty")
