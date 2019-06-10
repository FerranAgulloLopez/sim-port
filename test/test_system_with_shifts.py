import os
from unittest import TestCase

from src.Core import Core
from src.Parameters import Parameters
import numpy as np

class TestIntegrationCoreProcessor(TestCase):

    INTEGER_ROWS = [0, 2, 3, 4, 5, 6, 7, 8, 9]
    STRING_ROWS = [1]

    big_matrix = []

    def setUp(self):
        param = Parameters()
        param.num_processors = 2
        self.coreObj = Core(param)
        self.coreObj.output_file = open('./TEST_System.txt', "w+")
        self.coreObj.parameters.output_file = "TEST_System"
        self.coreObj.run()
        self.coreObj.output_file.close()

        with open('../output/TEST_System.csv', "r") as read:
            print("HEADER", read.readline())  # header
            line = read.readline()
            # [current_time, event_name, event_scheduled, event_time, idle_proc, service_proc, num_idle_proc, buff_len, queue_len, entities_system]
            while line:
                row = self.process_line(line)
                self.big_matrix.append(row)
                line = read.readline()

    def tearDown(self):
        self.coreObj = None
        os.remove("../output/TEST_System.csv")
        os.remove("../output/TEST_System.stats.csv")
        os.remove("./TEST_System.txt")

    def process_line(self, line):
        row = line.split(',')
        row = [tmp.split('\n')[0] for tmp in row]
        for i in self.INTEGER_ROWS:
            row[i] = int(row[i])
        for i in self.STRING_ROWS:
            row[i] = str(row[i])
        return row

    def test_system_with_shifts(self):
        pass
