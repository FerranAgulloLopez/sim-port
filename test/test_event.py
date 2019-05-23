from unittest import TestCase

from src.Event import Event


class TestEvent(TestCase):

    def setUp(self):
        self.eventObj = Event(eventTime=5)

    def tearDown(self):
        self.eventObj = None

    def test_ge(self):
        eventObj2 = Event(eventTime=5)
        self.assertTrue(eventObj2 >= self.eventObj, "The value should be equal")
        eventObj2 = Event(eventTime=10)
        self.assertTrue(eventObj2 >= self.eventObj, "The value should be greater")

    def test_gt(self):
        eventObj2 = Event(eventTime=10)
        self.assertTrue(eventObj2 >= self.eventObj, "The value should be greater")
