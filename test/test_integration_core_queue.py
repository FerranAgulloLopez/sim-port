from unittest import TestCase

from src.Core import Core
from src.Queue import Queue
from src.Source import Source


# Testing Source functions Integration
class TestIntegrationCoreQueue(TestCase):

    def setUp(self):
        self.coreObj = Core()

    def tearDown(self):
        self.coreObj = None

    def test_addOutput(self):
        source = Source(self.coreObj)
        self.assertIsNone(source.outputModule, "The output module should be empty")
        source.addOutput(Queue())
        self.assertIsNotNone(source.outputModule, "The output module shouldn't be empty")
