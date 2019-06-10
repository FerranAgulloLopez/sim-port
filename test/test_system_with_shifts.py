import os
from unittest import TestCase

from src.Constants import Constants
from src.Core import Core
from src.Parameters import Parameters


class TestSystemWithShifts(TestCase):
    INTEGER_ROWS = [0, 2, 3, 4, 5, 6, 7, 8, 9]
    STRING_ROWS = [1]

    static_big_matrix = []

    @classmethod
    def process_line(cls, line):
        row = line.split(',')
        row = [tmp.split('\n')[0] for tmp in row]
        for i in cls.INTEGER_ROWS:
            row[i] = int(row[i])
        for i in cls.STRING_ROWS:
            row[i] = str(row[i])
        return row

    @classmethod
    def setUpClass(self):
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
                row = TestSystemWithShifts.process_line(line)
                self.static_big_matrix.append(row)
                line = read.readline()

    @classmethod
    def tearDownClass(self):
        self.coreObj = None
        os.remove("../output/TEST_System.csv")
        os.remove("../output/TEST_System.stats.csv")
        os.remove("./TEST_System.txt")

    def setUp(self):
        self.big_matrix = self.static_big_matrix.copy()

    def test_system_checks_start_end_simulation(self):
        first_row = self.big_matrix[:][0]
        last_row = self.big_matrix[:][-1]
        self.assertEquals(first_row[1], Constants.START_SIMULATION,
                          "The first row should be the beginning of the simulation")
        self.assertEquals(last_row[1], Constants.END_SIMULATION,
                          "The first row should be the end of the simulation")
        self.assertEquals(last_row[0] - first_row[0], Constants.SIMULATION_DURATION,
                          "The simulation should be between 6 a.m. and 20 a.m.")
