from unittest import TestCase


class TestIntegrationCoreProcessor(TestCase):
    def setUp(self):
        #self.coreObj = Core()

    def tearDown(self):
        #self.coreObj = None

    def test_can_host_entity_unlimited_not_busy_output(self):
        """queueObj2 = Queue(0)
        queueObj = Queue(0)
        queueObj.addOutput(queueObj2)

        queueObj.nextArrival(0)

        self.assertEqual(queueObj.getQueueLength(), 0, "The queue must be empty")"""