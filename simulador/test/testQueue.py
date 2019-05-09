import unittest

from src.Queue import Queue


class TestQueueClass(unittest.TestCase):
    def setUp(self):
        self.queueObj = Queue()

    def tearDown(self):
        self.queueObj = None

    def test_can_host_entity_unlimited(self):
        self.assertTrue(self.queueObj.canHostEntity())
        self.assertTrue(self.queueObj.canHostEntity())
        self.assertTrue(self.queueObj.canHostEntity())


if __name__ == "main":
    unittest.main()
