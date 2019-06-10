from unittest import TestCase

from src.Core import Core
from src.Parameters import Parameters


class TestIntegrationCoreProcessor(TestCase):
    def setUp(self):
        self.coreObj = Core()

    def tearDown(self):
        self.coreObj = None

    def test_system_with_shifts(self):
        param = Parameters()
        param.num_processors = 2
        self.coreObj = Core(param)
        self.coreObj.output_file = open('./TEST_System.txt', "w+")
        self.coreObj.parameters.output_file = "TEST_System"
        self.coreObj.run()
        self.coreObj.output_file.close()
        with open('../output/TEST_System.csv', "r") as read:
            read.readline()  # header
            line = read.readline()
            [current_time, event_name, event_scheduled, event_time, idle_proc, service_proc, num_idle_proc, buff_len,
             queue_len, entities_system] = line.split(',')
            while line:
                [current_time, event_name, event_scheduled, event_time, idle_proc, service_proc, num_idle_proc,
                 buff_len, queue_len, entities_system] = line.split(',')
                print(event_name)
                line = read.readline()
